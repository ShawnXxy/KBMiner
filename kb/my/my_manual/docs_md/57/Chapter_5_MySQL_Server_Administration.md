The MySQL Server

MySQL Server (mysqld) is the main program that does most of the work in a MySQL installation. This
chapter provides an overview of MySQL Server and covers general server administration:

• Server configuration

• The data directory, particularly the mysql system database

• The server log files

• Management of multiple servers on a single machine

For additional information on administrative topics, see also:

• Chapter 6, Security

• Chapter 7, Backup and Recovery

• Chapter 16, Replication

5.1 The MySQL Server

mysqld is the MySQL server. The following discussion covers these MySQL server configuration topics:

• Startup options that the server supports. You can specify these options on the command line, through

configuration files, or both.

• Server system variables. These variables reflect the current state and values of the startup options,

some of which can be modified while the server is running.

• Server status variables. These variables contain counters and statistics about runtime operation.

• How to set the server SQL mode. This setting modifies certain aspects of SQL syntax and semantics,

for example for compatibility with code from other database systems, or to control the error handling for
particular situations.

• How the server manages client connections.

• Configuring and using IPv6 support.

• Configuring and using time zone support.

• Server-side help capabilities.

• The server shutdown process. There are performance and reliability considerations depending on the

type of table (transactional or nontransactional) and whether you use replication.

For listings of MySQL server variables and options that have been added, deprecated, or removed in
MySQL 5.7, see Section 1.4, “Server and Status Variables and Options Added, Deprecated, or Removed
in MySQL 5.7”.

Note

Not all storage engines are supported by all MySQL server binaries and
configurations. To find out how to determine which storage engines your MySQL
server installation supports, see Section 13.7.5.16, “SHOW ENGINES Statement”.

5.1.1 Configuring the Server

658

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Com_flush

Com_get_diagnostics

Com_grant

Com_group_replication_start

Com_group_replication_stop

Com_ha_close

Com_ha_open

Com_ha_read

Com_help

Com_insert

Com_insert_select

Com_install_plugin

Com_kill

Com_load

Com_lock_tables

Com_optimize

Com_preload_keys

Com_prepare_sql

Com_purge

Com_purge_before_date

Com_release_savepoint

Com_rename_table

Com_rename_user

Com_repair

Com_replace

Com_replace_select

Com_reset

Com_resignal

Com_revoke

Com_revoke_all

Com_rollback

Com_rollback_to_savepoint

Com_savepoint

Com_select

Com_set_option

Com_show_authors

Com_show_binlog_events

Com_show_binlogs

666

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Com_show_charsets

Com_show_collations

Com_show_contributors

Com_show_create_db

Com_show_create_event

Com_show_create_func

Com_show_create_proc

Com_show_create_table

Com_show_create_trigger

Com_show_create_user

Com_show_databases

Com_show_engine_logs

Com_show_engine_mutex

Com_show_engine_status

Com_show_errors

Com_show_events

Com_show_fields

Com_show_function_code

Com_show_function_status

Com_show_grants

Com_show_keys

Com_show_master_status

Com_show_ndb_status

Com_show_open_tables

Com_show_plugins

Com_show_privileges

Com_show_procedure_code

Com_show_procedure_status

Com_show_processlist

Com_show_profile

Com_show_profiles

Com_show_relaylog_events

Com_show_slave_hosts

Com_show_slave_status

Com_show_status

Com_show_storage_engines

Com_show_table_status

Com_show_tables

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

667

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Com_show_triggers

Com_show_variables

Com_show_warnings

Com_shutdown

Com_signal

Com_slave_start

Com_slave_stop

Com_stmt_close

Com_stmt_execute

Com_stmt_fetch

Com_stmt_prepare

Com_stmt_reprepare

Com_stmt_reset

Com_stmt_send_long_data

Com_truncate

Com_uninstall_plugin

Com_unlock_tables

Com_update

Com_update_multi

Com_xa_commit

Com_xa_end

Com_xa_prepare

Com_xa_recover

Com_xa_rollback

Com_xa_start

completion_typeYes

Compression

concurrent_insertYes

connect_timeoutYes

Yes

Yes

Yes

Yes

Yes

Yes

Connection_control_delay_generated

Yes
connection_control_failed_connections_threshold

Yes

Yes

connection_control_max_connection_delay

Yes

Yes

connection_control_min_connection_delay

Yes

Yes

Yes

Yes

Connection_errors_accept

Connection_errors_internal

Connection_errors_max_connections

Connection_errors_peer_address

Connection_errors_select

668

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Session

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Yes

No

Yes

Yes

No

Yes

Yes

Yes

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

ft_stopword_fileYes

gdb

general_log

Yes

Yes

general_log_fileYes

group_concat_max_len

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
group_replication_allow_local_disjoint_gtids_join

Yes

Yes

Yes
group_replication_allow_local_lower_version_join

Yes

Yes

group_replication_auto_increment_increment

Yes

Yes

Yes
group_replication_bootstrap_group
Yes

group_replication_components_stop_timeout

Yes

Yes

group_replication_compression_threshold

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_enforce_update_everywhere_checks

Yes

Yes

Yes

Yes
group_replication_exit_state_action
Yes

Yes

Yes
group_replication_flow_control_applier_threshold

Yes

Yes

Yes
group_replication_flow_control_certifier_threshold

Yes

Yes

group_replication_flow_control_mode

Yes

Yes

Yes
group_replication_force_members
Yes

group_replication_group_name

Yes

Yes

group_replication_group_seeds

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_gtid_assignment_block_size

Yes

Yes

Yes

group_replication_ip_whitelist

Yes

Yes

Yes
group_replication_local_address

Yes

Yes
group_replication_member_weight
Yes

Yes
group_replication_poll_spin_loops
Yes

group_replication_primary_member

group_replication_recovery_complete_at

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_recovery_reconnect_interval

Yes

Yes

Yes

group_replication_recovery_retry_count

Yes

Yes

Yes
group_replication_recovery_ssl_ca
Yes

group_replication_recovery_ssl_capath

Yes

Yes

Yes
group_replication_recovery_ssl_cert

Yes

group_replication_recovery_ssl_cipher

Yes

Yes

Yes
group_replication_recovery_ssl_crl
Yes

group_replication_recovery_ssl_crlpath

Yes

Yes

Yes
group_replication_recovery_ssl_key

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
group_replication_recovery_ssl_verify_server_cert

Yes

Yes

Yes
group_replication_recovery_use_ssl

Yes

group_replication_single_primary_mode

Yes

Yes

Yes

Yes

Global

No

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

671

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

group_replication_ssl_mode

Yes

Yes

Yes
group_replication_start_on_boot

Yes

group_replication_transaction_size_limit

Yes

Yes

Yes

Yes

Yes

Yes
group_replication_unreachable_majority_timeout

Yes

Yes

gtid_executed

Yes
gtid_executed_compression_period

Yes

gtid_mode

Yes

Yes

gtid_next

gtid_owned

gtid_purged

Handler_commit

Handler_delete

Handler_discover

Handler_external_lock

Handler_mrr_init

Handler_prepare

Handler_read_first

Handler_read_key

Handler_read_last

Handler_read_next

Handler_read_prev

Handler_read_rnd

Handler_read_rnd_next

Handler_rollback

Handler_savepoint

Handler_savepoint_rollback

Handler_update

Handler_write

have_compress

have_crypt

have_dynamic_loading

have_geometry

have_openssl

have_profiling

have_query_cache

have_rtree_keys

have_ssl

have_statement_timeout

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

672

Global

Global

Global

Global

Varies

Global

Global

Session

Both

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

No

Yes

Varies

Yes

No

Yes

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

have_symlink

help

Yes

host_cache_sizeYes

hostname

identity

ignore_builtin_innodb

Yes

ignore-db-dir Yes

ignore_db_dirs

init_connect

init_file

init_slave

initialize

initialize-
insecure

innodb

Yes

Yes

Yes

Yes

Yes

Yes

innodb_adaptive_flushing

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_adaptive_flushing_lwm

Yes

Yes

innodb_adaptive_hash_index

Yes

Yes

Yes
innodb_adaptive_hash_index_parts

Yes

Yes
innodb_adaptive_max_sleep_delay
Yes

innodb_api_bk_commit_interval

Yes

Yes

innodb_api_disable_rowlock

Yes

Yes

innodb_api_enable_binlog

Yes

innodb_api_enable_mdl

Yes

innodb_api_trx_level

Yes

Yes

Yes

Yes

innodb_autoextend_increment

Yes

Yes

innodb_autoinc_lock_mode

Yes

Yes

Innodb_available_undo_logs

innodb_background_drop_list_empty

Yes

Yes

Innodb_buffer_pool_bytes_data

Innodb_buffer_pool_bytes_dirty

innodb_buffer_pool_chunk_size

Yes

Yes

innodb_buffer_pool_dump_at_shutdown

Yes

Yes

innodb_buffer_pool_dump_now

Yes

Yes

innodb_buffer_pool_dump_pct

Yes

Yes

Innodb_buffer_pool_dump_status

innodb_buffer_pool_filename

Yes

Yes

innodb_buffer_pool_instances

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

No

Global

Global

Session

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

No

Yes

No

No

Yes

No

Yes

Yes

Yes

Yes

No

Yes

Yes

No

No

No

Yes

Yes

No

No

Yes

No

No

No

Yes

Yes

Yes

No

Yes

No

673

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Yes

Yes

Yes

innodb_buffer_pool_load_abort

Yes

Yes

Yes
innodb_buffer_pool_load_at_startup

Yes

innodb_buffer_pool_load_now

Yes

Yes

Innodb_buffer_pool_load_status

Innodb_buffer_pool_pages_data

Innodb_buffer_pool_pages_dirty

Innodb_buffer_pool_pages_flushed

Innodb_buffer_pool_pages_free

Innodb_buffer_pool_pages_latched

Innodb_buffer_pool_pages_misc

Innodb_buffer_pool_pages_total

Innodb_buffer_pool_read_ahead

Innodb_buffer_pool_read_ahead_evicted

Innodb_buffer_pool_read_ahead_rnd

Innodb_buffer_pool_read_requests

Innodb_buffer_pool_reads

Innodb_buffer_pool_resize_status

innodb_buffer_pool_size

Yes

Yes

Yes

Innodb_buffer_pool_wait_free

Innodb_buffer_pool_write_requests

Yes
innodb_change_buffer_max_size

Yes

innodb_change_buffering

Yes

Yes

Yes
innodb_change_buffering_debug

Yes

innodb_checksum_algorithm

Yes

Yes

innodb_checksumsYes

Yes

Yes
innodb_cmp_per_index_enabled

Yes

innodb_commit_concurrency

Yes

Yes

innodb_compress_debug

Yes

Yes

innodb_compression_failure_threshold_pct

Yes

Yes

innodb_compression_level

Yes

Yes

Yes
innodb_compression_pad_pct_max

Yes

innodb_concurrency_tickets

Yes

innodb_data_file_path

Yes

Innodb_data_fsyncs

Yes

Yes

innodb_data_home_dir

Yes

Yes

Innodb_data_pending_fsyncs

Innodb_data_pending_reads

Innodb_data_pending_writes

674

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

No

Yes

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Varies

No

No

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Innodb_data_read

Innodb_data_reads

Innodb_data_writes

Innodb_data_written

Innodb_dblwr_pages_written

Innodb_dblwr_writes

innodb_deadlock_detect

Yes

innodb_default_row_format

Yes

Yes

Yes

innodb_disable_resize_buffer_pool_debug

Yes

Yes

innodb_disable_sort_file_cache

Yes

Yes

innodb_doublewriteYes

innodb_fast_shutdown

Yes

Yes

Yes

Yes
innodb_fil_make_page_dirty_debug

Yes

innodb_file_formatYes

innodb_file_format_check

Yes

innodb_file_format_max

Yes

innodb_file_per_table

Yes

innodb_fill_factorYes

Yes

Yes

Yes

Yes

Yes

innodb_flush_log_at_timeout

Yes

Yes

Yes
innodb_flush_log_at_trx_commit

Yes

innodb_flush_method

Yes

innodb_flush_neighbors

Yes

innodb_flush_syncYes

innodb_flushing_avg_loops

Yes

Yes

Yes

Yes

Yes

innodb_force_load_corrupted

Yes

Yes

innodb_force_recovery

Yes

Yes

innodb_ft_aux_table

innodb_ft_cache_size

Yes

Yes

innodb_ft_enable_diag_print

Yes

Yes

innodb_ft_enable_stopword

Yes

innodb_ft_max_token_size

Yes

innodb_ft_min_token_size

Yes

Yes

Yes

Yes

innodb_ft_num_word_optimize

Yes

Yes

innodb_ft_result_cache_limit

Yes

Yes

Yes
innodb_ft_server_stopword_table
Yes

innodb_ft_sort_pll_degree

Yes

innodb_ft_total_cache_size

Yes

Yes

Yes

innodb_ft_user_stopword_table

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Both

No

No

No

No

No

No

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

No

No

Yes

No

Yes

Yes

No

No

Yes

Yes

Yes

No

No

Yes

675

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Innodb_have_atomic_builtins

innodb_io_capacityYes

innodb_io_capacity_max

Yes

innodb_large_prefixYes

Yes

Yes

Yes

innodb_limit_optimistic_insert_debug

Yes

Yes

innodb_lock_wait_timeout

Yes

Yes

Yes
innodb_locks_unsafe_for_binlog

Yes

innodb_log_buffer_size

Yes

Yes

innodb_log_checkpoint_now

Yes

Yes

innodb_log_checksums

Yes

Yes

innodb_log_compressed_pages

Yes

Yes

innodb_log_file_sizeYes

innodb_log_files_in_group

Yes

Yes

Yes

innodb_log_group_home_dir

Yes

Yes

Innodb_log_waits

innodb_log_write_ahead_size

Yes

Yes

Innodb_log_write_requests

Innodb_log_writes

innodb_lru_scan_depth

Yes

Yes

innodb_max_dirty_pages_pct

Yes

Yes

Yes
innodb_max_dirty_pages_pct_lwm
Yes

innodb_max_purge_lag

Yes

Yes

innodb_max_purge_lag_delay

Yes

Yes

innodb_max_undo_log_size

Yes

Yes

innodb_merge_threshold_set_all_debug

Yes

Yes

innodb_monitor_disable

Yes

innodb_monitor_enable

Yes

innodb_monitor_reset

Yes

innodb_monitor_reset_all

Yes

Innodb_num_open_files

innodb_numa_interleave

Yes

innodb_old_blocks_pct

Yes

innodb_old_blocks_time

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
innodb_online_alter_log_max_size
Yes

innodb_open_filesYes

Yes

innodb_optimize_fulltext_only

Yes

Yes

Innodb_os_log_fsyncs

Innodb_os_log_pending_fsyncs

676

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

No

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

No

No

No

No

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

No

Yes

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Innodb_os_log_pending_writes

Innodb_os_log_written

innodb_page_cleaners

Yes

Yes

Innodb_page_size

innodb_page_sizeYes

Yes

Innodb_pages_created

Innodb_pages_read

Innodb_pages_written

innodb_print_all_deadlocks

Yes

innodb_purge_batch_size

Yes

Yes

Yes

innodb_purge_rseg_truncate_frequency

Yes

Yes

innodb_purge_threads

Yes

Yes

innodb_random_read_ahead

Yes

Yes

innodb_read_ahead_threshold

Yes

Yes

innodb_read_io_threads

Yes

innodb_read_onlyYes

innodb_replication_delay

Yes

Yes

Yes

Yes

innodb_rollback_on_timeout

Yes

Yes

innodb_rollback_segments

Yes

Yes

Innodb_row_lock_current_waits

Innodb_row_lock_time

Innodb_row_lock_time_avg

Innodb_row_lock_time_max

Innodb_row_lock_waits

Innodb_rows_deleted

Innodb_rows_inserted

Innodb_rows_read

Innodb_rows_updated

innodb_saved_page_number_debug

Yes

Yes

innodb_sort_buffer_size

Yes

innodb_spin_wait_delay

Yes

innodb_stats_auto_recalc

Yes

Yes

Yes

Yes

innodb_stats_include_delete_marked

Yes

Yes

innodb_stats_method

Yes

innodb_stats_on_metadata

Yes

innodb_stats_persistent

Yes

Yes

Yes

Yes

innodb_stats_persistent_sample_pages

Yes

Yes

innodb_stats_sample_pages

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

No

No

No

No

No

No

No

No

Yes

Yes

Yes

No

Yes

Yes

No

No

Yes

No

Yes

No

No

No

No

No

No

No

No

No

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

677

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

innodb_stats_transient_sample_pages

Yes

Yes

innodb-
status-file

Yes

innodb_status_output

Yes

innodb_status_output_locks

Yes

innodb_strict_modeYes

innodb_support_xaYes

innodb_sync_array_size

Yes

innodb_sync_debugYes

innodb_sync_spin_loops

Yes

innodb_table_locksYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_temp_data_file_path

Yes

Yes

innodb_thread_concurrency

Yes

innodb_thread_sleep_delay

Yes

innodb_tmpdir Yes

Yes

Yes

Yes

Innodb_truncated_status_writes

innodb_trx_purge_view_update_only_debug

Yes

Yes

innodb_trx_rseg_n_slots_debug

Yes

Yes

innodb_undo_directory

Yes

innodb_undo_log_truncate

Yes

innodb_undo_logsYes

innodb_undo_tablespaces

Yes

innodb_use_native_aio

Yes

innodb_version

Yes

Yes

Yes

Yes

Yes

innodb_write_io_threads

Yes

Yes

insert_id

install

Yes

install-manual Yes

interactive_timeoutYes

Yes

Yes
internal_tmp_disk_storage_engine
Yes

join_buffer_sizeYes

keep_files_on_create

Yes

Key_blocks_not_flushed

Key_blocks_unused

Key_blocks_used

key_buffer_sizeYes

key_cache_age_threshold

Yes

key_cache_block_size

Yes

Yes

Yes

Yes

Yes

Yes

678

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Yes

Global

Global

Both

Both

Global

Global

Global

Both

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

No

No

Yes

Yes

No

Yes

Yes

Yes

No

Yes

Yes

No

Yes

Yes

No

No

No

No

Session

Yes

Both

Global

Both

Both

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

key_cache_division_limit

Yes

Yes

Yes

Key_read_requests

Key_reads

Key_write_requests

Key_writes

keyring_aws_cmk_idYes

keyring_aws_conf_file

Yes

keyring_aws_data_file

Yes

keyring_aws_regionYes

Yes

Yes

Yes

Yes

keyring_encrypted_file_data

Yes

Yes

Yes
keyring_encrypted_file_password
Yes

keyring_file_dataYes

Yes

Yes

Yes

keyring-
migration-
destination

keyring-
migration-
host

keyring-
migration-
password

keyring-
migration-port

keyring-
migration-
socket

keyring-
migration-
source

keyring-
migration-
user

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

keyring_okv_conf_dir

Yes

keyring_operations

language

Yes

large_files_support

large_page_size

Yes

Yes

large_pages Yes

Yes

last_insert_id

Last_query_cost

Last_query_partial_plans

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

No

No

No

No

Yes

No

No

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Session

Session

Session

Yes

Yes

No

No

No

No

Yes

No

No

679

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

lc_messages Yes

lc_messages_dirYes

lc_time_namesYes

license

local_infile

Yes

local-service Yes

lock_wait_timeoutYes

Locked_connects

locked_in_memory

Yes

Yes

Yes

Yes

Yes

log-bin

log_bin

Yes

Yes

log_bin_basename

log_bin_index Yes

Yes

log_bin_trust_function_creators

Yes

Yes

log_bin_use_v1_row_events

Yes

Yes

log_builtin_as_identified_by_password

Yes

Yes

log_error

Yes

log_error_verbosityYes

log-isam

log_output

Yes

Yes

Yes

Yes

Yes

Yes

log_queries_not_using_indexes

Yes

Yes

log-raw

log-short-
format

Yes

Yes

log_slave_updatesYes

Yes

Yes

Yes

log_slow_admin_statements

Yes

Yes

log_slow_slave_statements

Yes

Yes

Yes
log_statements_unsafe_for_binlog
Yes

log_syslog

Yes

log_syslog_facilityYes

log_syslog_include_pid

Yes

log_syslog_tag Yes

log-tc

log-tc-size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

log_throttle_queries_not_using_indexes

Yes

Yes

log_timestampsYes

log_warnings Yes

long_query_timeYes

Yes

Yes

Yes

680

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Global

Both

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Yes

No

Yes

No

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

No

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

low_priority_updatesYes

lower_case_file_system

lower_case_table_names

Yes

master-info-
file

Yes

master_info_repository

Yes

master-retry-
count

Yes

master_verify_checksum

Yes

max_allowed_packet

Yes

max_binlog_cache_size

Yes

max-binlog-
dump-events

Yes

max_binlog_sizeYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

max_binlog_stmt_cache_size

Yes

Yes

max_connect_errorsYes

max_connectionsYes

max_delayed_threads

Yes

max_digest_lengthYes

max_error_countYes

max_execution_timeYes

Yes

Yes

Yes

Yes

Yes

Yes

Max_execution_time_exceeded

Max_execution_time_set

Max_execution_time_set_failed

max_heap_table_size

Yes

Yes

max_insert_delayed_threads

max_join_size Yes

max_length_for_sort_data

Yes

max_points_in_geometry

Yes

max_prepared_stmt_count

Yes

max_relay_log_sizeYes

max_seeks_for_keyYes

max_sort_lengthYes

max_sp_recursion_depth

Yes

max_tmp_tables

Max_used_connections

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Max_used_connections_time

max_user_connections

Yes

max_write_lock_count

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Global

Global

Yes

No

No

Global

Yes

Global

Both

Global

Global

Global

Global

Global

Both

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Both

Both

Both

Both

Global

Global

Both

Global

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

681

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

mecab_charset

mecab_rc_file Yes

memlock

Yes

- Variable:
locked_in_memory

Yes

Yes

metadata_locks_cache_size

Yes

Yes

Yes
metadata_locks_hash_instances

Yes

min_examined_row_limit

Yes

multi_range_countYes

myisam-
block-size

Yes

myisam_data_pointer_size

Yes

myisam_max_sort_file_size

Yes

myisam_mmap_sizeYes

myisam_recover_options

Yes

myisam_repair_threads

Yes

myisam_sort_buffer_size

Yes

myisam_stats_method

Yes

myisam_use_mmapYes

mysql_firewall_mode

Yes

mysql_firewall_traceYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

mysql_native_password_proxy_users

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

mysqlx

Yes

Yes

Mysqlx_address

mysqlx_bind_address

Yes

Yes

Yes

Mysqlx_bytes_received

Mysqlx_bytes_sent

mysqlx_connect_timeout

Yes

Yes

Yes

Mysqlx_connection_accept_errors

Mysqlx_connection_errors

Mysqlx_connections_accepted

Mysqlx_connections_closed

Mysqlx_connections_rejected

Mysqlx_crud_create_view

Mysqlx_crud_delete

Mysqlx_crud_drop_view

Mysqlx_crud_find

Mysqlx_crud_insert

682

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Both

Both

Both

Global

Global

Global

Global

Global

Global

Both

Both

Global

Both

Both

Global

Global

Global

Both

Both

Both

Both

Both

No

No

No

No

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

Yes

No

No

No

No

No

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Mysqlx_crud_modify_view

Mysqlx_crud_update

Mysqlx_errors_sent

Mysqlx_errors_unknown_message_type

Mysqlx_expect_close

Mysqlx_expect_open

Yes
mysqlx_idle_worker_thread_timeout

Yes

Mysqlx_init_error

mysqlx_max_allowed_packet

Yes

Yes

mysqlx_max_connections

Yes

Yes

mysqlx_min_worker_threads

Yes

Yes

Mysqlx_notice_other_sent

Mysqlx_notice_warning_sent

Mysqlx_port

mysqlx_port

Yes

mysqlx_port_open_timeout

Yes

Yes

Yes

Mysqlx_rows_sent

Mysqlx_sessions

Mysqlx_sessions_accepted

Mysqlx_sessions_closed

Mysqlx_sessions_fatal_error

Mysqlx_sessions_killed

Mysqlx_sessions_rejected

Mysqlx_socket

Yes

Yes

Yes

Yes

Yes

Yes

mysqlx_socket Yes

Yes

Yes

Mysqlx_ssl_accept_renegotiates

Mysqlx_ssl_accepts

Mysqlx_ssl_active

mysqlx_ssl_ca Yes

mysqlx_ssl_capathYes

mysqlx_ssl_certYes

Mysqlx_ssl_cipher

mysqlx_ssl_cipherYes

Mysqlx_ssl_cipher_list

mysqlx_ssl_crl Yes

mysqlx_ssl_crlpathYes

Mysqlx_ssl_ctx_verify_depth

Mysqlx_ssl_ctx_verify_mode

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Both

Both

Global

Both

Global

Global

Global

Both

Both

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Both

Global

Both

Global

Global

Both

Both

No

No

No

No

No

No

Yes

No

Yes

Yes

Yes

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

683

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Mysqlx_ssl_finished_accepts

mysqlx_ssl_keyYes

Yes

Yes

Mysqlx_ssl_server_not_after

Mysqlx_ssl_server_not_before

Mysqlx_ssl_verify_depth

Mysqlx_ssl_verify_mode

Mysqlx_ssl_version

Mysqlx_stmt_create_collection

Mysqlx_stmt_create_collection_index

Mysqlx_stmt_disable_notices

Mysqlx_stmt_drop_collection

Mysqlx_stmt_drop_collection_index

Mysqlx_stmt_enable_notices

Mysqlx_stmt_ensure_collection

Mysqlx_stmt_execute_mysqlx

Mysqlx_stmt_execute_sql

Mysqlx_stmt_execute_xplugin

Mysqlx_stmt_kill_client

Mysqlx_stmt_list_clients

Mysqlx_stmt_list_notices

Mysqlx_stmt_list_objects

Mysqlx_stmt_ping

Mysqlx_worker_threads

Mysqlx_worker_threads_active

named_pipe Yes

Yes

named_pipe_full_access_group

Yes

Yes

ndb_allow_copying_alter_table

Yes

Yes

Yes

Yes

Yes

Ndb_api_adaptive_send_deferred_count

Ndb_api_adaptive_send_deferred_count_session

Ndb_api_adaptive_send_deferred_count_slave

Ndb_api_adaptive_send_forced_count

Ndb_api_adaptive_send_forced_count_session

Ndb_api_adaptive_send_forced_count_slave

Ndb_api_adaptive_send_unforced_count

Ndb_api_adaptive_send_unforced_count_session

Ndb_api_adaptive_send_unforced_count_slave

Ndb_api_bytes_received_count

Ndb_api_bytes_received_count_session

684

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Yes

No

No

No

No

No

No

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Ndb_api_bytes_received_count_slave

Ndb_api_bytes_sent_count

Ndb_api_bytes_sent_count_session

Ndb_api_bytes_sent_count_slave

Ndb_api_event_bytes_count

Ndb_api_event_bytes_count_injector

Ndb_api_event_data_count

Ndb_api_event_data_count_injector

Ndb_api_event_nondata_count

Ndb_api_event_nondata_count_injector

Ndb_api_pk_op_count

Ndb_api_pk_op_count_session

Ndb_api_pk_op_count_slave

Ndb_api_pruned_scan_count

Ndb_api_pruned_scan_count_session

Ndb_api_pruned_scan_count_slave

Ndb_api_range_scan_count

Ndb_api_range_scan_count_session

Ndb_api_range_scan_count_slave

Ndb_api_read_row_count

Ndb_api_read_row_count_session

Ndb_api_read_row_count_slave

Ndb_api_scan_batch_count

Ndb_api_scan_batch_count_session

Ndb_api_scan_batch_count_slave

Ndb_api_table_scan_count

Ndb_api_table_scan_count_session

Ndb_api_table_scan_count_slave

Ndb_api_trans_abort_count

Ndb_api_trans_abort_count_session

Ndb_api_trans_abort_count_slave

Ndb_api_trans_close_count

Ndb_api_trans_close_count_session

Ndb_api_trans_close_count_slave

Ndb_api_trans_commit_count

Ndb_api_trans_commit_count_session

Ndb_api_trans_commit_count_slave

Ndb_api_trans_local_read_row_count

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Session

Global

Global

Global

Global

Global

Global

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

685

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Ndb_api_trans_local_read_row_count_session

Ndb_api_trans_local_read_row_count_slave

Ndb_api_trans_start_count

Ndb_api_trans_start_count_session

Ndb_api_trans_start_count_slave

Ndb_api_uk_op_count

Ndb_api_uk_op_count_session

Ndb_api_uk_op_count_slave

Ndb_api_wait_exec_complete_count

Ndb_api_wait_exec_complete_count_session

Ndb_api_wait_exec_complete_count_slave

Ndb_api_wait_meta_request_count

Ndb_api_wait_meta_request_count_session

Ndb_api_wait_meta_request_count_slave

Ndb_api_wait_nanos_count

Ndb_api_wait_nanos_count_session

Ndb_api_wait_nanos_count_slave

Ndb_api_wait_scan_result_count

Ndb_api_wait_scan_result_count_session

Ndb_api_wait_scan_result_count_slave

Yes
ndb_autoincrement_prefetch_sz

Yes

ndb_batch_sizeYes

Yes

ndb_blob_read_batch_bytes

Yes

Yes

ndb_blob_write_batch_bytes

Yes

Yes

ndb_cache_check_time

Yes

Yes

ndb_clear_apply_status

Yes

ndb_cluster_connection_pool

Yes

Yes

ndb_cluster_connection_pool_nodeids

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Ndb_cluster_node_id

Ndb_config_from_host

Ndb_config_from_port

Ndb_conflict_fn_epoch

Ndb_conflict_fn_epoch_trans

Ndb_conflict_fn_epoch2

Ndb_conflict_fn_epoch2_trans

Ndb_conflict_fn_max

Ndb_conflict_fn_max_del_win

Ndb_conflict_fn_old

686

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Both

Both

Both

Both

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

No

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Ndb_conflict_last_conflict_epoch

Ndb_conflict_last_stable_epoch

Ndb_conflict_reflected_op_discard_count

Ndb_conflict_reflected_op_prepare_count

Ndb_conflict_refresh_op_count

Ndb_conflict_trans_conflict_commit_count

Ndb_conflict_trans_detect_iter_count

Ndb_conflict_trans_reject_count

Ndb_conflict_trans_row_conflict_count

Ndb_conflict_trans_row_reject_count

ndb-
connectstring

Yes

ndb_data_node_neighbour

Yes

ndb_default_column_format

Yes

ndb_default_column_format

Yes

ndb_deferred_constraints

Yes

ndb_deferred_constraints

Yes

ndb_distributionYes

ndb_distributionYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Ndb_epoch_delete_delete_count

ndb_eventbuffer_free_percent

Yes

Yes

ndb_eventbuffer_max_alloc

Yes

Yes

Ndb_execute_count

ndb_extra_loggingYes

ndb_force_sendYes

ndb_fully_replicatedYes

ndb_index_stat_enable

Yes

ndb_index_stat_option

Yes

ndb_join_pushdown

Yes

Yes

Yes

Yes

Yes

Ndb_last_commit_epoch_server

Ndb_last_commit_epoch_session

ndb_log_apply_status

Yes

ndb_log_apply_status

Yes

ndb_log_bin Yes

ndb_log_binlog_index

Yes

ndb_log_empty_epochs

Yes

ndb_log_empty_epochs

Yes

ndb_log_empty_update

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Session

Global

Global

Both

Global

Global

Global

Global

No

No

No

No

No

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

Yes

687

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

ndb_log_empty_update

Yes

ndb_log_exclusive_reads

Yes

ndb_log_exclusive_reads

Yes

ndb_log_fail_terminate

Yes

ndb_log_orig Yes

ndb_log_orig Yes

ndb_log_transaction_id

Yes

ndb_log_transaction_id

ndb_log_update_as_write

Yes

ndb_log_update_minimal

Yes

ndb_log_updated_only

Yes

ndb-mgmd-
host

Yes

ndb_nodeid

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Ndb_number_of_data_nodes

ndb_optimization_delay

Yes

Yes

ndb_optimized_node_selection

Yes

Yes

ndb_optimized_node_selection

Yes

Yes

Ndb_pruned_scan_count

Ndb_pushed_queries_defined

Ndb_pushed_queries_dropped

Ndb_pushed_queries_executed

Ndb_pushed_reads

ndb_read_backupYes

Yes

ndb_recv_thread_activation_threshold

Yes

Yes

ndb_recv_thread_cpu_mask

Yes

Yes

ndb_report_thresh_binlog_epoch_slip

Yes

Yes

ndb_report_thresh_binlog_mem_usage

Yes

Yes

ndb_row_checksum

Ndb_scan_count

ndb_show_foreign_key_mock_tables

Yes

Yes

ndb_slave_conflict_role

Yes

Yes

Ndb_slave_max_replicated_epoch

Ndb_system_name

ndb_table_no_logging

ndb_table_temporary

ndb-transid-
mysql-

Yes

688

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Session

Session

Yes

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

No

No

Yes

Yes

No

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

No

No

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Name
connection-
map

ndb_use_copying_alter_table

ndb_use_exact_count

ndb_use_transactions

Yes

Yes

ndb_version

ndb_version_string

ndb_wait_connectedYes

ndb_wait_setupYes

ndbcluster

Yes

ndbinfo_database

ndbinfo_max_bytesYes

ndbinfo_max_rowsYes

ndbinfo_offline

ndbinfo_show_hidden

Yes

ndbinfo_table_prefix

ndbinfo_version

net_buffer_lengthYes

net_read_timeoutYes

net_retry_countYes

net_write_timeoutYes

new

Yes

ngram_token_sizeYes

no-defaults

Yes

Not_flushed_delayed_rows

offline_mode Yes

old

Yes

old_alter_table Yes

old_passwords Yes

old-style-
user-limits

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Ongoing_anonymous_gtid_violating_transaction_count

Ongoing_anonymous_transaction_count

Ongoing_automatic_gtid_violating_transaction_count

Open_files

open_files_limitYes

Yes

Yes

Open_streams

Open_table_definitions

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Global

Global

Global

Global

Global

Both

Both

Global

Both

Global

Global

Both

Both

Both

Both

Both

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

No

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

No

No

Yes

No

Yes

Yes

No

No

No

No

No

No

No

689

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Open_tables

Opened_files

Opened_table_definitions

Opened_tables

optimizer_prune_level

Yes

optimizer_search_depth

Yes

optimizer_switchYes

optimizer_traceYes

optimizer_trace_features

Yes

optimizer_trace_limit

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
optimizer_trace_max_mem_size

Yes

optimizer_trace_offset

Yes

parser_max_mem_size

Yes

partition

Yes

performance_schema

Yes

Yes

Yes

Yes

Yes

Performance_schema_accounts_lost

performance_schema_accounts_size

Yes

Yes

Performance_schema_cond_classes_lost

Performance_schema_cond_instances_lost

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

performance-
schema-
consumer-
events-
stages-
current

performance-
schema-
consumer-
events-
stages-history

performance-
schema-
consumer-
events-
stages-
history-long

performance-
schema-
consumer-
events-
statements-
current

690

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

performance-
schema-
consumer-
events-
statements-
history

performance-
schema-
consumer-
events-
statements-
history-long

performance-
schema-
consumer-
events-
transactions-
current

performance-
schema-
consumer-
events-
transactions-
history

performance-
schema-
consumer-
events-
transactions-
history-long

performance-
schema-
consumer-
events-waits-
current

performance-
schema-
consumer-
events-waits-
history

performance-
schema-
consumer-
events-waits-
history-long

performance-
schema-
consumer-

691

Server Option, System Variable, and Status Variable Reference

Cmd-Line

Name
global-
instrumentation

Option File

System Var Status Var

Var Scope

Dynamic

Yes

Yes

performance-
schema-
consumer-
statements-
digest

Yes

Yes

performance-
schema-
consumer-
thread-
instrumentation

Performance_schema_digest_lost

Yes

Yes
performance_schema_digests_size
Yes

Yes

performance_schema_events_stages_history_long_size

Yes

Yes

Yes

Yes
performance_schema_events_stages_history_size

Yes

Yes

performance_schema_events_statements_history_long_size

Yes

Yes

Yes

performance_schema_events_statements_history_size

Yes

Yes

Yes

performance_schema_events_transactions_history_long_size

Yes

Yes

Yes

performance_schema_events_transactions_history_size

Yes

Yes

Yes

performance_schema_events_waits_history_long_size

Yes

Yes

Yes

Yes
performance_schema_events_waits_history_size

Yes

Yes

Performance_schema_file_classes_lost

Performance_schema_file_handles_lost

Performance_schema_file_instances_lost

Performance_schema_hosts_lost

Yes
performance_schema_hosts_size
Yes

Yes

Performance_schema_index_stat_lost

Yes

Yes

performance-
schema-
instrument

Performance_schema_locker_lost

Yes

Yes

Yes

Yes

Yes

Yes

performance_schema_max_cond_classes

Yes

Yes

performance_schema_max_cond_instances

Yes

Yes

performance_schema_max_digest_length

Yes

Yes

performance_schema_max_file_classes

Yes

Yes

performance_schema_max_file_handles

Yes

Yes

performance_schema_max_file_instances

Yes

Yes

performance_schema_max_index_stat

Yes

Yes

performance_schema_max_memory_classes

Yes

Yes

performance_schema_max_metadata_locks

Yes

Yes

692

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

performance_schema_max_mutex_classes

Yes

Yes

performance_schema_max_mutex_instances

Yes

Yes

Yes

Yes

performance_schema_max_prepared_statements_instances

Yes

Yes

Yes

performance_schema_max_program_instances

Yes

Yes

Yes

performance_schema_max_rwlock_classes

Yes

Yes

performance_schema_max_rwlock_instances

Yes

Yes

performance_schema_max_socket_classes

Yes

Yes

Yes

Yes

Yes

performance_schema_max_socket_instances

Yes

Yes

Yes

performance_schema_max_sql_text_length

Yes

Yes

performance_schema_max_stage_classes

Yes

Yes

Yes

Yes

performance_schema_max_statement_classes

Yes

Yes

Yes

performance_schema_max_statement_stack

Yes

Yes

performance_schema_max_table_handles

Yes

Yes

performance_schema_max_table_instances

Yes

Yes

performance_schema_max_table_lock_stat

Yes

Yes

performance_schema_max_thread_classes

Yes

Yes

performance_schema_max_thread_instances

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Performance_schema_memory_classes_lost

Performance_schema_metadata_lock_lost

Performance_schema_mutex_classes_lost

Performance_schema_mutex_instances_lost

Performance_schema_nested_statement_lost

Performance_schema_prepared_statements_lost

Performance_schema_program_lost

Performance_schema_rwlock_classes_lost

Performance_schema_rwlock_instances_lost

Performance_schema_session_connect_attrs_lost

Yes
performance_schema_session_connect_attrs_size

Yes

Yes

performance_schema_setup_actors_size

Yes

Yes

performance_schema_setup_objects_size

Yes

Yes

performance_schema_show_processlist

Yes

Yes

Yes

Yes

Yes

Performance_schema_socket_classes_lost

Performance_schema_socket_instances_lost

Performance_schema_stage_classes_lost

Performance_schema_statement_classes_lost

Performance_schema_table_handles_lost

Performance_schema_table_instances_lost

Performance_schema_table_lock_stat_lost

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Yes

No

No

No

No

No

No

No

693

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Performance_schema_thread_classes_lost

Performance_schema_thread_instances_lost

Performance_schema_users_lost

Yes
performance_schema_users_size
Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

pid_file

plugin_dir

plugin-load

plugin-load-
add

plugin-xxx

port

port-open-
timeout

Yes

Yes

Yes

Yes

Yes

Yes

Yes

preload_buffer_sizeYes

Prepared_stmt_count

print-defaults Yes

profiling

profiling_history_size

Yes

Yes

protocol_version

proxy_user

pseudo_slave_mode

pseudo_thread_id

Qcache_free_blocks

Qcache_free_memory

Qcache_hits

Qcache_inserts

Qcache_lowmem_prunes

Qcache_not_cached

Qcache_queries_in_cache

Qcache_total_blocks

Queries

query_alloc_block_size

Yes

query_cache_limitYes

query_cache_min_res_unit

Yes

query_cache_sizeYes

query_cache_typeYes

Yes

Yes

Yes

Yes

Yes

query_cache_wlock_invalidate

Yes

Yes

query_prealloc_sizeYes

Yes

694

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

No

No

No

No

No

No

Global

No

Both

Global

Both

Both

Global

Session

Session

Session

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Both

Both

Both

Yes

No

Yes

Yes

No

No

Yes

Yes

No

No

No

No

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Questions

rand_seed1

rand_seed2

range_alloc_block_size

Yes

Yes

Yes
range_optimizer_max_mem_size

Yes

rbr_exec_mode

read_buffer_sizeYes

read_only

Yes

read_rnd_buffer_size

Yes

relay_log

Yes

relay_log_basename

relay_log_indexYes

relay_log_info_fileYes

relay_log_info_repository

Yes

relay_log_purgeYes

relay_log_recoveryYes

relay_log_space_limit

Yes

remove

replicate-do-
db

replicate-do-
table

replicate-
ignore-db

replicate-
ignore-table

replicate-
rewrite-db

replicate-
same-server-
id

replicate-wild-
do-table

replicate-wild-
ignore-table

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

replication_optimize_for_static_plugin_config

Yes

Yes

replication_sender_observe_commit_only

Yes

Yes

report_host

Yes

report_passwordYes

report_port

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Session

Session

Both

Both

Session

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

Yes

Yes

No

No

Global

Global

Global

Global

Global

Yes

Yes

No

No

No

695

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

report_user

Yes

require_secure_transport

Yes

Yes

Yes

rewriter_enabled

Rewriter_number_loaded_rules

Rewriter_number_reloads

Rewriter_number_rewritten_queries

Rewriter_reload_error

rewriter_verbose

Rpl_semi_sync_master_clients

rpl_semi_sync_master_enabled

Yes

Yes

Rpl_semi_sync_master_net_avg_wait_time

Rpl_semi_sync_master_net_wait_time

Rpl_semi_sync_master_net_waits

Rpl_semi_sync_master_no_times

Rpl_semi_sync_master_no_tx

Rpl_semi_sync_master_status

Rpl_semi_sync_master_timefunc_failures

rpl_semi_sync_master_timeout

Yes

Yes

Yes
rpl_semi_sync_master_trace_level
Yes

Rpl_semi_sync_master_tx_avg_wait_time

Rpl_semi_sync_master_tx_wait_time

Rpl_semi_sync_master_tx_waits

rpl_semi_sync_master_wait_for_slave_count

Yes

Yes

rpl_semi_sync_master_wait_no_slave

Yes

Yes

Yes
rpl_semi_sync_master_wait_point
Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Rpl_semi_sync_master_wait_pos_backtraverse

Rpl_semi_sync_master_wait_sessions

Rpl_semi_sync_master_yes_tx

rpl_semi_sync_slave_enabled

Yes

Yes

Rpl_semi_sync_slave_status

Yes
rpl_semi_sync_slave_trace_level

Yes

rpl_stop_slave_timeout

Yes

Yes

Rsa_public_key

safe-user-
create

Yes

secure_auth Yes

secure_file_privYes

Select_full_join

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

696

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

No

Yes

Yes

No

No

No

No

Yes

No

Yes

No

No

No

No

No

No

No

Yes

Yes

No

No

No

Yes

Yes

Yes

No

No

No

Yes

No

Yes

Yes

No

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Select_full_range_join

Select_range

Select_range_check

Select_scan

server_id

Yes

server_id_bits Yes

server_uuid

session_track_gtidsYes

session_track_schema

Yes

Yes

Yes

Yes

Yes

session_track_state_change

Yes

Yes

Yes
session_track_system_variables

Yes

session_track_transaction_info

Yes

Yes

sha256_password_auto_generate_rsa_keys

Yes

Yes

sha256_password_private_key_path

Yes

Yes

sha256_password_proxy_users

Yes

Yes

Yes
sha256_password_public_key_path

Yes

shared_memoryYes

Yes

shared_memory_base_name

Yes

Yes

show_compatibility_56

Yes

Yes

show_create_table_verbosity

Yes

Yes

show_old_temporalsYes

Yes

Yes

show-slave-
auth-info

skip-
character-
set-client-
handshake

skip_external_locking

Yes

skip-grant-
tables

skip-host-
cache

Yes

Yes

skip_name_resolveYes

skip-
ndbcluster

Yes

skip_networkingYes

skip-new

Yes

skip-partition Yes

skip_show_database

Yes

skip_slave_startYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Both

Both

No

No

No

No

Yes

No

No

Yes

Yes

Yes

Yes

Yes

No

No

Yes

No

No

No

Yes

Yes

Yes

Global

No

Global

No

Global

No

Global

Global

No

No

697

Server Option, System Variable, and Status Variable Reference

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Name

skip-ssl

skip-stack-
trace

Yes

Yes

slave_allow_batching

Yes

slave_checkpoint_group

Yes

slave_checkpoint_period

Yes

Yes

Yes

Yes

Yes

Yes

slave_compressed_protocol

Yes

Yes

slave_exec_modeYes

Yes

Slave_heartbeat_period

Slave_last_heartbeat

slave_load_tmpdirYes

slave_max_allowed_packet

Yes

slave_net_timeoutYes

Slave_open_temp_tables

slave_parallel_typeYes

slave_parallel_workers

Yes

Yes

Yes

Yes

Yes

Yes

slave_pending_jobs_size_max

Yes

Yes

slave_preserve_commit_order

Yes

Yes

Slave_received_heartbeats

Slave_retried_transactions

Slave_rows_last_search_algorithm_used

slave_rows_search_algorithms

Yes

Yes

Slave_running

slave_skip_errorsYes

Yes

slave-sql-
verify-
checksum

slave_sql_verify_checksum

Yes

slave_transaction_retries

Yes

slave_type_conversions

Yes

Slow_launch_threads

slow_launch_timeYes

Slow_queries

slow_query_logYes

slow_query_log_fileYes

slow-start-
timeout

socket

Yes

Yes

sort_buffer_sizeYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

698

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Both

Global

Global

Global

Both

Yes

Yes

Yes

Yes

Yes

No

No

No

Yes

Yes

No

Yes

Yes

Yes

Yes

No

No

No

Yes

No

No

Yes

Yes

Yes

No

Yes

No

Yes

Yes

No

Yes

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Sort_merge_passes

Sort_range

Sort_rows

Sort_scan

sporadic-
binlog-dump-
fail

Yes

Yes

sql_auto_is_null

sql_big_selects

sql_buffer_result

sql_log_bin

sql_log_off

sql_mode

Yes

Yes

sql_notes

sql_quote_show_create

sql_safe_updates

sql_select_limit

sql_slave_skip_counter

sql_warnings

ssl

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Ssl_accept_renegotiates

Ssl_accepts

ssl_ca

Yes

Ssl_callback_cache_hits

ssl_capath

ssl_cert

Ssl_cipher

Yes

Yes

ssl_cipher

Yes

Ssl_cipher_list

Ssl_client_connects

Ssl_connect_renegotiates

ssl_crl

ssl_crlpath

Yes

Yes

Ssl_ctx_verify_depth

Ssl_ctx_verify_mode

Ssl_default_timeout

Ssl_finished_accepts

Ssl_finished_connects

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Both

Both

Both

Session

Both

Both

Both

Both

Both

Both

Global

Both

Global

Global

Global

Global

Global

Global

Both

Global

Both

Global

Global

Global

Global

Global

Global

Both

Global

Global

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

699

Server Option, System Variable, and Status Variable Reference

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Name

ssl_key

Yes

Yes

Yes

Ssl_server_not_after

Ssl_server_not_before

Ssl_session_cache_hits

Ssl_session_cache_misses

Ssl_session_cache_mode

Ssl_session_cache_overflows

Ssl_session_cache_size

Ssl_session_cache_timeouts

Ssl_sessions_reused

Ssl_used_session_cache_entries

Ssl_verify_depth

Ssl_verify_mode

Ssl_version

standalone

Yes

stored_program_cache

Yes

super-large-
pages

Yes

super_read_onlyYes

symbolic-links Yes

sync_binlog

sync_frm

Yes

Yes

sync_master_infoYes

sync_relay_log Yes

sync_relay_log_infoYes

sysdate-is-
now

Yes

system_time_zone

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

table_definition_cache

Yes

Yes

Table_locks_immediate

Table_locks_waited

table_open_cacheYes

Yes

Table_open_cache_hits

table_open_cache_instances

Yes

Yes

Table_open_cache_misses

Table_open_cache_overflows

tc-heuristic-
recover

Yes

Yes

Tc_log_max_pages_used

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

700

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Both

Both

Global

Global

Global

Global

Global

Global

Session

Global

Both

Both

Both

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Global

Yes

Global

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Both

Both

Yes

Yes

Yes

Yes

Yes

No

Yes

No

No

Yes

No

No

No

No

Yes

Global

No

Server Option, System Variable, and Status Variable Reference

Name

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Tc_log_page_size

Tc_log_page_waits

temp-pool

Yes

thread_cache_sizeYes

thread_handlingYes

thread_pool_algorithm

Yes

Yes

Yes

Yes

Yes

thread_pool_high_priority_connection

Yes

Yes

Yes
thread_pool_max_unused_threads
Yes

thread_pool_prio_kickup_timer

Yes

Yes

thread_pool_sizeYes

thread_pool_stall_limit

Yes

thread_stack Yes

Threads_cached

Threads_connected

Threads_created

Threads_running

time_format

time_zone

timestamp

tls_version

Yes

tmp_table_sizeYes

tmpdir

Yes

Yes

Yes

Yes

Yes

Yes

Yes

transaction_alloc_block_size

Yes

Yes

transaction_allow_batching

transaction_isolationYes

Yes

- Variable:
tx_isolation

transaction_prealloc_size

Yes

transaction_read_only

Yes

Yes

Yes

- Variable:
tx_read_only

Yes
transaction_write_set_extraction

Yes

tx_isolation

tx_read_only

unique_checks

updatable_views_with_limit

Yes

Yes

Uptime

Uptime_since_flush_status

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Session

Global

Both

Global

Both

Session

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Yes

Yes

Global

Global

No

No

Yes

No

No

Yes

Yes

Yes

No

Yes

No

No

No

No

No

No

Yes

Yes

No

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

701

Server System Variable Reference

Name

user

validate-
password

Cmd-Line

Option File

System Var Status Var

Var Scope

Dynamic

Yes

Yes

Yes

Yes

validate_password_check_user_name

Yes

Yes

Yes
validate_password_dictionary_file
Yes

Yes

Yes

validate_password_dictionary_file_last_parsed

validate_password_dictionary_file_words_count

Yes

Yes

validate_password_length

Yes

Yes

validate_password_mixed_case_count

Yes

Yes

Yes
validate_password_number_count
Yes

validate_password_policy

Yes

Yes

validate_password_special_char_count

Yes

Yes

validate-user-
plugins

verbose

version

Yes

Yes

version_comment

Yes

Yes

version_compile_machine

version_compile_os

version_tokens_session

Yes

Yes

Yes
version_tokens_session_number

Yes

wait_timeout Yes

Yes

warning_count

Notes:

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Session

Yes

Varies

No

No

Yes

Yes

Yes

Yes

Yes

No

No

No

No

Yes

No

Yes

No

1. This option is dynamic, but should be set only by server. You should not set this variable manually.

5.1.4 Server System Variable Reference

The following table lists all system variables applicable within mysqld.

The table lists command-line options (Cmd-line), options valid in configuration files (Option file), server
system variables (System Var), and status variables (Status var) in one unified list, with an indication of
where each option or variable is valid. If a server option set on the command line or in an option file differs
from the name of the corresponding system variable, the variable name is noted immediately below the
corresponding option. The scope of the variable (Var Scope) is Global, Session, or both. Please see the
corresponding item descriptions for details on setting and using the variables. Where appropriate, direct
links to further information about the items are provided.

Table 5.2 System Variable Summary

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

audit_log_buffer_sizeYes

audit_log_compressionYes

Yes

Yes

Yes

Yes

Global

Global

No

No

702

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

audit_log_connection_policy

Yes

Yes

audit_log_current_session

audit_log_disable Yes

audit_log_encryptionYes

audit_log_exclude_accounts

Yes

audit_log_file

Yes

audit_log_filter_id

audit_log_flush

Yes

Yes

Yes

Yes

audit_log_format Yes

Yes

audit_log_format_unix_timestamp

Yes

Yes

audit_log_include_accounts

Yes

audit_log_policy Yes

audit_log_read_buffer_size

Yes

audit_log_rotate_on_size

Yes

audit_log_statement_policy

Yes

audit_log_strategyYes

Yes

Yes

Yes

Yes

Yes

Yes

authentication_ldap_sasl_auth_method_name

Yes

Yes

Yes
authentication_ldap_sasl_bind_base_dn
Yes

Yes
authentication_ldap_sasl_bind_root_dn
Yes

Yes
authentication_ldap_sasl_bind_root_pwd

Yes

authentication_ldap_sasl_ca_path

Yes

Yes

authentication_ldap_sasl_group_search_attr

Yes

Yes

authentication_ldap_sasl_group_search_filter

Yes

Yes

Yes
authentication_ldap_sasl_init_pool_size
Yes

authentication_ldap_sasl_log_status

Yes

Yes

Yes
authentication_ldap_sasl_max_pool_size

Yes

Yes
authentication_ldap_sasl_server_host

Yes

Yes
authentication_ldap_sasl_server_port

Yes

authentication_ldap_sasl_tls

Yes

Yes

authentication_ldap_sasl_user_search_attr

Yes

Yes

authentication_ldap_simple_auth_method_name

Yes

Yes

authentication_ldap_simple_bind_base_dn

Yes

Yes

Yes
authentication_ldap_simple_bind_root_dn

Yes

authentication_ldap_simple_bind_root_pwd

Yes

Yes

authentication_ldap_simple_ca_path

Yes

Yes

authentication_ldap_simple_group_search_attr

Yes

Yes

authentication_ldap_simple_group_search_filter

Yes

Yes

authentication_ldap_simple_init_pool_size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Both

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Varies

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

No

Yes

No

Yes

No

No

Yes

No

Yes

Yes

No

Varies

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

703

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

Yes
authentication_ldap_simple_log_status
Yes

authentication_ldap_simple_max_pool_size

Yes

Yes

Yes
authentication_ldap_simple_server_host
Yes

Yes
authentication_ldap_simple_server_port
Yes

authentication_ldap_simple_tls

Yes

Yes

authentication_ldap_simple_user_search_attr

Yes

Yes

authentication_windows_log_level

Yes

Yes

authentication_windows_use_principal_name

Yes

Yes

auto_generate_certsYes

auto_increment_increment

Yes

auto_increment_offsetYes

autocommit

Yes

automatic_sp_privileges

Yes

avoid_temporal_upgrade

Yes

back_log

basedir

big_tables

bind_address

Yes

Yes

Yes

Yes

binlog_cache_sizeYes

binlog_checksum Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
binlog_direct_non_transactional_updates

Yes

binlog_error_actionYes

binlog_format

Yes

Yes

Yes

binlog_group_commit_sync_delay

Yes

Yes

binlog_group_commit_sync_no_delay_count

Yes

Yes

binlog_gtid_simple_recovery

Yes

binlog_max_flush_queue_time

Yes

binlog_order_commitsYes

binlog_row_imageYes

binlog_rows_query_log_events

Yes

binlog_stmt_cache_size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

binlog_transaction_dependency_history_size

Yes

Yes

Yes
binlog_transaction_dependency_tracking

Yes

block_encryption_mode

Yes

bulk_insert_buffer_sizeYes

character_set_client

character_set_connection

Yes

Yes

704

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Global

Global

Global

Global

Both

Global

Global

Global

Both

Global

Both

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Both

Both

Both

Both

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

Yes

Yes

Yes

Yes

Yes

No

No

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

character_set_database
(note 1)

character_set_filesystemYes

character_set_results

character_set_serverYes

character_set_system

character_sets_dirYes

check_proxy_usersYes

collation_connection

collation_database
(note 1)

collation_server Yes

completion_type Yes

concurrent_insert Yes

connect_timeout Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

connection_control_failed_connections_threshold

Yes

Yes

connection_control_max_connection_delay

Yes

Yes

connection_control_min_connection_delay

Yes

Yes

core_file

daemon_memcached_enable_binlog

Yes

Yes

Yes
daemon_memcached_engine_lib_name
Yes

Yes
daemon_memcached_engine_lib_path
Yes

daemon_memcached_option

Yes

Yes

daemon_memcached_r_batch_size

Yes

Yes

daemon_memcached_w_batch_size

Yes

Yes

datadir

Yes

Yes

date_format

datetime_format

debug

Yes

debug_sync

default_authentication_plugin

Yes

default_password_lifetime

Yes

default_storage_engineYes

default_tmp_storage_engine

Yes

default_week_formatYes

delay_key_write Yes

delayed_insert_limitYes

delayed_insert_timeout

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Global

Global

Global

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Session

Global

Global

Both

Both

Both

Global

Global

Global

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

No

No

No

No

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

705

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

delayed_queue_sizeYes

disabled_storage_engines

Yes

Yes

Yes

disconnect_on_expired_password

Yes

Yes

div_precision_increment

Yes

end_markers_in_jsonYes

enforce_gtid_consistency

Yes

eq_range_index_dive_limit

Yes

error_count

event_scheduler Yes

expire_logs_days Yes

explicit_defaults_for_timestamp

Yes

external_user

flush

flush_time

Yes

Yes

foreign_key_checks

ft_boolean_syntaxYes

ft_max_word_len Yes

ft_min_word_len Yes

ft_query_expansion_limit

Yes

ft_stopword_file Yes

general_log

Yes

general_log_file Yes

group_concat_max_lenYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_allow_local_disjoint_gtids_join

Yes

Yes

group_replication_allow_local_lower_version_join

Yes

Yes

group_replication_auto_increment_increment

Yes

Yes

group_replication_bootstrap_group

Yes

Yes

group_replication_components_stop_timeout

Yes

Yes

group_replication_compression_threshold

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

group_replication_enforce_update_everywhere_checks

Yes

Yes

Yes

group_replication_exit_state_action

Yes

Yes

group_replication_flow_control_applier_threshold

Yes

Yes

group_replication_flow_control_certifier_threshold

Yes

Yes

Yes
group_replication_flow_control_mode

Yes

group_replication_force_members

Yes

Yes

group_replication_group_name

Yes

group_replication_group_seeds

Yes

Yes

Yes

group_replication_gtid_assignment_block_size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

706

Global

Global

Global

Both

Both

Global

Both

Session

Global

Global

Both

Session

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

No

No

Yes

Yes

Varies

Yes

No

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

group_replication_ip_whitelist

Yes

group_replication_local_address

Yes

Yes

Yes

group_replication_member_weight

Yes

Yes

group_replication_poll_spin_loops

Yes

Yes

Yes
group_replication_recovery_complete_at

Yes

group_replication_recovery_reconnect_interval

Yes

Yes

Yes
group_replication_recovery_retry_count
Yes

group_replication_recovery_ssl_ca

Yes

Yes

Yes
group_replication_recovery_ssl_capath
Yes

group_replication_recovery_ssl_cert

Yes

Yes

Yes
group_replication_recovery_ssl_cipher
Yes

group_replication_recovery_ssl_crl

Yes

Yes

Yes
group_replication_recovery_ssl_crlpath
Yes

group_replication_recovery_ssl_key

Yes

Yes

group_replication_recovery_ssl_verify_server_cert

Yes

Yes

group_replication_recovery_use_ssl

Yes

Yes

Yes
group_replication_single_primary_mode
Yes

group_replication_ssl_mode

Yes

group_replication_start_on_boot

Yes

Yes

Yes

Yes
group_replication_transaction_size_limit
Yes

group_replication_unreachable_majority_timeout

Yes

Yes

gtid_executed

gtid_executed_compression_period

Yes

Yes

gtid_mode

Yes

Yes

gtid_next

gtid_owned

gtid_purged

have_compress

have_crypt

have_dynamic_loading

have_geometry

have_openssl

have_profiling

have_query_cache

have_rtree_keys

have_ssl

have_statement_timeout

have_symlink

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Varies

Global

Global

Session

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Varies

Yes

No

Yes

No

No

No

No

No

No

No

No

No

No

No

707

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

host_cache_size Yes

Yes

hostname

identity

ignore_builtin_innodbYes

ignore_db_dirs

init_connect

init_file

init_slave

Yes

Yes

Yes

innodb_adaptive_flushing

Yes

innodb_adaptive_flushing_lwm

Yes

innodb_adaptive_hash_index

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_adaptive_hash_index_parts

Yes

Yes

innodb_adaptive_max_sleep_delay

Yes

Yes

innodb_api_bk_commit_interval

Yes

innodb_api_disable_rowlock

Yes

innodb_api_enable_binlog

Yes

innodb_api_enable_mdl

Yes

innodb_api_trx_levelYes

innodb_autoextend_increment

Yes

innodb_autoinc_lock_mode

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_background_drop_list_empty

Yes

Yes

innodb_buffer_pool_chunk_size

Yes

Yes

Yes
innodb_buffer_pool_dump_at_shutdown
Yes

innodb_buffer_pool_dump_now

Yes

innodb_buffer_pool_dump_pct

Yes

innodb_buffer_pool_filename

Yes

innodb_buffer_pool_instances

Yes

innodb_buffer_pool_load_abort

Yes

Yes

Yes

Yes

Yes

Yes

innodb_buffer_pool_load_at_startup

Yes

Yes

innodb_buffer_pool_load_now

Yes

innodb_buffer_pool_size

Yes

Yes

Yes

innodb_change_buffer_max_size

Yes

Yes

innodb_change_buffering

Yes

innodb_change_buffering_debug

Yes

innodb_checksum_algorithm

Yes

innodb_checksumsYes

innodb_cmp_per_index_enabled

Yes

innodb_commit_concurrency

Yes

Yes

Yes

Yes

Yes

Yes

Yes

708

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Session

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

No

Yes

No

No

Yes

No

Yes

Yes

Yes

Yes

No

Yes

Yes

No

No

No

Yes

Yes

No

Yes

No

Yes

Yes

Yes

Yes

No

Yes

No

Yes

Varies

Yes

Yes

Yes

Yes

No

Yes

Yes

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

innodb_compress_debug

Yes

Yes

innodb_compression_failure_threshold_pct

Yes

Yes

innodb_compression_level

Yes

Yes

innodb_compression_pad_pct_max

Yes

Yes

innodb_concurrency_tickets

Yes

innodb_data_file_pathYes

innodb_data_home_dirYes

innodb_deadlock_detect

Yes

innodb_default_row_format

Yes

Yes

Yes

Yes

Yes

Yes

innodb_disable_resize_buffer_pool_debug

Yes

Yes

innodb_disable_sort_file_cache

Yes

innodb_doublewriteYes

innodb_fast_shutdownYes

Yes

Yes

Yes

innodb_fil_make_page_dirty_debug

Yes

Yes

innodb_file_formatYes

innodb_file_format_check

Yes

innodb_file_format_max

Yes

innodb_file_per_tableYes

innodb_fill_factor Yes

innodb_flush_log_at_timeout

Yes

innodb_flush_log_at_trx_commit

Yes

innodb_flush_methodYes

innodb_flush_neighbors

Yes

innodb_flush_syncYes

innodb_flushing_avg_loops

Yes

innodb_force_load_corrupted

Yes

innodb_force_recoveryYes

innodb_ft_aux_table

innodb_ft_cache_sizeYes

innodb_ft_enable_diag_print

Yes

innodb_ft_enable_stopword

Yes

innodb_ft_max_token_size

Yes

innodb_ft_min_token_size

Yes

innodb_ft_num_word_optimize

Yes

innodb_ft_result_cache_limit

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_ft_server_stopword_table

Yes

Yes

innodb_ft_sort_pll_degree

Yes

innodb_ft_total_cache_size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

No

No

Yes

No

Yes

Yes

No

No

Yes

Yes

Yes

No

No

709

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

innodb_ft_user_stopword_table

Yes

innodb_io_capacityYes

innodb_io_capacity_max

Yes

innodb_large_prefixYes

Yes

Yes

Yes

Yes

innodb_limit_optimistic_insert_debug

Yes

Yes

innodb_lock_wait_timeout

Yes

innodb_locks_unsafe_for_binlog

Yes

innodb_log_buffer_sizeYes

innodb_log_checkpoint_now

Yes

innodb_log_checksums

Yes

innodb_log_compressed_pages

Yes

innodb_log_file_sizeYes

innodb_log_files_in_group

Yes

innodb_log_group_home_dir

Yes

innodb_log_write_ahead_size

Yes

innodb_lru_scan_depthYes

innodb_max_dirty_pages_pct

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_max_dirty_pages_pct_lwm

Yes

Yes

innodb_max_purge_lagYes

innodb_max_purge_lag_delay

Yes

innodb_max_undo_log_size

Yes

Yes

Yes

Yes

Yes
innodb_merge_threshold_set_all_debug
Yes

innodb_monitor_disable

Yes

innodb_monitor_enableYes

innodb_monitor_resetYes

innodb_monitor_reset_all

Yes

innodb_numa_interleave

Yes

innodb_old_blocks_pctYes

innodb_old_blocks_time

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_online_alter_log_max_size

Yes

Yes

innodb_open_filesYes

innodb_optimize_fulltext_only

Yes

innodb_page_cleanersYes

innodb_page_sizeYes

innodb_print_all_deadlocks

Yes

innodb_purge_batch_size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
innodb_purge_rseg_truncate_frequency
Yes

innodb_purge_threadsYes

Yes

710

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

No

Yes

No

No

Yes

Yes

Yes

No

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

innodb_random_read_ahead

Yes

innodb_read_ahead_threshold

Yes

innodb_read_io_threads

Yes

innodb_read_onlyYes

innodb_replication_delay

Yes

innodb_rollback_on_timeout

Yes

innodb_rollback_segments

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_saved_page_number_debug

Yes

Yes

innodb_sort_buffer_size

Yes

innodb_spin_wait_delay

Yes

innodb_stats_auto_recalc

Yes

Yes

Yes

Yes

Yes
innodb_stats_include_delete_marked

Yes

innodb_stats_methodYes

innodb_stats_on_metadata

Yes

innodb_stats_persistent

Yes

Yes

Yes

Yes

Yes
innodb_stats_persistent_sample_pages
Yes

innodb_stats_sample_pages

Yes

Yes

Yes
innodb_stats_transient_sample_pages
Yes

innodb_status_outputYes

innodb_status_output_locks

Yes

innodb_strict_modeYes

innodb_support_xaYes

innodb_sync_array_size

Yes

innodb_sync_debugYes

innodb_sync_spin_loops

Yes

innodb_table_locksYes

innodb_temp_data_file_path

Yes

innodb_thread_concurrency

Yes

innodb_thread_sleep_delay

Yes

innodb_tmpdir

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

innodb_trx_purge_view_update_only_debug

Yes

Yes

innodb_trx_rseg_n_slots_debug

Yes

innodb_undo_directoryYes

innodb_undo_log_truncate

Yes

innodb_undo_logsYes

innodb_undo_tablespaces

Yes

innodb_use_native_aioYes

innodb_version

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Both

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

No

No

Yes

No

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

No

No

No

711

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

innodb_write_io_threads

Yes

insert_id

interactive_timeoutYes

Yes

Yes

internal_tmp_disk_storage_engine

Yes

Yes

join_buffer_size Yes

keep_files_on_createYes

key_buffer_size Yes

key_cache_age_threshold

Yes

key_cache_block_sizeYes

key_cache_division_limit

Yes

keyring_aws_cmk_idYes

keyring_aws_conf_fileYes

keyring_aws_data_fileYes

keyring_aws_regionYes

keyring_encrypted_file_data

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

keyring_encrypted_file_password

Yes

Yes

keyring_file_data Yes

keyring_okv_conf_dirYes

keyring_operations

language

Yes

large_files_support

large_page_size

large_pages

Yes

last_insert_id

lc_messages

Yes

lc_messages_dir Yes

lc_time_names Yes

license

local_infile

Yes

lock_wait_timeoutYes

locked_in_memory

log_bin

log_bin_basename

log_bin_index

Yes

log_bin_trust_function_creators

Yes

log_bin_use_v1_row_events

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
log_builtin_as_identified_by_password
Yes

log_error

Yes

Yes

712

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Session

Both

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

Both

Global

Both

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

Yes

Yes

No

Yes

No

Yes

Yes

No

No

No

No

Yes

Yes

Yes

No

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

log_error_verbosityYes

log_output

Yes

log_queries_not_using_indexes

Yes

log_slave_updatesYes

log_slow_admin_statements

Yes

log_slow_slave_statements

Yes

Yes

Yes

Yes

Yes

Yes

Yes

log_statements_unsafe_for_binlog

Yes

Yes

log_syslog

Yes

log_syslog_facilityYes

log_syslog_include_pidYes

log_syslog_tag Yes

Yes

Yes

Yes

Yes

Yes
log_throttle_queries_not_using_indexes
Yes

log_timestamps Yes

log_warnings

Yes

long_query_time Yes

low_priority_updatesYes

lower_case_file_system

lower_case_table_names

Yes

master_info_repositoryYes

master_verify_checksumYes

max_allowed_packetYes

max_binlog_cache_size

Yes

max_binlog_size Yes

max_binlog_stmt_cache_size

Yes

max_connect_errorsYes

max_connections Yes

max_delayed_threadsYes

max_digest_lengthYes

max_error_count Yes

max_execution_timeYes

max_heap_table_sizeYes

max_insert_delayed_threads

max_join_size

Yes

max_length_for_sort_data

Yes

max_points_in_geometry

Yes

max_prepared_stmt_count

Yes

max_relay_log_sizeYes

max_seeks_for_keyYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Both

Global

Global

Global

Global

Global

Both

Global

Both

Both

Both

Both

Both

Both

Both

Global

Global

Both

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

713

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

max_sort_length Yes

max_sp_recursion_depth

Yes

max_tmp_tables

max_user_connectionsYes

max_write_lock_countYes

mecab_rc_file

Yes

metadata_locks_cache_size

Yes

metadata_locks_hash_instances

Yes

min_examined_row_limit

Yes

multi_range_countYes

myisam_data_pointer_size

Yes

myisam_max_sort_file_size

Yes

myisam_mmap_sizeYes

myisam_recover_options

Yes

myisam_repair_threads

Yes

myisam_sort_buffer_size

Yes

myisam_stats_methodYes

myisam_use_mmapYes

mysql_firewall_modeYes

mysql_firewall_traceYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
mysql_native_password_proxy_users

Yes

mysqlx_bind_addressYes

mysqlx_connect_timeout

Yes

Yes

Yes

mysqlx_idle_worker_thread_timeout

Yes

Yes

mysqlx_max_allowed_packet

Yes

mysqlx_max_connections

Yes

mysqlx_min_worker_threads

Yes

mysqlx_port

Yes

mysqlx_port_open_timeout

Yes

mysqlx_socket

mysqlx_ssl_ca

Yes

Yes

mysqlx_ssl_capathYes

mysqlx_ssl_cert Yes

mysqlx_ssl_cipherYes

mysqlx_ssl_crl

Yes

mysqlx_ssl_crlpathYes

mysqlx_ssl_key Yes

named_pipe

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

714

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

No

No

No

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

No

No

No

No

No

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

named_pipe_full_access_group

Yes

ndb_allow_copying_alter_table

Yes

ndb_autoincrement_prefetch_sz

Yes

ndb_batch_size Yes

ndb_blob_read_batch_bytes

Yes

ndb_blob_write_batch_bytes

Yes

ndb_cache_check_time

Yes

ndb_clear_apply_status

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

ndb_cluster_connection_pool

Yes

Yes

Yes
ndb_cluster_connection_pool_nodeids
Yes

ndb_data_node_neighbour

Yes

ndb_default_column_format

Yes

ndb_default_column_format

Yes

ndb_deferred_constraints

Yes

ndb_deferred_constraints

Yes

ndb_distribution Yes

ndb_distribution Yes

ndb_eventbuffer_free_percent

Yes

ndb_eventbuffer_max_alloc

Yes

ndb_extra_loggingYes

ndb_force_send Yes

ndb_fully_replicatedYes

ndb_index_stat_enableYes

ndb_index_stat_optionYes

ndb_join_pushdown

ndb_log_apply_statusYes

ndb_log_apply_statusYes

ndb_log_bin

Yes

ndb_log_binlog_indexYes

ndb_log_empty_epochs

Yes

ndb_log_empty_epochs

Yes

ndb_log_empty_updateYes

ndb_log_empty_updateYes

ndb_log_exclusive_reads

Yes

ndb_log_exclusive_reads

Yes

ndb_log_fail_terminateYes

ndb_log_orig

ndb_log_orig

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Both

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

715

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

ndb_log_transaction_idYes

ndb_log_transaction_id

ndb_log_update_as_write

Yes

ndb_log_update_minimal

Yes

ndb_log_updated_onlyYes

ndb_optimization_delay

Yes

ndb_optimized_node_selection

Yes

ndb_optimized_node_selection

Yes

ndb_read_backupYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
ndb_recv_thread_activation_threshold

Yes

ndb_recv_thread_cpu_mask

Yes

Yes

Yes
ndb_report_thresh_binlog_epoch_slip

Yes

Yes
ndb_report_thresh_binlog_mem_usage
Yes

ndb_row_checksum

ndb_show_foreign_key_mock_tables

Yes

Yes

ndb_slave_conflict_roleYes

Yes

Ndb_system_name

ndb_table_no_logging

ndb_table_temporary

ndb_use_copying_alter_table

ndb_use_exact_count

ndb_use_transactionsYes

Yes

ndb_version

ndb_version_string

ndb_wait_connectedYes

ndb_wait_setup Yes

ndbinfo_database

ndbinfo_max_bytesYes

ndbinfo_max_rowsYes

ndbinfo_offline

ndbinfo_show_hiddenYes

ndbinfo_table_prefix

ndbinfo_version

net_buffer_length Yes

net_read_timeout Yes

net_retry_count Yes

net_write_timeoutYes

new

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

716

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Session

Session

Both

Both

Both

Global

Global

Global

Global

Global

Both

Both

Global

Both

Global

Global

Both

Both

Both

Both

Both

No

No

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

No

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

ngram_token_sizeYes

offline_mode

old

old_alter_table

Yes

Yes

Yes

old_passwords Yes

open_files_limit Yes

optimizer_prune_levelYes

optimizer_search_depth

Yes

optimizer_switch Yes

optimizer_trace Yes

optimizer_trace_features

Yes

optimizer_trace_limitYes

optimizer_trace_max_mem_size

Yes

optimizer_trace_offsetYes

parser_max_mem_sizeYes

performance_schemaYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
performance_schema_accounts_size

Yes

performance_schema_digests_size

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
performance_schema_events_stages_history_long_size

Yes

Yes

performance_schema_events_stages_history_size

Yes

Yes

Yes

performance_schema_events_statements_history_long_size

Yes

Yes

Yes

performance_schema_events_statements_history_size

Yes

Yes

Yes

performance_schema_events_transactions_history_long_size

Yes

Yes

Yes

Yes
performance_schema_events_transactions_history_size

Yes

Yes

performance_schema_events_waits_history_long_size

Yes

Yes

Yes

performance_schema_events_waits_history_size

Yes

Yes

performance_schema_hosts_size

Yes

Yes

performance_schema_max_cond_classes

Yes

Yes

performance_schema_max_cond_instances

Yes

Yes

performance_schema_max_digest_length

Yes

Yes

Yes
performance_schema_max_file_classes
Yes

Yes
performance_schema_max_file_handles
Yes

performance_schema_max_file_instances

Yes

Yes

Yes
performance_schema_max_index_stat
Yes

performance_schema_max_memory_classes

Yes

Yes

performance_schema_max_metadata_locks

Yes

Yes

performance_schema_max_mutex_classes

Yes

Yes

performance_schema_max_mutex_instances

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Both

Both

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

No

Yes

No

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

717

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

performance_schema_max_prepared_statements_instances

Yes

Yes

Yes

performance_schema_max_program_instances

Yes

Yes

performance_schema_max_rwlock_classes

Yes

Yes

performance_schema_max_rwlock_instances

Yes

Yes

performance_schema_max_socket_classes

Yes

Yes

performance_schema_max_socket_instances

Yes

Yes

performance_schema_max_sql_text_length

Yes

Yes

performance_schema_max_stage_classes

Yes

Yes

performance_schema_max_statement_classes

Yes

Yes

performance_schema_max_statement_stack

Yes

Yes

performance_schema_max_table_handles

Yes

Yes

performance_schema_max_table_instances

Yes

Yes

performance_schema_max_table_lock_stat

Yes

Yes

performance_schema_max_thread_classes

Yes

Yes

performance_schema_max_thread_instances

Yes

Yes

performance_schema_session_connect_attrs_size

Yes

Yes

Yes
performance_schema_setup_actors_size

Yes

performance_schema_setup_objects_size

Yes

Yes

Yes
performance_schema_show_processlist
Yes

performance_schema_users_size

Yes

Yes

pid_file

plugin_dir

port

Yes

Yes

Yes

preload_buffer_sizeYes

profiling

profiling_history_sizeYes

protocol_version

proxy_user

pseudo_slave_mode

pseudo_thread_id

query_alloc_block_sizeYes

query_cache_limitYes

query_cache_min_res_unit

Yes

query_cache_sizeYes

query_cache_typeYes

query_cache_wlock_invalidate

Yes

query_prealloc_sizeYes

rand_seed1

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

718

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Global

Session

Session

Session

Both

Global

Global

Global

Both

Both

Both

Session

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

No

Yes

No

No

No

No

Yes

Yes

Yes

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

rand_seed2

range_alloc_block_sizeYes

Yes

range_optimizer_max_mem_size

Yes

Yes

rbr_exec_mode

read_buffer_size Yes

read_only

Yes

read_rnd_buffer_sizeYes

relay_log

Yes

relay_log_basename

relay_log_index Yes

relay_log_info_fileYes

relay_log_info_repository

Yes

relay_log_purge Yes

relay_log_recoveryYes

relay_log_space_limitYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

replication_optimize_for_static_plugin_config

Yes

Yes

Yes
replication_sender_observe_commit_only

Yes

report_host

Yes

report_password Yes

report_port

report_user

Yes

Yes

require_secure_transport

Yes

rewriter_enabled

rewriter_verbose

rpl_semi_sync_master_enabled

Yes

rpl_semi_sync_master_timeout

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

rpl_semi_sync_master_trace_level

Yes

Yes

rpl_semi_sync_master_wait_for_slave_count

Yes

Yes

Yes
rpl_semi_sync_master_wait_no_slave

Yes

rpl_semi_sync_master_wait_point

Yes

Yes

rpl_semi_sync_slave_enabled

Yes

rpl_semi_sync_slave_trace_level

Yes

rpl_stop_slave_timeout

Yes

secure_auth

Yes

secure_file_priv Yes

server_id

server_id_bits

server_uuid

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Session

Both

Both

Session

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

Yes

Yes

No

No

Yes

Yes

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

No

No

719

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

session_track_gtidsYes

session_track_schemaYes

session_track_state_change

Yes

session_track_system_variables

Yes

session_track_transaction_info

Yes

Yes

Yes

Yes

Yes

Yes

sha256_password_auto_generate_rsa_keys

Yes

Yes

sha256_password_private_key_path

Yes

Yes

sha256_password_proxy_users

Yes

Yes

sha256_password_public_key_path

Yes

Yes

shared_memory Yes

shared_memory_base_name

Yes

show_compatibility_56Yes

show_create_table_verbosity

Yes

show_old_temporalsYes

skip_external_lockingYes

skip_name_resolveYes

skip_networking Yes

skip_show_databaseYes

skip_slave_start Yes

slave_allow_batchingYes

slave_checkpoint_group

Yes

slave_checkpoint_period

Yes

slave_compressed_protocol

Yes

slave_exec_modeYes

slave_load_tmpdirYes

slave_max_allowed_packet

Yes

slave_net_timeoutYes

slave_parallel_typeYes

slave_parallel_workersYes

slave_pending_jobs_size_max

Yes

slave_preserve_commit_order

Yes

slave_rows_search_algorithms

Yes

slave_skip_errorsYes

slave_sql_verify_checksum

Yes

slave_transaction_retries

Yes

slave_type_conversions

Yes

slow_launch_timeYes

slow_query_log Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

720

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Yes

Yes

Yes

Yes

Yes

No

No

Yes

No

No

No

Yes

Yes

Yes

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes

Yes

Yes

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

slow_query_log_fileYes

socket

Yes

sort_buffer_size Yes

sql_auto_is_null

sql_big_selects

sql_buffer_result

Yes

Yes

Yes

sql_log_bin

sql_log_off

sql_mode

sql_notes

Yes

Yes

sql_quote_show_create

sql_safe_updates

sql_select_limit

sql_slave_skip_counter

sql_warnings

ssl_ca

ssl_capath

ssl_cert

ssl_cipher

ssl_crl

ssl_crlpath

ssl_key

Yes

Yes

Yes

Yes

Yes

Yes

Yes

stored_program_cacheYes

super_read_only Yes

sync_binlog

sync_frm

Yes

Yes

sync_master_infoYes

sync_relay_log Yes

sync_relay_log_infoYes

system_time_zone

table_definition_cacheYes

table_open_cacheYes

table_open_cache_instances

Yes

thread_cache_sizeYes

thread_handling Yes

thread_pool_algorithmYes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes
thread_pool_high_priority_connection

Yes

thread_pool_max_unused_threads

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Both

Both

Both

Both

Session

Both

Both

Both

Both

Both

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

No

No

No

No

No

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

No

Yes

No

No

Yes

Yes

721

Server System Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

thread_pool_prio_kickup_timer

Yes

thread_pool_size Yes

thread_pool_stall_limitYes

thread_stack

Yes

time_format

time_zone

timestamp

tls_version

Yes

tmp_table_size Yes

tmpdir

Yes

transaction_alloc_block_size

Yes

transaction_allow_batching

transaction_isolationYes

- Variable:
tx_isolation

transaction_prealloc_size

Yes

transaction_read_onlyYes

- Variable:
tx_read_only

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

transaction_write_set_extraction

Yes

Yes

tx_isolation

tx_read_only

unique_checks

updatable_views_with_limit

Yes

Yes

Yes
validate_password_check_user_name

Yes

validate_password_dictionary_file

Yes

Yes

validate_password_length

Yes

Yes

Yes
validate_password_mixed_case_count
Yes

validate_password_number_count

Yes

Yes

validate_password_policy

Yes

Yes

Yes
validate_password_special_char_count
Yes

version

version_comment

version_compile_machine

version_compile_os

version_tokens_session

Yes

version_tokens_session_number

Yes

wait_timeout

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Global

Global

Global

Global

Global

Both

Session

Global

Both

Global

Both

Session

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Yes

No

Yes

No

No

Yes

Yes

No

Yes

No

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Varies

Yes

Yes

Yes

Yes

Yes

No

No

No

No

Yes

No

Yes

722

Server Status Variable Reference

Name

Cmd-Line

Option File

System Var

Var Scope

Dynamic

warning_count

Notes:

Yes

Session

No

1. This option is dynamic, but should be set only by server. You should not set this variable manually.

5.1.5 Server Status Variable Reference

The following table lists all status variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each
variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting
and using the variables. Where appropriate, direct links to further information about the items are provided.

Table 5.3 Status Variable Summary

Variable Type

Variable Scope

Variable Name

Aborted_clients

Aborted_connects

Audit_log_current_size

Integer

Integer

Integer

Audit_log_event_max_drop_size

Integer

Audit_log_events

Audit_log_events_filtered

Audit_log_events_lost

Audit_log_events_written

Audit_log_total_size

Audit_log_write_waits

Binlog_cache_disk_use

Binlog_cache_use

Binlog_stmt_cache_disk_use

Binlog_stmt_cache_use

Bytes_received

Bytes_sent

Com_admin_commands

Com_alter_db

Com_alter_db_upgrade

Com_alter_event

Com_alter_function

Com_alter_procedure

Com_alter_server

Com_alter_table

Com_alter_tablespace

Com_alter_user

Com_analyze

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

723

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Com_assign_to_keycache

Com_begin

Com_binlog

Com_call_procedure

Com_change_db

Com_change_master

Com_change_repl_filter

Com_check

Com_checksum

Com_commit

Com_create_db

Com_create_event

Com_create_function

Com_create_index

Com_create_procedure

Com_create_server

Com_create_table

Com_create_trigger

Com_create_udf

Com_create_user

Com_create_view

Com_dealloc_sql

Com_delete

Com_delete_multi

Com_do

Com_drop_db

Com_drop_event

Com_drop_function

Com_drop_index

Com_drop_procedure

Com_drop_server

Com_drop_table

Com_drop_trigger

Com_drop_user

Com_drop_view

Com_empty_query

Com_execute_sql

Com_explain_other

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

724

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Variable Name

Com_flush

Com_get_diagnostics

Com_grant

Com_group_replication_start

Com_group_replication_stop

Com_ha_close

Com_ha_open

Com_ha_read

Com_help

Com_insert

Com_insert_select

Com_install_plugin

Com_kill

Com_load

Com_lock_tables

Com_optimize

Com_preload_keys

Com_prepare_sql

Com_purge

Com_purge_before_date

Com_release_savepoint

Com_rename_table

Com_rename_user

Com_repair

Com_replace

Com_replace_select

Com_reset

Com_resignal

Com_revoke

Com_revoke_all

Com_rollback

Com_rollback_to_savepoint

Com_savepoint

Com_select

Com_set_option

Com_show_authors

Com_show_binlog_events

Com_show_binlogs

Server Status Variable Reference

Variable Type

Variable Scope

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Both

Both

Both

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

725

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Com_show_charsets

Com_show_collations

Com_show_contributors

Com_show_create_db

Com_show_create_event

Com_show_create_func

Com_show_create_proc

Com_show_create_table

Com_show_create_trigger

Com_show_create_user

Com_show_databases

Com_show_engine_logs

Com_show_engine_mutex

Com_show_engine_status

Com_show_errors

Com_show_events

Com_show_fields

Com_show_function_code

Com_show_function_status

Com_show_grants

Com_show_keys

Com_show_master_status

Com_show_ndb_status

Com_show_open_tables

Com_show_plugins

Com_show_privileges

Com_show_procedure_code

Com_show_procedure_status

Com_show_processlist

Com_show_profile

Com_show_profiles

Com_show_relaylog_events

Com_show_slave_hosts

Com_show_slave_status

Com_show_status

Com_show_storage_engines

Com_show_table_status

Com_show_tables

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

726

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Server Status Variable Reference

Variable Type

Variable Scope

Variable Name

Com_show_triggers

Com_show_variables

Com_show_warnings

Com_shutdown

Com_signal

Com_slave_start

Com_slave_stop

Com_stmt_close

Com_stmt_execute

Com_stmt_fetch

Com_stmt_prepare

Com_stmt_reprepare

Com_stmt_reset

Com_stmt_send_long_data

Com_truncate

Com_uninstall_plugin

Com_unlock_tables

Com_update

Com_update_multi

Com_xa_commit

Com_xa_end

Com_xa_prepare

Com_xa_recover

Com_xa_rollback

Com_xa_start

Compression

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Connection_control_delay_generatedInteger

Connection_errors_accept

Connection_errors_internal

Integer

Integer

Connection_errors_max_connectionsInteger

Connection_errors_peer_address Integer

Connection_errors_select

Connection_errors_tcpwrap

Connections

Created_tmp_disk_tables

Created_tmp_files

Created_tmp_tables

Delayed_errors

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Session

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Both

Global

727

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Delayed_insert_threads

Delayed_writes

Firewall_access_denied

Firewall_access_granted

Firewall_access_suspicious

Firewall_cached_entries

Flush_commands

Integer

Integer

Integer

Integer

Integer

Integer

Integer

group_replication_primary_memberString

Handler_commit

Handler_delete

Handler_discover

Handler_external_lock

Handler_mrr_init

Handler_prepare

Handler_read_first

Handler_read_key

Handler_read_last

Handler_read_next

Handler_read_prev

Handler_read_rnd

Handler_read_rnd_next

Handler_rollback

Handler_savepoint

Handler_savepoint_rollback

Handler_update

Handler_write

Innodb_available_undo_logs

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Innodb_buffer_pool_bytes_data

Integer

Innodb_buffer_pool_bytes_dirty

Integer

Innodb_buffer_pool_dump_status String

Innodb_buffer_pool_load_status

String

Innodb_buffer_pool_pages_data

Integer

Innodb_buffer_pool_pages_dirty

Integer

Innodb_buffer_pool_pages_flushed Integer

Innodb_buffer_pool_pages_free

Integer

Innodb_buffer_pool_pages_latched Integer

Innodb_buffer_pool_pages_misc

Integer

Innodb_buffer_pool_pages_total

Integer

728

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Innodb_buffer_pool_read_ahead

Integer

Innodb_buffer_pool_read_ahead_evicted

Integer

Innodb_buffer_pool_read_ahead_rndInteger

Innodb_buffer_pool_read_requests Integer

Innodb_buffer_pool_reads

Integer

Innodb_buffer_pool_resize_status String

Innodb_buffer_pool_wait_free

Integer

Innodb_buffer_pool_write_requests Integer

Innodb_data_fsyncs

Innodb_data_pending_fsyncs

Innodb_data_pending_reads

Innodb_data_pending_writes

Innodb_data_read

Innodb_data_reads

Innodb_data_writes

Innodb_data_written

Innodb_dblwr_pages_written

Innodb_dblwr_writes

Innodb_have_atomic_builtins

Innodb_log_waits

Innodb_log_write_requests

Innodb_log_writes

Innodb_num_open_files

Innodb_os_log_fsyncs

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Innodb_os_log_pending_fsyncs

Integer

Innodb_os_log_pending_writes

Integer

Innodb_os_log_written

Innodb_page_size

Innodb_pages_created

Innodb_pages_read

Innodb_pages_written

Integer

Integer

Integer

Integer

Integer

Innodb_row_lock_current_waits

Integer

Innodb_row_lock_time

Innodb_row_lock_time_avg

Innodb_row_lock_time_max

Innodb_row_lock_waits

Innodb_rows_deleted

Innodb_rows_inserted

Integer

Integer

Integer

Integer

Integer

Integer

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

729

Server Status Variable Reference

Variable Type

Variable Scope

Variable Name

Innodb_rows_read

Innodb_rows_updated

Integer

Integer

Innodb_truncated_status_writes

Integer

Key_blocks_not_flushed

Key_blocks_unused

Key_blocks_used

Key_read_requests

Key_reads

Key_write_requests

Key_writes

Last_query_cost

Last_query_partial_plans

Locked_connects

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Numeric

Integer

Integer

Max_execution_time_exceeded

Integer

Max_execution_time_set

Integer

Max_execution_time_set_failed

Integer

Max_used_connections

Integer

Max_used_connections_time

Datetime

mecab_charset

Mysqlx_address

Mysqlx_bytes_received

Mysqlx_bytes_sent

String

String

Integer

Integer

Mysqlx_connection_accept_errors Integer

Mysqlx_connection_errors

Mysqlx_connections_accepted

Mysqlx_connections_closed

Mysqlx_connections_rejected

Mysqlx_crud_create_view

Mysqlx_crud_delete

Mysqlx_crud_drop_view

Mysqlx_crud_find

Mysqlx_crud_insert

Mysqlx_crud_modify_view

Mysqlx_crud_update

Mysqlx_errors_sent

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Mysqlx_errors_unknown_message_type

Integer

Mysqlx_expect_close

Mysqlx_expect_open

Integer

Integer

730

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

Session

Global

Both

Both

Both

Global

Global

Global

Global

Both

Both

Both

Both

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Server Status Variable Reference

Variable Type

Variable Scope

Variable Name

Mysqlx_init_error

Mysqlx_notice_other_sent

Mysqlx_notice_warning_sent

Mysqlx_port

Mysqlx_rows_sent

Mysqlx_sessions

Mysqlx_sessions_accepted

Mysqlx_sessions_closed

Mysqlx_sessions_fatal_error

Mysqlx_sessions_killed

Mysqlx_sessions_rejected

Mysqlx_socket

Integer

Integer

Integer

String

Integer

Integer

Integer

Integer

Integer

Integer

Integer

String

Mysqlx_ssl_accept_renegotiates

Integer

Mysqlx_ssl_accepts

Mysqlx_ssl_active

Mysqlx_ssl_cipher

Mysqlx_ssl_cipher_list

Mysqlx_ssl_ctx_verify_depth

Mysqlx_ssl_ctx_verify_mode

Mysqlx_ssl_finished_accepts

Mysqlx_ssl_server_not_after

Mysqlx_ssl_server_not_before

Mysqlx_ssl_verify_depth

Mysqlx_ssl_verify_mode

Mysqlx_ssl_version

Mysqlx_stmt_create_collection

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Mysqlx_stmt_create_collection_indexInteger

Mysqlx_stmt_disable_notices

Mysqlx_stmt_drop_collection

Integer

Integer

Mysqlx_stmt_drop_collection_indexInteger

Mysqlx_stmt_enable_notices

Integer

Mysqlx_stmt_ensure_collection

String

Mysqlx_stmt_execute_mysqlx

Mysqlx_stmt_execute_sql

Mysqlx_stmt_execute_xplugin

Mysqlx_stmt_kill_client

Mysqlx_stmt_list_clients

Mysqlx_stmt_list_notices

Integer

Integer

Integer

Integer

Integer

Integer

Both

Both

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

Both

731

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Mysqlx_stmt_list_objects

Mysqlx_stmt_ping

Mysqlx_worker_threads

Mysqlx_worker_threads_active

Integer

Integer

Integer

Integer

Ndb_api_adaptive_send_deferred_count

Integer

Ndb_api_adaptive_send_deferred_count_session

Integer

Ndb_api_adaptive_send_deferred_count_slave

Integer

Ndb_api_adaptive_send_forced_count

Integer

Ndb_api_adaptive_send_forced_count_session

Integer

Ndb_api_adaptive_send_forced_count_slave

Integer

Ndb_api_adaptive_send_unforced_count

Integer

Ndb_api_adaptive_send_unforced_count_session

Integer

Ndb_api_adaptive_send_unforced_count_slave

Integer

Ndb_api_bytes_received_count

Integer

Ndb_api_bytes_received_count_session

Integer

Ndb_api_bytes_received_count_slaveInteger

Ndb_api_bytes_sent_count

Integer

Ndb_api_bytes_sent_count_sessionInteger

Ndb_api_bytes_sent_count_slave Integer

Ndb_api_event_bytes_count

Integer

Ndb_api_event_bytes_count_injectorInteger

Ndb_api_event_data_count

Integer

Ndb_api_event_data_count_injectorInteger

Ndb_api_event_nondata_count

Integer

Ndb_api_event_nondata_count_injector

Integer

Ndb_api_pk_op_count

Integer

Ndb_api_pk_op_count_session

Integer

Ndb_api_pk_op_count_slave

Ndb_api_pruned_scan_count

Integer

Integer

Ndb_api_pruned_scan_count_sessionInteger

Ndb_api_pruned_scan_count_slaveInteger

Ndb_api_range_scan_count

Integer

Ndb_api_range_scan_count_sessionInteger

Ndb_api_range_scan_count_slave Integer

Ndb_api_read_row_count

Integer

Ndb_api_read_row_count_session Integer

Ndb_api_read_row_count_slave

Integer

Ndb_api_scan_batch_count

Integer

732

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

Global

Global

Session

Global

Global

Global

Global

Global

Global

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Ndb_api_scan_batch_count_sessionInteger

Ndb_api_scan_batch_count_slave Integer

Ndb_api_table_scan_count

Integer

Ndb_api_table_scan_count_sessionInteger

Ndb_api_table_scan_count_slave Integer

Ndb_api_trans_abort_count

Integer

Ndb_api_trans_abort_count_sessionInteger

Ndb_api_trans_abort_count_slave Integer

Ndb_api_trans_close_count

Integer

Ndb_api_trans_close_count_sessionInteger

Ndb_api_trans_close_count_slave Integer

Ndb_api_trans_commit_count

Integer

Ndb_api_trans_commit_count_sessionInteger

Ndb_api_trans_commit_count_slaveInteger

Ndb_api_trans_local_read_row_countInteger

Ndb_api_trans_local_read_row_count_session

Integer

Ndb_api_trans_local_read_row_count_slave

Integer

Ndb_api_trans_start_count

Integer

Ndb_api_trans_start_count_sessionInteger

Ndb_api_trans_start_count_slave Integer

Ndb_api_uk_op_count

Integer

Ndb_api_uk_op_count_session

Integer

Ndb_api_uk_op_count_slave

Integer

Ndb_api_wait_exec_complete_countInteger

Ndb_api_wait_exec_complete_count_session

Integer

Integer
Ndb_api_wait_exec_complete_count_slave

Ndb_api_wait_meta_request_countInteger

Ndb_api_wait_meta_request_count_session

Integer

Integer
Ndb_api_wait_meta_request_count_slave

Ndb_api_wait_nanos_count

Integer

Ndb_api_wait_nanos_count_sessionInteger

Ndb_api_wait_nanos_count_slave Integer

Ndb_api_wait_scan_result_count

Integer

Integer
Ndb_api_wait_scan_result_count_session

Ndb_api_wait_scan_result_count_slaveInteger

Ndb_cluster_node_id

Ndb_config_from_host

Ndb_config_from_port

Integer

Integer

Integer

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Session

Global

Global

Both

Both

733

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Ndb_conflict_fn_epoch

Ndb_conflict_fn_epoch_trans

Ndb_conflict_fn_epoch2

Ndb_conflict_fn_epoch2_trans

Ndb_conflict_fn_max

Ndb_conflict_fn_max_del_win

Ndb_conflict_fn_old

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Ndb_conflict_last_conflict_epoch

Integer

Ndb_conflict_last_stable_epoch

Integer

Ndb_conflict_reflected_op_discard_count

Integer

Integer
Ndb_conflict_reflected_op_prepare_count

Ndb_conflict_refresh_op_count

Integer

Integer
Ndb_conflict_trans_conflict_commit_count

Ndb_conflict_trans_detect_iter_countInteger

Ndb_conflict_trans_reject_count

Integer

Ndb_conflict_trans_row_conflict_count

Integer

Ndb_conflict_trans_row_reject_countInteger

Ndb_epoch_delete_delete_count

Integer

Ndb_execute_count

Integer

Ndb_last_commit_epoch_server

Integer

Ndb_last_commit_epoch_session Integer

Ndb_cluster_node_id

Ndb_number_of_data_nodes

Ndb_pruned_scan_count

Ndb_pushed_queries_defined

Ndb_pushed_queries_dropped

Integer

Integer

Integer

Integer

Integer

Ndb_pushed_queries_executed

Integer

Ndb_pushed_reads

Ndb_scan_count

Integer

Integer

Ndb_slave_max_replicated_epoch Integer

Not_flushed_delayed_rows

Integer

Ongoing_anonymous_gtid_violating_transaction_count

Integer

Ongoing_anonymous_transaction_count

Integer

Ongoing_automatic_gtid_violating_transaction_count

Integer

Open_files

Open_streams

Open_table_definitions

Open_tables

Integer

Integer

Integer

Integer

734

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Server Status Variable Reference

Variable Type

Variable Scope

Variable Name

Opened_files

Opened_table_definitions

Opened_tables

Integer

Integer

Integer

Performance_schema_accounts_lostInteger

Integer
Performance_schema_cond_classes_lost

Integer
Performance_schema_cond_instances_lost

Performance_schema_digest_lost

Integer

Performance_schema_file_classes_lost

Integer

Performance_schema_file_handles_lost

Integer

Integer
Performance_schema_file_instances_lost

Performance_schema_hosts_lost

Integer

Performance_schema_index_stat_lost

Integer

Performance_schema_locker_lost

Integer

Performance_schema_memory_classes_lost

Integer

Integer
Performance_schema_metadata_lock_lost

Integer
Performance_schema_mutex_classes_lost

Performance_schema_mutex_instances_lost

Integer

Performance_schema_nested_statement_lost

Integer

Performance_schema_prepared_statements_lost

Integer

Performance_schema_program_lostInteger

Integer
Performance_schema_rwlock_classes_lost

Performance_schema_rwlock_instances_lost

Integer

Performance_schema_session_connect_attrs_lost

Integer

Integer
Performance_schema_socket_classes_lost

Performance_schema_socket_instances_lost

Integer

Integer
Performance_schema_stage_classes_lost

Performance_schema_statement_classes_lost

Integer

Integer
Performance_schema_table_handles_lost

Integer
Performance_schema_table_instances_lost

Integer
Performance_schema_table_lock_stat_lost

Integer
Performance_schema_thread_classes_lost

Performance_schema_thread_instances_lost

Integer

Performance_schema_users_lost

Integer

Prepared_stmt_count

Qcache_free_blocks

Qcache_free_memory

Qcache_hits

Qcache_inserts

Integer

Integer

Integer

Integer

Integer

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

735

Server Status Variable Reference

Variable Name

Variable Type

Variable Scope

Qcache_lowmem_prunes

Qcache_not_cached

Qcache_queries_in_cache

Qcache_total_blocks

Queries

Questions

Integer

Integer

Integer

Integer

Integer

Integer

Rewriter_number_loaded_rules

Integer

Rewriter_number_reloads

Integer

Rewriter_number_rewritten_queriesInteger

Rewriter_reload_error

Boolean

Rpl_semi_sync_master_clients

Integer

Integer
Rpl_semi_sync_master_net_avg_wait_time

Rpl_semi_sync_master_net_wait_timeInteger

Rpl_semi_sync_master_net_waits Integer

Rpl_semi_sync_master_no_times Integer

Rpl_semi_sync_master_no_tx

Integer

Rpl_semi_sync_master_status

Boolean

Integer
Rpl_semi_sync_master_timefunc_failures

Integer
Rpl_semi_sync_master_tx_avg_wait_time

Rpl_semi_sync_master_tx_wait_timeInteger

Rpl_semi_sync_master_tx_waits

Integer

Rpl_semi_sync_master_wait_pos_backtraverse

Integer

Rpl_semi_sync_master_wait_sessionsInteger

Rpl_semi_sync_master_yes_tx

Integer

Rpl_semi_sync_slave_status

Boolean

Rsa_public_key

Select_full_join

Select_full_range_join

Select_range

Select_range_check

Select_scan

Slave_heartbeat_period

Slave_last_heartbeat

Slave_open_temp_tables

Slave_received_heartbeats

Slave_retried_transactions

String

Integer

Integer

Integer

Integer

Integer

Numeric

Datetime

Integer

Integer

Integer

Slave_rows_last_search_algorithm_usedString

Slave_running

String

736

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Server Status Variable Reference

Variable Type

Variable Scope

Variable Name

Slow_launch_threads

Slow_queries

Sort_merge_passes

Sort_range

Sort_rows

Sort_scan

Ssl_accept_renegotiates

Ssl_accepts

Ssl_callback_cache_hits

Ssl_cipher

Ssl_cipher_list

Ssl_client_connects

Ssl_connect_renegotiates

Ssl_ctx_verify_depth

Ssl_ctx_verify_mode

Ssl_default_timeout

Ssl_finished_accepts

Ssl_finished_connects

Ssl_server_not_after

Ssl_server_not_before

Ssl_session_cache_hits

Ssl_session_cache_misses

Ssl_session_cache_mode

Ssl_session_cache_overflows

Ssl_session_cache_size

Ssl_session_cache_timeouts

Ssl_sessions_reused

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

String

String

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

String

Integer

Integer

Integer

Integer

Ssl_used_session_cache_entries Integer

Ssl_verify_depth

Ssl_verify_mode

Ssl_version

Table_locks_immediate

Table_locks_waited

Table_open_cache_hits

Table_open_cache_misses

Table_open_cache_overflows

Tc_log_max_pages_used

Tc_log_page_size

Integer

Integer

String

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Both

Both

Both

Both

Both

Both

Global

Global

Global

Both

Both

Global

Global

Global

Global

Both

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Session

Global

Both

Both

Both

Global

Global

Both

Both

Both

Global

Global

737

Server Command Options

Variable Type

Variable Scope

Variable Name

Tc_log_page_waits

Threads_cached

Threads_connected

Threads_created

Threads_running

Uptime

Uptime_since_flush_status

Integer

Integer

Integer

Integer

Integer

Integer

Integer

validate_password_dictionary_file_last_parsed

Datetime

validate_password_dictionary_file_words_count

Integer

5.1.6 Server Command Options

Global

Global

Global

Global

Global

Global

Global

Global

Global

When you start the mysqld server, you can specify program options using any of the methods described
in Section 4.2.2, “Specifying Program Options”. The most common methods are to provide options in an
option file or on the command line. However, in most cases it is desirable to make sure that the server
uses the same options each time it runs. The best way to ensure this is to list them in an option file. See
Section 4.2.2.2, “Using Option Files”. That section also describes option file format and syntax.

mysqld reads options from the [mysqld] and [server] groups. mysqld_safe reads options from the
[mysqld], [server], [mysqld_safe], and [safe_mysqld] groups. mysql.server reads options
from the [mysqld] and [mysql.server] groups.

An embedded MySQL server usually reads options from the [server], [embedded], and
[xxxxx_SERVER] groups, where xxxxx is the name of the application into which the server is embedded.

mysqld accepts many command options. For a brief summary, execute this command:

mysqld --help

To see the full list, use this command:

mysqld --verbose --help

Some of the items in the list are actually system variables that can be set at server startup. These can
be displayed at runtime using the SHOW VARIABLES statement. Some items displayed by the preceding
mysqld command do not appear in SHOW VARIABLES output; this is because they are options only and
not system variables.

The following list shows some of the most common server options. Additional options are described in
other sections:

• Options that affect security: See Section 6.1.4, “Security-Related mysqld Options and Variables”.

• SSL-related options: See Command Options for Encrypted Connections.

• Binary log control options: See Section 5.4.4, “The Binary Log”.

• Replication-related options: See Section 16.1.6, “Replication and Binary Logging Options and Variables”.

• Options for loading plugins such as pluggable storage engines: See Section 5.5.1, “Installing and

Uninstalling Plugins”.

• Options specific to particular storage engines: See Section 14.15, “InnoDB Startup Options and System

Variables” and Section 15.2.1, “MyISAM Startup Options”.

738

Server Command Options

Some options control the size of buffers or caches. For a given buffer, the server might need to allocate
internal data structures. These structures typically are allocated from the total memory allocated to the
buffer, and the amount of space required might be platform dependent. This means that when you assign
a value to an option that controls a buffer size, the amount of space actually available might differ from
the value assigned. In some cases, the amount might be less than the value assigned. It is also possible
that the server adjusts a value upward. For example, if you assign a value of 0 to an option for which the
minimal value is 1024, the server sets the value to 1024.

Values for buffer sizes, lengths, and stack sizes are given in bytes unless otherwise specified.

Some options take file name values. Unless otherwise specified, the default file location is the data
directory if the value is a relative path name. To specify the location explicitly, use an absolute path name.
Suppose that the data directory is /var/mysql/data. If a file-valued option is given as a relative path
name, it is located under /var/mysql/data. If the value is an absolute path name, its location is as given
by the path name.

You can also set the values of server system variables at server startup by using variable names as
options. To assign a value to a server system variable, use an option of the form --var_name=value. For
example, --sort_buffer_size=384M sets the sort_buffer_size variable to a value of 384MB.

When you assign a value to a variable, MySQL might automatically correct the value to stay within a given
range, or adjust the value to the closest permissible value if only certain values are permitted.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement,
specify this maximum by using an option of the form --maximum-var_name=value at server startup.

You can change the values of most system variables at runtime with the SET statement. See
Section 13.7.4.1, “SET Syntax for Variable Assignment”.

Section 5.1.7, “Server System Variables”, provides a full description for all variables, and additional
information for setting them at server startup and runtime. For information on changing system variables,
see Section 5.1.1, “Configuring the Server”.

• --help, -?

Command-Line Format

--help

Display a short help message and exit. Use both the --verbose and --help options to see the full
message.

• --allow-suspicious-udfs

Command-Line Format

--allow-suspicious-udfs[={OFF|ON}]

Type

Default Value

Boolean

OFF

This option controls whether loadable functions that have only an xxx symbol for the main function can
be loaded. By default, the option is off and only loadable functions that have at least one auxiliary symbol
can be loaded; this prevents attempts at loading functions from shared object files other than those
containing legitimate functions. See Loadable Function Security Precautions.

• --ansi

Command-Line Format

--ansi

739

Server Command Options

Use standard (ANSI) SQL syntax instead of MySQL syntax. For more precise control over the server
SQL mode, use the --sql-mode option instead. See Section 1.6, “MySQL Standards Compliance”, and
Section 5.1.10, “Server SQL Modes”.

•   --basedir=dir_name, -b dir_name

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--basedir=dir_name

basedir

Global

No

Directory name

configuration-dependent default

The path to the MySQL installation directory. This option sets the basedir system variable.

• --bootstrap

Command-Line Format

Deprecated

--bootstrap

Yes

This option is used by the mysql_install_db program to create the MySQL privilege tables without
having to start a full MySQL server.

Note

mysql_install_db is deprecated because its functionality has been integrated
into mysqld, the MySQL server. Consequently, the --bootstrap server option
that mysql_install_db passes to mysqld is also deprecated. To initialize a
MySQL installation, invoke mysqld with the --initialize or --initialize-
insecure option. For more information, see Section 2.9.1, “Initializing the Data
Directory”. Expect mysql_install_db and the --bootstrap server option to
be removed in a future release of MySQL.

--bootstrap is mutually exclusive with --daemonize, --initialize, and --initialize-
insecure.

Global transaction identifiers (GTIDs) are not disabled when --bootstrap is used. --bootstrap was
used (Bug #20980271). See Section 16.1.3, “Replication with Global Transaction Identifiers”.

When the server operates in bootstap mode, some functionality is unavailable that limits the statements
permitted in any file named by the init_file system variable. For more information, see the
description of that variable. In addition, the disabled_storage_engines system variable has no
effect.

• --character-set-client-handshake

Command-Line Format

Type

--character-set-client-
handshake[={OFF|ON}]

Boolean

740

Server Command Options

Default Value

ON

Do not ignore character set information sent by the client. To ignore client information and use the
default server character set, use --skip-character-set-client-handshake; this makes MySQL
behave like MySQL 4.0.

• --chroot=dir_name, -r dir_name

Command-Line Format

Type

--chroot=dir_name

Directory name

Put the mysqld server in a closed environment during startup by using the chroot() system call. This
is a recommended security measure. Use of this option somewhat limits LOAD DATA and SELECT ...
INTO OUTFILE.

• --console

Command-Line Format

Platform Specific

--console

Windows

(Windows only.) Write the error log to stderr and stdout (the console). mysqld does not close the
console window if this option is used.

--console takes precedence over --log-error if both are given. (In MySQL 5.5 and 5.6, this is
reversed: --log-error takes precedence over --console if both are given.)

• --core-file

Command-Line Format

--core-file

When this option is used, write a core file if mysqld dies; no arguments are needed (or accepted). The
name and location of the core file is system dependent. On Linux, a core file named core.pid is written
to the current working directory of the process, which for mysqld is the data directory. pid represents
the process ID of the server process. On macOS, a core file named core.pid is written to the /cores
directory. On Solaris, use the coreadm command to specify where to write the core file and how to
name it.

For some systems, to get a core file you must also specify the --core-file-size option to
mysqld_safe. See Section 4.3.2, “mysqld_safe — MySQL Server Startup Script”. On some systems,
such as Solaris, you do not get a core file if you are also using the --user option. There might be
additional restrictions or limitations. For example, it might be necessary to execute ulimit -c
unlimited before starting the server. Consult your system documentation.

• --daemonize

Command-Line Format

--daemonize[={OFF|ON}]

Type

Boolean

741

Server Command Options

Default Value

OFF

This option causes the server to run as a traditional, forking daemon, permitting it to work with operating
systems that use systemd for process control. For more information, see Section 2.5.10, “Managing
MySQL Server with systemd”.

--daemonize is mutually exclusive with --bootstrap, --initialize, and --initialize-
insecure.

•   --datadir=dir_name, -h dir_name

Command-Line Format

System Variable

Scope

Dynamic

Type

--datadir=dir_name

datadir

Global

No

Directory name

The path to the MySQL server data directory. This option sets the datadir system variable. See the
description of that variable.

• --debug[=debug_options], -# [debug_options]

Command-Line Format

System Variable

Scope

Dynamic

Type

--debug[=debug_options]

debug

Global, Session

Yes

String

Default Value (Unix)

Default Value (Windows)

d:t:i:o,/tmp/mysqld.trace

d:t:i:O,\mysqld.trace

If MySQL is configured with the -DWITH_DEBUG=1 CMake option, you can use this option to get a trace
file of what mysqld is doing. A typical debug_options string is d:t:o,file_name. The default is
d:t:i:o,/tmp/mysqld.trace on Unix and d:t:i:O,\mysqld.trace on Windows.

Using -DWITH_DEBUG=1 to configure MySQL with debugging support enables you to use the --
debug="d,parser_debug" option when you start the server. This causes the Bison parser that is
used to process SQL statements to dump a parser trace to the server's standard error output. Typically,
this output is written to the error log.

This option may be given multiple times. Values that begin with + or - are added to or subtracted from
the previous value. For example, --debug=T --debug=+P sets the value to P:T.

For more information, see Section 5.8.3, “The DBUG Package”.

• --debug-sync-timeout[=N]

Command-Line Format

--debug-sync-timeout[=#]

Type

Integer

Controls whether the Debug Sync facility for testing and debugging is enabled. Use of Debug Sync
requires that MySQL be configured with the -DWITH_DEBUG=ON CMake option (see Section 2.8.7,

742

Server Command Options

“MySQL Source-Configuration Options”). If Debug Sync is not compiled in, this option is not available.
The option value is a timeout in seconds. The default value is 0, which disables Debug Sync. To
enable it, specify a value greater than 0; this value also becomes the default timeout for individual
synchronization points. If the option is given without a value, the timeout is set to 300 seconds.

For a description of the Debug Sync facility and how to use synchronization points, see MySQL
Internals: Test Synchronization.

• --default-time-zone=timezone

Command-Line Format

--default-time-zone=name

Type

String

Set the default server time zone. This option sets the global time_zone system variable. If this option
is not given, the default time zone is the same as the system time zone (given by the value of the
system_time_zone system variable.

The system_time_zone variable differs from time_zone. Although they might have the same value,
the latter variable is used to initialize the time zone for each client that connects. See Section 5.1.13,
“MySQL Server Time Zone Support”.

• --defaults-extra-file=file_name

Read this option file after the global option file but (on Unix) before the user option file. If the file does
not exist or is otherwise inaccessible, an error occurs. If file_name is not an absolute path name, it is
interpreted relative to the current directory. This must be the first option on the command line if it is used.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-file=file_name

Read only the given option file. If the file does not exist or is otherwise inaccessible, an error occurs. If
file_name is not an absolute path name, it is interpreted relative to the current directory.

Note

This must be the first option on the command line if it is used, except that if the
server is started with the --defaults-file and --install (or --install-
manual) options, --install (or --install-manual) must be first.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --defaults-group-suffix=str

Read not only the usual option groups, but also groups with the usual names and a suffix of str. For
example, mysqld normally reads the [mysqld] group. If this option is given as --defaults-group-
suffix=_other, mysqld also reads the [mysqld_other] group.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --des-key-file=file_name

Command-Line Format

--des-key-file=file_name

743

Server Command Options

Deprecated

Yes

Read the default DES keys from this file. These keys are used by the DES_ENCRYPT() and
DES_DECRYPT() functions.

Note

The DES_ENCRYPT() and DES_DECRYPT() functions are deprecated in MySQL
5.7, are removed in MySQL 8.0, and should no longer be used. Consequently, --
des-key-file also is deprecated and is removed in MySQL 8.0.

• --disable-partition-engine-check

Command-Line Format

--disable-partition-engine-
check[={OFF|ON}]

Introduced

Deprecated

Type

Default Value (≥ 5.7.21)
Default Value (≥ 5.7.17, ≤ 5.7.20)

5.7.17

5.7.17

Boolean

ON

OFF

Whether to disable the startup check for tables with nonnative partitioning.

As of MySQL 5.7.17, the generic partitioning handler in the MySQL server is deprecated, and is removed
in MySQL 8.0, when the storage engine used for a given table is expected to provide its own (“native”)
partitioning handler. Currently, only the InnoDB and NDB storage engines do this.

Use of tables with nonnative partitioning results in an ER_WARN_DEPRECATED_SYNTAX warning. In
MySQL 5.7.17 through 5.7.20, the server automatically performs a check at startup to identify tables that
use nonnative partitioning; for any that are found, the server writes a message to its error log. To disable
this check, use the --disable-partition-engine-check option. In MySQL 5.7.21 and later, this
check is not performed; in these versions, you must start the server with --disable-partition-
engine-check=false, if you wish for the server to check for tables using the generic partitioning
handler (Bug #85830, Bug #25846957).

Use of tables with nonnative partitioning results in an ER_WARN_DEPRECATED_SYNTAX warning. Also,
the server performs a check at startup to identify tables that use nonnative partitioning; for any found,
the server writes a message to its error log. To disable this check, use the --disable-partition-
engine-check option.

To prepare for migration to MySQL 8.0, any table with nonnative partitioning should be changed to use
an engine that provides native partitioning, or be made nonpartitioned. For example, to change a table to
InnoDB, execute this statement:

ALTER TABLE table_name ENGINE = INNODB;

• --early-plugin-load=plugin_list

Command-Line Format

--early-plugin-load=plugin_list

Introduced

Type

744

Default Value (≥ 5.7.12)

5.7.11

String

empty string

Server Command Options

Default Value (5.7.11)

keyring_file plugin library file name

This option tells the server which plugins to load before loading mandatory built-in plugins and
before storage engine initialization. Early loading is supported only for plugins compiled with
PLUGIN_OPT_ALLOW_EARLY. If multiple --early-plugin-load options are given, only the last one
applies.

The option value is a semicolon-separated list of plugin_library and name=plugin_library
values. Each plugin_library is the name of a library file that contains plugin code, and each name
is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the
server loads all plugins in the library. With a preceding plugin name, the server loads only the named
plugin from the libary. The server looks for plugin library files in the directory named by the plugin_dir
system variable.

For example, if plugins named myplug1 and myplug2 are contained in the plugin library files
myplug1.so and myplug2.so, use this option to perform an early plugin load:

mysqld --early-plugin-load="myplug1=myplug1.so;myplug2=myplug2.so"

Quotes surround the argument value because otherwise some command interpreters interpret semicolon
(;) as a special character. (For example, Unix shells treat it as a command terminator.)

Each named plugin is loaded early for a single invocation of mysqld only. After a restart, the plugin is
not loaded early unless --early-plugin-load is used again.

If the server is started using --initialize or --initialize-insecure, plugins specified by --
early-plugin-load are not loaded.

If the server is run with --help, plugins specified by --early-plugin-load are loaded but not
initialized. This behavior ensures that plugin options are displayed in the help message.

InnoDB tablespace encryption relies on the MySQL Keyring for encryption key management, and
the keyring plugin to be used must be loaded prior to storage engine initialization to facilitate InnoDB
recovery for encrypted tables. For example, administrators who want the keyring_file plugin
loaded at startup should use --early-plugin-load with the appropriate option value (such as
keyring_file.so on Unix and Unix-like systems or keyring_file.dll on Windows).

Important

In MySQL 5.7.11, the default --early-plugin-load value is the name of the
keyring_file plugin library file, causing that plugin to be loaded by default. In
MySQL 5.7.12 and higher, the default --early-plugin-load value is empty;
to load the keyring_file plugin, you must explicitly specify the option with a
value naming the keyring_file plugin library file.

This change of default --early-plugin-load value introduces an
incompatibility for InnoDB tablespace encryption for upgrades from 5.7.11 to
5.7.12 or higher. Administrators who have encrypted InnoDB tablespaces must
take explicit action to ensure continued loading of the keyring plugin: Start the
server with an --early-plugin-load option that names the plugin library file.
For additional information, see Section 6.4.4.1, “Keyring Plugin Installation”.

For information about InnoDB tablespace encryption, see Section 14.14, “InnoDB Data-at-Rest
Encryption”. For general information about plugin loading, see Section 5.5.1, “Installing and Uninstalling
Plugins”.

745

Server Command Options

• --exit-info[=flags], -T [flags]

Command-Line Format

--exit-info[=flags]

Type

Integer

This is a bitmask of different flags that you can use for debugging the mysqld server. Do not use this
option unless you know exactly what it does!

• --external-locking

Command-Line Format

--external-locking[={OFF|ON}]

Type

Default Value

Boolean

OFF

Enable external locking (system locking), which is disabled by default. If you use this option on a system
on which lockd does not fully work (such as Linux), it is easy for mysqld to deadlock.

To disable external locking explicitly, use --skip-external-locking.

External locking affects only MyISAM table access. For more information, including conditions under
which it can and cannot be used, see Section 8.11.5, “External Locking”.

• --flush

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--flush[={OFF|ON}]

flush

Global

Yes

Boolean

OFF

Flush (synchronize) all changes to disk after each SQL statement. Normally, MySQL does a write of all
changes to disk only after each SQL statement and lets the operating system handle the synchronizing
to disk. See Section B.3.3.3, “What to Do If MySQL Keeps Crashing”.

Note

If --flush is specified, the value of flush_time does not matter and changes
to flush_time have no effect on flush behavior.

• --gdb

Command-Line Format

--gdb[={OFF|ON}]

Type

Default Value

Boolean

OFF

Install an interrupt handler for SIGINT (needed to stop mysqld with ^C to set breakpoints) and disable
stack tracing and core file handling. See Section 5.8.1.4, “Debugging mysqld under gdb”.

746

Server Command Options

• --ignore-db-dir=dir_name

Command-Line Format

--ignore-db-dir=dir_name

Deprecated

Type

5.7.16

Directory name

This option tells the server to ignore the given directory name for purposes of the SHOW DATABASES
statement or INFORMATION_SCHEMA tables. For example, if a MySQL configuration locates the data
directory at the root of a file system on Unix, the system might create a lost+found directory there that
the server should ignore. Starting the server with --ignore-db-dir=lost+found causes that name
not to be listed as a database.

To specify more than one name, use this option multiple times, once for each name. Specifying the
option with an empty value (that is, as --ignore-db-dir=) resets the directory list to the empty list.

Instances of this option given at server startup are used to set the ignore_db_dirs system variable.

This option is deprecated in MySQL 5.7. With the introduction of the data dictionary in MySQL 8.0, it
became superfluous and was removed in that version.

• --initialize

Command-Line Format

--initialize[={OFF|ON}]

Type

Default Value

Boolean

OFF

This option is used to initialize a MySQL installation by creating the data directory and populating the
tables in the mysql system database. For more information, see Section 2.9.1, “Initializing the Data
Directory”.

This option limits the effects of, or is not compatible with, a number of other startup options for the
MySQL server. Some of the most common issues of this sort are noted here:

• We strongly recommend, when initializing the data directory with --initialize, that you specify no
additional options other than --datadir, other options used for setting directory locations such as --
basedir, and possibly --user, if required. Options for the running MySQL server can be specified
when starting it once initialization has been completed and mysqld has shut down. This also applies
when using --initialize-insecure instead of --initialize.

• When the server is started with --initialize, some functionality is unavailable that limits the

statements permitted in any file named by the init_file system variable. For more information, see
the description of that variable. In addition, the disabled_storage_engines system variable has
no effect.

• The --ndbcluster option is ignored when used together with --initialize.

• --initialize is mutually exclusive with --bootstrap and --daemonize.

The items in the preceding list also apply when initializing the server using the --initialize-
insecure option.

• --initialize-insecure

Command-Line Format

--initialize-insecure[={OFF|ON}]

747

Server Command Options

Type

Default Value

Boolean

OFF

This option is used to initialize a MySQL installation by creating the data directory and populating the
tables in the mysql system database. This option implies --initialize, and the same restrictions
and limitations apply; for more information, see the description of that option, and Section 2.9.1,
“Initializing the Data Directory”.

Warning

This option creates a MySQL root user with an empty password, which is
insecure. For this reason, do not use it in production without setting this password
manually. See Post-Initialization root Password Assignment, for information about
how to do this.

• --innodb-xxx

Set an option for the InnoDB storage engine. The InnoDB options are listed in Section 14.15, “InnoDB
Startup Options and System Variables”.

• --install [service_name]

Command-Line Format

Platform Specific

--install [service_name]

Windows

(Windows only) Install the server as a Windows service that starts automatically during Windows startup.
The default service name is MySQL if no service_name value is given. For more information, see
Section 2.3.4.8, “Starting MySQL as a Windows Service”.

Note

If the server is started with the --defaults-file and --install options, --
install must be first.

• --install-manual [service_name]

Command-Line Format

Platform Specific

--install-manual [service_name]

Windows

(Windows only) Install the server as a Windows service that must be started manually. It does not start
automatically during Windows startup. The default service name is MySQL if no service_name value is
given. For more information, see Section 2.3.4.8, “Starting MySQL as a Windows Service”.

Note

If the server is started with the --defaults-file and --install-manual
options, --install-manual must be first.

• --language=lang_name, -L lang_name

Command-Line Format

--language=name

748

Deprecated

System Variable

Yes; use lc-messages-dir instead

language

Server Command Options

Scope

Dynamic

Type

Default Value

Global

No

Directory name

/usr/local/mysql/share/mysql/english/

The language to use for error messages. lang_name can be given as the language name or as the full
path name to the directory where the language files are installed. See Section 10.12, “Setting the Error
Message Language”.

--lc-messages-dir and --lc-messages should be used rather than --language, which
is deprecated (and handled as a synonym for --lc-messages-dir). You should expect the --
language option to be removed in a future release of MySQL.

• --large-pages

Command-Line Format

System Variable

Scope

Dynamic

Platform Specific

Type

Default Value

--large-pages[={OFF|ON}]

large_pages

Global

No

Linux

Boolean

OFF

Some hardware/operating system architectures support memory pages greater than the default (usually
4KB). The actual implementation of this support depends on the underlying hardware and operating
system. Applications that perform a lot of memory accesses may obtain performance improvements by
using large pages due to reduced Translation Lookaside Buffer (TLB) misses.

MySQL supports the Linux implementation of large page support (which is called HugeTLB in Linux).
See Section 8.12.4.3, “Enabling Large Page Support”. For Solaris support of large pages, see the
description of the --super-large-pages option.

--large-pages is disabled by default.

• --lc-messages=locale_name

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--lc-messages=name

lc_messages

Global, Session

Yes

String

en_US

The locale to use for error messages. The default is en_US. The server converts the argument to a
language name and combines it with the value of --lc-messages-dir to produce the location for the
error message file. See Section 10.12, “Setting the Error Message Language”.

749

Server Command Options

• --lc-messages-dir=dir_name

Command-Line Format

System Variable

Scope

Dynamic

Type

--lc-messages-dir=dir_name

lc_messages_dir

Global

No

Directory name

The directory where error messages are located. The server uses the value together with the value of --
lc-messages to produce the location for the error message file. See Section 10.12, “Setting the Error
Message Language”.

• --local-service

Command-Line Format

--local-service

(Windows only) A --local-service option following the service name causes the server to run
using the LocalService Windows account that has limited system privileges. If both --defaults-
file and --local-service are given following the service name, they can be in any order. See
Section 2.3.4.8, “Starting MySQL as a Windows Service”.

• --log-error[=file_name]

Command-Line Format

System Variable

Scope

Dynamic

Type

--log-error[=file_name]

log_error

Global

No

File name

Write the error log and startup messages to this file. See Section 5.4.2, “The Error Log”.

If the option names no file, the error log file name on Unix and Unix-like systems is host_name.err in
the data directory. The file name on Windows is the same, unless the --pid-file option is specified.
In that case, the file name is the PID file base name with a suffix of .err in the data directory.

If the option names a file, the error log file has that name (with an .err suffix added if the name has
no suffix), located under the data directory unless an absolute path name is given to specify a different
location.

On Windows, --console takes precedence over --log-error if both are given. In this case, the
server writes the error log to the console rather than to a file. (In MySQL 5.5 and 5.6, this is reversed: --
log-error takes precedence over --console if both are given.)

• --log-isam[=file_name]

Command-Line Format

--log-isam[=file_name]

Type

File name

Log all MyISAM changes to this file (used only when debugging MyISAM).

750

Server Command Options

• --log-raw

Command-Line Format

--log-raw[={OFF|ON}]

Type

Default Value

Boolean

OFF

Passwords in certain statements written to the general query log, slow query log, and binary log are
rewritten by the server not to occur literally in plain text. Password rewriting can be suppressed for
the general query log by starting the server with the --log-raw option. This option may be useful
for diagnostic purposes, to see the exact text of statements as received by the server, but for security
reasons is not recommended for production use.

If a query rewrite plugin is installed, the --log-raw option affects statement logging as follows:

• Without --log-raw, the server logs the statement returned by the query rewrite plugin. This may

differ from the statement as received.

• With --log-raw, the server logs the original statement as received.

For more information, see Section 6.1.2.3, “Passwords and Logging”.

• --log-short-format

Command-Line Format

Type

Default Value

--log-short-format[={OFF|ON}]

Boolean

OFF

Log less information to the slow query log, if it has been activated.

• --log-tc=file_name

Command-Line Format

Type

Default Value

--log-tc=file_name

File name

tc.log

The name of the memory-mapped transaction coordinator log file (for XA transactions that affect multiple
storage engines when the binary log is disabled). The default name is tc.log. The file is created under
the data directory if not given as a full path name. This option is unused.

• --log-tc-size=size

Command-Line Format

Type

Default Value (64-bit platforms, ≥ 5.7.21)
Default Value (64-bit platforms, ≤ 5.7.20)
Default Value (32-bit platforms, ≥ 5.7.21)
Default Value (32-bit platforms, ≤ 5.7.20)
Minimum Value

--log-tc-size=#

Integer

6 * page size

24576

6 * page size

24576

6 * page size

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

751

Server Command Options

The size in bytes of the memory-mapped transaction coordinator log. The default and minimum values
are 6 times the page size, and the value must be a multiple of the page size. (Before MySQL 5.7.21, the
default size is 24KB.)

• --log-warnings[=level], -W [level]

Command-Line Format

--log-warnings[=#]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Yes

log_warnings

Global

Yes

Integer

2

0

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

Note

The log_error_verbosity system variable is preferred over, and should
be used instead of, the --log-warnings option or log_warnings system
variable. For more information, see the descriptions of log_error_verbosity
and log_warnings. The --log-warnings command-line option and
log_warnings system variable are deprecated; expect them to be removed in a
future release of MySQL.

Whether to produce additional warning messages to the error log. This option is enabled by default.
To disable it, use --log-warnings=0. Specifying the option without a level value increments the
current value by 1. The server logs messages about statements that are unsafe for statement-based
logging if the value is greater than 0. Aborted connections and access-denied errors for new connection
attempts are logged if the value is greater than 1. See Section B.3.2.9, “Communication Errors and
Aborted Connections”.

• --memlock

Command-Line Format

--memlock[={OFF|ON}]

Type

Default Value

Boolean

OFF

Lock the mysqld process in memory. This option might help if you have a problem where the operating
system is causing mysqld to swap to disk.

--memlock works on systems that support the mlockall() system call; this includes Solaris, most
Linux distributions that use a 2.4 or higher kernel, and perhaps other Unix systems. On Linux systems,

752

Server Command Options

you can tell whether or not mlockall() (and thus this option) is supported by checking to see whether
or not it is defined in the system mman.h file, like this:

$> grep mlockall /usr/include/sys/mman.h

If mlockall() is supported, you should see in the output of the previous command something like the
following:

extern int mlockall (int __flags) __THROW;

Important

Use of this option may require you to run the server as root, which, for reasons
of security, is normally not a good idea. See Section 6.1.5, “How to Run MySQL
as a Normal User”.

On Linux and perhaps other systems, you can avoid the need to run the server as
root by changing the limits.conf file. See the notes regarding the memlock
limit in Section 8.12.4.3, “Enabling Large Page Support”.

You must not use this option on a system that does not support the mlockall()
system call; if you do so, mysqld is very likely to exit as soon as you try to start it.

• --myisam-block-size=N

Command-Line Format

--myisam-block-size=#

Type

Default Value

Minimum Value

Maximum Value

Integer

1024

1024

16384

The block size to be used for MyISAM index pages.

• --no-defaults

Do not read any option files. If program startup fails due to reading unknown options from an option file,
--no-defaults can be used to prevent them from being read. This must be the first option on the
command line if it is used.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --old-style-user-limits

Command-Line Format

--old-style-user-limits[={OFF|ON}]

Type

Default Value

Boolean

OFF

Enable old-style user limits. (Before MySQL 5.0.3, account resource limits were counted separately
for each host from which a user connected rather than per account row in the user table.) See
Section 6.2.16, “Setting Account Resource Limits”.

753

Server Command Options

• --partition[=value]

Command-Line Format

--partition[={OFF|ON}]

Deprecated

Disabled by

Type

Default Value

5.7.16

skip-partition

Boolean

ON

Enables or disables user-defined partitioning support in the MySQL Server.

This option is deprecated in MySQL 5.7.16, and is removed from MySQL 8.0 because in MySQL 8.0, the
partitioning engine is replaced by native partitioning, which cannot be disabled.

• --performance-schema-xxx

Configure a Performance Schema option. For details, see Section 25.14, “Performance Schema
Command Options”.

• --plugin-load=plugin_list

Command-Line Format

--plugin-load=plugin_list

Type

String

This option tells the server to load the named plugins at startup. If multiple --plugin-load options are
given, only the last one applies. Additional plugins to load may be specified using --plugin-load-add
options.

The option value is a semicolon-separated list of plugin_library and name=plugin_library
values. Each plugin_library is the name of a library file that contains plugin code, and each name
is the name of a plugin to load. If a plugin library is named without any preceding plugin name, the
server loads all plugins in the library. With a preceding plugin name, the server loads only the named
plugin from the libary. The server looks for plugin library files in the directory named by the plugin_dir
system variable.

For example, if plugins named myplug1 and myplug2 are contained in the plugin library files
myplug1.so and myplug2.so, use this option to perform an early plugin load:

mysqld --plugin-load="myplug1=myplug1.so;myplug2=myplug2.so"

Quotes surround the argument value because otherwise some command interpreters interpret semicolon
(;) as a special character. (For example, Unix shells treat it as a command terminator.)

Each named plugin is loaded for a single invocation of mysqld only. After a restart, the plugin is not
loaded unless --plugin-load is used again. This is in contrast to INSTALL PLUGIN, which adds an
entry to the mysql.plugins table to cause the plugin to be loaded for every normal server startup.

During the normal startup sequence, the server determines which plugins to load by reading the
mysql.plugins system table. If the server is started with the --skip-grant-tables option, plugins
registered in the mysql.plugins table are not loaded and are unavailable. --plugin-load enables

754

Server Command Options

plugins to be loaded even when --skip-grant-tables is given. --plugin-load also enables
plugins to be loaded at startup that cannot be loaded at runtime.

This option does not set a corresponding system variable. The output of SHOW PLUGINS provides
information about loaded plugins. More detailed information can be found in the Information Schema
PLUGINS table. See Section 5.5.2, “Obtaining Server Plugin Information”.

For additional information about plugin loading, see Section 5.5.1, “Installing and Uninstalling Plugins”.

• --plugin-load-add=plugin_list

Command-Line Format

--plugin-load-add=plugin_list

Type

String

This option complements the --plugin-load option. --plugin-load-add adds a plugin or plugins
to the set of plugins to be loaded at startup. The argument format is the same as for --plugin-load.
--plugin-load-add can be used to avoid specifying a large set of plugins as a single long unwieldy
--plugin-load argument.

--plugin-load-add can be given in the absence of --plugin-load, but any instance of --
plugin-load-add that appears before --plugin-load. has no effect because --plugin-load
resets the set of plugins to load. In other words, these options:

--plugin-load=x --plugin-load-add=y

are equivalent to this option:

--plugin-load="x;y"

But these options:

--plugin-load-add=y --plugin-load=x

are equivalent to this option:

--plugin-load=x

This option does not set a corresponding system variable. The output of SHOW PLUGINS provides
information about loaded plugins. More detailed information can be found in the Information Schema
PLUGINS table. See Section 5.5.2, “Obtaining Server Plugin Information”.

For additional information about plugin loading, see Section 5.5.1, “Installing and Uninstalling Plugins”.

• --plugin-xxx

Specifies an option that pertains to a server plugin. For example, many storage engines can be built as
plugins, and for such engines, options for them can be specified with a --plugin prefix. Thus, the --
innodb-file-per-table option for InnoDB can be specified as --plugin-innodb-file-per-
table.

For boolean options that can be enabled or disabled, the --skip prefix and other alternative formats are
supported as well (see Section 4.2.2.4, “Program Option Modifiers”). For example, --skip-plugin-
innodb-file-per-table disables innodb-file-per-table.

The rationale for the --plugin prefix is that it enables plugin options to be specified unambiguously if
there is a name conflict with a built-in server option. For example, were a plugin writer to name a plugin
“sql” and implement a “mode” option, the option name might be --sql-mode, which would conflict with755

Server Command Options

the built-in option of the same name. In such cases, references to the conflicting name are resolved in
favor of the built-in option. To avoid the ambiguity, users can specify the plugin option as --plugin-
sql-mode. Use of the --plugin prefix for plugin options is recommended to avoid any question of
ambiguity.

• --port=port_num, -P port_num

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--port=port_num

port

Global

No

Integer

3306

0

65535

The port number to use when listening for TCP/IP connections. On Unix and Unix-like systems, the port
number must be 1024 or higher unless the server is started by the root operating system user. Setting
this option to 0 causes the default value to be used.

• --port-open-timeout=num

Command-Line Format

--port-open-timeout=#

Type

Default Value

Integer

0

On some systems, when the server is stopped, the TCP/IP port might not become available immediately.
If the server is restarted quickly afterward, its attempt to reopen the port can fail. This option indicates
how many seconds the server should wait for the TCP/IP port to become free if it cannot be opened. The
default is not to wait.

• --print-defaults

Print the program name and all options that it gets from option files. Password values are masked. This
must be the first option on the command line if it is used, except that it may be used immediately after --
defaults-file or --defaults-extra-file.

For additional information about this and other option-file options, see Section 4.2.2.3, “Command-Line
Options that Affect Option-File Handling”.

• --remove [service_name]

Command-Line Format

Platform Specific

--remove [service_name]

Windows

(Windows only) Remove a MySQL Windows service. The default service name is MySQL if no
service_name value is given. For more information, see Section 2.3.4.8, “Starting MySQL as a
Windows Service”.

756

Server Command Options

• --safe-user-create

Command-Line Format

--safe-user-create[={OFF|ON}]

Type

Default Value

Boolean

OFF

If this option is enabled, a user cannot create new MySQL users by using the GRANT statement unless
the user has the INSERT privilege for the mysql.user system table or any column in the table. If you
want a user to have the ability to create new users that have those privileges that the user has the right
to grant, you should grant the user the following privilege:

GRANT INSERT(user) ON mysql.user TO 'user_name'@'host_name';

This ensures that the user cannot change any privilege columns directly, but has to use the GRANT
statement to give privileges to other users.

• --skip-grant-tables

Command-Line Format

--skip-grant-tables[={OFF|ON}]

Type

Boolean

757

Server Command Options

Default Value

OFF

This option affects the server startup sequence:

• --skip-grant-tables causes the server not to read the grant tables in the mysql system

database, and thus to start without using the privilege system at all. This gives anyone with access to
the server unrestricted access to all databases.

To cause a server started with --skip-grant-tables to load the grant tables at runtime, perform a
privilege-flushing operation, which can be done in these ways:

• Issue a MySQL FLUSH PRIVILEGES statement after connecting to the server.

• Execute a mysqladmin flush-privileges or mysqladmin reload command from the

command line.

Privilege flushing might also occur implicitly as a result of other actions performed after startup,
thus causing the server to start using the grant tables. For example, mysql_upgrade flushes the
privileges during the upgrade procedure.

• --skip-grant-tables causes the server not to load certain other objects registered in the mysql

system database:

• Plugins installed using INSTALL PLUGIN and registered in the mysql.plugin system table.

To cause plugins to be loaded even when using --skip-grant-tables, use the --plugin-
load or --plugin-load-add option.

• Scheduled events installed using CREATE EVENT and registered in the mysql.event system

table.

• Loadable functions installed using CREATE FUNCTION and registered in the mysql.func system

table.

• --skip-grant-tables causes the disabled_storage_engines system variable to have no

effect.

• --skip-host-cache

Command-Line Format

--skip-host-cache

Disable use of the internal host cache for faster name-to-IP resolution. With the cache disabled, the
server performs a DNS lookup every time a client connects.

Use of --skip-host-cache is similar to setting the host_cache_size system variable to 0, but
host_cache_size is more flexible because it can also be used to resize, enable, or disable the host
cache at runtime, not just at server startup.

Starting the server with --skip-host-cache does not prevent runtime changes to the value
of host_cache_size, but such changes have no effect and the cache is not re-enabled even if
host_cache_size is set larger than 0.

For more information about how the host cache works, see Section 5.1.11.2, “DNS Lookups and the
Host Cache”.

758

Server Command Options

•   --skip-innodb

Disable the InnoDB storage engine. In this case, because the default storage engine is InnoDB,
the server cannot start unless you also use --default-storage-engine and --default-tmp-
storage-engine to set the default to some other engine for both permanent and TEMPORARY tables.

The InnoDB storage engine cannot be disabled, and the --skip-innodb option is deprecated and has
no effect. Its use results in a warning. Expect this option to be removed in a future release of MySQL.

• --skip-new

Command-Line Format

--skip-new

This option disables (what used to be considered) new, possibly unsafe behaviors. It
results in these settings: delay_key_write=OFF, concurrent_insert=NEVER,
automatic_sp_privileges=OFF. It also causes OPTIMIZE TABLE to be mapped to ALTER TABLE
for storage engines for which OPTIMIZE TABLE is not supported.

• --skip-partition

Command-Line Format

--skip-partition

Deprecated

--disable-partition

5.7.16

Disables user-defined partitioning. Partitioned tables can be seen using SHOW TABLES or by querying
the Information Schema TABLES table, but cannot be created or modified, nor can data in such tables be
accessed. All partition-specific columns in the Information Schema PARTITIONS table display NULL.

Since DROP TABLE removes table definition (.frm) files, this statement works on partitioned tables
even when partitioning is disabled using the option. The statement, however, does not remove partition
definitions associated with partitioned tables in such cases. For this reason, you should avoid dropping
partitioned tables with partitioning disabled, or take action to remove orphaned .par files manually (if
present).

Note

In MySQL 5.7, partition definition (.par) files are no longer created for partitioned
InnoDB tables. Instead, partition definitions are stored in the InnoDB internal
data dictionary. Partition definition (.par) files continue to be used for partitioned
MyISAM tables.

This option is deprecated in MySQL 5.7.16, and is removed from MySQL 8.0 because in MySQL 8.0, the
partitioning engine is replaced by native partitioning, which cannot be disabled.

• --skip-show-database

Command-Line Format

System Variable

Scope

Dynamic

Type

--skip-show-database

skip_show_database

Global

No

Boolean

759

Server Command Options

Default Value

OFF

This option sets the skip_show_database system variable that controls who is permitted to use the
SHOW DATABASES statement. See Section 5.1.7, “Server System Variables”.

• --skip-stack-trace

Command-Line Format

--skip-stack-trace

Do not write stack traces. This option is useful when you are running mysqld under a debugger. On
some systems, you also must use this option to get a core file. See Section 5.8, “Debugging MySQL”.

• --slow-start-timeout=timeout

Command-Line Format

--slow-start-timeout=#

Type

Default Value

Integer

15000

This option controls the Windows service control manager's service start timeout. The value is the
maximum number of milliseconds that the service control manager waits before trying to kill the windows
service during startup. The default value is 15000 (15 seconds). If the MySQL service takes too long to
start, you may need to increase this value. A value of 0 means there is no timeout.

• --socket=path

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (Windows)

Default Value (Other)

--socket={file_name|pipe_name}

socket

Global

No

String

MySQL

/tmp/mysql.sock

On Unix, this option specifies the Unix socket file to use when listening for local connections. The default
value is /tmp/mysql.sock. If this option is given, the server creates the file in the data directory unless
an absolute path name is given to specify a different directory. On Windows, the option specifies the pipe
name to use when listening for local connections that use a named pipe. The default value is MySQL (not
case-sensitive).

• --sql-mode=value[,value[,value...]]

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--sql-mode=name

sql_mode

Global, Session

Yes

Set

ONLY_FULL_GROUP_BY
STRICT_TRANS_TABLES
NO_ZERO_IN_DATE NO_ZERO_DATE
ERROR_FOR_DIVISION_BY_ZERO

760

Valid Values

Server Command Options

NO_AUTO_CREATE_USER
NO_ENGINE_SUBSTITUTION

ALLOW_INVALID_DATES

ANSI_QUOTES

ERROR_FOR_DIVISION_BY_ZERO

HIGH_NOT_PRECEDENCE

IGNORE_SPACE

NO_AUTO_CREATE_USER

NO_AUTO_VALUE_ON_ZERO

NO_BACKSLASH_ESCAPES

NO_DIR_IN_CREATE

NO_ENGINE_SUBSTITUTION

NO_FIELD_OPTIONS

NO_KEY_OPTIONS

NO_TABLE_OPTIONS

NO_UNSIGNED_SUBTRACTION

NO_ZERO_DATE

NO_ZERO_IN_DATE

ONLY_FULL_GROUP_BY

PAD_CHAR_TO_FULL_LENGTH

PIPES_AS_CONCAT

REAL_AS_FLOAT

STRICT_ALL_TABLES

STRICT_TRANS_TABLES

Set the SQL mode. See Section 5.1.10, “Server SQL Modes”.

Note

MySQL installation programs may configure the SQL mode during the installation
process. If the SQL mode differs from the default or from what you expect, check
for a setting in an option file that the server reads at startup.

• --ssl, --skip-ssl

Command-Line Format

--ssl[={OFF|ON}]

761

Server Command Options

Disabled by

Type

Default Value

skip-ssl

Boolean

ON

The --ssl option specifies that the server permits but does not require encrypted connections. This
option is enabled by default.

--ssl can be specified in negated form as --skip-ssl or a synonym (--ssl=OFF, --disable-
ssl). In this case, the option specifies that the server does not permit encrypted connections, regardless
of the settings of the tls_xxx and ssl_xxx system variables.

For more information about configuring whether the server permits clients to connect using SSL
and indicating where to find SSL keys and certificates, see Section 6.3.1, “Configuring MySQL to
Use Encrypted Connections”, which also describes server capabilities for certificate and key file
autogeneration and autodiscovery. Consider setting at least the ssl_cert and ssl_key system
variables on the server side and the --ssl-ca (or --ssl-capath) option on the client side.

• --standalone

Command-Line Format

Platform Specific

--standalone

Windows

Available on Windows only; instructs the MySQL server not to run as a service.

• --super-large-pages

Command-Line Format

--super-large-pages[={OFF|ON}]

Platform Specific

Type

Default Value

Solaris

Boolean

OFF

Standard use of large pages in MySQL attempts to use the largest size supported, up to 4MB. Under
Solaris, a “super large pages” feature enables uses of pages up to 256MB. This feature is available for
recent SPARC platforms. It can be enabled or disabled by using the --super-large-pages or --
skip-super-large-pages option.

• --symbolic-links, --skip-symbolic-links

Command-Line Format

--symbolic-links[={OFF|ON}]

Type

Default Value

Boolean

ON

Enable or disable symbolic link support. On Unix, enabling symbolic links means that you can link a
MyISAM index file or data file to another directory with the INDEX DIRECTORY or DATA DIRECTORY
option of the CREATE TABLE statement. If you delete or rename the table, the files that its symbolic links
point to also are deleted or renamed. See Section 8.12.3.2, “Using Symbolic Links for MyISAM Tables
on Unix”.

This option has no meaning on Windows.

762

Server Command Options

• --sysdate-is-now

Command-Line Format

--sysdate-is-now[={OFF|ON}]

Type

Default Value

Boolean

OFF

SYSDATE() by default returns the time at which it executes, not the time at which the statement in which
it occurs begins executing. This differs from the behavior of NOW(). This option causes SYSDATE() to
be a synonym for NOW(). For information about the implications for binary logging and replication, see
the description for SYSDATE() in Section 12.7, “Date and Time Functions” and for SET TIMESTAMP in
Section 5.1.7, “Server System Variables”.

• --tc-heuristic-recover={COMMIT|ROLLBACK}

Command-Line Format

--tc-heuristic-recover=name

Type

Default Value

Valid Values

Enumeration

OFF

OFF

COMMIT

ROLLBACK

The decision to use in a manual heuristic recovery.

If a --tc-heuristic-recover option is specified, the server exits regardless of whether manual
heuristic recovery is successful.

On systems with more than one storage engine capable of two-phase commit, the ROLLBACK option is
not safe and causes recovery to halt with the following error:

[ERROR] --tc-heuristic-recover rollback
strategy is not safe on systems with more than one 2-phase-commit-capable
storage engine. Aborting crash recovery.

• --temp-pool

Command-Line Format

--temp-pool[={OFF|ON}]

Deprecated

Type

Default Value (Linux)

Default Value (Other)

5.7.18

Boolean

ON

OFF

This option is ignored except on Linux. On Linux, it causes most temporary files created by the server to
use a small set of names, rather than a unique name for each new file. This works around a problem in
the Linux kernel dealing with creating many new files with different names. With the old behavior, Linux
seems to “leak” memory, because it is being allocated to the directory entry cache rather than to the disk
cache.

As of MySQL 5.7.18, this option is deprecated and is removed in MySQL 8.0.

763

Server Command Options

• --transaction-isolation=level

Command-Line Format

System Variable (≥ 5.7.20)
Scope (≥ 5.7.20)
Dynamic (≥ 5.7.20)
Type

Default Value

Valid Values

--transaction-isolation=name

transaction_isolation

Global, Session

Yes

Enumeration

REPEATABLE-READ

READ-UNCOMMITTED

READ-COMMITTED

REPEATABLE-READ

SERIALIZABLE

Sets the default transaction isolation level. The level value can be READ-UNCOMMITTED, READ-
COMMITTED, REPEATABLE-READ, or SERIALIZABLE. See Section 13.3.6, “SET TRANSACTION
Statement”.

The default transaction isolation level can also be set at runtime using the SET TRANSACTION
statement or by setting the tx_isolation (or, as of MySQL 5.7.20, transaction_isolation)
system variable.

• --transaction-read-only

Command-Line Format

System Variable (≥ 5.7.20)
Scope (≥ 5.7.20)
Dynamic (≥ 5.7.20)
Type

Default Value

--transaction-read-only[={OFF|ON}]

transaction_read_only

Global, Session

Yes

Boolean

OFF

Sets the default transaction access mode. By default, read-only mode is disabled, so the mode is read/
write.

To set the default transaction access mode at runtime, use the SET TRANSACTION statement or set
the tx_read_only (or, as of MySQL 5.7.20, transaction_read_only) system variable. See
Section 13.3.6, “SET TRANSACTION Statement”.

• --tmpdir=dir_name, -t dir_name

Command-Line Format

System Variable

Scope

Dynamic

--tmpdir=dir_name

tmpdir

Global

No

764

Server Command Options

Type

Directory name

The path of the directory to use for creating temporary files. It might be useful if your default /tmp
directory resides on a partition that is too small to hold temporary tables. This option accepts several
paths that are used in round-robin fashion. Paths should be separated by colon characters (:) on Unix
and semicolon characters (;) on Windows.

--tmpdir can be a non-permanent location, such as a directory on a memory-based file system or a
directory that is cleared when the server host restarts. If the MySQL server is acting as a replica, and
you are using a non-permanent location for --tmpdir, consider setting a different temporary directory
for the replica using the slave_load_tmpdir system variable. For a replication replica, the temporary
files used to replicate LOAD DATA statements are stored in this directory, so with a permanent location
they can survive machine restarts, although replication can now continue after a restart if the temporary
files have been removed.

For more information about the storage location of temporary files, see Section B.3.3.5, “Where MySQL
Stores Temporary Files”.

• --user={user_name|user_id}, -u {user_name|user_id}

Command-Line Format

Type

--user=name

String

Run the mysqld server as the user having the name user_name or the numeric user ID user_id.
(“User” in this context refers to a system login account, not a MySQL user listed in the grant tables.)

This option is mandatory when starting mysqld as root. The server changes its user ID during its
startup sequence, causing it to run as that particular user rather than as root. See Section 6.1.1,
“Security Guidelines”.

To avoid a possible security hole where a user adds a --user=root option to a my.cnf file (thus
causing the server to run as root), mysqld uses only the first --user option specified and produces a
warning if there are multiple --user options. Options in /etc/my.cnf and $MYSQL_HOME/my.cnf are
processed before command-line options, so it is recommended that you put a --user option in /etc/
my.cnf and specify a value other than root. The option in /etc/my.cnf is found before any other --
user options, which ensures that the server runs as a user other than root, and that a warning results if
any other --user option is found.

• --validate-user-plugins[={OFF|ON}]

Command-Line Format

--validate-user-plugins[={OFF|ON}]

Type

Boolean

765

Server System Variables

Default Value

ON

If this option is enabled (the default), the server checks each user account and produces a warning if
conditions are found that would make the account unusable:

• The account requires an authentication plugin that is not loaded.

• The account requires the sha256_password authentication plugin but the server was started with

neither SSL nor RSA enabled as required by this plugin.

Enabling --validate-user-plugins slows down server initialization and FLUSH PRIVILEGES.
If you do not require the additional checking, you can disable this option at startup to avoid the
performance decrement.

• --verbose, -v

Use this option with the --help option for detailed help.

• --version, -V

Display version information and exit.

5.1.7 Server System Variables

The MySQL server maintains many system variables that affect its operation. Most system variables
can be set at server startup using options on the command line or in an option file. Most of them can be
changed dynamically at runtime using the SET statement, which enables you to modify operation of the
server without having to stop and restart it. Some variables are read-only, and their values are determined
by the system environment, by how MySQL is installed on the system, or possibly by the options used to
compile MySQL. Most system variables have a default value, but there are exceptions, including read-only
variables. You can also use system variable values in expressions.

At runtime, setting a global system variable value requires the SUPER privilege. Setting a session system
variable value normally requires no special privileges and can be done by any user, although there are
exceptions. For more information, see Section 5.1.8.1, “System Variable Privileges”

There are several ways to see the names and values of system variables:

• To see the values that a server uses based on its compiled-in defaults and any option files that it reads,

use this command:

mysqld --verbose --help

• To see the values that a server uses based on only its compiled-in defaults, ignoring the settings in any

option files, use this command:

mysqld --no-defaults --verbose --help

• To see the current values used by a running server, use the SHOW VARIABLES statement or the

Performance Schema system variable tables. See Section 25.12.13, “Performance Schema System
Variable Tables”.

This section provides a description of each system variable. For a system variable summary table, see
Section 5.1.4, “Server System Variable Reference”. For more information about manipulation of system
variables, see Section 5.1.8, “Using System Variables”.

For additional system variable information, see these sections:

766

Server System Variables

• Section 5.1.8, “Using System Variables”, discusses the syntax for setting and displaying system variable

values.

• Section 5.1.8.2, “Dynamic System Variables”, lists the variables that can be set at runtime.

• Information on tuning system variables can be found in Section 5.1.1, “Configuring the Server”.

• Section 14.15, “InnoDB Startup Options and System Variables”, lists InnoDB system variables.

• NDB Cluster System Variables, lists system variables which are specific to NDB Cluster.

• For information on server system variables specific to replication, see Section 16.1.6, “Replication and

Binary Logging Options and Variables”.

Note

Some of the following variable descriptions refer to “enabling” or “disabling” a
variable. These variables can be enabled with the SET statement by setting them
to ON or 1, or disabled by setting them to OFF or 0. Boolean variables can be set at
startup to the values ON, TRUE, OFF, and FALSE (not case-sensitive), as well as 1
and 0. See Section 4.2.2.4, “Program Option Modifiers”.

Some system variables control the size of buffers or caches. For a given buffer, the server might need to
allocate internal data structures. These structures typically are allocated from the total memory allocated
to the buffer, and the amount of space required might be platform dependent. This means that when you
assign a value to a system variable that controls a buffer size, the amount of space actually available might
differ from the value assigned. In some cases, the amount might be less than the value assigned. It is also
possible for the server to adjust a value upward. For example, if you assign a value of 0 to a variable for
which the minimal value is 1024, the server sets the value to 1024.

Values for buffer sizes, lengths, and stack sizes are given in bytes unless otherwise specified.

Note

Some system variable descriptions include a block size, in which case a value
that is not an integer multiple of the stated block size is rounded down to the
next lower multiple of the block size before being stored by the server, that is to
FLOOR(value) * block_size.

Example: Suppose that the block size for a given variable is given as 4096, and you
set the value of the variable to 100000 (we assume that the variable's maximum
value is greater than this number). Since 100000 / 4096 = 24.4140625, the server
automatically lowers the value to 98304 (24 * 4096) before storing it.

In some cases, the stated maximum for a variable is the maximum allowed by the
MySQL parser, but is not an exact multiple of the block size. In such cases, the
effective maximum is the next lower multiple of the block size.

Example: A system variable's maxmum value is shown as 4294967295 (232-1), and
its block size is 1024. 4294967295 / 1024 = 4194303.9990234375, so if you set
this variable to its stated maximum, the value actually stored is 4194303 * 1024 =
4294966272.

Some system variables take file name values. Unless otherwise specified, the default file location is the
data directory if the value is a relative path name. To specify the location explicitly, use an absolute path
name. Suppose that the data directory is /var/mysql/data. If a file-valued variable is given as a relative
path name, it is located under /var/mysql/data. If the value is an absolute path name, its location is as
given by the path name.

767

Server System Variables

• authentication_windows_log_level

Command-Line Format

System Variable

--authentication-windows-log-level=#

authentication_windows_log_level

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

No

Integer

2

0

4

This variable is available only if the authentication_windows Windows authentication plugin is
enabled and debugging code is enabled. See Section 6.4.1.8, “Windows Pluggable Authentication”.

This variable sets the logging level for the Windows authentication plugin. The following table shows the
permitted values.

Value

0

1

2

3

4

Description

No logging

Log only error messages

Log level 1 messages and warning messages

Log level 2 messages and information notes

Log level 3 messages and debug messages

• authentication_windows_use_principal_name

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--authentication-windows-use-
principal-name[={OFF|ON}]

authentication_windows_use_principal_name

Global

No

Boolean

ON

This variable is available only if the authentication_windows Windows authentication plugin is
enabled. See Section 6.4.1.8, “Windows Pluggable Authentication”.

A client that authenticates using the InitSecurityContext() function should provide a string
identifying the service to which it connects (targetName). MySQL uses the principal name (UPN) of the
account under which the server is running. The UPN has the form user_id@computer_name and need
not be registered anywhere to be used. This UPN is sent by the server at the beginning of authentication
handshake.

This variable controls whether the server sends the UPN in the initial challenge. By default, the variable
is enabled. For security reasons, it can be disabled to avoid sending the server's account name to a

768

Server System Variables

client as cleartext. If the variable is disabled, the server always sends a 0x00 byte in the first challenge,
the client does not specify targetName, and as a result, NTLM authentication is used.

If the server fails to obtain its UPN (which happens primarily in environments that do not support
Kerberos authentication), the UPN is not sent by the server and NTLM authentication is used.

• autocommit

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--autocommit[={OFF|ON}]

autocommit

Global, Session

Yes

Boolean

ON

The autocommit mode. If set to 1, all changes to a table take effect immediately. If set to 0, you must
use COMMIT to accept a transaction or ROLLBACK to cancel it. If autocommit is 0 and you change it to
1, MySQL performs an automatic COMMIT of any open transaction. Another way to begin a transaction
is to use a START TRANSACTION or BEGIN statement. See Section 13.3.1, “START TRANSACTION,
COMMIT, and ROLLBACK Statements”.

By default, client connections begin with autocommit set to 1. To cause clients to begin with a default
of 0, set the global autocommit value by starting the server with the --autocommit=0 option. To set
the variable using an option file, include these lines:

[mysqld]
autocommit=0

• automatic_sp_privileges

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--automatic-sp-privileges[={OFF|ON}]

automatic_sp_privileges

Global

Yes

Boolean

ON

When this variable has a value of 1 (the default), the server automatically grants the EXECUTE and
ALTER ROUTINE privileges to the creator of a stored routine, if the user cannot already execute
and alter or drop the routine. (The ALTER ROUTINE privilege is required to drop the routine.) The
server also automatically drops those privileges from the creator when the routine is dropped. If
automatic_sp_privileges is 0, the server does not automatically add or drop these privileges.

The creator of a routine is the account used to execute the CREATE statement for it. This might not be
the same as the account named as the DEFINER in the routine definition.

If you start mysqld with --skip-new, automatic_sp_privileges is set to OFF.

See also Section 23.2.2, “Stored Routines and MySQL Privileges”.

769

Server System Variables

• auto_generate_certs

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--auto-generate-certs[={OFF|ON}]

auto_generate_certs

Global

No

Boolean

ON

This variable is available if the server was compiled using OpenSSL (see Section 6.3.4, “SSL Library-
Dependent Capabilities”). It controls whether the server autogenerates SSL key and certificate files in
the data directory, if they do not already exist.

At startup, the server automatically generates server-side and client-side SSL certificate and key files
in the data directory if the auto_generate_certs system variable is enabled, no SSL options other
than --ssl are specified, and the server-side SSL files are missing from the data directory. These files
enable secure client connections using SSL; see Section 6.3.1, “Configuring MySQL to Use Encrypted
Connections”.

For more information about SSL file autogeneration, including file names and characteristics, see
Section 6.3.3.1, “Creating SSL and RSA Certificates and Keys using MySQL”

The sha256_password_auto_generate_rsa_keys system variable is related but controls
autogeneration of RSA key-pair files needed for secure password exchange using RSA over unencypted
connections.

• avoid_temporal_upgrade

Command-Line Format

--avoid-temporal-upgrade[={OFF|ON}]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Yes

avoid_temporal_upgrade

Global

Yes

Boolean

OFF

This variable controls whether ALTER TABLE implicitly upgrades temporal columns found to be in
pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds
precision). Upgrading such columns requires a table rebuild, which prevents any use of fast alterations
that might otherwise apply to the operation to be performed.

This variable is disabled by default. Enabling it causes ALTER TABLE not to rebuild temporal columns
and thereby be able to take advantage of possible fast alterations.

This variable is deprecated; expect it to be removed in a future release of MySQL.

• back_log

Command-Line Format

770

System Variable

--back-log=#

back_log

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Server System Variables

Global

No

Integer

-1 (signifies autosizing; do not assign this literal
value)

1

65535

The number of outstanding connection requests MySQL can have. This comes into play when the
main MySQL thread gets very many connection requests in a very short time. It then takes some
time (although very little) for the main thread to check the connection and start a new thread. The
back_log value indicates how many requests can be stacked during this short time before MySQL
momentarily stops answering new requests. You need to increase this only if you expect a large number
of connections in a short period of time.

In other words, this value is the size of the listen queue for incoming TCP/IP connections. Your operating
system has its own limit on the size of this queue. The manual page for the Unix listen() system
call should have more details. Check your OS documentation for the maximum value for this variable.
back_log cannot be set higher than your operating system limit.

The default value is based on the following formula, capped to a limit of 900:

50 + (max_connections / 5)

• basedir

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--basedir=dir_name

basedir

Global

No

Directory name

configuration-dependent default

The path to the MySQL installation base directory.

• big_tables

Command-Line Format

System Variable

Scope

Dynamic

Type

--big-tables[={OFF|ON}]

big_tables

Global, Session

Yes

Boolean

771

Server System Variables

Default Value

OFF

If enabled, the server stores all temporary tables on disk rather than in memory. This prevents most The
table tbl_name is full errors for SELECT operations that require a large temporary table, but also
slows down queries for which in-memory tables would suffice.

The default value for new connections is OFF (use in-memory temporary tables). Normally, it should
never be necessary to enable this variable because the server is able to handle large result sets
automatically by using memory for small temporary tables and switching to disk-based tables as
required.

• bind_address

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--bind-address=addr

bind_address

Global

No

String

*

The MySQL server listens on a single network socket for TCP/IP connections. This socket is bound to a
single address, but it is possible for an address to map onto multiple network interfaces. To specify an
address, set bind_address=addr at server startup, where addr is an IPv4 or IPv6 address or a host
name. If addr is a host name, the server resolves the name to an IP address and binds to that address.
If a host name resolves to multiple IP addresses, the server uses the first IPv4 address if there are any,
or the first IPv6 address otherwise.

The server treats different types of addresses as follows:

• If the address is *, the server accepts TCP/IP connections on all server host IPv4 interfaces, and, if
the server host supports IPv6, on all IPv6 interfaces. Use this address to permit both IPv4 and IPv6
connections on all server interfaces. This value is the default.

• If the address is 0.0.0.0, the server accepts TCP/IP connections on all server host IPv4 interfaces.

• If the address is ::, the server accepts TCP/IP connections on all server host IPv4 and IPv6

interfaces.

• If the address is an IPv4-mapped address, the server accepts TCP/IP connections for that address,

in either IPv4 or IPv6 format. For example, if the server is bound to ::ffff:127.0.0.1, clients can
connect using --host=127.0.0.1 or --host=::ffff:127.0.0.1.

• If the address is a “regular” IPv4 or IPv6 address (such as 127.0.0.1 or ::1), the server accepts

TCP/IP connections only for that IPv4 or IPv6 address.

If binding to the address fails, the server produces an error and does not start.

If you intend to bind the server to a specific address, be sure that the mysql.user system table
contains an account with administrative privileges that you can use to connect to that address.
Otherwise, you cannot shut down the server. For example, if you bind the server to *, you can connect
to it using all existing accounts. But if you bind the server to ::1, it accepts connections only on that

772

Server System Variables

address. In that case, first make sure that the 'root'@'::1' account is present in the mysql.user
table so you can still connect to the server to shut it down.

This variable has no effect for the embedded server (libmysqld) and is not visible within the embedded
server.

• block_encryption_mode

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--block-encryption-mode=#

block_encryption_mode

Global, Session

Yes

String

aes-128-ecb

This variable controls the block encryption mode for block-based algorithms such as AES. It affects
encryption for AES_ENCRYPT() and AES_DECRYPT().

block_encryption_mode takes a value in aes-keylen-mode format, where keylen is the key
length in bits and mode is the encryption mode. The value is not case-sensitive. Permitted keylen
values are 128, 192, and 256. Permitted encryption modes depend on whether MySQL was compiled
using OpenSSL or yaSSL:

• For OpenSSL, permitted mode values are: ECB, CBC, CFB1, CFB8, CFB128, OFB

• For yaSSL, permitted mode values are: ECB, CBC

For example, this statement causes the AES encryption functions to use a key length of 256 bits and the
CBC mode:

SET block_encryption_mode = 'aes-256-cbc';

An error occurs for attempts to set block_encryption_mode to a value containing an unsupported
key length or a mode that the SSL library does not support.

• bulk_insert_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--bulk-insert-buffer-size=#

bulk_insert_buffer_size

Global, Session

Yes

Integer

8388608

0

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

Unit

4294967295

bytes/thread

MyISAM uses a special tree-like cache to make bulk inserts faster for INSERT ... SELECT,
INSERT ... VALUES (...), (...), ..., and LOAD DATA when adding data to nonempty tables.
773

Server System Variables

This variable limits the size of the cache tree in bytes per thread. Setting it to 0 disables this optimization.
The default value is 8MB.

• character_set_client

System Variable

Scope

Dynamic

Type

Default Value

character_set_client

Global, Session

Yes

String

utf8

The character set for statements that arrive from the client. The session value of this variable is set using
the character set requested by the client when the client connects to the server. (Many clients support
a --default-character-set option to enable this character set to be specified explicitly. See also
Section 10.4, “Connection Character Sets and Collations”.) The global value of the variable is used to set
the session value in cases when the client-requested value is unknown or not available, or the server is
configured to ignore client requests:

• The client requests a character set not known to the server. For example, a Japanese-enabled client

requests sjis when connecting to a server not configured with sjis support.

• The client is from a version of MySQL older than MySQL 4.1, and thus does not request a character

set.

• mysqld was started with the --skip-character-set-client-handshake option, which causes

it to ignore client character set configuration. This reproduces MySQL 4.0 behavior and is useful
should you wish to upgrade the server without upgrading all the clients.

Some character sets cannot be used as the client character set. Attempting to use them as the
character_set_client value produces an error. See Impermissible Client Character Sets.

• character_set_connection

System Variable

Scope

Dynamic

Type

Default Value

character_set_connection

Global, Session

Yes

String

utf8

The character set used for literals specified without a character set introducer and for number-to-string
conversion. For information about introducers, see Section 10.3.8, “Character Set Introducers”.

• character_set_database

System Variable

Scope

Dynamic

Type

Default Value

774

character_set_database

Global, Session

Yes

String

latin1

Server System Variables

Footnote

This option is dynamic, but should be set only by
server. You should not set this variable manually.

The character set used by the default database. The server sets this variable whenever the
default database changes. If there is no default database, the variable has the same value as
character_set_server.

The global character_set_database and collation_database system variables are deprecated
in MySQL 5.7; expect them to be removed in a future version of MySQL.

Assigning a value to the session character_set_database and collation_database system
variables is deprecated in MySQL 5.7 and assignments produce a warning. You should expect the
session variables to become read only in a future version of MySQL and assignments to produce an
error, while remaining possible to access the session variables to determine the database character set
and collation for the default database.

• character_set_filesystem

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--character-set-filesystem=name

character_set_filesystem

Global, Session

Yes

String

binary

The file system character set. This variable is used to interpret string literals that refer to file names, such
as in the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD_FILE() function.
Such file names are converted from character_set_client to character_set_filesystem
before the file opening attempt occurs. The default value is binary, which means that no
conversion occurs. For systems on which multibyte file names are permitted, a different value
may be more appropriate. For example, if the system represents file names using UTF-8, set
character_set_filesystem to 'utf8mb4'.

• character_set_results

System Variable

Scope

Dynamic

Type

Default Value

character_set_results

Global, Session

Yes

String

utf8

The character set used for returning query results to the client. This includes result data such as column
values, result metadata such as column names, and error messages.

• character_set_server

Command-Line Format

System Variable

Scope

Dynamic

--character-set-server=name

character_set_server

Global, Session

Yes

775

Server System Variables

Type

Default Value

String

latin1

The servers default character set. See Section 10.15, “Character Set Configuration”. If you set this
variable, you should also set collation_server to specify the collation for the character set.

• character_set_system

System Variable

Scope

Dynamic

Type

Default Value

character_set_system

Global

No

String

utf8

The character set used by the server for storing identifiers. The value is always utf8.

• character_sets_dir

Command-Line Format

System Variable

Scope

Dynamic

Type

--character-sets-dir=dir_name

character_sets_dir

Global

No

Directory name

The directory where character sets are installed. See Section 10.15, “Character Set Configuration”.

• check_proxy_users

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--check-proxy-users[={OFF|ON}]

check_proxy_users

Global

Yes

Boolean

OFF

Some authentication plugins implement proxy user mapping for themselves (for example, the PAM and
Windows authentication plugins). Other authentication plugins do not support proxy users by default.
Of these, some can request that the MySQL server itself map proxy users according to granted proxy
privileges: mysql_native_password, sha256_password.

If the check_proxy_users system variable is enabled, the server performs proxy user mapping for any
authentication plugins that make such a request. However, it may also be necessary to enable plugin-
specific system variables to take advantage of server proxy user mapping support:

• For the mysql_native_password plugin, enable mysql_native_password_proxy_users.

• For the sha256_password plugin, enable sha256_password_proxy_users.

776

For information about user proxying, see Section 6.2.14, “Proxy Users”.

Server System Variables

• collation_connection

System Variable

Scope

Dynamic

Type

collation_connection

Global, Session

Yes

String

The collation of the connection character set. collation_connection is important for comparisons
of literal strings. For comparisons of strings with column values, collation_connection does
not matter because columns have their own collation, which has a higher collation precedence (see
Section 10.8.4, “Collation Coercibility in Expressions”).

• collation_database

System Variable

Scope

Dynamic

Type

Default Value

Footnote

collation_database

Global, Session

Yes

String

latin1_swedish_ci

This option is dynamic, but should be set only by
server. You should not set this variable manually.

The collation used by the default database. The server sets this variable whenever the default database
changes. If there is no default database, the variable has the same value as collation_server.

The global character_set_database and collation_database system variables are deprecated
in MySQL 5.7; expect them to be removed in a future version of MySQL.

Assigning a value to the session character_set_database and collation_database system
variables is deprecated in MySQL 5.7 and assignments produce a warning. Expect the session variables
to become read only in a future version of MySQL and assignments to produce an error, while remaining
possible to access the session variables to determine the database character set and collation for the
default database.

• collation_server

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--collation-server=name

collation_server

Global, Session

Yes

String

latin1_swedish_ci

The server's default collation. See Section 10.15, “Character Set Configuration”.

• completion_type

Command-Line Format

System Variable

--completion-type=#

completion_type

777

Scope

Dynamic

Type

Default Value

Valid Values

Server System Variables

Global, Session

Yes

Enumeration

NO_CHAIN

NO_CHAIN

CHAIN

RELEASE

0

1

2

The transaction completion type. This variable can take the values shown in the following table. The
variable can be assigned using either the name values or corresponding integer values.

Value

NO_CHAIN (or 0)

CHAIN (or 1)

RELEASE (or 2)

Description

COMMIT and ROLLBACK are unaffected. This is the
default value.

COMMIT and ROLLBACK are equivalent to COMMIT
AND CHAIN and ROLLBACK AND CHAIN,
respectively. (A new transaction starts immediately
with the same isolation level as the just-terminated
transaction.)

COMMIT and ROLLBACK are equivalent to COMMIT
RELEASE and ROLLBACK RELEASE, respectively.
(The server disconnects after terminating the
transaction.)

completion_type affects transactions that begin with START TRANSACTION or BEGIN and end with
COMMIT or ROLLBACK. It does not apply to implicit commits resulting from execution of the statements
listed in Section 13.3.3, “Statements That Cause an Implicit Commit”. It also does not apply for XA
COMMIT, XA ROLLBACK, or when autocommit=1.

• concurrent_insert

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

778

--concurrent-insert[=value]

concurrent_insert

Global

Yes

Enumeration

AUTO

NEVER

AUTO

ALWAYS

Server System Variables

0

1

2

If AUTO (the default), MySQL permits INSERT and SELECT statements to run concurrently for MyISAM
tables that have no free blocks in the middle of the data file.

This variable can take the values shown in the following table. The variable can be assigned using either
the name values or corresponding integer values.

Value

NEVER (or 0)

AUTO (or 1)

ALWAYS (or 2)

Description

Disables concurrent inserts

(Default) Enables concurrent insert for MyISAM
tables that do not have holes

Enables concurrent inserts for all MyISAM tables,
even those that have holes. For a table with a hole,
new rows are inserted at the end of the table if it
is in use by another thread. Otherwise, MySQL
acquires a normal write lock and inserts the row
into the hole.

If you start mysqld with --skip-new, concurrent_insert is set to NEVER.

See also Section 8.11.3, “Concurrent Inserts”.

• connect_timeout

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--connect-timeout=#

connect_timeout

Global

Yes

Integer

10

2

31536000

seconds

The number of seconds that the mysqld server waits for a connect packet before responding with Bad
handshake. The default value is 10 seconds.

Increasing the connect_timeout value might help if clients frequently encounter errors of the form
Lost connection to MySQL server at 'XXX', system error: errno.

• core_file

System Variable

Scope

core_file

Global

779

Dynamic

Type

Default Value

Server System Variables

No

Boolean

OFF

Whether to write a core file if the server unexpectedly exits. This variable is set by the --core-file
option.

• datadir

Command-Line Format

System Variable

Scope

Dynamic

Type

--datadir=dir_name

datadir

Global

No

Directory name

The path to the MySQL server data directory. Relative paths are resolved with respect to the current
directory. If you expect the server to be started automatically (that is, in contexts for which you cannot
assume what the current directory is), it is best to specify the datadir value as an absolute path.

• date_format

This variable is unused. It is deprecated and is removed in MySQL 8.0.

• datetime_format

This variable is unused. It is deprecated and is removed in MySQL 8.0.

• debug

Command-Line Format

System Variable

Scope

Dynamic

Type

--debug[=debug_options]

debug

Global, Session

Yes

String

Default Value (Unix)

Default Value (Windows)

d:t:i:o,/tmp/mysqld.trace

d:t:i:O,\mysqld.trace

This variable indicates the current debugging settings. It is available only for servers built with debugging
support. The initial value comes from the value of instances of the --debug option given at server
startup. The global and session values may be set at runtime.

Setting the session value of this system variable is a restricted operation. The session user must have
privileges sufficient to set restricted session variables. See Section 5.1.8.1, “System Variable Privileges”.

Assigning a value that begins with + or - cause the value to added to or subtracted from the current
value:

mysql> SET debug = 'T';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+

780

Server System Variables

| T       |
+---------+

mysql> SET debug = '+P';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| P:T     |
+---------+

mysql> SET debug = '-P';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| T       |
+---------+

For more information, see Section 5.8.3, “The DBUG Package”.

• debug_sync

System Variable

Scope

Dynamic

Type

debug_sync

Session

Yes

String

This variable is the user interface to the Debug Sync facility. Use of Debug Sync requires that MySQL be
configured with the -DWITH_DEBUG=ON CMake option (see Section 2.8.7, “MySQL Source-Configuration
Options”); otherwise, this system variable is not available.

The global variable value is read only and indicates whether the facility is enabled. By default, Debug
Sync is disabled and the value of debug_sync is OFF. If the server is started with --debug-sync-
timeout=N, where N is a timeout value greater than 0, Debug Sync is enabled and the value of
debug_sync is ON - current signal followed by the signal name. Also, N becomes the default
timeout for individual synchronization points.

The session value can be read by any user and has the same value as the global variable. The session
value can be set to control synchronization points.

Setting the session value of this system variable is a restricted operation. The session user must have
privileges sufficient to set restricted session variables. See Section 5.1.8.1, “System Variable Privileges”.

For a description of the Debug Sync facility and how to use synchronization points, see MySQL Server
Doxygen Documentation.

• default_authentication_plugin

Command-Line Format

--default-authentication-
plugin=plugin_name

System Variable

default_authentication_plugin

Scope

Dynamic

Type

Global

No

Enumeration

781

Server System Variables

Default Value

Valid Values

mysql_native_password

mysql_native_password

sha256_password

The default authentication plugin. These values are permitted:

• mysql_native_password: Use MySQL native passwords; see Section 6.4.1.1, “Native Pluggable

Authentication”.

• sha256_password: Use SHA-256 passwords; see Section 6.4.1.5, “SHA-256 Pluggable

Authentication”.

Note

If this variable has a value other than mysql_native_password, clients
older than MySQL 5.5.7 cannot connect because, of the permitted default
authentication plugins, they understand only the mysql_native_password
authentication protocol.

The default_authentication_plugin value affects these aspects of server operation:

• It determines which authentication plugin the server assigns to new accounts created by CREATE

USER and GRANT statements that do not explicitly specify an authentication plugin.

• The old_passwords system variable affects password hashing for accounts that use the

mysql_native_password or sha256_password authentication plugin. If the default authentication
plugin is one of those plugins, the server sets old_passwords at startup to the value required by the
plugin password hashing method.

• For an account created with either of the following statements, the server associates the account with
the default authentication plugin and assigns the account the given password, hashed as required by
that plugin:

CREATE USER ... IDENTIFIED BY 'cleartext password';
GRANT ...  IDENTIFIED BY 'cleartext password';

• For an account created with either of the following statements, the server associates the account with
the default authentication plugin and assigns the account the given password hash, if the password
hash has the format required by the plugin:

CREATE USER ... IDENTIFIED BY PASSWORD 'encrypted password';
GRANT ...  IDENTIFIED BY PASSWORD 'encrypted password';

If the password hash is not in the format required by the default authentication plugin, the statement
fails.

• default_password_lifetime

Command-Line Format

System Variable

Scope

Dynamic

Type

782

--default-password-lifetime=#

default_password_lifetime

Global

Yes

Integer

Server System Variables

Default Value (≥ 5.7.11)
Default Value (≤ 5.7.10)
Minimum Value

Maximum Value

Unit

0

360

0

65535

days

This variable defines the global automatic password expiration policy. The default
default_password_lifetime value is 0, which disables automatic password expiration. If the value
of default_password_lifetime is a positive integer N, it indicates the permitted password lifetime;
passwords must be changed every N days.

The global password expiration policy can be overridden as desired for individual accounts using
the password expiration options of the ALTER USER statement. See Section 6.2.11, “Password
Management”.

Note

Prior to MySQL 5.7.11, the default default_password_lifetime value is 360
(passwords must be changed approximately once per year). For those versions,
be aware that, if you make no changes to the default_password_lifetime
variable or to individual user accounts, all user passwords expire after 360
days, and all user accounts start running in restricted mode when this happens.
Clients (which are effectively users) connecting to the server then get an error
indicating that the password must be changed: ERROR 1820 (HY000): You
must reset your password using ALTER USER statement before
executing this statement.

However, this is easy to miss for clients that automatically connect to the server,
such as connections made from scripts. To avoid having such clients suddenly
stop working due to a password expiring, make sure to change the password
expiration settings for those clients, like this:

ALTER USER 'script'@'localhost' PASSWORD EXPIRE NEVER;

Alternatively, set the default_password_lifetime variable to 0, thus
disabling automatic password expiration for all users.

• default_storage_engine

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--default-storage-engine=name

default_storage_engine

Global, Session

Yes

Enumeration

InnoDB

The default storage engine for tables. See Chapter 15, Alternative Storage Engines. This variable sets
the storage engine for permanent tables only. To set the storage engine for TEMPORARY tables, set the
default_tmp_storage_engine system variable.

To see which storage engines are available and enabled, use the SHOW ENGINES statement or query
the INFORMATION_SCHEMA ENGINES table.

783

Server System Variables

If you disable the default storage engine at server startup, you must set the default engine for both
permanent and TEMPORARY tables to a different engine or the server cannot start.

• default_tmp_storage_engine

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--default-tmp-storage-engine=name

default_tmp_storage_engine

Global, Session

Yes

Enumeration

InnoDB

The default storage engine for TEMPORARY tables (created with CREATE TEMPORARY TABLE). To set
the storage engine for permanent tables, set the default_storage_engine system variable. Also see
the discussion of that variable regarding possible values.

If you disable the default storage engine at server startup, you must set the default engine for both
permanent and TEMPORARY tables to a different engine or the server cannot start.

• default_week_format

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--default-week-format=#

default_week_format

Global, Session

Yes

Integer

0

0

7

The default mode value to use for the WEEK() function. See Section 12.7, “Date and Time Functions”.

• delay_key_write

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

784

--delay-key-write[={OFF|ON|ALL}]

delay_key_write

Global

Yes

Enumeration

ON

OFF

ON

Server System Variables

ALL

This variable specifies how to use delayed key writes. It applies only to MyISAM tables. Delayed key
writing causes key buffers not to be flushed between writes. See also Section 15.2.1, “MyISAM Startup
Options”.

This variable can have one of the following values to affect handling of the DELAY_KEY_WRITE table
option that can be used in CREATE TABLE statements.

Option

OFF

ON

ALL

Description

DELAY_KEY_WRITE is ignored.

MySQL honors any DELAY_KEY_WRITE option
specified in CREATE TABLE statements. This is
the default value.

All new opened tables are treated as if they were
created with the DELAY_KEY_WRITE option
enabled.

Note

If you set this variable to ALL, you should not use MyISAM tables from within
another program (such as another MySQL server or myisamchk) when the
tables are in use. Doing so leads to index corruption.

If DELAY_KEY_WRITE is enabled for a table, the key buffer is not flushed for the table on
every index update, but only when the table is closed. This speeds up writes on keys a
lot, but if you use this feature, you should add automatic checking of all MyISAM tables by
starting the server with the myisam_recover_options system variable set (for example,
myisam_recover_options='BACKUP,FORCE'). See Section 5.1.7, “Server System Variables”, and
Section 15.2.1, “MyISAM Startup Options”.

If you start mysqld with --skip-new, delay_key_write is set to OFF.

Warning

If you enable external locking with --external-locking, there is no protection
against index corruption for tables that use delayed key writes.

• delayed_insert_limit

Command-Line Format

--delayed-insert-limit=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Yes

delayed_insert_limit

Global

Yes

Integer

100

1

Maximum Value (64-bit platforms)

18446744073709551615

785

Server System Variables

Maximum Value (32-bit platforms)

4294967295

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be
removed in a future release.

• delayed_insert_timeout

Command-Line Format

--delayed-insert-timeout=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Yes

delayed_insert_timeout

Global

Yes

Integer

300

1

31536000

seconds

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be
removed in a future release.

• delayed_queue_size

Command-Line Format

--delayed-queue-size=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Yes

delayed_queue_size

Global

Yes

Integer

1000

1

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be
removed in a future release.

• disabled_storage_engines

Command-Line Format

System Variable

Scope

Dynamic

Type

786

--disabled-storage-
engines=engine[,engine]...

disabled_storage_engines

Global

No

String

Server System Variables

Default Value

empty string

This variable indicates which storage engines cannot be used to create tables or tablespaces. For
example, to prevent new MyISAM or FEDERATED tables from being created, start the server with these
lines in the server option file:

[mysqld]
disabled_storage_engines="MyISAM,FEDERATED"

By default, disabled_storage_engines is empty (no engines disabled), but it can be set to a
comma-separated list of one or more engines (not case-sensitive). Any engine named in the value
cannot be used to create tables or tablespaces with CREATE TABLE or CREATE TABLESPACE,
and cannot be used with ALTER TABLE ... ENGINE or ALTER TABLESPACE ... ENGINE
to change the storage engine of existing tables or tablespaces. Attempts to do so result in an
ER_DISABLED_STORAGE_ENGINE error.

disabled_storage_engines does not restrict other DDL statements for existing tables, such as
CREATE INDEX, TRUNCATE TABLE, ANALYZE TABLE, DROP TABLE, or DROP TABLESPACE. This
permits a smooth transition so that existing tables or tablespaces that use a disabled engine can be
migrated to a permitted engine by means such as ALTER TABLE ... ENGINE permitted_engine.

It is permitted to set the default_storage_engine or default_tmp_storage_engine system
variable to a storage engine that is disabled. This could cause applications to behave erratically or fail,
although that might be a useful technique in a development environment for identifying applications that
use disabled engines, so that they can be modified.

disabled_storage_engines is disabled and has no effect if the server is started with any of these
options: --bootstrap, --initialize, --initialize-insecure, --skip-grant-tables.

Note

Setting disabled_storage_engines might cause an issue with
mysql_upgrade. For details, see Section 4.4.7, “mysql_upgrade — Check and
Upgrade MySQL Tables”.

• disconnect_on_expired_password

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--disconnect-on-expired-
password[={OFF|ON}]

disconnect_on_expired_password

Global

No

Boolean

ON

This variable controls how the server handles clients with expired passwords:

• If the client indicates that it can handle expired passwords, the value of

disconnect_on_expired_password is irrelevant. The server permits the client to connect but puts
it in sandbox mode.

787

Server System Variables

• If the client does not indicate that it can handle expired passwords, the server handles the client

according to the value of disconnect_on_expired_password:

• If disconnect_on_expired_password: is enabled, the server disconnects the client.

• If disconnect_on_expired_password: is disabled, the server permits the client to connect but

puts it in sandbox mode.

For more information about the interaction of client and server settings relating to expired-password
handling, see Section 6.2.12, “Server Handling of Expired Passwords”.

• div_precision_increment

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--div-precision-increment=#

div_precision_increment

Global, Session

Yes

Integer

4

0

30

This variable indicates the number of digits by which to increase the scale of the result of division
operations performed with the / operator. The default value is 4. The minimum and maximum values are
0 and 30, respectively. The following example illustrates the effect of increasing the default value.

mysql> SELECT 1/7;
+--------+
| 1/7    |
+--------+
| 0.1429 |
+--------+
mysql> SET div_precision_increment = 12;
mysql> SELECT 1/7;
+----------------+
| 1/7            |
+----------------+
| 0.142857142857 |
+----------------+

• end_markers_in_json

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--end-markers-in-json[={OFF|ON}]

end_markers_in_json

Global, Session

Yes

Boolean

OFF

Whether optimizer JSON output should add end markers. See Section 8.15.9, “The
end_markers_in_json System Variable”.

788

Server System Variables

• eq_range_index_dive_limit

Command-Line Format

System Variable

--eq-range-index-dive-limit=#

eq_range_index_dive_limit

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global, Session

Yes

Integer

200

0

4294967295

This variable indicates the number of equality ranges in an equality comparison condition when the
optimizer should switch from using index dives to index statistics in estimating the number of qualifying
rows. It applies to evaluation of expressions that have either of these equivalent forms, where the
optimizer uses a nonunique index to look up col_name values:

col_name IN(val1, ..., valN)
col_name = val1 OR ... OR col_name = valN

In both cases, the expression contains N equality ranges. The optimizer can make row estimates using
index dives or index statistics. If eq_range_index_dive_limit is greater than 0, the optimizer
uses existing index statistics instead of index dives if there are eq_range_index_dive_limit
or more equality ranges. Thus, to permit use of index dives for up to N equality ranges, set
eq_range_index_dive_limit to N + 1. To disable use of index statistics and always use index dives
regardless of N, set eq_range_index_dive_limit to 0.

For more information, see Equality Range Optimization of Many-Valued Comparisons.

To update table index statistics for best estimates, use ANALYZE TABLE.

• error_count

The number of errors that resulted from the last statement that generated messages. This variable is
read only. See Section 13.7.5.17, “SHOW ERRORS Statement”.

• event_scheduler

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

--event-scheduler[=value]

event_scheduler

Global

Yes

Enumeration

OFF

OFF

ON

DISABLED

This variable enables or disables, and starts or stops, the Event Scheduler. The possible status values
are ON, OFF, and DISABLED. Turning the Event Scheduler OFF is not the same as disabling the Event

789

Server System Variables

Scheduler, which requires setting the status to DISABLED. This variable and its effects on the Event
Scheduler's operation are discussed in greater detail in Section 23.4.2, “Event Scheduler Configuration”

• explicit_defaults_for_timestamp

Command-Line Format

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

--explicit-defaults-for-
timestamp[={OFF|ON}]

Yes

explicit_defaults_for_timestamp

Global, Session

Yes

Boolean

OFF

This system variable determines whether the server enables certain nonstandard
behaviors for default values and NULL-value handling in TIMESTAMP columns. By default,
explicit_defaults_for_timestamp is disabled, which enables the nonstandard behaviors.

If explicit_defaults_for_timestamp is disabled, the server enables the nonstandard behaviors
and handles TIMESTAMP columns as follows:

• TIMESTAMP columns not explicitly declared with the NULL attribute are automatically declared with the
NOT NULL attribute. Assigning such a column a value of NULL is permitted and sets the column to the
current timestamp.

• The first TIMESTAMP column in a table, if not explicitly declared with the NULL attribute or
an explicit DEFAULT or ON UPDATE attribute, is automatically declared with the DEFAULT
CURRENT_TIMESTAMP and ON UPDATE CURRENT_TIMESTAMP attributes.

• TIMESTAMP columns following the first one, if not explicitly declared with the NULL attribute or an

explicit DEFAULT attribute, are automatically declared as DEFAULT '0000-00-00 00:00:00' (the
“zero” timestamp). For inserted rows that specify no explicit value for such a column, the column is
assigned '0000-00-00 00:00:00' and no warning occurs.

Depending on whether strict SQL mode or the NO_ZERO_DATE SQL mode is enabled, a default value
of '0000-00-00 00:00:00' may be invalid. Be aware that the TRADITIONAL SQL mode includes
strict mode and NO_ZERO_DATE. See Section 5.1.10, “Server SQL Modes”.

The nonstandard behaviors just described are deprecated; expect them to be removed in a future
release of MySQL.

If explicit_defaults_for_timestamp is enabled, the server disables the nonstandard behaviors
and handles TIMESTAMP columns as follows:

• It is not possible to assign a TIMESTAMP column a value of NULL to set it to the current timestamp. To
assign the current timestamp, set the column to CURRENT_TIMESTAMP or a synonym such as NOW().

• TIMESTAMP columns not explicitly declared with the NOT NULL attribute are automatically declared
with the NULL attribute and permit NULL values. Assigning such a column a value of NULL sets it to
NULL, not the current timestamp.

• TIMESTAMP columns declared with the NOT NULL attribute do not permit NULL values. For inserts that
specify NULL for such a column, the result is either an error for a single-row insert if strict SQL mode

790

Server System Variables

is enabled, or '0000-00-00 00:00:00' is inserted for multiple-row inserts with strict SQL mode
disabled. In no case does assigning the column a value of NULL set it to the current timestamp.

• TIMESTAMP columns explicitly declared with the NOT NULL attribute and without an explicit DEFAULT
attribute are treated as having no default value. For inserted rows that specify no explicit value for
such a column, the result depends on the SQL mode. If strict SQL mode is enabled, an error occurs.
If strict SQL mode is not enabled, the column is declared with the implicit default of '0000-00-00
00:00:00' and a warning occurs. This is similar to how MySQL treats other temporal types such as
DATETIME.

• No TIMESTAMP column is automatically declared with the DEFAULT CURRENT_TIMESTAMP or ON

UPDATE CURRENT_TIMESTAMP attributes. Those attributes must be explicitly specified.

• The first TIMESTAMP column in a table is not handled differently from TIMESTAMP columns following

the first one.

If explicit_defaults_for_timestamp is disabled at server startup, this warning appears in the
error log:

[Warning] TIMESTAMP with implicit DEFAULT value is deprecated.
Please use --explicit_defaults_for_timestamp server option (see
documentation for more details).

As indicated by the warning, to disable the deprecated nonstandard behaviors, enable the
explicit_defaults_for_timestamp system variable at server startup.

Note

explicit_defaults_for_timestamp is itself deprecated because its only
purpose is to permit control over deprecated TIMESTAMP behaviors that are to be
removed in a future release of MySQL. When removal of those behaviors occurs,
explicit_defaults_for_timestamp no longer has any purpose, and you
can expect it to be removed as well.

For additional information, see Section 11.2.6, “Automatic Initialization and Updating for TIMESTAMP
and DATETIME”.

• external_user

System Variable

Scope

Dynamic

Type

external_user

Session

No

String

The external user name used during the authentication process, as set by the plugin used to
authenticate the client. With native (built-in) MySQL authentication, or if the plugin does not set the
value, this variable is NULL. See Section 6.2.14, “Proxy Users”.

• flush

Command-Line Format

System Variable

Scope

Dynamic

--flush[={OFF|ON}]

flush

Global

Yes

791

Server System Variables

Type

Default Value

Boolean

OFF

If ON, the server flushes (synchronizes) all changes to disk after each SQL statement. Normally, MySQL
does a write of all changes to disk only after each SQL statement and lets the operating system handle
the synchronizing to disk. See Section B.3.3.3, “What to Do If MySQL Keeps Crashing”. This variable is
set to ON if you start mysqld with the --flush option.

Note

If flush is enabled, the value of flush_time does not matter and changes to
flush_time have no effect on flush behavior.

• flush_time

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--flush-time=#

flush_time

Global

Yes

Integer

0

0

31536000

seconds

If this is set to a nonzero value, all tables are closed every flush_time seconds to free up resources
and synchronize unflushed data to disk. This option is best used only on systems with minimal
resources.

Note

If flush is enabled, the value of flush_time does not matter and changes to
flush_time have no effect on flush behavior.

• foreign_key_checks

System Variable

Scope

Dynamic

Type

Default Value

foreign_key_checks

Global, Session

Yes

Boolean

ON

If set to 1 (the default), foreign key constraints are checked. If set to 0, foreign key constraints are
ignored, with a couple of exceptions. When re-creating a table that was dropped, an error is returned
if the table definition does not conform to the foreign key constraints referencing the table. Likewise,
an ALTER TABLE operation returns an error if a foreign key definition is incorrectly formed. For more
information, see Section 13.1.18.5, “FOREIGN KEY Constraints”.

Setting this variable has the same effect on NDB tables as it does for InnoDB tables. Typically you
leave this setting enabled during normal operation, to enforce referential integrity. Disabling foreign

792

Server System Variables

key checking can be useful for reloading InnoDB tables in an order different from that required by their
parent/child relationships. See Section 13.1.18.5, “FOREIGN KEY Constraints”.

Setting foreign_key_checks to 0 also affects data definition statements: DROP SCHEMA drops
a schema even if it contains tables that have foreign keys that are referred to by tables outside the
schema, and DROP TABLE drops tables that have foreign keys that are referred to by other tables.

Note

Setting foreign_key_checks to 1 does not trigger a scan of the existing table
data. Therefore, rows added to the table while foreign_key_checks=0 are not
verified for consistency.

Dropping an index required by a foreign key constraint is not permitted, even with
foreign_key_checks=0. The foreign key constraint must be removed before
dropping the index (Bug #70260).

• ft_boolean_syntax

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--ft-boolean-syntax=name

ft_boolean_syntax

Global

Yes

String

+ -><()~*:""&|

The list of operators supported by boolean full-text searches performed using IN BOOLEAN MODE. See
Section 12.9.2, “Boolean Full-Text Searches”.

The default variable value is '+ -><()~*:""&|'. The rules for changing the value are as follows:

• Operator function is determined by position within the string.

• The replacement value must be 14 characters.

• Each character must be an ASCII nonalphanumeric character.

• Either the first or second character must be a space.

• No duplicates are permitted except the phrase quoting operators in positions 11 and 12. These two

characters are not required to be the same, but they are the only two that may be.

• Positions 10, 13, and 14 (which by default are set to :, &, and |) are reserved for future extensions.

• ft_max_word_len

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--ft-max-word-len=#

ft_max_word_len

Global

No

Integer

84

793

Server System Variables

Minimum Value

Maximum Value

10

84

The maximum length of the word to be included in a MyISAM FULLTEXT index.

Note

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable.
Use REPAIR TABLE tbl_name QUICK.

• ft_min_word_len

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--ft-min-word-len=#

ft_min_word_len

Global

No

Integer

4

1

82

The minimum length of the word to be included in a MyISAM FULLTEXT index.

Note

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable.
Use REPAIR TABLE tbl_name QUICK.

• ft_query_expansion_limit

Command-Line Format

System Variable

--ft-query-expansion-limit=#

ft_query_expansion_limit

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

No

Integer

20

0

1000

The number of top matches to use for full-text searches performed using WITH QUERY EXPANSION.

• ft_stopword_file

Command-Line Format

System Variable

Scope

Dynamic

Type

794

--ft-stopword-file=file_name

ft_stopword_file

Global

No

File name

Server System Variables

The file from which to read the list of stopwords for full-text searches on MyISAM tables. The server looks
for the file in the data directory unless an absolute path name is given to specify a different directory.
All the words from the file are used; comments are not honored. By default, a built-in list of stopwords is
used (as defined in the storage/myisam/ft_static.c file). Setting this variable to the empty string
('') disables stopword filtering. See also Section 12.9.4, “Full-Text Stopwords”.

Note

FULLTEXT indexes on MyISAM tables must be rebuilt after changing this variable
or the contents of the stopword file. Use REPAIR TABLE tbl_name QUICK.

• general_log

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--general-log[={OFF|ON}]

general_log

Global

Yes

Boolean

OFF

Whether the general query log is enabled. The value can be 0 (or OFF) to disable the log or 1 (or ON) to
enable the log. The destination for log output is controlled by the log_output system variable; if that
value is NONE, no log entries are written even if the log is enabled.

• general_log_file

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--general-log-file=file_name

general_log_file

Global

Yes

File name

host_name.log

The name of the general query log file. The default value is host_name.log, but the initial value can be
changed with the --general_log_file option.

• group_concat_max_len

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--group-concat-max-len=#

group_concat_max_len

Global, Session

Yes

Integer

1024

4

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

795

Server System Variables

The maximum permitted result length in bytes for the GROUP_CONCAT() function. The default is 1024.

• have_compress

YES if the zlib compression library is available to the server, NO if not. If not, the COMPRESS() and
UNCOMPRESS() functions cannot be used.

• have_crypt

YES if the crypt() system call is available to the server, NO if not. If not, the ENCRYPT() function
cannot be used.

Note

The ENCRYPT() function is deprecated in MySQL 5.7, will be removed in a
future release of MySQL, and should no longer be used. (For one-way hashing,
consider using SHA2() instead.) Consequently, have_crypt also is deprecated;
expect it to be removed in a future release.

• have_dynamic_loading

YES if mysqld supports dynamic loading of plugins, NO if not. If the value is NO, you cannot use options
such as --plugin-load to load plugins at server startup, or the INSTALL PLUGIN statement to load
plugins at runtime.

• have_geometry

YES if the server supports spatial data types, NO if not.

• have_openssl

This variable is a synonym for have_ssl.

• have_profiling

YES if statement profiling capability is present, NO if not. If present, the profiling system variable
controls whether this capability is enabled or disabled. See Section 13.7.5.31, “SHOW PROFILES
Statement”.

This variable is deprecated; expect it to be removed in a future release of MySQL.

• have_query_cache

YES if mysqld supports the query cache, NO if not.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes have_query_cache.

• have_rtree_keys

YES if RTREE indexes are available, NO if not. (These are used for spatial indexes in MyISAM tables.)

• have_ssl

System Variable

have_ssl

796

Scope

Dynamic

Type

Valid Values

Server System Variables

Global

No

String

YES (SSL support available)

DISABLED (SSL support was compiled into server,
but server was not started with necessary options
to enable it)

YES if mysqld supports SSL connections, DISABLED if the server was compiled with SSL support,
but was not started with the appropriate connection-encryption options. For more information, see
Section 2.8.6, “Configuring SSL Library Support”.

• have_statement_timeout

System Variable

have_statement_timeout

Scope

Dynamic

Type

Global

No

Boolean

Whether the statement execution timeout feature is available (see Statement Execution Time Optimizer
Hints). The value can be NO if the background thread used by this feature could not be initialized.

• have_symlink

YES if symbolic link support is enabled, NO if not. This is required on Unix for support of the DATA
DIRECTORY and INDEX DIRECTORY table options. If the server is started with the --skip-symbolic-
links option, the value is DISABLED.

This variable has no meaning on Windows.

• host_cache_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--host-cache-size=#

host_cache_size

Global

Yes

Integer

-1 (signifies autosizing; do not assign this literal
value)

0

65536

The MySQL server maintains an in-memory host cache that contains client host name and IP address
information and is used to avoid Domain Name System (DNS) lookups; see Section 5.1.11.2, “DNS
Lookups and the Host Cache”.

The host_cache_size variable controls the size of the host cache, as well as the size of the
Performance Schema host_cache table that exposes the cache contents. Setting host_cache_size
has these effects:

797

Server System Variables

• Setting the size to 0 disables the host cache. With the cache disabled, the server performs a DNS

lookup every time a client connects.

• Changing the size at runtime causes an implicit host cache flushing operation that clears the host

cache, truncates the host_cache table, and unblocks any blocked hosts.

The default value is autosized to 128, plus 1 for a value of max_connections up to 500, plus 1 for
every increment of 20 over 500 in the max_connections value, capped to a limit of 2000.

Using the --skip-host-cache option is similar to setting the host_cache_size system variable to
0, but host_cache_size is more flexible because it can also be used to resize, enable, and disable the
host cache at runtime, not just at server startup.

Starting the server with --skip-host-cache does not prevent runtime changes to the value
of host_cache_size, but such changes have no effect and the cache is not re-enabled even if
host_cache_size is set larger than 0.

Setting the host_cache_size system variable rather than the --skip-host-cache option is
preferred for the reasons given in the previous paragraph. In addition, the --skip-host-cache option
is deprecated in MySQL 8.0, and its removal is expected in a future version of MySQL.

• hostname

System Variable

Scope

Dynamic

Type

hostname

Global

No

String

The server sets this variable to the server host name at startup.

• identity

This variable is a synonym for the last_insert_id variable. It exists for compatibility with other
database systems. You can read its value with SELECT @@identity, and set it using SET identity.

• ignore_db_dirs

Deprecated

System Variable

Scope

Dynamic

Type

5.7.16

ignore_db_dirs

Global

No

String

A comma-separated list of names that are not considered as database directories in the data directory.
The value is set from any instances of --ignore-db-dir given at server startup.

As of MySQL 5.7.11, --ignore-db-dir can be used at data directory initialization time with mysqld
--initialize to specify directories that the server should ignore for purposes of assessing whether
an existing data directory is considered empty. See Section 2.9.1, “Initializing the Data Directory”.

This system variable is deprecated in MySQL 5.7. With the introduction of the data dictionary in MySQL
8.0, it became superfluous and was removed in that version.

798

Server System Variables

• init_connect

Command-Line Format

System Variable

Scope

Dynamic

Type

--init-connect=name

init_connect

Global

Yes

String

A string to be executed by the server for each client that connects. The string consists of one or more
SQL statements, separated by semicolon characters.

For users that have the SUPER privilege, the content of init_connect is not executed. This is done so
that an erroneous value for init_connect does not prevent all clients from connecting. For example,
the value might contain a statement that has a syntax error, thus causing client connections to fail. Not
executing init_connect for users that have the SUPER privilege enables them to open a connection
and fix the init_connect value.

As of MySQL 5.7.22, init_connect execution is skipped for any client user with an expired password.
This is done because such a user cannot execute arbitrary statements, and thus init_connect
execution fails, leaving the client unable to connect. Skipping init_connect execution enables the
user to connect and change password.

The server discards any result sets produced by statements in the value of init_connect.

• init_file

Command-Line Format

System Variable

Scope

Dynamic

Type

--init-file=file_name

init_file

Global

No

File name

If specified, this variable names a file containing SQL statements to be read and executed during the
startup process. Each statement must be on a single line and should not include comments.

If the server is started with any of the --bootstrap, --initialize, or --initialize-insecure
options, it operates in bootstap mode and some functionality is unavailable that limits the statements
permitted in the file. These include statements that relate to account management (such as CREATE
USER or GRANT), replication, and global transaction identifiers. See Section 16.1.3, “Replication with
Global Transaction Identifiers”.

• innodb_xxx

InnoDB system variables are listed in Section 14.15, “InnoDB Startup Options and System Variables”.
These variables control many aspects of storage, memory use, and I/O patterns for InnoDB tables, and
are especially important now that InnoDB is the default storage engine.

• insert_id

The value to be used by the following INSERT or ALTER TABLE statement when inserting an
AUTO_INCREMENT value. This is mainly used with the binary log.

• interactive_timeout

799

Server System Variables

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--interactive-timeout=#

interactive_timeout

Global, Session

Yes

Integer

28800

1

31536000

seconds

The number of seconds the server waits for activity on an interactive connection before closing
it. An interactive client is defined as a client that uses the CLIENT_INTERACTIVE option to
mysql_real_connect(). See also wait_timeout.

• internal_tmp_disk_storage_engine

Command-Line Format

System Variable

--internal-tmp-disk-storage-engine=#

internal_tmp_disk_storage_engine

Scope

Dynamic

Type

Default Value

Valid Values

Global

Yes

Enumeration

INNODB

MYISAM

INNODB

The storage engine for on-disk internal temporary tables (see Section 8.4.4, “Internal Temporary Table
Use in MySQL”). Permitted values are MYISAM and INNODB (the default).

The optimizer uses the storage engine defined by internal_tmp_disk_storage_engine for on-disk
internal temporary tables.

When using internal_tmp_disk_storage_engine=INNODB (the default), queries that generate on-
disk internal temporary tables that exceed InnoDB row or column limits return Row size too large
or Too many columns errors. The workaround is to set internal_tmp_disk_storage_engine to
MYISAM.

• join_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

800

--join-buffer-size=#

join_buffer_size

Global, Session

Yes

Integer

262144

128

Server System Variables

Maximum Value (Windows)

4294967168

Maximum Value (Other, 64-bit platforms)

18446744073709551488

Maximum Value (Other, 32-bit platforms)

4294967168

Unit

Block Size

bytes

128

The minimum size of the buffer that is used for plain index scans, range index scans, and joins that
do not use indexes and thus perform full table scans. Normally, the best way to get fast joins is to add
indexes. Increase the value of join_buffer_size to get a faster full join when adding indexes is not
possible. One join buffer is allocated for each full join between two tables. For a complex join between
several tables for which indexes are not used, multiple join buffers might be necessary.

The default is 256KB. The maximum permissible setting for join_buffer_size is 4GB−1. Larger
values are permitted for 64-bit platforms (except 64-bit Windows, for which large values are truncated
to 4GB−1 with a warning). The block size is 128, and a value that is not an exact multiple of the block
size is rounded down to the next lower multiple of the block size by MySQL Server before storing the
value for the system variable. The parser allows values up to the maximum unsigned integer value for
the platform (4294967295 or 232
−1 for a 64-bit
system) but the actual maximum is a block size lower.

−1 for a 32-bit system, 18446744073709551615 or 264

Unless a Block Nested-Loop or Batched Key Access algorithm is used, there is no gain from setting the
buffer larger than required to hold each matching row, and all joins allocate at least the minimum size,
so use caution in setting this variable to a large value globally. It is better to keep the global setting small
and change the session setting to a larger value only in sessions that are doing large joins. Memory
allocation time can cause substantial performance drops if the global size is larger than needed by most
queries that use it.

When Block Nested-Loop is used, a larger join buffer can be beneficial up to the point where all required
columns from all rows in the first table are stored in the join buffer. This depends on the query; the
optimal size may be smaller than holding all rows from the first tables.

When Batched Key Access is used, the value of join_buffer_size defines how large the batch of
keys is in each request to the storage engine. The larger the buffer, the more sequential access is made
to the right hand table of a join operation, which can significantly improve performance.

For additional information about join buffering, see Section 8.2.1.6, “Nested-Loop Join Algorithms”. For
information about Batched Key Access, see Section 8.2.1.11, “Block Nested-Loop and Batched Key
Access Joins”.

• keep_files_on_create

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--keep-files-on-create[={OFF|ON}]

keep_files_on_create

Global, Session

Yes

Boolean

OFF

If a MyISAM table is created with no DATA DIRECTORY option, the .MYD file is created in the database
directory. By default, if MyISAM finds an existing .MYD file in this case, it overwrites it. The same applies
to .MYI files for tables created with no INDEX DIRECTORY option. To suppress this behavior, set the

801

Server System Variables

keep_files_on_create variable to ON (1), in which case MyISAM does not overwrite existing files
and returns an error instead. The default value is OFF (0).

If a MyISAM table is created with a DATA DIRECTORY or INDEX DIRECTORY option and an existing
.MYD or .MYI file is found, MyISAM always returns an error. It does not overwrite a file in the specified
directory.

• key_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--key-buffer-size=#

key_buffer_size

Global

Yes

Integer

8388608

0

Maximum Value (64-bit platforms)

OS_PER_PROCESS_LIMIT

Maximum Value (32-bit platforms)

Unit

4294967295

bytes

Index blocks for MyISAM tables are buffered and are shared by all threads. key_buffer_size is the
size of the buffer used for index blocks. The key buffer is also known as the key cache.

The minimum permissible setting is 0, but you cannot set key_buffer_size to 0 dynamically. A setting
of 0 drops the key cache, which is not permitted at runtime. Setting key_buffer_size to 0 is permitted
only at startup, in which case the key cache is not initialized. Changing the key_buffer_size setting
at runtime from a value of 0 to a permitted non-zero value initializes the key cache.

key_buffer_size can be increased or decreased only in increments or multiples of 4096 bytes.
Increasing or decreasing the setting by a nonconforming value produces a warning and truncates the
setting to a conforming value.

The maximum permissible setting for key_buffer_size is 4GB−1 on 32-bit platforms. Larger values
are permitted for 64-bit platforms. The effective maximum size might be less, depending on your
available physical RAM and per-process RAM limits imposed by your operating system or hardware
platform. The value of this variable indicates the amount of memory requested. Internally, the server
allocates as much memory as possible up to this amount, but the actual allocation might be less.

You can increase the value to get better index handling for all reads and multiple writes; on a system
whose primary function is to run MySQL using the MyISAM storage engine, 25% of the machine's total
memory is an acceptable value for this variable. However, you should be aware that, if you make the
value too large (for example, more than 50% of the machine's total memory), your system might start
to page and become extremely slow. This is because MySQL relies on the operating system to perform
file system caching for data reads, so you must leave some room for the file system cache. You should
also consider the memory requirements of any other storage engines that you may be using in addition
to MyISAM.

For even more speed when writing many rows at the same time, use LOCK TABLES. See
Section 8.2.4.1, “Optimizing INSERT Statements”.

You can check the performance of the key buffer by issuing a SHOW STATUS statement and examining
the Key_read_requests, Key_reads, Key_write_requests, and Key_writes status variables.

802

Server System Variables

(See Section 13.7.5, “SHOW Statements”.) The Key_reads/Key_read_requests ratio should
normally be less than 0.01. The Key_writes/Key_write_requests ratio is usually near 1 if you are
using mostly updates and deletes, but might be much smaller if you tend to do updates that affect many
rows at the same time or if you are using the DELAY_KEY_WRITE table option.

The fraction of the key buffer in use can be determined using key_buffer_size in conjunction
with the Key_blocks_unused status variable and the buffer block size, which is available from the
key_cache_block_size system variable:

1 - ((Key_blocks_unused * key_cache_block_size) / key_buffer_size)

This value is an approximation because some space in the key buffer is allocated internally for
administrative structures. Factors that influence the amount of overhead for these structures include
block size and pointer size. As block size increases, the percentage of the key buffer lost to overhead
tends to decrease. Larger blocks results in a smaller number of read operations (because more keys are
obtained per read), but conversely an increase in reads of keys that are not examined (if not all keys in a
block are relevant to a query).

It is possible to create multiple MyISAM key caches. The size limit of 4GB applies to each cache
individually, not as a group. See Section 8.10.2, “The MyISAM Key Cache”.

• key_cache_age_threshold

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--key-cache-age-threshold=#

key_cache_age_threshold

Global

Yes

Integer

300

100

Maximum Value (64-bit platforms)

18446744073709551516

Maximum Value (32-bit platforms)

Block Size

4294967196

100

This value controls the demotion of buffers from the hot sublist of a key cache to the warm sublist. Lower
values cause demotion to happen more quickly. The minimum value is 100. The default value is 300.
See Section 8.10.2, “The MyISAM Key Cache”.

• key_cache_block_size

Command-Line Format

System Variable

--key-cache-block-size=#

key_cache_block_size

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

1024

512

16384

803

Server System Variables

Unit

Block Size

bytes

512

The size in bytes of blocks in the key cache. The default value is 1024. See Section 8.10.2, “The
MyISAM Key Cache”.

• key_cache_division_limit

Command-Line Format

System Variable

--key-cache-division-limit=#

key_cache_division_limit

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

100

1

100

The division point between the hot and warm sublists of the key cache buffer list. The value is the
percentage of the buffer list to use for the warm sublist. Permissible values range from 1 to 100. The
default value is 100. See Section 8.10.2, “The MyISAM Key Cache”.

• large_files_support

System Variable

large_files_support

Scope

Dynamic

Type

Global

No

Boolean

Whether mysqld was compiled with options for large file support.

• large_pages

Command-Line Format

System Variable

Scope

Dynamic

Platform Specific

Type

Default Value

--large-pages[={OFF|ON}]

large_pages

Global

No

Linux

Boolean

OFF

Whether large page support is enabled (via the --large-pages option). See Section 8.12.4.3,
“Enabling Large Page Support”.

• large_page_size

System Variable

804

Scope

large_page_size

Global

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Server System Variables

No

Integer

0

0

65535

bytes

If large page support is enabled, this shows the size of memory pages. Large memory pages are
supported only on Linux; on other platforms, the value of this variable is always 0. See Section 8.12.4.3,
“Enabling Large Page Support”.

• last_insert_id

The value to be returned from LAST_INSERT_ID(). This is stored in the binary log when you use
LAST_INSERT_ID() in a statement that updates a table. Setting this variable does not update the value
returned by the mysql_insert_id() C API function.

• lc_messages

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--lc-messages=name

lc_messages

Global, Session

Yes

String

en_US

The locale to use for error messages. The default is en_US. The server converts the argument to a
language name and combines it with the value of lc_messages_dir to produce the location for the
error message file. See Section 10.12, “Setting the Error Message Language”.

• lc_messages_dir

Command-Line Format

System Variable

Scope

Dynamic

Type

--lc-messages-dir=dir_name

lc_messages_dir

Global

No

Directory name

The directory where error messages are located. The server uses the value together with the value of
lc_messages to produce the location for the error message file. See Section 10.12, “Setting the Error
Message Language”.

• lc_time_names

Command-Line Format

System Variable

Scope

Dynamic

--lc-time-names=value

lc_time_names

Global, Session

Yes

805

Server System Variables

Type

String

This variable specifies the locale that controls the language used to display day and month names
and abbreviations. This variable affects the output from the DATE_FORMAT(), DAYNAME() and
MONTHNAME() functions. Locale names are POSIX-style values such as 'ja_JP' or 'pt_BR'.
The default value is 'en_US' regardless of your system's locale setting. For further information, see
Section 10.16, “MySQL Server Locale Support”.

• license

System Variable

Scope

Dynamic

Type

Default Value

The type of license the server has.

• local_infile

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

license

Global

No

String

GPL

--local-infile[={OFF|ON}]

local_infile

Global

Yes

Boolean

ON

This variable controls server-side LOCAL capability for LOAD DATA statements. Depending on the
local_infile setting, the server refuses or permits local data loading by clients that have LOCAL
enabled on the client side.

To explicitly cause the server to refuse or permit LOAD DATA LOCAL statements (regardless of how
client programs and libraries are configured at build time or runtime), start mysqld with local_infile
disabled or enabled, respectively. local_infile can also be set at runtime. For more information, see
Section 6.1.6, “Security Considerations for LOAD DATA LOCAL”.

• lock_wait_timeout

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

806

--lock-wait-timeout=#

lock_wait_timeout

Global, Session

Yes

Integer

31536000

1

31536000

Server System Variables

Unit

seconds

This variable specifies the timeout in seconds for attempts to acquire metadata locks. The permissible
values range from 1 to 31536000 (1 year). The default is 31536000.

This timeout applies to all statements that use metadata locks. These include DML and DDL operations
on tables, views, stored procedures, and stored functions, as well as LOCK TABLES, FLUSH TABLES
WITH READ LOCK, and HANDLER statements.

This timeout does not apply to implicit accesses to system tables in the mysql database, such as grant
tables modified by GRANT or REVOKE statements or table logging statements. The timeout does apply to
system tables accessed directly, such as with SELECT or UPDATE.

The timeout value applies separately for each metadata lock attempt. A given statement can require
more than one lock, so it is possible for the statement to block for longer than the lock_wait_timeout
value before reporting a timeout error. When lock timeout occurs, ER_LOCK_WAIT_TIMEOUT is reported.

lock_wait_timeout does not apply to delayed inserts, which always execute with a timeout of 1 year.
This is done to avoid unnecessary timeouts because a session that issues a delayed insert receives no
notification of delayed insert timeouts.

• locked_in_memory

System Variable

Scope

Dynamic

Type

Default Value

locked_in_memory

Global

No

Boolean

OFF

Whether mysqld was locked in memory with --memlock.

• log_error

Command-Line Format

System Variable

Scope

Dynamic

Type

--log-error[=file_name]

log_error

Global

No

File name

The error log output destination. If the destination is the console, the value is stderr. Otherwise, the
destination is a file and the log_error value is the file name. See Section 5.4.2, “The Error Log”.

• log_error_verbosity

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--log-error-verbosity=#

log_error_verbosity

Global

Yes

Integer

3

807

Server System Variables

Minimum Value

Maximum Value

1

3

The verbosity of the server in writing error, warning, and note messages to the error log. The following
table shows the permitted values. The default is 3.

log_error_verbosity Value

1

2

3

Permitted Messages

Error messages

Error and warning messages

Error, warning, and information messages

log_error_verbosity was added in MySQL 5.7.2. It is preferred over, and should be used instead
of, the older log_warnings system variable. See the description of log_warnings for information
about how that variable relates to log_error_verbosity. In particular, assigning a value to
log_warnings assigns a value to log_error_verbosity and vice versa.

• log_output

Command-Line Format

System Variable

--log-output=name

log_output

Scope

Dynamic

Type

Default Value

Valid Values

Global

Yes

Set

FILE

TABLE

FILE

NONE

The destination or destinations for general query log and slow query log output. The value is a list one
or more comma-separated words chosen from TABLE, FILE, and NONE. TABLE selects logging to the
general_log and slow_log tables in the mysql system database. FILE selects logging to log files.
NONE disables logging. If NONE is present in the value, it takes precedence over any other words that are
present. TABLE and FILE can both be given to select both log output destinations.

This variable selects log output destinations, but does not enable log output. To do that, enable the
general_log and slow_query_log system variables. For FILE logging, the general_log_file
and slow_query_log_file system variables determine the log file locations. For more information,
see Section 5.4.1, “Selecting General Query Log and Slow Query Log Output Destinations”.

• log_queries_not_using_indexes

Command-Line Format

--log-queries-not-using-
indexes[={OFF|ON}]

System Variable

log_queries_not_using_indexes

Scope

Dynamic

Type

808

Global

Yes

Boolean

Server System Variables

Default Value

OFF

If you enable this variable with the slow query log enabled, queries that are expected to retrieve all
rows are logged. See Section 5.4.5, “The Slow Query Log”. This option does not necessarily mean that
no index is used. For example, a query that uses a full index scan uses an index but would be logged
because the index would not limit the number of rows.

• log_slow_admin_statements

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--log-slow-admin-statements[={OFF|
ON}]

log_slow_admin_statements

Global

Yes

Boolean

OFF

Include slow administrative statements in the statements written to the slow query log. Administrative
statements include ALTER TABLE, ANALYZE TABLE, CHECK TABLE, CREATE INDEX, DROP INDEX,
OPTIMIZE TABLE, and REPAIR TABLE.

• log_syslog

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (Unix)

Default Value (Windows)

--log-syslog[={OFF|ON}]

log_syslog

Global

Yes

Boolean

OFF

ON

Whether to write error log output to the system log. This is the Event Log on Windows, and syslog on
Unix and Unix-like systems. The default value is platform specific:

• On Windows, Event Log output is enabled by default.

• On Unix and Unix-like systems, syslog output is disabled by default.

Regardless of the default, log_syslog can be set explicitly to control output on any supported platform.

System log output control is distinct from sending error output to a file or the console. Error output can be
directed to a file or the console in addition to or instead of the system log as desired. See Section 5.4.2,
“The Error Log”.

• log_syslog_facility

Command-Line Format

--log-syslog-facility=value

System Variable

Scope

log_syslog_facility

Global

809

Dynamic

Type

Default Value

Server System Variables

Yes

String

daemon

The facility for error log output written to syslog (what type of program is sending the message). This
variable has no effect unless the log_syslog system variable is enabled. See Section 5.4.2.3, “Error
Logging to the System Log”.

The permitted values can vary per operating system; consult your system syslog documentation.

This variable does not exist on Windows.

• log_syslog_include_pid

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--log-syslog-include-pid[={OFF|ON}]

log_syslog_include_pid

Global

Yes

Boolean

ON

Whether to include the server process ID in each line of error log output written to syslog. This variable
has no effect unless the log_syslog system variable is enabled. See Section 5.4.2.3, “Error Logging to
the System Log”.

This variable does not exist on Windows.

• log_syslog_tag

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--log-syslog-tag=tag

log_syslog_tag

Global

Yes

String

empty string

The tag to be added to the server identifier in error log output written to syslog. This variable has no
effect unless the log_syslog system variable is enabled. See Section 5.4.2.3, “Error Logging to the
System Log”.

By default, the server identifier is mysqld with no tag. If a tag value of tag is specified, it is appended to
the server identifier with a leading hyphen, resulting in an identifier of mysqld-tag.

On Windows, to use a tag that does not already exist, the server must be run from an account with
Administrator privileges, to permit creation of a registry entry for the tag. Elevated privileges are not
required if the tag already exists.

• log_timestamps

810

Command-Line Format

--log-timestamps=#

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

Server System Variables

log_timestamps

Global

Yes

Enumeration

UTC

UTC

SYSTEM

This variable controls the time zone of timestamps in messages written to the error log, and in general
query log and slow query log messages written to files. It does not affect the time zone of general query
log and slow query log messages written to tables (mysql.general_log, mysql.slow_log). Rows
retrieved from those tables can be converted from the local system time zone to any desired time zone
with CONVERT_TZ() or by setting the session time_zone system variable.

Permitted log_timestamps values are UTC (the default) and SYSTEM (local system time zone).

Timestamps are written using ISO 8601 / RFC 3339 format: YYYY-MM-DDThh:mm:ss.uuuuuu plus a
tail value of Z signifying Zulu time (UTC) or ±hh:mm (an offset from UTC).

• log_throttle_queries_not_using_indexes

Command-Line Format

--log-throttle-queries-not-using-
indexes=#

System Variable

log_throttle_queries_not_using_indexes

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

0

0

4294967295

If log_queries_not_using_indexes is enabled, the
log_throttle_queries_not_using_indexes variable limits the number of such queries per
minute that can be written to the slow query log. A value of 0 (the default) means “no limit”. For more
information, see Section 5.4.5, “The Slow Query Log”.

• log_warnings

Command-Line Format

--log-warnings[=#]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Yes

log_warnings

Global

Yes

Integer

2

0

811

Server System Variables

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

Whether to produce additional warning messages to the error log. As of MySQL 5.7.2, information items
previously governed by log_warnings are governed by log_error_verbosity, which is preferred
over, and should be used instead of, the older log_warnings system variable. (The log_warnings
system variable and --log-warnings command-line option are deprecated; expect them to be
removed in a future release of MySQL.)

log_warnings is enabled by default (the default is 1 before MySQL 5.7.2, 2 as of 5.7.2). To disable it,
set it to 0. If the value is greater than 0, the server logs messages about statements that are unsafe for
statement-based logging. If the value is greater than 1, the server logs aborted connections and access-
denied errors for new connection attempts. See Section B.3.2.9, “Communication Errors and Aborted
Connections”.

If you use replication, enabling this variable by setting it greater than 0 is recommended, to get more
information about what is happening, such as messages about network failures and reconnections.

If a replica server is started with log_warnings enabled, the replica prints messages to the error log to
provide information about its status, such as the binary log and relay log coordinates where it starts its
job, when it is switching to another relay log, when it reconnects after a disconnect, and so forth.

Assigning a value to log_warnings assigns a value to log_error_verbosity and vice versa. The
variables are related as follows:

• Suppression of all log_warnings items, achieved with log_warnings=0, is achieved with

log_error_verbosity=1 (errors only).

• Items printed for log_warnings=1 or higher count as warnings and are printed for

log_error_verbosity=2 or higher.

• Items printed for log_warnings=2 count as notes and are printed for log_error_verbosity=3.

As of MySQL 5.7.2, the default log level is controlled by log_error_verbosity, which has a
default of 3. In addition, the default for log_warnings changes from 1 to 2, which corresponds
to log_error_verbosity=3. To achieve a logging level similar to the previous default, set
log_error_verbosity=2.

In MySQL 5.7.2 and higher, use of log_warnings is still permitted but maps onto use of
log_error_verbosity as follows:

• Setting log_warnings=0 is equivalent to log_error_verbosity=1 (errors only).

• Setting log_warnings=1 is equivalent to log_error_verbosity=2 (errors, warnings).

• Setting log_warnings=2 (or higher) is equivalent to log_error_verbosity=3 (errors, warnings,

notes), and the server sets log_warnings to 2 if a larger value is specified.

• long_query_time

Command-Line Format

System Variable

Scope

Dynamic

812

--long-query-time=#

long_query_time

Global, Session

Yes

Type

Default Value

Minimum Value

Maximum Value

Unit

Server System Variables

Numeric

10

0

31536000

seconds

If a query takes longer than this many seconds, the server increments the Slow_queries status
variable. If the slow query log is enabled, the query is logged to the slow query log file. This value
is measured in real time, not CPU time, so a query that is under the threshold on a lightly loaded
system might be above the threshold on a heavily loaded one. The minimum and default values of
long_query_time are 0 and 10, respectively. The maximum is 31536000, which is 365 days in
seconds. The value can be specified to a resolution of microseconds. See Section 5.4.5, “The Slow
Query Log”.

Smaller values of this variable result in more statements being considered long-running, with the result
that more space is required for the slow query log. For very small values (less than one second), the
log may grow quite large in a small time. Increasing the number of statements considered long-running
may also result in false positives for the “excessive Number of Long Running Processes” alert in MySQL
Enterprise Monitor, especially if Group Replication is enabled. For these reasons, very small values
should be used in test environments only, or, in production environments, only for a short period.

• low_priority_updates

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--low-priority-updates[={OFF|ON}]

low_priority_updates

Global, Session

Yes

Boolean

OFF

If set to 1, all INSERT, UPDATE, DELETE, and LOCK TABLE WRITE statements wait until there is no
pending SELECT or LOCK TABLE READ on the affected table. The same effect can be obtained using
{INSERT | REPLACE | DELETE | UPDATE} LOW_PRIORITY ... to lower the priority of only one
query. This variable affects only storage engines that use only table-level locking (such as MyISAM,
MEMORY, and MERGE). See Section 8.11.2, “Table Locking Issues”.

• lower_case_file_system

System Variable

lower_case_file_system

Scope

Dynamic

Type

Global

No

Boolean

This variable describes the case sensitivity of file names on the file system where the data directory is
located. OFF means file names are case-sensitive, ON means they are not case-sensitive. This variable
is read only because it reflects a file system attribute and setting it would have no effect on the file
system.

813

Server System Variables

• lower_case_table_names

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (macOS)

Default Value (Unix)

Default Value (Windows)

Minimum Value

Maximum Value

--lower-case-table-names[=#]

lower_case_table_names

Global

No

Integer

2

0

1

0

2

If set to 0, table names are stored as specified and comparisons are case-sensitive. If set to 1, table
names are stored in lowercase on disk and comparisons are not case-sensitive. If set to 2, table names
are stored as given but compared in lowercase. This option also applies to database names and table
aliases. For additional details, see Section 9.2.3, “Identifier Case Sensitivity”.

The default value of this variable is platform-dependent (see lower_case_file_system). On Linux
and other Unix-like systems, the default is 0. On Windows the default value is 1. On macOS, the default
value is 2. On Linux (and other Unix-like systems), setting the value to 2 is not supported; the server
forces the value to 0 instead.

You should not set lower_case_table_names to 0 if you are running MySQL on a system where
the data directory resides on a case-insensitive file system (such as on Windows or macOS). It is an
unsupported combination that could result in a hang condition when running an INSERT INTO ...
SELECT ... FROM tbl_name operation with the wrong tbl_name lettercase. With MyISAM,
accessing table names using different lettercases could cause index corruption.

An error message is printed and the server exits if you attempt to start the server with --
lower_case_table_names=0 on a case-insensitive file system.

The setting of this variable affects the behavior of replication filtering options with regard to case
sensitivity. For more information, see Section 16.2.5, “How Servers Evaluate Replication Filtering Rules”.

• max_allowed_packet

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

814

--max-allowed-packet=#

max_allowed_packet

Global, Session

Yes

Integer

4194304

1024

1073741824

bytes

Server System Variables

Block Size

1024

The maximum size of one packet or any generated/intermediate string, or any parameter sent by the
mysql_stmt_send_long_data() C API function. The default is 4MB.

The packet message buffer is initialized to net_buffer_length bytes, but can grow up to
max_allowed_packet bytes when needed. This value by default is small, to catch large (possibly
incorrect) packets.

You must increase this value if you are using large BLOB columns or long strings. It should be as big
as the largest BLOB you want to use. The protocol limit for max_allowed_packet is 1GB. The value
should be a multiple of 1024; nonmultiples are rounded down to the nearest multiple.

When you change the message buffer size by changing the value of the max_allowed_packet
variable, you should also change the buffer size on the client side if your client program permits it.
The default max_allowed_packet value built in to the client library is 1GB, but individual client
programs might override this. For example, mysql and mysqldump have defaults of 16MB and 24MB,
respectively. They also enable you to change the client-side value by setting max_allowed_packet on
the command line or in an option file.

The session value of this variable is read only. The client can receive up to as many bytes as the
session value. However, the server cannot send to the client more bytes than the current global
max_allowed_packet value. (The global value could be less than the session value if the global value
is changed after the client connects.)

• max_connect_errors

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--max-connect-errors=#

max_connect_errors

Global

Yes

Integer

100

1

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

After max_connect_errors successive connection requests from a host are interrupted without a
successful connection, the server blocks that host from further connections. If a connection from a
host is established successfully within fewer than max_connect_errors attempts after a previous
connection was interrupted, the error count for the host is cleared to zero. To unblock blocked hosts,
flush the host cache; see Flushing the Host Cache.

• max_connections

Command-Line Format

System Variable

Scope

Dynamic

Type

--max-connections=#

max_connections

Global

Yes

Integer

815

Server System Variables

Default Value

Minimum Value

Maximum Value

151

1

100000

The maximum permitted number of simultaneous client connections. The maximum effective value
is the lesser of the effective value of open_files_limit - 810, and the value actually set for
max_connections.

For more information, see Section 5.1.11.1, “Connection Interfaces”.

• max_delayed_threads

Command-Line Format

--max-delayed-threads=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Yes

max_delayed_threads

Global, Session

Yes

Integer

20

0

16384

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be
removed in a future release.

• max_digest_length

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--max-digest-length=#

max_digest_length

Global

No

Integer

1024

0

1048576

bytes

The maximum number of bytes of memory reserved per session for computation of normalized
statement digests. Once that amount of space is used during digest computation, truncation occurs:
no further tokens from a parsed statement are collected or figure into its digest value. Statements that
differ only after that many bytes of parsed tokens produce the same normalized statement digest and are
considered identical if compared or if aggregated for digest statistics.

The length used for calculating a normalized statement digest is the sum of the length of the normalized
statement digest and the length of the statement digest. Since the length of the statement digest is

816

Server System Variables

always 64, when the value of max_digest_length is 1024 (the default), the maximum length for a
normalized SQL statement before truncation occurs is 1024 - 64 = 960 bytes.

Warning

Setting max_digest_length to zero disables digest production, which also
disables server functionality that requires digests, such as MySQL Enterprise
Firewall.

Decreasing the max_digest_length value reduces memory use but causes the digest value of more
statements to become indistinguishable if they differ only at the end. Increasing the value permits longer
statements to be distinguished but increases memory use, particularly for workloads that involve large
numbers of simultaneous sessions (the server allocates max_digest_length bytes per session).

The parser uses this system variable as a limit on the maximum length of normalized statement
digests that it computes. The Performance Schema, if it tracks statement digests, makes
a copy of the digest value, using the performance_schema_max_digest_length.
system variable as a limit on the maximum length of digests that it stores. Consequently, if
performance_schema_max_digest_length is less than max_digest_length, digest values
stored in the Performance Schema are truncated relative to the original digest values.

For more information about statement digesting, see Section 25.10, “Performance Schema Statement
Digests”.

• max_error_count

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--max-error-count=#

max_error_count

Global, Session

Yes

Integer

64

0

65535

The maximum number of error, warning, and information messages to be stored for display by the SHOW
ERRORS and SHOW WARNINGS statements. This is the same as the number of condition areas in the
diagnostics area, and thus the number of conditions that can be inspected by GET DIAGNOSTICS.

• max_execution_time

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--max-execution-time=#

max_execution_time

Global, Session

Yes

Integer

0

0

4294967295

817

Server System Variables

Unit

milliseconds

The execution timeout for SELECT statements, in milliseconds. If the value is 0, timeouts are not
enabled.

max_execution_time applies as follows:

• The global max_execution_time value provides the default for the session value for new

connections. The session value applies to SELECT executions executed within the session that include
no MAX_EXECUTION_TIME(N) optimizer hint or for which N is 0.

• max_execution_time applies to read-only SELECT statements. Statements that are not read only

are those that invoke a stored function that modifies data as a side effect.

• max_execution_time is ignored for SELECT statements in stored programs.

• max_heap_table_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--max-heap-table-size=#

max_heap_table_size

Global, Session

Yes

Integer

16777216

16384

Maximum Value (64-bit platforms)

18446744073709550592

Maximum Value (32-bit platforms)

4294966272

Unit

Block Size

bytes

1024

This variable sets the maximum size to which user-created MEMORY tables are permitted to grow. The
value of the variable is used to calculate MEMORY table MAX_ROWS values.

Setting this variable has no effect on any existing MEMORY table, unless the table is re-created with a
statement such as CREATE TABLE or altered with ALTER TABLE or TRUNCATE TABLE. A server restart
also sets the maximum size of existing MEMORY tables to the global max_heap_table_size value.

This variable is also used in conjunction with tmp_table_size to limit the size of internal in-memory
tables. See Section 8.4.4, “Internal Temporary Table Use in MySQL”.

max_heap_table_size is not replicated. See Section 16.4.1.20, “Replication and MEMORY Tables”,
and Section 16.4.1.37, “Replication and Variables”, for more information.

• max_insert_delayed_threads

Deprecated

System Variable

Scope

Dynamic

Type

Yes

max_insert_delayed_threads

Global, Session

Yes

Integer

818

Server System Variables

Default Value

Minimum Value

Maximum Value

0

20

16384

This variable is a synonym for max_delayed_threads.

This system variable is deprecated (because DELAYED inserts are not supported); expect it to be
removed in a future release.

• max_join_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--max-join-size=#

max_join_size

Global, Session

Yes

Integer

18446744073709551615

1

18446744073709551615

Do not permit statements that probably need to examine more than max_join_size rows (for single-
table statements) or row combinations (for multiple-table statements) or that are likely to do more than
max_join_size disk seeks. By setting this value, you can catch statements where keys are not used
properly and that would probably take a long time. Set it if your users tend to perform joins that lack a
WHERE clause, that take a long time, or that return millions of rows. For more information, see Using
Safe-Updates Mode (--safe-updates).

Setting this variable to a value other than DEFAULT resets the value of sql_big_selects to 0. If you
set the sql_big_selects value again, the max_join_size variable is ignored.

If a query result is in the query cache, no result size check is performed, because the result has
previously been computed and it does not burden the server to send it to the client.

• max_length_for_sort_data

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--max-length-for-sort-data=#

max_length_for_sort_data

Global, Session

Yes

Integer

1024

4

8388608

bytes

The cutoff on the size of index values that determines which filesort algorithm to use. See
Section 8.2.1.14, “ORDER BY Optimization”.

819

Server System Variables

• max_points_in_geometry

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--max-points-in-geometry=#

max_points_in_geometry

Global, Session

Yes

Integer

65536

3

1048576

The maximum value of the points_per_circle argument to the ST_Buffer_Strategy() function.

• max_prepared_stmt_count

Command-Line Format

System Variable

--max-prepared-stmt-count=#

max_prepared_stmt_count

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

16382

0

1048576

This variable limits the total number of prepared statements in the server. It can be used in environments
where there is the potential for denial-of-service attacks based on running the server out of memory by
preparing huge numbers of statements. If the value is set lower than the current number of prepared
statements, existing statements are not affected and can be used, but no new statements can be
prepared until the current number drops below the limit. Setting the value to 0 disables prepared
statements.

• max_seeks_for_key

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (Windows)

--max-seeks-for-key=#

max_seeks_for_key

Global, Session

Yes

Integer

4294967295

Default Value (Other, 64-bit platforms)

18446744073709551615

Default Value (Other, 32-bit platforms)

4294967295

Minimum Value

Maximum Value (Windows)

1

4294967295

Maximum Value (Other, 64-bit platforms)

18446744073709551615

Maximum Value (Other, 32-bit platforms)

4294967295

820

Server System Variables

Limit the assumed maximum number of seeks when looking up rows based on a key. The MySQL
optimizer assumes that no more than this number of key seeks are required when searching for
matching rows in a table by scanning an index, regardless of the actual cardinality of the index (see
Section 13.7.5.22, “SHOW INDEX Statement”). By setting this to a low value (say, 100), you can force
MySQL to prefer indexes instead of table scans.

• max_sort_length

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--max-sort-length=#

max_sort_length

Global, Session

Yes

Integer

1024

4

8388608

bytes

The number of bytes to use when sorting data values. The server uses only the first max_sort_length
bytes of each value and ignores the rest. Consequently, values that differ only after the first
max_sort_length bytes compare as equal for GROUP BY, ORDER BY, and DISTINCT operations.

Increasing the value of max_sort_length may require increasing the value of sort_buffer_size as
well. For details, see Section 8.2.1.14, “ORDER BY Optimization”

• max_sp_recursion_depth

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--max-sp-recursion-depth[=#]

max_sp_recursion_depth

Global, Session

Yes

Integer

0

0

255

The number of times that any given stored procedure may be called recursively. The default value for
this option is 0, which completely disables recursion in stored procedures. The maximum value is 255.

Stored procedure recursion increases the demand on thread stack space. If you increase the value of
max_sp_recursion_depth, it may be necessary to increase thread stack size by increasing the value
of thread_stack at server startup.

• max_tmp_tables

This variable is unused. It is deprecated and is removed in MySQL 8.0.

821

Server System Variables

• max_user_connections

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--max-user-connections=#

max_user_connections

Global, Session

Yes

Integer

0

0

4294967295

The maximum number of simultaneous connections permitted to any given MySQL user account. A
value of 0 (the default) means “no limit.”

This variable has a global value that can be set at server startup or runtime. It also has a read-only
session value that indicates the effective simultaneous-connection limit that applies to the account
associated with the current session. The session value is initialized as follows:

• If the user account has a nonzero MAX_USER_CONNECTIONS resource limit, the session

max_user_connections value is set to that limit.

• Otherwise, the session max_user_connections value is set to the global value.

Account resource limits are specified using the CREATE USER or ALTER USER statement. See
Section 6.2.16, “Setting Account Resource Limits”.

• max_write_lock_count

Command-Line Format

System Variable

Scope

Dynamic

Type

--max-write-lock-count=#

max_write_lock_count

Global

Yes

Integer

Default Value (Windows)

4294967295

Default Value (Other, 64-bit platforms)

18446744073709551615

Default Value (Other, 32-bit platforms)

4294967295

Minimum Value

Maximum Value (Windows)

1

4294967295

Maximum Value (Other, 64-bit platforms)

18446744073709551615

Maximum Value (Other, 32-bit platforms)

4294967295

After this many write locks, permit some pending read lock requests to be processed in between. Write
lock requests have higher priority than read lock requests. However, if max_write_lock_count is set
to some low value (say, 10), read lock requests may be preferred over pending write lock requests if
the read lock requests have already been passed over in favor of 10 write lock requests. Normally this
behavior does not occur because max_write_lock_count by default has a very large value.

822

Server System Variables

• mecab_rc_file

Command-Line Format

System Variable

Scope

Dynamic

Type

--mecab-rc-file=file_name

mecab_rc_file

Global

No

File name

The mecab_rc_file option is used when setting up the MeCab full-text parser.

The mecab_rc_file option defines the path to the mecabrc configuration file, which is the
configuration file for MeCab. The option is read-only and can only be set at startup. The mecabrc
configuration file is required to initialize MeCab.

For information about the MeCab full-text parser, see Section 12.9.9, “MeCab Full-Text Parser Plugin”.

For information about options that can be specified in the MeCab mecabrc configuration file, refer to the
MeCab Documentation on the Google Developers site.

• metadata_locks_cache_size

Command-Line Format

--metadata-locks-cache-size=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Yes

metadata_locks_cache_size

Global

No

Integer

1024

1

1048576

bytes

The size of the metadata locks cache. The server uses this cache to avoid creation and destruction of
synchronization objects. This is particularly helpful on systems where such operations are expensive,
such as Windows XP.

In MySQL 5.7.4, metadata locking implementation changes make this variable unnecessary, and so it is
deprecated; expect it to be removed in a future release of MySQL.

• metadata_locks_hash_instances

Command-Line Format

--metadata-locks-hash-instances=#

Deprecated

System Variable

Scope

Dynamic

Type

Yes

metadata_locks_hash_instances

Global

No

Integer

823

Default Value

Minimum Value

Maximum Value

Server System Variables

8

1

1024

The set of metadata locks can be partitioned into separate hashes to permit connections
accessing different objects to use different locking hashes and reduce contention. The
metadata_locks_hash_instances system variable specifies the number of hashes (default 8).

In MySQL 5.7.4, metadata locking implementation changes make this variable unnecessary, and so it is
deprecated; expect it to be removed in a future release of MySQL.

• min_examined_row_limit

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--min-examined-row-limit=#

min_examined_row_limit

Global, Session

Yes

Integer

0

0

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

Queries that examine fewer than this number of rows are not logged to the slow query log.

• multi_range_count

Command-Line Format

--multi-range-count=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Yes

multi_range_count

Global, Session

Yes

Integer

256

1

4294967295

This variable has no effect. It is deprecated and is removed in MySQL 8.0.

• myisam_data_pointer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

--myisam-data-pointer-size=#

myisam_data_pointer_size

Global

Yes

Integer

824

Default Value

Minimum Value

Maximum Value

Unit

Server System Variables

6

2

7

bytes

The default pointer size in bytes, to be used by CREATE TABLE for MyISAM tables when no MAX_ROWS
option is specified. This variable cannot be less than 2 or larger than 7. The default value is 6. See
Section B.3.2.10, “The table is full”.

• myisam_max_sort_file_size

Command-Line Format

System Variable

Scope

Dynamic

Type

--myisam-max-sort-file-size=#

myisam_max_sort_file_size

Global

Yes

Integer

Default Value (Windows)

2146435072

Default Value (Other, 64-bit platforms)

9223372036853727232

Default Value (Other, 32-bit platforms)

2147483648

Minimum Value

Maximum Value (Windows)

0

2146435072

Maximum Value (Other, 64-bit platforms)

9223372036853727232

Maximum Value (Other, 32-bit platforms)

2147483648

Unit

bytes

The maximum size of the temporary file that MySQL is permitted to use while re-creating a MyISAM
index (during REPAIR TABLE, ALTER TABLE, or LOAD DATA). If the file size would be larger than this
value, the index is created using the key cache instead, which is slower. The value is given in bytes.

If MyISAM index files exceed this size and disk space is available, increasing the value may help
performance. The space must be available in the file system containing the directory where the original
index file is located.

• myisam_mmap_size

Command-Line Format

System Variable

Scope

Dynamic

Type

--myisam-mmap-size=#

myisam_mmap_size

Global

No

Integer

Default Value (64-bit platforms)

Default Value (32-bit platforms)

Minimum Value

18446744073709551615

4294967295

7

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

825

Server System Variables

Unit

bytes

The maximum amount of memory to use for memory mapping compressed MyISAM files. If many
compressed MyISAM tables are used, the value can be decreased to reduce the likelihood of memory-
swapping problems.

• myisam_recover_options

Command-Line Format

System Variable

--myisam-recover-options[=list]

myisam_recover_options

Scope

Dynamic

Type

Default Value

Valid Values

Global

No

Enumeration

OFF

OFF

DEFAULT

BACKUP

FORCE

QUICK

Set the MyISAM storage engine recovery mode. The variable value is any combination of the values of
OFF, DEFAULT, BACKUP, FORCE, or QUICK. If you specify multiple values, separate them by commas.
Specifying the variable with no value at server startup is the same as specifying DEFAULT, and
specifying with an explicit value of "" disables recovery (same as a value of OFF). If recovery is enabled,
each time mysqld opens a MyISAM table, it checks whether the table is marked as crashed or was not
closed properly. (The last option works only if you are running with external locking disabled.) If this is
the case, mysqld runs a check on the table. If the table was corrupted, mysqld attempts to repair it.

The following options affect how the repair works.

Option

OFF

DEFAULT

BACKUP

FORCE

QUICK

Description

No recovery.

Recovery without backup, forcing, or quick
checking.

If the data file was changed during recovery,
save a backup of the tbl_name.MYD file as
tbl_name-datetime.BAK.

Run recovery even if we would lose more than one
row from the .MYD file.

Do not check the rows in the table if there are not
any delete blocks.

Before the server automatically repairs a table, it writes a note about the repair to the error log. If you
want to be able to recover from most problems without user intervention, you should use the options

826

Server System Variables

BACKUP,FORCE. This forces a repair of a table even if some rows would be deleted, but it keeps the old
data file as a backup so that you can later examine what happened.

See Section 15.2.1, “MyISAM Startup Options”.

• myisam_repair_threads

Command-Line Format

--myisam-repair-threads=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

5.7.38 (removed in 5.7.39)

myisam_repair_threads

Global, Session

Yes

Integer

1

1

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

Note

This system variable is deprecated in MySQL 5.7; expect it to be removed in a
future release of MySQL.

From MySQL 5.7.38, values other than 1 produce a warning.

If this value is greater than 1, MyISAM table indexes are created in parallel (each index in its own thread)
during the Repair by sorting process. The default value is 1.

Note

Multithreaded repair is beta-quality code.

• myisam_sort_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--myisam-sort-buffer-size=#

myisam_sort_buffer_size

Global, Session

Yes

Integer

8388608

4096

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

Unit

4294967295

bytes

The size of the buffer that is allocated when sorting MyISAM indexes during a REPAIR TABLE or when
creating indexes with CREATE INDEX or ALTER TABLE.

827

Server System Variables

• myisam_stats_method

Command-Line Format

System Variable

--myisam-stats-method=name

myisam_stats_method

Scope

Dynamic

Type

Default Value

Valid Values

Global, Session

Yes

Enumeration

nulls_unequal

nulls_unequal

nulls_equal

nulls_ignored

How the server treats NULL values when collecting statistics about the distribution of index values
for MyISAM tables. This variable has three possible values, nulls_equal, nulls_unequal, and
nulls_ignored. For nulls_equal, all NULL index values are considered equal and form a single
value group that has a size equal to the number of NULL values. For nulls_unequal, NULL values are
considered unequal, and each NULL forms a distinct value group of size 1. For nulls_ignored, NULL
values are ignored.

The method that is used for generating table statistics influences how the optimizer chooses indexes for
query execution, as described in Section 8.3.7, “InnoDB and MyISAM Index Statistics Collection”.

• myisam_use_mmap

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--myisam-use-mmap[={OFF|ON}]

myisam_use_mmap

Global

Yes

Boolean

OFF

Use memory mapping for reading and writing MyISAM tables.

• mysql_native_password_proxy_users

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--mysql-native-password-proxy-
users[={OFF|ON}]

mysql_native_password_proxy_users

Global

Yes

Boolean

OFF

This variable controls whether the mysql_native_password built-in authentication plugin supports
proxy users. It has no effect unless the check_proxy_users system variable is enabled. For
information about user proxying, see Section 6.2.14, “Proxy Users”.

828

Server System Variables

• named_pipe

Command-Line Format

System Variable

Scope

Dynamic

Platform Specific

Type

Default Value

--named-pipe[={OFF|ON}]

named_pipe

Global

No

Windows

Boolean

OFF

(Windows only.) Indicates whether the server supports connections over named pipes.

• named_pipe_full_access_group

Command-Line Format

--named-pipe-full-access-group=value

Introduced

System Variable

Scope

Dynamic

Platform Specific

Type

Default Value

Valid Values

5.7.25

named_pipe_full_access_group

Global

No

Windows

String

empty string

empty string

valid Windows local group name

*everyone*

(Windows only.) The access control granted to clients on the named pipe created by the MySQL server
is set to the minimum necessary for successful communication when the named_pipe system variable
is enabled to support named-pipe connections. Some MySQL client software can open named pipe
connections without any additional configuration; however, other client software may still require full
access to open a named pipe connection.

This variable sets the name of a Windows local group whose members are granted sufficient access by
the MySQL server to use named-pipe clients. As of MySQL 5.7.34, the default value is set to an empty
string, which means that no Windows user is granted full access to the named pipe.

A new Windows local group name (for example, mysql_access_client_users) can be created in
Windows and then used to replace the default value when access is absolutely necessary. In this case,
limit the membership of the group to as few users as possible, removing users from the group when their
client software is upgraded. A non-member of the group who attempts to open a connection to MySQL
with the affected named-pipe client is denied access until a Windows administrator adds the user to the
group. Newly added users must log out and log in again to join the group (required by Windows).

Setting the value to '*everyone*' provides a language-independent way of referring to the Everyone
group on Windows. The Everyone group is not secure by default.

829

• net_buffer_length

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Block Size

Server System Variables

--net-buffer-length=#

net_buffer_length

Global, Session

Yes

Integer

16384

1024

1048576

bytes

1024

Each client thread is associated with a connection buffer and result buffer. Both begin with a size given
by net_buffer_length but are dynamically enlarged up to max_allowed_packet bytes as needed.
The result buffer shrinks to net_buffer_length after each SQL statement.

This variable should not normally be changed, but if you have very little memory, you can set it to the
expected length of statements sent by clients. If statements exceed this length, the connection buffer is
automatically enlarged. The maximum value to which net_buffer_length can be set is 1MB.

The session value of this variable is read only.

• net_read_timeout

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--net-read-timeout=#

net_read_timeout

Global, Session

Yes

Integer

30

1

31536000

seconds

The number of seconds to wait for more data from a connection before aborting the read. When the
server is reading from the client, net_read_timeout is the timeout value controlling when to abort.
When the server is writing to the client, net_write_timeout is the timeout value controlling when to
abort. See also slave_net_timeout.

• net_retry_count

Command-Line Format

System Variable

Scope

Dynamic

830

--net-retry-count=#

net_retry_count

Global, Session

Yes

Server System Variables

Type

Default Value

Minimum Value

Integer

10

1

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

If a read or write on a communication port is interrupted, retry this many times before giving up. This
value should be set quite high on FreeBSD because internal interrupts are sent to all threads.

• net_write_timeout

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--net-write-timeout=#

net_write_timeout

Global, Session

Yes

Integer

60

1

31536000

seconds

The number of seconds to wait for a block to be written to a connection before aborting the write. See
also net_read_timeout.

• new

Command-Line Format

System Variable

Scope

Dynamic

Disabled by

Type

Default Value

--new[={OFF|ON}]

new

Global, Session

Yes

skip-new

Boolean

OFF

This variable was used in MySQL 4.0 to turn on some 4.1 behaviors, and is retained for backward
compatibility. Its value is always OFF.

In NDB Cluster, setting this variable to ON makes it possible to employ partitioning types other than KEY
or LINEAR KEY with NDB tables. This experimental feature is not supported in production, and is now
deprecated and thus subject to removal in a future release. For additional information, see User-defined
partitioning and the NDB storage engine (NDB Cluster).

• ngram_token_size

Command-Line Format

System Variable

Scope

--ngram-token-size=#

ngram_token_size

Global

831

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Server System Variables

No

Integer

2

1

10

Defines the n-gram token size for the n-gram full-text parser. The ngram_token_size option is read-
only and can only be modified at startup. The default value is 2 (bigram). The maximum value is 10.

For more information about how to configure this variable, see Section 12.9.8, “ngram Full-Text Parser”.

• offline_mode

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--offline-mode[={OFF|ON}]

offline_mode

Global

Yes

Boolean

OFF

Whether the server is in “offline mode”, which has these characteristics:

• Connected client users who do not have the SUPER privilege are disconnected on the next request,

with an appropriate error. Disconnection includes terminating running statements and releasing locks.
Such clients also cannot initiate new connections, and receive an appropriate error.

• Connected client users who have the SUPER privilege are not disconnected, and can initiate new

connections to manage the server.

• Replica threads are permitted to keep applying data to the server.

Only users who have the SUPER privilege can control offline mode. To put a server in offline mode,
change the value of the offline_mode system variable from OFF to ON. To resume normal operations,
change offline_mode from ON to OFF. In offline mode, clients that are refused access receive an
ER_SERVER_OFFLINE_MODE error.

• old

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--old[={OFF|ON}]

old

Global

No

Boolean

OFF

old is a compatibility variable. It is disabled by default, but can be enabled at startup to revert the server
to behaviors present in older versions.

When old is enabled, it changes the default scope of index hints to that used prior to MySQL 5.1.17.
That is, index hints with no FOR clause apply only to how indexes are used for row retrieval and not

832

Server System Variables

to resolution of ORDER BY or GROUP BY clauses. (See Section 8.9.4, “Index Hints”.) Take care about
enabling this in a replication setup. With statement-based binary logging, having different modes for the
source and replicas might lead to replication errors.

• old_alter_table

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--old-alter-table[={OFF|ON}]

old_alter_table

Global, Session

Yes

Boolean

OFF

When this variable is enabled, the server does not use the optimized method of processing an ALTER
TABLE operation. It reverts to using a temporary table, copying over the data, and then renaming the
temporary table to the original, as used by MySQL 5.0 and earlier. For more information on the operation
of ALTER TABLE, see Section 13.1.8, “ALTER TABLE Statement”.

• old_passwords

Command-Line Format

--old-passwords=value

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

Yes

old_passwords

Global, Session

Yes

Enumeration

0

0

2

Note

This system variable is deprecated in MySQL 5.7; expect it to be removed in a
future release of MySQL.

This variable controls the password hashing method used by the PASSWORD() function. It also
influences password hashing performed by CREATE USER and GRANT statements that specify a
password using an IDENTIFIED BY clause.

The following table shows, for each password hashing method, the permitted value of old_passwords
and which authentication plugins use the hashing method.

Password Hashing Method

old_passwords Value

MySQL 4.1 native hashing

0

Associated Authentication
Plugin

mysql_native_password

833

Server System Variables

Password Hashing Method

old_passwords Value

SHA-256 hashing

2

Associated Authentication
Plugin

sha256_password

If you set old_passwords=2, follow the instructions for using the sha256_password plugin at
Section 6.4.1.5, “SHA-256 Pluggable Authentication”.

The server sets the global old_passwords value during startup to be consistent with
the password hashing method required by the authentication plugin indicated by the
default_authentication_plugin system variable.

When a client successfully connects to the server, the server sets the session old_passwords
value appropriately for the account authentication method. For example, if the account uses the
sha256_password authentication plugin, the server sets old_passwords=2.

For additional information about authentication plugins and hashing formats, see Section 6.2.13,
“Pluggable Authentication”, and Section 6.1.2.4, “Password Hashing in MySQL”.

• open_files_limit

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--open-files-limit=#

open_files_limit

Global

No

Integer

5000, with possible adjustment

0

platform dependent

The number of file descriptors available to mysqld from the operating system:

• At startup, mysqld reserves descriptors with setrlimit(), using the value requested at by

setting this variable directly or by using the --open-files-limit option to mysqld_safe. If
mysqld produces the error Too many open files, try increasing the open_files_limit value.
Internally, the maximum value for this variable is the maximum unsigned integer value, but the actual
maximum is platform dependent.

• At runtime, the value of open_files_limit indicates the number of file descriptors actually

permitted to mysqld by the operating system, which might differ from the value requested at startup. If
the number of file descriptors requested during startup cannot be allocated, mysqld writes a warning
to the error log.

The effective open_files_limit value is based on the value specified at system startup (if any) and
the values of max_connections and table_open_cache, using these formulas:

• 10 + max_connections + (table_open_cache * 2)

• max_connections * 5

• The operating system limit if that limit is positive but not Infinity.

834

Server System Variables

• If the operating system limit is Infinity: open_files_limit value if specified at startup, 5000 if not.

The server attempts to obtain the number of file descriptors using the maximum of those values. If that
many descriptors cannot be obtained, the server attempts to obtain as many as the system permits.

The effective value is 0 on systems where MySQL cannot change the number of open files.

On Unix, the value cannot be set greater than the value displayed by the ulimit -n command.
On Linux systems using systemd, the value cannot be set greater than LimitNOFile (this
is DefaultLimitNOFILE, if LimitNOFile is not set); otherwise, on Linux, the value of
open_files_limit cannot exceed ulimit -n.

• optimizer_prune_level

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--optimizer-prune-level=#

optimizer_prune_level

Global, Session

Yes

Integer

1

0

1

Controls the heuristics applied during query optimization to prune less-promising partial plans from the
optimizer search space. A value of 0 disables heuristics so that the optimizer performs an exhaustive
search. A value of 1 causes the optimizer to prune plans based on the number of rows retrieved by
intermediate plans.

• optimizer_search_depth

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--optimizer-search-depth=#

optimizer_search_depth

Global, Session

Yes

Integer

62

0

62

The maximum depth of search performed by the query optimizer. Values larger than the number of
relations in a query result in better query plans, but take longer to generate an execution plan for a
query. Values smaller than the number of relations in a query return an execution plan quicker, but the
resulting plan may be far from being optimal. If set to 0, the system automatically picks a reasonable
value.

• optimizer_switch

Command-Line Format

--optimizer-switch=value

835

Server System Variables

System Variable

Scope

Dynamic

Type

optimizer_switch

Global, Session

Yes

Set

Valid Values (≥ 5.7.33)

batched_key_access={on|off}

block_nested_loop={on|off}

condition_fanout_filter={on|off}

derived_merge={on|off}

duplicateweedout={on|off}

engine_condition_pushdown={on|off}

firstmatch={on|off}

index_condition_pushdown={on|off}

index_merge={on|off}

index_merge_intersection={on|off}

index_merge_sort_union={on|off}

index_merge_union={on|off}

loosescan={on|off}

materialization={on|off}

mrr={on|off}

mrr_cost_based={on|off}

prefer_ordering_index={on|off}

semijoin={on|off}

subquery_materialization_cost_based={on|
off}

use_index_extensions={on|off}

batched_key_access={on|off}

block_nested_loop={on|off}

condition_fanout_filter={on|off}

derived_merge={on|off}

duplicateweedout={on|off}

engine_condition_pushdown={on|off}

Valid Values (≤ 5.7.32)

836

Server System Variables

firstmatch={on|off}

index_condition_pushdown={on|off}

index_merge={on|off}

index_merge_intersection={on|off}

index_merge_sort_union={on|off}

index_merge_union={on|off}

loosescan={on|off}

materialization={on|off}

mrr={on|off}

mrr_cost_based={on|off}

semijoin={on|off}

subquery_materialization_cost_based={on|
off}

use_index_extensions={on|off}

The optimizer_switch system variable enables control over optimizer behavior. The value of this
variable is a set of flags, each of which has a value of on or off to indicate whether the corresponding
optimizer behavior is enabled or disabled. This variable has global and session values and can be
changed at runtime. The global default can be set at server startup.

To see the current set of optimizer flags, select the variable value:

mysql> SELECT @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,
                    index_merge_sort_union=on,
                    index_merge_intersection=on,
                    engine_condition_pushdown=on,
                    index_condition_pushdown=on,
                    mrr=on,mrr_cost_based=on,
                    block_nested_loop=on,batched_key_access=off,
                    materialization=on,semijoin=on,loosescan=on,
                    firstmatch=on,duplicateweedout=on,
                    subquery_materialization_cost_based=on,
                    use_index_extensions=on,
                    condition_fanout_filter=on,derived_merge=on,
                    prefer_ordering_index=on

For more information about the syntax of this variable and the optimizer behaviors that it controls, see
Section 8.9.2, “Switchable Optimizations”.

• optimizer_trace

Command-Line Format

--optimizer-trace=value

System Variable

Scope

optimizer_trace

Global, Session

837

Server System Variables

Dynamic

Type

Yes

String

This variable controls optimizer tracing. For details, see Section 8.15, “Tracing the Optimizer”.

• optimizer_trace_features

Command-Line Format

System Variable

Scope

Dynamic

Type

--optimizer-trace-features=value

optimizer_trace_features

Global, Session

Yes

String

This variable enables or disables selected optimizer tracing features. For details, see Section 8.15,
“Tracing the Optimizer”.

• optimizer_trace_limit

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--optimizer-trace-limit=#

optimizer_trace_limit

Global, Session

Yes

Integer

1

0

2147483647

The maximum number of optimizer traces to display. For details, see Section 8.15, “Tracing the
Optimizer”.

• optimizer_trace_max_mem_size

Command-Line Format

System Variable

--optimizer-trace-max-mem-size=#

optimizer_trace_max_mem_size

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Global, Session

Yes

Integer

16384

0

4294967295

bytes

The maximum cumulative size of stored optimizer traces. For details, see Section 8.15, “Tracing the
Optimizer”.

838

Server System Variables

• optimizer_trace_offset

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--optimizer-trace-offset=#

optimizer_trace_offset

Global, Session

Yes

Integer

-1

-2147483647

2147483647

The offset of optimizer traces to display. For details, see Section 8.15, “Tracing the Optimizer”.

• performance_schema_xxx

Performance Schema system variables are listed in Section 25.15, “Performance Schema System
Variables”. These variables may be used to configure Performance Schema operation.

• parser_max_mem_size

Command-Line Format

--parser-max-mem-size=#

Introduced

System Variable

Scope

Dynamic

Type

Default Value (64-bit platforms)

Default Value (32-bit platforms)

Minimum Value

5.7.12

parser_max_mem_size

Global, Session

Yes

Integer

18446744073709551615

4294967295

10000000

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

Unit

4294967295

bytes

The maximum amount of memory available to the parser. The default value places no limit on memory
available. The value can be reduced to protect against out-of-memory situations caused by parsing long
or complex SQL statements.

• pid_file

Command-Line Format

System Variable

Scope

Dynamic

--pid-file=file_name

pid_file

Global

No

839

Server System Variables

Type

File name

The path name of the file in which the server writes its process ID. The server creates the file in the
data directory unless an absolute path name is given to specify a different directory. If you specify this
variable, you must specify a value. If you do not specify this variable, MySQL uses a default value of
host_name.pid, where host_name is the name of the host machine.

The process ID file is used by other programs such as mysqld_safe to determine the server's process
ID. On Windows, this variable also affects the default error log file name. See Section 5.4.2, “The Error
Log”.

• plugin_dir

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--plugin-dir=dir_name

plugin_dir

Global

No

Directory name

BASEDIR/lib/plugin

The path name of the plugin directory.

If the plugin directory is writable by the server, it may be possible for a user to write executable code
to a file in the directory using SELECT ... INTO DUMPFILE. This can be prevented by making
plugin_dir read only to the server or by setting secure_file_priv to a directory where SELECT
writes can be made safely.

• port

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--port=port_num

port

Global

No

Integer

3306

0

65535

The number of the port on which the server listens for TCP/IP connections. This variable can be set with
the --port option.

• preload_buffer_size

Command-Line Format

System Variable

--preload-buffer-size=#

preload_buffer_size

Scope

Dynamic

Type

840

Global, Session

Yes

Integer

Server System Variables

Default Value

Minimum Value

Maximum Value

Unit

32768

1024

1073741824

bytes

The size of the buffer that is allocated when preloading indexes.

• profiling

If set to 0 or OFF (the default), statement profiling is disabled. If set to 1 or ON, statement profiling
is enabled and the SHOW PROFILE and SHOW PROFILES statements provide access to profiling
information. See Section 13.7.5.31, “SHOW PROFILES Statement”.

This variable is deprecated; expect it to be removed in a future release of MySQL.

• profiling_history_size

The number of statements for which to maintain profiling information if profiling is enabled. The
default value is 15. The maximum value is 100. Setting the value to 0 effectively disables profiling. See
Section 13.7.5.31, “SHOW PROFILES Statement”.

This variable is deprecated; expect it to be removed in a future release of MySQL.

• protocol_version

System Variable

protocol_version

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

No

Integer

10

0

4294967295

The version of the client/server protocol used by the MySQL server.

• proxy_user

System Variable

Scope

Dynamic

Type

proxy_user

Session

No

String

If the current client is a proxy for another user, this variable is the proxy user account name. Otherwise,
this variable is NULL. See Section 6.2.14, “Proxy Users”.

• pseudo_slave_mode

System Variable

Scope

Dynamic

pseudo_slave_mode

Session

Yes

841

Server System Variables

Type

Boolean

This system variable is for internal server use. pseudo_slave_mode assists with the correct handling
of transactions that originated on older or newer servers than the server currently processing them.
mysqlbinlog sets the value of pseudo_slave_mode to true before executing any SQL statements.

pseudo_slave_mode has the following effects on the handling of prepared XA transactions, which can
be attached to or detached from the handling session (by default, the session that issues XA START):

• If true, and the handling session has executed an internal-use BINLOG statement, XA transactions are
automatically detached from the session as soon as the first part of the transaction up to XA PREPARE
finishes, so they can be committed or rolled back by any session that has the XA_RECOVER_ADMIN
privilege.

• If false, XA transactions remain attached to the handling session as long as that session is alive,
during which time no other session can commit the transaction. The prepared transaction is only
detached if the session disconnects or the server restarts.

• pseudo_thread_id

System Variable

pseudo_thread_id

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

This variable is for internal server use.

Warning

Session

Yes

Integer

2147483647

0

2147483647

Changing the session value of the pseudo_thread_id system variable
changes the value returned by the CONNECTION_ID() function.

• query_alloc_block_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

842

--query-alloc-block-size=#

query_alloc_block_size

Global, Session

Yes

Integer

8192

1024

4294966272

bytes

Server System Variables

Block Size

1024

The allocation size in bytes of memory blocks that are allocated for objects created during statement
parsing and execution. If you have problems with memory fragmentation, it might help to increase this
parameter.

The block size for the byte number is 1024. A value that is not an exact multiple of the block size is
rounded down to the next lower multiple of the block size by MySQL Server before storing the value for
the system variable. The parser allows values up to the maximum unsigned integer value for the platform
(4294967295 or 232
−1 for a 64-bit system) but the
actual maximum is a block size lower.

−1 for a 32-bit system, 18446744073709551615 or 264

• query_cache_limit

Command-Line Format

--query-cache-limit=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

5.7.20

query_cache_limit

Global

Yes

Integer

1048576

0

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

Unit

4294967295

bytes

Do not cache results that are larger than this number of bytes. The default value is 1MB.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes query_cache_limit.

• query_cache_min_res_unit

Command-Line Format

--query-cache-min-res-unit=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

5.7.20

query_cache_min_res_unit

Global

Yes

Integer

4096

512

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

4294967295

843

Server System Variables

Unit

bytes

The minimum size (in bytes) for blocks allocated by the query cache. The default value is 4096 (4KB).
Tuning information for this variable is given in Section 8.10.3.3, “Query Cache Configuration”.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes query_cache_min_res_unit.

• query_cache_size

Command-Line Format

--query-cache-size=#

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

5.7.20

query_cache_size

Global

Yes

Integer

1048576

0

Maximum Value (64-bit platforms)

18446744073709551615

Maximum Value (32-bit platforms)

Unit

4294967295

bytes

The amount of memory allocated for caching query results. By default, the query cache is
disabled. This is achieved using a default value of 1M, with a default for query_cache_type of
0. (To reduce overhead significantly if you set the size to 0, you should also start the server with
query_cache_type=0.

The permissible values are multiples of 1024; other values are rounded down to the nearest multiple.
For nonzero values of query_cache_size, that many bytes of memory are allocated even if
query_cache_type=0. See Section 8.10.3.3, “Query Cache Configuration”, for more information.

The query cache needs a minimum size of about 40KB to allocate its structures. (The exact size
depends on system architecture.) If you set the value of query_cache_size too small, a warning
occurs, as described in Section 8.10.3.3, “Query Cache Configuration”.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes query_cache_size.

• query_cache_type

Command-Line Format

--query-cache-type=#

Deprecated

System Variable

Scope

Dynamic

844

5.7.20

query_cache_type

Global, Session

Yes

Type

Default Value

Valid Values

Server System Variables

Enumeration

0

0

1

2

Set the query cache type. Setting the GLOBAL value sets the type for all clients that connect thereafter.
Individual clients can set the SESSION value to affect their own use of the query cache. Possible values
are shown in the following table.

Option

0 or OFF

1 or ON

2 or DEMAND

Description

Do not cache results in or retrieve results from the
query cache. Note that this does not deallocate
the query cache buffer. To do that, you should set
query_cache_size to 0.

Cache all cacheable query results except for those
that begin with SELECT SQL_NO_CACHE.

Cache results only for cacheable queries that begin
with SELECT SQL_CACHE.

This variable defaults to OFF.

If the server is started with query_cache_type set to 0, it does not acquire the query cache mutex at
all, which means that the query cache cannot be enabled at runtime and there is reduced overhead in
query execution.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes query_cache_type.

• query_cache_wlock_invalidate

Command-Line Format

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

--query-cache-wlock-invalidate[={OFF|
ON}]

5.7.20

query_cache_wlock_invalidate

Global, Session

Yes

Boolean

OFF

Normally, when one client acquires a WRITE lock on a table, other clients are not blocked from issuing
statements that read from the table if the query results are present in the query cache. Setting this
variable to 1 causes acquisition of a WRITE lock for a table to invalidate any queries in the query cache

845

Server System Variables

that refer to the table. This forces other clients that attempt to access the table to wait while the lock is in
effect.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes query_cache_wlock_invalidate.

• query_prealloc_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--query-prealloc-size=#

query_prealloc_size

Global, Session

Yes

Integer

8192

8192

Maximum Value (64-bit platforms)

18446744073709550592

Maximum Value (32-bit platforms)

4294966272

Unit

Block Size

bytes

1024

The size in bytes of the persistent buffer used for statement parsing and execution. This buffer is not
freed between statements. If you are running complex queries, a larger query_prealloc_size value
might be helpful in improving performance, because it can reduce the need for the server to perform
memory allocation during query execution operations. You should be aware that doing this does not
necessarily eliminate allocation completely; the server may still allocate memory in some situations, such
as for operations relating to transactions, or to stored programs.

• rand_seed1

System Variable

rand_seed1

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Session

Yes

Integer

N/A

0

4294967295

The rand_seed1 and rand_seed2 variables exist as session variables only, and can be set but not
read. The variables—but not their values—are shown in the output of SHOW VARIABLES.

The purpose of these variables is to support replication of the RAND() function. For statements that
invoke RAND(), the source passes two values to the replica, where they are used to seed the random
number generator. The replica uses these values to set the session variables rand_seed1 and
rand_seed2 so that RAND() on the replica generates the same value as on the source.

846

Server System Variables

• rand_seed2

See the description for rand_seed1.

• range_alloc_block_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--range-alloc-block-size=#

range_alloc_block_size

Global, Session

Yes

Integer

4096

4096

Maximum Value (64-bit platforms)

18446744073709550592

Maximum Value

Unit

Block Size

4294966272

bytes

1024

The size in bytes of blocks that are allocated when doing range optimization.

The block size for the byte number is 1024. A value that is not an exact multiple of the block size is
rounded down to the next lower multiple of the block size by MySQL Server before storing the value for
the system variable. The parser allows values up to the maximum unsigned integer value for the platform
(4294967295 or 232
−1 for a 64-bit system) but the
actual maximum is a block size lower.

−1 for a 32-bit system, 18446744073709551615 or 264

• range_optimizer_max_mem_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (≥ 5.7.12)
Default Value (≤ 5.7.11)
Minimum Value

Maximum Value

Unit

--range-optimizer-max-mem-size=#

range_optimizer_max_mem_size

Global, Session

Yes

Integer

8388608

1536000

0

18446744073709551615

bytes

The limit on memory consumption for the range optimizer. A value of 0 means “no limit.” If an execution
plan considered by the optimizer uses the range access method but the optimizer estimates that the
amount of memory needed for this method would exceed the limit, it abandons the plan and considers
other plans. For more information, see Limiting Memory Use for Range Optimization.

• rbr_exec_mode

System Variable

rbr_exec_mode

847

Scope

Dynamic

Type

Default Value

Valid Values

Server System Variables

Session

Yes

Enumeration

STRICT

STRICT

IDEMPOTENT

For internal use by mysqlbinlog. This variable switches the server between IDEMPOTENT mode and
STRICT mode. IDEMPOTENT mode causes suppression of duplicate-key and no-key-found errors in
BINLOG statements generated by mysqlbinlog. This mode is useful when replaying a row-based
binary log on a server that causes conflicts with existing data. mysqlbinlog sets this mode when you
specify the --idempotent option by writing the following to the output:

SET SESSION RBR_EXEC_MODE=IDEMPOTENT;

• read_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Block Size

--read-buffer-size=#

read_buffer_size

Global, Session

Yes

Integer

131072

8192

2147479552

bytes

4096

Each thread that does a sequential scan for a MyISAM table allocates a buffer of this size (in bytes)
for each table it scans. If you do many sequential scans, you might want to increase this value, which
defaults to 131072. The value of this variable should be a multiple of 4KB. If it is set to a value that is not
a multiple of 4KB, its value is rounded down to the nearest multiple of 4KB.

This option is also used in the following context for all storage engines:

• For caching the indexes in a temporary file (not a temporary table), when sorting rows for ORDER BY.

• For bulk insert into partitions.

• For caching results of nested queries.

read_buffer_size is also used in one other storage engine-specific way: to determine the memory
block size for MEMORY tables.

For more information about memory use during different operations, see Section 8.12.4.1, “How MySQL
Uses Memory”.

848

Server System Variables

• read_only

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--read-only[={OFF|ON}]

read_only

Global

Yes

Boolean

OFF

If the read_only system variable is enabled, the server permits no client updates except from users
who have the SUPER privilege. This variable is disabled by default.

The server also supports a super_read_only system variable (disabled by default), which has these
effects:

• If super_read_only is enabled, the server prohibits client updates, even from users who have the

SUPER privilege.

• Setting super_read_only to ON implicitly forces read_only to ON.

• Setting read_only to OFF implicitly forces super_read_only to OFF.

Even with read_only enabled, the server permits these operations:

• Updates performed by replication threads, if the server is a replica. In replication setups, it can be

useful to enable read_only on replica servers to ensure that replicas accept updates only from the
source server and not from clients.

• Use of ANALYZE TABLE or OPTIMIZE TABLE statements. The purpose of read-only mode is to
prevent changes to table structure or contents. Analysis and optimization do not qualify as such
changes. This means, for example, that consistency checks on read-only replicas can be performed
with mysqlcheck --all-databases --analyze.

• Use of FLUSH STATUS statements, which are always written to the binary log.

• Operations on TEMPORARY tables.

• Inserts into the log tables (mysql.general_log and mysql.slow_log); see Section 5.4.1,

“Selecting General Query Log and Slow Query Log Output Destinations”.

• As of MySQL 5.7.16, updates to Performance Schema tables, such as UPDATE or TRUNCATE TABLE

operations.

Changes to read_only on a replication source server are not replicated to replica servers. The value
can be set on a replica independent of the setting on the source.

The following conditions apply to attempts to enable read_only (including implicit attempts resulting
from enabling super_read_only):

• The attempt fails and an error occurs if you have any explicit locks (acquired with LOCK TABLES) or

have a pending transaction.

• The attempt blocks while other clients have any ongoing statement, active LOCK TABLES WRITE,
or ongoing commit, until the locks are released and the statements and transactions end. While

849

Server System Variables

the attempt to enable read_only is pending, requests by other clients for table locks or to begin
transactions also block until read_only has been set.

• The attempt blocks if there are active transactions that hold metadata locks, until those transactions

end.

• read_only can be enabled while you hold a global read lock (acquired with FLUSH TABLES WITH

READ LOCK) because that does not involve table locks.

• read_rnd_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--read-rnd-buffer-size=#

read_rnd_buffer_size

Global, Session

Yes

Integer

262144

1

2147483647

bytes

This variable is used for reads from MyISAM tables, and, for any storage engine, for Multi-Range Read
optimization.

When reading rows from a MyISAM table in sorted order following a key-sorting operation, the rows are
read through this buffer to avoid disk seeks. See Section 8.2.1.14, “ORDER BY Optimization”. Setting
the variable to a large value can improve ORDER BY performance by a lot. However, this is a buffer
allocated for each client, so you should not set the global variable to a large value. Instead, change the
session variable only from within those clients that need to run large queries.

For more information about memory use during different operations, see Section 8.12.4.1, “How MySQL
Uses Memory”. For information about Multi-Range Read optimization, see Section 8.2.1.10, “Multi-
Range Read Optimization”.

• require_secure_transport

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--require-secure-transport[={OFF|ON}]

require_secure_transport

Global

Yes

Boolean

OFF

Whether client connections to the server are required to use some form of secure transport. When
this variable is enabled, the server permits only TCP/IP connections encrypted using TLS/SSL, or

850

Server System Variables

connections that use a socket file (on Unix) or shared memory (on Windows). The server rejects
nonsecure connection attempts, which fail with an ER_SECURE_TRANSPORT_REQUIRED error.

This capability supplements per-account SSL requirements, which take precedence. For example, if
an account is defined with REQUIRE SSL, enabling require_secure_transport does not make it
possible to use the account to connect using a Unix socket file.

It is possible for a server to have no secure transports available. For example, a server on Windows
supports no secure transports if started without specifying any SSL certificate or key files and
with the shared_memory system variable disabled. Under these conditions, attempts to enable
require_secure_transport at startup cause the server to write a message to the error log and exit.
Attempts to enable the variable at runtime fail with an ER_NO_SECURE_TRANSPORTS_CONFIGURED
error.

See also Configuring Encrypted Connections as Mandatory.

• secure_auth

Command-Line Format

--secure-auth[={OFF|ON}]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

Yes

secure_auth

Global

Yes

Boolean

ON

ON

If this variable is enabled, the server blocks connections by clients that attempt to use accounts that
have passwords stored in the old (pre-4.1) format. Enable this variable to prevent all use of passwords
employing the old format (and hence insecure communication over the network).

This variable is deprecated; expect it to be removed in a future release of MySQL. It is always enabled
and attempting to disable it produces an error.

Server startup fails with an error if this variable is enabled and the privilege tables are in pre-4.1 format.
See Section 6.4.1.3, “Migrating Away from Pre-4.1 Password Hashing and the mysql_old_password
Plugin”.

Note

Passwords that use the pre-4.1 hashing method are less secure than passwords
that use the native password hashing method and should be avoided. Pre-4.1
passwords are deprecated and support for them is removed in MySQL 5.7.5. For
account upgrade instructions, see Section 6.4.1.3, “Migrating Away from Pre-4.1
Password Hashing and the mysql_old_password Plugin”.

• secure_file_priv

Command-Line Format

--secure-file-priv=dir_name

System Variable

Scope

secure_file_priv

Global

851

Dynamic

Type

Default Value

Valid Values

Server System Variables

No

String

platform specific

empty string

dirname

NULL

This variable is used to limit the effect of data import and export operations, such as those performed by
the LOAD DATA and SELECT ... INTO OUTFILE statements and the LOAD_FILE() function. These
operations are permitted only to users who have the FILE privilege.

secure_file_priv may be set as follows:

• If empty, the variable has no effect. This is not a secure setting.

• If set to the name of a directory, the server limits import and export operations to work only with files in

that directory. The directory must exist; the server does not create it.

• If set to NULL, the server disables import and export operations.

The default value is platform specific and depends on the value of the INSTALL_LAYOUT CMake option,
as shown in the following table. To specify the default secure_file_priv value explicitly if you are
building from source, use the INSTALL_SECURE_FILE_PRIVDIR CMake option.

INSTALL_LAYOUT Value

STANDALONE, WIN

DEB, RPM, SLES, SVR4

Otherwise

Default secure_file_priv Value

NULL (>= MySQL 5.7.16), empty (< MySQL 5.7.16)

/var/lib/mysql-files

mysql-files under the
CMAKE_INSTALL_PREFIX value

To set the default secure_file_priv value for the libmysqld embedded server, use the
INSTALL_SECURE_FILE_PRIV_EMBEDDEDDIR CMake option. The default value for this option is NULL.

The server checks the value of secure_file_priv at startup and writes a warning to the error log
if the value is insecure. A non-NULL value is considered insecure if it is empty, or the value is the data
directory or a subdirectory of it, or a directory that is accessible by all users. If secure_file_priv is
set to a nonexistent path, the server writes an error message to the error log and exits.

• session_track_gtids

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

852

--session-track-gtids=value

session_track_gtids

Global, Session

Yes

Enumeration

OFF

OFF

OWN_GTID

Server System Variables

ALL_GTIDS

Controls whether the server returns GTIDs to the client, enabling the client to use them to track the
server state. Depending on the variable value, at the end of executing each transaction, the server’s
GTIDs are captured and returned to the client as part of the acknowledgement. The possible values for
session_track_gtids are as follows:

• OFF: The server does not return GTIDs to the client. This is the default.

• OWN_GTID: The server returns the GTIDs for all transactions that were successfully committed by this
client in its current session since the last acknowledgement. Typically, this is the single GTID for the
last transaction committed, but if a single client request resulted in multiple transactions, the server
returns a GTID set containing all the relevant GTIDs.

• ALL_GTIDS: The server returns the global value of its gtid_executed system variable, which it

reads at a point after the transaction is successfully committed. As well as the GTID for the transaction
just committed, this GTID set includes all transactions committed on the server by any client, and can
include transactions committed after the point when the transaction currently being acknowledged was
committed.

session_track_gtids cannot be set within transactional context.

For more information about session state tracking, see Section 5.1.15, “Server Tracking of Client
Session State”.

• session_track_schema

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--session-track-schema[={OFF|ON}]

session_track_schema

Global, Session

Yes

Boolean

ON

Controls whether the server tracks when the default schema (database) is set within the current session
and notifies the client to make the schema name available.

If the schema name tracker is enabled, name notification occurs each time the default schema is set,
even if the new schema name is the same as the old.

For more information about session state tracking, see Section 5.1.15, “Server Tracking of Client
Session State”.

• session_track_state_change

Command-Line Format

--session-track-state-change[={OFF|
ON}]

System Variable

session_track_state_change

Scope

Dynamic

Type

Global, Session

Yes

Boolean

853

Server System Variables

Default Value

OFF

Controls whether the server tracks changes to the state of the current session and notifies the client
when state changes occur. Changes can be reported for these attributes of client session state:

• The default schema (database).

• Session-specific values for system variables.

• User-defined variables.

• Temporary tables.

• Prepared statements.

If the session state tracker is enabled, notification occurs for each change that involves tracked session
attributes, even if the new attribute values are the same as the old. For example, setting a user-defined
variable to its current value results in a notification.

The session_track_state_change variable controls only notification of when changes occur, not
what the changes are. For example, state-change notifications occur when the default schema is set or
tracked session system variables are assigned, but the notification does not include the schema name or
variable values. To receive notification of the schema name or session system variable values, use the
session_track_schema or session_track_system_variables system variable, respectively.

Note

Assigning a value to session_track_state_change itself is not considered a
state change and is not reported as such. However, if its name listed in the value
of session_track_system_variables, any assignments to it do result in
notification of the new value.

For more information about session state tracking, see Section 5.1.15, “Server Tracking of Client
Session State”.

• session_track_system_variables

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--session-track-system-variables=#

session_track_system_variables

Global, Session

Yes

String

time_zone, autocommit,
character_set_client,
character_set_results,
character_set_connection

Controls whether the server tracks assignments to session system variables and notifies the client of the
name and value of each assigned variable. The variable value is a comma-separated list of variables
for which to track assignments. By default, notification is enabled for time_zone, autocommit,

854

Server System Variables

character_set_client, character_set_results, and character_set_connection. (The
latter three variables are those affected by SET NAMES.)

The special value * causes the server to track assignments to all session variables. If given, this value
must be specified by itself without specific system variable names.

To disable notification of session variable assignments, set session_track_system_variables to
the empty string.

If session system variable tracking is enabled, notification occurs for all assignments to tracked session
variables, even if the new values are the same as the old.

For more information about session state tracking, see Section 5.1.15, “Server Tracking of Client
Session State”.

• session_track_transaction_info

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

--session-track-transaction-
info=value

session_track_transaction_info

Global, Session

Yes

Enumeration

OFF

OFF

STATE

CHARACTERISTICS

Controls whether the server tracks the state and characteristics of transactions within the current session
and notifies the client to make this information available. These session_track_transaction_info
values are permitted:

• OFF: Disable transaction state tracking. This is the default.

• STATE: Enable transaction state tracking without characteristics tracking. State tracking enables the
client to determine whether a transaction is in progress and whether it could be moved to a different
session without being rolled back.

• CHARACTERISTICS: Enable transaction state tracking, including characteristics tracking.

Characteristics tracking enables the client to determine how to restart a transaction in another session
so that it has the same characteristics as in the original session. The following characteristics are
relevant for this purpose:

ISOLATION LEVEL
READ ONLY
READ WRITE
WITH CONSISTENT SNAPSHOT

For a client to safely relocate a transaction to another session, it must track not only transaction state
but also transaction characteristics. In addition, the client must track the transaction_isolation

855

Server System Variables

and transaction_read_only system variables to correctly determine the session defaults. (To track
these variables, list them in the value of the session_track_system_variables system variable.)

For more information about session state tracking, see Section 5.1.15, “Server Tracking of Client
Session State”.

• sha256_password_auto_generate_rsa_keys

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--sha256-password-auto-generate-rsa-
keys[={OFF|ON}]

sha256_password_auto_generate_rsa_keys

Global

No

Boolean

ON

This variable is available if the server was compiled using OpenSSL (see Section 6.3.4, “SSL Library-
Dependent Capabilities”). It controls whether the server autogenerates RSA private/public key-pair files
in the data directory, if they do not already exist.

At startup, the server automatically generates RSA private/public key-pair files in the data directory if
the sha256_password_auto_generate_rsa_keys system variable is enabled, no RSA options
are specified, and the RSA files are missing from the data directory. These files enable secure
password exchange using RSA over unencrypted connections for accounts authenticated by the
sha256_password plugin; see Section 6.4.1.5, “SHA-256 Pluggable Authentication”.

For more information about RSA file autogeneration, including file names and characteristics, see
Section 6.3.3.1, “Creating SSL and RSA Certificates and Keys using MySQL”

The auto_generate_certs system variable is related but controls autogeneration of SSL certificate
and key files needed for secure connections using SSL.

• sha256_password_private_key_path

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--sha256-password-private-key-
path=file_name

sha256_password_private_key_path

Global

No

File name

private_key.pem

This variable is available if MySQL was compiled using OpenSSL (see Section 6.3.4, “SSL
Library-Dependent Capabilities”). Its value is the path name of the RSA private key file for the

856

Server System Variables

sha256_password authentication plugin. If the file is named as a relative path, it is interpreted relative
to the server data directory. The file must be in PEM format.

Important

Because this file stores a private key, its access mode should be restricted so
that only the MySQL server can read it.

For information about sha256_password, see Section 6.4.1.5, “SHA-256 Pluggable Authentication”.

• sha256_password_proxy_users

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--sha256-password-proxy-users[={OFF|
ON}]

sha256_password_proxy_users

Global

Yes

Boolean

OFF

This variable controls whether the sha256_password built-in authentication plugin supports proxy
users. It has no effect unless the check_proxy_users system variable is enabled. For information
about user proxying, see Section 6.2.14, “Proxy Users”.

• sha256_password_public_key_path

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--sha256-password-public-key-
path=file_name

sha256_password_public_key_path

Global

No

File name

public_key.pem

This variable is available if MySQL was compiled using OpenSSL (see Section 6.3.4, “SSL
Library-Dependent Capabilities”). Its value is the path name of the RSA public key file for the
sha256_password authentication plugin. If the file is named as a relative path, it is interpreted relative
to the server data directory. The file must be in PEM format. Because this file stores a public key, copies
can be freely distributed to client users. (Clients that explicitly specify a public key when connecting to
the server using RSA password encryption must use the same public key as that used by the server.)

For information about sha256_password, including information about how clients specify the RSA
public key, see Section 6.4.1.5, “SHA-256 Pluggable Authentication”.

• shared_memory

Command-Line Format

System Variable

Scope

Dynamic

--shared-memory[={OFF|ON}]

shared_memory

Global

No

857

Server System Variables

Platform Specific

Type

Default Value

Windows

Boolean

OFF

(Windows only.) Whether the server permits shared-memory connections.

• shared_memory_base_name

Command-Line Format

System Variable

Scope

Dynamic

Platform Specific

Type

Default Value

--shared-memory-base-name=name

shared_memory_base_name

Global

No

Windows

String

MYSQL

(Windows only.) The name of shared memory to use for shared-memory connections. This is useful
when running multiple MySQL instances on a single physical machine. The default name is MYSQL. The
name is case-sensitive.

This variable applies only if the server is started with the shared_memory system variable enabled to
support shared-memory connections.

• show_compatibility_56

Command-Line Format

--show-compatibility-56[={OFF|ON}]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Yes

show_compatibility_56

Global

Yes

Boolean

OFF

The INFORMATION_SCHEMA has tables that contain system and status variable information (see
Section 24.3.11, “The INFORMATION_SCHEMA GLOBAL_VARIABLES and SESSION_VARIABLES
Tables”, and Section 24.3.10, “The INFORMATION_SCHEMA GLOBAL_STATUS and
SESSION_STATUS Tables”). As of MySQL 5.7.6, the Performance Schema also contains system and
status variable tables (see Section 25.12.13, “Performance Schema System Variable Tables”, and
Section 25.12.14, “Performance Schema Status Variable Tables”). The Performance Schema tables are
intended to replace the INFORMATION_SCHEMA tables, which are deprecated as of MySQL 5.7.6 and
are removed in MySQL 8.0.

For advice on migrating away from the INFORMATION_SCHEMA tables to the Performance Schema
tables, see Section 25.20, “Migrating to Performance Schema System and Status Variable Tables”.
To assist in the migration, you can use the show_compatibility_56 system variable, which affects
whether MySQL 5.6 compatibility is enabled with respect to how system and status variable information

858

Server System Variables

is provided by the INFORMATION_SCHEMA and Performance Schema tables, and also by the SHOW
VARIABLES and SHOW STATUS statements.

Note

show_compatibility_56 is deprecated because its only purpose is to permit
control over deprecated system and status variable information sources which
you can expect to be removed in a future release of MySQL. When those sources
are removed, show_compatibility_56 no longer has any purpose, and you
can expect it be removed as well.

The following discussion describes the effects of show_compatibility_56:

• Overview of show_compatibility_56 Effects

• Effect of show_compatibility_56 on SHOW Statements

• Effect of show_compatibility_56 on INFORMATION_SCHEMA Tables

• Effect of show_compatibility_56 on Performance Schema Tables

• Effect of show_compatibility_56 on Slave Status Variables

• Effect of show_compatibility_56 on FLUSH STATUS

For better understanding, it is strongly recommended that you also read these sections:

• Section 25.12.13, “Performance Schema System Variable Tables”

• Section 25.12.14, “Performance Schema Status Variable Tables”

• Section 25.12.15.10, “Status Variable Summary Tables”

Overview of show_compatibility_56 Effects

The show_compatibility_56 system variable affects these aspects of server operation regarding
system and status variables:

• Information available from the SHOW VARIABLES and SHOW STATUS statements

• Information available from the INFORMATION_SCHEMA tables that provide system and status variable

information

• Information available from the Performance Schema tables that provide system and status variable

information

• The effect of the FLUSH STATUS statement on status variables

This list summarizes the effects of show_compatibility_56, with additional details given later:

• When show_compatibility_56 is ON, compatibility with MySQL 5.6 is enabled. Older variable

information sources (SHOW statements, INFORMATION_SCHEMA tables) produce the same output as in
MySQL 5.6.

• When show_compatibility_56 is OFF, compatibility with MySQL 5.6 is disabled. Selecting from
the INFORMATION_SCHEMA tables produces an error because the Performance Schema tables are

859

Server System Variables

intended to replace them. The INFORMATION_SCHEMA tables are deprecated as of MySQL 5.7.6 and
are removed in MySQL 8.0.

To obtain system and status variable information When show_compatibility_56=OFF, use the
Performance Schema tables or the SHOW statements.

Note

When show_compatibility_56=OFF, the SHOW VARIABLES and
SHOW STATUS statements display rows from the Performance Schema
global_variables, session_variables, global_status, and
session_status tables.

As of MySQL 5.7.9, those tables are world readable and accessible without the
SELECT privilege, which means that SELECT is not needed to use the SHOW
statements, either. Before MySQL 5.7.9, the SELECT privilege is required to
access those Performance Schema tables, either directly, or indirectly through
the SHOW statements.

• Several Slave_xxx status variables are available from SHOW STATUS when

show_compatibility_56 is ON. When show_compatibility_56 is OFF, some of those variables
are not exposed to SHOW STATUS. The information they provide is available in replication-related
Performance Schema tables, as described later.

• show_compatibility_56 has no effect on system variable access using @@ notation:

@@GLOBAL.var_name, @@SESSION.var_name, @@var_name.

• show_compatibility_56 has no effect for the embedded server, which produces 5.6-compatible

output in all cases.

The following descriptions detail the effect of setting show_compatibility_56 to ON or OFF in the
contexts in which this variable applies.

Effect of show_compatibility_56 on SHOW Statements

SHOW GLOBAL VARIABLES statement:

• ON: MySQL 5.6 output.

• OFF: Output displays rows from the Performance Schema global_variables table.

SHOW [SESSION | LOCAL] VARIABLES statement:

• ON: MySQL 5.6 output.

• OFF: Output displays rows from the Performance Schema session_variables table. (In MySQL
5.7.6 and 5.7.7, OFF output does not fully reflect all system variable values in effect for the current
session; it includes no rows for global variables that have no session counterpart. This is corrected in
MySQL 5.7.8.)

SHOW GLOBAL STATUS statement:

• ON: MySQL 5.6 output.

860

Server System Variables

• OFF: Output displays rows from the Performance Schema global_status table, plus the Com_xxx

statement execution counters.

OFF output includes no rows for session variables that have no global counterpart, unlike ON output.

SHOW [SESSION | LOCAL] STATUS statement:

• ON: MySQL 5.6 output.

• OFF: Output displays rows from the Performance Schema session_status table, plus the Com_xxx
statement execution counters. (In MySQL 5.7.6 and 5.7.7, OFF output does not fully reflect all status
variable values in effect for the current session; it includes no rows for global variables that have no
session counterpart. This is corrected in MySQL 5.7.8.)

In MySQL 5.7.6 and 5.7.7, for each of the SHOW statements just described, use of a WHERE
clause produces a warning when show_compatibility_56=ON and an error when
show_compatibility_56=OFF. (This applies to WHERE clauses that are not optimized away. For
example, WHERE 1 is trivially true, is optimized away, and thus produces no warning or error.) This
behavior does not occur as of MySQL 5.7.8; WHERE is supported as before 5.7.6.

Effect of show_compatibility_56 on INFORMATION_SCHEMA Tables

INFORMATION_SCHEMA tables (GLOBAL_VARIABLES, SESSION_VARIABLES, GLOBAL_STATUS, and
SESSION_STATUS):

• ON: MySQL 5.6 output, with a deprecation warning.

• OFF: Selecting from these tables produces an error. (Before 5.7.9, selecting from these tables

produces no output, with a deprecation warning.)

Effect of show_compatibility_56 on Performance Schema Tables

Performance Schema system variable tables:

• OFF:

• global_variables: Global system variables only.

• session_variables: System variables in effect for the current session: A row for each session

variable, and a row for each global variable that has no session counterpart.

• variables_by_thread: Session system variables only, for each active session.

861

Server System Variables

• ON: Same output as for OFF. (Before 5.7.8, these tables produce no output.)

Performance Schema status variable tables:

• OFF:

• global_status: Global status variables only.

• session_status: Status variables in effect the current session: A row for each session variable,

and a row for each global variable that has no session counterpart.

• status_by_account Session status variables only, aggregated per account.

• status_by_host: Session status variables only, aggregated per host name.

• status_by_thread: Session status variables only, for each active session.

• status_by_user: Session status variables only, aggregated per user name.

The Performance Schema does not collect statistics for Com_xxx status variables
in the status variable tables. To obtain global and per-session statement execution
counts, use the events_statements_summary_global_by_event_name and
events_statements_summary_by_thread_by_event_name tables, respectively.

• ON: Same output as for OFF. (Before 5.7.9, these tables produce no output.)

Effect of show_compatibility_56 on Slave Status Variables

Replica status variables:

• ON: Several Slave_xxx status variables are available from SHOW STATUS.

• OFF: Some of those replica variables are not exposed to SHOW STATUS or the Performance Schema
status variable tables. The information they provide is available in replication-related Performance
Schema tables. The following table shows which Slave_xxx status variables become unavailable in
SHOW STATUS and their locations in Performance Schema replication tables.

Status Variable

Slave_heartbeat_period

Slave_last_heartbeat

Slave_received_heartbeats

Slave_retried_transactions

Performance Schema Location

replication_connection_configuration
table, HEARTBEAT_INTERVAL column

replication_connection_status table,
LAST_HEARTBEAT_TIMESTAMP column

replication_connection_status table,
COUNT_RECEIVED_HEARTBEATS column

replication_applier_status table,
COUNT_TRANSACTIONS_RETRIES column

862

Server System Variables

Status Variable

Slave_running

Performance Schema Location

replication_connection_status and
replication_applier_status tables,
SERVICE_STATE column

Effect of show_compatibility_56 on FLUSH STATUS

FLUSH STATUS statement:

• ON: This statement produces MySQL 5.6 behavior. It adds the current thread's session status variable

values to the global values and resets the session values to zero. Some global variables may be
reset to zero as well. It also resets the counters for key caches (default and named) to zero and sets
Max_used_connections to the current number of open connections.

• OFF: This statement adds the session status from all active sessions to the global status variables,

resets the status of all active sessions, and resets account, host, and user status values aggregated
from disconnected sessions.

• show_create_table_verbosity

Command-Line Format

Introduced

System Variable

Scope

Dynamic

Type

Default Value

--show-create-table-verbosity[={OFF|
ON}]

5.7.22

show_create_table_verbosity

Global, Session

Yes

Boolean

OFF

SHOW CREATE TABLE normally does not show the ROW_FORMAT table option if the row format is the
default format. Enabling this variable causes SHOW CREATE TABLE to display ROW_FORMAT regardless
of whether it is the default format.

• show_old_temporals

Command-Line Format

--show-old-temporals[={OFF|ON}]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Yes

show_old_temporals

Global, Session

Yes

Boolean

OFF

Whether SHOW CREATE TABLE output includes comments to flag temporal columns found to be in
pre-5.6.4 format (TIME, DATETIME, and TIMESTAMP columns without support for fractional seconds
precision). This variable is disabled by default. If enabled, SHOW CREATE TABLE output looks like this:

CREATE TABLE `mytbl` (
  `ts` timestamp /* 5.5 binary format */ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dt` datetime /* 5.5 binary format */ DEFAULT NULL,

863

Server System Variables

  `t` time /* 5.5 binary format */ DEFAULT NULL
) DEFAULT CHARSET=latin1

Output for the COLUMN_TYPE column of the Information Schema COLUMNS table is affected similarly.

This variable is deprecated; expect it to be removed in a future release of MySQL.

• skip_external_locking

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--skip-external-locking[={OFF|ON}]

skip_external_locking

Global

No

Boolean

ON

This is OFF if mysqld uses external locking (system locking), ON if external locking is disabled. This
affects only MyISAM table access.

This variable is set by the --external-locking or --skip-external-locking option. External
locking is disabled by default.

External locking affects only MyISAM table access. For more information, including conditions under
which it can and cannot be used, see Section 8.11.5, “External Locking”.

• skip_name_resolve

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--skip-name-resolve[={OFF|ON}]

skip_name_resolve

Global

No

Boolean

OFF

Whether to resolve host names when checking client connections. If this variable is OFF, mysqld
resolves host names when checking client connections. If it is ON, mysqld uses only IP numbers; in
this case, all Host column values in the grant tables must be IP addresses. See Section 5.1.11.2, “DNS
Lookups and the Host Cache”.

Depending on the network configuration of your system and the Host values for your accounts, clients
may need to connect using an explicit --host option, such as --host=127.0.0.1 or --host=::1.

An attempt to connect to the host 127.0.0.1 normally resolves to the localhost account. However,
this fails if the server is run with skip_name_resolve enabled. If you plan to do that, make sure an
account exists that can accept a connection. For example, to be able to connect as root using --
host=127.0.0.1 or --host=::1, create these accounts:

CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY 'root-password';
CREATE USER 'root'@'::1' IDENTIFIED BY 'root-password';

864

Server System Variables

• skip_networking

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--skip-networking[={OFF|ON}]

skip_networking

Global

No

Boolean

OFF

This variable controls whether the server permits TCP/IP connections. By default, it is disabled (permit
TCP connections). If enabled, the server permits only local (non-TCP/IP) connections and all interaction
with mysqld must be made using named pipes or shared memory (on Windows) or Unix socket files
(on Unix). This option is highly recommended for systems where only local clients are permitted. See
Section 5.1.11.2, “DNS Lookups and the Host Cache”.

• skip_show_database

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--skip-show-database

skip_show_database

Global

No

Boolean

OFF

This prevents people from using the SHOW DATABASES statement if they do not have the SHOW
DATABASES privilege. This can improve security if you have concerns about users being able to see
databases belonging to other users. Its effect depends on the SHOW DATABASES privilege: If the
variable value is ON, the SHOW DATABASES statement is permitted only to users who have the SHOW
DATABASES privilege, and the statement displays all database names. If the value is OFF, SHOW
DATABASES is permitted to all users, but displays the names of only those databases for which the user
has the SHOW DATABASES or other privilege.

Caution

Because a global privilege is considered a privilege for all databases, any global
privilege enables a user to see all database names with SHOW DATABASES or by
examining the INFORMATION_SCHEMA SCHEMATA table.

• slow_launch_time

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--slow-launch-time=#

slow_launch_time

Global

Yes

Integer

2

0

31536000

865

Server System Variables

Unit

seconds

If creating a thread takes longer than this many seconds, the server increments the
Slow_launch_threads status variable.

• slow_query_log

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--slow-query-log[={OFF|ON}]

slow_query_log

Global

Yes

Boolean

OFF

Whether the slow query log is enabled. The value can be 0 (or OFF) to disable the log or 1 (or ON) to
enable the log. The destination for log output is controlled by the log_output system variable; if that
value is NONE, no log entries are written even if the log is enabled.

“Slow” is determined by the value of the long_query_time variable. See Section 5.4.5, “The Slow
Query Log”.

• slow_query_log_file

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--slow-query-log-file=file_name

slow_query_log_file

Global

Yes

File name

host_name-slow.log

The name of the slow query log file. The default value is host_name-slow.log, but the initial value
can be changed with the --slow_query_log_file option.

• socket

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (Windows)

Default Value (Other)

--socket={file_name|pipe_name}

socket

Global

No

String

MySQL

/tmp/mysql.sock

On Unix platforms, this variable is the name of the socket file that is used for local client connections.
The default is /tmp/mysql.sock. (For some distribution formats, the directory might be different, such
as /var/lib/mysql for RPMs.)

On Windows, this variable is the name of the named pipe that is used for local client connections. The
default value is MySQL (not case-sensitive).

866

Server System Variables

• sort_buffer_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

--sort-buffer-size=#

sort_buffer_size

Global, Session

Yes

Integer

262144

32768

Maximum Value (Windows)

4294967295

Maximum Value (Other, 64-bit platforms)

18446744073709551615

Maximum Value (Other, 32-bit platforms)

4294967295

Unit

bytes

Each session that must perform a sort allocates a buffer of this size. sort_buffer_size is not
specific to any storage engine and applies in a general manner for optimization. At minimum the
sort_buffer_size value must be large enough to accommodate fifteen tuples in the sort buffer. Also,
increasing the value of max_sort_length may require increasing the value of sort_buffer_size.
For more information, see Section 8.2.1.14, “ORDER BY Optimization”

If you see many Sort_merge_passes per second in SHOW GLOBAL STATUS output, you can consider
increasing the sort_buffer_size value to speed up ORDER BY or GROUP BY operations that cannot
be improved with query optimization or improved indexing.

The optimizer tries to work out how much space is needed but can allocate more, up to the limit. Setting
it larger than required globally slows down most queries that sort. It is best to increase it as a session
setting, and only for the sessions that need a larger size. On Linux, there are thresholds of 256KB and
2MB where larger values may significantly slow down memory allocation, so you should consider staying
below one of those values. Experiment to find the best value for your workload. See Section B.3.3.5,
“Where MySQL Stores Temporary Files”.

The maximum permissible setting for sort_buffer_size is 4GB−1. Larger values are permitted for
64-bit platforms (except 64-bit Windows, for which large values are truncated to 4GB−1 with a warning).

• sql_auto_is_null

System Variable

Scope

Dynamic

Type

Default Value

sql_auto_is_null

Global, Session

Yes

Boolean

OFF

If this variable is enabled, then after a statement that successfully inserts an automatically generated
AUTO_INCREMENT value, you can find that value by issuing a statement of the following form:

SELECT * FROM tbl_name WHERE auto_col IS NULL

If the statement returns a row, the value returned is the same as if you invoked the LAST_INSERT_ID()
function. For details, including the return value after a multiple-row insert, see Section 12.15,

867

Server System Variables

“Information Functions”. If no AUTO_INCREMENT value was successfully inserted, the SELECT statement
returns no row.

The behavior of retrieving an AUTO_INCREMENT value by using an IS NULL comparison is used by
some ODBC programs, such as Access. See Obtaining Auto-Increment Values. This behavior can be
disabled by setting sql_auto_is_null to OFF.

The default value of sql_auto_is_null is OFF.

• sql_big_selects

System Variable

Scope

Dynamic

Type

Default Value

sql_big_selects

Global, Session

Yes

Boolean

ON

If set to OFF, MySQL aborts SELECT statements that are likely to take a very long time to execute (that
is, statements for which the optimizer estimates that the number of examined rows exceeds the value of
max_join_size). This is useful when an inadvisable WHERE statement has been issued. The default
value for a new connection is ON, which permits all SELECT statements.

If you set the max_join_size system variable to a value other than DEFAULT, sql_big_selects is
set to OFF.

• sql_buffer_result

System Variable

Scope

Dynamic

Type

Default Value

sql_buffer_result

Global, Session

Yes

Boolean

OFF

If enabled, sql_buffer_result forces results from SELECT statements to be put into temporary
tables. This helps MySQL free the table locks early and can be beneficial in cases where it takes a long
time to send results to the client. The default value is OFF.

• sql_log_off

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

sql_log_off

Global, Session

Yes

Boolean

OFF

OFF (enable logging)

ON (disable logging)

868

This variable controls whether logging to the general query log is disabled for the current session
(assuming that the general query log itself is enabled). The default value is OFF (that is, enable logging).

Server System Variables

To disable or enable general query logging for the current session, set the session sql_log_off
variable to ON or OFF.

Setting the session value of this system variable is a restricted operation. The session user must have
privileges sufficient to set restricted session variables. See Section 5.1.8.1, “System Variable Privileges”.

• sql_mode

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

--sql-mode=name

sql_mode

Global, Session

Yes

Set

ONLY_FULL_GROUP_BY
STRICT_TRANS_TABLES
NO_ZERO_IN_DATE NO_ZERO_DATE
ERROR_FOR_DIVISION_BY_ZERO
NO_AUTO_CREATE_USER
NO_ENGINE_SUBSTITUTION

ALLOW_INVALID_DATES

ANSI_QUOTES

ERROR_FOR_DIVISION_BY_ZERO

HIGH_NOT_PRECEDENCE

IGNORE_SPACE

NO_AUTO_CREATE_USER

NO_AUTO_VALUE_ON_ZERO

NO_BACKSLASH_ESCAPES

NO_DIR_IN_CREATE

NO_ENGINE_SUBSTITUTION

NO_FIELD_OPTIONS

NO_KEY_OPTIONS

NO_TABLE_OPTIONS

NO_UNSIGNED_SUBTRACTION

NO_ZERO_DATE

NO_ZERO_IN_DATE

ONLY_FULL_GROUP_BY

PAD_CHAR_TO_FULL_LENGTH

869

Server System Variables

PIPES_AS_CONCAT

REAL_AS_FLOAT

STRICT_ALL_TABLES

STRICT_TRANS_TABLES

The current server SQL mode, which can be set dynamically. For details, see Section 5.1.10, “Server
SQL Modes”.

Note

MySQL installation programs may configure the SQL mode during the installation
process. If the SQL mode differs from the default or from what you expect, check
for a setting in an option file that the server reads at startup.

• sql_notes

System Variable

Scope

Dynamic

Type

Default Value

sql_notes

Global, Session

Yes

Boolean

ON

If enabled (the default), diagnostics of Note level increment warning_count and the server records
them. If disabled, Note diagnostics do not increment warning_count and the server does not record
them. mysqldump includes output to disable this variable so that reloading the dump file does not
produce warnings for events that do not affect the integrity of the reload operation.

• sql_quote_show_create

System Variable

Scope

Dynamic

Type

Default Value

sql_quote_show_create

Global, Session

Yes

Boolean

ON

If enabled (the default), the server quotes identifiers for SHOW CREATE TABLE and SHOW CREATE
DATABASE statements. If disabled, quoting is disabled. This option is enabled by default so that
replication works for identifiers that require quoting. See Section 13.7.5.10, “SHOW CREATE TABLE
Statement”, and Section 13.7.5.6, “SHOW CREATE DATABASE Statement”.

• sql_safe_updates

System Variable

Scope

Dynamic

Type

Default Value

870

sql_safe_updates

Global, Session

Yes

Boolean

OFF

Server System Variables

If this variable is enabled, UPDATE and DELETE statements that do not use a key in the WHERE clause
or a LIMIT clause produce an error. This makes it possible to catch UPDATE and DELETE statements
where keys are not used properly and that would probably change or delete a large number of rows. The
default value is OFF.

For the mysql client, sql_safe_updates can be enabled by using the --safe-updates option. For
more information, see Using Safe-Updates Mode (--safe-updates).

• sql_select_limit

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

sql_select_limit

Global, Session

Yes

Integer

18446744073709551615

0

18446744073709551615

The maximum number of rows to return from SELECT statements. For more information, see Using Safe-
Updates Mode (--safe-updates).

The default value for a new connection is the maximum number of rows that the server permits per table.
Typical default values are (232)−1 or (264)−1. If you have changed the limit, the default value can be
restored by assigning a value of DEFAULT.

If a SELECT has a LIMIT clause, the LIMIT takes precedence over the value of sql_select_limit.

• sql_warnings

System Variable

Scope

Dynamic

Type

Default Value

sql_warnings

Global, Session

Yes

Boolean

OFF

This variable controls whether single-row INSERT statements produce an information string if warnings
occur. The default is OFF. Set the value to ON to produce an information string.

• ssl_ca

Command-Line Format

System Variable

Scope

Dynamic

Type

--ssl-ca=file_name

ssl_ca

Global

No

File name

871

Server System Variables

Default Value

NULL

The path name of the Certificate Authority (CA) certificate file in PEM format. The file contains a list of
trusted SSL Certificate Authorities.

• ssl_capath

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--ssl-capath=dir_name

ssl_capath

Global

No

Directory name

NULL

The path name of the directory that contains trusted SSL Certificate Authority (CA) certificate files in
PEM format. You must run OpenSSL rehash on the directory specified by this option prior to using it.
On Linux systems, you can invoke rehash like this:

$> openssl rehash path/to/directory

On Windows platforms, you can use the c_rehash script in a command prompt, like this:

\> c_rehash path/to/directory

See openssl-rehash for complete syntax and other information.

Support for this capability depends on the SSL library used to compile MySQL; see Section 6.3.4, “SSL
Library-Dependent Capabilities”.

• ssl_cert

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--ssl-cert=file_name

ssl_cert

Global

No

File name

NULL

The path name of the server SSL public key certificate file in PEM format.

If the server is started with ssl_cert set to a certificate that uses any restricted cipher or cipher
category, the server starts with support for encrypted connections disabled. For information about cipher
restrictions, see Connection Cipher Configuration.

• ssl_cipher

Command-Line Format

System Variable

872

Scope

Dynamic

--ssl-cipher=name

ssl_cipher

Global

No

Server System Variables

Type

Default Value

String

NULL

The list of permissible ciphers for connection encryption. If no cipher in the list is supported, encrypted
connections do not work.

For greatest portability, the cipher list should be a list of one or more cipher names, separated by colons.
This format is understood both by OpenSSL and yaSSL. The following example shows two cipher names
separated by a colon:

[mysqld]
ssl_cipher="DHE-RSA-AES128-GCM-SHA256:AES128-SHA"

OpenSSL supports a more flexible syntax for specifying ciphers, as described in the OpenSSL
documentation at https://www.openssl.org/docs/manmaster/man1/openssl-ciphers.html. yaSSL does not,
so attempts to use that extended syntax fail for a MySQL distribution compiled using yaSSL.

For information about which encryption ciphers MySQL supports, see Section 6.3.2, “Encrypted
Connection TLS Protocols and Ciphers”.

• ssl_crl

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--ssl-crl=file_name

ssl_crl

Global

No

File name

NULL

The path name of the file containing certificate revocation lists in PEM format. Support for revocation-
list capability depends on the SSL library used to compile MySQL. See Section 6.3.4, “SSL Library-
Dependent Capabilities”.

• ssl_crlpath

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--ssl-crlpath=dir_name

ssl_crlpath

Global

No

Directory name

NULL

The path of the directory that contains certificate revocation-list files in PEM format. Support for
revocation-list capability depends on the SSL library used to compile MySQL. See Section 6.3.4, “SSL
Library-Dependent Capabilities”.

• ssl_key

Command-Line Format

System Variable

--ssl-key=file_name

ssl_key

873

Scope

Dynamic

Type

Default Value

Server System Variables

Global

No

File name

NULL

The path name of the server SSL private key file in PEM format. For better security, use a certificate with
an RSA key size of at least 2048 bits.

If the key file is protected by a passphrase, the server prompts the user for the passphrase. The
password must be given interactively; it cannot be stored in a file. If the passphrase is incorrect, the
program continues as if it could not read the key.

• stored_program_cache

Command-Line Format

System Variable

--stored-program-cache=#

stored_program_cache

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

256

16

524288

Sets a soft upper limit for the number of cached stored routines per connection. The value of this
variable is specified in terms of the number of stored routines held in each of the two caches maintained
by the MySQL Server for, respectively, stored procedures and stored functions.

Whenever a stored routine is executed this cache size is checked before the first or top-level statement
in the routine is parsed; if the number of routines of the same type (stored procedures or stored functions
according to which is being executed) exceeds the limit specified by this variable, the corresponding
cache is flushed and memory previously allocated for cached objects is freed. This allows the cache to
be flushed safely, even when there are dependencies between stored routines.

• super_read_only

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--super-read-only[={OFF|ON}]

super_read_only

Global

Yes

Boolean

OFF

If the read_only system variable is enabled, the server permits no client updates except from users
who have the SUPER privilege. If the super_read_only system variable is also enabled, the server
prohibits client updates even from users who have SUPER. See the description of the read_only

874

Server System Variables

system variable for a description of read-only mode and information about how read_only and
super_read_only interact.

Client updates prevented when super_read_only is enabled include operations that do not
necessarily appear to be updates, such as CREATE FUNCTION (to install a loadable function) and
INSTALL PLUGIN. These operations are prohibited because they involve changes to tables in the
mysql system database.

Changes to super_read_only on a replication source server are not replicated to replica servers. The
value can be set on a replica independent of the setting on the source.

• sync_frm

Command-Line Format

--sync-frm[={OFF|ON}]

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Yes

sync_frm

Global

Yes

Boolean

ON

If this variable is set to 1, when any nontemporary table is created its .frm file is synchronized to disk
(using fdatasync()). This is slower but safer in case of a crash. The default is 1.

This variable is deprecated in MySQL 5.7 and is removed in MySQL 8.0 (when .frm files become
obsolete).

• system_time_zone

System Variable

system_time_zone

Scope

Dynamic

Type

Global

No

String

The server system time zone. When the server begins executing, it inherits a time zone setting from the
machine defaults, possibly modified by the environment of the account used for running the server or the
startup script. The value is used to set system_time_zone. To explicitly specify the system time zone,
set the TZ environment variable or use the --timezone option of the mysqld_safe script.

The system_time_zone variable differs from the time_zone variable. Although they might have
the same value, the latter variable is used to initialize the time zone for each client that connects. See
Section 5.1.13, “MySQL Server Time Zone Support”.

• table_definition_cache

Command-Line Format

System Variable

Scope

Dynamic

Type

--table-definition-cache=#

table_definition_cache

Global

Yes

Integer

875

Server System Variables

Default Value

Minimum Value

Maximum Value

-1 (signifies autosizing; do not assign this literal
value)

400

524288

The number of table definitions (from .frm files) that can be stored in the table definition cache. If you
use a large number of tables, you can create a large table definition cache to speed up opening of
tables. The table definition cache takes less space and does not use file descriptors, unlike the normal
table cache. The minimum value is 400. The default value is based on the following formula, capped to a
limit of 2000:

400 + (table_open_cache / 2)

For InnoDB, the table_definition_cache setting acts as a soft limit for the number of table
instances in the InnoDB data dictionary cache and the number file-per-table tablespaces that can be
open at one time.

If the number of table instances in the InnoDB data dictionary cache exceeds the
table_definition_cache limit, an LRU mechanism begins marking table instances for eviction
and eventually removes them from the InnoDB data dictionary cache. The number of open tables with
cached metadata can be higher than the table_definition_cache limit due to table instances with
foreign key relationships, which are not placed on the LRU list.

The number of file-per-table tablespaces that can be open at one time is limited by both the
table_definition_cache and innodb_open_files settings. If both variables are set, the
highest setting is used. If neither variable is set, the table_definition_cache setting, which
has a higher default value, is used. If the number of open tablespaces exceeds the limit defined by
table_definition_cache or innodb_open_files, an LRU mechanism searches the LRU list for
tablespace files that are fully flushed and not currently being extended. This process is performed each
time a new tablespace is opened. Only inactive tablespaces are closed.

• table_open_cache

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--table-open-cache=#

table_open_cache

Global

Yes

Integer

2000

1

524288

The number of open tables for all threads. Increasing this value increases the number of file descriptors
that mysqld requires. The effective value of this variable is the greater of the effective value of
open_files_limit - 10 - the effective value of max_connections / 2, and 400; that is

MAX(
    (open_files_limit - 10 - max_connections) / 2,
    400

876

Server System Variables

   )

You can check whether you need to increase the table cache by checking the Opened_tables
status variable. If the value of Opened_tables is large and you do not use FLUSH TABLES often
(which just forces all tables to be closed and reopened), then you should increase the value of the
table_open_cache variable. For more information about the table cache, see Section 8.4.3.1, “How
MySQL Opens and Closes Tables”.

• table_open_cache_instances

Command-Line Format

System Variable

--table-open-cache-instances=#

table_open_cache_instances

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

No

Integer

16

1

64

The number of open tables cache instances. To improve scalability by reducing contention among
sessions, the open tables cache can be partitioned into several smaller cache instances of size
table_open_cache / table_open_cache_instances . A session needs to lock only one instance
to access it for DML statements. This segments cache access among instances, permitting higher
performance for operations that use the cache when there are many sessions accessing tables. (DDL
statements still require a lock on the entire cache, but such statements are much less frequent than DML
statements.)

A value of 8 or 16 is recommended on systems that routinely use 16 or more cores. However, if
you have many large triggers on your tables that cause a high memory load, the default setting for
table_open_cache_instances might lead to excessive memory usage. In that situation, it can be
helpful to set table_open_cache_instances to 1 in order to restrict memory usage.

• thread_cache_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--thread-cache-size=#

thread_cache_size

Global

Yes

Integer

-1 (signifies autosizing; do not assign this literal
value)

0

16384

How many threads the server should cache for reuse. When a client disconnects, the client's threads
are put in the cache if there are fewer than thread_cache_size threads there. Requests for threads
are satisfied by reusing threads taken from the cache if possible, and only when the cache is empty is
a new thread created. This variable can be increased to improve performance if you have a lot of new
connections. Normally, this does not provide a notable performance improvement if you have a good

877

Server System Variables

thread implementation. However, if your server sees hundreds of connections per second you should
normally set thread_cache_size high enough so that most new connections use cached threads. By
examining the difference between the Connections and Threads_created status variables, you can
see how efficient the thread cache is. For details, see Section 5.1.9, “Server Status Variables”.

The default value is based on the following formula, capped to a limit of 100:

8 + (max_connections / 100)

This variable has no effect for the embedded server (libmysqld) and as of MySQL 5.7.2 is no longer
visible within the embedded server.

• thread_handling

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

--thread-handling=name

thread_handling

Global

No

Enumeration

one-thread-per-connection

no-threads

one-thread-per-connection

loaded-dynamically

The thread-handling model used by the server for connection threads. The permissible values are no-
threads (the server uses a single thread to handle one connection), one-thread-per-connection
(the server uses one thread to handle each client connection), and loaded-dynamically (set by the
thread pool plugin when it initializes). no-threads is useful for debugging under Linux; see Section 5.8,
“Debugging MySQL”.

This variable has no effect for the embedded server (libmysqld) and as of MySQL 5.7.2 is no longer
visible within the embedded server.

• thread_pool_algorithm

Command-Line Format

System Variable

--thread-pool-algorithm=#

thread_pool_algorithm

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

No

Integer

0

0

1

This variable controls which algorithm the thread pool plugin uses:

• A value of 0 (the default) uses a conservative low-concurrency algorithm which is most well tested and

is known to produce very good results.

878

Server System Variables

• A value of 1 increases the concurrency and uses a more aggressive algorithm which at times has

been known to perform 5–10% better on optimal thread counts, but has degrading performance as the
number of connections increases. Its use should be considered as experimental and not supported.

This variable is available only if the thread pool plugin is enabled. See Section 5.5.3, “MySQL Enterprise
Thread Pool”.

• thread_pool_high_priority_connection

Command-Line Format

--thread-pool-high-priority-
connection=#

System Variable

thread_pool_high_priority_connection

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global, Session

Yes

Integer

0

0

1

This variable affects queuing of new statements prior to execution. If the value is 0 (false, the default),
statement queuing uses both the low-priority and high-priority queues. If the value is 1 (true), queued
statements always go to the high-priority queue.

This variable is available only if the thread pool plugin is enabled. See Section 5.5.3, “MySQL Enterprise
Thread Pool”.

• thread_pool_max_unused_threads

Command-Line Format

System Variable

--thread-pool-max-unused-threads=#

thread_pool_max_unused_threads

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Global

Yes

Integer

0

0

4096

The maximum permitted number of unused threads in the thread pool. This variable makes it possible to
limit the amount of memory used by sleeping threads.

A value of 0 (the default) means no limit on the number of sleeping threads. A value of N where N is
greater than 0 means 1 consumer thread and N−1 reserve threads. In this case, if a thread is ready to
sleep but the number of sleeping threads is already at the maximum, the thread exits rather than going
to sleep.

A sleeping thread is either sleeping as a consumer thread or a reserve thread. The thread pool permits
one thread to be the consumer thread when sleeping. If a thread goes to sleep and there is no existing
consumer thread, it sleeps as a consumer thread. When a thread must be woken up, a consumer thread

879

Server System Variables

is selected if there is one. A reserve thread is selected only when there is no consumer thread to wake
up.

This variable is available only if the thread pool plugin is enabled. See Section 5.5.3, “MySQL Enterprise
Thread Pool”.

• thread_pool_prio_kickup_timer

Command-Line Format

System Variable

--thread-pool-prio-kickup-timer=#

thread_pool_prio_kickup_timer

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Global

Yes

Integer

1000

0

4294967294

milliseconds

This variable affects statements waiting for execution in the low-priority queue. The value is the number
of milliseconds before a waiting statement is moved to the high-priority queue. The default is 1000 (1
second).

This variable is available only if the thread pool plugin is enabled. See Section 5.5.3, “MySQL Enterprise
Thread Pool”.

• thread_pool_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

--thread-pool-size=#

thread_pool_size

Global

No

Integer

16

1

64

The number of thread groups in the thread pool. This is the most important parameter controlling thread
pool performance. It affects how many statements can execute simultaneously. If a value outside the
range of permissible values is specified, the thread pool plugin does not load and the server writes a
message to the error log.

This variable is available only if the thread pool plugin is enabled. See Section 5.5.3, “MySQL Enterprise
Thread Pool”.

• thread_pool_stall_limit

Command-Line Format

System Variable

880

--thread-pool-stall-limit=#

thread_pool_stall_limit

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Server System Variables

Global

Yes

Integer

6

4

600

milliseconds * 10

This variable affects executing statements. The value is the amount of time a statement has to finish
after starting to execute before it becomes defined as stalled, at which point the thread pool permits the
thread group to begin executing another statement. The value is measured in 10 millisecond units, so
the default of 6 means 60ms. Short wait values permit threads to start more quickly. Short values are
also better for avoiding deadlock situations. Long wait values are useful for workloads that include long-
running statements, to avoid starting too many new statements while the current ones execute.

This variable is available only if the thread pool plugin is enabled. See Section 5.5.3, “MySQL Enterprise
Thread Pool”.

• thread_stack

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value (64-bit platforms)

Default Value (32-bit platforms)

Minimum Value

--thread-stack=#

thread_stack

Global

No

Integer

262144

196608

131072

Maximum Value (64-bit platforms)

18446744073709550592

Maximum Value (32-bit platforms)

4294966272

Unit

Block Size

bytes

1024

The stack size for each thread. The default is large enough for normal operation. If the thread stack
size is too small, it limits the complexity of the SQL statements that the server can handle, the recursion
depth of stored procedures, and other memory-consuming actions.

• time_format

This variable is unused. It is deprecated and is removed in MySQL 8.0.

• time_zone

System Variable

Scope

Dynamic

Type

time_zone

Global, Session

Yes

String

881

Server System Variables

Default Value

Minimum Value

Maximum Value

SYSTEM

-12:59

+13:00

The current time zone. This variable is used to initialize the time zone for each client that connects. By
default, the initial value of this is 'SYSTEM' (which means, “use the value of system_time_zone”).
The value can be specified explicitly at server startup with the --default-time-zone option. See
Section 5.1.13, “MySQL Server Time Zone Support”.

Note

If set to SYSTEM, every MySQL function call that requires a time zone calculation
makes a system library call to determine the current system time zone. This call
may be protected by a global mutex, resulting in contention.

• timestamp

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

timestamp

Session

Yes

Numeric

UNIX_TIMESTAMP()

1

2147483647

Set the time for this client. This is used to get the original timestamp if you use the binary log to
restore rows. timestamp_value should be a Unix epoch timestamp (a value like that returned by
UNIX_TIMESTAMP(), not a value in 'YYYY-MM-DD hh:mm:ss' format) or DEFAULT.

Setting timestamp to a constant value causes it to retain that value until it is changed again. Setting
timestamp to DEFAULT causes its value to be the current date and time as of the time it is accessed.
The maximum value corresponds to '2038-01-19 03:14:07' UTC, the same as for the TIMESTAMP
data type.

timestamp is a DOUBLE rather than BIGINT because its value includes a microseconds part.

SET timestamp affects the value returned by NOW() but not by SYSDATE(). This means that
timestamp settings in the binary log have no effect on invocations of SYSDATE(). The server can be
started with the --sysdate-is-now option to cause SYSDATE() to be a synonym for NOW(), in which
case SET timestamp affects both functions.

• tls_version

Command-Line Format

--tls-version=protocol_list

Introduced

System Variable

Scope

Dynamic

Type

882

5.7.10

tls_version

Global

No

String

Server System Variables

Default Value (≥ 5.7.28)
Default Value (≤ 5.7.27)

TLSv1,TLSv1.1,TLSv1.2

TLSv1,TLSv1.1,TLSv1.2 (OpenSSL)

TLSv1,TLSv1.1 (yaSSL)

Which protocols the server permits for encrypted connections. The value is a comma-separated list
containing one or more protocol versions. The protocols that can be named for this variable depend
on the SSL library used to compile MySQL. Permitted protocols should be chosen such as not to leave
“holes” in the list. For details, see Section 6.3.2, “Encrypted Connection TLS Protocols and Ciphers”.

Note

As of MySQL 5.7.35, the TLSv1 and TLSv1.1 connection protocols are
deprecated and support for them is subject to removal in a future version of
MySQL. See Deprecated TLS Protocols.

Setting this variable to an empty string disables encrypted connections.

• tmp_table_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

--tmp-table-size=#

tmp_table_size

Global, Session

Yes

Integer

16777216

1024

18446744073709551615

bytes

The maximum size of internal in-memory temporary tables. This variable does not apply to user-created
MEMORY tables.

The actual limit is the smaller of tmp_table_size and max_heap_table_size. When an in-memory
temporary table exceeds the limit, MySQL automatically converts it to an on-disk temporary table.
The internal_tmp_disk_storage_engine option defines the storage engine used for on-disk
temporary tables.

Increase the value of tmp_table_size (and max_heap_table_size if necessary) if you do many
advanced GROUP BY queries and you have lots of memory.

You can compare the number of internal on-disk temporary tables created to the total number of internal
temporary tables created by comparing Created_tmp_disk_tables and Created_tmp_tables
values.

See also Section 8.4.4, “Internal Temporary Table Use in MySQL”.

• tmpdir

Command-Line Format

System Variable

--tmpdir=dir_name

tmpdir

883

Server System Variables

Scope

Dynamic

Type

Global

No

Directory name

The path of the directory to use for creating temporary files. It might be useful if your default /tmp
directory resides on a partition that is too small to hold temporary tables. This variable can be set to a list
of several paths that are used in round-robin fashion. Paths should be separated by colon characters (:)
on Unix and semicolon characters (;) on Windows.

tmpdir can be a non-permanent location, such as a directory on a memory-based file system or a
directory that is cleared when the server host restarts. If the MySQL server is acting as a replica, and
you are using a non-permanent location for tmpdir, consider setting a different temporary directory for
the replica using the slave_load_tmpdir variable. For a replica, the temporary files used to replicate
LOAD DATA statements are stored in this directory, so with a permanent location they can survive
machine restarts, although replication can now continue after a restart if the temporary files have been
removed.

For more information about the storage location of temporary files, see Section B.3.3.5, “Where MySQL
Stores Temporary Files”.

• transaction_alloc_block_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Block Size

--transaction-alloc-block-size=#

transaction_alloc_block_size

Global, Session

Yes

Integer

8192

1024

131072

bytes

1024

The amount in bytes by which to increase a per-transaction memory pool which needs memory. See the
description of transaction_prealloc_size.

• transaction_isolation

Command-Line Format

System Variable (≥ 5.7.20)
Scope (≥ 5.7.20)
Dynamic (≥ 5.7.20)
Type

Default Value

Valid Values

884

--transaction-isolation=name

transaction_isolation

Global, Session

Yes

Enumeration

REPEATABLE-READ

READ-UNCOMMITTED

READ-COMMITTED

Server System Variables

REPEATABLE-READ

SERIALIZABLE

The transaction isolation level. The default is REPEATABLE-READ.

The transaction isolation level has three scopes: global, session, and next transaction. This three-scope
implementation leads to some nonstandard isolation-level assignment semantics, as described later.

To set the global transaction isolation level at startup, use the --transaction-isolation server
option.

At runtime, the isolation level can be set directly using the SET statement to assign a value to the
transaction_isolation system variable, or indirectly using the SET TRANSACTION statement. If
you set transaction_isolation directly to an isolation level name that contains a space, the name
should be enclosed within quotation marks, with the space replaced by a dash. For example, use this
SET statement to set the global value:

SET GLOBAL transaction_isolation = 'READ-COMMITTED';

Setting the global transaction_isolation value sets the isolation level for all subsequent sessions.
Existing sessions are unaffected.

To set the session or next-level transaction_isolation value, use the SET statement. For most
session system variables, these statements are equivalent ways to set the value:

SET @@SESSION.var_name = value;
SET SESSION var_name = value;
SET var_name = value;
SET @@var_name = value;

As mentioned previously, the transaction isolation level has a next-transaction scope, in addition to the
global and session scopes. To enable the next-transaction scope to be set, SET syntax for assigning
session system variable values has nonstandard semantics for transaction_isolation:

• To set the session isolation level, use any of these syntaxes:

SET @@SESSION.transaction_isolation = value;
SET SESSION transaction_isolation = value;

885

Server System Variables

SET transaction_isolation = value;

For each of those syntaxes, these semantics apply:

• Sets the isolation level for all subsequent transactions performed within the session.

• Permitted within transactions, but does not affect the current ongoing transaction.

• If executed between transactions, overrides any preceding statement that sets the next-transaction

isolation level.

• Corresponds to SET SESSION TRANSACTION ISOLATION LEVEL (with the SESSION keyword).

• To set the next-transaction isolation level, use this syntax:

SET @@transaction_isolation = value;

For that syntax, these semantics apply:

• Sets the isolation level only for the next single transaction performed within the session.

• Subsequent transactions revert to the session isolation level.

• Not permitted within transactions.

• Corresponds to SET TRANSACTION ISOLATION LEVEL (without the SESSION keyword).

For more information about SET TRANSACTION and its relationship to the transaction_isolation
system variable, see Section 13.3.6, “SET TRANSACTION Statement”.

Note

transaction_isolation was added in MySQL 5.7.20 as a synonym for
tx_isolation, which is now deprecated and is removed in MySQL 8.0.
Applications should be adjusted to use transaction_isolation in preference
to tx_isolation.

• transaction_prealloc_size

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value

Unit

Block Size

--transaction-prealloc-size=#

transaction_prealloc_size

Global, Session

Yes

Integer

4096

1024

131072

bytes

1024

There is a per-transaction memory pool from which various transaction-related allocations take memory.
The initial size of the pool in bytes is transaction_prealloc_size. For every allocation that
cannot be satisfied from the pool because it has insufficient memory available, the pool is increased

886

Server System Variables

by transaction_alloc_block_size bytes. When the transaction ends, the pool is truncated to
transaction_prealloc_size bytes.

By making transaction_prealloc_size sufficiently large to contain all statements within a single
transaction, you can avoid many malloc() calls.

• transaction_read_only

Command-Line Format

System Variable (≥ 5.7.20)
Scope (≥ 5.7.20)
Dynamic (≥ 5.7.20)
Type

Default Value

--transaction-read-only[={OFF|ON}]

transaction_read_only

Global, Session

Yes

Boolean

OFF

The transaction access mode. The value can be OFF (read/write; the default) or ON (read only).

The transaction access mode has three scopes: global, session, and next transaction. This three-scope
implementation leads to some nonstandard access-mode assignment semantics, as described later.

To set the global transaction access mode at startup, use the --transaction-read-only server
option.

At runtime, the access mode can be set directly using the SET statement to assign a value to the
transaction_read_only system variable, or indirectly using the SET TRANSACTION statement. For
example, use this SET statement to set the global value:

SET GLOBAL transaction_read_only = ON;

Setting the global transaction_read_only value sets the access mode for all subsequent sessions.
Existing sessions are unaffected.

To set the session or next-level transaction_read_only value, use the SET statement. For most
session system variables, these statements are equivalent ways to set the value:

SET @@SESSION.var_name = value;
SET SESSION var_name = value;
SET var_name = value;
SET @@var_name = value;

As mentioned previously, the transaction access mode has a next-transaction scope, in addition to the
global and session scopes. To enable the next-transaction scope to be set, SET syntax for assigning
session system variable values has nonstandard semantics for transaction_read_only,

• To set the session access mode, use any of these syntaxes:

SET @@SESSION.transaction_read_only = value;
SET SESSION transaction_read_only = value;

887

Server System Variables

SET transaction_read_only = value;

For each of those syntaxes, these semantics apply:

• Sets the access mode for all subsequent transactions performed within the session.

• Permitted within transactions, but does not affect the current ongoing transaction.

• If executed between transactions, overrides any preceding statement that sets the next-transaction

access mode.

• Corresponds to SET SESSION TRANSACTION {READ WRITE | READ ONLY} (with the

SESSION keyword).

• To set the next-transaction access mode, use this syntax:

SET @@transaction_read_only = value;

For that syntax, these semantics apply:

• Sets the access mode only for the next single transaction performed within the session.

• Subsequent transactions revert to the session access mode.

• Not permitted within transactions.

• Corresponds to SET TRANSACTION {READ WRITE | READ ONLY} (without the SESSION

keyword).

For more information about SET TRANSACTION and its relationship to the transaction_read_only
system variable, see Section 13.3.6, “SET TRANSACTION Statement”.

Note

transaction_read_only was added in MySQL 5.7.20 as a synonym for
tx_read_only, which is now deprecated and is removed in MySQL 8.0.
Applications should be adjusted to use transaction_read_only in preference
to tx_read_only.

• tx_isolation

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

888

5.7.20

tx_isolation

Global, Session

Yes

Enumeration

REPEATABLE-READ

READ-UNCOMMITTED

READ-COMMITTED

REPEATABLE-READ

Server System Variables

SERIALIZABLE

The default transaction isolation level. Defaults to REPEATABLE-READ.

Note

transaction_isolation was added in MySQL 5.7.20 as a synonym for
tx_isolation, which is now deprecated and is removed in MySQL 8.0.
Applications should be adjusted to use transaction_isolation in preference
to tx_isolation. See the description of transaction_isolation for
details.

• tx_read_only

Deprecated

System Variable

Scope

Dynamic

Type

Default Value

5.7.20

tx_read_only

Global, Session

Yes

Boolean

OFF

The default transaction access mode. The value can be OFF (read/write, the default) or ON (read only).

Note

transaction_read_only was added in MySQL 5.7.20 as a synonym for
tx_read_only, which is now deprecated and is removed in MySQL 8.0.
Applications should be adjusted to use transaction_read_only in preference
to tx_read_only. See the description of transaction_read_only for
details.

• unique_checks

System Variable

Scope

Dynamic

Type

Default Value

unique_checks

Global, Session

Yes

Boolean

ON

If set to 1 (the default), uniqueness checks for secondary indexes in InnoDB tables are performed. If set
to 0, storage engines are permitted to assume that duplicate keys are not present in input data. If you
know for certain that your data does not contain uniqueness violations, you can set this to 0 to speed up
large table imports to InnoDB.

Setting this variable to 0 does not require storage engines to ignore duplicate keys. An engine is still
permitted to check for them and issue duplicate-key errors if it detects them.

• updatable_views_with_limit

Command-Line Format

--updatable-views-with-limit[={OFF|
ON}]

889

Server System Variables

System Variable

Scope

Dynamic

Type

Default Value

updatable_views_with_limit

Global, Session

Yes

Boolean

1

This variable controls whether updates to a view can be made when the view does not contain all
columns of the primary key defined in the underlying table, if the update statement contains a LIMIT
clause. (Such updates often are generated by GUI tools.) An update is an UPDATE or DELETE statement.
Primary key here means a PRIMARY KEY, or a UNIQUE index in which no column can contain NULL.

The variable can have two values:

• 1 or YES: Issue a warning only (not an error message). This is the default value.

• 0 or NO: Prohibit the update.

• validate_password_xxx

The validate_password plugin implements a set of system variables having names of the form
validate_password_xxx. These variables affect password testing by that plugin; see Section 6.4.3.2,
“Password Validation Plugin Options and Variables”.

• version

The version number for the server. The value might also include a suffix indicating server build or
configuration information. -log indicates that one or more of the general log, slow query log, or binary
log are enabled. -debug indicates that the server was built with debugging support enabled.

• version_comment

System Variable

Scope

Dynamic

Type

version_comment

Global

No

String

The CMake configuration program has a COMPILATION_COMMENT option that permits a comment to be
specified when building MySQL. This variable contains the value of that comment. See Section 2.8.7,
“MySQL Source-Configuration Options”.

• version_compile_machine

System Variable

version_compile_machine

Scope

Dynamic

Type

The type of the server binary.

• version_compile_os

Global

No

String

System Variable

version_compile_os

890

Scope

Dynamic

Type

Using System Variables

Global

No

String

The type of operating system on which MySQL was built.

• wait_timeout

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

Minimum Value

Maximum Value (Windows)

Maximum Value (Other)

Unit

--wait-timeout=#

wait_timeout

Global, Session

Yes

Integer

28800

1

2147483

31536000

seconds

The number of seconds the server waits for activity on a noninteractive connection before closing it.

On thread startup, the session wait_timeout value is initialized from the global wait_timeout
value or from the global interactive_timeout value, depending on the type of client (as
defined by the CLIENT_INTERACTIVE connect option to mysql_real_connect()). See also
interactive_timeout.

• warning_count

The number of errors, warnings, and notes that resulted from the last statement that generated
messages. This variable is read only. See Section 13.7.5.40, “SHOW WARNINGS Statement”.

5.1.8 Using System Variables

The MySQL server maintains many system variables that configure its operation. Section 5.1.7, “Server
System Variables”, describes the meaning of these variables. Each system variable has a default value.
System variables can be set at server startup using options on the command line or in an option file.
Most of them can be changed dynamically while the server is running by means of the SET statement,
which enables you to modify operation of the server without having to stop and restart it. You can also use
system variable values in expressions.

Many system variables are built in. System variables implemented by a server plugin are exposed when
the plugin is installed and have names that begin with the plugin name. For example, the audit_log
plugin implements a system variable named audit_log_policy.

There are two scopes in which system variables exist. Global variables affect the overall operation of the
server. Session variables affect its operation for individual client connections. A given system variable can
have both a global and a session value. Global and session system variables are related as follows:

• When the server starts, it initializes each global variable to its default value. These defaults can be

changed by options specified on the command line or in an option file. (See Section 4.2.2, “Specifying
Program Options”.)

891

Using System Variables

• The server also maintains a set of session variables for each client that connects. The client's session
variables are initialized at connect time using the current values of the corresponding global variables.
For example, a client's SQL mode is controlled by the session sql_mode value, which is initialized when
the client connects to the value of the global sql_mode value.

For some system variables, the session value is not initialized from the corresponding global value; if so,
that is indicated in the variable description.

System variable values can be set globally at server startup by using options on the command line
or in an option file. At startup, the syntax for system variables is the same as for command options,
so within variable names, dashes and underscores may be used interchangeably. For example, --
general_log=ON and --general-log=ON are equivalent.

When you use a startup option to set a variable that takes a numeric value, the value can be given with a
suffix of K, M, or G (either uppercase or lowercase) to indicate a multiplier of 1024, 10242 or 10243; that is,
units of kilobytes, megabytes, or gigabytes, respectively. Thus, the following command starts the server
with an InnoDB log file size of 16 megabytes and a maximum packet size of one gigabyte:

mysqld --innodb-log-file-size=16M --max-allowed-packet=1G

Within an option file, those variables are set like this:

[mysqld]
innodb_log_file_size=16M
max_allowed_packet=1G

The lettercase of suffix letters does not matter; 16M and 16m are equivalent, as are 1G and 1g.

To restrict the maximum value to which a system variable can be set at runtime with the SET statement,
specify this maximum by using an option of the form --maximum-var_name=value at server startup. For
example, to prevent the value of innodb_log_file_size from being increased to more than 32MB at
runtime, use the option --maximum-innodb-log-file-size=32M.

Many system variables are dynamic and can be changed at runtime by using the SET statement. For a
list, see Section 5.1.8.2, “Dynamic System Variables”. To change a system variable with SET, refer to
it by name, optionally preceded by a modifier. At runtime, system variable names must be written using
underscores, not dashes. The following examples briefly illustrate this syntax:

• Set a global system variable:

SET GLOBAL max_connections = 1000;
SET @@GLOBAL.max_connections = 1000;

• Set a session system variable:

SET SESSION sql_mode = 'TRADITIONAL';
SET @@SESSION.sql_mode = 'TRADITIONAL';
SET @@sql_mode = 'TRADITIONAL';

For complete details about SET syntax, see Section 13.7.4.1, “SET Syntax for Variable Assignment”.
For a description of the privilege requirements for setting system variables, see Section 5.1.8.1, “System
Variable Privileges”

Suffixes for specifying a value multiplier can be used when setting a variable at server startup, but not to
set the value with SET at runtime. On the other hand, with SET you can assign a variable's value using
an expression, which is not true when you set a variable at server startup. For example, the first of the
following lines is legal at server startup, but the second is not:

$> mysql --max_allowed_packet=16M
$> mysql --max_allowed_packet=16*1024*1024

892

Using System Variables

Conversely, the second of the following lines is legal at runtime, but the first is not:

mysql> SET GLOBAL max_allowed_packet=16M;
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;

To display system variable names and values, use the SHOW VARIABLES statement:

mysql> SHOW VARIABLES;
+---------------------------------+-----------------------------------+
| Variable_name                   | Value                             |
+---------------------------------+-----------------------------------+
| auto_increment_increment        | 1                                 |
| auto_increment_offset           | 1                                 |
| automatic_sp_privileges         | ON                                |
| back_log                        | 50                                |
| basedir                         | /home/mysql/                      |
| binlog_cache_size               | 32768                             |
| bulk_insert_buffer_size         | 8388608                           |
| character_set_client            | utf8                              |
| character_set_connection        | utf8                              |
| character_set_database          | latin1                            |
| character_set_filesystem        | binary                            |
| character_set_results           | utf8                              |
| character_set_server            | latin1                            |
| character_set_system            | utf8                              |
| character_sets_dir              | /home/mysql/share/mysql/charsets/ |
| collation_connection            | utf8_general_ci                   |
| collation_database              | latin1_swedish_ci                 |
| collation_server                | latin1_swedish_ci                 |
...
| innodb_autoextend_increment     | 8                                 |
| innodb_buffer_pool_size         | 8388608                           |
| innodb_checksums                | ON                                |
| innodb_commit_concurrency       | 0                                 |
| innodb_concurrency_tickets      | 500                               |
| innodb_data_file_path           | ibdata1:10M:autoextend            |
| innodb_data_home_dir            |                                   |
...
| version                         | 5.7.18-log                        |
| version_comment                 | Source distribution               |
| version_compile_machine         | i686                              |
| version_compile_os              | suse-linux                        |
| wait_timeout                    | 28800                             |
+---------------------------------+-----------------------------------+

With a LIKE clause, the statement displays only those variables that match the pattern. To obtain a
specific variable name, use a LIKE clause as shown:

SHOW VARIABLES LIKE 'max_join_size';
SHOW SESSION VARIABLES LIKE 'max_join_size';

To get a list of variables whose name match a pattern, use the % wildcard character in a LIKE clause:

SHOW VARIABLES LIKE '%size%';
SHOW GLOBAL VARIABLES LIKE '%size%';

Wildcard characters can be used in any position within the pattern to be matched. Strictly speaking,
because _ is a wildcard that matches any single character, you should escape it as \_ to match it literally.
In practice, this is rarely necessary.

For SHOW VARIABLES, if you specify neither GLOBAL nor SESSION, MySQL returns SESSION values.

The reason for requiring the GLOBAL keyword when setting GLOBAL-only variables but not when retrieving
them is to prevent problems in the future:

893

Using System Variables

• Were a SESSION variable to be removed that has the same name as a GLOBAL variable, a client with

privileges sufficient to modify global variables might accidentally change the GLOBAL variable rather than
just the SESSION variable for its own session.

• Were a SESSION variable to be added with the same name as a GLOBAL variable, a client that intends to

change the GLOBAL variable might find only its own SESSION variable changed.

5.1.8.1 System Variable Privileges

A system variable can have a global value that affects server operation as a whole, a session value that
affects only the current session, or both. To modify system variable runtime values, use the SET statement.
See Section 13.7.4.1, “SET Syntax for Variable Assignment”. This section describes the privileges required
to assign values to system variables at runtime.

Setting a global system variable runtime value requires the SUPER privilege.

To set a session system variable runtime value, use the SET SESSION statement. In contrast to setting
global runtime values, setting session runtime values normally requires no special privileges and can be
done by any user to affect the current session. For some system variables, setting the session value may
have effects outside the current session and thus is a restricted operation that can be done only by users
who have the SUPER privilege. If a session system variable is restricted in this way, the variable description
indicates that restriction. Examples include binlog_format and sql_log_bin. Setting the session
value of these variables affects binary logging for the current session, but may also have wider implications
for the integrity of server replication and backups.

5.1.8.2 Dynamic System Variables

Many server system variables are dynamic and can be set at runtime. See Section 13.7.4.1, “SET Syntax
for Variable Assignment”. For a description of the privilege requirements for setting system variables, see
Section 5.1.8.1, “System Variable Privileges”

The following table lists all dynamic system variables applicable within mysqld.

The table lists each variable's data type and scope. The last column indicates whether the scope for each
variable is Global, Session, or both. Please see the corresponding item descriptions for details on setting
and using the variables. Where appropriate, direct links to further information about the items are provided.

Variables that have a type of “string” take a string value. Variables that have a type of “numeric” take a
numeric value. Variables that have a type of “boolean” can be set to 0, 1, ON or OFF. Variables that are
marked as “enumeration” normally should be set to one of the available values for the variable, but can
also be set to the number that corresponds to the desired enumeration value. For enumerated system
variables, the first enumeration value corresponds to 0. This differs from the ENUM data type used for table
columns, for which the first enumeration value corresponds to 1.

Table 5.4 Dynamic System Variable Summary

Variable Name

Variable Type

Variable Scope

audit_log_connection_policy

Enumeration

audit_log_disable

Boolean

audit_log_exclude_accounts

String

audit_log_flush

Boolean

audit_log_format_unix_timestamp Boolean

audit_log_include_accounts

audit_log_read_buffer_size

String

Integer

Global

Global

Global

Global

Global

Global

Varies

894

Using System Variables

Variable Name

Variable Type

Variable Scope

audit_log_rotate_on_size

Integer

audit_log_statement_policy

Enumeration

authentication_ldap_sasl_auth_method_name

String

authentication_ldap_sasl_bind_base_dnString

authentication_ldap_sasl_bind_root_dnString

authentication_ldap_sasl_bind_root_pwdString

authentication_ldap_sasl_ca_path String

authentication_ldap_sasl_group_search_attr

String

authentication_ldap_sasl_group_search_filter

String

authentication_ldap_sasl_init_pool_sizeInteger

authentication_ldap_sasl_log_statusInteger

authentication_ldap_sasl_max_pool_size

Integer

authentication_ldap_sasl_server_hostString

authentication_ldap_sasl_server_portInteger

authentication_ldap_sasl_tls

Boolean

authentication_ldap_sasl_user_search_attr

String

authentication_ldap_simple_auth_method_name

String

authentication_ldap_simple_bind_base_dn

String

String
authentication_ldap_simple_bind_root_dn

authentication_ldap_simple_bind_root_pwd

String

authentication_ldap_simple_ca_pathString

authentication_ldap_simple_group_search_attr

String

authentication_ldap_simple_group_search_filter

String

Integer
authentication_ldap_simple_init_pool_size

authentication_ldap_simple_log_statusInteger

Integer
authentication_ldap_simple_max_pool_size

authentication_ldap_simple_server_hostString

authentication_ldap_simple_server_port

Integer

authentication_ldap_simple_tls

Boolean

authentication_ldap_simple_user_search_attr

String

auto_increment_increment

auto_increment_offset

autocommit

automatic_sp_privileges

avoid_temporal_upgrade

big_tables

binlog_cache_size

binlog_checksum

Integer

Integer

Boolean

Boolean

Boolean

Boolean

Integer

String

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Global

Global

Both

Global

Global

895

Using System Variables

Variable Name

Variable Type

Variable Scope

binlog_direct_non_transactional_updatesBoolean

binlog_error_action

binlog_format

Enumeration

Enumeration

binlog_group_commit_sync_delay Integer

binlog_group_commit_sync_no_delay_count

Integer

binlog_max_flush_queue_time

Integer

binlog_order_commits

binlog_row_image

Boolean

Enumeration

binlog_rows_query_log_events

Boolean

binlog_stmt_cache_size

Integer

binlog_transaction_dependency_history_size

Integer

binlog_transaction_dependency_trackingEnumeration

block_encryption_mode

bulk_insert_buffer_size

character_set_client

character_set_connection

character_set_database

character_set_filesystem

character_set_results

character_set_server

check_proxy_users

collation_connection

collation_database

collation_server

completion_type

concurrent_insert

connect_timeout

String

Integer

String

String

String

String

String

String

Boolean

String

String

String

Enumeration

Enumeration

Integer

connection_control_failed_connections_threshold

Integer

Integer
connection_control_max_connection_delay

Integer
connection_control_min_connection_delay

debug

debug_sync

default_password_lifetime

String

String

Integer

default_storage_engine

Enumeration

default_tmp_storage_engine

Enumeration

default_week_format

delay_key_write

delayed_insert_limit

Integer

Enumeration

Integer

896

Both

Global

Both

Global

Global

Global

Global

Both

Both

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Global

Both

Both

Both

Both

Global

Global

Global

Global

Global

Both

Session

Global

Both

Both

Both

Global

Global

Using System Variables

Variable Name

Variable Type

Variable Scope

delayed_insert_timeout

delayed_queue_size

div_precision_increment

end_markers_in_json

Integer

Integer

Integer

Boolean

enforce_gtid_consistency

Enumeration

eq_range_index_dive_limit

Integer

event_scheduler

expire_logs_days

Enumeration

Integer

explicit_defaults_for_timestamp

Boolean

flush

flush_time

foreign_key_checks

ft_boolean_syntax

general_log

general_log_file

group_concat_max_len

Boolean

Integer

Boolean

String

Boolean

File name

Integer

group_replication_allow_local_disjoint_gtids_join

Boolean

group_replication_allow_local_lower_version_join

Boolean

group_replication_auto_increment_increment

Integer

group_replication_bootstrap_group Boolean

group_replication_components_stop_timeout

Integer

Integer
group_replication_compression_threshold

group_replication_enforce_update_everywhere_checks

Boolean

group_replication_exit_state_actionEnumeration

group_replication_flow_control_applier_threshold

Integer

group_replication_flow_control_certifier_threshold

Integer

group_replication_flow_control_modeEnumeration

group_replication_force_members String

group_replication_group_name

group_replication_group_seeds

String

String

group_replication_gtid_assignment_block_size

Integer

group_replication_ip_whitelist

String

group_replication_local_address

String

group_replication_member_weight Integer

group_replication_poll_spin_loops Integer

group_replication_recovery_complete_atEnumeration

group_replication_recovery_reconnect_interval

Integer

group_replication_recovery_retry_count

Integer

Global

Global

Both

Both

Global

Both

Global

Global

Both

Global

Global

Both

Global

Global

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

897

Using System Variables

Variable Name

Variable Type

Variable Scope

group_replication_recovery_ssl_ca String

group_replication_recovery_ssl_capathString

group_replication_recovery_ssl_certString

group_replication_recovery_ssl_cipherString

group_replication_recovery_ssl_crl File name

group_replication_recovery_ssl_crlpathDirectory name

group_replication_recovery_ssl_keyString

group_replication_recovery_ssl_verify_server_cert

Boolean

group_replication_recovery_use_sslBoolean

group_replication_single_primary_modeBoolean

group_replication_ssl_mode

Enumeration

group_replication_start_on_boot

Boolean

group_replication_transaction_size_limit

Integer

group_replication_unreachable_majority_timeout

Integer

gtid_executed_compression_periodInteger

gtid_mode

gtid_next

gtid_purged

host_cache_size

identity

init_connect

init_slave

Enumeration

Enumeration

String

Integer

Integer

String

String

innodb_adaptive_flushing

Boolean

innodb_adaptive_flushing_lwm

Integer

innodb_adaptive_hash_index

Boolean

innodb_adaptive_max_sleep_delay Integer

innodb_api_bk_commit_interval

Integer

innodb_api_trx_level

innodb_autoextend_increment

Integer

Integer

innodb_background_drop_list_emptyBoolean

innodb_buffer_pool_dump_at_shutdownBoolean

innodb_buffer_pool_dump_now

Boolean

innodb_buffer_pool_dump_pct

Integer

innodb_buffer_pool_filename

File name

innodb_buffer_pool_load_abort

Boolean

innodb_buffer_pool_load_now

Boolean

innodb_buffer_pool_size

Integer

innodb_change_buffer_max_size Integer

898

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

Global

Global

Session

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Using System Variables

Variable Name

Variable Type

Variable Scope

innodb_change_buffering

Enumeration

innodb_change_buffering_debug

Integer

innodb_checksum_algorithm

Enumeration

innodb_cmp_per_index_enabled Boolean

innodb_commit_concurrency

Integer

innodb_compress_debug

Enumeration

Integer
innodb_compression_failure_threshold_pct

innodb_compression_level

Integer

innodb_compression_pad_pct_maxInteger

innodb_concurrency_tickets

innodb_deadlock_detect

Integer

Boolean

innodb_default_row_format

Enumeration

innodb_disable_resize_buffer_pool_debug

Boolean

innodb_disable_sort_file_cache

Boolean

innodb_fast_shutdown

Integer

innodb_fil_make_page_dirty_debugInteger

innodb_file_format

innodb_file_format_max

innodb_file_per_table

innodb_fill_factor

innodb_flush_log_at_timeout

String

String

Boolean

Integer

Integer

innodb_flush_log_at_trx_commit

Enumeration

innodb_flush_neighbors

Enumeration

innodb_flush_sync

innodb_flushing_avg_loops

innodb_ft_aux_table

innodb_ft_enable_diag_print

innodb_ft_enable_stopword

innodb_ft_num_word_optimize

innodb_ft_result_cache_limit

Boolean

Integer

String

Boolean

Boolean

Integer

Integer

innodb_ft_server_stopword_table String

innodb_ft_user_stopword_table

String

innodb_io_capacity

innodb_io_capacity_max

innodb_large_prefix

Integer

Integer

Boolean

innodb_limit_optimistic_insert_debugInteger

innodb_lock_wait_timeout

innodb_log_checkpoint_now

Integer

Boolean

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Both

Global

Global

Global

Global

Both

Global

899

Using System Variables

Variable Name

Variable Type

Variable Scope

innodb_log_checksums

Boolean

innodb_log_compressed_pages

Boolean

innodb_log_write_ahead_size

innodb_lru_scan_depth

Integer

Integer

innodb_max_dirty_pages_pct

Numeric

innodb_max_dirty_pages_pct_lwm Numeric

innodb_max_purge_lag

innodb_max_purge_lag_delay

innodb_max_undo_log_size

Integer

Integer

Integer

innodb_merge_threshold_set_all_debug

Integer

innodb_monitor_disable

innodb_monitor_enable

innodb_monitor_reset

innodb_monitor_reset_all

innodb_old_blocks_pct

innodb_old_blocks_time

String

String

Enumeration

Enumeration

Integer

Integer

innodb_online_alter_log_max_size Integer

innodb_optimize_fulltext_only

innodb_print_all_deadlocks

innodb_purge_batch_size

Boolean

Boolean

Integer

innodb_purge_rseg_truncate_frequency

Integer

innodb_random_read_ahead

Boolean

innodb_read_ahead_threshold

innodb_replication_delay

innodb_rollback_segments

Integer

Integer

Integer

innodb_saved_page_number_debugInteger

innodb_spin_wait_delay

innodb_stats_auto_recalc

Integer

Boolean

innodb_stats_include_delete_markedBoolean

innodb_stats_method

Enumeration

innodb_stats_on_metadata

innodb_stats_persistent

Boolean

Boolean

innodb_stats_persistent_sample_pages

Integer

innodb_stats_sample_pages

Integer

innodb_stats_transient_sample_pagesInteger

innodb_status_output

innodb_status_output_locks

innodb_strict_mode

Boolean

Boolean

Boolean

900

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Using System Variables

Variable Type

Variable Scope

Variable Name

innodb_support_xa

innodb_sync_spin_loops

innodb_table_locks

innodb_thread_concurrency

innodb_thread_sleep_delay

Boolean

Integer

Boolean

Integer

Integer

innodb_tmpdir

Directory name

Boolean
innodb_trx_purge_view_update_only_debug

innodb_trx_rseg_n_slots_debug

Integer

innodb_undo_log_truncate

Boolean

innodb_undo_logs

insert_id

interactive_timeout

Integer

Integer

Integer

internal_tmp_disk_storage_engine Enumeration

join_buffer_size

keep_files_on_create

key_buffer_size

key_cache_age_threshold

key_cache_block_size

key_cache_division_limit

keyring_aws_cmk_id

keyring_aws_region

Integer

Boolean

Integer

Integer

Integer

Integer

String

Enumeration

keyring_encrypted_file_data

File name

keyring_encrypted_file_password String

keyring_file_data

File name

keyring_okv_conf_dir

Directory name

keyring_operations

last_insert_id

lc_messages

lc_time_names

local_infile

lock_wait_timeout

Boolean

Integer

String

String

Boolean

Integer

log_bin_trust_function_creators

Boolean

log_bin_use_v1_row_events

Boolean

log_builtin_as_identified_by_passwordBoolean

log_error_verbosity

log_output

Integer

Set

log_queries_not_using_indexes

Boolean

log_slow_admin_statements

Boolean

Both

Global

Both

Global

Global

Both

Global

Global

Global

Global

Session

Both

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Session

Both

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

901

Using System Variables

Variable Name

Variable Type

Variable Scope

log_slow_slave_statements

Boolean

log_statements_unsafe_for_binlog Boolean

log_syslog

log_syslog_facility

log_syslog_include_pid

log_syslog_tag

Boolean

String

Boolean

String

log_throttle_queries_not_using_indexes

Integer

log_timestamps

log_warnings

long_query_time

low_priority_updates

master_info_repository

master_verify_checksum

max_allowed_packet

max_binlog_cache_size

max_binlog_size

max_binlog_stmt_cache_size

max_connect_errors

max_connections

max_delayed_threads

max_error_count

max_execution_time

max_heap_table_size

max_insert_delayed_threads

max_join_size

max_length_for_sort_data

max_points_in_geometry

max_prepared_stmt_count

max_relay_log_size

max_seeks_for_key

max_sort_length

max_sp_recursion_depth

max_tmp_tables

max_user_connections

max_write_lock_count

min_examined_row_limit

multi_range_count

myisam_data_pointer_size

Enumeration

Integer

Numeric

Boolean

String

Boolean

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

Integer

902

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Global

Global

Both

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Both

Both

Both

Both

Both

Global

Both

Both

Global

Using System Variables

Variable Name

Variable Type

Variable Scope

myisam_max_sort_file_size

myisam_repair_threads

myisam_sort_buffer_size

Integer

Integer

Integer

myisam_stats_method

Enumeration

myisam_use_mmap

mysql_firewall_mode

mysql_firewall_trace

Boolean

Boolean

Boolean

mysql_native_password_proxy_usersBoolean

mysqlx_connect_timeout

Integer

mysqlx_idle_worker_thread_timeoutInteger

mysqlx_max_allowed_packet

mysqlx_max_connections

mysqlx_min_worker_threads

Integer

Integer

Integer

ndb_allow_copying_alter_table

Boolean

ndb_autoincrement_prefetch_sz

Integer

ndb_batch_size

ndb_blob_read_batch_bytes

ndb_blob_write_batch_bytes

ndb_cache_check_time

ndb_clear_apply_status

ndb_data_node_neighbour

Integer

Integer

Integer

Integer

Boolean

Integer

ndb_default_column_format

Enumeration

ndb_default_column_format

Enumeration

ndb_deferred_constraints

ndb_deferred_constraints

ndb_distribution

ndb_distribution

ndb_eventbuffer_free_percent

ndb_eventbuffer_max_alloc

ndb_extra_logging

ndb_force_send

ndb_fully_replicated

ndb_index_stat_enable

ndb_index_stat_option

ndb_join_pushdown

ndb_log_binlog_index

ndb_log_empty_epochs

ndb_log_empty_epochs

Integer

Integer

Enumeration

Enumeration

Integer

Integer

Integer

Boolean

Boolean

Boolean

String

Boolean

Boolean

Boolean

Boolean

Global

Both

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Global

Global

Global

Both

Both

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Global

903

Using System Variables

Variable Name

Variable Type

Variable Scope

ndb_log_empty_update

ndb_log_empty_update

ndb_log_exclusive_reads

ndb_log_exclusive_reads

ndb_log_update_as_write

ndb_log_update_minimal

ndb_log_updated_only

ndb_optimization_delay

Boolean

Boolean

Boolean

Boolean

Boolean

Boolean

Boolean

Integer

ndb_optimized_node_selection

Integer

ndb_read_backup

Boolean

ndb_recv_thread_activation_thresholdInteger

ndb_recv_thread_cpu_mask

Bitmap

ndb_report_thresh_binlog_epoch_slipInteger

ndb_report_thresh_binlog_mem_usageInteger

ndb_row_checksum

Integer

ndb_show_foreign_key_mock_tablesBoolean

ndb_slave_conflict_role

Enumeration

ndb_table_no_logging

ndb_table_temporary

ndb_use_exact_count

ndb_use_transactions

ndbinfo_max_bytes

ndbinfo_max_rows

ndbinfo_offline

ndbinfo_show_hidden

net_buffer_length

net_read_timeout

net_retry_count

net_write_timeout

new

offline_mode

old_alter_table

old_passwords

optimizer_prune_level

optimizer_search_depth

optimizer_switch

optimizer_trace

optimizer_trace_features

Boolean

Boolean

Boolean

Boolean

Integer

Integer

Boolean

Boolean

Integer

Integer

Integer

Integer

Boolean

Boolean

Boolean

Enumeration

Integer

Integer

Set

String

String

904

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Session

Session

Both

Both

Both

Both

Global

Both

Both

Both

Both

Both

Both

Global

Both

Both

Both

Both

Both

Both

Both

Using System Variables

Variable Name

Variable Type

Variable Scope

optimizer_trace_limit

Integer

optimizer_trace_max_mem_size

Integer

optimizer_trace_offset

parser_max_mem_size

Integer

Integer

performance_schema_show_processlistBoolean

preload_buffer_size

profiling

profiling_history_size

pseudo_slave_mode

pseudo_thread_id

query_alloc_block_size

query_cache_limit

query_cache_min_res_unit

query_cache_size

query_cache_type

Integer

Boolean

Integer

Boolean

Integer

Integer

Integer

Integer

Integer

Enumeration

query_cache_wlock_invalidate

Boolean

query_prealloc_size

rand_seed1

rand_seed2

range_alloc_block_size

Integer

Integer

Integer

Integer

range_optimizer_max_mem_size Integer

rbr_exec_mode

read_buffer_size

read_only

read_rnd_buffer_size

relay_log_info_repository

relay_log_purge

Enumeration

Integer

Boolean

Integer

String

Boolean

Boolean
replication_optimize_for_static_plugin_config

replication_sender_observe_commit_only

Boolean

require_secure_transport

rewriter_enabled

rewriter_verbose

Boolean

Boolean

Integer

rpl_semi_sync_master_enabled

Boolean

rpl_semi_sync_master_timeout

Integer

rpl_semi_sync_master_trace_level Integer

rpl_semi_sync_master_wait_for_slave_count

Integer

rpl_semi_sync_master_wait_no_slaveBoolean

rpl_semi_sync_master_wait_point Enumeration

Both

Both

Both

Both

Global

Both

Both

Both

Session

Session

Both

Global

Global

Global

Both

Both

Both

Session

Session

Both

Both

Session

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

905

Using System Variables

Variable Name

Variable Type

Variable Scope

rpl_semi_sync_slave_enabled

Boolean

rpl_semi_sync_slave_trace_level

Integer

rpl_stop_slave_timeout

secure_auth

server_id

Integer

Boolean

Integer

session_track_gtids

Enumeration

session_track_schema

session_track_state_change

Boolean

Boolean

session_track_system_variables

String

session_track_transaction_info

Enumeration

sha256_password_proxy_users

Boolean

show_compatibility_56

show_create_table_verbosity

show_old_temporals

slave_allow_batching

slave_checkpoint_group

slave_checkpoint_period

Boolean

Boolean

Boolean

Boolean

Integer

Integer

slave_compressed_protocol

Boolean

slave_exec_mode

Enumeration

slave_max_allowed_packet

slave_net_timeout

slave_parallel_type

slave_parallel_workers

slave_pending_jobs_size_max

Integer

Integer

Enumeration

Integer

Integer

slave_preserve_commit_order

Boolean

slave_rows_search_algorithms

Set

slave_sql_verify_checksum

slave_transaction_retries

slave_type_conversions

slow_launch_time

slow_query_log

Boolean

Integer

Set

Integer

Boolean

slow_query_log_file

File name

sort_buffer_size

sql_auto_is_null

sql_big_selects

sql_buffer_result

sql_log_bin

sql_log_off

Integer

Boolean

Boolean

Boolean

Boolean

Boolean

906

Global

Global

Global

Global

Global

Both

Both

Both

Both

Both

Global

Global

Both

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Both

Both

Both

Session

Both

Using System Variables

Variable Name

Variable Type

Variable Scope

sql_mode

sql_notes

sql_quote_show_create

sql_safe_updates

sql_select_limit

sql_slave_skip_counter

sql_warnings

stored_program_cache

super_read_only

sync_binlog

sync_frm

sync_master_info

sync_relay_log

sync_relay_log_info

table_definition_cache

table_open_cache

thread_cache_size

Set

Boolean

Boolean

Boolean

Integer

Integer

Boolean

Integer

Boolean

Integer

Boolean

Integer

Integer

Integer

Integer

Integer

Integer

thread_pool_high_priority_connectionInteger

thread_pool_max_unused_threads Integer

thread_pool_prio_kickup_timer

thread_pool_stall_limit

time_zone

timestamp

tmp_table_size

transaction_alloc_block_size

Integer

Integer

String

Numeric

Integer

Integer

transaction_allow_batching

Boolean

transaction_isolation

Enumeration

transaction_prealloc_size

transaction_read_only

Integer

Boolean

transaction_write_set_extraction

Enumeration

tx_isolation

tx_read_only

unique_checks

updatable_views_with_limit

Enumeration

Boolean

Boolean

Boolean

validate_password_check_user_nameBoolean

validate_password_dictionary_file File name

validate_password_length

Integer

validate_password_mixed_case_count

Integer

Both

Both

Both

Both

Both

Global

Both

Global

Global

Global

Global

Global

Global

Global

Global

Global

Global

Both

Global

Global

Global

Both

Session

Both

Both

Session

Both

Both

Both

Both

Both

Both

Both

Both

Global

Global

Global

Global

907

Using System Variables

Variable Name

Variable Type

Variable Scope

validate_password_number_count

Integer

validate_password_policy

Enumeration

validate_password_special_char_count

Integer

version_tokens_session

wait_timeout

String

Integer

Global

Global

Global

Both

Both

5.1.8.3 Structured System Variables

A structured variable differs from a regular system variable in two respects:

• Its value is a structure with components that specify server parameters considered to be closely related.

• There might be several instances of a given type of structured variable. Each one has a different name

and refers to a different resource maintained by the server.

MySQL supports one structured variable type, which specifies parameters governing the operation of key
caches. A key cache structured variable has these components:

• key_buffer_size

• key_cache_block_size

• key_cache_division_limit

• key_cache_age_threshold

This section describes the syntax for referring to structured variables. Key cache variables are used
for syntax examples, but specific details about how key caches operate are found elsewhere, in
Section 8.10.2, “The MyISAM Key Cache”.

To refer to a component of a structured variable instance, you can use a compound name in
instance_name.component_name format. Examples:

hot_cache.key_buffer_size
hot_cache.key_cache_block_size
cold_cache.key_cache_block_size

For each structured system variable, an instance with the name of default is always predefined. If you
refer to a component of a structured variable without any instance name, the default instance is used.
Thus, default.key_buffer_size and key_buffer_size both refer to the same system variable.

Structured variable instances and components follow these naming rules:

• For a given type of structured variable, each instance must have a name that is unique within variables

of that type. However, instance names need not be unique across structured variable types. For
example, each structured variable has an instance named default, so default is not unique across
variable types.

• The names of the components of each structured variable type must be unique across all system

variable names. If this were not true (that is, if two different types of structured variables could share
component member names), it would not be clear which default structured variable to use for references
to member names that are not qualified by an instance name.

• If a structured variable instance name is not legal as an unquoted identifier, refer to it as a quoted

identifier using backticks. For example, hot-cache is not legal, but `hot-cache` is.

908

Server Status Variables

• global, session, and local are not legal instance names. This avoids a conflict with notation such as

@@GLOBAL.var_name for referring to nonstructured system variables.

Currently, the first two rules have no possibility of being violated because the only structured variable type
is the one for key caches. These rules may assume greater significance if some other type of structured
variable is created in the future.

With one exception, you can refer to structured variable components using compound names in any
context where simple variable names can occur. For example, you can assign a value to a structured
variable using a command-line option:

$> mysqld --hot_cache.key_buffer_size=64K

In an option file, use this syntax:

[mysqld]
hot_cache.key_buffer_size=64K

If you start the server with this option, it creates a key cache named hot_cache with a size of 64KB in
addition to the default key cache that has a default size of 8MB.

Suppose that you start the server as follows:

$> mysqld --key_buffer_size=256K \
         --extra_cache.key_buffer_size=128K \
         --extra_cache.key_cache_block_size=2048

In this case, the server sets the size of the default key cache to 256KB. (You could also have written
--default.key_buffer_size=256K.) In addition, the server creates a second key cache named
extra_cache that has a size of 128KB, with the size of block buffers for caching table index blocks set to
2048 bytes.

The following example starts the server with three different key caches having sizes in a 3:1:1 ratio:

$> mysqld --key_buffer_size=6M \
         --hot_cache.key_buffer_size=2M \
         --cold_cache.key_buffer_size=2M

Structured variable values may be set and retrieved at runtime as well. For example, to set a key cache
named hot_cache to a size of 10MB, use either of these statements:

mysql> SET GLOBAL hot_cache.key_buffer_size = 10*1024*1024;
mysql> SET @@GLOBAL.hot_cache.key_buffer_size = 10*1024*1024;

To retrieve the cache size, do this:

mysql> SELECT @@GLOBAL.hot_cache.key_buffer_size;

However, the following statement does not work. The variable is not interpreted as a compound name, but
as a simple string for a LIKE pattern-matching operation:

mysql> SHOW GLOBAL VARIABLES LIKE 'hot_cache.key_buffer_size';

This is the exception to being able to use structured variable names anywhere a simple variable name may
occur.

5.1.9 Server Status Variables

The MySQL server maintains many status variables that provide information about its operation. You can
view these variables and their values by using the SHOW [GLOBAL | SESSION] STATUS statement (see
Section 13.7.5.35, “SHOW STATUS Statement”). The optional GLOBAL keyword aggregates the values
over all connections, and SESSION shows the values for the current connection.

909

Server Status Variables

mysql> SHOW GLOBAL STATUS;
+-----------------------------------+------------+
| Variable_name                     | Value      |
+-----------------------------------+------------+
| Aborted_clients                   | 0          |
| Aborted_connects                  | 0          |
| Bytes_received                    | 155372598  |
| Bytes_sent                        | 1176560426 |
...
| Connections                       | 30023      |
| Created_tmp_disk_tables           | 0          |
| Created_tmp_files                 | 3          |
| Created_tmp_tables                | 2          |
...
| Threads_created                   | 217        |
| Threads_running                   | 88         |
| Uptime                            | 1389872    |
+-----------------------------------+------------+

Many status variables are reset to 0 by the FLUSH STATUS statement.

This section provides a description of each status variable. For a status variable summary, see
Section 5.1.5, “Server Status Variable Reference”. For information about status variables specific to NDB
Cluster, see NDB Cluster Status Variables.

The status variables have the meanings shown in the following list.

• Aborted_clients

The number of connections that were aborted because the client died without closing the connection
properly. See Section B.3.2.9, “Communication Errors and Aborted Connections”.

• Aborted_connects

The number of failed attempts to connect to the MySQL server. See Section B.3.2.9, “Communication
Errors and Aborted Connections”.

For additional connection-related information, check the Connection_errors_xxx status variables
and the host_cache table.

As of MySQL 5.7.3, Aborted_connects is not visible in the embedded server because for that server it
is not updated and is not meaningful.

• Binlog_cache_disk_use

The number of transactions that used the temporary binary log cache but that exceeded the value of
binlog_cache_size and used a temporary file to store statements from the transaction.

The number of nontransactional statements that caused the binary log transaction cache to be written to
disk is tracked separately in the Binlog_stmt_cache_disk_use status variable.

• Binlog_cache_use

The number of transactions that used the binary log cache.

• Binlog_stmt_cache_disk_use

The number of nontransaction statements that used the binary log statement cache but that exceeded
the value of binlog_stmt_cache_size and used a temporary file to store those statements.

• Binlog_stmt_cache_use

910

Server Status Variables

The number of nontransactional statements that used the binary log statement cache.

• Bytes_received

The number of bytes received from all clients.

• Bytes_sent

The number of bytes sent to all clients.

• Com_xxx

The Com_xxx statement counter variables indicate the number of times each xxx statement has
been executed. There is one status variable for each type of statement. For example, Com_delete
and Com_update count DELETE and UPDATE statements, respectively. Com_delete_multi and
Com_update_multi are similar but apply to DELETE and UPDATE statements that use multiple-table
syntax.

If a query result is returned from query cache, the server increments the Qcache_hits status variable,
not Com_select. See Section 8.10.3.4, “Query Cache Status and Maintenance”.

All Com_stmt_xxx variables are increased even if a prepared statement argument is unknown or an
error occurred during execution. In other words, their values correspond to the number of requests
issued, not to the number of requests successfully completed. For example, because status variables
are initialized for each server startup and do not persist across restarts, the Com_shutdown variable that
tracks SHUTDOWN statements normally has a value of zero, but can be nonzero if SHUTDOWN statements
were executed but failed.

The Com_stmt_xxx status variables are as follows:

• Com_stmt_prepare

• Com_stmt_execute

• Com_stmt_fetch

• Com_stmt_send_long_data

• Com_stmt_reset

• Com_stmt_close

Those variables stand for prepared statement commands. Their names refer to the COM_xxx command
set used in the network layer. In other words, their values increase whenever prepared statement
API calls such as mysql_stmt_prepare(), mysql_stmt_execute(), and so forth are executed.
However, Com_stmt_prepare, Com_stmt_execute and Com_stmt_close also increase for
PREPARE, EXECUTE, or DEALLOCATE PREPARE, respectively. Additionally, the values of the older
statement counter variables Com_prepare_sql, Com_execute_sql, and Com_dealloc_sql

911

Server Status Variables

increase for the PREPARE, EXECUTE, and DEALLOCATE PREPARE statements. Com_stmt_fetch
stands for the total number of network round-trips issued when fetching from cursors.

Com_stmt_reprepare indicates the number of times statements were automatically reprepared by the
server after metadata changes to tables or views referred to by the statement. A reprepare operation
increments Com_stmt_reprepare, and also Com_stmt_prepare.

Com_explain_other indicates the number of EXPLAIN FOR CONNECTION statements executed. See
Section 8.8.4, “Obtaining Execution Plan Information for a Named Connection”.

Com_change_repl_filter indicates the number of CHANGE REPLICATION FILTER statements
executed.

• Compression

Whether the client connection uses compression in the client/server protocol.

• Connection_errors_xxx

These variables provide information about errors that occur during the client connection process.
They are global only and represent error counts aggregated across connections from all hosts. These
variables track errors not accounted for by the host cache (see Section 5.1.11.2, “DNS Lookups and
the Host Cache”), such as errors that are not associated with TCP connections, occur very early in the
connection process (even before an IP address is known), or are not specific to any particular IP address
(such as out-of-memory conditions).

As of MySQL 5.7.3, the Connection_errors_xxx status variables are not visible in the embedded
server because for that server they are not updated and are not meaningful.

• Connection_errors_accept

The number of errors that occurred during calls to accept() on the listening port.

• Connection_errors_internal

The number of connections refused due to internal errors in the server, such as failure to start a new
thread or an out-of-memory condition.

• Connection_errors_max_connections

The number of connections refused because the server max_connections limit was reached.

• Connection_errors_peer_address

The number of errors that occurred while searching for connecting client IP addresses.

• Connection_errors_select

The number of errors that occurred during calls to select() or poll() on the listening port. (Failure
of this operation does not necessarily means a client connection was rejected.)

• Connection_errors_tcpwrap

The number of connections refused by the libwrap library.

• Connections

The number of connection attempts (successful or not) to the MySQL server.

912

Server Status Variables

• Created_tmp_disk_tables

The number of internal on-disk temporary tables created by the server while executing statements.

You can compare the number of internal on-disk temporary tables created to the total number of internal
temporary tables created by comparing Created_tmp_disk_tables and Created_tmp_tables
values.

See also Section 8.4.4, “Internal Temporary Table Use in MySQL”.

• Created_tmp_files

How many temporary files mysqld has created.

• Created_tmp_tables

The number of internal temporary tables created by the server while executing statements.

You can compare the number of internal on-disk temporary tables created to the total number of internal
temporary tables created by comparing Created_tmp_disk_tables and Created_tmp_tables
values.

See also Section 8.4.4, “Internal Temporary Table Use in MySQL”.

Each invocation of the SHOW STATUS statement uses an internal temporary table and increments the
global Created_tmp_tables value.

• Delayed_errors

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed
in a future release.

• Delayed_insert_threads

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed
in a future release.

• Delayed_writes

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed
in a future release.

• Flush_commands

The number of times the server flushes tables, whether because a user executed a FLUSH TABLES
statement or due to internal server operation. It is also incremented by receipt of a COM_REFRESH
packet. This is in contrast to Com_flush, which indicates how many FLUSH statements have been
executed, whether FLUSH TABLES, FLUSH LOGS, and so forth.

• group_replication_primary_member

Shows the primary member's UUID when the group is operating in single-primary mode. If the group is
operating in multi-primary mode, shows an empty string.

• Handler_commit

The number of internal COMMIT statements.

• Handler_delete

913

Server Status Variables

The number of times that rows have been deleted from tables.

• Handler_external_lock

The server increments this variable for each call to its external_lock() function, which generally
occurs at the beginning and end of access to a table instance. There might be differences among
storage engines. This variable can be used, for example, to discover for a statement that accesses a
partitioned table how many partitions were pruned before locking occurred: Check how much the counter
increased for the statement, subtract 2 (2 calls for the table itself), then divide by 2 to get the number of
partitions locked.

• Handler_mrr_init

The number of times the server uses a storage engine's own Multi-Range Read implementation for table
access.

• Handler_prepare

A counter for the prepare phase of two-phase commit operations.

• Handler_read_first

The number of times the first entry in an index was read. If this value is high, it suggests that the server
is doing a lot of full index scans (for example, SELECT col1 FROM foo, assuming that col1 is
indexed).

• Handler_read_key

The number of requests to read a row based on a key. If this value is high, it is a good indication that
your tables are properly indexed for your queries.

• Handler_read_last

The number of requests to read the last key in an index. With ORDER BY, the server issues a first-key
request followed by several next-key requests, whereas with ORDER BY DESC, the server issues a last-
key request followed by several previous-key requests.

• Handler_read_next

The number of requests to read the next row in key order. This value is incremented if you are querying
an index column with a range constraint or if you are doing an index scan.

• Handler_read_prev

The number of requests to read the previous row in key order. This read method is mainly used to
optimize ORDER BY ... DESC.

• Handler_read_rnd

The number of requests to read a row based on a fixed position. This value is high if you are doing a
lot of queries that require sorting of the result. You probably have a lot of queries that require MySQL to
scan entire tables or you have joins that do not use keys properly.

• Handler_read_rnd_next

The number of requests to read the next row in the data file. This value is high if you are doing a lot of
table scans. Generally this suggests that your tables are not properly indexed or that your queries are
not written to take advantage of the indexes you have.

914

Server Status Variables

• Handler_rollback

The number of requests for a storage engine to perform a rollback operation.

• Handler_savepoint

The number of requests for a storage engine to place a savepoint.

• Handler_savepoint_rollback

The number of requests for a storage engine to roll back to a savepoint.

• Handler_update

The number of requests to update a row in a table.

• Handler_write

The number of requests to insert a row in a table.

• Innodb_available_undo_logs

Note

The Innodb_available_undo_logs status variable is deprecated as of
MySQL 5.7.19; expect it to be removed in a future release.

The total number of available InnoDB rollback segments. Supplements the
innodb_rollback_segments system variable, which defines the number of active rollback segments.

One rollback segment always resides in the system tablespace, and 32 rollback segments are reserved
for use by temporary tables and are hosted in the temporary tablespace (ibtmp1). See Section 14.6.7,
“Undo Logs”.

If you initiate a MySQL instance with 32 or fewer rollback segments, InnoDB still assigns one rollback
segment to the system tablespace and 32 rollback segments to the temporary tablespace. In this case,
Innodb_available_undo_logs reports 33 available rollback segments even though the instance
was initialized with a lesser innodb_rollback_segments value.

• Innodb_buffer_pool_dump_status

The progress of an operation to record the pages held in the InnoDB buffer pool, triggered by the setting
of innodb_buffer_pool_dump_at_shutdown or innodb_buffer_pool_dump_now.

For related information and examples, see Section 14.8.3.6, “Saving and Restoring the Buffer Pool
State”.

• Innodb_buffer_pool_load_status

The progress of an operation to warm up the InnoDB buffer pool by reading in a
set of pages corresponding to an earlier point in time, triggered by the setting of
innodb_buffer_pool_load_at_startup or innodb_buffer_pool_load_now. If the operation
introduces too much overhead, you can cancel it by setting innodb_buffer_pool_load_abort.

For related information and examples, see Section 14.8.3.6, “Saving and Restoring the Buffer Pool
State”.

• Innodb_buffer_pool_bytes_data

915

Server Status Variables

The total number of bytes in the InnoDB buffer pool containing data. The number includes
both dirty and clean pages. For more accurate memory usage calculations than with
Innodb_buffer_pool_pages_data, when compressed tables cause the buffer pool to hold pages of
different sizes.

• Innodb_buffer_pool_pages_data

The number of pages in the InnoDB buffer pool containing data. The number includes both dirty and
clean pages. When using compressed tables, the reported Innodb_buffer_pool_pages_data value
may be larger than Innodb_buffer_pool_pages_total (Bug #59550).

• Innodb_buffer_pool_bytes_dirty

The total current number of bytes held in dirty pages in the InnoDB buffer pool. For more accurate
memory usage calculations than with Innodb_buffer_pool_pages_dirty, when compressed tables
cause the buffer pool to hold pages of different sizes.

• Innodb_buffer_pool_pages_dirty

The current number of dirty pages in the InnoDB buffer pool.

• Innodb_buffer_pool_pages_flushed

The number of requests to flush pages from the InnoDB buffer pool.

• Innodb_buffer_pool_pages_free

The number of free pages in the InnoDB buffer pool.

• Innodb_buffer_pool_pages_latched

The number of latched pages in the InnoDB buffer pool. These are pages currently being read or
written, or that cannot be flushed or removed for some other reason. Calculation of this variable is
expensive, so it is available only when the UNIV_DEBUG system is defined at server build time.

• Innodb_buffer_pool_pages_misc

The number of pages in the InnoDB buffer pool that are busy because they have
been allocated for administrative overhead, such as row locks or the adaptive hash
index. This value can also be calculated as Innodb_buffer_pool_pages_total −
Innodb_buffer_pool_pages_free − Innodb_buffer_pool_pages_data. When using
compressed tables, Innodb_buffer_pool_pages_misc may report an out-of-bounds value (Bug
#59550).

• Innodb_buffer_pool_pages_total

The total size of the InnoDB buffer pool, in pages. When using compressed tables,
the reported Innodb_buffer_pool_pages_data value may be larger than
Innodb_buffer_pool_pages_total (Bug #59550)

• Innodb_buffer_pool_read_ahead

The number of pages read into the InnoDB buffer pool by the read-ahead background thread.

• Innodb_buffer_pool_read_ahead_evicted

The number of pages read into the InnoDB buffer pool by the read-ahead background thread that were
subsequently evicted without having been accessed by queries.

916

Server Status Variables

• Innodb_buffer_pool_read_ahead_rnd

The number of “random” read-aheads initiated by InnoDB. This happens when a query scans a large
portion of a table but in random order.

• Innodb_buffer_pool_read_requests

The number of logical read requests.

• Innodb_buffer_pool_reads

The number of logical reads that InnoDB could not satisfy from the buffer pool, and had to read directly
from disk.

• Innodb_buffer_pool_resize_status

The status of an operation to resize the InnoDB buffer pool dynamically, triggered by setting the
innodb_buffer_pool_size parameter dynamically. The innodb_buffer_pool_size parameter
is dynamic, which allows you to resize the buffer pool without restarting the server. See Configuring
InnoDB Buffer Pool Size Online for related information.

• Innodb_buffer_pool_wait_free

Normally, writes to the InnoDB buffer pool happen in the background. When InnoDB needs to read or
create a page and no clean pages are available, InnoDB flushes some dirty pages first and waits for that
operation to finish. This counter counts instances of these waits. If innodb_buffer_pool_size has
been set properly, this value should be small.

• Innodb_buffer_pool_write_requests

The number of writes done to the InnoDB buffer pool.

• Innodb_data_fsyncs

The number of fsync() operations so far. The frequency of fsync() calls is influenced by the setting
of the innodb_flush_method configuration option.

• Innodb_data_pending_fsyncs

The current number of pending fsync() operations. The frequency of fsync() calls is influenced by
the setting of the innodb_flush_method configuration option.

• Innodb_data_pending_reads

The current number of pending reads.

• Innodb_data_pending_writes

The current number of pending writes.

• Innodb_data_read

The amount of data read since the server was started (in bytes).

• Innodb_data_reads

The total number of data reads (OS file reads).

• Innodb_data_writes

917

Server Status Variables

The total number of data writes.

• Innodb_data_written

The amount of data written so far, in bytes.

• Innodb_dblwr_pages_written

The number of pages that have been written to the doublewrite buffer. See Section 14.12.1, “InnoDB
Disk I/O”.

• Innodb_dblwr_writes

The number of doublewrite operations that have been performed. See Section 14.12.1, “InnoDB Disk I/
O”.

• Innodb_have_atomic_builtins

Indicates whether the server was built with atomic instructions.

• Innodb_log_waits

The number of times that the log buffer was too small and a wait was required for it to be flushed before
continuing.

• Innodb_log_write_requests

The number of write requests for the InnoDB redo log.

• Innodb_log_writes

The number of physical writes to the InnoDB redo log file.

• Innodb_num_open_files

The number of files InnoDB currently holds open.

• Innodb_os_log_fsyncs

The number of fsync() writes done to the InnoDB redo log files.

• Innodb_os_log_pending_fsyncs

The number of pending fsync() operations for the InnoDB redo log files.

• Innodb_os_log_pending_writes

The number of pending writes to the InnoDB redo log files.

• Innodb_os_log_written

The number of bytes written to the InnoDB redo log files.

• Innodb_page_size

InnoDB page size (default 16KB). Many values are counted in pages; the page size enables them to be
easily converted to bytes.

• Innodb_pages_created

918

Server Status Variables

The number of pages created by operations on InnoDB tables.

• Innodb_pages_read

The number of pages read from the InnoDB buffer pool by operations on InnoDB tables.

• Innodb_pages_written

The number of pages written by operations on InnoDB tables.

• Innodb_row_lock_current_waits

The number of row locks currently being waited for by operations on InnoDB tables.

• Innodb_row_lock_time

The total time spent in acquiring row locks for InnoDB tables, in milliseconds.

• Innodb_row_lock_time_avg

The average time to acquire a row lock for InnoDB tables, in milliseconds.

• Innodb_row_lock_time_max

The maximum time to acquire a row lock for InnoDB tables, in milliseconds.

• Innodb_row_lock_waits

The number of times operations on InnoDB tables had to wait for a row lock.

• Innodb_rows_deleted

The number of rows deleted from InnoDB tables.

• Innodb_rows_inserted

The number of rows inserted into InnoDB tables.

• Innodb_rows_read

The number of rows read from InnoDB tables.

• Innodb_rows_updated

The estimated number of rows updated in InnoDB tables.

Note

This value is not meant to be 100% accurate. For an accurate (but more
expensive) result, use ROW_COUNT().

• Innodb_truncated_status_writes

The number of times output from the SHOW ENGINE INNODB STATUS statement has been truncated.

• Key_blocks_not_flushed

The number of key blocks in the MyISAM key cache that have changed but have not yet been flushed to
disk.

919

Server Status Variables

• Key_blocks_unused

The number of unused blocks in the MyISAM key cache. You can use this value to determine how much
of the key cache is in use; see the discussion of key_buffer_size in Section 5.1.7, “Server System
Variables”.

• Key_blocks_used

The number of used blocks in the MyISAM key cache. This value is a high-water mark that indicates the
maximum number of blocks that have ever been in use at one time.

• Key_read_requests

The number of requests to read a key block from the MyISAM key cache.

• Key_reads

The number of physical reads of a key block from disk into the MyISAM key cache. If Key_reads is
large, then your key_buffer_size value is probably too small. The cache miss rate can be calculated
as Key_reads/Key_read_requests.

• Key_write_requests

The number of requests to write a key block to the MyISAM key cache.

• Key_writes

The number of physical writes of a key block from the MyISAM key cache to disk.

• Last_query_cost

The total cost of the last compiled query as computed by the query optimizer. This is useful for
comparing the cost of different query plans for the same query. The default value of 0 means that no
query has been compiled yet. The default value is 0. Last_query_cost has session scope.

Last_query_cost can be computed accurately only for simple, “flat” queries, but not for complex
queries such as those containing subqueries or UNION. For the latter, the value is set to 0.

• Last_query_partial_plans

The number of iterations the query optimizer made in execution plan construction for the previous query.

Last_query_partial_plans has session scope.

• Locked_connects

The number of attempts to connect to locked user accounts. For information about account locking and
unlocking, see Section 6.2.15, “Account Locking”.

• Max_execution_time_exceeded

The number of SELECT statements for which the execution timeout was exceeded.

• Max_execution_time_set

The number of SELECT statements for which a nonzero execution timeout was set. This includes
statements that include a nonzero MAX_EXECUTION_TIME optimizer hint, and statements that include
no such hint but execute while the timeout indicated by the max_execution_time system variable is
nonzero.

920

Server Status Variables

• Max_execution_time_set_failed

The number of SELECT statements for which the attempt to set an execution timeout failed.

• Max_used_connections

The maximum number of connections that have been in use simultaneously since the server started.

• Max_used_connections_time

The time at which Max_used_connections reached its current value.

• Not_flushed_delayed_rows

This status variable is deprecated (because DELAYED inserts are not supported); expect it to be removed
in a future release.

• mecab_charset

The character set currently used by the MeCab full-text parser plugin. For related information, see
Section 12.9.9, “MeCab Full-Text Parser Plugin”.

• Ongoing_anonymous_transaction_count

Shows the number of ongoing transactions which have been marked as anonymous. This can be used
to ensure that no further transactions are waiting to be processed.

• Ongoing_anonymous_gtid_violating_transaction_count

This status variable is only available in debug builds. Shows the number of ongoing transactions which
use gtid_next=ANONYMOUS and that violate GTID consistency.

• Ongoing_automatic_gtid_violating_transaction_count

This status variable is only available in debug builds. Shows the number of ongoing transactions which
use gtid_next=AUTOMATIC and that violate GTID consistency.

• Open_files

The number of files that are open. This count includes regular files opened by the server. It does not
include other types of files such as sockets or pipes. Also, the count does not include files that storage
engines open using their own internal functions rather than asking the server level to do so.

• Open_streams

The number of streams that are open (used mainly for logging).

• Open_table_definitions

The number of cached .frm files.

• Open_tables

The number of tables that are open.

• Opened_files

The number of files that have been opened with my_open() (a mysys library function). Parts of the
server that open files without using this function do not increment the count.

921

Server Status Variables

• Opened_table_definitions

The number of .frm files that have been cached.

• Opened_tables

The number of tables that have been opened. If Opened_tables is big, your table_open_cache
value is probably too small.

• Performance_schema_xxx

Performance Schema status variables are listed in Section 25.16, “Performance Schema Status
Variables”. These variables provide information about instrumentation that could not be loaded or
created due to memory constraints.

• Prepared_stmt_count

The current number of prepared statements. (The maximum number of statements is given by the
max_prepared_stmt_count system variable.)

• Qcache_free_blocks

The number of free memory blocks in the query cache.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_free_blocks.

• Qcache_free_memory

The amount of free memory for the query cache.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_free_memory.

• Qcache_hits

The number of query cache hits.

The discussion at the beginning of this section indicates how to relate this statement-counting status
variable to other such variables.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_hits.

• Qcache_inserts

The number of queries added to the query cache.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_inserts.

922

Server Status Variables

• Qcache_lowmem_prunes

The number of queries that were deleted from the query cache because of low memory.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_lowmem_prunes.

• Qcache_not_cached

The number of noncached queries (not cacheable, or not cached due to the query_cache_type
setting).

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_not_cached.

• Qcache_queries_in_cache

The number of queries registered in the query cache.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_queries_in_cache.

• Qcache_total_blocks

The total number of blocks in the query cache.

Note

The query cache is deprecated as of MySQL 5.7.20, and is removed in MySQL
8.0. Deprecation includes Qcache_total_blocks.

• Queries

The number of statements executed by the server. This variable includes statements executed within
stored programs, unlike the Questions variable. It does not count COM_PING or COM_STATISTICS
commands.

The discussion at the beginning of this section indicates how to relate this statement-counting status
variable to other such variables.

• Questions

The number of statements executed by the server. This includes only statements sent to the server
by clients and not statements executed within stored programs, unlike the Queries variable. This
variable does not count COM_PING, COM_STATISTICS, COM_STMT_PREPARE, COM_STMT_CLOSE, or
COM_STMT_RESET commands.

The discussion at the beginning of this section indicates how to relate this statement-counting status
variable to other such variables.

923

Server Status Variables

• Rpl_semi_sync_master_clients

The number of semisynchronous replicas.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_net_avg_wait_time

The average time in microseconds the source waited for a replica reply. This variable is deprecated,
always 0; expect it to be in a future version.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_net_wait_time

The total time in microseconds the source waited for replica replies. This variable is deprecated, and is
always 0; expect it to be removed in a future version.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_net_waits

The total number of times the source waited for replica replies.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_no_times

The number of times the source turned off semisynchronous replication.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_no_tx

The number of commits that were not acknowledged successfully by a replica.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_status

Whether semisynchronous replication currently is operational on the source. The value is ON if the plugin
has been enabled and a commit acknowledgment has occurred. It is OFF if the plugin is not enabled or
the source has fallen back to asynchronous replication due to commit acknowledgment timeout.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_timefunc_failures

The number of times the source failed when calling time functions such as gettimeofday().

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_tx_avg_wait_time

The average time in microseconds the source waited for each transaction.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_tx_wait_time

924

Server Status Variables

The total time in microseconds the source waited for transactions.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_tx_waits

The total number of times the source waited for transactions.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_wait_pos_backtraverse

The total number of times the source waited for an event with binary coordinates lower than events
waited for previously. This can occur when the order in which transactions start waiting for a reply is
different from the order in which their binary log events are written.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_wait_sessions

The number of sessions currently waiting for replica replies.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_master_yes_tx

The number of commits that were acknowledged successfully by a replica.

This variable is available only if the source-side semisynchronous replication plugin is installed.

• Rpl_semi_sync_slave_status

Whether semisynchronous replication currently is operational on the replica. This is ON if the plugin has
been enabled and the replica I/O thread is running, OFF otherwise.

This variable is available only if the replica-side semisynchronous replication plugin is installed.

• Rsa_public_key

This variable is available if MySQL was compiled using OpenSSL (see Section 6.3.4, “SSL
Library-Dependent Capabilities”). Its value is the public key used by the sha256_password
authentication plugin for RSA key pair-based password exchange. The value is nonempty
only if the server successfully initializes the private and public keys in the files named by the
sha256_password_private_key_path and sha256_password_public_key_path system
variables. The value of Rsa_public_key comes from the latter file.

For information about sha256_password, see Section 6.4.1.5, “SHA-256 Pluggable Authentication”.

• Select_full_join

The number of joins that perform table scans because they do not use indexes. If this value is not 0, you
should carefully check the indexes of your tables.

• Select_full_range_join

The number of joins that used a range search on a reference table.

• Select_range

925

Server Status Variables

The number of joins that used ranges on the first table. This is normally not a critical issue even if the
value is quite large.

• Select_range_check

The number of joins without keys that check for key usage after each row. If this is not 0, you should
carefully check the indexes of your tables.

• Select_scan

The number of joins that did a full scan of the first table.

• Slave_heartbeat_period

Shows the replication heartbeat interval (in seconds) on a replication replica.

This variable is affected by the value of the show_compatibility_56 system variable. For details,
see Effect of show_compatibility_56 on Slave Status Variables.

Note

This variable only shows the status of the default replication channel. To
monitor any replication channel, use the HEARTBEAT_INTERVAL column in the
replication_connection_configuration table for the replication channel.
Slave_heartbeat_period is deprecated and is removed in MySQL 8.0.

• Slave_last_heartbeat

Shows when the most recent heartbeat signal was received by a replica, as a TIMESTAMP value.

This variable is affected by the value of the show_compatibility_56 system variable. For details,
see Effect of show_compatibility_56 on Slave Status Variables.

Note

This variable only shows the status of the default replication channel. To monitor
any replication channel, use the LAST_HEARTBEAT_TIMESTAMP column in
the replication_connection_status table for the replication channel.
Slave_last_heartbeat is deprecated and is removed in MySQL 8.0.

• Slave_open_temp_tables

The number of temporary tables that the replica SQL thread currently has open. If the value is greater
than zero, it is not safe to shut down the replica; see Section 16.4.1.29, “Replication and Temporary
Tables”. This variable reports the total count of open temporary tables for all replication channels.

926

Server Status Variables

• Slave_received_heartbeats

This counter increments with each replication heartbeat received by a replication replica since the last
time that the replica was restarted or reset, or a CHANGE MASTER TO statement was issued.

This variable is affected by the value of the show_compatibility_56 system variable. For details,
see Effect of show_compatibility_56 on Slave Status Variables.

Note

This variable only shows the status of the default replication channel. To monitor
any replication channel, use the COUNT_RECEIVED_HEARTBEATS column in
the replication_connection_status table for the replication channel.
Slave_received_heartbeats is deprecated and is removed in MySQL 8.0.

• Slave_retried_transactions

The total number of times since startup that the replication replica SQL thread has retried transactions.

This variable is affected by the value of the show_compatibility_56 system variable. For details,
see Effect of show_compatibility_56 on Slave Status Variables.

Note

This variable only shows the status of the default replication channel. To monitor
any replication channel, use the COUNT_TRANSACTIONS_RETRIES column
in the replication_applier_status table for the replication channel.
Slave_retried_transactions is deprecated and is removed in MySQL 8.0.

• Slave_rows_last_search_algorithm_used

The search algorithm that was most recently used by this replica to locate rows for row-based
replication. The result shows whether the replica used indexes, a table scan, or hashing as the search
algorithm for the last transaction executed on any channel.

The method used depends on the setting for the slave_rows_search_algorithms system variable,
and the keys that are available on the relevant table.

This variable is available only for debug builds of MySQL.

• Slave_running

This is ON if this server is a replica that is connected to a replication source, and both the I/O and SQL
threads are running; otherwise, it is OFF.

This variable is affected by the value of the show_compatibility_56 system variable. For details,
see Effect of show_compatibility_56 on Slave Status Variables.

Note

This variable only shows the status of the default replication channel. To
monitor any replication channel, use the SERVICE_STATE column in the
replication_applier_status or replication_connection_status
tables of the replication channel. Slave_running is deprecated and is removed
in MySQL 8.0.

927

Server Status Variables

• Slow_launch_threads

The number of threads that have taken more than slow_launch_time seconds to create.

This variable is not meaningful in the embedded server (libmysqld) and as of MySQL 5.7.2 is no
longer visible within the embedded server.

• Slow_queries

The number of queries that have taken more than long_query_time seconds. This counter
increments regardless of whether the slow query log is enabled. For information about that log, see
Section 5.4.5, “The Slow Query Log”.

• Sort_merge_passes

The number of merge passes that the sort algorithm has had to do. If this value is large, you should
consider increasing the value of the sort_buffer_size system variable.

• Sort_range

The number of sorts that were done using ranges.

• Sort_rows

The number of sorted rows.

• Sort_scan

The number of sorts that were done by scanning the table.

• Ssl_accept_renegotiates

The number of negotiates needed to establish the connection.

• Ssl_accepts

The number of accepted SSL connections.

• Ssl_callback_cache_hits

The number of callback cache hits.

• Ssl_cipher

The current encryption cipher (empty for unencrypted connections).

• Ssl_cipher_list

The list of possible SSL ciphers (empty for non-SSL connections).

• Ssl_client_connects

The number of SSL connection attempts to an SSL-enabled source.

• Ssl_connect_renegotiates

The number of negotiates needed to establish the connection to an SSL-enabled source.

• Ssl_ctx_verify_depth

928

Server Status Variables

The SSL context verification depth (how many certificates in the chain are tested).

• Ssl_ctx_verify_mode

The SSL context verification mode.

• Ssl_default_timeout

The default SSL timeout.

• Ssl_finished_accepts

The number of successful SSL connections to the server.

• Ssl_finished_connects

The number of successful replica connections to an SSL-enabled source.

• Ssl_server_not_after

The last date for which the SSL certificate is valid. To check SSL certificate expiration information, use
this statement:

mysql> SHOW STATUS LIKE 'Ssl_server_not%';
+-----------------------+--------------------------+
| Variable_name         | Value                    |
+-----------------------+--------------------------+
| Ssl_server_not_after  | Apr 28 14:16:39 2025 GMT |
| Ssl_server_not_before | May  1 14:16:39 2015 GMT |
+-----------------------+--------------------------+

• Ssl_server_not_before

The first date for which the SSL certificate is valid.

• Ssl_session_cache_hits

The number of SSL session cache hits.

• Ssl_session_cache_misses

The number of SSL session cache misses.

• Ssl_session_cache_mode

The SSL session cache mode.

• Ssl_session_cache_overflows

The number of SSL session cache overflows.

• Ssl_session_cache_size

The SSL session cache size.

• Ssl_session_cache_timeouts

The number of SSL session cache timeouts.

• Ssl_sessions_reused

929

Server Status Variables

This is equal to 0 if TLS was not used in the current MySQL session, or if a TLS session has not been
reused; otherwise it is equal to 1.

Ssl_sessions_reused has session scope.

• Ssl_used_session_cache_entries

How many SSL session cache entries were used.

• Ssl_verify_depth

The verification depth for replication SSL connections.

• Ssl_verify_mode

The verification mode used by the server for a connection that uses SSL. The value is a bitmask; bits are
defined in the openssl/ssl.h header file:

# define SSL_VERIFY_NONE                 0x00
# define SSL_VERIFY_PEER                 0x01
# define SSL_VERIFY_FAIL_IF_NO_PEER_CERT 0x02
# define SSL_VERIFY_CLIENT_ONCE          0x04

SSL_VERIFY_PEER indicates that the server asks for a client certificate. If the client supplies one, the
server performs verification and proceeds only if verification is successful. SSL_VERIFY_CLIENT_ONCE
indicates that a request for the client certificate is done only in the initial handshake.

• Ssl_version

The SSL protocol version of the connection (for example, TLSv1). If the connection is not encrypted, the
value is empty.

• Table_locks_immediate

The number of times that a request for a table lock could be granted immediately.

• Table_locks_waited

The number of times that a request for a table lock could not be granted immediately and a wait was
needed. If this is high and you have performance problems, you should first optimize your queries, and
then either split your table or tables or use replication.

• Table_open_cache_hits

The number of hits for open tables cache lookups.

• Table_open_cache_misses

The number of misses for open tables cache lookups.

• Table_open_cache_overflows

The number of overflows for the open tables cache. This is the number of times, after a table is
opened or closed, a cache instance has an unused entry and the size of the instance is larger than
table_open_cache / table_open_cache_instances.

930

Server SQL Modes

• Tc_log_max_pages_used

For the memory-mapped implementation of the log that is used by mysqld when it acts as the
transaction coordinator for recovery of internal XA transactions, this variable indicates the largest
number of pages used for the log since the server started. If the product of Tc_log_max_pages_used
and Tc_log_page_size is always significantly less than the log size, the size is larger than necessary
and can be reduced. (The size is set by the --log-tc-size option. This variable is unused: It is
unneeded for binary log-based recovery, and the memory-mapped recovery log method is not used
unless the number of storage engines that are capable of two-phase commit and that support XA
transactions is greater than one. (InnoDB is the only applicable engine.)

• Tc_log_page_size

The page size used for the memory-mapped implementation of the XA recovery log. The default value
is determined using getpagesize(). This variable is unused for the same reasons as described for
Tc_log_max_pages_used.

• Tc_log_page_waits

For the memory-mapped implementation of the recovery log, this variable increments each time the
server was not able to commit a transaction and had to wait for a free page in the log. If this value is
large, you might want to increase the log size (with the --log-tc-size option). For binary log-based
recovery, this variable increments each time the binary log cannot be closed because there are two-
phase commits in progress. (The close operation waits until all such transactions are finished.)

• Threads_cached

The number of threads in the thread cache.

This variable is not meaningful in the embedded server (libmysqld) and as of MySQL 5.7.2 is no
longer visible within the embedded server.

• Threads_connected

The number of currently open connections.

• Threads_created

The number of threads created to handle connections. If Threads_created is big, you may
want to increase the thread_cache_size value. The cache miss rate can be calculated as
Threads_created/Connections.

• Threads_running

The number of threads that are not sleeping.

• Uptime

The number of seconds that the server has been up.

• Uptime_since_flush_status

The number of seconds since the most recent FLUSH STATUS statement.

5.1.10 Server SQL Modes

The MySQL server can operate in different SQL modes, and can apply these modes differently for different
clients, depending on the value of the sql_mode system variable. DBAs can set the global SQL mode to

931

Server SQL Modes

match site server operating requirements, and each application can set its session SQL mode to its own
requirements.

Modes affect the SQL syntax MySQL supports and the data validation checks it performs. This makes it
easier to use MySQL in different environments and to use MySQL together with other database servers.

• Setting the SQL Mode

• The Most Important SQL Modes

• Full List of SQL Modes

• Combination SQL Modes

• Strict SQL Mode

• Comparison of the IGNORE Keyword and Strict SQL Mode

• SQL Mode Changes in MySQL 5.7

For answers to questions often asked about server SQL modes in MySQL, see Section A.3, “MySQL 5.7
FAQ: Server SQL Mode”.

When working with InnoDB tables, consider also the innodb_strict_mode system variable. It enables
additional error checks for InnoDB tables.

Setting the SQL Mode

The default SQL mode in MySQL 5.7 includes these modes: ONLY_FULL_GROUP_BY,
STRICT_TRANS_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE, ERROR_FOR_DIVISION_BY_ZERO,
NO_AUTO_CREATE_USER, and NO_ENGINE_SUBSTITUTION.

These modes were added to the default SQL mode in MySQL 5.7: The ONLY_FULL_GROUP_BY and
STRICT_TRANS_TABLES modes were added in MySQL 5.7.5. The NO_AUTO_CREATE_USER mode was
added in MySQL 5.7.7. The ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE
modes were added in MySQL 5.7.8. For additional discussion regarding these changes to the default SQL
mode value, see SQL Mode Changes in MySQL 5.7.

To set the SQL mode at server startup, use the --sql-mode="modes" option on the command line, or
sql-mode="modes" in an option file such as my.cnf (Unix operating systems) or my.ini (Windows).
modes is a list of different modes separated by commas. To clear the SQL mode explicitly, set it to an
empty string using --sql-mode="" on the command line, or sql-mode="" in an option file.

Note

MySQL installation programs may configure the SQL mode during the installation
process. If the SQL mode differs from the default or from what you expect, check for
a setting in an option file that the server reads at startup.

To change the SQL mode at runtime, set the global or session sql_mode system variable using a SET
statement:

SET GLOBAL sql_mode = 'modes';
SET SESSION sql_mode = 'modes';

Setting the GLOBAL variable requires the SUPER privilege and affects the operation of all clients that
connect from that time on. Setting the SESSION variable affects only the current client. Each client can
change its session sql_mode value at any time.

932

Server SQL Modes

To determine the current global or session sql_mode setting, select its value:

SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;

Important

SQL mode and user-defined partitioning.
after creating and inserting data into partitioned tables can cause major changes
in the behavior of such tables, and could lead to loss or corruption of data. It is
strongly recommended that you never change the SQL mode once you have
created tables employing user-defined partitioning.

 Changing the server SQL mode

When replicating partitioned tables, differing SQL modes on the source and replica
can also lead to problems. For best results, you should always use the same server
SQL mode on the source and replica.

For more information, see Section 22.6, “Restrictions and Limitations on
Partitioning”.

The Most Important SQL Modes

The most important sql_mode values are probably these:

•   ANSI

This mode changes syntax and behavior to conform more closely to standard SQL. It is one of the
special combination modes listed at the end of this section.

•   STRICT_TRANS_TABLES

If a value could not be inserted as given into a transactional table, abort the statement. For a
nontransactional table, abort the statement if the value occurs in a single-row statement or the first row
of a multiple-row statement. More details are given later in this section.

As of MySQL 5.7.5, the default SQL mode includes STRICT_TRANS_TABLES.

•   TRADITIONAL

Make MySQL behave like a “traditional” SQL database system. A simple description of this mode is “give
an error instead of a warning” when inserting an incorrect value into a column. It is one of the special
combination modes listed at the end of this section.

Note

With TRADITIONAL mode enabled, an INSERT or UPDATE aborts as soon as an
error occurs. If you are using a nontransactional storage engine, this may not be
what you want because data changes made prior to the error may not be rolled
back, resulting in a “partially done” update.

When this manual refers to “strict mode,” it means a mode with either or both STRICT_TRANS_TABLES or
STRICT_ALL_TABLES enabled.

Full List of SQL Modes

The following list describes all supported SQL modes:

• ALLOW_INVALID_DATES

933

Server SQL Modes

Do not perform full checking of dates. Check only that the month is in the range from 1 to 12 and the day
is in the range from 1 to 31. This may be useful for Web applications that obtain year, month, and day in
three different fields and store exactly what the user inserted, without date validation. This mode applies
to DATE and DATETIME columns. It does not apply to TIMESTAMP columns, which always require a valid
date.

With ALLOW_INVALID_DATES disabled, the server requires that month and day values be legal, and
not merely in the range 1 to 12 and 1 to 31, respectively. With strict mode disabled, invalid dates such as
'2004-04-31' are converted to '0000-00-00' and a warning is generated. With strict mode enabled,
invalid dates generate an error. To permit such dates, enable ALLOW_INVALID_DATES.

• ANSI_QUOTES

Treat " as an identifier quote character (like the ` quote character) and not as a string quote character.
You can still use ` to quote identifiers with this mode enabled. With ANSI_QUOTES enabled, you cannot
use double quotation marks to quote literal strings because they are interpreted as identifiers.

• ERROR_FOR_DIVISION_BY_ZERO

The ERROR_FOR_DIVISION_BY_ZERO mode affects handling of division by zero, which includes
MOD(N,0). For data-change operations (INSERT, UPDATE), its effect also depends on whether strict
SQL mode is enabled.

• If this mode is not enabled, division by zero inserts NULL and produces no warning.

• If this mode is enabled, division by zero inserts NULL and produces a warning.

• If this mode and strict mode are enabled, division by zero produces an error, unless IGNORE is given
as well. For INSERT IGNORE and UPDATE IGNORE, division by zero inserts NULL and produces a
warning.

For SELECT, division by zero returns NULL. Enabling ERROR_FOR_DIVISION_BY_ZERO causes a
warning to be produced as well, regardless of whether strict mode is enabled.

ERROR_FOR_DIVISION_BY_ZERO is deprecated. ERROR_FOR_DIVISION_BY_ZERO is not part of strict
mode, but should be used in conjunction with strict mode and is enabled by default. A warning occurs
if ERROR_FOR_DIVISION_BY_ZERO is enabled without also enabling strict mode or vice versa. For
additional discussion, see SQL Mode Changes in MySQL 5.7.

Because ERROR_FOR_DIVISION_BY_ZERO is deprecated; expect it to be removed in a future release of
MySQL as a separate mode name and its effect included in the effects of strict SQL mode.

• HIGH_NOT_PRECEDENCE

The precedence of the NOT operator is such that expressions such as NOT a BETWEEN b AND c are
parsed as NOT (a BETWEEN b AND c). In some older versions of MySQL, the expression was parsed
as (NOT a) BETWEEN b AND c. The old higher-precedence behavior can be obtained by enabling the
HIGH_NOT_PRECEDENCE SQL mode.

mysql> SET sql_mode = '';
mysql> SELECT NOT 1 BETWEEN -5 AND 5;
        -> 0
mysql> SET sql_mode = 'HIGH_NOT_PRECEDENCE';
mysql> SELECT NOT 1 BETWEEN -5 AND 5;
        -> 1

• IGNORE_SPACE

934

Server SQL Modes

Permit spaces between a function name and the ( character. This causes built-in function names to
be treated as reserved words. As a result, identifiers that are the same as function names must be
quoted as described in Section 9.2, “Schema Object Names”. For example, because there is a COUNT()
function, the use of count as a table name in the following statement causes an error:

mysql> CREATE TABLE count (i INT);
ERROR 1064 (42000): You have an error in your SQL syntax

The table name should be quoted:

mysql> CREATE TABLE `count` (i INT);
Query OK, 0 rows affected (0.00 sec)

The IGNORE_SPACE SQL mode applies to built-in functions, not to loadable functions or stored
functions. It is always permissible to have spaces after a loadable function or stored function name,
regardless of whether IGNORE_SPACE is enabled.

For further discussion of IGNORE_SPACE, see Section 9.2.5, “Function Name Parsing and Resolution”.

• NO_AUTO_CREATE_USER

Prevent the GRANT statement from automatically creating new user accounts if it would otherwise do so,
unless authentication information is specified. The statement must specify a nonempty password using
IDENTIFIED BY or an authentication plugin using IDENTIFIED WITH.

It is preferable to create MySQL accounts with CREATE USER rather than GRANT.
NO_AUTO_CREATE_USER is deprecated and the default SQL mode includes NO_AUTO_CREATE_USER.
Assignments to sql_mode that change the NO_AUTO_CREATE_USER mode state produce a warning,
except assignments that set sql_mode to DEFAULT. Expect NO_AUTO_CREATE_USER to be be
removed in a future release of MySQL, and its effect to be enabled at all times (and for GRANT not to
create accounts any longer).

Previously, before NO_AUTO_CREATE_USER was deprecated, one reason not to enable it was that it
was not replication safe. Now it can be enabled and replication-safe user management performed with
CREATE USER IF NOT EXISTS, DROP USER IF EXISTS, and ALTER USER IF EXISTS rather
than GRANT. These statements enable safe replication when replicas may have different grants than
those on the source. See Section 13.7.1.2, “CREATE USER Statement”, Section 13.7.1.3, “DROP
USER Statement”, and Section 13.7.1.1, “ALTER USER Statement”.

• NO_AUTO_VALUE_ON_ZERO

NO_AUTO_VALUE_ON_ZERO affects handling of AUTO_INCREMENT columns. Normally, you generate the
next sequence number for the column by inserting either NULL or 0 into it. NO_AUTO_VALUE_ON_ZERO
suppresses this behavior for 0 so that only NULL generates the next sequence number.

This mode can be useful if 0 has been stored in a table's AUTO_INCREMENT column. (Storing 0 is not
a recommended practice, by the way.) For example, if you dump the table with mysqldump and then
reload it, MySQL normally generates new sequence numbers when it encounters the 0 values, resulting
in a table with contents different from the one that was dumped. Enabling NO_AUTO_VALUE_ON_ZERO
before reloading the dump file solves this problem. For this reason, mysqldump automatically includes in
its output a statement that enables NO_AUTO_VALUE_ON_ZERO.

935

Server SQL Modes

• NO_BACKSLASH_ESCAPES

Enabling this mode disables the use of the backslash character (\) as an escape character within strings
and identifiers. With this mode enabled, backslash becomes an ordinary character like any other, and
the default escape sequence for LIKE expressions is changed so that no escape character is used.

• NO_DIR_IN_CREATE

When creating a table, ignore all INDEX DIRECTORY and DATA DIRECTORY directives. This option is
useful on replica replication servers.

• NO_ENGINE_SUBSTITUTION

Control automatic substitution of the default storage engine when a statement such as CREATE TABLE
or ALTER TABLE specifies a storage engine that is disabled or not compiled in.

By default, NO_ENGINE_SUBSTITUTION is enabled.

Because storage engines can be pluggable at runtime, unavailable engines are treated the same way:

With NO_ENGINE_SUBSTITUTION disabled, for CREATE TABLE the default engine is used and a
warning occurs if the desired engine is unavailable. For ALTER TABLE, a warning occurs and the table
is not altered.

With NO_ENGINE_SUBSTITUTION enabled, an error occurs and the table is not created or altered if the
desired engine is unavailable.

• NO_FIELD_OPTIONS

Do not print MySQL-specific column options in the output of SHOW CREATE TABLE. This mode is used
by mysqldump in portability mode.

Note

As of MySQL 5.7.22, NO_FIELD_OPTIONS is deprecated. It is removed in
MySQL 8.0.

• NO_KEY_OPTIONS

Do not print MySQL-specific index options in the output of SHOW CREATE TABLE. This mode is used by
mysqldump in portability mode.

Note

As of MySQL 5.7.22, NO_KEY_OPTIONS is deprecated. It is removed in MySQL
8.0.

• NO_TABLE_OPTIONS

Do not print MySQL-specific table options (such as ENGINE) in the output of SHOW CREATE TABLE.
This mode is used by mysqldump in portability mode.

Note

As of MySQL 5.7.22, NO_TABLE_OPTIONS is deprecated. It is removed in
MySQL 8.0.

• NO_UNSIGNED_SUBTRACTION

936

Server SQL Modes

Subtraction between integer values, where one is of type UNSIGNED, produces an unsigned result by
default. If the result would otherwise have been negative, an error results:

mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT CAST(0 AS UNSIGNED) - 1;
ERROR 1690 (22003): BIGINT UNSIGNED value is out of range in '(cast(0 as unsigned) - 1)'

If the NO_UNSIGNED_SUBTRACTION SQL mode is enabled, the result is negative:

mysql> SET sql_mode = 'NO_UNSIGNED_SUBTRACTION';
mysql> SELECT CAST(0 AS UNSIGNED) - 1;
+-------------------------+
| CAST(0 AS UNSIGNED) - 1 |
+-------------------------+
|                      -1 |
+-------------------------+

If the result of such an operation is used to update an UNSIGNED integer column, the result is clipped
to the maximum value for the column type, or clipped to 0 if NO_UNSIGNED_SUBTRACTION is enabled.
With strict SQL mode enabled, an error occurs and the column remains unchanged.

When NO_UNSIGNED_SUBTRACTION is enabled, the subtraction result is signed, even if any operand is
unsigned. For example, compare the type of column c2 in table t1 with that of column c2 in table t2:

mysql> SET sql_mode='';
mysql> CREATE TABLE test (c1 BIGINT UNSIGNED NOT NULL);
mysql> CREATE TABLE t1 SELECT c1 - 1 AS c2 FROM test;
mysql> DESCRIBE t1;
+-------+---------------------+------+-----+---------+-------+
| Field | Type                | Null | Key | Default | Extra |
+-------+---------------------+------+-----+---------+-------+
| c2    | bigint(21) unsigned | NO   |     | 0       |       |
+-------+---------------------+------+-----+---------+-------+

mysql> SET sql_mode='NO_UNSIGNED_SUBTRACTION';
mysql> CREATE TABLE t2 SELECT c1 - 1 AS c2 FROM test;
mysql> DESCRIBE t2;
+-------+------------+------+-----+---------+-------+
| Field | Type       | Null | Key | Default | Extra |
+-------+------------+------+-----+---------+-------+
| c2    | bigint(21) | NO   |     | 0       |       |
+-------+------------+------+-----+---------+-------+

This means that BIGINT UNSIGNED is not 100% usable in all contexts. See Section 12.10, “Cast
Functions and Operators”.

937

Server SQL Modes

• NO_ZERO_DATE

The NO_ZERO_DATE mode affects whether the server permits '0000-00-00' as a valid date. Its effect
also depends on whether strict SQL mode is enabled.

• If this mode is not enabled, '0000-00-00' is permitted and inserts produce no warning.

• If this mode is enabled, '0000-00-00' is permitted and inserts produce a warning.

• If this mode and strict mode are enabled, '0000-00-00' is not permitted and inserts produce an

error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, '0000-00-00' is
permitted and inserts produce a warning.

NO_ZERO_DATE is deprecated. NO_ZERO_DATE is not part of strict mode, but should be used in
conjunction with strict mode and is enabled by default. A warning occurs if NO_ZERO_DATE is enabled
without also enabling strict mode or vice versa. For additional discussion, see SQL Mode Changes in
MySQL 5.7.

Because NO_ZERO_DATE is deprecated; expect it to be removed in a future release of MySQL as a
separate mode name and its effect included in the effects of strict SQL mode.

• NO_ZERO_IN_DATE

The NO_ZERO_IN_DATE mode affects whether the server permits dates in which the year part
is nonzero but the month or day part is 0. (This mode affects dates such as '2010-00-01' or
'2010-01-00', but not '0000-00-00'. To control whether the server permits '0000-00-00', use
the NO_ZERO_DATE mode.) The effect of NO_ZERO_IN_DATE also depends on whether strict SQL mode
is enabled.

• If this mode is not enabled, dates with zero parts are permitted and inserts produce no warning.

• If this mode is enabled, dates with zero parts are inserted as '0000-00-00' and produce a warning.

• If this mode and strict mode are enabled, dates with zero parts are not permitted and inserts produce

an error, unless IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, dates with zero
parts are inserted as '0000-00-00' and produce a warning.

NO_ZERO_IN_DATE is deprecated. NO_ZERO_IN_DATE is not part of strict mode, but should be used
in conjunction with strict mode and is enabled by default. A warning occurs if NO_ZERO_IN_DATE is
enabled without also enabling strict mode or vice versa. For additional discussion, see SQL Mode
Changes in MySQL 5.7.

Because NO_ZERO_IN_DATE is deprecated; expect it to be removed in a future release of MySQL as a
separate mode name and its effect included in the effects of strict SQL mode.

• ONLY_FULL_GROUP_BY

Reject queries for which the select list, HAVING condition, or ORDER BY list refer to nonaggregated
columns that are neither named in the GROUP BY clause nor are functionally dependent on (uniquely
determined by) GROUP BY columns.

As of MySQL 5.7.5, the default SQL mode includes ONLY_FULL_GROUP_BY. (Before 5.7.5, MySQL does
not detect functional dependency and ONLY_FULL_GROUP_BY is not enabled by default.)

A MySQL extension to standard SQL permits references in the HAVING clause to aliased expressions
in the select list. Before MySQL 5.7.5, enabling ONLY_FULL_GROUP_BY disables this extension,
thus requiring the HAVING clause to be written using unaliased expressions. As of MySQL 5.7.5,

938

Server SQL Modes

this restriction is lifted so that the HAVING clause can refer to aliases regardless of whether
ONLY_FULL_GROUP_BY is enabled.

For additional discussion and examples, see Section 12.19.3, “MySQL Handling of GROUP BY”.

• PAD_CHAR_TO_FULL_LENGTH

By default, trailing spaces are trimmed from CHAR column values on retrieval. If
PAD_CHAR_TO_FULL_LENGTH is enabled, trimming does not occur and retrieved CHAR values are
padded to their full length. This mode does not apply to VARCHAR columns, for which trailing spaces are
retained on retrieval.

mysql> CREATE TABLE t1 (c1 CHAR(10));
Query OK, 0 rows affected (0.37 sec)

mysql> INSERT INTO t1 (c1) VALUES('xy');
Query OK, 1 row affected (0.01 sec)

mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT c1, CHAR_LENGTH(c1) FROM t1;
+------+-----------------+
| c1   | CHAR_LENGTH(c1) |
+------+-----------------+
| xy   |               2 |
+------+-----------------+
1 row in set (0.00 sec)

mysql> SET sql_mode = 'PAD_CHAR_TO_FULL_LENGTH';
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT c1, CHAR_LENGTH(c1) FROM t1;
+------------+-----------------+
| c1         | CHAR_LENGTH(c1) |
+------------+-----------------+
| xy         |              10 |
+------------+-----------------+
1 row in set (0.00 sec)

• PIPES_AS_CONCAT

Treat || as a string concatenation operator (same as CONCAT()) rather than as a synonym for OR.

• REAL_AS_FLOAT

Treat REAL as a synonym for FLOAT. By default, MySQL treats REAL as a synonym for DOUBLE.

• STRICT_ALL_TABLES

Enable strict SQL mode for all storage engines. Invalid data values are rejected. For details, see Strict
SQL Mode.

From MySQL 5.7.4 through 5.7.7, STRICT_ALL_TABLES includes the effect of the
ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE modes. For additional
discussion, see SQL Mode Changes in MySQL 5.7.

• STRICT_TRANS_TABLES

Enable strict SQL mode for transactional storage engines, and when possible for nontransactional
storage engines. For details, see Strict SQL Mode.

939

Server SQL Modes

From MySQL 5.7.4 through 5.7.7, STRICT_TRANS_TABLES includes the effect of the
ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE modes. For additional
discussion, see SQL Mode Changes in MySQL 5.7.

Combination SQL Modes

The following special modes are provided as shorthand for combinations of mode values from the
preceding list.

• ANSI

Equivalent to REAL_AS_FLOAT, PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, and (as of
MySQL 5.7.5) ONLY_FULL_GROUP_BY.

ANSI mode also causes the server to return an error for queries where a set function S with an outer
reference S(outer_ref) cannot be aggregated in the outer query against which the outer reference
has been resolved. This is such a query:

SELECT * FROM t1 WHERE t1.a IN (SELECT MAX(t1.b) FROM t2 WHERE ...);

Here, MAX(t1.b) cannot aggregated in the outer query because it appears in the WHERE clause of that
query. Standard SQL requires an error in this situation. If ANSI mode is not enabled, the server treats
S(outer_ref) in such queries the same way that it would interpret S(const).

See Section 1.6, “MySQL Standards Compliance”.

• DB2

Equivalent to PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, NO_KEY_OPTIONS,
NO_TABLE_OPTIONS, NO_FIELD_OPTIONS.

Note

As of MySQL 5.7.22, DB2 is deprecated. It is removed in MySQL 8.0.

• MAXDB

Equivalent to PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, NO_KEY_OPTIONS,
NO_TABLE_OPTIONS, NO_FIELD_OPTIONS, NO_AUTO_CREATE_USER.

Note

As of MySQL 5.7.22, MAXDB is deprecated. It is removed in MySQL 8.0.

• MSSQL

Equivalent to PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, NO_KEY_OPTIONS,
NO_TABLE_OPTIONS, NO_FIELD_OPTIONS.

Note

As of MySQL 5.7.22, MSSQL is deprecated. It is removed in MySQL 8.0.

• MYSQL323

940

Server SQL Modes

Equivalent to MYSQL323, HIGH_NOT_PRECEDENCE. This means HIGH_NOT_PRECEDENCE plus some
SHOW CREATE TABLE behaviors specific to MYSQL323:

• TIMESTAMP column display does not include DEFAULT or ON UPDATE attributes.

• String column display does not include character set and collation attributes. For CHAR and VARCHAR

columns, if the collation is binary, BINARY is appended to the column type.

• The ENGINE=engine_name table option displays as TYPE=engine_name.

• For MEMORY tables, the storage engine is displayed as HEAP.

Note

As of MySQL 5.7.22, MYSQL323 is deprecated. It is removed in MySQL 8.0.

• MYSQL40

Equivalent to MYSQL40, HIGH_NOT_PRECEDENCE. This means HIGH_NOT_PRECEDENCE plus some
behaviors specific to MYSQL40. These are the same as for MYSQL323, except that SHOW CREATE
TABLE does not display HEAP as the storage engine for MEMORY tables.

Note

As of MySQL 5.7.22, MYSQL40 is deprecated. It is removed in MySQL 8.0.

• ORACLE

Equivalent to PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, NO_KEY_OPTIONS,
NO_TABLE_OPTIONS, NO_FIELD_OPTIONS, NO_AUTO_CREATE_USER.

Note

As of MySQL 5.7.22, ORACLE is deprecated. It is removed in MySQL 8.0.

• POSTGRESQL

Equivalent to PIPES_AS_CONCAT, ANSI_QUOTES, IGNORE_SPACE, NO_KEY_OPTIONS,
NO_TABLE_OPTIONS, NO_FIELD_OPTIONS.

Note

As of MySQL 5.7.22, POSTGRESQL is deprecated. It is removed in MySQL 8.0.

• TRADITIONAL

Before MySQL 5.7.4, and in MySQL 5.7.8 and later, TRADITIONAL is equivalent to
STRICT_TRANS_TABLES, STRICT_ALL_TABLES, NO_ZERO_IN_DATE, NO_ZERO_DATE,
ERROR_FOR_DIVISION_BY_ZERO, NO_AUTO_CREATE_USER, and NO_ENGINE_SUBSTITUTION.

From MySQL 5.7.4 though 5.7.7, TRADITIONAL is equivalent to STRICT_TRANS_TABLES,
STRICT_ALL_TABLES, NO_AUTO_CREATE_USER, and NO_ENGINE_SUBSTITUTION. The
NO_ZERO_IN_DATE, NO_ZERO_DATE, and ERROR_FOR_DIVISION_BY_ZERO modes are not
named because in those versions their effects are included in the effects of strict SQL mode
(STRICT_ALL_TABLES or STRICT_TRANS_TABLES). Thus, the effects of TRADITIONAL are the same

941

Server SQL Modes

in all MySQL 5.7 versions (and the same as in MySQL 5.6). For additional discussion, see SQL Mode
Changes in MySQL 5.7.

Strict SQL Mode

Strict mode controls how MySQL handles invalid or missing values in data-change statements such as
INSERT or UPDATE. A value can be invalid for several reasons. For example, it might have the wrong data
type for the column, or it might be out of range. A value is missing when a new row to be inserted does not
contain a value for a non-NULL column that has no explicit DEFAULT clause in its definition. (For a NULL
column, NULL is inserted if the value is missing.) Strict mode also affects DDL statements such as CREATE
TABLE.

If strict mode is not in effect, MySQL inserts adjusted values for invalid or missing values and produces
warnings (see Section 13.7.5.40, “SHOW WARNINGS Statement”). In strict mode, you can produce this
behavior by using INSERT IGNORE or UPDATE IGNORE.

For statements such as SELECT that do not change data, invalid values generate a warning in strict mode,
not an error.

Strict mode produces an error for attempts to create a key that exceeds the maximum key length. When
strict mode is not enabled, this results in a warning and truncation of the key to the maximum key length.

Strict mode does not affect whether foreign key constraints are checked. foreign_key_checks can be
used for that. (See Section 5.1.7, “Server System Variables”.)

Strict SQL mode is in effect if either STRICT_ALL_TABLES or STRICT_TRANS_TABLES is enabled,
although the effects of these modes differ somewhat:

• For transactional tables, an error occurs for invalid or missing values in a data-change statement when
either STRICT_ALL_TABLES or STRICT_TRANS_TABLES is enabled. The statement is aborted and
rolled back.

• For nontransactional tables, the behavior is the same for either mode if the bad value occurs in the

first row to be inserted or updated: The statement is aborted and the table remains unchanged. If the
statement inserts or modifies multiple rows and the bad value occurs in the second or later row, the
result depends on which strict mode is enabled:

• For STRICT_ALL_TABLES, MySQL returns an error and ignores the rest of the rows. However,

because the earlier rows have been inserted or updated, the result is a partial update. To avoid this,
use single-row statements, which can be aborted without changing the table.

• For STRICT_TRANS_TABLES, MySQL converts an invalid value to the closest valid value for the
column and inserts the adjusted value. If a value is missing, MySQL inserts the implicit default
value for the column data type. In either case, MySQL generates a warning rather than an error and
continues processing the statement. Implicit defaults are described in Section 11.6, “Data Type Default
Values”.

Strict mode affects handling of division by zero, zero dates, and zeros in dates as follows:

• Strict mode affects handling of division by zero, which includes MOD(N,0):

For data-change operations (INSERT, UPDATE):

• If strict mode is not enabled, division by zero inserts NULL and produces no warning.

• If strict mode is enabled, division by zero produces an error, unless IGNORE is given as well. For
INSERT IGNORE and UPDATE IGNORE, division by zero inserts NULL and produces a warning.

942

Server SQL Modes

For SELECT, division by zero returns NULL. Enabling strict mode causes a warning to be produced as
well.

• Strict mode affects whether the server permits '0000-00-00' as a valid date:

• If strict mode is not enabled, '0000-00-00' is permitted and inserts produce no warning.

• If strict mode is enabled, '0000-00-00' is not permitted and inserts produce an error, unless

IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, '0000-00-00' is permitted
and inserts produce a warning.

• Strict mode affects whether the server permits dates in which the year part is nonzero but the month or

day part is 0 (dates such as '2010-00-01' or '2010-01-00'):

• If strict mode is not enabled, dates with zero parts are permitted and inserts produce no warning.

• If strict mode is enabled, dates with zero parts are not permitted and inserts produce an error, unless

IGNORE is given as well. For INSERT IGNORE and UPDATE IGNORE, dates with zero parts are
inserted as '0000-00-00' (which is considered valid with IGNORE) and produce a warning.

For more information about strict mode with respect to IGNORE, see Comparison of the IGNORE Keyword
and Strict SQL Mode.

Before MySQL 5.7.4, and in MySQL 5.7.8 and later, strict mode affects handling of division by zero, zero
dates, and zeros in dates in conjunction with the ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and
NO_ZERO_IN_DATE modes. From MySQL 5.7.4 though 5.7.7, the ERROR_FOR_DIVISION_BY_ZERO,
NO_ZERO_DATE, and NO_ZERO_IN_DATE modes do nothing when named explicitly and their effects are
included in the effects of strict mode. For additional discussion, see SQL Mode Changes in MySQL 5.7.

Comparison of the IGNORE Keyword and Strict SQL Mode

This section compares the effect on statement execution of the IGNORE keyword (which downgrades
errors to warnings) and strict SQL mode (which upgrades warnings to errors). It describes which
statements they affect, and which errors they apply to.

The following table presents a summary comparison of statement behavior when the default is to produce
an error versus a warning. An example of when the default is to produce an error is inserting a NULL into
a NOT NULL column. An example of when the default is to produce a warning is inserting a value of the
wrong data type into a column (such as inserting the string 'abc' into an integer column).

Operational Mode

When Statement Default is Error When Statement Default is

Without IGNORE or strict SQL
mode

With IGNORE

Error

Warning

Warning

Warning

Warning (same as without
IGNORE or strict SQL mode)

With strict SQL mode

Error (same as without IGNORE or
strict SQL mode)

Error

With IGNORE and strict SQL mode Warning

Warning

One conclusion to draw from the table is that when the IGNORE keyword and strict SQL mode are both
in effect, IGNORE takes precedence. This means that, although IGNORE and strict SQL mode can be
considered to have opposite effects on error handling, they do not cancel when used together.

• The Effect of IGNORE on Statement Execution

943

Server SQL Modes

• The Effect of Strict SQL Mode on Statement Execution

The Effect of IGNORE on Statement Execution

Several statements in MySQL support an optional IGNORE keyword. This keyword causes the server
to downgrade certain types of errors and generate warnings instead. For a multiple-row statement,
downgrading an error to a warning may enable a row to be processed. Otherwise, IGNORE causes the
statement to skip to the next row instead of aborting. (For nonignorable errors, an error occurs regardless
of the IGNORE keyword.)

Example: If the table t has a primary key column i containing unique values, attempting to insert the same
value of i into multiple rows normally produces a duplicate-key error:

mysql> CREATE TABLE t (i INT NOT NULL PRIMARY KEY);
mysql> INSERT INTO t (i) VALUES(1),(1);
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'

With IGNORE, the row containing the duplicate key still is not inserted, but a warning occurs instead of an
error:

mysql> INSERT IGNORE INTO t (i) VALUES(1),(1);
Query OK, 1 row affected, 1 warning (0.01 sec)
Records: 2  Duplicates: 1  Warnings: 1

mysql> SHOW WARNINGS;
+---------+------+---------------------------------------+
| Level   | Code | Message                               |
+---------+------+---------------------------------------+
| Warning | 1062 | Duplicate entry '1' for key 'PRIMARY' |
+---------+------+---------------------------------------+
1 row in set (0.00 sec)

Example: If the table t2 has a NOT NULL column id, attempting to insert NULL produces an error in strict
SQL mode:

mysql> CREATE TABLE t2 (id INT NOT NULL);
mysql> INSERT INTO t2 (id) VALUES(1),(NULL),(3);
ERROR 1048 (23000): Column 'id' cannot be null
mysql> SELECT * FROM t2;
Empty set (0.00 sec)

If the SQL mode is not strict, IGNORE causes the NULL to be inserted as the column implicit default (0 in
this case), which enables the row to be handled without skipping it:

mysql> INSERT INTO t2 (id) VALUES(1),(NULL),(3);
mysql> SELECT * FROM t2;
+----+
| id |
+----+
|  1 |
|  0 |
|  3 |
+----+

These statements support the IGNORE keyword:

• CREATE TABLE ... SELECT: IGNORE does not apply to the CREATE TABLE or SELECT parts of the
statement but to inserts into the table of rows produced by the SELECT. Rows that duplicate an existing
row on a unique key value are discarded.

• DELETE: IGNORE causes MySQL to ignore errors during the process of deleting rows.

• INSERT: With IGNORE, rows that duplicate an existing row on a unique key value are discarded. Rows

set to values that would cause data conversion errors are set to the closest valid values instead.

944

Server SQL Modes

 For partitioned tables where no partition matching a given value is found, IGNORE causes the insert
operation to fail silently for rows containing the unmatched value.

• LOAD DATA, LOAD XML: With IGNORE, rows that duplicate an existing row on a unique key value are

discarded.

• UPDATE: With IGNORE, rows for which duplicate-key conflicts occur on a unique key value are not

updated. Rows updated to values that would cause data conversion errors are updated to the closest
valid values instead.

The IGNORE keyword applies to the following ignorable errors:

• ER_BAD_NULL_ERROR

• ER_DUP_ENTRY

• ER_DUP_ENTRY_WITH_KEY_NAME

• ER_DUP_KEY

• ER_NO_PARTITION_FOR_GIVEN_VALUE

• ER_NO_PARTITION_FOR_GIVEN_VALUE_SILENT

• ER_NO_REFERENCED_ROW_2

• ER_ROW_DOES_NOT_MATCH_GIVEN_PARTITION_SET

• ER_ROW_IS_REFERENCED_2

• ER_SUBQUERY_NO_1_ROW

• ER_VIEW_CHECK_FAILED

The Effect of Strict SQL Mode on Statement Execution

The MySQL server can operate in different SQL modes, and can apply these modes differently for different
clients, depending on the value of the sql_mode system variable. In “strict” SQL mode, the server
upgrades certain warnings to errors.

For example, in non-strict SQL mode, inserting the string 'abc' into an integer column results in
conversion of the value to 0 and a warning:

mysql> SET sql_mode = '';
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t (i) VALUES('abc');
Query OK, 1 row affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------+
| Level   | Code | Message                                                |
+---------+------+--------------------------------------------------------+
| Warning | 1366 | Incorrect integer value: 'abc' for column 'i' at row 1 |
+---------+------+--------------------------------------------------------+
1 row in set (0.00 sec)

In strict SQL mode, the invalid value is rejected with an error:

mysql> SET sql_mode = 'STRICT_ALL_TABLES';
Query OK, 0 rows affected (0.00 sec)

945

Server SQL Modes

mysql> INSERT INTO t (i) VALUES('abc');
ERROR 1366 (HY000): Incorrect integer value: 'abc' for column 'i' at row 1

For more information about possible settings of the sql_mode system variable, see Section 5.1.10,
“Server SQL Modes”.

Strict SQL mode applies to the following statements under conditions for which some value might be out of
range or an invalid row is inserted into or deleted from a table:

• ALTER TABLE

• CREATE TABLE

• CREATE TABLE ... SELECT

• DELETE (both single table and multiple table)

• INSERT

• LOAD DATA

• LOAD XML

• SELECT SLEEP()

• UPDATE (both single table and multiple table)

Within stored programs, individual statements of the types just listed execute in strict SQL mode if the
program was defined while strict mode was in effect.

Strict SQL mode applies to the following errors, which represent a class of errors in which an input value
is either invalid or missing. A value is invalid if it has the wrong data type for the column or might be out of
range. A value is missing if a new row to be inserted does not contain a value for a NOT NULL column that
has no explicit DEFAULT clause in its definition.

ER_BAD_NULL_ERROR
ER_CUT_VALUE_GROUP_CONCAT
ER_DATA_TOO_LONG
ER_DATETIME_FUNCTION_OVERFLOW
ER_DIVISION_BY_ZERO
ER_INVALID_ARGUMENT_FOR_LOGARITHM
ER_NO_DEFAULT_FOR_FIELD
ER_NO_DEFAULT_FOR_VIEW_FIELD
ER_TOO_LONG_KEY
ER_TRUNCATED_WRONG_VALUE
ER_TRUNCATED_WRONG_VALUE_FOR_FIELD
ER_WARN_DATA_OUT_OF_RANGE
ER_WARN_NULL_TO_NOTNULL
ER_WARN_TOO_FEW_RECORDS
ER_WRONG_ARGUMENTS
ER_WRONG_VALUE_FOR_TYPE
WARN_DATA_TRUNCATED

Note

Because continued MySQL development defines new errors, there may be errors
not in the preceding list to which strict SQL mode applies.

SQL Mode Changes in MySQL 5.7

In MySQL 5.7.22, these SQL modes are deprecated and are removed in MySQL 8.0: DB2, MAXDB,
MSSQL, MYSQL323, MYSQL40, ORACLE, POSTGRESQL, NO_FIELD_OPTIONS, NO_KEY_OPTIONS,
NO_TABLE_OPTIONS.

946

Connection Management

In MySQL 5.7, the ONLY_FULL_GROUP_BY SQL mode is enabled by default because GROUP BY
processing has become more sophisticated to include detection of functional dependencies. However,
if you find that having ONLY_FULL_GROUP_BY enabled causes queries for existing applications to be
rejected, either of these actions should restore operation:

• If it is possible to modify an offending query, do so, either so that nonaggregated columns are

functionally dependent on GROUP BY columns, or by referring to nonaggregated columns using
ANY_VALUE().

• If it is not possible to modify an offending query (for example, if it is generated by a third-party

application), set the sql_mode system variable at server startup to not enable ONLY_FULL_GROUP_BY.

In MySQL 5.7, the ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE SQL
modes are deprecated. The long term plan is to have the three modes be included in strict SQL mode
and to remove them as explicit modes in a future release of MySQL. For compatibility in MySQL 5.7 with
MySQL 5.6 strict mode and to provide additional time for affected applications to be modified, the following
behaviors apply:

• ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE are not part of strict SQL
mode, but it is intended that they be used together with strict mode. As a reminder, a warning occurs if
they are enabled without also enabling strict mode or vice versa.

• ERROR_FOR_DIVISION_BY_ZERO, NO_ZERO_DATE, and NO_ZERO_IN_DATE are enabled by default.

With the preceding changes, stricter data checking is still enabled by default, but the individual modes can
be disabled in environments where it is currently desirable or necessary to do so.

5.1.11 Connection Management

This section describes how MySQL Server manages connections. This includes a description of the
available connection interfaces, how the server uses connection handler threads, details about the
administrative connection interface, and management of DNS lookups.

5.1.11.1 Connection Interfaces

This section describes aspects of how the MySQL server manages client connections.

• Network Interfaces and Connection Manager Threads

• Client Connection Thread Management

• Connection Volume Management

Network Interfaces and Connection Manager Threads

The server is capable of listening for client connections on multiple network interfaces. Connection
manager threads handle client connection requests on the network interfaces that the server listens to:

• On all platforms, one manager thread handles TCP/IP connection requests.

• On Unix, the same manager thread also handles Unix socket file connection requests.

• On Windows, one manager thread handles shared-memory connection requests, and another handles

named-pipe connection requests.

The server does not create threads to handle interfaces that it does not listen to. For example, a Windows
server that does not have support for named-pipe connections enabled does not create a thread to handle
them.

947

Connection Management

Individual server plugins or components may implement their own connection interface:

• X Plugin enables MySQL Server to communicate with clients using X Protocol. See Section 19.4, “X

Plugin”.

Client Connection Thread Management

Connection manager threads associate each client connection with a thread dedicated to it that handles
authentication and request processing for that connection. Manager threads create a new thread when
necessary but try to avoid doing so by consulting the thread cache first to see whether it contains a thread
that can be used for the connection. When a connection ends, its thread is returned to the thread cache if
the cache is not full.

In this connection thread model, there are as many threads as there are clients currently connected, which
has some disadvantages when server workload must scale to handle large numbers of connections.
For example, thread creation and disposal becomes expensive. Also, each thread requires server and
kernel resources, such as stack space. To accommodate a large number of simultaneous connections,
the stack size per thread must be kept small, leading to a situation where it is either too small or the server
consumes large amounts of memory. Exhaustion of other resources can occur as well, and scheduling
overhead can become significant.

MySQL Enterprise Edition includes a thread pool plugin that provides an alternative thread-handling model
designed to reduce overhead and improve performance. It implements a thread pool that increases server
performance by efficiently managing statement execution threads for large numbers of client connections.
See Section 5.5.3, “MySQL Enterprise Thread Pool”.

To control and monitor how the server manages threads that handle client connections, several system
and status variables are relevant. (See Section 5.1.7, “Server System Variables”, and Section 5.1.9,
“Server Status Variables”.)

• The thread_cache_size system variable determines the thread cache size. By default, the
server autosizes the value at startup, but it can be set explicitly to override this default. A value
of 0 disables caching, which causes a thread to be set up for each new connection and disposed
of when the connection terminates. To enable N inactive connection threads to be cached, set
thread_cache_size to N at server startup or at runtime. A connection thread becomes inactive when
the client connection with which it was associated terminates.

• To monitor the number of threads in the cache and how many threads have been created because a

thread could not be taken from the cache, check the Threads_cached and Threads_created status
variables.

• When the thread stack is too small, this limits the complexity of the SQL statements the server can

handle, the recursion depth of stored procedures, and other memory-consuming actions. To set a stack
size of N bytes for each thread, start the server with thread_stack set to N.

Connection Volume Management

To control the maximum number of clients the server permits to connect simultaneously, set the
max_connections system variable at server startup or at runtime. It may be necessary to increase
max_connections if more clients attempt to connect simultaneously then the server is configured to
handle (see Section B.3.2.5, “Too many connections”).

mysqld actually permits max_connections + 1 client connections. The extra connection is reserved
for use by accounts that have the SUPER privilege. By granting the privilege to administrators and not
to normal users (who should not need it), an administrator who also has the PROCESS privilege can
connect to the server and use SHOW PROCESSLIST to diagnose problems even if the maximum number of
unprivileged clients are connected. See Section 13.7.5.29, “SHOW PROCESSLIST Statement”.

948

Connection Management

If the server refuses a connection because the max_connections limit is reached, it increments the
Connection_errors_max_connections status variable.

The maximum number of connections MySQL supports (that is, the maximum value to which
max_connections can be set) depends on several factors:

• The quality of the thread library on a given platform.

• The amount of RAM available.

• The amount of RAM is used for each connection.

• The workload from each connection.

• The desired response time.

• The number of file descriptors available.

Linux or Solaris should be able to support at least 500 to 1000 simultaneous connections routinely and as
many as 10,000 connections if you have many gigabytes of RAM available and the workload from each is
low or the response time target undemanding.

Increasing the max_connections value increases the number of file descriptors that mysqld requires. If
the required number of descriptors are not available, the server reduces the value of max_connections.
For comments on file descriptor limits, see Section 8.4.3.1, “How MySQL Opens and Closes Tables”.

Increasing the open_files_limit system variable may be necessary, which may also require raising
the operating system limit on how many file descriptors can be used by MySQL. Consult your operating
system documentation to determine whether it is possible to increase the limit and how to do so. See also
Section B.3.2.16, “File Not Found and Similar Errors”.

5.1.11.2 DNS Lookups and the Host Cache

The MySQL server maintains an in-memory host cache that contains information about clients: IP address,
host name, and error information. The Performance Schema host_cache table exposes the contents
of the host cache so that it can be examined using SELECT statements. This may help you diagnose the
causes of connection problems. See Section 25.12.16.1, “The host_cache Table”.

The following sections discuss how the host cache works, as well as other topics such as how to configure
and monitor the cache.

• Host Cache Operation

• Configuring the Host Cache

• Monitoring the Host Cache

• Flushing the Host Cache

• Dealing with Blocked Hosts

Host Cache Operation

The server uses the host cache only for non-localhost TCP connections. It does not use the cache for
TCP connections established using a loopback interface address (for example, 127.0.0.1 or ::1), or for
connections established using a Unix socket file, named pipe, or shared memory.

The server uses the host cache for several purposes:

949

Connection Management

• By caching the results of IP-to-host name lookups, the server avoids doing a Domain Name System

(DNS) lookup for each client connection. Instead, for a given host, it needs to perform a lookup only for
the first connection from that host.

• The cache contains information about errors that occur during the client connection process.
Some errors are considered “blocking.” If too many of these occur successively from a given
host without a successful connection, the server blocks further connections from that host. The
max_connect_errors system variable determines the permitted number of successive errors before
blocking occurs.

For each applicable new client connection, the server uses the client IP address to check whether the
client host name is in the host cache. If so, the server refuses or continues to process the connection
request depending on whether or not the host is blocked. If the host is not in the cache, the server attempts
to resolve the host name. First, it resolves the IP address to a host name and resolves that host name back
to an IP address. Then it compares the result to the original IP address to ensure that they are the same.
The server stores information about the result of this operation in the host cache. If the cache is full, the
least recently used entry is discarded.

The server performs host name resolution using the getaddrinfo() system call.

The server handles entries in the host cache like this:

1. When the first TCP client connection reaches the server from a given IP address, a new cache entry
is created to record the client IP, host name, and client lookup validation flag. Initially, the host name
is set to NULL and the flag is false. This entry is also used for subsequent client TCP connections from
the same originating IP.

2.

If the validation flag for the client IP entry is false, the server attempts an IP-to-host name-to-IP
DNS resolution. If that is successful, the host name is updated with the resolved host name and the
validation flag is set to true. If resolution is unsuccessful, the action taken depends on whether the error
is permanent or transient. For permanent failures, the host name remains NULL and the validation flag
is set to true. For transient failures, the host name and validation flag remain unchanged. (In this case,
another DNS resolution attempt occurs the next time a client connects from this IP.)

3.

If an error occurs while processing an incoming client connection from a given IP address, the server
updates the corresponding error counters in the entry for that IP. For a description of the errors
recorded, see Section 25.12.16.1, “The host_cache Table”.

To unblock blocked hosts, flush the host cache; see Dealing with Blocked Hosts.

It is possible for a blocked host to become unblocked even without flushing the host cache if activity from
other hosts occurs:

• If the cache is full when a connection arrives from a client IP not in the cache, the server discards the

least recently used cache entry to make room for the new entry.

• If the discarded entry is for a blocked host, that host becomes unblocked.

Some connection errors are not associated with TCP connections, occur very early in the connection
process (even before an IP address is known), or are not specific to any particular IP address (such as out-
of-memory conditions). For information about these errors, check the Connection_errors_xxx status
variables (see Section 5.1.9, “Server Status Variables”).

Configuring the Host Cache

The host cache is enabled by default. The host_cache_size system variable controls its size, as well
as the size of the Performance Schema host_cache table that exposes the cache contents. The cache

950

Connection Management

size can be set at server startup and changed at runtime. For example, to set the size to 100 at startup, put
these lines in the server my.cnf file:

[mysqld]
host_cache_size=200

To change the size to 300 at runtime, do this:

SET GLOBAL host_cache_size=300;

Setting host_cache_size to 0, either at server startup or at runtime, disables the host cache. With the
cache disabled, the server performs a DNS lookup every time a client connects.

Changing the cache size at runtime causes an implicit host cache flushing operation that clears the host
cache, truncates the host_cache table, and unblocks any blocked hosts; see Flushing the Host Cache.

Using the --skip-host-cache option is similar to setting the host_cache_size system variable to
0, but host_cache_size is more flexible because it can also be used to resize, enable, and disable the
host cache at runtime, not just at server startup. Starting the server with --skip-host-cache does not
prevent runtime changes to the value of host_cache_size, but such changes have no effect and the
cache is not re-enabled even if host_cache_size is set larger than 0.

To disable DNS host name lookups, start the server with the skip_name_resolve system variable
enabled. In this case, the server uses only IP addresses and not host names to match connecting hosts to
rows in the MySQL grant tables. Only accounts specified in those tables using IP addresses can be used.
(A client may not be able to connect if no account exists that specifies the client IP address.)

If you have a very slow DNS and many hosts, you might be able to improve performance either by enabling
skip_name_resolve to disable DNS lookups, or by increasing the value of host_cache_size to make
the host cache larger.

To disallow TCP/IP connections entirely, start the server with the skip_networking system variable
enabled.

To adjust the permitted number of successive connection errors before host blocking occurs, set the
max_connect_errors system variable. For example, to set the value at startup put these lines in the
server my.cnf file:

[mysqld]
max_connect_errors=10000

To change the value at runtime, do this:

SET GLOBAL max_connect_errors=10000;

Monitoring the Host Cache

The Performance Schema host_cache table exposes the contents of the host cache. This table can be
examined using SELECT statements, which may help you diagnose the causes of connection problems.
The Performance Schema must be enabled or this table is empty. For information about this table, see
Section 25.12.16.1, “The host_cache Table”.

Flushing the Host Cache

Flushing the host cache might be advisable or desirable under these conditions:

• Some of your client hosts change IP address.

• The error message Host 'host_name' is blocked occurs for connections from legitimate hosts.

(See Dealing with Blocked Hosts.)

951

IPv6 Support

Flushing the host cache has these effects:

• It clears the in-memory host cache.

• It removes all rows from the Performance Schema host_cache table that exposes the cache contents.

• It unblocks any blocked hosts. This enables further connection attempts from those hosts.

To flush the host cache, use any of these methods:

• Change the value of the host_cache_size system variable. This requires the SUPER privilege.

• Execute a TRUNCATE TABLE statement that truncates the Performance Schema host_cache table.

This requires the DROP privilege for the table.

• Execute a FLUSH HOSTS statement. This requires the RELOAD privilege.

• Execute a mysqladmin flush-hosts command. This requires the RELOAD privilege.

Dealing with Blocked Hosts

The server uses the host cache to track errors that occur during the client connection process. If the
following error occurs, it means that mysqld has received many connection requests from the given host
that were interrupted in the middle:

Host 'host_name' is blocked because of many connection errors.
Unblock with 'mysqladmin flush-hosts'

The value of the max_connect_errors system variable determines how many successive interrupted
connection requests the server permits before blocking a host. After max_connect_errors failed
requests without a successful connection, the server assumes that something is wrong (for example, that
someone is trying to break in), and blocks the host from further connection requests.

To unblock blocked hosts, flush the host cache; see Flushing the Host Cache.

Alternatively, to avoid having the error message occur, set max_connect_errors as described
in Configuring the Host Cache. The default value of max_connect_errors is 100. Increasing
max_connect_errors to a large value makes it less likely that a host reaches the threshold and
becomes blocked. However, if the Host 'host_name' is blocked error message occurs, first verify
that there is nothing wrong with TCP/IP connections from the blocked hosts. It does no good to increase
the value of max_connect_errors if there are network problems.

5.1.12 IPv6 Support

Support for IPv6 in MySQL includes these capabilities:

• MySQL Server can accept TCP/IP connections from clients connecting over IPv6. For example, this

command connects over IPv6 to the MySQL server on the local host:

$> mysql -h ::1

To use this capability, two things must be true:

• Your system must be configured to support IPv6. See Section 5.1.12.1, “Verifying System Support for

IPv6”.

• The default MySQL server configuration permits IPv6 connections in addition to IPv4 connections. To
change the default configuration, start the server with the bind_address system variable set to an
appropriate value. See Section 5.1.7, “Server System Variables”.

952

IPv6 Support

• MySQL account names permit IPv6 addresses to enable DBAs to specify privileges for clients that

connect to the server over IPv6. See Section 6.2.4, “Specifying Account Names”. IPv6 addresses can be
specified in account names in statements such as CREATE USER, GRANT, and REVOKE. For example:

mysql> CREATE USER 'bill'@'::1' IDENTIFIED BY 'secret';
mysql> GRANT SELECT ON mydb.* TO 'bill'@'::1';

• IPv6 functions enable conversion between string and internal format IPv6 address formats, and checking
whether values represent valid IPv6 addresses. For example, INET6_ATON() and INET6_NTOA() are
similar to INET_ATON() and INET_NTOA(), but handle IPv6 addresses in addition to IPv4 addresses.
See Section 12.20, “Miscellaneous Functions”.

The following sections describe how to set up MySQL so that clients can connect to the server over IPv6.

5.1.12.1 Verifying System Support for IPv6

Before MySQL Server can accept IPv6 connections, the operating system on your server host must
support IPv6. As a simple test to determine whether that is true, try this command:

$> ping6 ::1
16 bytes from ::1, icmp_seq=0 hlim=64 time=0.171 ms
16 bytes from ::1, icmp_seq=1 hlim=64 time=0.077 ms
...

To produce a description of your system's network interfaces, invoke ifconfig -a and look for IPv6
addresses in the output.

If your host does not support IPv6, consult your system documentation for instructions on enabling it. It
might be that you need only reconfigure an existing network interface to add an IPv6 address. Or a more
extensive change might be needed, such as rebuilding the kernel with IPv6 options enabled.

These links may be helpful in setting up IPv6 on various platforms:

• Windows

• Gentoo Linux

• Ubuntu Linux

• Linux (Generic)

• macOS

5.1.12.2 Configuring the MySQL Server to Permit IPv6 Connections

The MySQL server listens on a single network socket for TCP/IP connections. This socket is bound to a
single address, but it is possible for an address to map onto multiple network interfaces. To specify an
address, set bind_address=addr at server startup, where addr is an IPv4 or IPv6 address or a host
name. For details, see the bind_address description in Section 5.1.7, “Server System Variables”.

5.1.12.3 Connecting Using the IPv6 Local Host Address

The following procedure shows how to configure MySQL to permit IPv6 connections by clients that connect
to the local server using the ::1 local host address. The instructions given here assume that your system
supports IPv6.

1. Start the MySQL server with an appropriate bind_address setting to permit it to accept IPv6
connections. For example, put the following lines in the server option file and restart the server:

953

IPv6 Support

[mysqld]
bind_address = *

Alternatively, you can bind the server to ::1, but that makes the server more restrictive for TCP/IP
connections. It accepts only IPv6 connections for that single address and rejects IPv4 connections. For
more information, see the bind_address description in Section 5.1.7, “Server System Variables”.

2. As an administrator, connect to the server and create an account for a local user who connects from

the ::1 local IPv6 host address:

mysql> CREATE USER 'ipv6user'@'::1' IDENTIFIED BY 'ipv6pass';

For the permitted syntax of IPv6 addresses in account names, see Section 6.2.4, “Specifying Account
Names”. In addition to the CREATE USER statement, you can issue GRANT statements that give specific
privileges to the account, although that is not necessary for the remaining steps in this procedure.

3.

Invoke the mysql client to connect to the server using the new account:

$> mysql -h ::1 -u ipv6user -pipv6pass

4. Try some simple statements that show connection information:

mysql> STATUS
...
Connection:   ::1 via TCP/IP
...

mysql> SELECT CURRENT_USER(), @@bind_address;
+----------------+----------------+
| CURRENT_USER() | @@bind_address |
+----------------+----------------+
| ipv6user@::1   | ::             |
+----------------+----------------+

5.1.12.4 Connecting Using IPv6 Nonlocal Host Addresses

The following procedure shows how to configure MySQL to permit IPv6 connections by remote clients. It is
similar to the preceding procedure for local clients, but the server and client hosts are distinct and each has
its own nonlocal IPv6 address. The example uses these addresses:

Server host: 2001:db8:0:f101::1
Client host: 2001:db8:0:f101::2

These addresses are chosen from the nonroutable address range recommended by IANA for
documentation purposes and suffice for testing on your local network. To accept IPv6 connections from
clients outside the local network, the server host must have a public address. If your network provider
assigns you an IPv6 address, you can use that. Otherwise, another way to obtain an address is to use an
IPv6 broker; see Section 5.1.12.5, “Obtaining an IPv6 Address from a Broker”.

1. Start the MySQL server with an appropriate bind_address setting to permit it to accept IPv6
connections. For example, put the following lines in the server option file and restart the server:

[mysqld]
bind_address = *

Alternatively, you can bind the server to 2001:db8:0:f101::1, but that makes the server more
restrictive for TCP/IP connections. It accepts only IPv6 connections for that single address and rejects
IPv4 connections. For more information, see the bind_address description in Section 5.1.7, “Server
System Variables”.

954

IPv6 Support

2. On the server host (2001:db8:0:f101::1), create an account for a user who connects from the

client host (2001:db8:0:f101::2):

mysql> CREATE USER 'remoteipv6user'@'2001:db8:0:f101::2' IDENTIFIED BY 'remoteipv6pass';

3. On the client host (2001:db8:0:f101::2), invoke the mysql client to connect to the server using the

new account:

$> mysql -h 2001:db8:0:f101::1 -u remoteipv6user -premoteipv6pass

4. Try some simple statements that show connection information:

mysql> STATUS
...
Connection:   2001:db8:0:f101::1 via TCP/IP
...

mysql> SELECT CURRENT_USER(), @@bind_address;
+-----------------------------------+----------------+
| CURRENT_USER()                    | @@bind_address |
+-----------------------------------+----------------+
| remoteipv6user@2001:db8:0:f101::2 | ::             |
+-----------------------------------+----------------+

5.1.12.5 Obtaining an IPv6 Address from a Broker

If you do not have a public IPv6 address that enables your system to communicate over IPv6 outside
your local network, you can obtain one from an IPv6 broker. The Wikipedia IPv6 Tunnel Broker page
lists several brokers and their features, such as whether they provide static addresses and the supported
routing protocols.

After configuring your server host to use a broker-supplied IPv6 address, start the MySQL server with an
appropriate bind_address setting to permit the server to accept IPv6 connections. For example, put the
following lines in the server option file and restart the server:

[mysqld]
bind_address = *

Alternatively, you can bind the server to the specific IPv6 address provided by the broker, but that makes
the server more restrictive for TCP/IP connections. It accepts only IPv6 connections for that single address
and rejects IPv4 connections. For more information, see the bind_address description in Section 5.1.7,
“Server System Variables”. In addition, if the broker allocates dynamic addresses, the address provided
for your system might change the next time you connect to the broker. If so, any accounts you create that
name the original address become invalid. To bind to a specific address but avoid this change-of-address
problem, you may be able to arrange with the broker for a static IPv6 address.

The following example shows how to use Freenet6 as the broker and the gogoc IPv6 client package on
Gentoo Linux.

1. Create an account at Freenet6 by visiting this URL and signing up:

http://gogonet.gogo6.com

2. After creating the account, go to this URL, sign in, and create a user ID and password for the IPv6

broker:

http://gogonet.gogo6.com/page/freenet6-registration

3. As root, install gogoc:

$> emerge gogoc

955

MySQL Server Time Zone Support

4. Edit /etc/gogoc/gogoc.conf to set the userid and password values. For example:

userid=gogouser
passwd=gogopass

5. Start gogoc:

$> /etc/init.d/gogoc start

To start gogoc each time your system boots, execute this command:

$> rc-update add gogoc default

6. Use ping6 to try to ping a host:

$> ping6 ipv6.google.com

7. To see your IPv6 address:

$> ifconfig tun

5.1.13 MySQL Server Time Zone Support

This section describes the time zone settings maintained by MySQL, how to load the system tables
required for named time support, how to stay current with time zone changes, and how to enable leap-
second support.

For information about time zone settings in replication setups, see Section 16.4.1.15, “Replication and
System Functions” and Section 16.4.1.31, “Replication and Time Zones”.

• Time Zone Variables

• Populating the Time Zone Tables

• Staying Current with Time Zone Changes

• Time Zone Leap Second Support

Time Zone Variables

MySQL Server maintains several time zone settings:

• The server system time zone. When the server starts, it attempts to determine the time zone of the

host machine and uses it to set the system_time_zone system variable. The value does not change
thereafter.

To explicitly specify the system time zone for MySQL Server at startup, set the TZ environment variable
before you start mysqld. If you start the server using mysqld_safe, its --timezone option provides
another way to set the system time zone. The permissible values for TZ and --timezone are system
dependent. Consult your operating system documentation to see what values are acceptable.

• The server current time zone. The global time_zone system variable indicates the time zone the server
currently is operating in. The initial time_zone value is 'SYSTEM', which indicates that the server time
zone is the same as the system time zone.

Note

If set to SYSTEM, every MySQL function call that requires a time zone calculation
makes a system library call to determine the current system time zone. This call
may be protected by a global mutex, resulting in contention.

956

MySQL Server Time Zone Support

The initial global server time zone value can be specified explicitly at startup with the --default-
time-zone option on the command line, or you can use the following line in an option file:

default-time-zone='timezone'

If you have the SUPER privilege, you can set the global server time zone value at runtime with this
statement:

SET GLOBAL time_zone = timezone;

• Per-session time zones. Each client that connects has its own session time zone setting, given by the
session time_zone variable. Initially, the session variable takes its value from the global time_zone
variable, but the client can change its own time zone with this statement:

SET time_zone = timezone;

The session time zone setting affects display and storage of time values that are zone-sensitive. This
includes the values displayed by functions such as NOW() or CURTIME(), and values stored in and
retrieved from TIMESTAMP columns. Values for TIMESTAMP columns are converted from the session time
zone to UTC for storage, and from UTC to the session time zone for retrieval.

The session time zone setting does not affect values displayed by functions such as UTC_TIMESTAMP()
or values in DATE, TIME, or DATETIME columns. Nor are values in those data types stored in UTC; the
time zone applies for them only when converting from TIMESTAMP values. If you want locale-specific
arithmetic for DATE, TIME, or DATETIME values, convert them to UTC, perform the arithmetic, and then
convert back.

The current global and session time zone values can be retrieved like this:

SELECT @@GLOBAL.time_zone, @@SESSION.time_zone;

timezone values can be given in several formats, none of which are case-sensitive:

• As the value 'SYSTEM', indicating that the server time zone is the same as the system time zone.

• As a string indicating an offset from UTC of the form [H]H:MM, prefixed with a + or -, such as

'+10:00', '-6:00', or '+05:30'. A leading zero can optionally be used for hours values less than
10; MySQL prepends a leading zero when storing and retriving the value in such cases. MySQL converts
'-00:00' or '-0:00' to '+00:00'.

A time zone offset must be in the range '-12:59' to '+13:00', inclusive.

• As a named time zone, such as 'Europe/Helsinki', 'US/Eastern', 'MET', or 'UTC'.

Note

Named time zones can be used only if the time zone information tables in the
mysql database have been created and populated. Otherwise, use of a named
time zone results in an error:

mysql> SET time_zone = 'UTC';
ERROR 1298 (HY000): Unknown or incorrect time zone: 'UTC'

Populating the Time Zone Tables

Several tables in the mysql system database exist to store time zone information (see Section 5.3, “The
mysql System Database”). The MySQL installation procedure creates the time zone tables, but does not
load them. To do so manually, use the following instructions.

957

MySQL Server Time Zone Support

Note

Loading the time zone information is not necessarily a one-time operation because
the information changes occasionally. When such changes occur, applications that
use the old rules become out of date and you may find it necessary to reload the
time zone tables to keep the information used by your MySQL server current. See
Staying Current with Time Zone Changes.

If your system has its own zoneinfo database (the set of files describing time zones), use the
mysql_tzinfo_to_sql program to load the time zone tables. Examples of such systems are Linux,
macOS, FreeBSD, and Solaris. One likely location for these files is the /usr/share/zoneinfo directory.
If your system has no zoneinfo database, you can use a downloadable package, as described later in this
section.

To load the time zone tables from the command line, pass the zoneinfo directory path name to
mysql_tzinfo_to_sql and send the output into the mysql program. For example:

mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql

The mysql command shown here assumes that you connect to the server using an account such as root
that has privileges for modifying tables in the mysql system database. Adjust the connection parameters
as required.

mysql_tzinfo_to_sql reads your system's time zone files and generates SQL statements from them.
mysql processes those statements to load the time zone tables.

mysql_tzinfo_to_sql also can be used to load a single time zone file or generate leap second
information:

• To load a single time zone file tz_file that corresponds to a time zone name tz_name, invoke

mysql_tzinfo_to_sql like this:

mysql_tzinfo_to_sql tz_file tz_name | mysql -u root -p mysql

With this approach, you must execute a separate command to load the time zone file for each named
zone that the server needs to know about.

• If your time zone must account for leap seconds, initialize leap second information like this, where

tz_file is the name of your time zone file:

mysql_tzinfo_to_sql --leap tz_file | mysql -u root -p mysql

After running mysql_tzinfo_to_sql, restart the server so that it does not continue to use any
previously cached time zone data.

If your system has no zoneinfo database (for example, Windows), you can use a package containing SQL
statements that is available for download at the MySQL Developer Zone:

https://dev.mysql.com/downloads/timezones.html

Warning

Do not use a downloadable time zone package if your system has a zoneinfo
database. Use the mysql_tzinfo_to_sql utility instead. Otherwise, you may
cause a difference in datetime handling between MySQL and other applications on
your system.

To use an SQL-statement time zone package that you have downloaded, unpack it, then load the
unpacked file contents into the time zone tables:

958

MySQL Server Time Zone Support

mysql -u root -p mysql < file_name

Then restart the server.

Warning

Do not use a downloadable time zone package that contains MyISAM tables. That
is intended for older MySQL versions. MySQL 5.7 and higher uses InnoDB for the
time zone tables. Trying to replace them with MyISAM tables causes problems.

Staying Current with Time Zone Changes

When time zone rules change, applications that use the old rules become out of date. To stay current, it is
necessary to make sure that your system uses current time zone information is used. For MySQL, there
are multiple factors to consider in staying current:

• The operating system time affects the value that the MySQL server uses for times if its time zone is set
to SYSTEM. Make sure that your operating system is using the latest time zone information. For most
operating systems, the latest update or service pack prepares your system for the time changes. Check
the website for your operating system vendor for an update that addresses the time changes.

• If you replace the system's /etc/localtime time zone file with a version that uses rules differing from
those in effect at mysqld startup, restart mysqld so that it uses the updated rules. Otherwise, mysqld
might not notice when the system changes its time.

• If you use named time zones with MySQL, make sure that the time zone tables in the mysql database

are up to date:

• If your system has its own zoneinfo database, reload the MySQL time zone tables whenever the

zoneinfo database is updated.

• For systems that do not have their own zoneinfo database, check the MySQL Developer Zone for

updates. When a new update is available, download it and use it to replace the content of your current
time zone tables.

For instructions for both methods, see Populating the Time Zone Tables. mysqld caches time zone
information that it looks up, so after updating the time zone tables, restart mysqld to make sure that it
does not continue to serve outdated time zone data.

If you are uncertain whether named time zones are available, for use either as the server's time zone
setting or by clients that set their own time zone, check whether your time zone tables are empty. The
following query determines whether the table that contains time zone names has any rows:

mysql> SELECT COUNT(*) FROM mysql.time_zone_name;
+----------+
| COUNT(*) |
+----------+
|        0 |
+----------+

A count of zero indicates that the table is empty. In this case, no applications currently are using named
time zones, and you need not update the tables (unless you want to enable named time zone support). A
count greater than zero indicates that the table is not empty and that its contents are available to be used
for named time zone support. In this case, be sure to reload your time zone tables so that applications that
use named time zones obtain correct query results.

To check whether your MySQL installation is updated properly for a change in Daylight Saving Time rules,
use a test like the one following. The example uses values that are appropriate for the 2007 DST 1-hour
change that occurs in the United States on March 11 at 2 a.m.

959

MySQL Server Time Zone Support

The test uses this query:

SELECT
  CONVERT_TZ('2007-03-11 2:00:00','US/Eastern','US/Central') AS time1,
  CONVERT_TZ('2007-03-11 3:00:00','US/Eastern','US/Central') AS time2;

The two time values indicate the times at which the DST change occurs, and the use of named time zones
requires that the time zone tables be used. The desired result is that both queries return the same result
(the input time, converted to the equivalent value in the 'US/Central' time zone).

Before updating the time zone tables, you see an incorrect result like this:

+---------------------+---------------------+
| time1               | time2               |
+---------------------+---------------------+
| 2007-03-11 01:00:00 | 2007-03-11 02:00:00 |
+---------------------+---------------------+

After updating the tables, you should see the correct result:

+---------------------+---------------------+
| time1               | time2               |
+---------------------+---------------------+
| 2007-03-11 01:00:00 | 2007-03-11 01:00:00 |
+---------------------+---------------------+

Time Zone Leap Second Support

Leap second values are returned with a time part that ends with :59:59. This means that a function
such as NOW() can return the same value for two or three consecutive seconds during the leap second.
It remains true that literal temporal values having a time part that ends with :59:60 or :59:61 are
considered invalid.

If it is necessary to search for TIMESTAMP values one second before the leap second, anomalous results
may be obtained if you use a comparison with 'YYYY-MM-DD hh:mm:ss' values. The following example
demonstrates this. It changes the session time zone to UTC so there is no difference between internal
TIMESTAMP values (which are in UTC) and displayed values (which have time zone correction applied).

mysql> CREATE TABLE t1 (
         a INT,
         ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         PRIMARY KEY (ts)
       );
Query OK, 0 rows affected (0.01 sec)

mysql> -- change to UTC
mysql> SET time_zone = '+00:00';
Query OK, 0 rows affected (0.00 sec)

mysql> -- Simulate NOW() = '2008-12-31 23:59:59'
mysql> SET timestamp = 1230767999;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 (a) VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> -- Simulate NOW() = '2008-12-31 23:59:60'
mysql> SET timestamp = 1230768000;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 (a) VALUES (2);

960

Server-Side Help Support

Query OK, 1 row affected (0.00 sec)

mysql> -- values differ internally but display the same
mysql> SELECT a, ts, UNIX_TIMESTAMP(ts) FROM t1;
+------+---------------------+--------------------+
| a    | ts                  | UNIX_TIMESTAMP(ts) |
+------+---------------------+--------------------+
|    1 | 2008-12-31 23:59:59 |         1230767999 |
|    2 | 2008-12-31 23:59:59 |         1230768000 |
+------+---------------------+--------------------+
2 rows in set (0.00 sec)

mysql> -- only the non-leap value matches
mysql> SELECT * FROM t1 WHERE ts = '2008-12-31 23:59:59';
+------+---------------------+
| a    | ts                  |
+------+---------------------+
|    1 | 2008-12-31 23:59:59 |
+------+---------------------+
1 row in set (0.00 sec)

mysql> -- the leap value with seconds=60 is invalid
mysql> SELECT * FROM t1 WHERE ts = '2008-12-31 23:59:60';
Empty set, 2 warnings (0.00 sec)

To work around this, you can use a comparison based on the UTC value actually stored in the column,
which has the leap second correction applied:

mysql> -- selecting using UNIX_TIMESTAMP value return leap value
mysql> SELECT * FROM t1 WHERE UNIX_TIMESTAMP(ts) = 1230768000;
+------+---------------------+
| a    | ts                  |
+------+---------------------+
|    2 | 2008-12-31 23:59:59 |
+------+---------------------+
1 row in set (0.00 sec)

5.1.14 Server-Side Help Support

MySQL Server supports a HELP statement that returns information from the MySQL Reference Manual
(see Section 13.8.3, “HELP Statement”). This information is stored in several tables in the mysql database
(see Section 5.3, “The mysql System Database”). Proper operation of the HELP statement requires that
these help tables be initialized.

For a new installation of MySQL using a binary or source distribution on Unix, help-table content
initialization occurs when you initialize the data directory (see Section 2.9.1, “Initializing the Data
Directory”). For an RPM distribution on Linux or binary distribution on Windows, content initialization occurs
as part of the MySQL installation process.

For a MySQL upgrade using a binary distribution, help-table content is not upgraded automatically, but
you can upgrade it manually. Locate the fill_help_tables.sql file in the share or share/mysql
directory. Change location into that directory and process the file with the mysql client as follows:

mysql -u root -p mysql < fill_help_tables.sql

The command shown here assumes that you connect to the server using an account such as root that
has privileges for modifying tables in the mysql database. Adjust the connection parameters as required.

If you are working with Git and a MySQL development source tree, the source tree contains only a “stub”
version of fill_help_tables.sql. To obtain a non-stub copy, use one from a source or binary
distribution.

961

Server Tracking of Client Session State

Note

Each MySQL series has its own series-specific reference manual, so help-table
content is series specific as well. This has implications for replication because help-
table content should match the MySQL series. If you load MySQL 5.7 help content
into a MySQL 5.7 source server, it does not make sense to replicate that content
to a replica server from a different MySQL series and for which that content is not
appropriate. For this reason, as you upgrade individual servers in a replication
scenario, you should upgrade each server's help tables, using the instructions given
earlier.

5.1.15 Server Tracking of Client Session State

The MySQL server implements several session state trackers. A client can enable these trackers to
receive notification of changes to its session state.

• Uses for Session State Trackers

• Available Session State Trackers

• C API Session State Tracker Support

• Test Suite Session State Tracker Support

Uses for Session State Trackers

Session state trackers have uses such as these:

• To facilitate session migration.

• To facilitate transaction switching.

One use for the tracker mechanism is to provide a means for MySQL connectors and client applications to
determine whether any session context is available to permit session migration from one server to another.
(To change sessions in a load-balanced environment, it is necessary to detect whether there is session
state to take into consideration when deciding whether a switch can be made.)

Another use for the tracker mechanism is to permit applications to know when transactions can be moved
from one session to another. Transaction state tracking enables this, which is useful for applications
that may wish to move transactions from a busy server to one that is less loaded. For example, a load-
balancing connector managing a client connection pool could move transactions between available
sessions in the pool.

However, session switching cannot be done at arbitrary times. If a session is in the middle of a transaction
for which reads or writes have been done, switching to a different session implies a transaction rollback on
the original session. A session switch must be done only when a transaction does not yet have any reads
or writes performed within it.

Examples of when transactions might reasonably be switched:

• Immediately after START TRANSACTION

• After COMMIT AND CHAIN

In addition to knowing transaction state, it is useful to know transaction characteristics, so as to use the
same characteristics if the transaction is moved to a different session. The following characteristics are
relevant for this purpose:

READ ONLY
READ WRITE

962

Server Tracking of Client Session State

ISOLATION LEVEL
WITH CONSISTENT SNAPSHOT

Available Session State Trackers

To support the session-tracking activities, notification is available for these types of client session state
information:

• Changes to these attributes of client session state:

• The default schema (database).

• Session-specific values for system variables.

• User-defined variables.

• Temporary tables.

• Prepared statements.

The session_track_state_change system variable controls this tracker.

• Changes to the default schema name. The session_track_schema system variable controls this

tracker.

• Changes to the session values of system variables. The session_track_system_variables

system variable controls this tracker.

• Available GTIDs. The session_track_gtids system variable controls this tracker.

• Information about transaction state and characteristics. The session_track_transaction_info

system variable controls this tracker.

For descriptions of the tracker-related system variables, see Section 5.1.7, “Server System Variables”.
Those system variables permit control over which change notifications occur, but do not provide a way
to access notification information. Notification occurs in the MySQL client/server protocol, which includes
tracker information in OK packets so that session state changes can be detected.

C API Session State Tracker Support

To enable client applications to extract state-change information from OK packets returned by the server,
the MySQL C API provides a pair of functions:

• mysql_session_track_get_first() fetches the first part of the state-change information received

from the server. See mysql_session_track_get_first().

• mysql_session_track_get_next() fetches any remaining state-change information received from
the server. Following a successful call to mysql_session_track_get_first(), call this function
repeatedly as long as it returns success. See mysql_session_track_get_next().

Test Suite Session State Tracker Support

The mysqltest program has disable_session_track_info and enable_session_track_info
commands that control whether session tracker notifications occur. You can use these commands to see
from the command line what notifications SQL statements produce. Suppose that a file testscript
contains the following mysqltest script:

DROP TABLE IF EXISTS test.t1;
CREATE TABLE test.t1 (i INT, f FLOAT);
--enable_session_track_info

963

Server Tracking of Client Session State

SET @@SESSION.session_track_schema=ON;
SET @@SESSION.session_track_system_variables='*';
SET @@SESSION.session_track_state_change=ON;
USE information_schema;
SET NAMES 'utf8mb4';
SET @@SESSION.session_track_transaction_info='CHARACTERISTICS';
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
SET TRANSACTION READ WRITE;
START TRANSACTION;
SELECT 1;
INSERT INTO test.t1 () VALUES();
INSERT INTO test.t1 () VALUES(1, RAND());
COMMIT;

Run the script as follows to see the information provided by the enabled trackers. For a
description of the Tracker: information displayed by mysqltest for the various trackers, see
mysql_session_track_get_first().

$> mysqltest < testscript
DROP TABLE IF EXISTS test.t1;
CREATE TABLE test.t1 (i INT, f FLOAT);
SET @@SESSION.session_track_schema=ON;
SET @@SESSION.session_track_system_variables='*';
-- Tracker : SESSION_TRACK_SYSTEM_VARIABLES
-- session_track_system_variables
-- *

SET @@SESSION.session_track_state_change=ON;
-- Tracker : SESSION_TRACK_SYSTEM_VARIABLES
-- session_track_state_change
-- ON

USE information_schema;
-- Tracker : SESSION_TRACK_SCHEMA
-- information_schema

-- Tracker : SESSION_TRACK_STATE_CHANGE
-- 1

SET NAMES 'utf8mb4';
-- Tracker : SESSION_TRACK_SYSTEM_VARIABLES
-- character_set_client
-- utf8mb4
-- character_set_connection
-- utf8mb4
-- character_set_results
-- utf8mb4

-- Tracker : SESSION_TRACK_STATE_CHANGE
-- 1

SET @@SESSION.session_track_transaction_info='CHARACTERISTICS';
-- Tracker : SESSION_TRACK_SYSTEM_VARIABLES
-- session_track_transaction_info
-- CHARACTERISTICS

-- Tracker : SESSION_TRACK_STATE_CHANGE
-- 1

-- Tracker : SESSION_TRACK_TRANSACTION_CHARACTERISTICS
--

-- Tracker : SESSION_TRACK_TRANSACTION_STATE
-- ________

SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Tracker : SESSION_TRACK_TRANSACTION_CHARACTERISTICS

964

The Server Shutdown Process

-- SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

SET TRANSACTION READ WRITE;
-- Tracker : SESSION_TRACK_TRANSACTION_CHARACTERISTICS
-- SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; SET TRANSACTION READ WRITE;

START TRANSACTION;
-- Tracker : SESSION_TRACK_TRANSACTION_CHARACTERISTICS
-- SET TRANSACTION ISOLATION LEVEL SERIALIZABLE; START TRANSACTION READ WRITE;

-- Tracker : SESSION_TRACK_TRANSACTION_STATE
-- T_______

SELECT 1;
1
1
-- Tracker : SESSION_TRACK_TRANSACTION_STATE
-- T_____S_

INSERT INTO test.t1 () VALUES();
-- Tracker : SESSION_TRACK_TRANSACTION_STATE
-- T___W_S_

INSERT INTO test.t1 () VALUES(1, RAND());
-- Tracker : SESSION_TRACK_TRANSACTION_STATE
-- T___WsS_

COMMIT;
-- Tracker : SESSION_TRACK_TRANSACTION_CHARACTERISTICS
--

-- Tracker : SESSION_TRACK_TRANSACTION_STATE
-- ________

ok

Preceding the START TRANSACTION statement, two SET TRANSACTION statements execute
that set the isolation level and access mode characteristics for the next transaction. The
SESSION_TRACK_TRANSACTION_CHARACTERISTICS value indicates those next-transaction values that
have been set.

Following the COMMIT statement that ends the transaction, the
SESSION_TRACK_TRANSACTION_CHARACTERISTICS value is reported as empty. This indicates that the
next-transaction characteristics that were set preceding the start of the transaction have been reset, and
that the session defaults apply. To track changes to those session defaults, track the session values of the
transaction_isolation and transaction_read_only system variables.

To see information about GTIDs, enable the SESSION_TRACK_GTIDS tracker using the
session_track_gtids system system variable.

5.1.16 The Server Shutdown Process

The server shutdown process takes place as follows:

1. The shutdown process is initiated.

This can occur initiated several ways. For example, a user with the SHUTDOWN privilege can execute a
mysqladmin shutdown command. mysqladmin can be used on any platform supported by MySQL.
Other operating system-specific shutdown initiation methods are possible as well: The server shuts
down on Unix when it receives a SIGTERM signal. A server running as a service on Windows shuts
down when the services manager tells it to.

2. The server creates a shutdown thread if necessary.

965

The Server Shutdown Process

Depending on how shutdown was initiated, the server might create a thread to handle the shutdown
process. If shutdown was requested by a client, a shutdown thread is created. If shutdown is the result
of receiving a SIGTERM signal, the signal thread might handle shutdown itself, or it might create a
separate thread to do so. If the server tries to create a shutdown thread and cannot (for example, if
memory is exhausted), it issues a diagnostic message that appears in the error log:

Error: Can't create thread to kill server

3. The server stops accepting new connections.

To prevent new activity from being initiated during shutdown, the server stops accepting new
client connections by closing the handlers for the network interfaces to which it normally listens for
connections: the TCP/IP port, the Unix socket file, the Windows named pipe, and shared memory on
Windows.

4. The server terminates current activity.

For each thread associated with a client connection, the server breaks the connection to the client and
marks the thread as killed. Threads die when they notice that they are so marked. Threads for idle
connections die quickly. Threads that currently are processing statements check their state periodically
and take longer to die. For additional information about thread termination, see Section 13.7.6.4,
“KILL Statement”, in particular for the instructions about killed REPAIR TABLE or OPTIMIZE TABLE
operations on MyISAM tables.

For threads that have an open transaction, the transaction is rolled back. If a thread is updating a
nontransactional table, an operation such as a multiple-row UPDATE or INSERT may leave the table
partially updated because the operation can terminate before completion.

If the server is a source replication server, it treats threads associated with currently connected replicas
like other client threads. That is, each one is marked as killed and exits when it next checks its state.

If the server is a replica, it stops the I/O and SQL threads, if they are active, before marking client
threads as killed. The SQL thread is permitted to finish its current statement (to avoid causing
replication problems), and then stops. If the SQL thread is in the middle of a transaction at this point,
the server waits until the current replication event group (if any) has finished executing, or until the user
issues a KILL QUERY or KILL CONNECTION statement. See also Section 13.4.2.6, “STOP SLAVE
Statement”. Since nontransactional statements cannot be rolled back, in order to guarantee crash-safe
replication, only transactional tables should be used.

Note

To guarantee crash safety on the replica, you must run the replica with --
relay-log-recovery enabled.

See also Section 16.2.4, “Relay Log and Replication Metadata Repositories”).

5. The server shuts down or closes storage engines.

At this stage, the server flushes the table cache and closes all open tables.

Each storage engine performs any actions necessary for tables that it manages. InnoDB flushes its
buffer pool to disk (unless innodb_fast_shutdown is 2), writes the current LSN to the tablespace,
and terminates its own internal threads. MyISAM flushes any pending index writes for a table.

6. The server exits.

966

The MySQL Data Directory

To provide information to management processes, the server returns one of the exit codes described in the
following list. The phrase in parentheses indicates the action taken by systemd in response to the code, for
platforms on which systemd is used to manage the server.

• 0 = successful termination (no restart done)

• 1 = unsuccessful termination (no restart done)

• 2 = unsuccessful termination (restart done)

5.2 The MySQL Data Directory

Information managed by the MySQL server is stored under a directory known as the data directory. The
following list briefly describes the items typically found in the data directory, with cross references for
additional information:

• Data directory subdirectories. Each subdirectory of the data directory is a database directory and
corresponds to a database managed by the server. All MySQL installations have certain standard
databases:

• The mysql directory corresponds to the mysql system database, which contains information required

by the MySQL server as it runs. See Section 5.3, “The mysql System Database”.

• The performance_schema directory corresponds to the Performance Schema, which provides

information used to inspect the internal execution of the server at runtime. See Chapter 25, MySQL
Performance Schema.

• The sys directory corresponds to the sys schema, which provides a set of objects to help interpret

Performance Schema information more easily. See Chapter 26, MySQL sys Schema.

• The ndbinfo directory corresponds to the ndbinfo database that stores information specific to NDB
Cluster (present only for installations built to include NDB Cluster). See Section 21.6.15, “ndbinfo: The
NDB Cluster Information Database”.

Other subdirectories correspond to databases created by users or applications.

Note

INFORMATION_SCHEMA is a standard database, but its implementation uses no
corresponding database directory.

• Log files written by the server. See Section 5.4, “MySQL Server Logs”.

• InnoDB tablespace and log files. See Chapter 14, The InnoDB Storage Engine.

• Default/autogenerated SSL and RSA certificate and key files. See Section 6.3.3, “Creating SSL and RSA

Certificates and Keys”.

• The server process ID file (while the server is running).

Some items in the preceding list can be relocated elsewhere by reconfiguring the server. In addition, the
--datadir option enables the location of the data directory itself to be changed. For a given MySQL
installation, check the server configuration to determine whether items have been moved.

5.3 The mysql System Database

The mysql database is the system database. It contains tables that store information required by the
MySQL server as it runs.

967

Grant System Tables

Tables in the mysql database fall into these categories:

• Grant System Tables

• Object Information System Tables

• Log System Tables

• Server-Side Help System Tables

• Time Zone System Tables

• Replication System Tables

• Optimizer System Tables

• Miscellaneous System Tables

The remainder of this section enumerates the tables in each category, with cross references for additional
information. System tables use the MyISAM storage engine unless otherwise indicated.

Warning

Do not convert MySQL system tables in the mysql database from MyISAM to
InnoDB tables. This is an unsupported operation. If you do this, MySQL does not
restart until you restore the old system tables from a backup or regenerate them by
reinitializing the data directory (see Section 2.9.1, “Initializing the Data Directory”).

Grant System Tables

These system tables contain grant information about user accounts and the privileges held by them:

• user: User accounts, global privileges, and other nonprivilege columns.

• db: Database-level privileges.

• tables_priv: Table-level privileges.

• columns_priv: Column-level privileges.

• procs_priv: Stored procedure and function privileges.

• proxies_priv: Proxy-user privileges.

For more information about the structure, contents, and purpose of the grant tables, see Section 6.2.3,
“Grant Tables”.

Object Information System Tables

These system tables contain information about stored programs, loadable functions, and server-side
plugins:

• event: The registry for Event Scheduler events installed using CREATE EVENT. If the server is started
with the --skip-grant-tables option, the event scheduler is disabled and events registered in the
table do not run. See Section 23.4.2, “Event Scheduler Configuration”.

• func: The registry for loadable functions installed using CREATE FUNCTION. During the normal startup
sequence, the server loads functions registered in this table. If the server is started with the --skip-
grant-tables option, functions registered in the table are not loaded and are unavailable. See
Section 5.6.1, “Installing and Uninstalling Loadable Functions”.

968

Log System Tables

• plugin: The registry for server-side plugins installed using INSTALL PLUGIN. During the normal

startup sequence, the server loads plugins registered in this table. If the server is started with the --
skip-grant-tables option, plugins registered in the table are not loaded and are unavailable. See
Section 5.5.1, “Installing and Uninstalling Plugins”.

The plugin table uses the InnoDB storage engine as of MySQL 5.7.6, MyISAM before that.

• proc: Information about stored procedures and functions. See Section 23.2, “Using Stored Routines”.

Log System Tables

The server uses these system tables for logging:

•   general_log: The general query log table.

•   slow_log: The slow query log table.

Log tables use the CSV storage engine.

For more information, see Section 5.4, “MySQL Server Logs”.

Server-Side Help System Tables

These system tables contain server-side help information:

•   help_category: Information about help categories.

•   help_keyword: Keywords associated with help topics.

•   help_relation: Mappings between help keywords and topics.

•   help_topic: Help topic contents.

These tables use the InnoDB storage engine as of MySQL 5.7.5, MyISAM before that.

For more information, see Section 5.1.14, “Server-Side Help Support”.

Time Zone System Tables

These system tables contain time zone information:

•   time_zone: Time zone IDs and whether they use leap seconds.

•   time_zone_leap_second: When leap seconds occur.

•   time_zone_name: Mappings between time zone IDs and names.

•     time_zone_transition, time_zone_transition_type: Time zone descriptions.

These tables use the InnoDB storage engine as of MySQL 5.7.5, MyISAM before that.

For more information, see Section 5.1.13, “MySQL Server Time Zone Support”.

Replication System Tables

The server uses these system tables to support replication:

•   gtid_executed: Table for storing GTID values. See mysql.gtid_executed Table.

The gtid_executed table uses the InnoDB storage engine.

969

Optimizer System Tables

•   ndb_binlog_index: Binary log information for NDB Cluster replication. See Section 21.7.4, “NDB

Cluster Replication Schema and Tables”.

Prior to NDB 7.5.2, this table employed the MyISAM storage engine. In NDB 7.5.2 and later, it uses
InnoDB. If you are planning an upgrade from a NDB Cluster previous release to NDB 7.5.2 or later, see
Section 21.3.7, “Upgrading and Downgrading NDB Cluster”, for important information relating to this
change.

•       slave_master_info, slave_relay_log_info, slave_worker_info: Used to store

replication information on replica servers. See Section 16.2.4, “Relay Log and Replication Metadata
Repositories”.

All three of these tables use the InnoDB storage engine.

Optimizer System Tables

These system tables are for use by the optimizer:

•     innodb_index_stats, innodb_table_stats: Used for InnoDB persistent optimizer statistics.

See Section 14.8.11.1, “Configuring Persistent Optimizer Statistics Parameters”.

•     server_cost, engine_cost: The optimizer cost model uses tables that contain cost estimate

information about operations that occur during query execution. server_cost contains optimizer cost
estimates for general server operations. engine_cost contains estimates for operations specific to
particular storage engines. See Section 8.9.5, “The Optimizer Cost Model”.

These tables use the InnoDB storage engine.

Miscellaneous System Tables

Other system tables do not fall into the preceding categories:

•     audit_log_filter, audit_log_user: If MySQL Enterprise Audit is installed, these tables provide

persistent storage of audit log filter definitions and user accounts. See Audit Log Tables.

•     firewall_users, firewall_whitelist: If MySQL Enterprise Firewall is installed, these tables
provide persistent storage for information used by the firewall. See Section 6.4.6, “MySQL Enterprise
Firewall”.

•   servers: Used by the FEDERATED storage engine. See Section 15.8.2.2, “Creating a FEDERATED

Table Using CREATE SERVER”.

The servers table uses the InnoDB storage engine as of MySQL 5.7.6, MyISAM before that.

5.4 MySQL Server Logs

MySQL Server has several logs that can help you find out what activity is taking place.

Log Type

Error log

General query log

Binary log

970

Information Written to Log

Problems encountered starting, running, or stopping
mysqld

Established client connections and statements
received from clients

Statements that change data (also used for
replication)

Selecting General Query Log and Slow Query Log Output Destinations

Log Type

Relay log

Slow query log

Information Written to Log

Data changes received from a replication source
server

Queries that took more than long_query_time
seconds to execute

DDL log (metadata log)

Metadata operations performed by DDL statements

By default, no logs are enabled, except the error log on Windows. (The DDL log is always created when
required, and has no user-configurable options; see Section 5.4.6, “The DDL Log”.) The following log-
specific sections provide information about the server options that enable logging.

By default, the server writes files for all enabled logs in the data directory. You can force the server
to close and reopen the log files (or in some cases switch to a new log file) by flushing the logs. Log
flushing occurs when you issue a FLUSH LOGS statement; execute mysqladmin with a flush-logs or
refresh argument; or execute mysqldump with a --flush-logs option. See Section 13.7.6.3, “FLUSH
Statement”, Section 4.5.2, “mysqladmin — A MySQL Server Administration Program”, and Section 4.5.4,
“mysqldump — A Database Backup Program”. In addition, the binary log is flushed when its size reaches
the value of the max_binlog_size system variable.

You can control the general query and slow query logs during runtime. You can enable or disable logging,
or change the log file name. You can tell the server to write general query and slow query entries to log
tables, log files, or both. For details, see Section 5.4.1, “Selecting General Query Log and Slow Query Log
Output Destinations”, Section 5.4.3, “The General Query Log”, and Section 5.4.5, “The Slow Query Log”.

The relay log is used only on replicas, to hold data changes from the replication source server that must
also be made on the replica. For discussion of relay log contents and configuration, see Section 16.2.4.1,
“The Relay Log”.

For information about log maintenance operations such as expiration of old log files, see Section 5.4.7,
“Server Log Maintenance”.

For information about keeping logs secure, see Section 6.1.2.3, “Passwords and Logging”.

5.4.1 Selecting General Query Log and Slow Query Log Output Destinations

MySQL Server provides flexible control over the destination of output written to the general query log
and the slow query log, if those logs are enabled. Possible destinations for log entries are log files or the
general_log and slow_log tables in the mysql system database. File output, table output, or both can
be selected.

• Log Control at Server Startup

• Log Control at Runtime

• Log Table Benefits and Characteristics

Log Control at Server Startup

The log_output system variable specifies the destination for log output. Setting this variable does not in
itself enable the logs; they must be enabled separately.

• If log_output is not specified at startup, the default logging destination is FILE.

• If log_output is specified at startup, its value is a list one or more comma-separated words chosen
from TABLE (log to tables), FILE (log to files), or NONE (do not log to tables or files). NONE, if present,
takes precedence over any other specifiers.

971

Selecting General Query Log and Slow Query Log Output Destinations

The general_log system variable controls logging to the general query log for the selected log
destinations. If specified at server startup, general_log takes an optional argument of 1 or 0 to enable or
disable the log. To specify a file name other than the default for file logging, set the general_log_file
variable. Similarly, the slow_query_log variable controls logging to the slow query log for the selected
destinations and setting slow_query_log_file specifies a file name for file logging. If either log is
enabled, the server opens the corresponding log file and writes startup messages to it. However, further
logging of queries to the file does not occur unless the FILE log destination is selected.

Examples:

• To write general query log entries to the log table and the log file, use --log_output=TABLE,FILE to

select both log destinations and --general_log to enable the general query log.

• To write general and slow query log entries only to the log tables, use --log_output=TABLE to select

tables as the log destination and --general_log and --slow_query_log to enable both logs.

• To write slow query log entries only to the log file, use --log_output=FILE to select files as the log

destination and --slow_query_log to enable the slow query log. In this case, because the default log
destination is FILE, you could omit the log_output setting.

Log Control at Runtime

The system variables associated with log tables and files enable runtime control over logging:

• The log_output variable indicates the current logging destination. It can be modified at runtime to

change the destination.

• The general_log and slow_query_log variables indicate whether the general query log and slow

query log are enabled (ON) or disabled (OFF). You can set these variables at runtime to control whether
the logs are enabled.

• The general_log_file and slow_query_log_file variables indicate the names of the general

query log and slow query log files. You can set these variables at server startup or at runtime to change
the names of the log files.

• To disable or enable general query logging for the current session, set the session sql_log_off

variable to ON or OFF. (This assumes that the general query log itself is enabled.)

Log Table Benefits and Characteristics

The use of tables for log output offers the following benefits:

• Log entries have a standard format. To display the current structure of the log tables, use these

statements:

SHOW CREATE TABLE mysql.general_log;
SHOW CREATE TABLE mysql.slow_log;

• Log contents are accessible through SQL statements. This enables the use of queries that select only
those log entries that satisfy specific criteria. For example, to select log contents associated with a
particular client (which can be useful for identifying problematic queries from that client), it is easier to do
this using a log table than a log file.

• Logs are accessible remotely through any client that can connect to the server and issue queries (if the
client has the appropriate log table privileges). It is not necessary to log in to the server host and directly
access the file system.

972

Selecting General Query Log and Slow Query Log Output Destinations

The log table implementation has the following characteristics:

• In general, the primary purpose of log tables is to provide an interface for users to observe the runtime

execution of the server, not to interfere with its runtime execution.

• CREATE TABLE, ALTER TABLE, and DROP TABLE are valid operations on a log table. For ALTER
TABLE and DROP TABLE, the log table cannot be in use and must be disabled, as described later.

• By default, the log tables use the CSV storage engine that writes data in comma-separated values

format. For users who have access to the .CSV files that contain log table data, the files are easy to
import into other programs such as spreadsheets that can process CSV input.

The log tables can be altered to use the MyISAM storage engine. You cannot use ALTER TABLE to alter
a log table that is in use. The log must be disabled first. No engines other than CSV or MyISAM are legal
for the log tables.

Log Tables and “Too many open files” Errors.
If you select TABLE as a log destination and the log tables use the CSV storage engine, you may find that
disabling and enabling the general query log or slow query log repeatedly at runtime results in a number
of open file descriptors for the .CSV file, possibly resulting in a “Too many open files” error. To work
around this issue, execute FLUSH TABLES or ensure that the value of open_files_limit is greater
than the value of table_open_cache_instances.

• To disable logging so that you can alter (or drop) a log table, you can use the following strategy.

The example uses the general query log; the procedure for the slow query log is similar but uses the
slow_log table and slow_query_log system variable.

SET @old_log_state = @@GLOBAL.general_log;
SET GLOBAL general_log = 'OFF';
ALTER TABLE mysql.general_log ENGINE = MyISAM;
SET GLOBAL general_log = @old_log_state;

• TRUNCATE TABLE is a valid operation on a log table. It can be used to expire log entries.

• RENAME TABLE is a valid operation on a log table. You can atomically rename a log table (to perform log

rotation, for example) using the following strategy:

USE mysql;
DROP TABLE IF EXISTS general_log2;
CREATE TABLE general_log2 LIKE general_log;
RENAME TABLE general_log TO general_log_backup, general_log2 TO general_log;

• CHECK TABLE is a valid operation on a log table.

• LOCK TABLES cannot be used on a log table.

• INSERT, DELETE, and UPDATE cannot be used on a log table. These operations are permitted only

internally to the server itself.

• FLUSH TABLES WITH READ LOCK and the state of the read_only system variable have no effect on

log tables. The server can always write to the log tables.

• Entries written to the log tables are not written to the binary log and thus are not replicated to replicas.

• To flush the log tables or log files, use FLUSH TABLES or FLUSH LOGS, respectively.

• Partitioning of log tables is not permitted.

• A mysqldump dump includes statements to recreate those tables so that they are not missing after

reloading the dump file. Log table contents are not dumped.

973

5.4.2 The Error Log

The Error Log

This section discusses how to configure the MySQL server for logging of diagnostic messages to the error
log. For information about selecting the error message character set and language, see Section 10.6,
“Error Message Character Set”, and Section 10.12, “Setting the Error Message Language”.

The error log contains a record of mysqld startup and shutdown times. It also contains diagnostic
messages such as errors, warnings, and notes that occur during server startup and shutdown, and while
the server is running. For example, if mysqld notices that a table needs to be automatically checked or
repaired, it writes a message to the error log.

On some operating systems, the error log contains a stack trace if mysqld exits abnormally. The trace can
be used to determine where mysqld exited. See Section 5.8, “Debugging MySQL”.

If used to start mysqld, mysqld_safe may write messages to the error log. For example, when
mysqld_safe notices abnormal mysqld exits, it restarts mysqld and writes a mysqld restarted
message to the error log.

The following sections discuss aspects of configuring error logging. In the discussion, “console” means
stderr, the standard error output. This is your terminal or console window unless the standard error
output has been redirected to a different destination.

The server interprets options that determine where to write error messages somewhat differently for
Windows and Unix systems. Be sure to configure error logging using the information appropriate to your
platform.

5.4.2.1 Error Logging on Windows

On Windows, mysqld uses the --log-error, --pid-file, and --console options to determine
whether mysqld writes the error log to the console or a file, and, if to a file, the file name:

• If --console is given, mysqld writes the error log to the console. (--console takes precedence over
--log-error if both are given, and the following items regarding --log-error do not apply. Prior to
MySQL 5.7, this is reversed: --log-error takes precedence over --console.)

• If --log-error is not given, or is given without naming a file, mysqld writes the error log to a file

named host_name.err in the data directory, unless the --pid-file option is specified. In that case,
the file name is the PID file base name with a suffix of .err in the data directory.

• If --log-error is given to name a file, mysqld writes the error log to that file (with an .err suffix

added if the name has no suffix). The file location is under the data directory unless an absolute path
name is given to specify a different location.

If the server writes the error log to the console, it sets the log_error system variable to stderr.
Otherwise, the server writes the error log to a file and sets log_error to the file name.

In addition, the server by default writes events and error messages to the Windows Event Log within the
Application log:

• Entries marked as Error, Warning, and Note are written to the Event Log, but not messages such as

information statements from individual storage engines.

• Event Log entries have a source of MySQL.

• Information written to the Event Log is controlled using the log_syslog system variable, which on

Windows is enabled by default. See Section 5.4.2.3, “Error Logging to the System Log”.

974

5.4.2.2 Error Logging on Unix and Unix-Like Systems

The Error Log

On Unix and Unix-like systems, mysqld uses the --log-error option to determine whether mysqld
writes the error log to the console or a file, and, if to a file, the file name:

• If --log-error is not given, mysqld writes the error log to the console.

• If --log-error is given without naming a file, mysqld writes the error log to a file named

host_name.err in the data directory.

• If --log-error is given to name a file, mysqld writes the error log to that file (with an .err suffix

added if the name has no suffix). The file location is under the data directory unless an absolute path
name is given to specify a different location.

• If --log-error is given in an option file in a [mysqld], [server], or [mysqld_safe] section,

on systems that use mysqld_safe to start the server, mysqld_safe finds and uses the option, and
passes it to mysqld.

Note

It is common for Yum or APT package installations to configure an error log
file location under /var/log with an option like log-error=/var/log/
mysqld.log in a server configuration file. Removing the path name from the
option causes the host_name.err file in the data directory to be used.

If the server writes the error log to the console, it sets the log_error system variable to stderr.
Otherwise, the server writes the error log to a file and sets log_error to the file name.

5.4.2.3 Error Logging to the System Log

It is possible to have mysqld write the error log to the system log (the Event Log on Windows, and
syslog on Unix and Unix-like systems). To do so, use these system variables:

• log_syslog: Enable this variable to send the error log to the system log. (On Windows, log_syslog

is enabled by default.)

If log_syslog is enabled, the following system variables can also be used for finer control.

• log_syslog_facility: The default facility for syslog messages is daemon. Set this variable to

specify a different facility.

• log_syslog_include_pid: Whether to include the server process ID in each line of syslog output.

• log_syslog_tag: This variable defines a tag to add to the server identifier (mysqld) in syslog

messages. If defined, the tag is appended to the identifier with a leading hyphen.

Note

Error logging to the system log may require additional system configuration. Consult
the system log documentation for your platform.

On Unix and Unix-like systems, control of output to syslog is also available using mysqld_safe, which
can capture server error output and pass it to syslog.

Note

Using mysqld_safe for syslog error logging is deprecated; you should use the
server system variables instead.

975

The General Query Log

mysqld_safe has three error-logging options, --syslog, --skip-syslog, and --log-error. The
default with no logging options or with --skip-syslog is to use the default log file. To explicitly specify
use of an error log file, specify --log-error=file_name to mysqld_safe, which then arranges for
mysqld to write messages to a log file. To use syslog, specify the --syslog option. For syslog output,
a tag can be specified with --syslog-tag=tag_val; this is appended to the mysqld server identifier
with a leading hyphen.

5.4.2.4 Error Log Filtering

The log_error_verbosity system variable controls server verbosity for writing error, warning, and
note messages to the error log. Permitted values are 1 (errors only), 2 (errors and warnings), 3 (errors,
warnings, and notes), with a default of 3. If the value is greater than 2, the server logs aborted connections
and access-denied errors for new connection attempts. See Section B.3.2.9, “Communication Errors and
Aborted Connections”.

5.4.2.5 Error Log Output Format

The ID included in error log messages is that of the thread within mysqld responsible for writing the
message. This indicates which part of the server produced the message, and is consistent with general
query log and slow query log messages, which include the connection thread ID.

The log_timestamps system variable controls the time zone of timestamps in messages written to the
error log (as well as to general query log and slow query log files).

Permitted log_timestamps values are UTC (the default) and SYSTEM (the local system time zone).
Timestamps are written using ISO 8601 / RFC 3339 format: YYYY-MM-DDThh:mm:ss.uuuuuu plus a
tail value of Z signifying Zulu time (UTC) or ±hh:mm (an offset that indicates the local system time zone
adjustment relative to UTC). For example:

2020-08-07T15:02:00.832521Z            (UTC)
2020-08-07T10:02:00.832521-05:00       (SYSTEM)

5.4.2.6 Error Log File Flushing and Renaming

If you flush the error log using a FLUSH ERROR LOGS or FLUSH LOGS statment, or a mysqladmin
flush-logs command, the server closes and reopens any error log file to which it is writing. To rename
an error log file, do so manually before flushing. Flushing the logs then opens a new file with the original
file name. For example, assuming a log file name of host_name.err, use the following commands to
rename the file and create a new one:

mv host_name.err host_name.err-old
mysqladmin flush-logs error
mv host_name.err-old backup-directory

On Windows, use rename rather than mv.

If the location of the error log file is not writable by the server, the log-flushing operation fails to create a
new log file. For example, on Linux, the server might write the error log to the /var/log/mysqld.log
file, where the /var/log directory is owned by root and is not writable by mysqld. For information about
handling this case, see Section 5.4.7, “Server Log Maintenance”.

If the server is not writing to a named error log file, no error log file renaming occurs when the error log is
flushed.

5.4.3 The General Query Log

The general query log is a general record of what mysqld is doing. The server writes information to this
log when clients connect or disconnect, and it logs each SQL statement received from clients. The general

976

The General Query Log

query log can be very useful when you suspect an error in a client and want to know exactly what the client
sent to mysqld.

Each line that shows when a client connects also includes using connection_type to indicate the
protocol used to establish the connection. connection_type is one of TCP/IP (TCP/IP connection
established without SSL), SSL/TLS (TCP/IP connection established with SSL), Socket (Unix socket file
connection), Named Pipe (Windows named pipe connection), or Shared Memory (Windows shared
memory connection).

mysqld writes statements to the query log in the order that it receives them, which might differ from the
order in which they are executed. This logging order is in contrast with that of the binary log, for which
statements are written after they are executed but before any locks are released. In addition, the query log
may contain statements that only select data while such statements are never written to the binary log.

When using statement-based binary logging on a replication source server, statements received by its
replicas are written to the query log of each replica. Statements are written to the query log of the source if
a client reads events with the mysqlbinlog utility and passes them to the server.

However, when using row-based binary logging, updates are sent as row changes rather than SQL
statements, and thus these statements are never written to the query log when binlog_format is ROW.
A given update also might not be written to the query log when this variable is set to MIXED, depending on
the statement used. See Section 16.2.1.1, “Advantages and Disadvantages of Statement-Based and Row-
Based Replication”, for more information.

By default, the general query log is disabled. To specify the initial general query log state explicitly,
use --general_log[={0|1}]. With no argument or an argument of 1, --general_log enables
the log. With an argument of 0, this option disables the log. To specify a log file name, use --
general_log_file=file_name. To specify the log destination, use the log_output system variable
(as described in Section 5.4.1, “Selecting General Query Log and Slow Query Log Output Destinations”).

Note

If you specify the TABLE log destination, see Log Tables and “Too many open files”
Errors.

If you specify no name for the general query log file, the default name is host_name.log. The server
creates the file in the data directory unless an absolute path name is given to specify a different directory.

To disable or enable the general query log or change the log file name at runtime, use the global
general_log and general_log_file system variables. Set general_log to 0 (or OFF) to disable
the log or to 1 (or ON) to enable it. Set general_log_file to specify the name of the log file. If a log file
already is open, it is closed and the new file is opened.

When the general query log is enabled, the server writes output to any destinations specified by the
log_output system variable. If you enable the log, the server opens the log file and writes startup
messages to it. However, further logging of queries to the file does not occur unless the FILE log
destination is selected. If the destination is NONE, the server writes no queries even if the general log is
enabled. Setting the log file name has no effect on logging if the log destination value does not contain
FILE.

Server restarts and log flushing do not cause a new general query log file to be generated (although
flushing closes and reopens it). To rename the file and create a new one, use the following commands:

$> mv host_name.log host_name-old.log
$> mysqladmin flush-logs general
$> mv host_name-old.log backup-directory

977

The Binary Log

On Windows, use rename rather than mv.

You can also rename the general query log file at runtime by disabling the log:

SET GLOBAL general_log = 'OFF';

With the log disabled, rename the log file externally (for example, from the command line). Then enable the
log again:

SET GLOBAL general_log = 'ON';

This method works on any platform and does not require a server restart.

To disable or enable general query logging for the current session, set the session sql_log_off variable
to ON or OFF. (This assumes that the general query log itself is enabled.)

Passwords in statements written to the general query log are rewritten by the server not to occur literally in
plain text. Password rewriting can be suppressed for the general query log by starting the server with the
--log-raw option. This option may be useful for diagnostic purposes, to see the exact text of statements
as received by the server, but for security reasons is not recommended for production use. See also
Section 6.1.2.3, “Passwords and Logging”.

An implication of password rewriting is that statements that cannot be parsed (due, for example, to syntax
errors) are not written to the general query log because they cannot be known to be password free. Use
cases that require logging of all statements including those with errors should use the --log-raw option,
bearing in mind that this also bypasses password rewriting.

Password rewriting occurs only when plain text passwords are expected. For statements with syntax that
expect a password hash value, no rewriting occurs. If a plain text password is supplied erroneously for
such syntax, the password is logged as given, without rewriting. For example, the following statement is
logged as shown because a password hash value is expected:

CREATE USER 'user1'@'localhost' IDENTIFIED BY PASSWORD 'not-so-secret';

The log_timestamps system variable controls the time zone of timestamps in messages written to the
general query log file (as well as to the slow query log file and the error log). It does not affect the time
zone of general query log and slow query log messages written to log tables, but rows retrieved from those
tables can be converted from the local system time zone to any desired time zone with CONVERT_TZ() or
by setting the session time_zone system variable.

5.4.4 The Binary Log

The binary log contains “events” that describe database changes such as table creation operations or
changes to table data. It also contains events for statements that potentially could have made changes
(for example, a DELETE which matched no rows), unless row-based logging is used. The binary log also
contains information about how long each statement took that updated data. The binary log has two
important purposes:

• For replication, the binary log on a replication source server provides a record of the data changes
to be sent to replicas. The source sends the events contained in its binary log to its replicas, which
execute those events to make the same data changes that were made on the source. See Section 16.2,
“Replication Implementation”.

• Certain data recovery operations require use of the binary log. After a backup has been restored, the

events in the binary log that were recorded after the backup was made are re-executed. These events
bring databases up to date from the point of the backup. See Section 7.5, “Point-in-Time (Incremental)
Recovery”.

978

The Binary Log

The binary log is not used for statements such as SELECT or SHOW that do not modify data. To log all
statements (for example, to identify a problem query), use the general query log. See Section 5.4.3, “The
General Query Log”.

Running a server with binary logging enabled makes performance slightly slower. However, the benefits of
the binary log in enabling you to set up replication and for restore operations generally outweigh this minor
performance decrement.

The binary log is generally resilient to unexpected halts because only complete transactions are logged or
read back. See Section 16.3.2, “Handling an Unexpected Halt of a Replica” for more information.

Passwords in statements written to the binary log are rewritten by the server not to occur literally in plain
text. See also Section 6.1.2.3, “Passwords and Logging”.

The following discussion describes some of the server options and variables that affect the operation of
binary logging. For a complete list, see Section 16.1.6.4, “Binary Logging Options and Variables”.

To enable the binary log, start the server with the --log-bin[=base_name] option. If no base_name
value is given, the default name is the value of the --pid-file option (which by default is the name of
host machine) followed by -bin. If the base name is given, the server writes the file in the data directory
unless the base name is given with a leading absolute path name to specify a different directory. It is
recommended that you specify a base name explicitly rather than using the default of the host name; see
Section B.3.7, “Known Issues in MySQL”, for the reason.

If you supply an extension in the log name (for example, --log-bin=base_name.extension), the
extension is silently removed and ignored.

mysqld appends a numeric extension to the binary log base name to generate binary log file names. The
number increases each time the server creates a new log file, thus creating an ordered series of files. The
server creates a new file in the series each time any of the following events occurs:

• The server is started or restarted

• The server flushes the logs.

• The size of the current log file reaches max_binlog_size.

A binary log file may become larger than max_binlog_size if you are using large transactions because a
transaction is written to the file in one piece, never split between files.

To keep track of which binary log files have been used, mysqld also creates a binary log index file that
contains the names of the binary log files. By default, this has the same base name as the binary log file,
with the extension '.index'. You can change the name of the binary log index file with the --log-bin-
index[=file_name] option. You should not manually edit this file while mysqld is running; doing so
would confuse mysqld.

The term “binary log file” generally denotes an individual numbered file containing database events. The
term “binary log” collectively denotes the set of numbered binary log files plus the index file.

A client that has privileges sufficient to set restricted session system variables (see Section 5.1.8.1,
“System Variable Privileges”) can disable binary logging of its own statements by using a SET
sql_log_bin=OFF statement.

By default, the server logs the length of the event as well as the event itself and uses this to verify that
the event was written correctly. You can also cause the server to write checksums for the events by
setting the binlog_checksum system variable. When reading back from the binary log, the source
uses the event length by default, but can be made to use checksums if available by enabling the

979

The Binary Log

master_verify_checksum system variable. The replication I/O thread also verifies events received from
the source. You can cause the replication SQL thread to use checksums if available when reading from the
relay log by enabling the slave_sql_verify_checksum system variable.

The format of the events recorded in the binary log is dependent on the binary logging format. Three format
types are supported, row-based logging, statement-based logging and mixed-base logging. The binary
logging format used depends on the MySQL version. For general descriptions of the logging formats, see
Section 5.4.4.1, “Binary Logging Formats”. For detailed information about the format of the binary log, see
MySQL Internals: The Binary Log.

The server evaluates the --binlog-do-db and --binlog-ignore-db options in the same way as it
does the --replicate-do-db and --replicate-ignore-db options. For information about how this
is done, see Section 16.2.5.1, “Evaluation of Database-Level Replication and Binary Logging Options”.

A replica by default does not write to its own binary log any data modifications that are received from the
source. To log these modifications, start the replica with the --log-slave-updates option in addition to
the --log-bin option (see Section 16.1.6.3, “Replica Server Options and Variables”). This is done when
a replica is also to act as a source to other replicas in chained replication.

You can delete all binary log files with the RESET MASTER statement, or a subset of them with PURGE
BINARY LOGS. See Section 13.7.6.6, “RESET Statement”, and Section 13.4.1.1, “PURGE BINARY LOGS
Statement”.

If you are using replication, you should not delete old binary log files on the source until you are sure that
no replica still needs to use them. For example, if your replicas never run more than three days behind,
once a day you can execute mysqladmin flush-logs binary on the source and then remove any
logs that are more than three days old. You can remove the files manually, but it is preferable to use
PURGE BINARY LOGS, which also safely updates the binary log index file for you (and which can take a
date argument). See Section 13.4.1.1, “PURGE BINARY LOGS Statement”.

You can display the contents of binary log files with the mysqlbinlog utility. This can be useful when you
want to reprocess statements in the log for a recovery operation. For example, you can update a MySQL
server from the binary log as follows:

$> mysqlbinlog log_file | mysql -h server_name

mysqlbinlog also can be used to display relay log file contents because they are written using the
same format as binary log files. For more information on the mysqlbinlog utility and how to use it, see
Section 4.6.7, “mysqlbinlog — Utility for Processing Binary Log Files”. For more information about the
binary log and recovery operations, see Section 7.5, “Point-in-Time (Incremental) Recovery”.

Binary logging is done immediately after a statement or transaction completes but before any locks are
released or any commit is done. This ensures that the log is logged in commit order.

Updates to nontransactional tables are stored in the binary log immediately after execution.

Within an uncommitted transaction, all updates (UPDATE, DELETE, or INSERT) that change transactional
tables such as InnoDB tables are cached until a COMMIT statement is received by the server. At that point,
mysqld writes the entire transaction to the binary log before the COMMIT is executed.

Modifications to nontransactional tables cannot be rolled back. If a transaction that is rolled back includes
modifications to nontransactional tables, the entire transaction is logged with a ROLLBACK statement at the
end to ensure that the modifications to those tables are replicated.

When a thread that handles the transaction starts, it allocates a buffer of binlog_cache_size to buffer
statements. If a statement is bigger than this, the thread opens a temporary file to store the transaction.
The temporary file is deleted when the thread ends.

980

The Binary Log

The Binlog_cache_use status variable shows the number of transactions that used this buffer (and
possibly a temporary file) for storing statements. The Binlog_cache_disk_use status variable shows
how many of those transactions actually had to use a temporary file. These two variables can be used for
tuning binlog_cache_size to a large enough value that avoids the use of temporary files.

The max_binlog_cache_size system variable (default 4GB, which is also the maximum) can be used
to restrict the total size used to cache a multiple-statement transaction. If a transaction is larger than this
many bytes, it fails and rolls back. The minimum value is 4096.

If you are using the binary log and row based logging, concurrent inserts are converted to normal inserts
for CREATE ... SELECT or INSERT ... SELECT statements. This is done to ensure that you can
re-create an exact copy of your tables by applying the log during a backup operation. If you are using
statement-based logging, the original statement is written to the log.

The binary log format has some known limitations that can affect recovery from backups. See
Section 16.4.1, “Replication Features and Issues”.

Binary logging for stored programs is done as described in Section 23.7, “Stored Program Binary Logging”.

Note that the binary log format differs in MySQL 5.7 from previous versions of MySQL, due to
enhancements in replication. See Section 16.4.2, “Replication Compatibility Between MySQL Versions”.

If the server is unable to write to the binary log, flush binary log files, or synchronize the binary log to disk,
the binary log on the source can become inconsistent and replicas can lose synchronization with the
source. The binlog_error_action system variable controls the action taken if an error of this type is
encountered with the binary log.

• The default setting, ABORT_SERVER, makes the server halt binary logging and shut down. At this point,
you can identify and correct the cause of the error. On restart, recovery proceeds as in the case of an
unexpected server halt (see Section 16.3.2, “Handling an Unexpected Halt of a Replica”).

• The setting IGNORE_ERROR provides backward compatibility with older versions of MySQL. With this
setting, the server continues the ongoing transaction and logs the error, then halts binary logging, but
continues to perform updates. At this point, you can identify and correct the cause of the error. To
resume binary logging, log_bin must be enabled again, which requires a server restart. Only use this
option if you require backward compatibility, and the binary log is non-essential on this MySQL server
instance. For example, you might use the binary log only for intermittent auditing or debugging of the
server, and not use it for replication from the server or rely on it for point-in-time restore operations.

By default, the binary log is synchronized to disk at each write (sync_binlog=1). If sync_binlog was
not enabled, and the operating system or machine (not only the MySQL server) crashed, there is a chance
that the last statements of the binary log could be lost. To prevent this, enable the sync_binlog system
variable to synchronize the binary log to disk after every N commit groups. See Section 5.1.7, “Server
System Variables”. The safest value for sync_binlog is 1 (the default), but this is also the slowest.

For example, if you are using InnoDB tables and the MySQL server processes a COMMIT statement, it
writes many prepared transactions to the binary log in sequence, synchronizes the binary log, and then
commits this transaction into InnoDB. If the server unexpectedly exits between those two operations, the
transaction is rolled back by InnoDB at restart but still exists in the binary log. Such an issue is resolved
assuming --innodb_support_xa is set to 1, the default. Although this option is related to the support
of XA transactions in InnoDB, it also ensures that the binary log and InnoDB data files are synchronized.
For this option to provide a greater degree of safety, the MySQL server should also be configured to
synchronize the binary log and the InnoDB logs to disk before committing the transaction. The InnoDB
logs are synchronized by default, and sync_binlog=1 can be used to synchronize the binary log. The
effect of this option is that at restart after a crash, after doing a rollback of transactions, the MySQL server
scans the latest binary log file to collect transaction xid values and calculate the last valid position in the
binary log file. The MySQL server then tells InnoDB to complete any prepared transactions that were

981

The Binary Log

successfully written to the to the binary log, and truncates the binary log to the last valid position. This
ensures that the binary log reflects the exact data of InnoDB tables, and therefore the replica remains in
synchrony with the source because it does not receive a statement which has been rolled back.

Note

innodb_support_xa is deprecated; expect it to be removed in a future release.
InnoDB support for two-phase commit in XA transactions is always enabled as of
MySQL 5.7.10.

If the MySQL server discovers at crash recovery that the binary log is shorter than it should have been, it
lacks at least one successfully committed InnoDB transaction. This should not happen if sync_binlog=1
and the disk/file system do an actual sync when they are requested to (some do not), so the server prints
an error message The binary log file_name is shorter than its expected size. In this
case, this binary log is not correct and replication should be restarted from a fresh snapshot of the source's
data.

The session values of the following system variables are written to the binary log and honored by the
replica when parsing the binary log:

• sql_mode (except that the NO_DIR_IN_CREATE mode is not replicated; see Section 16.4.1.37,

“Replication and Variables”)

• foreign_key_checks

• unique_checks

• character_set_client

• collation_connection

• collation_database

• collation_server

• sql_auto_is_null

5.4.4.1 Binary Logging Formats

The server uses several logging formats to record information in the binary log. The exact format employed
depends on the version of MySQL being used. There are three logging formats:

• Replication capabilities in MySQL originally were based on propagation of SQL statements from source
to replica. This is called statement-based logging. You can cause this format to be used by starting the
server with --binlog-format=STATEMENT.

• In row-based logging, the source writes events to the binary log that indicate how individual table

rows are affected. It is important therefore that tables always use a primary key to ensure rows can be
efficiently identified. You can cause the server to use row-based logging by starting it with --binlog-
format=ROW.

• A third option is also available: mixed logging. With mixed logging, statement-based logging is used by
default, but the logging mode switches automatically to row-based in certain cases as described below.
You can cause MySQL to use mixed logging explicitly by starting mysqld with the option --binlog-
format=MIXED.

The logging format can also be set or limited by the storage engine being used. This helps to eliminate
issues when replicating certain statements between a source and replica which are using different storage
engines.

982

The Binary Log

With statement-based replication, there may be issues with replicating nondeterministic statements. In
deciding whether or not a given statement is safe for statement-based replication, MySQL determines
whether it can guarantee that the statement can be replicated using statement-based logging. If MySQL
cannot make this guarantee, it marks the statement as potentially unreliable and issues the warning,
Statement may not be safe to log in statement format.

You can avoid these issues by using MySQL's row-based replication instead.

5.4.4.2 Setting The Binary Log Format

You can select the binary logging format explicitly by starting the MySQL server with --binlog-
format=type. The supported values for type are:

• STATEMENT causes logging to be statement based.

• ROW causes logging to be row based.

• MIXED causes logging to use mixed format.

Setting the binary logging format does not activate binary logging for the server. The setting only takes
effect when binary logging is enabled on the server, which is the case when the log_bin system variable
is set to ON. In MySQL 5.7, binary logging is not enabled by default, and you enable it using the --log-
bin option.

The logging format also can be switched at runtime, although note that there are a number of situations in
which you cannot do this, as discussed later in this section. Set the global value of the binlog_format
system variable to specify the format for clients that connect subsequent to the change:

mysql> SET GLOBAL binlog_format = 'STATEMENT';
mysql> SET GLOBAL binlog_format = 'ROW';
mysql> SET GLOBAL binlog_format = 'MIXED';

An individual client can control the logging format for its own statements by setting the session value of
binlog_format:

mysql> SET SESSION binlog_format = 'STATEMENT';
mysql> SET SESSION binlog_format = 'ROW';
mysql> SET SESSION binlog_format = 'MIXED';

Changing the global binlog_format value requires privileges sufficient to set global system variables.
Changing the session binlog_format value requires privileges sufficient to set restricted session system
variables. See Section 5.1.8.1, “System Variable Privileges”.

There are several reasons why a client might want to set binary logging on a per-session basis:

• A session that makes many small changes to the database might want to use row-based logging.

• A session that performs updates that match many rows in the WHERE clause might want to use
statement-based logging because it is more efficient to log a few statements than many rows.

• Some statements require a lot of execution time on the source, but result in just a few rows being

modified. It might therefore be beneficial to replicate them using row-based logging.

There are exceptions when you cannot switch the replication format at runtime:

• From within a stored function or a trigger.

• If the NDB storage engine is enabled.

• If the session is currently in row-based replication mode and has open temporary tables.

983

The Binary Log

Trying to switch the format in any of these cases results in an error.

Switching the replication format at runtime is not recommended when any temporary tables exist, because
temporary tables are logged only when using statement-based replication, whereas with row-based
replication they are not logged. With mixed replication, temporary tables are usually logged; exceptions
happen with loadable functions and with the UUID() function.

Switching the replication format while replication is ongoing can also cause issues. Each MySQL
Server can set its own and only its own binary logging format (true whether binlog_format is set
with global or session scope). This means that changing the logging format on a replication source
server does not cause a replica to change its logging format to match. When using STATEMENT mode,
the binlog_format system variable is not replicated. When using MIXED or ROW logging mode, it is
replicated but is ignored by the replica.

A replica is not able to convert binary log entries received in ROW logging format to STATEMENT format
for use in its own binary log. The replica must therefore use ROW or MIXED format if the source does.
Changing the binary logging format on the source from STATEMENT to ROW or MIXED while replication
is ongoing to a replica with STATEMENT format can cause replication to fail with errors such as Error
executing row event: 'Cannot execute statement: impossible to write to binary
log since statement is in row format and BINLOG_FORMAT = STATEMENT.' Changing
the binary logging format on the replica to STATEMENT format when the source is still using MIXED or
ROW format also causes the same type of replication failure. To change the format safely, you must stop
replication and ensure that the same change is made on both the source and the replica.

If you are using InnoDB tables and the transaction isolation level is READ COMMITTED or READ
UNCOMMITTED, only row-based logging can be used. It is possible to change the logging format to
STATEMENT, but doing so at runtime leads very rapidly to errors because InnoDB can no longer perform
inserts.

With the binary log format set to ROW, many changes are written to the binary log using the row-based
format. Some changes, however, still use the statement-based format. Examples include all DDL (data
definition language) statements such as CREATE TABLE, ALTER TABLE, or DROP TABLE.

The --binlog-row-event-max-size option is available for servers that are capable of row-based
replication. Rows are stored into the binary log in chunks having a size in bytes not exceeding the value of
this option. The value must be a multiple of 256. The default value is 8192.

Warning

When using statement-based logging for replication, it is possible for the data on
the source and replica to become different if a statement is designed in such a way
that the data modification is nondeterministic; that is, it is left to the will of the query
optimizer. In general, this is not a good practice even outside of replication. For a
detailed explanation of this issue, see Section B.3.7, “Known Issues in MySQL”.

5.4.4.3 Mixed Binary Logging Format

When running in MIXED logging format, the server automatically switches from statement-based to row-
based logging under the following conditions:

• When a DML statement updates an NDBCLUSTER table.

• When a function contains UUID().

• When one or more tables with AUTO_INCREMENT columns are updated and a trigger or stored

function is invoked. Like all other unsafe statements, this generates a warning if binlog_format =
STATEMENT.

984

The Binary Log

For more information, see Section 16.4.1.1, “Replication and AUTO_INCREMENT”.

• When the body of a view requires row-based replication, the statement creating the view also uses it. For

example, this occurs when the statement creating a view uses the UUID() function.

• When a call to a loadable function is involved.

• If a statement is logged by row and the session that executed the statement has any temporary tables,

logging by row is used for all subsequent statements (except for those accessing temporary tables) until
all temporary tables in use by that session are dropped.

This is true whether or not any temporary tables are actually logged.

Temporary tables cannot be logged using row-based format; thus, once row-based logging is used, all
subsequent statements using that table are unsafe. The server approximates this condition by treating
all statements executed during the session as unsafe until the session no longer holds any temporary
tables.

• When FOUND_ROWS() or ROW_COUNT() is used. (Bug #12092, Bug #30244)

• When USER(), CURRENT_USER(), or CURRENT_USER is used. (Bug #28086)

• When a statement refers to one or more system variables. (Bug #31168)

Exception.
logging format to switch:

 The following system variables, when used with session scope (only), do not cause the

• auto_increment_increment

• auto_increment_offset

• character_set_client

• character_set_connection

• character_set_database

• character_set_server

• collation_connection

• collation_database

• collation_server

• foreign_key_checks

• identity

• last_insert_id

• lc_time_names

• pseudo_thread_id

• sql_auto_is_null

• time_zone

985

The Binary Log

• timestamp

• unique_checks

For information about determining system variable scope, see Section 5.1.8, “Using System Variables”.

For information about how replication treats sql_mode, see Section 16.4.1.37, “Replication and
Variables”.

• When one of the tables involved is a log table in the mysql database.

• When the LOAD_FILE() function is used. (Bug #39701)

Note

A warning is generated if you try to execute a statement using statement-based
logging that should be written using row-based logging. The warning is shown both
in the client (in the output of SHOW WARNINGS) and through the mysqld error log.
A warning is added to the SHOW WARNINGS table each time such a statement is
executed. However, only the first statement that generated the warning for each
client session is written to the error log to prevent flooding the log.

In addition to the decisions above, individual engines can also determine the logging format used when
information in a table is updated. The logging capabilities of an individual engine can be defined as follows:

• If an engine supports row-based logging, the engine is said to be row-logging capable.

• If an engine supports statement-based logging, the engine is said to be statement-logging capable.

A given storage engine can support either or both logging formats. The following table lists the formats
supported by each engine.

Storage Engine

Row Logging Supported

Statement Logging Supported

ARCHIVE

BLACKHOLE

CSV

EXAMPLE

FEDERATED

HEAP

InnoDB

MyISAM

MERGE

NDB

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

Yes

No

Yes

Yes

Yes when the transaction isolation
level is REPEATABLE READ or
SERIALIZABLE; No otherwise.

Yes

Yes

No

Whether a statement is to be logged and the logging mode to be used is determined according to the type
of statement (safe, unsafe, or binary injected), the binary logging format (STATEMENT, ROW, or MIXED), and
the logging capabilities of the storage engine (statement capable, row capable, both, or neither). (Binary
injection refers to logging a change that must be logged using ROW format.)

Statements may be logged with or without a warning; failed statements are not logged, but generate errors
in the log. This is shown in the following decision table. Type, binlog_format, SLC, and RLC columns

986

The Binary Log

outline the conditions, and Error / Warning and Logged as columns represent the corresponding actions.
SLC stands for “statement-logging capable”, and RLC stands for “row-logging capable”.

Type

*

binlog_formatSLC

*

No

RLC

No

Safe

Safe

Safe

STATEMENT

MIXED

ROW

Yes

Yes

Yes

No

No

No

Unsafe

STATEMENT

Yes

No

Unsafe

MIXED

Yes

No

Error / Warning Logged as

-

STATEMENT

STATEMENT

-

STATEMENT

-

Error:
Cannot
execute
statement:
Binary logging
is impossible
since at least
one engine is
involved that
is both row-
incapable and
statement-
incapable.

-

-

Error:
Cannot
execute
statement:
Binary logging is
impossible since
BINLOG_FORMAT
= ROW and at
least one table
uses a storage
engine that is
not capable
of row-based
logging.

Warning:
Unsafe
statement
binlogged
in statement
format, since
BINLOG_FORMAT
= STATEMENT

Error:
Cannot
execute
statement:
Binary logging
of an unsafe
statement is
impossible
when the
storage engine
is limited to

987

The Binary Log

Type

binlog_formatSLC

RLC

Unsafe

ROW

Yes

No

Row Injection

STATEMENT

Yes

No

Row Injection

MIXED

Yes

No

Row Injection

ROW

Yes

No

Error / Warning Logged as
statement-based
logging, even if
BINLOG_FORMAT
= MIXED.

-

-

-

-

Error:
Cannot
execute
statement:
Binary logging is
impossible since
BINLOG_FORMAT
= ROW and at
least one table
uses a storage
engine that is
not capable
of row-based
logging.

Error:
Cannot
execute row
injection:
Binary logging
is not possible
since at least
one table uses a
storage engine
that is not
capable of row-
based logging.

Error:
Cannot
execute row
injection:
Binary logging
is not possible
since at least
one table uses a
storage engine
that is not
capable of row-
based logging.

Error:
Cannot
execute row
injection:
Binary logging
is not possible
since at least
one table uses a
storage engine

988

The Binary Log

Type

binlog_formatSLC

RLC

Safe

STATEMENT

No

Yes

Safe

Safe

MIXED

ROW

Unsafe

STATEMENT

No

No

No

Yes

Yes

Yes

Unsafe

Unsafe

MIXED

ROW

Row Injection

STATEMENT

No

No

No

Yes

Yes

Yes

Row Injection

MIXED

Row Injection

ROW

No

No

Yes

Yes

-

-

Error / Warning Logged as
that is not
capable of row-
based logging.

-

Error:
Cannot
execute
statement:
Binary logging is
impossible since
BINLOG_FORMAT
= STATEMENT
and at least
one table uses
a storage
engine that is
not capable of
statement-based
logging.

-

-

Error:
Cannot
execute
statement:
Binary logging is
impossible since
BINLOG_FORMAT
= STATEMENT
and at least
one table uses
a storage
engine that is
not capable of
statement-based
logging.

-

-

Error:
Cannot
execute row
injection:
Binary
logging is not
possible since
BINLOG_FORMAT
= STATEMENT.

ROW

ROW

-

ROW

ROW

-

ROW

ROW

989

The Binary Log

binlog_formatSLC

Error / Warning Logged as

Type

Safe

Safe

Safe

STATEMENT

MIXED

ROW

Yes

Yes

Yes

Yes

Unsafe

STATEMENT

Unsafe

Unsafe

MIXED

ROW

Row Injection

STATEMENT

Yes

Yes

Yes

RLC

Yes

Yes

Yes

Yes

Yes

Yes

Yes

-

-

-

Warning:
Unsafe
statement
binlogged
in statement
format since
BINLOG_FORMAT
= STATEMENT.

-

-

Error:
Cannot
execute row
injection:
Binary logging
is not possible
because
BINLOG_FORMAT
= STATEMENT.

STATEMENT

STATEMENT

ROW

STATEMENT

ROW

ROW

-

ROW

ROW

Row Injection

MIXED

Row Injection

ROW

Yes

Yes

Yes

Yes

-

-

When a warning is produced by the determination, a standard MySQL warning is produced (and is
available using SHOW WARNINGS). The information is also written to the mysqld error log. Only one
error for each error instance per client connection is logged to prevent flooding the log. The log message
includes the SQL statement that was attempted.

If log_error_verbosity is 2 or greater on a replica, the replica prints messages to the error log to
provide information about its status, such as the binary log and relay log coordinates where it starts its job,
when it is switching to another relay log, when it reconnects after a disconnect, statements that are unsafe
for statement-based logging, and so forth.

5.4.4.4 Logging Format for Changes to mysql Database Tables

The contents of the grant tables in the mysql database can be modified directly (for example, with INSERT
or DELETE) or indirectly (for example, with GRANT or CREATE USER). Statements that affect mysql
database tables are written to the binary log using the following rules:

• Data manipulation statements that change data in mysql database tables directly are logged according
to the setting of the binlog_format system variable. This pertains to statements such as INSERT,
UPDATE, DELETE, REPLACE, DO, LOAD DATA, SELECT, and TRUNCATE TABLE.

• Statements that change the mysql database indirectly are logged as statements regardless of the value
of binlog_format. This pertains to statements such as GRANT, REVOKE, SET PASSWORD, RENAME
USER, CREATE (all forms except CREATE TABLE ... SELECT), ALTER (all forms), and DROP (all
forms).

990

The Slow Query Log

CREATE TABLE ... SELECT is a combination of data definition and data manipulation. The CREATE
TABLE part is logged using statement format and the SELECT part is logged according to the value of
binlog_format.

5.4.5 The Slow Query Log

The slow query log consists of SQL statements that take more than long_query_time seconds to
execute and require at least min_examined_row_limit rows to be examined. The slow query log can
be used to find queries that take a long time to execute and are therefore candidates for optimization.
However, examining a long slow query log can be a time-consuming task. To make this easier, you can
use the mysqldumpslow command to process a slow query log file and summarize its contents. See
Section 4.6.8, “mysqldumpslow — Summarize Slow Query Log Files”.

The time to acquire the initial locks is not counted as execution time. mysqld writes a statement to the
slow query log after it has been executed and after all locks have been released, so log order might differ
from execution order.

• Slow Query Log Parameters

• Slow Query Log Contents

Slow Query Log Parameters

The minimum and default values of long_query_time are 0 and 10, respectively. The value can be
specified to a resolution of microseconds.

By default, administrative statements are not logged, nor are queries that do not use indexes
for lookups. This behavior can be changed using log_slow_admin_statements and
log_queries_not_using_indexes, as described later.

By default, the slow query log is disabled. To specify the initial slow query log state explicitly, use
--slow_query_log[={0|1}]. With no argument or an argument of 1, --slow_query_log
enables the log. With an argument of 0, this option disables the log. To specify a log file name, use --
slow_query_log_file=file_name. To specify the log destination, use the log_output system
variable (as described in Section 5.4.1, “Selecting General Query Log and Slow Query Log Output
Destinations”).

Note

If you specify the TABLE log destination, see Log Tables and “Too many open files”
Errors.

If you specify no name for the slow query log file, the default name is host_name-slow.log. The server
creates the file in the data directory unless an absolute path name is given to specify a different directory.

To disable or enable the slow query log or change the log file name at runtime, use the global
slow_query_log and slow_query_log_file system variables. Set slow_query_log to 0 to disable
the log or to 1 to enable it. Set slow_query_log_file to specify the name of the log file. If a log file
already is open, it is closed and the new file is opened.

The server writes less information to the slow query log if you use the --log-short-format option.

To include slow administrative statements in the slow query log, enable the
log_slow_admin_statements system variable. Administrative statements include ALTER TABLE,
ANALYZE TABLE, CHECK TABLE, CREATE INDEX, DROP INDEX, OPTIMIZE TABLE, and REPAIR
TABLE.

991

The Slow Query Log

To include queries that do not use indexes for row lookups in the statements written to the slow query log,
enable the log_queries_not_using_indexes system variable. (Even with that variable enabled, the
server does not log queries that would not benefit from the presence of an index due to the table having
fewer than two rows.)

When queries that do not use an index are logged, the slow query log may grow quickly. It is possible
to put a rate limit on these queries by setting the log_throttle_queries_not_using_indexes
system variable. By default, this variable is 0, which means there is no limit. Positive values impose a per-
minute limit on logging of queries that do not use indexes. The first such query opens a 60-second window
within which the server logs queries up to the given limit, then suppresses additional queries. If there are
suppressed queries when the window ends, the server logs a summary that indicates how many there
were and the aggregate time spent in them. The next 60-second window begins when the server logs the
next query that does not use indexes.

The server uses the controlling parameters in the following order to determine whether to write a query to
the slow query log:

1. The query must either not be an administrative statement, or log_slow_admin_statements must

be enabled.

2. The query must have taken at least long_query_time seconds, or

log_queries_not_using_indexes must be enabled and the query used no indexes for row
lookups.

3. The query must have examined at least min_examined_row_limit rows.

4. The query must not be suppressed according to the

log_throttle_queries_not_using_indexes setting.

The log_timestamps system variable controls the time zone of timestamps in messages written to the
slow query log file (as well as to the general query log file and the error log). It does not affect the time
zone of general query log and slow query log messages written to log tables, but rows retrieved from those
tables can be converted from the local system time zone to any desired time zone with CONVERT_TZ() or
by setting the session time_zone system variable.

The server does not log queries handled by the query cache.

By default, a replica does not write replicated queries to the slow query log. To change this, enable
the log_slow_slave_statements system variable. Note that if row-based replication is in use
(binlog_format=ROW), log_slow_slave_statements has no effect. Queries are only added to
the replica's slow query log when they are logged in statement format in the binary log, that is, when
binlog_format=STATEMENT is set, or when binlog_format=MIXED is set and the statement is logged
in statement format. Slow queries that are logged in row format when binlog_format=MIXED is set, or
that are logged when binlog_format=ROW is set, are not added to the replica's slow query log, even if
log_slow_slave_statements is enabled.

Slow Query Log Contents

When the slow query log is enabled, the server writes output to any destinations specified by the
log_output system variable. If you enable the log, the server opens the log file and writes startup
messages to it. However, further logging of queries to the file does not occur unless the FILE log
destination is selected. If the destination is NONE, the server writes no queries even if the slow query log is
enabled. Setting the log file name has no effect on logging if FILE is not selected as an output destination.

If the slow query log is enabled and FILE is selected as an output destination, each statement written to
the log is preceded by a line that begins with a # character and has these fields (with all fields on a single
line):

992

The DDL Log

• Query_time: duration

The statement execution time in seconds.

• Lock_time: duration

The time to acquire locks in seconds.

• Rows_sent: N

The number of rows sent to the client.

• Rows_examined:

The number of rows examined by the server layer (not counting any processing internal to storage
engines).

Each statement written to the slow query log file is preceded by a SET statement that includes a timestamp
indicating when the slow statement was logged (which occurs after the statement finishes executing).

Passwords in statements written to the slow query log are rewritten by the server not to occur literally in
plain text. See Section 6.1.2.3, “Passwords and Logging”.

From MySQL 5.7.38, statements that cannot be parsed (due, for example, to syntax errors) are not written
to the slow query log.

5.4.6 The DDL Log

The DDL log, or metadata log, records metadata operations generated by data definition statements
affecting table partitioning, such as ALTER TABLE t3 DROP PARTITION p2, where we must make
certain that the partition is completely dropped and that its definition is removed from the list of partitions
for table t3. MySQL uses this log to recover from a crash occurring in the middle of a partitioning metadata
operation.

A record of partitioning metadata operations is written to the file ddl_log.log, in the MySQL data
directory. This is a binary file; it is not intended to be human-readable, and you should not attempt to
modify its contents in any way.

ddl_log.log is not created until it is actually needed for recording metadata statements, and is removed
following a successful start of mysqld. Thus, it is possible for this file not to be present on a MySQL server
that is functioning in a completely normal manner.

ddl_log.log can hold up to 1048573 entries, equivalent to 4 GB in size. Once this limit is exceeded, you
must rename or remove the file before it is possible to execute any additional DDL statements. This is a
known issue (Bug #83708).

There are no user-configurable server options or variables associated with this file.

5.4.7 Server Log Maintenance

As described in Section 5.4, “MySQL Server Logs”, MySQL Server can create several different log files to
help you see what activity is taking place. However, you must clean up these files regularly to ensure that
the logs do not take up too much disk space.

When using MySQL with logging enabled, you may want to back up and remove old log files from time to
time and tell MySQL to start logging to new files. See Section 7.2, “Database Backup Methods”.

993

Server Log Maintenance

On a Linux (Red Hat) installation, you can use the mysql-log-rotate script for log maintenance. If you
installed MySQL from an RPM distribution, this script should have been installed automatically. Be careful
with this script if you are using the binary log for replication. You should not remove binary logs until you
are certain that their contents have been processed by all replicas.

On other systems, you must install a short script yourself that you start from cron (or its equivalent) for
handling log files.

For the binary log, you can set the expire_logs_days system variable to expire binary log files
automatically after a given number of days (see Section 5.1.7, “Server System Variables”). If you are using
replication, you should set the variable no lower than the maximum number of days your replicas might
lag behind the source. To remove binary logs on demand, use the PURGE BINARY LOGS statement (see
Section 13.4.1.1, “PURGE BINARY LOGS Statement”).

To force MySQL to start using new log files, flush the logs. Log flushing occurs when you execute a FLUSH
LOGS statement or a mysqladmin flush-logs, mysqladmin refresh, mysqldump --flush-logs,
or mysqldump --master-data command. See Section 13.7.6.3, “FLUSH Statement”, Section 4.5.2,
“mysqladmin — A MySQL Server Administration Program”, and Section 4.5.4, “mysqldump — A Database
Backup Program”. In addition, the server flushes the binary log automatically when current binary log file
size reaches the value of the max_binlog_size system variable.

FLUSH LOGS supports optional modifiers to enable selective flushing of individual logs (for example,
FLUSH BINARY LOGS). See Section 13.7.6.3, “FLUSH Statement”.

A log-flushing operation has the following effects:

• If binary logging is enabled, the server closes the current binary log file and opens a new log file with the

next sequence number.

• If general query logging or slow query logging to a log file is enabled, the server closes and reopens the

log file.

• If the server was started with the --log-error option to cause the error log to be written to a file, the

server closes and reopens the log file.

Execution of log-flushing statements or commands requires connecting to the server using an account
that has the RELOAD privilege. On Unix and Unix-like systems, another way to flush the logs is to send a
SIGHUP signal to the server, which can be done by root or the account that owns the server process.
Signals enable log flushing to be performed without having to connect to the server. However, SIGHUP
has additional effects other than log flushing that might be undesirable. For details, see Section 4.10, “Unix
Signal Handling in MySQL”.

As mentioned previously, flushing the binary log creates a new binary log file, whereas flushing the general
query log, slow query log, or error log just closes and reopens the log file. For the latter logs, to cause
a new log file to be created on Unix, rename the current log file first before flushing it. At flush time, the
server opens the new log file with the original name. For example, if the general query log, slow query log,
and error log files are named mysql.log, mysql-slow.log, and err.log, you can use a series of
commands like this from the command line:

cd mysql-data-directory
mv mysql.log mysql.log.old
mv mysql-slow.log mysql-slow.log.old
mv err.log err.log.old
mysqladmin flush-logs

On Windows, use rename rather than mv.

994

MySQL Server Plugins

At this point, you can make a backup of mysql.log.old, mysql-slow.log.old, and err.log.old,
then remove them from disk.

To rename the general query log or slow query log at runtime, first connect to the server and disable the
log:

SET GLOBAL general_log = 'OFF';
SET GLOBAL slow_query_log = 'OFF';

With the logs disabled, rename the log files externally (for example, from the command line). Then enable
the logs again:

SET GLOBAL general_log = 'ON';
SET GLOBAL slow_query_log = 'ON';

This method works on any platform and does not require a server restart.

Note

For the server to recreate a given log file after you have renamed the file externally,
the file location must be writable by the server. This may not always be the
case. For example, on Linux, the server might write the error log as /var/log/
mysqld.log, where /var/log is owned by root and not writable by mysqld. In
this case, log-flushing operations fail to create a new log file.

To handle this situation, you must manually create the new log file with the
proper ownership after renaming the original log file. For example, execute these
commands as root:

mv /var/log/mysqld.log /var/log/mysqld.log.old
install -omysql -gmysql -m0644 /dev/null /var/log/mysqld.log

5.5 MySQL Server Plugins

MySQL supports an plugin API that enables creation of server plugins. Plugins can be loaded at server
startup, or loaded and unloaded at runtime without restarting the server. The plugins supported by this
interface include, but are not limited to, storage engines, INFORMATION_SCHEMA tables, full-text parser
plugins, partitioning support, and server extensions.

MySQL distributions include several plugins that implement server extensions:

• Plugins for authenticating attempts by clients to connect to MySQL Server. Plugins are available for

several authentication protocols. See Section 6.2.13, “Pluggable Authentication”.

• A connection control plugin that enables administrators to introduce an increasing delay after a certain

number of consecutive failed client connection attempts. See Section 6.4.2, “Connection Control
Plugins”.

• A password-validation plugin implements password strength policies and assesses the strength of

potential passwords. See Section 6.4.3, “The Password Validation Plugin”.

• Semisynchronous replication plugins implement an interface to replication capabilities that permit
the source to proceed as long as at least one replica has responded to each transaction. See
Section 16.3.9, “Semisynchronous Replication”.

• Group Replication enables you to create a highly available distributed MySQL service across a group of

MySQL server instances, with data consistency, conflict detection and resolution, and group membership
services all built-in. See Chapter 17, Group Replication.

995

Installing and Uninstalling Plugins

• MySQL Enterprise Edition includes a thread pool plugin that manages connection threads to increase
server performance by efficiently managing statement execution threads for large numbers of client
connections. See Section 5.5.3, “MySQL Enterprise Thread Pool”.

• MySQL Enterprise Edition includes an audit plugin for monitoring and logging of connection and query

activity. See Section 6.4.5, “MySQL Enterprise Audit”.

• MySQL Enterprise Edition includes a firewall plugin that implements an application-level firewall to

enable database administrators to permit or deny SQL statement execution based on matching against
allowlists of accepted statement patterns. See Section 6.4.6, “MySQL Enterprise Firewall”.

• A query rewrite plugin examines statements received by MySQL Server and possibly rewrites them

before the server executes them. See Section 5.5.4, “The Rewriter Query Rewrite Plugin”.

• Version Tokens enables creation of and synchronization around server tokens that applications can

use to prevent accessing incorrect or out-of-date data. Version Tokens is based on a plugin library that
implements a version_tokens plugin and a set of loadable functions. See Section 5.5.5, “Version
Tokens”.

• Keyring plugins provide secure storage for sensitive information. See Section 6.4.4, “The MySQL

Keyring”.

• X Plugin extends MySQL Server to be able to function as a document store. Running X Plugin enables
MySQL Server to communicate with clients using the X Protocol, which is designed to expose the ACID
compliant storage abilities of MySQL as a document store. See Section 19.4, “X Plugin”.

• Test framework plugins test server services. For information about these plugins, see the Plugins for
Testing Plugin Services section of the MySQL Server Doxygen documentation, available at https://
dev.mysql.com/doc/index-other.html.

The following sections describe how to install and uninstall plugins, and how to determine at runtime which
plugins are installed and obtain information about them. For information about writing plugins, see The
MySQL Plugin API.

5.5.1 Installing and Uninstalling Plugins

Server plugins must be loaded into the server before they can be used. MySQL supports plugin loading at
server startup and runtime. It is also possible to control the activation state of loaded plugins at startup, and
to unload them at runtime.

While a plugin is loaded, information about it is available as described in Section 5.5.2, “Obtaining Server
Plugin Information”.

• Installing Plugins

• Controlling Plugin Activation State

• Uninstalling Plugins

Installing Plugins

Before a server plugin can be used, it must be installed using one of the following methods. In the
descriptions, plugin_name stands for a plugin name such as innodb, csv, or validate_password.

• Built-in Plugins

• Plugins Registered in the mysql.plugin System Table

996

Installing and Uninstalling Plugins

• Plugins Named with Command-Line Options

• Plugins Installed with the INSTALL PLUGIN Statement

Built-in Plugins

A built-in plugin is known by the server automatically. By default, the server enables the plugin at startup.
Some built-in plugins permit this to be changed with the --plugin_name[=activation_state] option.

Plugins Registered in the mysql.plugin System Table

The mysql.plugin system table serves as a registry of plugins (other than built-in plugins, which need
not be registered). During the normal startup sequence, the server loads plugins registered in the table. By
default, for a plugin loaded from the mysql.plugin table, the server also enables the plugin. This can be
changed with the --plugin_name[=activation_state] option.

If the server is started with the --skip-grant-tables option, plugins registered in the mysql.plugin
table are not loaded and are unavailable.

Plugins Named with Command-Line Options

A plugin located in a plugin library file can be loaded at server startup with the --plugin-load, --
plugin-load-add, or --early-plugin-load option. Normally, for a plugin loaded at startup, the
server also enables the plugin. This can be changed with the --plugin_name[=activation_state]
option.

The --plugin-load and --plugin-load-add options load plugins after built-in plugins and storage
engines have initialized during the server startup sequence. The --early-plugin-load option is used
to load plugins that must be available prior to initialization of built-in plugins and storage engines.

The value of each plugin-loading option is a semicolon-separated list of plugin_library and
name=plugin_library values. Each plugin_library is the name of a library file that contains plugin
code, and each name is the name of a plugin to load. If a plugin library is named without any preceding
plugin name, the server loads all plugins in the library. With a preceding plugin name, the server loads
only the named plugin from the libary. The server looks for plugin library files in the directory named by the
plugin_dir system variable.

Plugin-loading options do not register any plugin in the mysql.plugin table. For subsequent restarts,
the server loads the plugin again only if --plugin-load, --plugin-load-add, or --early-plugin-
load is given again. That is, the option produces a one-time plugin-installation operation that persists for a
single server invocation.

--plugin-load, --plugin-load-add, and --early-plugin-load enable plugins to be loaded
even when --skip-grant-tables is given (which causes the server to ignore the mysql.plugin
table). --plugin-load, --plugin-load-add, and --early-plugin-load also enable plugins to be
loaded at startup that cannot be loaded at runtime.

The --plugin-load-add option complements the --plugin-load option:

• Each instance of --plugin-load resets the set of plugins to load at startup, whereas --plugin-

load-add adds a plugin or plugins to the set of plugins to be loaded without resetting the current set.
Consequently, if multiple instances of --plugin-load are specified, only the last one applies. With
multiple instances of --plugin-load-add, all of them apply.

• The argument format is the same as for --plugin-load, but multiple instances of --plugin-load-
add can be used to avoid specifying a large set of plugins as a single long unwieldy --plugin-load
argument.

997

Installing and Uninstalling Plugins

• --plugin-load-add can be given in the absence of --plugin-load, but any instance of --

plugin-load-add that appears before --plugin-load has no effect because --plugin-load
resets the set of plugins to load.

For example, these options:

--plugin-load=x --plugin-load-add=y

are equivalent to these options:

--plugin-load-add=x --plugin-load-add=y

and are also equivalent to this option:

--plugin-load="x;y"

But these options:

--plugin-load-add=y --plugin-load=x

are equivalent to this option:

--plugin-load=x

Plugins Installed with the INSTALL PLUGIN Statement

A plugin located in a plugin library file can be loaded at runtime with the INSTALL PLUGIN statement.
The statement also registers the plugin in the mysql.plugin table to cause the server to load it
on subsequent restarts. For this reason, INSTALL PLUGIN requires the INSERT privilege for the
mysql.plugin table.

The plugin library file base name depends on your platform. Common suffixes are .so for Unix and Unix-
like systems, .dll for Windows.

Example: The --plugin-load-add option installs a plugin at server startup. To install a plugin named
myplugin from a plugin library file named somepluglib.so, use these lines in a my.cnf file:

[mysqld]
plugin-load-add=myplugin=somepluglib.so

In this case, the plugin is not registered in mysql.plugin. Restarting the server without the --plugin-
load-add option causes the plugin not to be loaded at startup.

Alternatively, the INSTALL PLUGIN statement causes the server to load the plugin code from the library
file at runtime:

INSTALL PLUGIN myplugin SONAME 'somepluglib.so';

INSTALL PLUGIN also causes “permanent” plugin registration: The plugin is listed in the mysql.plugin
table to ensure that the server loads it on subsequent restarts.

Many plugins can be loaded either at server startup or at runtime. However, if a plugin is designed such
that it must be loaded and initialized during server startup, attempts to load it at runtime using INSTALL
PLUGIN produce an error:

mysql> INSTALL PLUGIN myplugin SONAME 'somepluglib.so';
ERROR 1721 (HY000): Plugin 'myplugin' is marked as not dynamically
installable. You have to stop the server to install it.

In this case, you must use --plugin-load, --plugin-load-add, or --early-plugin-load.

998

Installing and Uninstalling Plugins

If a plugin is named both using a --plugin-load, --plugin-load-add, or --early-plugin-load
option and (as a result of an earlier INSTALL PLUGIN statement) in the mysql.plugin table, the server
starts but writes these messages to the error log:

[ERROR] Function 'plugin_name' already exists
[Warning] Couldn't load plugin named 'plugin_name'
with soname 'plugin_object_file'.

Controlling Plugin Activation State

If the server knows about a plugin when it starts (for example, because the plugin is named using
a --plugin-load-add option or is registered in the mysql.plugin table), the server loads
and enables the plugin by default. It is possible to control activation state for such a plugin using a
--plugin_name[=activation_state] startup option, where plugin_name is the name of the plugin
to affect, such as innodb, csv, or validate_password. As with other options, dashes and underscores
are interchangeable in option names. Also, activation state values are not case-sensitive. For example, --
my_plugin=ON and --my-plugin=on are equivalent.

• --plugin_name=OFF

Tells the server to disable the plugin. This may not be possible for certain built-in plugins, such as
mysql_native_password.

• --plugin_name[=ON]

Tells the server to enable the plugin. (Specifying the option as --plugin_name without a value has the
same effect.) If the plugin fails to initialize, the server runs with the plugin disabled.

• --plugin_name=FORCE

Tells the server to enable the plugin, but if plugin initialization fails, the server does not start. In other
words, this option forces the server to run with the plugin enabled or not at all.

• --plugin_name=FORCE_PLUS_PERMANENT

Like FORCE, but in addition prevents the plugin from being unloaded at runtime. If a user attempts to do
so with UNINSTALL PLUGIN, an error occurs.

Plugin activation states are visible in the LOAD_OPTION column of the Information Schema PLUGINS table.

Suppose that CSV, BLACKHOLE, and ARCHIVE are built-in pluggable storage engines and that you want
the server to load them at startup, subject to these conditions: The server is permitted to run if CSV
initialization fails, must require that BLACKHOLE initialization succeeds, and should disable ARCHIVE. To
accomplish that, use these lines in an option file:

[mysqld]
csv=ON
blackhole=FORCE
archive=OFF

The --enable-plugin_name option format is a synonym for --plugin_name=ON. The
--disable-plugin_name and --skip-plugin_name option formats are synonyms for
--plugin_name=OFF.

If a plugin is disabled, either explicitly with OFF or implicitly because it was enabled with ON but fails
to initialize, aspects of server operation that require the plugin change. For example, if the plugin
implements a storage engine, existing tables for the storage engine become inaccessible, and attempts
to create new tables for the storage engine result in tables that use the default storage engine unless the
NO_ENGINE_SUBSTITUTION SQL mode is enabled to cause an error to occur instead.

999

Obtaining Server Plugin Information

Disabling a plugin may require adjustment to other options. For example, if you start the server
using --skip-innodb to disable InnoDB, other innodb_xxx options likely need to be omitted
at startup. In addition, because InnoDB is the default storage engine, it cannot start unless you
specify another available storage engine with --default_storage_engine. You must also set --
default_tmp_storage_engine.

Uninstalling Plugins

At runtime, the UNINSTALL PLUGIN statement disables and uninstalls a plugin known to the server. The
statement unloads the plugin and removes it from the mysql.plugin system table, if it is registered there.
For this reason, UNINSTALL PLUGIN statement requires the DELETE privilege for the mysql.plugin
table. With the plugin no longer registered in the table, the server does not load the plugin during
subsequent restarts.

UNINSTALL PLUGIN can unload a plugin regardless of whether it was loaded at runtime with INSTALL
PLUGIN or at startup with a plugin-loading option, subject to these conditions:

• It cannot unload plugins that are built in to the server. These can be identified as those that have a
library name of NULL in the output from INFORMATION_SCHEMA.PLUGINS or SHOW PLUGINS.

• It cannot unload plugins for which the server was started with

--plugin_name=FORCE_PLUS_PERMANENT, which prevents plugin unloading at runtime. These can
be identified from the LOAD_OPTION column of the Information Schema PLUGINS table.

To uninstall a plugin that currently is loaded at server startup with a plugin-loading option, use this
procedure.

1. Remove from the my.cnf file any options related to the plugin.

2. Restart the server.

3. Plugins normally are installed using either a plugin-loading option at startup or with INSTALL PLUGIN
at runtime, but not both. However, removing options for a plugin from the my.cnf file may not be
sufficient to uninstall it if at some point INSTALL PLUGIN has also been used. If the plugin still
appears in the output from INFORMATION_SCHEMA.PLUGINS or SHOW PLUGINS, use UNINSTALL
PLUGIN to remove it from the mysql.plugin table. Then restart the server again.

5.5.2 Obtaining Server Plugin Information

There are several ways to determine which plugins are installed in the server:

• The Information Schema PLUGINS table contains a row for each loaded plugin. Any that have a

PLUGIN_LIBRARY value of NULL are built in and cannot be unloaded.

mysql> SELECT * FROM INFORMATION_SCHEMA.PLUGINS\G
*************************** 1. row ***************************
           PLUGIN_NAME: binlog
        PLUGIN_VERSION: 1.0
         PLUGIN_STATUS: ACTIVE
           PLUGIN_TYPE: STORAGE ENGINE
   PLUGIN_TYPE_VERSION: 50158.0
        PLUGIN_LIBRARY: NULL
PLUGIN_LIBRARY_VERSION: NULL
         PLUGIN_AUTHOR: MySQL AB
    PLUGIN_DESCRIPTION: This is a pseudo storage engine to represent the binlog in a transaction
        PLUGIN_LICENSE: GPL
           LOAD_OPTION: FORCE
...
*************************** 10. row ***************************

1000

MySQL Enterprise Thread Pool

           PLUGIN_NAME: InnoDB
        PLUGIN_VERSION: 1.0
         PLUGIN_STATUS: ACTIVE
           PLUGIN_TYPE: STORAGE ENGINE
   PLUGIN_TYPE_VERSION: 50158.0
        PLUGIN_LIBRARY: ha_innodb_plugin.so
PLUGIN_LIBRARY_VERSION: 1.0
         PLUGIN_AUTHOR: Innobase Oy
    PLUGIN_DESCRIPTION: Supports transactions, row-level locking,
                        and foreign keys
        PLUGIN_LICENSE: GPL
           LOAD_OPTION: ON
...

• The SHOW PLUGINS statement displays a row for each loaded plugin. Any that have a Library value of

NULL are built in and cannot be unloaded.

mysql> SHOW PLUGINS\G
*************************** 1. row ***************************
   Name: binlog
 Status: ACTIVE
   Type: STORAGE ENGINE
Library: NULL
License: GPL
...
*************************** 10. row ***************************
   Name: InnoDB
 Status: ACTIVE
   Type: STORAGE ENGINE
Library: ha_innodb_plugin.so
License: GPL
...

• The mysql.plugin table shows which plugins have been registered with INSTALL PLUGIN. The table
contains only plugin names and library file names, so it does not provide as much information as the
PLUGINS table or the SHOW PLUGINS statement.

5.5.3 MySQL Enterprise Thread Pool

Note

MySQL Enterprise Thread Pool is an extension included in MySQL Enterprise
Edition, a commercial product. To learn more about commercial products, https://
www.mysql.com/products/.

MySQL Enterprise Edition includes MySQL Enterprise Thread Pool, implemented using a server plugin.
The default thread-handling model in MySQL Server executes statements using one thread per client
connection. As more clients connect to the server and execute statements, overall performance degrades.
The thread pool plugin provides an alternative thread-handling model designed to reduce overhead
and improve performance. The plugin implements a thread pool that increases server performance by
efficiently managing statement execution threads for large numbers of client connections.

The thread pool addresses several problems of the model that uses one thread per connection:

• Too many thread stacks make CPU caches almost useless in highly parallel execution workloads. The

thread pool promotes thread stack reuse to minimize the CPU cache footprint.

• With too many threads executing in parallel, context switching overhead is high. This also presents a

challenge to the operating system scheduler. The thread pool controls the number of active threads to
keep the parallelism within the MySQL server at a level that it can handle and that is appropriate for the
server host on which MySQL is executing.

1001

MySQL Enterprise Thread Pool

• Too many transactions executing in parallel increases resource contention. In InnoDB, this increases

the time spent holding central mutexes. The thread pool controls when transactions start to ensure that
not too many execute in parallel.

Additional Resources

Section A.15, “MySQL 5.7 FAQ: MySQL Enterprise Thread Pool”

5.5.3.1 Thread Pool Elements

MySQL Enterprise Thread Pool comprises these elements:

• A plugin library file implements a plugin for the thread pool code as well as several associated monitoring

tables that provide information about thread pool operation.

For a detailed description of how the thread pool works, see Section 5.5.3.3, “Thread Pool Operation”.

The INFORMATION_SCHEMA tables are named TP_THREAD_STATE, TP_THREAD_GROUP_STATE, and
TP_THREAD_GROUP_STATS. These tables provide information about thread pool operation. For more
information, see Section 24.5, “INFORMATION_SCHEMA Thread Pool Tables”.

• Several system variables are related to the thread pool. The thread_handling system variable has a

value of loaded-dynamically when the server successfully loads the thread pool plugin.

The other related system variables are implemented by the thread pool plugin and are not available
unless it is enabled. For information about using these variables, see Section 5.5.3.3, “Thread Pool
Operation”, and Section 5.5.3.4, “Thread Pool Tuning”.

• The Performance Schema has instruments that expose information about the thread pool and may be

used to investigate operational performance. To identify them, use this query:

SELECT * FROM performance_schema.setup_instruments
WHERE NAME LIKE '%thread_pool%';

For more information, see Chapter 25, MySQL Performance Schema.

5.5.3.2 Thread Pool Installation

This section describes how to install MySQL Enterprise Thread Pool. For general information about
installing plugins, see Section 5.5.1, “Installing and Uninstalling Plugins”.

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the
directory named by the plugin_dir system variable). If necessary, configure the plugin directory location
by setting the value of plugin_dir at server startup.

The plugin library file base name is thread_pool. The file name suffix differs per platform (for example,
.so for Unix and Unix-like systems, .dll for Windows).

To enable thread pool capability, load the plugins to be used by starting the server with the --plugin-
load-add option. For example, if you name only the plugin library file, the server loads all plugins that it
contains (that is, the thread pool plugin and all the INFORMATION_SCHEMA tables). To do this, put these
lines in the server my.cnf file, adjusting the .so suffix for your platform as necessary:

[mysqld]
plugin-load-add=thread_pool.so

That is equivalent to loading all thread pool plugins by naming them individually:

[mysqld]

1002

MySQL Enterprise Thread Pool

plugin-load-add=thread_pool=thread_pool.so
plugin-load-add=tp_thread_state=thread_pool.so
plugin-load-add=tp_thread_group_state=thread_pool.so
plugin-load-add=tp_thread_group_stats=thread_pool.so

If desired, you can load individual plugins from the library file. To load the thread pool plugin but not the
INFORMATION_SCHEMA tables, use an option like this:

[mysqld]
plugin-load-add=thread_pool=thread_pool.so

To load the thread pool plugin and only the TP_THREAD_STATE INFORMATION_SCHEMA table, use
options like this:

[mysqld]
plugin-load-add=thread_pool=thread_pool.so
plugin-load-add=tp_thread_state=thread_pool.so

Note

If you do not load all the INFORMATION_SCHEMA tables, some or all MySQL
Enterprise Monitor thread pool graphs are empty.

To verify plugin installation, examine the Information Schema PLUGINS table or use the SHOW PLUGINS
statement (see Section 5.5.2, “Obtaining Server Plugin Information”). For example:

mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS
       FROM INFORMATION_SCHEMA.PLUGINS
       WHERE PLUGIN_NAME LIKE 'thread%' OR PLUGIN_NAME LIKE 'tp%';
+-----------------------+---------------+
| PLUGIN_NAME           | PLUGIN_STATUS |
+-----------------------+---------------+
| thread_pool           | ACTIVE        |
| TP_THREAD_STATE       | ACTIVE        |
| TP_THREAD_GROUP_STATE | ACTIVE        |
| TP_THREAD_GROUP_STATS | ACTIVE        |
+-----------------------+---------------+

If the server loads the thread pool plugin successfully, it sets the thread_handling system variable to
loaded-dynamically.

If a plugin fails to initialize, check the server error log for diagnostic messages.

5.5.3.3 Thread Pool Operation

The thread pool consists of a number of thread groups, each of which manages a set of client connections.
As connections are established, the thread pool assigns them to thread groups in round-robin fashion.

The thread pool exposes system variables that may be used to configure its operation:

• thread_pool_algorithm: The concurrency algorithm to use for scheduling.

• thread_pool_high_priority_connection: How to schedule statement execution for a session.

• thread_pool_max_unused_threads: How many sleeping threads to permit.

• thread_pool_prio_kickup_timer: How long before the thread pool moves a statement awaiting

execution from the low-priority queue to the high-priority queue.

• thread_pool_size: The number of thread groups in the thread pool. This is the most important

parameter controlling thread pool performance.

• thread_pool_stall_limit: The time before an executing statement is considered to be stalled.

1003

MySQL Enterprise Thread Pool

To configure the number of thread groups, use the thread_pool_size system variable. The default
number of groups is 16. For guidelines on setting this variable, see Section 5.5.3.4, “Thread Pool Tuning”.

The maximum number of threads per group is 4096 (or 4095 on some systems where one thread is used
internally).

The thread pool separates connections and threads, so there is no fixed relationship between connections
and the threads that execute statements received from those connections. This differs from the default
thread-handling model that associates one thread with one connection such that a given thread executes
all statements from its connection.

The thread pool tries to ensure a maximum of one thread executing in each group at any time, but
sometimes permits more threads to execute temporarily for best performance:

• Each thread group has a listener thread that listens for incoming statements from the connections

assigned to the group. When a statement arrives, the thread group either begins executing it
immediately or queues it for later execution:

• Immediate execution occurs if the statement is the only one received and no statements are queued or

currently executing.

• Queuing occurs if the statement cannot begin executing immediately.

• If immediate execution occurs, the listener thread performs it. (This means that temporarily no thread
in the group is listening.) If the statement finishes quickly, the executing thread returns to listening for
statements. Otherwise, the thread pool considers the statement stalled and starts another thread as a
listener thread (creating it if necessary). To ensure that no thread group becomes blocked by stalled
statements, the thread pool has a background thread that regularly monitors thread group states.

By using the listening thread to execute a statement that can begin immediately, there is no need to
create an additional thread if the statement finishes quickly. This ensures the most efficient execution
possible in the case of a low number of concurrent threads.

When the thread pool plugin starts, it creates one thread per group (the listener thread), plus the
background thread. Additional threads are created as necessary to execute statements.

• The value of the thread_pool_stall_limit system variable determines the meaning of “finishes

quickly” in the previous item. The default time before threads are considered stalled is 60ms but can be
set to a maximum of 6s. This parameter is configurable to enable you to strike a balance appropriate for
the server work load. Short wait values permit threads to start more quickly. Short values are also better
for avoiding deadlock situations. Long wait values are useful for workloads that include long-running
statements, to avoid starting too many new statements while the current ones execute.

• The thread pool focuses on limiting the number of concurrent short-running statements. Before an
executing statement reaches the stall time, it prevents other statements from beginning to execute.
If the statement executes past the stall time, it is permitted to continue but no longer prevents other
statements from starting. In this way, the thread pool tries to ensure that in each thread group there is
never more than one short-running statement, although there might be multiple long-running statements.
It is undesirable to let long-running statements prevent other statements from executing because there is
no limit on the amount of waiting that might be necessary. For example, on a replication source, a thread
that is sending binary log events to a replica effectively runs forever.

• A statement becomes blocked if it encounters a disk I/O operation or a user level lock (row lock or table
lock). The block would cause the thread group to become unused, so there are callbacks to the thread
pool to ensure that the thread pool can immediately start a new thread in this group to execute another
statement. When a blocked thread returns, the thread pool permits it to restart immediately.

1004

MySQL Enterprise Thread Pool

• There are two queues, a high-priority queue and a low-priority queue. The first statement in a
transaction goes to the low-priority queue. Any following statements for the transaction go to
the high-priority queue if the transaction is ongoing (statements for it have begun executing),
or to the low-priority queue otherwise. Queue assignment can be affected by enabling the
thread_pool_high_priority_connection system variable, which causes all queued statements
for a session to go into the high-priority queue.

Statements for a nontransactional storage engine, or a transactional engine if autocommit is enabled,
are treated as low-priority statements because in this case each statement is a transaction. Thus, given
a mix of statements for InnoDB and MyISAM tables, the thread pool prioritizes those for InnoDB over
those for MyISAM unless autocommit is enabled. With autocommit enabled, all statements are low
priority.

• When the thread group selects a queued statement for execution, it first looks in the high-priority

queue, then in the low-priority queue. If a statement is found, it is removed from its queue and begins to
execute.

• If a statement stays in the low-priority queue too long, the thread pool moves to the high-priority queue.

The value of the thread_pool_prio_kickup_timer system variable controls the time before
movement. For each thread group, a maximum of one statement per 10ms (100 per second) is moved
from the low-priority queue to the high-priority queue.

• The thread pool reuses the most active threads to obtain a much better use of CPU caches. This is a

small adjustment that has a great impact on performance.

• While a thread executes a statement from a user connection, Performance Schema instrumentation

accounts thread activity to the user connection. Otherwise, Performance Schema accounts activity to the
thread pool.

Here are examples of conditions under which a thread group might have multiple threads started to
execute statements:

• One thread begins executing a statement, but runs long enough to be considered stalled. The thread

group permits another thread to begin executing another statement even through the first thread is still
executing.

• One thread begins executing a statement, then becomes blocked and reports this back to the thread

pool. The thread group permits another thread to begin executing another statement.

• One thread begins executing a statement, becomes blocked, but does not report back that it is blocked
because the block does not occur in code that has been instrumented with thread pool callbacks. In
this case, the thread appears to the thread group to be still running. If the block lasts long enough for
the statement to be considered stalled, the group permits another thread to begin executing another
statement.

The thread pool is designed to be scalable across an increasing number of connections. It is also designed
to avoid deadlocks that can arise from limiting the number of actively executing statements. It is important
that threads that do not report back to the thread pool do not prevent other statements from executing and
thus cause the thread pool to become deadlocked. Examples of such statements follow:

• Long-running statements. These would lead to all resources used by only a few statements and they

could prevent all others from accessing the server.

• Binary log dump threads that read the binary log and send it to replicas. This is a kind of long-running

“statement” that runs for a very long time, and that should not prevent other statements from executing.

• Statements blocked on a row lock, table lock, sleep, or any other blocking activity that has not been

reported back to the thread pool by MySQL Server or a storage engine.

1005

MySQL Enterprise Thread Pool

In each case, to prevent deadlock, the statement is moved to the stalled category when it does not
complete quickly, so that the thread group can permit another statement to begin executing. With this
design, when a thread executes or becomes blocked for an extended time, the thread pool moves the
thread to the stalled category and for the rest of the statement's execution, it does not prevent other
statements from executing.

The maximum number of threads that can occur is the sum of max_connections and
thread_pool_size. This can happen in a situation where all connections are in execution mode and an
extra thread is created per group to listen for more statements. This is not necessarily a state that happens
often, but it is theoretically possible.

5.5.3.4 Thread Pool Tuning

This section provides guidelines on setting thread pool system variables for best performance, measured
using a metric such as transactions per second.

thread_pool_size is the most important parameter controlling thread pool performance. It can be set
only at server startup. Our experience in testing the thread pool indicates the following:

• If the primary storage engine is InnoDB, the optimal thread_pool_size setting is likely to be between
16 and 36, with the most common optimal values tending to be from 24 to 36. We have not seen any
situation where the setting has been optimal beyond 36. There may be special cases where a value
smaller than 16 is optimal.

For workloads such as DBT2 and Sysbench, the optimum for InnoDB seems to be usually around 36.
For very write-intensive workloads, the optimal setting can sometimes be lower.

• If the primary storage engine is MyISAM, the thread_pool_size setting should be fairly low. Optimal
performance is often seen with values from 4 to 8. Higher values tend to have a slightly negative but not
dramatic impact on performance.

Another system variable, thread_pool_stall_limit, is important for handling of blocked and long-
running statements. If all calls that block the MySQL Server are reported to the thread pool, it would always
know when execution threads are blocked. However, this may not always be true. For example, blocks
could occur in code that has not been instrumented with thread pool callbacks. For such cases, the thread
pool must be able to identify threads that appear to be blocked. This is done by means of a timeout that
can be tuned using the thread_pool_stall_limit system variable, the value of which is measured
in 10ms units. This parameter ensures that the server does not become completely blocked. The value of
thread_pool_stall_limit has an upper limit of 6 seconds to prevent the risk of a deadlocked server.

thread_pool_stall_limit also enables the thread pool to handle long-running statements. If a long-
running statement was permitted to block a thread group, all other connections assigned to the group
would be blocked and unable to start execution until the long-running statement completed. In the worst
case, this could take hours or even days.

The value of thread_pool_stall_limit should be chosen such that statements that execute longer
than its value are considered stalled. Stalled statements generate a lot of extra overhead since they involve
extra context switches and in some cases even extra thread creations. On the other hand, setting the
thread_pool_stall_limit parameter too high means that long-running statements block a number of
short-running statements for longer than necessary. Short wait values permit threads to start more quickly.
Short values are also better for avoiding deadlock situations. Long wait values are useful for workloads
that include long-running statements, to avoid starting too many new statements while the current ones
execute.

Suppose a server executes a workload where 99.9% of the statements complete within 100ms even when
the server is loaded, and the remaining statements take between 100ms and 2 hours fairly evenly spread.

1006

The Rewriter Query Rewrite Plugin

In this case, it would make sense to set thread_pool_stall_limit to 10 (10 × 10ms = 100ms). The
default value of 6 (60ms) is suitable for servers that primarily execute very simple statements.

The thread_pool_stall_limit parameter can be changed at runtime to enable you to strike a
balance appropriate for the server work load. Assuming that the TP_THREAD_GROUP_STATS table is
enabled, you can use the following query to determine the fraction of executed statements that stalled:

SELECT SUM(STALLED_QUERIES_EXECUTED) / SUM(QUERIES_EXECUTED)
FROM INFORMATION_SCHEMA.TP_THREAD_GROUP_STATS;

This number should be as low as possible. To decrease the likelihood of statements stalling, increase the
value of thread_pool_stall_limit.

When a statement arrives, what is the maximum time it can be delayed before it actually starts executing?
Suppose that the following conditions apply:

• There are 200 statements queued in the low-priority queue.

• There are 10 statements queued in the high-priority queue.

• thread_pool_prio_kickup_timer is set to 10000 (10 seconds).

• thread_pool_stall_limit is set to 100 (1 second).

In the worst case, the 10 high-priority statements represent 10 transactions that continue executing for a
long time. Thus, in the worst case, no statements are moved to the high-priority queue because it already
contains statements awaiting execution. After 10 seconds, the new statement is eligible to be moved to
the high-priority queue. However, before it can be moved, all the statements before it must be moved as
well. This could take another 2 seconds because a maximum of 100 statements per second are moved to
the high-priority queue. Now when the statement reaches the high-priority queue, there could potentially
be many long-running statements ahead of it. In the worst case, every one of those becomes stalled and
it takes 1 second for each statement before the next statement is retrieved from the high-priority queue.
Thus, in this scenario, it takes 222 seconds before the new statement starts executing.

This example shows a worst case for an application. How to handle it depends on the application. If the
application has high requirements for the response time, it should most likely throttle users at a higher
level itself. Otherwise, it can use the thread pool configuration parameters to set some kind of a maximum
waiting time.

5.5.4 The Rewriter Query Rewrite Plugin

MySQL supports query rewrite plugins that can examine and possibly modify SQL statements received by
the server before the server executes them. See Query Rewrite Plugins.

MySQL distributions include a postparse query rewrite plugin named Rewriter and scripts for installing
the plugin and its associated elements. These elements work together to provide SELECT rewriting
capability:

• A server-side plugin named Rewriter examines SELECT statements and may rewrite them, based
on its in-memory cache of rewrite rules. Standalone SELECT statements and SELECT statements in
prepared statements are subject to rewriting. SELECT statements occurring within view definitions or
stored programs are not subject to rewriting.

• The Rewriter plugin uses a database named query_rewrite containing a table named

rewrite_rules. The table provides persistent storage for the rules that the plugin uses to decide
whether to rewrite statements. Users communicate with the plugin by modifying the set of rules stored in
this table. The plugin communicates with users by setting the message column of table rows.

1007

The Rewriter Query Rewrite Plugin

• The query_rewrite database contains a stored procedure named flush_rewrite_rules() that

loads the contents of the rules table into the plugin.

• A loadable function named load_rewrite_rules() is used by the flush_rewrite_rules()

stored procedure.

• The Rewriter plugin exposes system variables that enable plugin configuration and status variables

that provide runtime operational information.

The following sections describe how to install and use the Rewriter plugin, and provide reference
information for its associated elements.

5.5.4.1 Installing or Uninstalling the Rewriter Query Rewrite Plugin

Note

If installed, the Rewriter plugin involves some overhead even when disabled. To
avoid this overhead, do not install the plugin unless you plan to use it.

To install or uninstall the Rewriter query rewrite plugin, choose the appropriate script located in the
share directory of your MySQL installation:

• install_rewriter.sql: Choose this script to install the Rewriter plugin and its associated

elements.

• uninstall_rewriter.sql: Choose this script to uninstall the Rewriter plugin and its associated

elements.

Run the chosen script as follows:

$> mysql -u root -p < install_rewriter.sql
Enter password: (enter root password here)

The example here uses the install_rewriter.sql installation script. Substitute
uninstall_rewriter.sql if you are uninstalling the plugin.

Running an installation script should install and enable the plugin. To verify that, connect to the server and
execute this statement:

mysql> SHOW GLOBAL VARIABLES LIKE 'rewriter_enabled';
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| rewriter_enabled | ON    |
+------------------+-------+

For usage instructions, see Section 5.5.4.2, “Using the Rewriter Query Rewrite Plugin”. For reference
information, see Section 5.5.4.3, “Rewriter Query Rewrite Plugin Reference”.

5.5.4.2 Using the Rewriter Query Rewrite Plugin

To enable or disable the plugin, enable or disable the rewriter_enabled system variable. By default,
the Rewriter plugin is enabled when you install it (see Section 5.5.4.1, “Installing or Uninstalling the
Rewriter Query Rewrite Plugin”). To set the initial plugin state explicitly, you can set the variable at server
startup. For example, to enable the plugin in an option file, use these lines:

[mysqld]
rewriter_enabled=ON

It is also possible to enable or disable the plugin at runtime:

1008

The Rewriter Query Rewrite Plugin

SET GLOBAL rewriter_enabled = ON;
SET GLOBAL rewriter_enabled = OFF;

Assuming that the Rewriter plugin is enabled, it examines and possibly modifies each SELECT statement
received by the server. The plugin determines whether to rewrite statements based on its in-memory cache
of rewriting rules, which are loaded from the rewrite_rules table in the query_rewrite database.

• Adding Rewrite Rules

• How Statement Matching Works

• Rewriting Prepared Statements

• Rewriter Plugin Operational Information

• Rewriter Plugin Use of Character Sets

Adding Rewrite Rules

To add rules for the Rewriter plugin, add rows to the rewrite_rules table, then invoke the
flush_rewrite_rules() stored procedure to load the rules from the table into the plugin. The following
example creates a simple rule to match statements that select a single literal value:

INSERT INTO query_rewrite.rewrite_rules (pattern, replacement)
VALUES('SELECT ?', 'SELECT ? + 1');

The resulting table contents look like this:

mysql> SELECT * FROM query_rewrite.rewrite_rules\G
*************************** 1. row ***************************
                id: 1
           pattern: SELECT ?
  pattern_database: NULL
       replacement: SELECT ? + 1
           enabled: YES
           message: NULL
    pattern_digest: NULL
normalized_pattern: NULL

The rule specifies a pattern template indicating which SELECT statements to match, and a
replacement template indicating how to rewrite matching statements. However, adding the rule to the
rewrite_rules table is not sufficient to cause the Rewriter plugin to use the rule. You must invoke
flush_rewrite_rules() to load the table contents into the plugin in-memory cache:

mysql> CALL query_rewrite.flush_rewrite_rules();

Tip

If your rewrite rules seem not to be working properly, make sure that you have
reloaded the rules table by calling flush_rewrite_rules().

When the plugin reads each rule from the rules table, it computes a normalized (statement digest) form
from the pattern and a digest hash value, and uses them to update the normalized_pattern and
pattern_digest columns:

mysql> SELECT * FROM query_rewrite.rewrite_rules\G
*************************** 1. row ***************************
                id: 1
           pattern: SELECT ?
  pattern_database: NULL
       replacement: SELECT ? + 1
           enabled: YES
           message: NULL

1009

The Rewriter Query Rewrite Plugin

    pattern_digest: 46b876e64cd5c41009d91c754921f1d4
normalized_pattern: select ?

For information about statement digesting, normalized statements, and digest hash values, see
Section 25.10, “Performance Schema Statement Digests”.

If a rule cannot be loaded due to some error, calling flush_rewrite_rules() produces an error:

mysql> CALL query_rewrite.flush_rewrite_rules();
ERROR 1644 (45000): Loading of some rule(s) failed.

When this occurs, the plugin writes an error message to the message column of the rule row to
communicate the problem. Check the rewrite_rules table for rows with non-NULL message column
values to see what problems exist.

Patterns use the same syntax as prepared statements (see Section 13.5.1, “PREPARE Statement”).
Within a pattern template, ? characters act as parameter markers that match data values. The ? characters
should not be enclosed within quotation marks. Parameter markers can be used only where data values
should appear, and they cannot be used for SQL keywords, identifiers, functions, and so on. The plugin
parses a statement to identify the literal values (as defined in Section 9.1, “Literal Values”), so you can put
a parameter marker in place of any literal value.

Like the pattern, the replacement can contain ? characters. For a statement that matches a pattern
template, the plugin rewrites it, replacing ? parameter markers in the replacement using data values
matched by the corresponding markers in the pattern. The result is a complete statement string. The
plugin asks the server to parse it, and returns the result to the server as the representation of the rewritten
statement.

After adding and loading the rule, check whether rewriting occurs according to whether statements match
the rule pattern:

mysql> SELECT PI();
+----------+
| PI()     |
+----------+
| 3.141593 |
+----------+
1 row in set (0.01 sec)

mysql> SELECT 10;
+--------+
| 10 + 1 |
+--------+
|     11 |
+--------+
1 row in set, 1 warning (0.00 sec)

No rewriting occurs for the first SELECT statement, but does for the second. The second statement
illustrates that when the Rewriter plugin rewrites a statement, it produces a warning message. To view
the message, use SHOW WARNINGS:

mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
  Level: Note
   Code: 1105
Message: Query 'SELECT 10' rewritten to 'SELECT 10 + 1' by a query rewrite plugin

To enable or disable an existing rule, modify its enabled column and reload the table into the plugin. To
disable rule 1:

UPDATE query_rewrite.rewrite_rules SET enabled = 'NO' WHERE id = 1;
CALL query_rewrite.flush_rewrite_rules();

1010

The Rewriter Query Rewrite Plugin

This enables you to deactivate a rule without removing it from the table.

To re-enable rule 1:

UPDATE query_rewrite.rewrite_rules SET enabled = 'YES' WHERE id = 1;
CALL query_rewrite.flush_rewrite_rules();

The rewrite_rules table contains a pattern_database column that Rewriter uses for matching
table names that are not qualified with a database name:

• Qualified table names in statements match qualified names in the pattern if corresponding database and

table names are identical.

• Unqualified table names in statements match unqualified names in the pattern only if the default

database is the same as pattern_database and the table names are identical.

Suppose that a table named appdb.users has a column named id and that applications are expected
to select rows from the table using a query of one of these forms, where the second can be used when
appdb is the default database:

SELECT * FROM users WHERE appdb.id = id_value;
SELECT * FROM users WHERE id = id_value;

Suppose also that the id column is renamed to user_id (perhaps the table must be modified to
add another type of ID and it is necessary to indicate more specifically what type of ID the id column
represents).

The change means that applications must refer to user_id rather than id in the WHERE clause, but
old applications that cannot be updated no longer work properly. The Rewriter plugin can solve this
problem by matching and rewriting problematic statements. To match the statement SELECT * FROM
appdb.users WHERE id = value and rewrite it as SELECT * FROM appdb.users WHERE
user_id = value, you can insert a row representing a replacement rule into the rewrite rules table. If
you also want to match this SELECT using the unqualified table name, it is also necessary to add an explicit
rule. Using ? as a value placeholder, the two INSERT statements needed look like this:

INSERT INTO query_rewrite.rewrite_rules
    (pattern, replacement) VALUES(
    'SELECT * FROM appdb.users WHERE id = ?',
    'SELECT * FROM appdb.users WHERE user_id = ?'
    );
INSERT INTO query_rewrite.rewrite_rules
    (pattern, replacement, pattern_database) VALUES(
    'SELECT * FROM users WHERE id = ?',
    'SELECT * FROM users WHERE user_id = ?',
    'appdb'
    );

After adding the two new rules, execute the following statement to cause them to take effect:

CALL query_rewrite.flush_rewrite_rules();

Rewriter uses the first rule to match statements that use the qualified table name, and the second to
match statements that use the unqualified name. The second rule works only when appdb is the default
database.

How Statement Matching Works

The Rewriter plugin uses statement digests and digest hash values to match incoming statements
against rewrite rules in stages. The max_digest_length system variable determines the size of the
buffer used for computing statement digests. Larger values enable computation of digests that distinguish

1011

The Rewriter Query Rewrite Plugin

longer statements. Smaller values use less memory but increase the likelihood of longer statements
colliding with the same digest value.

The plugin matches each statement to the rewrite rules as follows:

1. Compute the statement digest hash value and compare it to the rule digest hash values. This is subject

to false positives, but serves as a quick rejection test.

2.

3.

If the statement digest hash value matches any pattern digest hash values, match the normalized
(statement digest) form of the statement to the normalized form of the matching rule patterns.

If the normalized statement matches a rule, compare the literal values in the statement and the pattern.
A ? character in the pattern matches any literal value in the statement. If the statement prepares a
SELECT statement, ? in the pattern also matches ? in the statement. Otherwise, corresponding literals
must be the same.

If multiple rules match a statement, it is nondeterministic which one the plugin uses to rewrite the
statement.

If a pattern contains more markers than the replacement, the plugin discards excess data values. If a
pattern contains fewer markers than the replacement, it is an error. The plugin notices this when the rules
table is loaded, writes an error message to the message column of the rule row to communicate the
problem, and sets the Rewriter_reload_error status variable to ON.

Rewriting Prepared Statements

Prepared statements are rewritten at parse time (that is, when they are prepared), not when they are
executed later.

Prepared statements differ from nonprepared statements in that they may contain ? characters as
parameter markers. To match a ? in a prepared statement, a Rewriter pattern must contain ? in the
same location. Suppose that a rewrite rule has this pattern:

SELECT ?, 3

The following table shows several prepared SELECT statements and whether the rule pattern matches
them.

Prepared Statement

Whether Pattern Matches Statement

PREPARE s AS 'SELECT 3, 3'

PREPARE s AS 'SELECT ?, 3'

PREPARE s AS 'SELECT 3, ?'

PREPARE s AS 'SELECT ?, ?'

Yes

Yes

No

No

Rewriter Plugin Operational Information

The Rewriter plugin makes information available about its operation by means of several status
variables:

mysql> SHOW GLOBAL STATUS LIKE 'Rewriter%';
+-----------------------------------+-------+
| Variable_name                     | Value |
+-----------------------------------+-------+
| Rewriter_number_loaded_rules      | 1     |
| Rewriter_number_reloads           | 5     |
| Rewriter_number_rewritten_queries | 1     |
| Rewriter_reload_error             | ON    |
+-----------------------------------+-------+

1012

The Rewriter Query Rewrite Plugin

For descriptions of these variables, see Rewriter Query Rewrite Plugin Status Variables.

When you load the rules table by calling the flush_rewrite_rules() stored procedure, if
an error occurs for some rule, the CALL statement produces an error, and the plugin sets the
Rewriter_reload_error status variable to ON:

mysql> CALL query_rewrite.flush_rewrite_rules();
ERROR 1644 (45000): Loading of some rule(s) failed.

mysql> SHOW GLOBAL STATUS LIKE 'Rewriter_reload_error';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| Rewriter_reload_error | ON    |
+-----------------------+-------+

In this case, check the rewrite_rules table for rows with non-NULL message column values to see
what problems exist.

Rewriter Plugin Use of Character Sets

When the rewrite_rules table is loaded into the Rewriter plugin, the plugin interprets statements
using the current global value of the character_set_client system variable. If the global
character_set_client value is changed subsequently, the rules table must be reloaded.

A client must have a session character_set_client value identical to what the global value was when
the rules table was loaded or rule matching does not work for that client.

5.5.4.3 Rewriter Query Rewrite Plugin Reference

The following discussion serves as a reference to these elements associated with the Rewriter query
rewrite plugin:

• The Rewriter rules table in the query_rewrite database

• Rewriter procedures and functions

• Rewriter system and status variables

Rewriter Query Rewrite Plugin Rules Table

The rewrite_rules table in the query_rewrite database provides persistent storage for the rules that
the Rewriter plugin uses to decide whether to rewrite statements.

Users communicate with the plugin by modifying the set of rules stored in this table. The plugin
communicates information to users by setting the table's message column.

Note

The rules table is loaded into the plugin by the flush_rewrite_rules stored
procedure. Unless that procedure has been called following the most recent table
modification, the table contents do not necessarily correspond to the set of rules the
plugin is using.

The rewrite_rules table has these columns:

• id

The rule ID. This column is the table primary key. You can use the ID to uniquely identify any rule.

1013

The Rewriter Query Rewrite Plugin

• pattern

The template that indicates the pattern for statements that the rule matches. Use ? to represent
parameter markers that match data values.

• pattern_database

The database used to match unqualified table names in statements. Qualified table names in statements
match qualified names in the pattern if corresponding database and table names are identical.
Unqualified table names in statements match unqualified names in the pattern only if the default
database is the same as pattern_database and the table names are identical.

• replacement

The template that indicates how to rewrite statements matching the pattern column value. Use ?
to represent parameter markers that match data values. In rewritten statements, the plugin replaces
? parameter markers in replacement using data values matched by the corresponding markers in
pattern.

• enabled

Whether the rule is enabled. Load operations (performed by invoking the flush_rewrite_rules()
stored procedure) load the rule from the table into the Rewriter in-memory cache only if this column is
YES.

This column makes it possible to deactivate a rule without removing it: Set the column to a value other
than YES and reload the table into the plugin.

• message

The plugin uses this column for communicating with users. If no error occurs when the rules table is
loaded into memory, the plugin sets the message column to NULL. A non-NULL value indicates an error
and the column contents are the error message. Errors can occur under these circumstances:

• Either the pattern or the replacement is an incorrect SQL statement that produces syntax errors.

• The replacement contains more ? parameter markers than the pattern.

If a load error occurs, the plugin also sets the Rewriter_reload_error status variable to ON.

• pattern_digest

This column is used for debugging and diagnostics. If the column exists when the rules table is loaded
into memory, the plugin updates it with the pattern digest. This column may be useful if you are trying to
determine why some statement fails to be rewritten.

• normalized_pattern

This column is used for debugging and diagnostics. If the column exists when the rules table is loaded
into memory, the plugin updates it with the normalized form of the pattern. This column may be useful if
you are trying to determine why some statement fails to be rewritten.

Rewriter Query Rewrite Plugin Procedures and Functions

Rewriter plugin operation uses a stored procedure that loads the rules table into its in-memory cache,
and a helper loadable function. Under normal operation, users invoke only the stored procedure. The
function is intended to be invoked by the stored procedure, not directly by users.

1014

The Rewriter Query Rewrite Plugin

• flush_rewrite_rules()

This stored procedure uses the load_rewrite_rules() function to load the contents of the
rewrite_rules table into the Rewriter in-memory cache.

Calling flush_rewrite_rules() implies COMMIT.

Invoke this procedure after you modify the rules table to cause the plugin to update its cache from the
new table contents. If any errors occur, the plugin sets the message column for the appropriate rule rows
in the table and sets the Rewriter_reload_error status variable to ON.

• load_rewrite_rules()

This function is a helper routine used by the flush_rewrite_rules() stored procedure.

Rewriter Query Rewrite Plugin System Variables

The Rewriter query rewrite plugin supports the following system variables. These variables are available
only if the plugin is installed (see Section 5.5.4.1, “Installing or Uninstalling the Rewriter Query Rewrite
Plugin”).

• rewriter_enabled

System Variable

Scope

Dynamic

Type

Default Value

Valid Values

rewriter_enabled

Global

Yes

Boolean

ON

OFF

Whether the Rewriter query rewrite plugin is enabled.

• rewriter_verbose

System Variable

rewriter_verbose

Scope

Dynamic

Type

For internal use.

Global

Yes

Integer

Rewriter Query Rewrite Plugin Status Variables

The Rewriter query rewrite plugin supports the following status variables. These variables are available
only if the plugin is installed (see Section 5.5.4.1, “Installing or Uninstalling the Rewriter Query Rewrite
Plugin”).

• Rewriter_number_loaded_rules

The number of rewrite plugin rewrite rules successfully loaded from the rewrite_rules table into
memory for use by the Rewriter plugin.

• Rewriter_number_reloads

1015

Version Tokens

The number of times the rewrite_rules table has been loaded into the in-memory cache used by the
Rewriter plugin.

• Rewriter_number_rewritten_queries

The number of queries rewritten by the Rewriter query rewrite plugin since it was loaded.

• Rewriter_reload_error

Whether an error occurred the most recent time that the rewrite_rules table was loaded into the in-
memory cache used by the Rewriter plugin. If the value is OFF, no error occurred. If the value is ON, an
error occurred; check the message column of the rewriter_rules table for error messages.

5.5.5 Version Tokens

MySQL includes Version Tokens, a feature that enables creation of and synchronization around server
tokens that applications can use to prevent accessing incorrect or out-of-date data.

The Version Tokens interface has these characteristics:

• Version tokens are pairs consisting of a name that serves as a key or identifier, plus a value.

• Version tokens can be locked. An application can use token locks to indicate to other cooperating

applications that tokens are in use and should not be modified.

• Version token lists are established per server (for example, to specify the server assignment or

operational state). In addition, an application that communicates with a server can register its own list of
tokens that indicate the state it requires the server to be in. An SQL statement sent by the application to
a server not in the required state produces an error. This is a signal to the application that it should seek
a different server in the required state to receive the SQL statement.

The following sections describe the elements of Version Tokens, discuss how to install and use it, and
provide reference information for its elements.

5.5.5.1 Version Tokens Elements

Version Tokens is based on a plugin library that implements these elements:

• A server-side plugin named version_tokens holds the list of version tokens associated with the server
and subscribes to notifications for statement execution events. The version_tokens plugin uses the
audit plugin API to monitor incoming statements from clients and matches each client's session-specific
version token list against the server version token list. If there is a match, the plugin lets the statement
through and the server continues to process it. Otherwise, the plugin returns an error to the client and
the statement fails.

• A set of loadable functions provides an SQL-level API for manipulating and inspecting the list of server

version tokens maintained by the plugin. The SUPER privilege is required to call any of the Version Token
functions.

• A system variable enables clients to specify the list of version tokens that register the required server
state. If the server has a different state when a client sends a statement, the client receives an error.

5.5.5.2 Installing or Uninstalling Version Tokens

Note

If installed, Version Tokens involves some overhead. To avoid this overhead, do not
install it unless you plan to use it.

1016

Version Tokens

This section describes how to install or uninstall Version Tokens, which is implemented in a plugin library
file containing a plugin and loadable functions. For general information about installing or uninstalling
plugins and loadable functions, see Section 5.5.1, “Installing and Uninstalling Plugins”, and Section 5.6.1,
“Installing and Uninstalling Loadable Functions”.

To be usable by the server, the plugin library file must be located in the MySQL plugin directory (the
directory named by the plugin_dir system variable). If necessary, configure the plugin directory location
by setting the value of plugin_dir at server startup.

The plugin library file base name is version_tokens. The file name suffix differs per platform (for
example, .so for Unix and Unix-like systems, .dll for Windows).

To install the Version Tokens plugin and functions, use the INSTALL PLUGIN and CREATE FUNCTION
statements, adjusting the .so suffix for your platform as necessary:

INSTALL PLUGIN version_tokens SONAME 'version_token.so';
CREATE FUNCTION version_tokens_set RETURNS STRING
  SONAME 'version_token.so';
CREATE FUNCTION version_tokens_show RETURNS STRING
  SONAME 'version_token.so';
CREATE FUNCTION version_tokens_edit RETURNS STRING
  SONAME 'version_token.so';
CREATE FUNCTION version_tokens_delete RETURNS STRING
  SONAME 'version_token.so';
CREATE FUNCTION version_tokens_lock_shared RETURNS INT
  SONAME 'version_token.so';
CREATE FUNCTION version_tokens_lock_exclusive RETURNS INT
  SONAME 'version_token.so';
CREATE FUNCTION version_tokens_unlock RETURNS INT
  SONAME 'version_token.so';

You must install the functions to manage the server's version token list, but you must also install the plugin
because the functions do not work correctly without it.

If the plugin and functions are used on a replication source server, install them on all replica servers as well
to avoid replication problems.

Once installed as just described, the plugin and functions remain installed until uninstalled. To remove
them, use the UNINSTALL PLUGIN and DROP FUNCTION statements:

UNINSTALL PLUGIN version_tokens;
DROP FUNCTION version_tokens_set;
DROP FUNCTION version_tokens_show;
DROP FUNCTION version_tokens_edit;
DROP FUNCTION version_tokens_delete;
DROP FUNCTION version_tokens_lock_shared;
DROP FUNCTION version_tokens_lock_exclusive;
DROP FUNCTION version_tokens_unlock;

5.5.5.3 Using Version Tokens

Before using Version Tokens, install it according to the instructions provided at Section 5.5.5.2, “Installing
or Uninstalling Version Tokens”.

A scenario in which Version Tokens can be useful is a system that accesses a collection of MySQL
servers but needs to manage them for load balancing purposes by monitoring them and adjusting server
assignments according to load changes. Such a system comprises these elements:

• The collection of MySQL servers to be managed.

1017

Version Tokens

• An administrative or management application that communicates with the servers and organizes them
into high-availability groups. Groups serve different purposes, and servers within each group may have
different assignments. Assignment of a server within a certain group can change at any time.

• Client applications that access the servers to retrieve and update data, choosing servers according to
the purposes assigned them. For example, a client should not send an update to a read-only server.

Version Tokens permit server access to be managed according to assignment without requiring clients to
repeatedly query the servers about their assignments:

• The management application performs server assignments and establishes version tokens on each

server to reflect its assignment. The application caches this information to provide a central access point
to it.

If at some point the management application needs to change a server assignment (for example, to
change it from permitting writes to read only), it changes the server's version token list and updates its
cache.

• To improve performance, client applications obtain cache information from the management application,

enabling them to avoid having to retrieve information about server assignments for each statement.
Based on the type of statements it issues (for example, reads versus writes), a client selects an
appropriate server and connects to it.

• In addition, the client sends to the server its own client-specific version tokens to register the assignment
it requires of the server. For each statement sent by the client to the server, the server compares its own
token list with the client token list. If the server token list contains all tokens present in the client token list
with the same values, there is a match and the server executes the statement.

On the other hand, perhaps the management application has changed the server assignment and its
version token list. In this case, the new server assignment may now be incompatible with the client
requirements. A token mismatch between the server and client token lists occurs and the server
returns an error in reply to the statement. This is an indication to the client to refresh its version token
information from the management application cache, and to select a new server to communicate with.

The client-side logic for detecting version token errors and selecting a new server can be implemented
different ways:

• The client can handle all version token registration, mismatch detection, and connection switching itself.

• The logic for those actions can be implemented in a connector that manages connections between

clients and MySQL servers. Such a connector might handle mismatch error detection and statement
resending itself, or it might pass the error to the application and leave it to the application to resend the
statement.

The following example illustrates the preceding discussion in more concrete form.

When Version Tokens initializes on a given server, the server's version token list is empty. Token list
maintenance is performed by calling functions. The SUPER privilege is required to call any of the Version
Token functions, so token list modification is expected to be done by a management or administrative
application that has that privilege.

Suppose that a management application communicates with a set of servers that are queried by clients to
access employee and product databases (named emp and prod, respectively). All servers are permitted
to process data retrieval statements, but only some of them are permitted to make database updates. To
handle this on a database-specific basis, the management application establishes a list of version tokens
on each server. In the token list for a given server, token names represent database names and token

1018

Version Tokens

values are read or write depending on whether the database must be used in read-only fashion or
whether it can take reads and writes.

Client applications register a list of version tokens they require the server to match by setting a system
variable. Variable setting occurs on a client-specific basis, so different clients can register different
requirements. By default, the client token list is empty, which matches any server token list. When a client
sets its token list to a nonempty value, matching may succeed or fail, depending on the server version
token list.

To define the version token list for a server, the management application calls the
version_tokens_set() function. (There are also functions for modifying and displaying the token list,
described later.) For example, the application might send these statements to a group of three servers:

Server 1:

mysql> SELECT version_tokens_set('emp=read;prod=read');
+------------------------------------------+
| version_tokens_set('emp=read;prod=read') |
+------------------------------------------+
| 2 version tokens set.                    |
+------------------------------------------+

Server 2:

mysql> SELECT version_tokens_set('emp=write;prod=read');
+-------------------------------------------+
| version_tokens_set('emp=write;prod=read') |
+-------------------------------------------+
| 2 version tokens set.                     |
+-------------------------------------------+

Server 3:

mysql> SELECT version_tokens_set('emp=read;prod=write');
+-------------------------------------------+
| version_tokens_set('emp=read;prod=write') |
+-------------------------------------------+
| 2 version tokens set.                     |
+-------------------------------------------+

The token list in each case is specified as a semicolon-separated list of name=value pairs. The resulting
token list values result in these server assingments:

• Any server accepts reads for either database.

• Only server 2 accepts updates for the emp database.

• Only server 3 accepts updates for the prod database.

In addition to assigning each server a version token list, the management application also maintains a
cache that reflects the server assignments.

Before communicating with the servers, a client application contacts the management application
and retrieves information about server assignments. Then the client selects a server based on those
assignments. Suppose that a client wants to perform both reads and writes on the emp database. Based on
the preceding assignments, only server 2 qualifies. The client connects to server 2 and registers its server
requirements there by setting its version_tokens_session system variable:

mysql> SET @@SESSION.version_tokens_session = 'emp=write';

1019

Version Tokens

For subsequent statements sent by the client to server 2, the server compares its own version token list to
the client list to check whether they match. If so, statements execute normally:

mysql> UPDATE emp.employee SET salary = salary * 1.1 WHERE id = 4981;
Query OK, 1 row affected (0.07 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT last_name, first_name FROM emp.employee WHERE id = 4981;
+-----------+------------+
| last_name | first_name |
+-----------+------------+
| Smith     | Abe        |
+-----------+------------+
1 row in set (0.01 sec)

Discrepancies between the server and client version token lists can occur two ways:

• A token name in the version_tokens_session value is not present in the server token list. In this

case, an ER_VTOKEN_PLUGIN_TOKEN_NOT_FOUND error occurs.

• A token value in the version_tokens_session value differs from the value of the corresponding

token in the server token list. In this case, an ER_VTOKEN_PLUGIN_TOKEN_MISMATCH error occurs.

As long as the assignment of server 2 does not change, the client continues to use it for reads and writes.
But suppose that the management application wants to change server assignments so that writes for the
emp database must be sent to server 1 instead of server 2. To do this, it uses version_tokens_edit()
to modify the emp token value on the two servers (and updates its cache of server assignments):

Server 1:

mysql> SELECT version_tokens_edit('emp=write');
+----------------------------------+
| version_tokens_edit('emp=write') |
+----------------------------------+
| 1 version tokens updated.        |
+----------------------------------+

Server 2:

mysql> SELECT version_tokens_edit('emp=read');
+---------------------------------+
| version_tokens_edit('emp=read') |
+---------------------------------+
| 1 version tokens updated.       |
+---------------------------------+

version_tokens_edit() modifies the named tokens in the server token list and leaves other tokens
unchanged.

The next time the client sends a statement to server 2, its own token list no longer matches the server
token list and an error occurs:

mysql> UPDATE emp.employee SET salary = salary * 1.1 WHERE id = 4982;
ERROR 3136 (42000): Version token mismatch for emp. Correct value read

In this case, the client should contact the management application to obtain updated information about
server assignments, select a new server, and send the failed statement to the new server.

Note

Each client must cooperate with Version Tokens by sending only statements in
accordance with the token list that it registers with a given server. For example, if

1020

Version Tokens

a client registers a token list of 'emp=read', there is nothing in Version Tokens to
prevent the client from sending updates for the emp database. The client itself must
refrain from doing so.

For each statement received from a client, the server implicitly uses locking, as follows:

• Take a shared lock for each token named in the client token list (that is, in the

version_tokens_session value)

• Perform the comparison between the server and client token lists

• Execute the statement or produce an error depending on the comparison result

• Release the locks

The server uses shared locks so that comparisons for multiple sessions can occur without blocking, while
preventing changes to the tokens for any session that attempts to acquire an exclusive lock before it
manipulates tokens of the same names in the server token list.

The preceding example uses only a few of the functions included in the Version Tokens plugin library, but
there are others. One set of functions permits the server's list of version tokens to be manipulated and
inspected. Another set of functions permits version tokens to be locked and unlocked.

These functions permit the server's list of version tokens to be created, changed, removed, and inspected:

• version_tokens_set() completely replaces the current list and assigns a new list. The argument is a

semicolon-separated list of name=value pairs.

• version_tokens_edit() enables partial modifications to the current list. It can add new tokens or

change the values of existing tokens. The argument is a semicolon-separated list of name=value pairs.

• version_tokens_delete() deletes tokens from the current list. The argument is a semicolon-

separated list of token names.

• version_tokens_show() displays the current token list. It takes no argument.

Each of those functions, if successful, returns a binary string indicating what action occurred. The following
example establishes the server token list, modifies it by adding a new token, deletes some tokens, and
displays the resulting token list:

mysql> SELECT version_tokens_set('tok1=a;tok2=b');
+-------------------------------------+
| version_tokens_set('tok1=a;tok2=b') |
+-------------------------------------+
| 2 version tokens set.               |
+-------------------------------------+
mysql> SELECT version_tokens_edit('tok3=c');
+-------------------------------+
| version_tokens_edit('tok3=c') |
+-------------------------------+
| 1 version tokens updated.     |
+-------------------------------+
mysql> SELECT version_tokens_delete('tok2;tok1');
+------------------------------------+
| version_tokens_delete('tok2;tok1') |
+------------------------------------+
| 2 version tokens deleted.          |
+------------------------------------+
mysql> SELECT version_tokens_show();
+-----------------------+

1021

Version Tokens

| version_tokens_show() |
+-----------------------+
| tok3=c;               |
+-----------------------+

Warnings occur if a token list is malformed:

mysql> SELECT version_tokens_set('tok1=a; =c');
+----------------------------------+
| version_tokens_set('tok1=a; =c') |
+----------------------------------+
| 1 version tokens set.            |
+----------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SHOW WARNINGS\G
*************************** 1. row ***************************
  Level: Warning
   Code: 42000
Message: Invalid version token pair encountered. The list provided
         is only partially updated.
1 row in set (0.00 sec)

As mentioned previously, version tokens are defined using a semicolon-separated list of name=value
pairs. Consider this invocation of version_tokens_set():

mysql> SELECT version_tokens_set('tok1=b;;; tok2= a = b ; tok1 = 1\'2 3"4')
+---------------------------------------------------------------+
| version_tokens_set('tok1=b;;; tok2= a = b ; tok1 = 1\'2 3"4') |
+---------------------------------------------------------------+
| 3 version tokens set.                                         |
+---------------------------------------------------------------+

Version Tokens interprets the argument as follows:

• Whitespace around names and values is ignored. Whitespace within names and values is permitted.
(For version_tokens_delete(), which takes a list of names without values, whitespace around
names is ignored.)

• There is no quoting mechanism.

• Order of tokens is not significant except that if a token list contains multiple instances of a given token

name, the last value takes precedence over earlier values.

Given those rules, the preceding version_tokens_set() call results in a token list with
two tokens: tok1 has the value 1'2 3"4, and tok2 has the value a = b. To verify this, call
version_tokens_show():

mysql> SELECT version_tokens_show();
+--------------------------+
| version_tokens_show()    |
+--------------------------+
| tok2=a = b;tok1=1'2 3"4; |
+--------------------------+

If the token list contains two tokens, why did version_tokens_set() return the value 3 version
tokens set? That occurred because the original token list contained two definitions for tok1, and the
second definition replaced the first.

The Version Tokens token-manipulation functions place these constraints on token names and values:

• Token names cannot contain = or ; characters and have a maximum length of 64 characters.

1022

Version Tokens

• Token values cannot contain ; characters. Length of values is constrained by the value of the

max_allowed_packet system variable.

• Version Tokens treats token names and values as binary strings, so comparisons are case-sensitive.

Version Tokens also includes a set of functions enabling tokens to be locked and unlocked:

• version_tokens_lock_exclusive() acquires exclusive version token locks. It takes a list of one or

more lock names and a timeout value.

• version_tokens_lock_shared() acquires shared version token locks. It takes a list of one or more

lock names and a timeout value.

• version_tokens_unlock() releases version token locks (exclusive and shared). It takes no

argument.

Each locking function returns nonzero for success. Otherwise, an error occurs:

mysql> SELECT version_tokens_lock_shared('lock1', 'lock2', 0);
+-------------------------------------------------+
| version_tokens_lock_shared('lock1', 'lock2', 0) |
+-------------------------------------------------+
|                                               1 |
+-------------------------------------------------+

mysql> SELECT version_tokens_lock_shared(NULL, 0);
ERROR 3131 (42000): Incorrect locking service lock name '(null)'.

Locking using Version Tokens locking functions is advisory; applications must agree to cooperate.

It is possible to lock nonexisting token names. This does not create the tokens.

Note

Version Tokens locking functions are based on the locking service described at
Section 5.5.6.1, “The Locking Service”, and thus have the same semantics for
shared and exclusive locks. (Version Tokens uses the locking service routines built
into the server, not the locking service function interface, so those functions need
not be installed to use Version Tokens.) Locks acquired by Version Tokens use
a locking service namespace of version_token_locks. Locking service locks
can be monitored using the Performance Schema, so this is also true for Version
Tokens locks. For details, see Locking Service Monitoring.

For the Version Tokens locking functions, token name arguments are used exactly as specified.
Surrounding whitespace is not ignored and = and ; characters are permitted. This is because Version
Tokens simply passes the token names to be locked as is to the locking service.

5.5.5.4 Version Tokens Reference

The following discussion serves as a reference to these Version Tokens elements:

• Version Tokens Functions

• Version Tokens System Variables

Version Tokens Functions

The Version Tokens plugin library includes several functions. One set of functions permits the server's list
of version tokens to be manipulated and inspected. Another set of functions permits version tokens to be
locked and unlocked. The SUPER privilege is required to invoke any Version Tokens function.

1023

Version Tokens

The following functions permit the server's list of version tokens to be created, changed, removed, and
inspected. Interpretation of name_list and token_list arguments (including whitespace handling)
occurs as described in Section 5.5.5.3, “Using Version Tokens”, which provides details about the syntax for
specifying tokens, as well as additional examples.

• version_tokens_delete(name_list)

Deletes tokens from the server's list of version tokens using the name_list argument and returns a
binary string that indicates the outcome of the operation. name_list is a semicolon-separated list of
version token names to delete.

mysql> SELECT version_tokens_delete('tok1;tok3');
+------------------------------------+
| version_tokens_delete('tok1;tok3') |
+------------------------------------+
| 2 version tokens deleted.          |
+------------------------------------+

An argument of NULL is treated as an empty string, which has no effect on the token list.

version_tokens_delete() deletes the tokens named in its argument, if they exist. (It is not an error
to delete nonexisting tokens.) To clear the token list entirely without knowing which tokens are in the list,
pass NULL or a string containing no tokens to version_tokens_set():

mysql> SELECT version_tokens_set(NULL);
+------------------------------+
| version_tokens_set(NULL)     |
+------------------------------+
| Version tokens list cleared. |
+------------------------------+
mysql> SELECT version_tokens_set('');
+------------------------------+
| version_tokens_set('')       |
+------------------------------+
| Version tokens list cleared. |
+------------------------------+

• version_tokens_edit(token_list)

Modifies the server's list of version tokens using the token_list argument and returns a binary string
that indicates the outcome of the operation. token_list is a semicolon-separated list of name=value
pairs specifying the name of each token to be defined and its value. If a token exists, its value is updated
with the given value. If a token does not exist, it is created with the given value. If the argument is NULL
or a string containing no tokens, the token list remains unchanged.

mysql> SELECT version_tokens_set('tok1=value1;tok2=value2');
+-----------------------------------------------+
| version_tokens_set('tok1=value1;tok2=value2') |
+-----------------------------------------------+
| 2 version tokens set.                         |
+-----------------------------------------------+
mysql> SELECT version_tokens_edit('tok2=new_value2;tok3=new_value3');
+--------------------------------------------------------+
| version_tokens_edit('tok2=new_value2;tok3=new_value3') |
+--------------------------------------------------------+
| 2 version tokens updated.                              |
+--------------------------------------------------------+

• version_tokens_set(token_list)

Replaces the server's list of version tokens with the tokens defined in the token_list argument
and returns a binary string that indicates the outcome of the operation. token_list is a semicolon-

1024

Version Tokens

separated list of name=value pairs specifying the name of each token to be defined and its value. If the
argument is NULL or a string containing no tokens, the token list is cleared.

mysql> SELECT version_tokens_set('tok1=value1;tok2=value2');
+-----------------------------------------------+
| version_tokens_set('tok1=value1;tok2=value2') |
+-----------------------------------------------+
| 2 version tokens set.                         |
+-----------------------------------------------+

• version_tokens_show()

Returns the server's list of version tokens as a binary string containing a semicolon-separated list of
name=value pairs.

mysql> SELECT version_tokens_show();
+--------------------------+
| version_tokens_show()    |
+--------------------------+
| tok2=value2;tok1=value1; |
+--------------------------+

The following functions permit version tokens to be locked and unlocked:

• version_tokens_lock_exclusive(token_name[, token_name] ..., timeout)

Acquires exclusive locks on one or more version tokens, specified by name as strings, timing out with an
error if the locks are not acquired within the given timeout value.

mysql> SELECT version_tokens_lock_exclusive('lock1', 'lock2', 10);
+-----------------------------------------------------+
| version_tokens_lock_exclusive('lock1', 'lock2', 10) |
+-----------------------------------------------------+
|                                                   1 |
+-----------------------------------------------------+

• version_tokens_lock_shared(token_name[, token_name] ..., timeout)

Acquires shared locks on one or more version tokens, specified by name as strings, timing out with an
error if the locks are not acquired within the given timeout value.

mysql> SELECT version_tokens_lock_shared('lock1', 'lock2', 10);
+--------------------------------------------------+
| version_tokens_lock_shared('lock1', 'lock2', 10) |
+--------------------------------------------------+
|                                                1 |
+--------------------------------------------------+

• version_tokens_unlock()

Releases all locks that were acquired within the current session using
version_tokens_lock_exclusive() and version_tokens_lock_shared().

mysql> SELECT version_tokens_unlock();
+-------------------------+
| version_tokens_unlock() |
+-------------------------+
|                       1 |
+-------------------------+

The locking functions share these characteristics:

• The return value is nonzero for success. Otherwise, an error occurs.

1025

Version Tokens

• Token names are strings.

• In contrast to argument handling for the functions that manipulate the server token list, whitespace

surrounding token name arguments is not ignored and = and ; characters are permitted.

• It is possible to lock nonexisting token names. This does not create the tokens.

• Timeout values are nonnegative integers representing the time in seconds to wait to acquire locks before
timing out with an error. If the timeout is 0, there is no waiting and the function produces an error if locks
cannot be acquired immediately.

• Version Tokens locking functions are based on the locking service described at Section 5.5.6.1, “The

Locking Service”.

Version Tokens System Variables

Version Tokens supports the following system variables. These variables are unavailable unless the
Version Tokens plugin is installed (see Section 5.5.5.2, “Installing or Uninstalling Version Tokens”).

System variables:

• version_tokens_session

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

--version-tokens-session=value

version_tokens_session

Global, Session

Yes

String

NULL

The session value of this variable specifies the client version token list and indicates the tokens that the
client session requires the server version token list to have.

If the version_tokens_session variable is NULL (the default) or has an empty value, any server
version token list matches. (In effect, an empty value disables matching requirements.)

If the version_tokens_session variable has a nonempty value, any mismatch between its value
and the server version token list results in an error for any statement the session sends to the server. A
mismatch occurs under these conditions:

• A token name in the version_tokens_session value is not present in the server token list. In this

case, an ER_VTOKEN_PLUGIN_TOKEN_NOT_FOUND error occurs.

• A token value in the version_tokens_session value differs from the value of the corresponding

token in the server token list. In this case, an ER_VTOKEN_PLUGIN_TOKEN_MISMATCH error occurs.

It is not a mismatch for the server version token list to include a token not named in the
version_tokens_session value.

Suppose that a management application has set the server token list as follows:

mysql> SELECT version_tokens_set('tok1=a;tok2=b;tok3=c');
+--------------------------------------------+
| version_tokens_set('tok1=a;tok2=b;tok3=c') |
+--------------------------------------------+
| 3 version tokens set.                      |
+--------------------------------------------+

1026

MySQL Plugin Services

A client registers the tokens it requires the server to match by setting its version_tokens_session
value. Then, for each subsequent statement sent by the client, the server checks its token list against the
client version_tokens_session value and produces an error if there is a mismatch:

mysql> SET @@SESSION.version_tokens_session = 'tok1=a;tok2=b';
mysql> SELECT 1;
+---+
| 1 |
+---+
| 1 |
+---+

mysql> SET @@SESSION.version_tokens_session = 'tok1=b';
mysql> SELECT 1;
ERROR 3136 (42000): Version token mismatch for tok1. Correct value a

The first SELECT succeeds because the client tokens tok1 and tok2 are present in the server token list
and each token has the same value in the server list. The second SELECT fails because, although tok1
is present in the server token list, it has a different value than specified by the client.

At this point, any statement sent by the client fails, unless the server token list changes such that it
matches again. Suppose that the management application changes the server token list as follows:

mysql> SELECT version_tokens_edit('tok1=b');
+-------------------------------+
| version_tokens_edit('tok1=b') |
+-------------------------------+
| 1 version tokens updated.     |
+-------------------------------+
mysql> SELECT version_tokens_show();
+-----------------------+
| version_tokens_show() |
+-----------------------+
| tok3=c;tok1=b;tok2=b; |
+-----------------------+

Now the client version_tokens_session value matches the server token list and the client can once
again successfully execute statements:

mysql> SELECT 1;
+---+
| 1 |
+---+
| 1 |
+---+

• version_tokens_session_number

Command-Line Format

System Variable

Scope

Dynamic

Type

Default Value

This variable is for internal use.

5.5.6 MySQL Plugin Services

--version-tokens-session-number=#

version_tokens_session_number

Global, Session

No

Integer

0

1027

MySQL Plugin Services

MySQL server plugins have access to server “plugin services.” The plugin services interface complements
the plugin API by exposing server functionality that plugins can call. For developer information about
writing plugin services, see MySQL Services for Plugins. The following sections describe plugin services
available at the SQL and C-language levels.

5.5.6.1 The Locking Service

MySQL distributions provide a locking interface that is accessible at two levels:

• At the SQL level, as a set of loadable functions that each map onto calls to the service routines.

• As a C language interface, callable as a plugin service from server plugins or loadable functions.

For general information about plugin services, see Section 5.5.6, “MySQL Plugin Services”. For general
information about loadable functions, see Adding a Loadable Function.

The locking interface has these characteristics:

• Locks have three attributes: Lock namespace, lock name, and lock mode:

• Locks are identified by the combination of namespace and lock name. The namespace enables
different applications to use the same lock names without colliding by creating locks in separate
namespaces. For example, if applications A and B use namespaces of ns1 and ns2, respectively,
each application can use lock names lock1 and lock2 without interfering with the other application.

• A lock mode is either read or write. Read locks are shared: If a session has a read lock on a given lock
identifier, other sessions can acquire a read lock on the same identifier. Write locks are exclusive: If a
session has a write lock on a given lock identifier, other sessions cannot acquire a read or write lock
on the same identifier.

• Namespace and lock names must be non-NULL, nonempty, and have a maximum length of 64

characters. A namespace or lock name specified as NULL, the empty string, or a string longer than 64
characters results in an ER_LOCKING_SERVICE_WRONG_NAME error.

• The locking interface treats namespace and lock names as binary strings, so comparisons are case-

sensitive.

• The locking interface provides functions to acquire locks and release locks. No special privilege is
required to call these functions. Privilege checking is the responsibility of the calling application.

• Locks can be waited for if not immediately available. Lock acquisition calls take an integer timeout value

that indicates how many seconds to wait to acquire locks before giving up. If the timeout is reached
without successful lock acquisition, an ER_LOCKING_SERVICE_TIMEOUT error occurs. If the timeout is
0, there is no waiting and the call produces an error if locks cannot be acquired immediately.

• The locking interface detects deadlock between lock-acquisition calls in different sessions. In

this case, the locking service chooses a caller and terminates its lock-acquisition request with an
ER_LOCKING_SERVICE_DEADLOCK error. This error does not cause transactions to roll back. To
choose a session in case of deadlock, the locking service prefers sessions that hold read locks over
sessions that hold write locks.

• A session can acquire multiple locks with a single lock-acquisition call. For a given call, lock

acquisition is atomic: The call succeeeds if all locks are acquired. If acquisition of any lock fails,
the call acquires no locks and fails, typically with an ER_LOCKING_SERVICE_TIMEOUT or
ER_LOCKING_SERVICE_DEADLOCK error.

• A session can acquire multiple locks for the same lock identifier (namespace and lock name

combination). These lock instances can be read locks, write locks, or a mix of both.

1028

MySQL Plugin Services

• Locks acquired within a session are released explicitly by calling a release-locks function, or implicitly

when the session terminates (either normally or abnormally). Locks are not released when transactions
commit or roll back.

• Within a session, all locks for a given namespace when released are released together.

The interface provided by the locking service is distinct from that provided by GET_LOCK() and related
SQL functions (see Section 12.14, “Locking Functions”). For example, GET_LOCK() does not implement
namespaces and provides only exclusive locks, not distinct read and write locks.

The Locking Service C Interface

This section describes how to use the locking service C language interface. To use the function interface
instead, see The Locking Service Function Interface For general characteristics of the locking service
interface, see Section 5.5.6.1, “The Locking Service”. For general information about plugin services, see
Section 5.5.6, “MySQL Plugin Services”.

Source files that use the locking service should include this header file:

#include <mysql/service_locking.h>

To acquire one or more locks, call this function:

int mysql_acquire_locking_service_locks(MYSQL_THD opaque_thd,
                                        const char* lock_namespace,
                                        const char**lock_names,
                                        size_t lock_num,
                                        enum enum_locking_service_lock_type lock_type,
                                        unsigned long lock_timeout);

The arguments have these meanings:

• opaque_thd: A thread handle. If specified as NULL, the handle for the current thread is used.

• lock_namespace: A null-terminated string that indicates the lock namespace.

• lock_names: An array of null-terminated strings that provides the names of the locks to acquire.

• lock_num: The number of names in the lock_names array.

• lock_type: The lock mode, either LOCKING_SERVICE_READ or LOCKING_SERVICE_WRITE to

acquire read locks or write locks, respectively.

• lock_timeout: An integer number of seconds to wait to acquire the locks before giving up.

To release locks acquired for a given namespace, call this function:

int mysql_release_locking_service_locks(MYSQL_THD opaque_thd,
                                        const char* lock_namespace);

The arguments have these meanings:

• opaque_thd: A thread handle. If specified as NULL, the handle for the current thread is used.

• lock_namespace: A null-terminated string that indicates the lock namespace.

Locks acquired or waited for by the locking service can be monitored at the SQL level using the
Performance Schema. For details, see Locking Service Monitoring.

The Locking Service Function Interface

This section describes how to use the locking service interface provided by its loadable functions. To
use the C language interface instead, see The Locking Service C Interface For general characteristics of

1029

MySQL Plugin Services

the locking service interface, see Section 5.5.6.1, “The Locking Service”. For general information about
loadable functions, see Adding a Loadable Function.

• Installing or Uninstalling the Locking Service Function Interface

• Using the Locking Service Function Interface

• Locking Service Monitoring

• Locking Service Interface Function Reference

Installing or Uninstalling the Locking Service Function Interface

The locking service routines described in The Locking Service C Interface need not be installed because
they are built into the server. The same is not true of the loadable functions that map onto calls to the
service routines: The functions must be installed before use. This section describes how to do that. For
general information about loadable function installation, see Section 5.6.1, “Installing and Uninstalling
Loadable Functions”.

The locking service functions are implemented in a plugin library file located in the directory named by the
plugin_dir system variable. The file base name is locking_service. The file name suffix differs per
platform (for example, .so for Unix and Unix-like systems, .dll for Windows).

To install the locking service functions, use the CREATE FUNCTION statement, adjusting the .so suffix for
your platform as necessary:

CREATE FUNCTION service_get_read_locks RETURNS INT
  SONAME 'locking_service.so';
CREATE FUNCTION service_get_write_locks RETURNS INT
  SONAME 'locking_service.so';
CREATE FUNCTION service_release_locks RETURNS INT
  SONAME 'locking_service.so';

If the functions are used on a replication source server, install them on all replica servers as well to avoid
replication problems.

Once installed, the functions remain installed until uninstalled. To remove them, use the DROP FUNCTION
statement:

DROP FUNCTION service_get_read_locks;
DROP FUNCTION service_get_write_locks;
DROP FUNCTION service_release_locks;

Using the Locking Service Function Interface

Before using the locking service functions, install them according to the instructions provided at Installing or
Uninstalling the Locking Service Function Interface.

To acquire one or more read locks, call this function:

mysql> SELECT service_get_read_locks('mynamespace', 'rlock1', 'rlock2', 10);
+---------------------------------------------------------------+
| service_get_read_locks('mynamespace', 'rlock1', 'rlock2', 10) |
+---------------------------------------------------------------+
|                                                             1 |
+---------------------------------------------------------------+

The first argument is the lock namespace. The final argument is an integer timeout indicating how many
seconds to wait to acquire the locks before giving up. The arguments in between are the lock names.

For the example just shown, the function acquires locks with lock identifiers (mynamespace, rlock1)
and (mynamespace, rlock2).

1030

MySQL Plugin Services

To acquire write locks rather than read locks, call this function:

mysql> SELECT service_get_write_locks('mynamespace', 'wlock1', 'wlock2', 10);
+----------------------------------------------------------------+
| service_get_write_locks('mynamespace', 'wlock1', 'wlock2', 10) |
+----------------------------------------------------------------+
|                                                              1 |
+----------------------------------------------------------------+

In this case, the lock identifiers are (mynamespace, wlock1) and (mynamespace, wlock2).

To release all locks for a namespace, use this function:

mysql> SELECT service_release_locks('mynamespace');
+--------------------------------------+
| service_release_locks('mynamespace') |
+--------------------------------------+
|                                    1 |
+--------------------------------------+

Each locking function returns nonzero for success. If the function fails, an error occurs. For example, the
following error occurs because lock names cannot be empty:

mysql> SELECT service_get_read_locks('mynamespace', '', 10);
ERROR 3131 (42000): Incorrect locking service lock name ''.

A session can acquire multiple locks for the same lock identifier. As long as a different session does not
have a write lock for an identifier, the session can acquire any number of read or write locks. Each lock
request for the identifier acquires a new lock. The following statements acquire three write locks with the
same identifier, then three read locks for the same identifier:

SELECT service_get_write_locks('ns', 'lock1', 'lock1', 'lock1', 0);
SELECT service_get_read_locks('ns', 'lock1', 'lock1', 'lock1', 0);

If you examine the Performance Schema metadata_locks table at this point, you find that the
session holds six distinct locks with the same (ns, lock1) identifier. (For details, see Locking Service
Monitoring.)

Because the session holds at least one write lock on (ns, lock1), no other session can acquire a lock
for it, either read or write. If the session held only read locks for the identifier, other sessions could acquire
read locks for it, but not write locks.

Locks for a single lock-acquisition call are acquired atomically, but atomicity does not hold across calls.
Thus, for a statement such as the following, where service_get_write_locks() is called once per
row of the result set, atomicity holds for each individual call, but not for the statement as a whole:

SELECT service_get_write_locks('ns', 'lock1', 'lock2', 0) FROM t1 WHERE ... ;

Caution

Because the locking service returns a separate lock for each successful request for
a given lock identifier, it is possible for a single statement to acquire a large number
of locks. For example:

INSERT INTO ... SELECT service_get_write_locks('ns', t1.col_name, 0) FROM t1;

These types of statements may have certain adverse effects. For example, if the
statement fails part way through and rolls back, locks acquired up to the point of
failure still exist. If the intent is for there to be a correspondence between rows
inserted and locks acquired, that intent is not satisfied. Also, if it is important that
locks are granted in a certain order, be aware that result set order may differ

1031

MySQL Plugin Services

depending on which execution plan the optimizer chooses. For these reasons, it
may be best to limit applications to a single lock-acquisition call per statement.

Locking Service Monitoring

The locking service is implemented using the MySQL Server metadata locks framework, so you monitor
locking service locks acquired or waited for by examining the Performance Schema metadata_locks
table.

First, enable the metadata lock instrument:

mysql> UPDATE performance_schema.setup_instruments SET ENABLED = 'YES'
    -> WHERE NAME = 'wait/lock/metadata/sql/mdl';

Then acquire some locks and check the contents of the metadata_locks table:

mysql> SELECT service_get_write_locks('mynamespace', 'lock1', 0);
+----------------------------------------------------+
| service_get_write_locks('mynamespace', 'lock1', 0) |
+----------------------------------------------------+
|                                                  1 |
+----------------------------------------------------+
mysql> SELECT service_get_read_locks('mynamespace', 'lock2', 0);
+---------------------------------------------------+
| service_get_read_locks('mynamespace', 'lock2', 0) |
+---------------------------------------------------+
|                                                 1 |
+---------------------------------------------------+
mysql> SELECT OBJECT_TYPE, OBJECT_SCHEMA, OBJECT_NAME, LOCK_TYPE, LOCK_STATUS
    -> FROM performance_schema.metadata_locks
    -> WHERE OBJECT_TYPE = 'LOCKING SERVICE'\G
*************************** 1. row ***************************
  OBJECT_TYPE: LOCKING SERVICE
OBJECT_SCHEMA: mynamespace
  OBJECT_NAME: lock1
    LOCK_TYPE: EXCLUSIVE
  LOCK_STATUS: GRANTED
*************************** 2. row ***************************
  OBJECT_TYPE: LOCKING SERVICE
OBJECT_SCHEMA: mynamespace
  OBJECT_NAME: lock2
    LOCK_TYPE: SHARED
  LOCK_STATUS: GRANTED

Locking service locks have an OBJECT_TYPE value of LOCKING SERVICE. This is distinct from, for
example, locks acquired with the GET_LOCK() function, which have an OBJECT_TYPE of USER LEVEL
LOCK.

The lock namespace, name, and mode appear in the OBJECT_SCHEMA, OBJECT_NAME, and LOCK_TYPE
columns. Read and write locks have LOCK_TYPE values of SHARED and EXCLUSIVE, respectively.

The LOCK_STATUS value is GRANTED for an acquired lock, PENDING for a lock that is being waited for.
You see PENDING if one session holds a write lock and another session is attempting to acquire a lock
having the same identifier.

Locking Service Interface Function Reference

The SQL interface to the locking service implements the loadable functions described in this section. For
usage examples, see Using the Locking Service Function Interface.

The functions share these characteristics:

• The return value is nonzero for success. Otherwise, an error occurs.

1032

MySQL Plugin Services

• Namespace and lock names must be non-NULL, nonempty, and have a maximum length of 64

characters.

• Timeout values must be integers indicating how many seconds to wait to acquire locks before giving up
with an error. If the timeout is 0, there is no waiting and the function produces an error if locks cannot be
acquired immediately.

These locking service functions are available:

• service_get_read_locks(namespace, lock_name[, lock_name] ..., timeout)

Acquires one or more read (shared) locks in the given namespace using the given lock names, timing
out with an error if the locks are not acquired within the given timeout value.

• service_get_write_locks(namespace, lock_name[, lock_name] ..., timeout)

Acquires one or more write (exclusive) locks in the given namespace using the given lock names, timing
out with an error if the locks are not acquired within the given timeout value.

• service_release_locks(namespace)

For the given namespace, releases all locks that were acquired within the current session using
service_get_read_locks() and service_get_write_locks().

It is not an error for there to be no locks in the namespace.

5.5.6.2 The Keyring Service

MySQL Server supports a keyring service that enables internal server components and plugins to securely
store sensitive information for later retrieval. MySQL distributions provide a keyring interface that is
accessible at two levels:

• At the SQL level, as a set of loadable functions that each map onto calls to the service routines.

• As a C language interface, callable as a plugin service from server plugins or loadable functions.

This section describes how to use the keyring service functions to store, retrieve, and remove keys in the
MySQL keyring keystore. For information about the SQL interface that uses functions, Section 6.4.4.8,
“General-Purpose Keyring Key-Management Functions”. For general keyring information, see
Section 6.4.4, “The MySQL Keyring”.

The keyring service uses whatever underlying keyring plugin is enabled, if any. If no keyring plugin is
enabled, keyring service calls fail.

A “record” in the keystore consists of data (the key itself) and a unique identifier through which the key is
accessed. The identifier has two parts:

• key_id: The key ID or name. key_id values that begin with mysql_ are reserved by MySQL Server.

• user_id: The session effective user ID. If there is no user context, this value can be NULL. The value

need not actually be a “user”; the meaning depends on the application.

Functions that implement the keyring function interface pass the value of CURRENT_USER() as the
user_id value to keyring service functions.

The keyring service functions have these characteristics in common:

• Each function returns 0 for success, 1 for failure.

1033

MySQL Plugin Services

• The key_id and user_id arguments form a unique combination indicating which key in the keyring to

use.

• The key_type argument provides additional information about the key, such as its encryption method or

intended use.

• Keyring service functions treat key IDs, user names, types, and values as binary strings, so comparisons

are case-sensitive. For example, IDs of MyKey and mykey refer to different keys.

These keyring service functions are available:

• my_key_fetch()

Deobfuscates and retrieves a key from the keyring, along with its type. The function allocates the
memory for the buffers used to store the returned key and key type. The caller should zero or obfuscate
the memory when it is no longer needed, then free it.

Syntax:

my_bool my_key_fetch(const char *key_id, const char **key_type,
                     const char* user_id, void **key, size_t *key_len)

Arguments:

• key_id, user_id: Null-terminated strings that as a pair form a unique identifier indicating which key

to fetch.

• key_type: The address of a buffer pointer. The function stores into it a pointer to a null-terminated

string that provides additional information about the key (stored when the key was added).

• key: The address of a buffer pointer. The function stores into it a pointer to the buffer containing the

fetched key data.

• key_len: The address of a variable into which the function stores the size in bytes of the *key buffer.

Return value:

Returns 0 for success, 1 for failure.

• my_key_generate()

Generates a new random key of a given type and length and stores it in the keyring. The key has a
length of key_len and is associated with the identifier formed from key_id and user_id. The type
and length values must be consistent with the values supported by the underlying keyring plugin. See
Section 6.4.4.6, “Supported Keyring Key Types and Lengths”.

Syntax:

my_bool my_key_generate(const char *key_id, const char *key_type,
                        const char *user_id, size_t key_len)

Arguments:

• key_id, user_id: Null-terminated strings that as a pair form a unique identifier for the key to be

generated.

• key_type: A null-terminated string that provides additional information about the key.

• key_len: The size in bytes of the key to be generated.

1034

MySQL Server Loadable Functions

Return value:

Returns 0 for success, 1 for failure.

• my_key_remove()

Removes a key from the keyring.

Syntax:

my_bool my_key_remove(const char *key_id, const char* user_id)

Arguments:

• key_id, user_id: Null-terminated strings that as a pair form a unique identifier for the key to be

removed.

Return value:

Returns 0 for success, 1 for failure.

• my_key_store()

Obfuscates and stores a key in the keyring.

Syntax:

my_bool my_key_store(const char *key_id, const char *key_type,
                     const char* user_id, void *key, size_t key_len)

Arguments:

• key_id, user_id: Null-terminated strings that as a pair form a unique identifier for the key to be

stored.

• key_type: A null-terminated string that provides additional information about the key.

• key: The buffer containing the key data to be stored.

• key_len: The size in bytes of the key buffer.

Return value:

Returns 0 for success, 1 for failure.

5.6 MySQL Server Loadable Functions

MySQL supports loadable functions, that is, functions that are not built in but can be loaded at runtime
(either during startup or later) to extend server capabilities, or unloaded to remove capabilities. For a table
describing the available loadable functions, see Section 12.2, “Loadable Function Reference”. Loadable
functions contrast with built-in (native) functions, which are implemented as part of the server and are
always available; for a table, see Section 12.1, “Built-In Function and Operator Reference”.

Note

Loadable functions previously were known as user-defined functions (UDFs). That
terminology was something of a misnomer because “user-defined” also can apply

1035

Installing and Uninstalling Loadable Functions

to other types of functions, such as stored functions (a type of stored object written
using SQL) and native functions added by modifying the server source code.

MySQL distributions include loadable functions that implement, in whole or in part, these server
capabilities:

• MySQL Enterprise Edition includes functions that perform encryption operations based on the OpenSSL

library. See Section 6.6, “MySQL Enterprise Encryption”.

• MySQL Enterprise Edition includes functions that provide an SQL-level API for masking and de-

identification operations. See Section 6.5.1, “MySQL Enterprise Data Masking and De-Identification
Elements”.

• MySQL Enterprise Edition includes audit logging for monitoring and logging of connection and query

activity. See Section 6.4.5, “MySQL Enterprise Audit”.

• MySQL Enterprise Edition includes a firewall capability that implements an application-level firewall to

enable database administrators to permit or deny SQL statement execution based on matching against
patterns for accepted statement. See Section 6.4.6, “MySQL Enterprise Firewall”.

• A query rewriter examines statements received by MySQL Server and possibly rewrites them before the

server executes them. See Section 5.5.4, “The Rewriter Query Rewrite Plugin”

• Version Tokens enables creation of and synchronization around server tokens that applications can use

to prevent accessing incorrect or out-of-date data. See Section 5.5.5, “Version Tokens”.

• The MySQL Keyring provides secure storage for sensitive information. See Section 6.4.4, “The MySQL

Keyring”.

• A locking service provides a locking interface for application use. See Section 5.5.6.1, “The Locking

Service”.

The following sections describe how to install and uninstall loadable functions, and how to determine at
runtime which loadable functions are installed and obtain information about them.

For information about writing loadable functions, see Adding Functions to MySQL.

5.6.1 Installing and Uninstalling Loadable Functions

Loadable functions, as the name implies, must be loaded into the server before they can be used. MySQL
supports automatic function loading during server startup and manual loading thereafter.

While a loadable function is loaded, information about it is available as described in Section 5.6.2,
“Obtaining Information About Loadable Functions”.

• Installing Loadable Functions

• Uninstalling Loadable Functions

• Reinstalling or Upgrading Loadable Functions

Installing Loadable Functions

To load a loadable function manually, use the CREATE FUNCTION statement. For example:

CREATE FUNCTION metaphon
  RETURNS STRING
  SONAME 'udf_example.so';

1036

Obtaining Information About Loadable Functions

The file base name depends on your platform. Common suffixes are .so for Unix and Unix-like systems,
.dll for Windows.

CREATE FUNCTION has these effects:

• It loads the function into the server to make it available immediately.

• It registers the function in the mysql.func system table to make it persistent across server restarts. For

this reason, CREATE FUNCTION requires the INSERT privilege for the mysql system database.

Automatic loading of loadable functions occurs during the normal server startup sequence. The server
loads functions registered in the mysql.func table. If the server is started with the --skip-grant-
tables option, functions registered in the table are not loaded and are unavailable.

Uninstalling Loadable Functions

To remove a loadable function, use the DROP FUNCTION statement. For example:

DROP FUNCTION metaphon;

DROP FUNCTION has these effects:

• It unloads the function to make it unavailable.

• It removes the function from the mysql.func system table. For this reason, DROP FUNCTION requires

the DELETE privilege for the mysql system database. With the function no longer registered in the
mysql.func table, the server does not load the function during subsequent restarts.

While a loadable function is loaded, information about it is available from the mysql.func system table.
See Section 5.6.2, “Obtaining Information About Loadable Functions”. CREATE FUNCTION adds the
function to the table and DROP FUNCTION removes it.

Reinstalling or Upgrading Loadable Functions

To reinstall or upgrade the shared library associated with a loadable function, issue a DROP FUNCTION
statement, upgrade the shared library, and then issue a CREATE FUNCTION statement. If you upgrade the
shared library first and then use DROP FUNCTION, the server may unexpectedly shut down.

5.6.2 Obtaining Information About Loadable Functions

The mysql.func system table shows which loadable functions have been registered using CREATE
FUNCTION:

SELECT * FROM mysql.func;

The func table has these columns:

• name

The function name as referred to in SQL statements.

• ret

The function return value type. Permitted values are 0 (STRING), 1 (REAL), 2 (INTEGER), 3 (ROW), or 4
(DECIMAL).

• dl

The name of the function library file containing the executable function code. The file is located in the
directory named by the plugin_dir system variable.

1037

Running Multiple MySQL Instances on One Machine

• type

The function type, either function (scalar) or aggregate.

5.7 Running Multiple MySQL Instances on One Machine

In some cases, you might want to run multiple instances of MySQL on a single machine. You might want
to test a new MySQL release while leaving an existing production setup undisturbed. Or you might want to
give different users access to different mysqld servers that they manage themselves. (For example, you
might be an Internet Service Provider that wants to provide independent MySQL installations for different
customers.)

It is possible to use a different MySQL server binary per instance, or use the same binary for multiple
instances, or any combination of the two approaches. For example, you might run a server from MySQL
5.6 and one from MySQL 5.7, to see how different versions handle a given workload. Or you might run
multiple instances of the current production version, each managing a different set of databases.

Whether or not you use distinct server binaries, each instance that you run must be configured with unique
values for several operating parameters. This eliminates the potential for conflict between instances.
Parameters can be set on the command line, in option files, or by setting environment variables. See
Section 4.2.2, “Specifying Program Options”. To see the values used by a given instance, connect to it and
execute a SHOW VARIABLES statement.

The primary resource managed by a MySQL instance is the data directory. Each instance should use a
different data directory, the location of which is specified using the --datadir=dir_name option. For
methods of configuring each instance with its own data directory, and warnings about the dangers of failing
to do so, see Section 5.7.1, “Setting Up Multiple Data Directories”.

In addition to using different data directories, several other options must have different values for each
server instance:

• --port=port_num

--port controls the port number for TCP/IP connections. Alternatively, if the host has multiple network
addresses, you can set the bind_address system variable to cause each server to listen to a different
address.

• --socket={file_name|pipe_name}

--socket controls the Unix socket file path on Unix or the named-pipe name on Windows. On
Windows, it is necessary to specify distinct pipe names only for those servers configured to permit
named-pipe connections.

• --shared-memory-base-name=name

This option is used only on Windows. It designates the shared-memory name used by a Windows server
to permit clients to connect using shared memory. It is necessary to specify distinct shared-memory
names only for those servers configured to permit shared-memory connections.

• --pid-file=file_name

This option indicates the path name of the file in which the server writes its process ID.

If you use the following log file options, their values must differ for each server:

• --general_log_file=file_name

1038

Setting Up Multiple Data Directories

• --log-bin[=file_name]

• --slow_query_log_file=file_name

• --log-error[=file_name]

For further discussion of log file options, see Section 5.4, “MySQL Server Logs”.

To achieve better performance, you can specify the following option differently for each server, to spread
the load between several physical disks:

• --tmpdir=dir_name

Having different temporary directories also makes it easier to determine which MySQL server created any
given temporary file.

If you have multiple MySQL installations in different locations, you can specify the base directory for each
installation with the --basedir=dir_name option. This causes each instance to automatically use a
different data directory, log files, and PID file because the default for each of those parameters is relative
to the base directory. In that case, the only other options you need to specify are the --socket and --
port options. Suppose that you install different versions of MySQL using tar file binary distributions.
These install in different locations, so you can start the server for each installation using the command
bin/mysqld_safe under its corresponding base directory. mysqld_safe determines the proper --
basedir option to pass to mysqld, and you need specify only the --socket and --port options to
mysqld_safe.

As discussed in the following sections, it is possible to start additional servers by specifying appropriate
command options or by setting environment variables. However, if you need to run multiple servers on
a more permanent basis, it is more convenient to use option files to specify for each server those option
values that must be unique to it. The --defaults-file option is useful for this purpose.

5.7.1 Setting Up Multiple Data Directories

Each MySQL Instance on a machine should have its own data directory. The location is specified using the
--datadir=dir_name option.

There are different methods of setting up a data directory for a new instance:

• Create a new data directory.

• Copy an existing data directory.

The following discussion provides more detail about each method.

Warning

Normally, you should never have two servers that update data in the same
databases. This may lead to unpleasant surprises if your operating system does
not support fault-free system locking. If (despite this warning) you run multiple
servers using the same data directory and they have logging enabled, you must
use the appropriate options to specify log file names that are unique to each server.
Otherwise, the servers try to log to the same files.

Even when the preceding precautions are observed, this kind of setup works only
with MyISAM and MERGE tables, and not with any of the other storage engines. Also,
this warning against sharing a data directory among servers always applies in an
NFS environment. Permitting multiple MySQL servers to access a common data

1039

Running Multiple MySQL Instances on Windows

directory over NFS is a very bad idea. The primary problem is that NFS is the speed
bottleneck. It is not meant for such use. Another risk with NFS is that you must
devise a way to ensure that two or more servers do not interfere with each other.
Usually NFS file locking is handled by the lockd daemon, but at the moment there
is no platform that performs locking 100% reliably in every situation.

Create a New Data Directory

With this method, the data directory is in the same state as when you first install MySQL. It has the default
set of MySQL accounts and no user data.

On Unix, initialize the data directory. See Section 2.9, “Postinstallation Setup and Testing”.

On Windows, the data directory is included in the MySQL distribution:

• MySQL Zip archive distributions for Windows contain an unmodified data directory. You can unpack

such a distribution into a temporary location, then copy it data directory to where you are setting up the
new instance.

• Windows MSI package installers create and set up the data directory that the installed server uses, but
also create a pristine “template” data directory named data under the installation directory. After an
installation has been performed using an MSI package, the template data directory can be copied to set
up additional MySQL instances.

Copy an Existing Data Directory

With this method, any MySQL accounts or user data present in the data directory are carried over to the
new data directory.

1. Stop the existing MySQL instance using the data directory. This must be a clean shutdown so that the

instance flushes any pending changes to disk.

2. Copy the data directory to the location where the new data directory should be.

3. Copy the my.cnf or my.ini option file used by the existing instance. This serves as a basis for the

new instance.

4. Modify the new option file so that any pathnames referring to the original data directory refer to the
new data directory. Also, modify any other options that must be unique per instance, such as the
TCP/IP port number and the log files. For a list of parameters that must be unique per instance, see
Section 5.7, “Running Multiple MySQL Instances on One Machine”.

5. Start the new instance, telling it to use the new option file.

5.7.2 Running Multiple MySQL Instances on Windows

You can run multiple servers on Windows by starting them manually from the command line, each with
appropriate operating parameters, or by installing several servers as Windows services and running them
that way. General instructions for running MySQL from the command line or as a service are given in
Section 2.3, “Installing MySQL on Microsoft Windows”. The following sections describe how to start each
server with different values for those options that must be unique per server, such as the data directory.
These options are listed in Section 5.7, “Running Multiple MySQL Instances on One Machine”.

5.7.2.1 Starting Multiple MySQL Instances at the Windows Command Line

The procedure for starting a single MySQL server manually from the command line is described in
Section 2.3.4.6, “Starting MySQL from the Windows Command Line”. To start multiple servers this way,

1040

Running Multiple MySQL Instances on Windows

you can specify the appropriate options on the command line or in an option file. It is more convenient
to place the options in an option file, but it is necessary to make sure that each server gets its own set
of options. To do this, create an option file for each server and tell the server the file name with a --
defaults-file option when you run it.

Suppose that you want to run one instance of mysqld on port 3307 with a data directory of C:\mydata1,
and another instance on port 3308 with a data directory of C:\mydata2. Use this procedure:

1. Make sure that each data directory exists, including its own copy of the mysql database that contains

the grant tables.

2. Create two option files. For example, create one file named C:\my-opts1.cnf that looks like this:

[mysqld]
datadir = C:/mydata1
port = 3307

Create a second file named C:\my-opts2.cnf that looks like this:

[mysqld]
datadir = C:/mydata2
port = 3308

3. Use the --defaults-file option to start each server with its own option file:

C:\> C:\mysql\bin\mysqld --defaults-file=C:\my-opts1.cnf
C:\> C:\mysql\bin\mysqld --defaults-file=C:\my-opts2.cnf

Each server starts in the foreground (no new prompt appears until the server exits later), so you must
issue those two commands in separate console windows.

To shut down the servers, connect to each using the appropriate port number:

C:\> C:\mysql\bin\mysqladmin --port=3307 --host=127.0.0.1 --user=root --password shutdown
C:\> C:\mysql\bin\mysqladmin --port=3308 --host=127.0.0.1 --user=root --password shutdown

Servers configured as just described permit clients to connect over TCP/IP. If your version of Windows
supports named pipes and you also want to permit named-pipe connections, specify options that enable
the named pipe and specify its name. Each server that supports named-pipe connections must use a
unique pipe name. For example, the C:\my-opts1.cnf file might be written like this:

[mysqld]
datadir = C:/mydata1
port = 3307
enable-named-pipe
socket = mypipe1

Modify C:\my-opts2.cnf similarly for use by the second server. Then start the servers as described
previously.

A similar procedure applies for servers that you want to permit shared-memory connections. Enable such
connections by starting the server with the shared_memory system variable enabled and specify a unique
shared-memory name for each server by setting the shared_memory_base_name system variable.

5.7.2.2 Starting Multiple MySQL Instances as Windows Services

On Windows, a MySQL server can run as a Windows service. The procedures for installing, controlling,
and removing a single MySQL service are described in Section 2.3.4.8, “Starting MySQL as a Windows
Service”.

1041

Running Multiple MySQL Instances on Windows

To set up multiple MySQL services, you must make sure that each instance uses a different service name
in addition to the other parameters that must be unique per instance.

For the following instructions, suppose that you want to run the mysqld server from two different versions
of MySQL that are installed at C:\mysql-5.7.9 and C:\mysql-5.7.44, respectively. (This might be
the case if you are running 5.7.9 as your production server, but also want to conduct tests using 5.7.44.)

To install MySQL as a Windows service, use the --install or --install-manual option. For
information about these options, see Section 2.3.4.8, “Starting MySQL as a Windows Service”.

Based on the preceding information, you have several ways to set up multiple services. The following
instructions describe some examples. Before trying any of them, shut down and remove any existing
MySQL services.

• Approach 1: Specify the options for all services in one of the standard option files. To do this, use a

different service name for each server. Suppose that you want to run the 5.7.9 mysqld using the service
name of mysqld1 and the 5.7.44 mysqld using the service name mysqld2. In this case, you can use
the [mysqld1] group for 5.7.9 and the [mysqld2] group for 5.7.44. For example, you can set up C:
\my.cnf like this:

# options for mysqld1 service
[mysqld1]
basedir = C:/mysql-5.7.9
port = 3307
enable-named-pipe
socket = mypipe1

# options for mysqld2 service
[mysqld2]
basedir = C:/mysql-5.7.44
port = 3308
enable-named-pipe
socket = mypipe2

Install the services as follows, using the full server path names to ensure that Windows registers the
correct executable program for each service:

C:\> C:\mysql-5.7.9\bin\mysqld --install mysqld1
C:\> C:\mysql-5.7.44\bin\mysqld --install mysqld2

To start the services, use the services manager, or NET START or SC START with the appropriate
service names:

C:\> SC START mysqld1
C:\> SC START mysqld2

To stop the services, use the services manager, or use NET STOP or SC STOP with the appropriate
service names:

C:\> SC STOP mysqld1
C:\> SC STOP mysqld2

• Approach 2: Specify options for each server in separate files and use --defaults-file when you
install the services to tell each server what file to use. In this case, each file should list options using a
[mysqld] group.

With this approach, to specify options for the 5.7.9 mysqld, create a file C:\my-opts1.cnf that looks
like this:

[mysqld]
basedir = C:/mysql-5.7.9

1042

Running Multiple MySQL Instances on Unix

port = 3307
enable-named-pipe
socket = mypipe1

For the 5.7.44 mysqld, create a file C:\my-opts2.cnf that looks like this:

[mysqld]
basedir = C:/mysql-5.7.44
port = 3308
enable-named-pipe
socket = mypipe2

Install the services as follows (enter each command on a single line):

C:\> C:\mysql-5.7.9\bin\mysqld --install mysqld1
           --defaults-file=C:\my-opts1.cnf
C:\> C:\mysql-5.7.44\bin\mysqld --install mysqld2
           --defaults-file=C:\my-opts2.cnf

When you install a MySQL server as a service and use a --defaults-file option, the service name
must precede the option.

After installing the services, start and stop them the same way as in the preceding example.

To remove multiple services, use SC DELETE mysqld_service_name for each one. Alternatively, use
mysqld --remove for each one, specifying a service name following the --remove option. If the service
name is the default (MySQL), you can omit it when using mysqld --remove.

5.7.3 Running Multiple MySQL Instances on Unix

Note

The discussion here uses mysqld_safe to launch multiple instances of
MySQL. For MySQL installation using an RPM distribution, server startup and
shutdown is managed by systemd on several Linux platforms. On these platforms,
mysqld_safe is not installed because it is unnecessary. For information about
using systemd to handle multiple MySQL instances, see Section 2.5.10, “Managing
MySQL Server with systemd”.

One way is to run multiple MySQL instances on Unix is to compile different servers with different default
TCP/IP ports and Unix socket files so that each one listens on different network interfaces. Compiling in
different base directories for each installation also results automatically in a separate, compiled-in data
directory, log file, and PID file location for each server.

Assume that an existing 5.6 server is configured for the default TCP/IP port number (3306) and Unix
socket file (/tmp/mysql.sock). To configure a new 5.7.44 server to have different operating parameters,
use a CMake command something like this:

$> cmake . -DMYSQL_TCP_PORT=port_number \
             -DMYSQL_UNIX_ADDR=file_name \
             -DCMAKE_INSTALL_PREFIX=/usr/local/mysql-5.7.44

Here, port_number and file_name must be different from the default TCP/IP port number and Unix
socket file path name, and the CMAKE_INSTALL_PREFIX value should specify an installation directory
different from the one under which the existing MySQL installation is located.

If you have a MySQL server listening on a given port number, you can use the following command to find
out what operating parameters it is using for several important configurable variables, including the base
directory and Unix socket file name:

1043

Using Client Programs in a Multiple-Server Environment

$> mysqladmin --host=host_name --port=port_number variables

With the information displayed by that command, you can tell what option values not to use when
configuring an additional server.

If you specify localhost as the host name, mysqladmin defaults to using a Unix socket file rather than
TCP/IP. To explicitly specify the transport protocol, use the --protocol={TCP|SOCKET|PIPE|MEMORY}
option.

You need not compile a new MySQL server just to start with a different Unix socket file and TCP/IP port
number. It is also possible to use the same server binary and start each invocation of it with different
parameter values at runtime. One way to do so is by using command-line options:

$> mysqld_safe --socket=file_name --port=port_number

To start a second server, provide different --socket and --port option values, and pass a --
datadir=dir_name option to mysqld_safe so that the server uses a different data directory.

Alternatively, put the options for each server in a different option file, then start each server using a --
defaults-file option that specifies the path to the appropriate option file. For example, if the option files
for two server instances are named /usr/local/mysql/my.cnf and /usr/local/mysql/my.cnf2,
start the servers like this: command:

$> mysqld_safe --defaults-file=/usr/local/mysql/my.cnf
$> mysqld_safe --defaults-file=/usr/local/mysql/my.cnf2

Another way to achieve a similar effect is to use environment variables to set the Unix socket file name and
TCP/IP port number:

$> MYSQL_UNIX_PORT=/tmp/mysqld-new.sock
$> MYSQL_TCP_PORT=3307
$> export MYSQL_UNIX_PORT MYSQL_TCP_PORT
$> mysqld --initialize --user=mysql
...set root password...
$> mysqld_safe --datadir=/path/to/datadir &

This is a quick way of starting a second server to use for testing. The nice thing about this method is that
the environment variable settings apply to any client programs that you invoke from the same shell. Thus,
connections for those clients are automatically directed to the second server.

Section 4.9, “Environment Variables”, includes a list of other environment variables you can use to affect
MySQL programs.

On Unix, the mysqld_multi script provides another way to start multiple servers. See Section 4.3.4,
“mysqld_multi — Manage Multiple MySQL Servers”.

5.7.4 Using Client Programs in a Multiple-Server Environment

To connect with a client program to a MySQL server that is listening to different network interfaces from
those compiled into your client, you can use one of the following methods:

• Start the client with --host=host_name --port=port_number to connect using TCP/IP to a remote
server, with --host=127.0.0.1 --port=port_number to connect using TCP/IP to a local server, or
with --host=localhost --socket=file_name to connect to a local server using a Unix socket file
or a Windows named pipe.

• Start the client with --protocol=TCP to connect using TCP/IP, --protocol=SOCKET to connect

using a Unix socket file, --protocol=PIPE to connect using a named pipe, or --protocol=MEMORY
to connect using shared memory. For TCP/IP connections, you may also need to specify --host and

1044

Debugging MySQL

--port options. For the other types of connections, you may need to specify a --socket option to
specify a Unix socket file or Windows named-pipe name, or a --shared-memory-base-name option
to specify the shared-memory name. Shared-memory connections are supported only on Windows.

•     On Unix, set the MYSQL_UNIX_PORT and MYSQL_TCP_PORT environment variables to point to the
Unix socket file and TCP/IP port number before you start your clients. If you normally use a specific
socket file or port number, you can place commands to set these environment variables in your .login
file so that they apply each time you log in. See Section 4.9, “Environment Variables”.

• Specify the default Unix socket file and TCP/IP port number in the [client] group of an option file. For
example, you can use C:\my.cnf on Windows, or the .my.cnf file in your home directory on Unix.
See Section 4.2.2.2, “Using Option Files”.

• In a C program, you can specify the socket file or port number arguments in the

mysql_real_connect() call. You can also have the program read option files by calling
mysql_options(). See C API Basic Function Descriptions.

• If you are using the Perl DBD::mysql module, you can read options from MySQL option files. For

example:

$dsn = "DBI:mysql:test;mysql_read_default_group=client;"
        . "mysql_read_default_file=/usr/local/mysql/data/my.cnf";
$dbh = DBI->connect($dsn, $user, $password);

See Section 27.9, “MySQL Perl API”.

Other programming interfaces may provide similar capabilities for reading option files.

5.8 Debugging MySQL

This section describes debugging techniques that assist efforts to track down problems in MySQL.

5.8.1 Debugging a MySQL Server

If you are using some functionality that is very new in MySQL, you can try to run mysqld with the --skip-
new option (which disables all new, potentially unsafe functionality). See Section B.3.3.3, “What to Do If
MySQL Keeps Crashing”.

If mysqld does not want to start, verify that you have no my.cnf files that interfere with your setup! You
can check your my.cnf arguments with mysqld --print-defaults and avoid using them by starting
with mysqld --no-defaults ....

If mysqld starts to eat up CPU or memory or if it “hangs,” you can use mysqladmin processlist
status to find out if someone is executing a query that takes a long time. It may be a good idea to run
mysqladmin -i10 processlist status in some window if you are experiencing performance
problems or problems when new clients cannot connect.

The command mysqladmin debug dumps some information about locks in use, used memory and query
usage to the MySQL log file. This may help solve some problems. This command also provides some
useful information even if you have not compiled MySQL for debugging!

If the problem is that some tables are getting slower and slower you should try to optimize the table with
OPTIMIZE TABLE or myisamchk. See Chapter 5, MySQL Server Administration. You should also check
the slow queries with EXPLAIN.

You should also read the OS-specific section in this manual for problems that may be unique to your
environment. See Section 2.1, “General Installation Guidance”.

1045

Debugging a MySQL Server

5.8.1.1 Compiling MySQL for Debugging

If you have some very specific problem, you can always try to debug MySQL. To do this you must
configure MySQL with the -DWITH_DEBUG=1 option. You can check whether MySQL was compiled
with debugging by doing: mysqld --help. If the --debug flag is listed with the options then you have
debugging enabled. mysqladmin ver also lists the mysqld version as mysql ... --debug in this
case.

If mysqld stops crashing when you configure it with the -DWITH_DEBUG=1 CMake option, you probably
have found a compiler bug or a timing bug within MySQL. In this case, you can try to add -g using the
CMAKE_C_FLAGS and CMAKE_CXX_FLAGS CMake options and not use -DWITH_DEBUG=1. If mysqld
dies, you can at least attach to it with gdb or use gdb on the core file to find out what happened.

When you configure MySQL for debugging you automatically enable a lot of extra safety check functions
that monitor the health of mysqld. If they find something “unexpected,” an entry is written to stderr,
which mysqld_safe directs to the error log! This also means that if you are having some unexpected
problems with MySQL and are using a source distribution, the first thing you should do is to configure
MySQL for debugging. If you believe that you have found a bug, please use the instructions at Section 1.5,
“How to Report Bugs or Problems”.

In the Windows MySQL distribution, mysqld.exe is by default compiled with support for trace files.

5.8.1.2 Creating Trace Files

If the mysqld server does not start or it crashes easily, you can try to create a trace file to find the problem.

To do this, you must have a mysqld that has been compiled with debugging support. You can check this
by executing mysqld -V. If the version number ends with -debug, it is compiled with support for trace
files. (On Windows, the debugging server is named mysqld-debug rather than mysqld.)

Start the mysqld server with a trace log in /tmp/mysqld.trace on Unix or \mysqld.trace on
Windows:

$> mysqld --debug

On Windows, you should also use the --standalone flag to not start mysqld as a service. In a console
window, use this command:

C:\> mysqld-debug --debug --standalone

After this, you can use the mysql.exe command-line tool in a second console window to reproduce the
problem. You can stop the mysqld server with mysqladmin shutdown.

The trace file can become very large! To generate a smaller trace file, you can use debugging options
something like this:

mysqld --debug=d,info,error,query,general,where:O,/tmp/mysqld.trace

This only prints information with the most interesting tags to the trace file.

If you file a bug, please add only those lines from the trace file to the bug report that indicate where
something seems to go wrong. If you cannot locate the wrong place, open a bug report and upload
the whole trace file to the report, so that a MySQL developer can take a look at it. For instructions, see
Section 1.5, “How to Report Bugs or Problems”.

The trace file is made with the DBUG package by Fred Fish. See Section 5.8.3, “The DBUG Package”.

1046

Debugging a MySQL Server

5.8.1.3 Using WER with PDB to create a Windows crashdump

Program Database files (with suffix pdb) are included in the ZIP Archive Debug Binaries & Test Suite
distribution of MySQL. These files provide information for debugging your MySQL installation in the event
of a problem. This is a separate download from the standard MSI or Zip file.

Note

The PDB files are available in a separate file labeled "ZIP Archive Debug Binaries &
Test Suite".

The PDB file contains more detailed information about mysqld and other tools that enables more detailed
trace and dump files to be created. You can use these with WinDbg or Visual Studio to debug mysqld.

For more information on PDB files, see Microsoft Knowledge Base Article 121366. For more information on
the debugging options available, see Debugging Tools for Windows.

To use WinDbg, either install the full Windows Driver Kit (WDK) or install the standalone version.

Important

The .exe and .pdb files must be an exact match (both version number and
MySQL server edition) or WinDBG complains while attempting to load the symbols.

1. To generate a minidump mysqld.dmp, enable the core-file option under the [mysqld] section in

my.ini. Restart the MySQL server after making these changes.

2. Create a directory to store the generated files, such as c:\symbols

3. Determine the path to your windbg.exe executable using the Find GUI or from the command line,

for example: dir /s /b windbg.exe -- a common default is C:\Program Files\Debugging Tools for
Windows (x64)\windbg.exe

4. Launch windbg.exe giving it the paths to mysqld-debug.exe, mysqld.pdb, mysqld.dmp, and the

source code. Alternatively, pass in each path from the WinDbg GUI. For example:

windbg.exe -i "C:\mysql-5.7.44-winx64\bin\"^
 -z "C:\mysql-5.7.44-winx64\data\mysqld.dmp"^
 -srcpath "E:\ade\mysql_archives\5.7\5.7.44\mysql-5.7.44"^
 -y "C:\mysql-5.7.44-winx64\bin;SRV*c:\symbols*http://msdl.microsoft.com/download/symbols"^
 -v -n -c "!analyze -vvvvv"

Note

The ^ character and newline are removed by the Windows command line
processor, so be sure the spaces remain intact.

5.8.1.4 Debugging mysqld under gdb

On most systems you can also start mysqld from gdb to get more information if mysqld crashes.

With some older gdb versions on Linux you must use run --one-thread if you want to be able to debug
mysqld threads. In this case, you can only have one thread active at a time.

NPTL threads (the new thread library on Linux) may cause problems while running mysqld under gdb.
Some symptoms are:

• mysqld hangs during startup (before it writes ready for connections).

• mysqld crashes during a pthread_mutex_lock() or pthread_mutex_unlock() call.

1047

Debugging a MySQL Server

In this case, you should set the following environment variable in the shell before starting gdb:

LD_ASSUME_KERNEL=2.4.1
export LD_ASSUME_KERNEL

When running mysqld under gdb, you should disable the stack trace with --skip-stack-trace to be
able to catch segfaults within gdb.

Use the --gdb option to mysqld to install an interrupt handler for SIGINT (needed to stop mysqld with
^C to set breakpoints) and disable stack tracing and core file handling.

It is very hard to debug MySQL under gdb if you do a lot of new connections the whole time as
gdb does not free the memory for old threads. You can avoid this problem by starting mysqld with
thread_cache_size set to a value equal to max_connections + 1. In most cases just using --
thread_cache_size=5' helps a lot!

If you want to get a core dump on Linux if mysqld dies with a SIGSEGV signal, you can start mysqld with
the --core-file option. This core file can be used to make a backtrace that may help you find out why
mysqld died:

$> gdb mysqld core
gdb>   backtrace full
gdb>   quit

See Section B.3.3.3, “What to Do If MySQL Keeps Crashing”.

If you are using gdb on Linux, you should install a .gdb file, with the following information, in your current
directory:

set print sevenbit off
handle SIGUSR1 nostop noprint
handle SIGUSR2 nostop noprint
handle SIGWAITING nostop noprint
handle SIGLWP nostop noprint
handle SIGPIPE nostop
handle SIGALRM nostop
handle SIGHUP nostop
handle SIGTERM nostop noprint

Here is an example how to debug mysqld:

$> gdb /usr/local/libexec/mysqld
gdb> run
...
backtrace full # Do this when mysqld crashes

Include the preceding output in a bug report, which you can file using the instructions in Section 1.5, “How
to Report Bugs or Problems”.

If mysqld hangs, you can try to use some system tools like strace or /usr/proc/bin/pstack to
examine where mysqld has hung.

strace /tmp/log libexec/mysqld

If you are using the Perl DBI interface, you can turn on debugging information by using the trace method
or by setting the DBI_TRACE environment variable.

5.8.1.5 Using a Stack Trace

On some operating systems, the error log contains a stack trace if mysqld dies unexpectedly. You can
use this to find out where (and maybe why) mysqld died. See Section 5.4.2, “The Error Log”. To get

1048

Debugging a MySQL Server

a stack trace, you must not compile mysqld with the -fomit-frame-pointer option to gcc. See
Section 5.8.1.1, “Compiling MySQL for Debugging”.

A stack trace in the error log looks something like this:

mysqld got signal 11;
Attempting backtrace. You can use the following information
to find out where mysqld died. If you see no messages after
this, something went terribly wrong...

stack_bottom = 0x41fd0110 thread_stack 0x40000
mysqld(my_print_stacktrace+0x32)[0x9da402]
mysqld(handle_segfault+0x28a)[0x6648e9]
/lib/libpthread.so.0[0x7f1a5af000f0]
/lib/libc.so.6(strcmp+0x2)[0x7f1a5a10f0f2]
mysqld(_Z21check_change_passwordP3THDPKcS2_Pcj+0x7c)[0x7412cb]
mysqld(_ZN16set_var_password5checkEP3THD+0xd0)[0x688354]
mysqld(_Z17sql_set_variablesP3THDP4ListI12set_var_baseE+0x68)[0x688494]
mysqld(_Z21mysql_execute_commandP3THD+0x41a0)[0x67a170]
mysqld(_Z11mysql_parseP3THDPKcjPS2_+0x282)[0x67f0ad]
mysqld(_Z16dispatch_command19enum_server_commandP3THDPcj+0xbb7[0x67fdf8]
mysqld(_Z10do_commandP3THD+0x24d)[0x6811b6]
mysqld(handle_one_connection+0x11c)[0x66e05e]

If resolution of function names for the trace fails, the trace contains less information:

mysqld got signal 11;
Attempting backtrace. You can use the following information
to find out where mysqld died. If you see no messages after
this, something went terribly wrong...

stack_bottom = 0x41fd0110 thread_stack 0x40000
[0x9da402]
[0x6648e9]
[0x7f1a5af000f0]
[0x7f1a5a10f0f2]
[0x7412cb]
[0x688354]
[0x688494]
[0x67a170]
[0x67f0ad]
[0x67fdf8]
[0x6811b6]
[0x66e05e]

In the latter case, you can use the resolve_stack_dump utility to determine where mysqld died by
using the following procedure:

1. Copy the numbers from the stack trace to a file, for example mysqld.stack. The numbers should not

include the surrounding square brackets:

0x9da402
0x6648e9
0x7f1a5af000f0
0x7f1a5a10f0f2
0x7412cb
0x688354
0x688494
0x67a170
0x67f0ad
0x67fdf8
0x6811b6
0x66e05e

2. Make a symbol file for the mysqld server:

1049

Debugging a MySQL Server

$> nm -n libexec/mysqld > /tmp/mysqld.sym

If mysqld is not linked statically, use the following command instead:

$> nm -D -n libexec/mysqld > /tmp/mysqld.sym

If you want to decode C++ symbols, use the --demangle, if available, to nm. If your version of nm does
not have this option, you must use the c++filt command after the stack dump has been produced to
demangle the C++ names.

3. Execute the following command:

$> resolve_stack_dump -s /tmp/mysqld.sym -n mysqld.stack

If you were not able to include demangled C++ names in your symbol file, process the
resolve_stack_dump output using c++filt:

$> resolve_stack_dump -s /tmp/mysqld.sym -n mysqld.stack | c++filt

This prints out where mysqld died. If that does not help you find out why mysqld died, you should
create a bug report and include the output from the preceding command with the bug report.

However, in most cases it does not help us to have just a stack trace to find the reason for the problem.
To be able to locate the bug or provide a workaround, in most cases we need to know the statement
that killed mysqld and preferably a test case so that we can repeat the problem! See Section 1.5, “How
to Report Bugs or Problems”.

Newer versions of glibc stack trace functions also print the address as relative to the object. On glibc-
based systems (Linux), the trace for an unexpected exit within a plugin looks something like:

plugin/auth/auth_test_plugin.so(+0x9a6)[0x7ff4d11c29a6]

To translate the relative address (+0x9a6) into a file name and line number, use this command:

$> addr2line -fie auth_test_plugin.so 0x9a6
auth_test_plugin
mysql-trunk/plugin/auth/test_plugin.c:65

The addr2line utility is part of the binutils package on Linux.

On Solaris, the procedure is similar. The Solaris printstack() already prints relative addresses:

plugin/auth/auth_test_plugin.so:0x1510

To translate, use this command:

$> gaddr2line -fie auth_test_plugin.so 0x1510
mysql-trunk/plugin/auth/test_plugin.c:88

Windows already prints the address, function name and line:

000007FEF07E10A4 auth_test_plugin.dll!auth_test_plugin()[test_plugin.c:72]

5.8.1.6 Using Server Logs to Find Causes of Errors in mysqld

Note that before starting mysqld with the general query log enabled, you should check all your tables with
myisamchk. See Chapter 5, MySQL Server Administration.

If mysqld dies or hangs, you should start mysqld with the general query log enabled. See Section 5.4.3,
“The General Query Log”. When mysqld dies again, you can examine the end of the log file for the query
that killed mysqld.

1050

Debugging a MySQL Server

If you use the default general query log file, the log is stored in the database directory as host_name.log
In most cases it is the last query in the log file that killed mysqld, but if possible you should verify this by
restarting mysqld and executing the found query from the mysql command-line tools. If this works, you
should also test all complicated queries that did not complete.

You can also try the command EXPLAIN on all SELECT statements that takes a long time to ensure that
mysqld is using indexes properly. See Section 13.8.2, “EXPLAIN Statement”.

You can find the queries that take a long time to execute by starting mysqld with the slow query log
enabled. See Section 5.4.5, “The Slow Query Log”.

If you find the text mysqld restarted in the error log (normally a file named host_name.err) you
probably have found a query that causes mysqld to fail. If this happens, you should check all your tables
with myisamchk (see Chapter 5, MySQL Server Administration), and test the queries in the MySQL log
files to see whether one fails. If you find such a query, try first upgrading to the newest MySQL version. If
this does not help, report a bug, see Section 1.5, “How to Report Bugs or Problems”.

If you have started mysqld with the myisam_recover_options system variable set, MySQL
automatically checks and tries to repair MyISAM tables if they are marked as 'not closed properly' or
'crashed'. If this happens, MySQL writes an entry in the hostname.err file 'Warning: Checking
table ...' which is followed by Warning: Repairing table if the table needs to be repaired. If you
get a lot of these errors, without mysqld having died unexpectedly just before, then something is wrong
and needs to be investigated further. See Section 5.1.6, “Server Command Options”.

When the server detects MyISAM table corruption, it writes additional information to the error log, such as
the name and line number of the source file, and the list of threads accessing the table. Example: Got an
error from thread_id=1, mi_dynrec.c:368. This is useful information to include in bug reports.

It is not a good sign if mysqld did die unexpectedly, but in this case, you should not investigate the
Checking table... messages, but instead try to find out why mysqld died.

5.8.1.7 Making a Test Case If You Experience Table Corruption

The following procedure applies to MyISAM tables. For information about steps to take when encountering
InnoDB table corruption, see Section 1.5, “How to Report Bugs or Problems”.

If you encounter corrupted MyISAM tables or if mysqld always fails after some update statements, you can
test whether the issue is reproducible by doing the following:

1. Stop the MySQL daemon with mysqladmin shutdown.

2. Make a backup of the tables to guard against the very unlikely case that the repair does something

bad.

3. Check all tables with myisamchk -s database/*.MYI. Repair any corrupted tables with

myisamchk -r database/table.MYI.

4. Make a second backup of the tables.

5. Remove (or move away) any old log files from the MySQL data directory if you need more space.

6. Start mysqld with the binary log enabled. If you want to find a statement that crashes mysqld, you
should start the server with the general query log enabled as well. See Section 5.4.3, “The General
Query Log”, and Section 5.4.4, “The Binary Log”.

7. When you have gotten a crashed table, stop the mysqld server.

8. Restore the backup.

1051

Debugging a MySQL Client

9. Restart the mysqld server without the binary log enabled.

10. Re-execute the statements with mysqlbinlog binary-log-file | mysql. The binary log is

saved in the MySQL database directory with the name hostname-bin.NNNNNN.

11. If the tables are corrupted again or you can get mysqld to die with the above command, you have

found a reproducible bug. FTP the tables and the binary log to our bugs database using the instructions
given in Section 1.5, “How to Report Bugs or Problems”. If you are a support customer, you can use the
MySQL Customer Support Center (https://www.mysql.com/support/) to alert the MySQL team about the
problem and have it fixed as soon as possible.

5.8.2 Debugging a MySQL Client

To be able to debug a MySQL client with the integrated debug package, you should configure MySQL with
-DWITH_DEBUG=1. See Section 2.8.7, “MySQL Source-Configuration Options”.

Before running a client, you should set the MYSQL_DEBUG environment variable:

$> MYSQL_DEBUG=d:t:O,/tmp/client.trace
$> export MYSQL_DEBUG

This causes clients to generate a trace file in /tmp/client.trace.

If you have problems with your own client code, you should attempt to connect to the server and run your
query using a client that is known to work. Do this by running mysql in debugging mode (assuming that
you have compiled MySQL with debugging on):

$> mysql --debug=d:t:O,/tmp/client.trace

This provides useful information in case you mail a bug report. See Section 1.5, “How to Report Bugs or
Problems”.

If your client crashes at some 'legal' looking code, you should check that your mysql.h include file
matches your MySQL library file. A very common mistake is to use an old mysql.h file from an old MySQL
installation with new MySQL library.

5.8.3 The DBUG Package

The MySQL server and most MySQL clients are compiled with the DBUG package originally created by
Fred Fish. When you have configured MySQL for debugging, this package makes it possible to get a trace
file of what the program is doing. See Section 5.8.1.2, “Creating Trace Files”.

This section summarizes the argument values that you can specify in debug options on the command line
for MySQL programs that have been built with debugging support.

The DBUG package can be used by invoking a program with the --debug[=debug_options] or -#
[debug_options] option. If you specify the --debug or -# option without a debug_options value,
most MySQL programs use a default value. The server default is d:t:i:o,/tmp/mysqld.trace on
Unix and d:t:i:O,\mysqld.trace on Windows. The effect of this default is:

• d: Enable output for all debug macros

• t: Trace function calls and exits

• i: Add PID to output lines

• o,/tmp/mysqld.trace, O,\mysqld.trace: Set the debug output file.

1052

The DBUG Package

Most client programs use a default debug_options value of d:t:o,/tmp/program_name.trace,
regardless of platform.

Here are some example debug control strings as they might be specified on a shell command line:

--debug=d:t
--debug=d:f,main,subr1:F:L:t,20
--debug=d,input,output,files:n
--debug=d:t:i:O,\\mysqld.trace

For mysqld, it is also possible to change DBUG settings at runtime by setting the debug system variable.
This variable has global and session values:

mysql> SET GLOBAL debug = 'debug_options';
mysql> SET SESSION debug = 'debug_options';

Changing the global debug value requires privileges sufficient to set global system variables. Changing
the session debug value requires privileges sufficient to set restricted session system variables. See
Section 5.1.8.1, “System Variable Privileges”.

The debug_options value is a sequence of colon-separated fields:

field_1:field_2:...:field_N

Each field within the value consists of a mandatory flag character, optionally preceded by a + or -
character, and optionally followed by a comma-separated list of modifiers:

[+|-]flag[,modifier,modifier,...,modifier]

The following table describes the permitted flag characters. Unrecognized flag characters are silently
ignored.

Flag

d

D

f

F

i

L

Description

Enable output from DBUG_XXX macros for the
current state. May be followed by a list of keywords,
which enables output only for the DBUG macros with
that keyword. An empty list of keywords enables
output for all macros.

In MySQL, common debug macro keywords to
enable are enter, exit, error, warning, info,
and loop.

Delay after each debugger output line. The
argument is the delay, in tenths of seconds,
subject to machine capabilities. For example, D,20
specifies a delay of two seconds.

Limit debugging, tracing, and profiling to the list of
named functions. An empty list enables all functions.
The appropriate d or t flags must still be given; this
flag only limits their actions if they are enabled.

Identify the source file name for each line of debug
or trace output.

Identify the process with the PID or thread ID for
each line of debug or trace output.

Identify the source file line number for each line of
debug or trace output.

1053

The DBUG Package

Flag

Description

n

N

o

O

a

A

p

P

r

t

T

Print the current function nesting depth for each line
of debug or trace output.

Number each line of debug output.

Redirect the debugger output stream to the
specified file. The default output is stderr.

Like o, but the file is really flushed between each
write. When needed, the file is closed and reopened
between each write.

Like o, but opens for append.

Like O, but opens for append.

Limit debugger actions to specified processes. A
process must be identified with the DBUG_PROCESS
macro and match one in the list for debugger
actions to occur.

Print the current process name for each line of
debug or trace output.

When pushing a new state, do not inherit the
previous state's function nesting level. Useful when
the output is to start at the left margin.

Enable function call/exit trace lines. May be followed
by a list (containing only one modifier) giving
a numeric maximum trace level, beyond which
no output occurs for either debugging or tracing
macros. The default is a compile time option.

Print the current timestamp for every line of output.

The leading + or - character and trailing list of modifiers are used for flag characters such as d or f that
can enable a debug operation for all applicable modifiers or just some of them:

• With no leading + or -, the flag value is set to exactly the modifier list as given.

• With a leading + or -, the modifiers in the list are added to or subtracted from the current modifier list.

The following examples show how this works for the d flag. An empty d list enabled output for all debug
macros. A nonempty list enables output only for the macro keywords in the list.

These statements set the d value to the modifier list as given:

mysql> SET debug = 'd';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| d       |
+---------+
mysql> SET debug = 'd,error,warning';
mysql> SELECT @@debug;
+-----------------+
| @@debug         |
+-----------------+
| d,error,warning |
+-----------------+

1054

Tracing mysqld Using DTrace

A leading + or - adds to or subtracts from the current d value:

mysql> SET debug = '+d,loop';
mysql> SELECT @@debug;
+----------------------+
| @@debug              |
+----------------------+
| d,error,warning,loop |
+----------------------+
mysql> SET debug = '-d,error,loop';
mysql> SELECT @@debug;
+-----------+
| @@debug   |
+-----------+
| d,warning |
+-----------+

Adding to “all macros enabled” results in no change:

mysql> SET debug = 'd';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| d       |
+---------+
mysql> SET debug = '+d,loop';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
| d       |
+---------+

Disabling all enabled macros disables the d flag entirely:

mysql> SET debug = 'd,error,loop';
mysql> SELECT @@debug;
+--------------+
| @@debug      |
+--------------+
| d,error,loop |
+--------------+
mysql> SET debug = '-d,error,loop';
mysql> SELECT @@debug;
+---------+
| @@debug |
+---------+
|         |
+---------+

5.8.4 Tracing mysqld Using DTrace

Support for DTrace is deprecated in MySQL 5.7 and is removed in MySQL 8.0.

The DTrace probes in the MySQL server are designed to provide information about the execution of
queries within MySQL and the different areas of the system being utilized during that process. The
organization and triggering of the probes means that the execution of an entire query can be monitored
with one level of probes (query-start and query-done) but by monitoring other probes you can get
successively more detailed information about the execution of the query in terms of the locks used, sort
methods and even row-by-row and storage-engine level execution information.

The DTrace probes are organized so that you can follow the entire query process, from the point of
connection from a client, through the query execution, row-level operations, and back out again. You

1055

Tracing mysqld Using DTrace

can think of the probes as being fired within a specific sequence during a typical client connect/execute/
disconnect sequence, as shown in the following figure.

Figure 5.1 DTrace Probe Sequence

Global information is provided in the arguments to the DTrace probes at various levels. Global information,
that is, the connection ID and user/host and where relevant the query string, is provided at key levels
(connection-start, command-start, query-start, and query-exec-start). As you go deeper
into the probes, it is assumed either you are only interested in the individual executions (row-level probes
provide information on the database and table name only), or that you intend to combine the row-level
probes with the notional parent probes to provide the information about a specific query. Examples of this
are given as the format and arguments of each probe are provided.

MySQL includes support for DTrace probes on these platforms:

• Solaris 10 Update 5 (Solaris 5/08) on SPARC, x86 and x86_64 platforms

• OS X / macOS 10.4 and higher

• Oracle Linux 6 and higher with UEK kernel (as of MySQL 5.7.5)

Enabling the probes should be automatic on these platforms. To explicitly enable or disable the probes
during building, use the -DENABLE_DTRACE=1 or -DENABLE_DTRACE=0 option to CMake.

If a non-Solaris platform includes DTrace support, building mysqld on that platform includes DTrace
support.

Additional Resources

• For more information on DTrace and writing DTrace scripts, read the DTrace User Guide.

• For an introduction to DTrace, see the MySQL Dev Zone article Getting started with DTracing MySQL.

5.8.4.1 mysqld DTrace Probe Reference

MySQL supports the following static probes, organized into groups of functionality.

Table 5.5 MySQL DTrace Probes

Group

Connection

Command

1056

Probes

connection-start, connection-done

command-start, command-done

Group

Query

Query Parsing

Query Cache

Query Execution

Row Level

Row Reads

Index Reads

Lock

Filesort

Statement

Network

Keycache

Tracing mysqld Using DTrace

Probes

query-start, query-done

query-parse-start, query-parse-done

query-cache-hit, query-cache-miss

query-exec-start, query-exec-done

insert-row-start, insert-row-done

update-row-start, update-row-done

delete-row-start, delete-row-done

read-row-start, read-row-done

index-read-row-start, index-read-row-
done

handler-rdlock-start, handler-rdlock-
done

handler-wrlock-start, handler-wrlock-
done

handler-unlock-start, handler-unlock-
done

filesort-start, filesort-done

select-start, select-done

insert-start, insert-done

insert-select-start, insert-select-done

update-start, update-done

multi-update-start, multi-update-done

delete-start, delete-done

multi-delete-start, multi-delete-done

net-read-start, net-read-done, net-
write-start, net-write-done

keycache-read-start, keycache-read-
block, keycache-read-done, keycache-
read-hit, keycache-read-miss, keycache-
write-start, keycache-write-block,
keycache-write-done

Note

When extracting the argument data from the probes, each argument is available as
argN, starting with arg0. To identify each argument within the definitions they are
provided with a descriptive name, but you must access the information using the
corresponding argN parameter.

Connection Probes

The connection-start and connection-done probes enclose a connection from a client, regardless
of whether the connection is through a socket or network connection.

connection-start(connectionid, user, host)

1057

Tracing mysqld Using DTrace

connection-done(status, connectionid)

• connection-start: Triggered after a connection and successful login/authentication have been

completed by a client. The arguments contain the connection information:

• connectionid: An unsigned long containing the connection ID. This is the same as the process

ID shown as the Id value in the output from SHOW PROCESSLIST.

• user: The username used when authenticating. The value is blank for the anonymous user.

• host: The host of the client connection. For a connection made using Unix sockets, the value is blank.

• connection-done: Triggered just as the connection to the client has been closed. The arguments are:

• status: The status of the connection when it was closed. A logout operation has a value of 0; any

other termination of the connection has a nonzero value.

• connectionid: The connection ID of the connection that was closed.

The following D script quantifies and summarizes the average duration of individual connections, and
provides a count, dumping the information every 60 seconds:

#!/usr/sbin/dtrace -s

mysql*:::connection-start
{
  self->start = timestamp;
}

mysql*:::connection-done
/self->start/
{
  @ = quantize(((timestamp - self->start)/1000000));
  self->start = 0;
}

tick-60s
{
  printa(@);
}

When executed on a server with a large number of clients you might see output similar to this:

  1  57413                        :tick-60s

           value  ------------- Distribution ------------- count
              -1 |                                         0
               0 |@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 30011
               1 |                                         59
               2 |                                         5
               4 |                                         20
               8 |                                         29
              16 |                                         18
              32 |                                         27
              64 |                                         30
             128 |                                         11
             256 |                                         10
             512 |                                         1
            1024 |                                         6
            2048 |                                         8
            4096 |                                         9
            8192 |                                         8
           16384 |                                         2

1058

Tracing mysqld Using DTrace

           32768 |                                         1
           65536 |                                         1
          131072 |                                         0
          262144 |                                         1
          524288 |                                         0

Command Probes

The command probes are executed before and after a client command is executed, including any
SQL statement that might be executed during that period. Commands include operations such as the
initialization of the DB, use of the COM_CHANGE_USER operation (supported by the MySQL protocol), and
manipulation of prepared statements. Many of these commands are used only by the MySQL client API
from various connectors such as PHP and Java.

command-start(connectionid, command, user, host)
command-done(status)

• command-start: Triggered when a command is submitted to the server.

• connectionid: The connection ID of the client executing the command.

• command: An integer representing the command that was executed. Possible values are shown in the

following table.

Value

00

01

02

03

04

05

06

07

08

09

10

11

12

13

14

15

16

17

18

19

Name

COM_SLEEP

COM_QUIT

COM_INIT_DB

COM_QUERY

COM_FIELD_LIST

Description

Internal thread state

Close connection

Select database (USE ...)

Execute a query

Get a list of fields

COM_CREATE_DB

Create a database (deprecated)

COM_DROP_DB

COM_REFRESH

COM_SHUTDOWN

COM_STATISTICS

COM_PROCESS_INFO

COM_CONNECT

Drop a database (deprecated)

Refresh connection

Shutdown server

Get statistics

Get processes (SHOW
PROCESSLIST)

Initialize connection

COM_PROCESS_KILL

Kill process

COM_DEBUG

COM_PING

COM_TIME

Get debug information

Ping

Internal thread state

COM_DELAYED_INSERT

Internal thread state

COM_CHANGE_USER

Change user

COM_BINLOG_DUMP

COM_TABLE_DUMP

Used by a replica or
mysqlbinlog to initiate a
binary log read

Used by a replica to get the
source table information

1059

Tracing mysqld Using DTrace

Value

Name

Description

20

21

22

23

24

25

26

27

28

COM_CONNECT_OUT

COM_REGISTER_SLAVE

Used by a replica to log a
connection to the server

Used by a replica during
registration

COM_STMT_PREPARE

Prepare a statement

COM_STMT_EXECUTE

Execute a statement

COM_STMT_SEND_LONG_DATAUsed by a client when

requesting extended data

COM_STMT_CLOSE

Close a prepared statement

COM_STMT_RESET

Reset a prepared statement

COM_SET_OPTION

Set a server option

COM_STMT_FETCH

Fetch a prepared statement

• user: The user executing the command.

• host: The client host.

• command-done: Triggered when the command execution completes. The status argument contains 0
if the command executed successfully, or 1 if the statement was terminated before normal completion.

The command-start and command-done probes are best used when combined with the statement
probes to get an idea of overall execution time.

Query Probes

The query-start and query-done probes are triggered when a specific query is received by the server
and when the query has been completed and the information has been successfully sent to the client.

query-start(query, connectionid, database, user, host)
query-done(status)

• query-start: Triggered after the query string has been received from the client. The arguments are:

• query: The full text of the submitted query.

• connectionid: The connection ID of the client that submitted the query. The connection ID equals
the connection ID returned when the client first connects and the Id value in the output from SHOW
PROCESSLIST.

• database: The database name on which the query is being executed.

• user: The username used to connect to the server.

• host: The hostname of the client.

• query-done: Triggered once the query has been executed and the information has been returned
to the client. The probe includes a single argument, status, which returns 0 when the query is
successfully executed and 1 if there was an error.

You can get a simple report of the execution time for each query using the following D script:

#!/usr/sbin/dtrace -s

1060

Tracing mysqld Using DTrace

#pragma D option quiet

dtrace:::BEGIN
{
   printf("%-20s %-20s %-40s %-9s\n", "Who", "Database", "Query", "Time(ms)");
}

mysql*:::query-start
{
   self->query = copyinstr(arg0);
   self->connid = arg1;
   self->db    = copyinstr(arg2);
   self->who   = strjoin(copyinstr(arg3),strjoin("@",copyinstr(arg4)));
   self->querystart = timestamp;
}

mysql*:::query-done
{
   printf("%-20s %-20s %-40s %-9d\n",self->who,self->db,self->query,
          (timestamp - self->querystart) / 1000000);
}

When executing the above script you should get a basic idea of the execution time of your queries:

$> ./query.d
Who                  Database             Query                                    Time(ms)
root@localhost       test                 select * from t1 order by i limit 10     0
root@localhost       test                 set global query_cache_size=0            0
root@localhost       test                 select * from t1 order by i limit 10     776
root@localhost       test                 select * from t1 order by i limit 10     773
root@localhost       test                 select * from t1 order by i desc limit 10 795

Query Parsing Probes

The query parsing probes are triggered before the original SQL statement is parsed and when the parsing
of the statement and determination of the execution model required to process the statement has been
completed:

query-parse-start(query)
query-parse-done(status)

• query-parse-start: Triggered just before the statement is parsed by the MySQL query parser. The

single argument, query, is a string containing the full text of the original query.

• query-parse-done: Triggered when the parsing of the original statement has been completed.
The status is an integer describing the status of the operation. A 0 indicates that the query was
successfully parsed. A 1 indicates that the parsing of the query failed.

For example, you could monitor the execution time for parsing a given query using the following D script:

#!/usr/sbin/dtrace -s

#pragma D option quiet

mysql*:::query-parse-start
{
   self->parsestart = timestamp;
   self->parsequery = copyinstr(arg0);
}

mysql*:::query-parse-done
/arg0 == 0/
{
   printf("Parsing %s: %d microseconds\n", self->parsequery,((timestamp - self->parsestart)/1000));

1061

Tracing mysqld Using DTrace

}

mysql*:::query-parse-done
/arg0 != 0/
{
   printf("Error parsing %s: %d microseconds\n", self->parsequery,((timestamp - self->parsestart)/1000));
}

In the above script a predicate is used on query-parse-done so that different output is generated based
on the status value of the probe.

When running the script and monitoring the execution:

$> ./query-parsing.d
Error parsing select from t1 join (t2) on (t1.i = t2.i) order by t1.s,t1.i limit 10: 36 ms
Parsing select * from t1 join (t2) on (t1.i = t2.i) order by t1.s,t1.i limit 10: 176 ms

Query Cache Probes

The query cache probes are fired when executing any query. The query-cache-hit query is triggered
when a query exists in the query cache and can be used to return the query cache information. The
arguments contain the original query text and the number of rows returned from the query cache for the
query. If the query is not within the query cache, or the query cache is not enabled, then the query-
cache-miss probe is triggered instead.

query-cache-hit(query, rows)
query-cache-miss(query)

• query-cache-hit: Triggered when the query has been found within the query cache. The first

argument, query, contains the original text of the query. The second argument, rows, is an integer
containing the number of rows in the cached query.

• query-cache-miss: Triggered when the query is not found within the query cache. The first argument,

query, contains the original text of the query.

The query cache probes are best combined with a probe on the main query so that you can determine the
differences in times between using or not using the query cache for specified queries. For example, in the
following D script, the query and query cache information are combined into the information output during
monitoring:

#!/usr/sbin/dtrace -s

#pragma D option quiet

dtrace:::BEGIN
{
   printf("%-20s %-20s %-40s %2s %-9s\n", "Who", "Database", "Query", "QC", "Time(ms)");
}

mysql*:::query-start
{
   self->query = copyinstr(arg0);
   self->connid = arg1;
   self->db    = copyinstr(arg2);
   self->who   = strjoin(copyinstr(arg3),strjoin("@",copyinstr(arg4)));
   self->querystart = timestamp;
   self->qc = 0;
}

mysql*:::query-cache-hit
{
   self->qc = 1;
}

1062

Tracing mysqld Using DTrace

mysql*:::query-cache-miss
{
   self->qc = 0;
}

mysql*:::query-done
{
   printf("%-20s %-20s %-40s %-2s %-9d\n",self->who,self->db,self->query,(self->qc ? "Y" : "N"),
          (timestamp - self->querystart) / 1000000);
}

When executing the script you can see the effects of the query cache. Initially the query cache is disabled.
If you set the query cache size and then execute the query multiple times you should see that the query
cache is being used to return the query data:

$> ./query-cache.d
root@localhost       test                 select * from t1 order by i limit 10     N  1072
root@localhost                            set global query_cache_size=262144       N  0
root@localhost       test                 select * from t1 order by i limit 10     N  781
root@localhost       test                 select * from t1 order by i limit 10     Y  0

Query Execution Probes

The query execution probe is triggered when the actual execution of the query starts, after the parsing and
checking the query cache but before any privilege checks or optimization. By comparing the difference
between the start and done probes you can monitor the time actually spent servicing the query (instead of
just handling the parsing and other elements of the query).

query-exec-start(query, connectionid, database, user, host, exec_type)
query-exec-done(status)

Note

The information provided in the arguments for query-start and query-exec-
start are almost identical and designed so that you can choose to monitor
either the entire query process (using query-start) or only the execution (using
query-exec-start) while exposing the core information about the user, client,
and query being executed.

• query-exec-start: Triggered when the execution of a individual query is started. The arguments are:

• query: The full text of the submitted query.

• connectionid: The connection ID of the client that submitted the query. The connection ID equals
the connection ID returned when the client first connects and the Id value in the output from SHOW
PROCESSLIST.

• database: The database name on which the query is being executed.

• user: The username used to connect to the server.

• host: The hostname of the client.

• exec_type: The type of execution. Execution types are determined based on the contents of the

query and where it was submitted. The values for each type are shown in the following table.

Value

0

Description

Executed query from sql_parse, top-level query.

1063

Tracing mysqld Using DTrace

Value

1

2

3

Description

Executed prepared statement

Executed cursor statement

Executed query in stored procedure

• query-exec-done: Triggered when the execution of the query has completed. The probe includes a

single argument, status, which returns 0 when the query is successfully executed and 1 if there was an
error.

Row-Level Probes

The *row-{start,done} probes are triggered each time a row operation is pushed down to a storage
engine. For example, if you execute an INSERT statement with 100 rows of data, then the insert-row-
start and insert-row-done probes are triggered 100 times each, for each row insert.

insert-row-start(database, table)
insert-row-done(status)

update-row-start(database, table)
update-row-done(status)

delete-row-start(database, table)
delete-row-done(status)

• insert-row-start: Triggered before a row is inserted into a table.

• insert-row-done: Triggered after a row is inserted into a table.

• update-row-start: Triggered before a row is updated in a table.

• update-row-done: Triggered before a row is updated in a table.

• delete-row-start: Triggered before a row is deleted from a table.

• delete-row-done: Triggered before a row is deleted from a table.

The arguments supported by the probes are consistent for the corresponding start and done probes in
each case:

• database: The database name.

• table: The table name.

• status: The status; 0 for success or 1 for failure.

Because the row-level probes are triggered for each individual row access, these probes can be triggered
many thousands of times each second, which may have a detrimental effect on both the monitoring
script and MySQL. The DTrace environment should limit the triggering on these probes to prevent the
performance being adversely affected. Either use the probes sparingly, or use counter or aggregation
functions to report on these probes and then provide a summary when the script terminates or as part of a
query-done or query-exec-done probes.

The following example script summarizes the duration of each row operation within a larger query:

#!/usr/sbin/dtrace -s

#pragma D option quiet

1064

Tracing mysqld Using DTrace

dtrace:::BEGIN
{
   printf("%-2s %-10s %-10s %9s %9s %-s \n",
          "St", "Who", "DB", "ConnID", "Dur ms", "Query");
}

mysql*:::query-start
{
   self->query = copyinstr(arg0);
   self->who   = strjoin(copyinstr(arg3),strjoin("@",copyinstr(arg4)));
   self->db    = copyinstr(arg2);
   self->connid = arg1;
   self->querystart = timestamp;
   self->rowdur = 0;
}

mysql*:::query-done
{
   this->elapsed = (timestamp - self->querystart) /1000000;
   printf("%2d %-10s %-10s %9d %9d %s\n",
          arg0, self->who, self->db,
          self->connid, this->elapsed, self->query);
}

mysql*:::query-done
/ self->rowdur /
{
   printf("%34s %9d %s\n", "", (self->rowdur/1000000), "-> Row ops");
}

mysql*:::insert-row-start
{
   self->rowstart = timestamp;
}

mysql*:::delete-row-start
{
   self->rowstart = timestamp;
}

mysql*:::update-row-start
{
   self->rowstart = timestamp;
}

mysql*:::insert-row-done
{
   self->rowdur += (timestamp-self->rowstart);
}

mysql*:::delete-row-done
{
   self->rowdur += (timestamp-self->rowstart);
}

mysql*:::update-row-done
{
   self->rowdur += (timestamp-self->rowstart);
}

Running the above script with a query that inserts data into a table, you can monitor the exact time spent
performing the raw row insertion:

St Who        DB            ConnID    Dur ms Query
 0 @localhost test              13     20767 insert into t1(select * from t2)
                                        4827 -> Row ops

1065

Tracing mysqld Using DTrace

Read Row Probes

The read row probes are triggered at a storage engine level each time a row read operation occurs. These
probes are specified within each storage engine (as opposed to the *row-start probes which are in the
storage engine interface). These probes can therefore be used to monitor individual storage engine row-
level operations and performance. Because these probes are triggered around the storage engine row
read interface, they may be hit a significant number of times during a basic query.

read-row-start(database, table, scan_flag)
read-row-done(status)

• read-row-start: Triggered when a row is read by the storage engine from the specified database

and table. The scan_flag is set to 1 (true) when the read is part of a table scan (that is, a sequential
read), or 0 (false) when the read is of a specific record.

• read-row-done: Triggered when a row read operation within a storage engine completes. The status

returns 0 on success, or a positive value on failure.

Index Probes

The index probes are triggered each time a row is read using one of the indexes for the specified table.
The probe is triggered within the corresponding storage engine for the table.

index-read-row-start(database, table)
index-read-row-done(status)

• index-read-row-start: Triggered when a row is read by the storage engine from the specified

database and table.

• index-read-row-done: Triggered when an indexed row read operation within a storage engine

completes. The status returns 0 on success, or a positive value on failure.

Lock Probes

The lock probes are called whenever an external lock is requested by MySQL for a table using the
corresponding lock mechanism on the table as defined by the table's engine type. There are three different
types of lock, the read lock, write lock, and unlock operations. Using the probes you can determine the
duration of the external locking routine (that is, the time taken by the storage engine to implement the
lock, including any time waiting for another lock to become free) and the total duration of the lock/unlock
process.

handler-rdlock-start(database, table)
handler-rdlock-done(status)

handler-wrlock-start(database, table)
handler-wrlock-done(status)

handler-unlock-start(database, table)
handler-unlock-done(status)

• handler-rdlock-start: Triggered when a read lock is requested on the specified database and

table.

• handler-wrlock-start: Triggered when a write lock is requested on the specified database and

table.

• handler-unlock-start: Triggered when an unlock request is made on the specified database and

table.

1066

Tracing mysqld Using DTrace

• handler-rdlock-done: Triggered when a read lock request completes. The status is 0 if the lock

operation succeeded, or >0 on failure.

• handler-wrlock-done: Triggered when a write lock request completes. The status is 0 if the lock

operation succeeded, or >0 on failure.

• handler-unlock-done: Triggered when an unlock request completes. The status is 0 if the unlock

operation succeeded, or >0 on failure.

You can use arrays to monitor the locking and unlocking of individual tables and then calculate the duration
of the entire table lock using the following script:

#!/usr/sbin/dtrace -s

#pragma D option quiet

mysql*:::handler-rdlock-start
{
   self->rdlockstart = timestamp;
   this->lockref = strjoin(copyinstr(arg0),strjoin("@",copyinstr(arg1)));
   self->lockmap[this->lockref] = self->rdlockstart;
   printf("Start: Lock->Read   %s.%s\n",copyinstr(arg0),copyinstr(arg1));
}

mysql*:::handler-wrlock-start
{
   self->wrlockstart = timestamp;
   this->lockref = strjoin(copyinstr(arg0),strjoin("@",copyinstr(arg1)));
   self->lockmap[this->lockref] = self->rdlockstart;
   printf("Start: Lock->Write  %s.%s\n",copyinstr(arg0),copyinstr(arg1));
}

mysql*:::handler-unlock-start
{
   self->unlockstart = timestamp;
   this->lockref = strjoin(copyinstr(arg0),strjoin("@",copyinstr(arg1)));
   printf("Start: Lock->Unlock %s.%s (%d ms lock duration)\n",
          copyinstr(arg0),copyinstr(arg1),
          (timestamp - self->lockmap[this->lockref])/1000000);
}

mysql*:::handler-rdlock-done
{
   printf("End:   Lock->Read   %d ms\n",
          (timestamp - self->rdlockstart)/1000000);
}

mysql*:::handler-wrlock-done
{
   printf("End:   Lock->Write  %d ms\n",
          (timestamp - self->wrlockstart)/1000000);
}

mysql*:::handler-unlock-done
{
   printf("End:   Lock->Unlock %d ms\n",
          (timestamp - self->unlockstart)/1000000);
}

When executed, you should get information both about the duration of the locking process itself, and of the
locks on a specific table:

Start: Lock->Read   test.t2
End:   Lock->Read   0 ms
Start: Lock->Unlock test.t2 (25743 ms lock duration)

1067

Tracing mysqld Using DTrace

End:   Lock->Unlock 0 ms
Start: Lock->Read   test.t2
End:   Lock->Read   0 ms
Start: Lock->Unlock test.t2 (1 ms lock duration)
End:   Lock->Unlock 0 ms
Start: Lock->Read   test.t2
End:   Lock->Read   0 ms
Start: Lock->Unlock test.t2 (1 ms lock duration)
End:   Lock->Unlock 0 ms
Start: Lock->Read   test.t2
End:   Lock->Read   0 ms

Filesort Probes

The filesort probes are triggered whenever a filesort operation is applied to a table. For more information
on filesort and the conditions under which it occurs, see Section 8.2.1.14, “ORDER BY Optimization”.

filesort-start(database, table)
filesort-done(status, rows)

• filesort-start: Triggered when the filesort operation starts on a table. The two arguments to the

probe, database and table, identify the table being sorted.

• filesort-done: Triggered when the filesort operation completes. Two arguments are supplied, the

status (0 for success, 1 for failure), and the number of rows sorted during the filesort process.

An example of this is in the following script, which tracks the duration of the filesort process in addition to
the duration of the main query:

#!/usr/sbin/dtrace -s

#pragma D option quiet

dtrace:::BEGIN
{
   printf("%-2s %-10s %-10s %9s %18s %-s \n",
          "St", "Who", "DB", "ConnID", "Dur microsec", "Query");
}

mysql*:::query-start
{
   self->query = copyinstr(arg0);
   self->who   = strjoin(copyinstr(arg3),strjoin("@",copyinstr(arg4)));
   self->db    = copyinstr(arg2);
   self->connid = arg1;
   self->querystart = timestamp;
   self->filesort = 0;
   self->fsdb = "";
   self->fstable = "";
}

mysql*:::filesort-start
{
  self->filesort = timestamp;
  self->fsdb = copyinstr(arg0);
  self->fstable = copyinstr(arg1);
}

mysql*:::filesort-done
{
   this->elapsed = (timestamp - self->filesort) /1000;
   printf("%2d %-10s %-10s %9d %18d Filesort on %s\n",
          arg0, self->who, self->fsdb,
          self->connid, this->elapsed, self->fstable);
}

1068

Tracing mysqld Using DTrace

mysql*:::query-done
{
   this->elapsed = (timestamp - self->querystart) /1000;
   printf("%2d %-10s %-10s %9d %18d %s\n",
          arg0, self->who, self->db,
          self->connid, this->elapsed, self->query);
}

Executing a query on a large table with an ORDER BY clause that triggers a filesort, and then creating an
index on the table and then repeating the same query, you can see the difference in execution speed:

St Who        DB            ConnID       Dur microsec Query
 0 @localhost test              14           11335469 Filesort on t1
 0 @localhost test              14           11335787 select * from t1 order by i limit 100
 0 @localhost test              14          466734378 create index t1a on t1 (i)
 0 @localhost test              14              26472 select * from t1 order by i limit 100

Statement Probes

The individual statement probes are provided to give specific information about different statement types.
For the start probes the string of the query is provided as the only argument. Depending on the statement
type, the information provided by the corresponding done probe can differ. For all done probes the status
of the operation (0 for success, >0 for failure) is provided. For SELECT, INSERT, INSERT ... (SELECT
FROM ...), DELETE, and DELETE FROM t1,t2 operations the number of rows affected is returned.

For UPDATE and UPDATE t1,t2 ... statements the number of rows matched and the number of rows
actually changed is provided. This is because the number of rows actually matched by the corresponding
WHERE clause, and the number of rows changed can differ. MySQL does not update the value of a row if
the value already matches the new setting.

select-start(query)
select-done(status,rows)

insert-start(query)
insert-done(status,rows)

insert-select-start(query)
insert-select-done(status,rows)

update-start(query)
update-done(status,rowsmatched,rowschanged)

multi-update-start(query)
multi-update-done(status,rowsmatched,rowschanged)

delete-start(query)
delete-done(status,rows)

multi-delete-start(query)
multi-delete-done(status,rows)

• select-start: Triggered before a SELECT statement.

• select-done: Triggered at the end of a SELECT statement.

• insert-start: Triggered before a INSERT statement.

• insert-done: Triggered at the end of an INSERT statement.

• insert-select-start: Triggered before an INSERT ... SELECT statement.

• insert-select-done: Triggered at the end of an INSERT ... SELECT statement.

1069

Tracing mysqld Using DTrace

• update-start: Triggered before an UPDATE statement.

• update-done: Triggered at the end of an UPDATE statement.

• multi-update-start: Triggered before an UPDATE statement involving multiple tables.

• multi-update-done: Triggered at the end of an UPDATE statement involving multiple tables.

• delete-start: Triggered before a DELETE statement.

• delete-done: Triggered at the end of a DELETE statement.

• multi-delete-start: Triggered before a DELETE statement involving multiple tables.

• multi-delete-done: Triggered at the end of a DELETE statement involving multiple tables.

The arguments for the statement probes are:

• query: The query string.

• status: The status of the query. 0 for success, and >0 for failure.

• rows: The number of rows affected by the statement. This returns the number rows found for SELECT,
the number of rows deleted for DELETE, and the number of rows successfully inserted for INSERT.

• rowsmatched: The number of rows matched by the WHERE clause of an UPDATE operation.

• rowschanged: The number of rows actually changed during an UPDATE operation.

You use these probes to monitor the execution of these statement types without having to monitor the user
or client executing the statements. A simple example of this is to track the execution times:

#!/usr/sbin/dtrace -s

#pragma D option quiet

dtrace:::BEGIN
{
   printf("%-60s %-8s %-8s %-8s\n", "Query", "RowsU", "RowsM", "Dur (ms)");
}

mysql*:::update-start, mysql*:::insert-start,
mysql*:::delete-start, mysql*:::multi-delete-start,
mysql*:::multi-delete-done, mysql*:::select-start,
mysql*:::insert-select-start, mysql*:::multi-update-start
{
    self->query = copyinstr(arg0);
    self->querystart = timestamp;
}

mysql*:::insert-done, mysql*:::select-done,
mysql*:::delete-done, mysql*:::multi-delete-done, mysql*:::insert-select-done
/ self->querystart /
{
    this->elapsed = ((timestamp - self->querystart)/1000000);
    printf("%-60s %-8d %-8d %d\n",
           self->query,
           0,
           arg1,
           this->elapsed);
    self->querystart = 0;
}

1070

Tracing mysqld Using DTrace

mysql*:::update-done, mysql*:::multi-update-done
/ self->querystart /
{
    this->elapsed = ((timestamp - self->querystart)/1000000);
    printf("%-60s %-8d %-8d %d\n",
           self->query,
           arg1,
           arg2,
           this->elapsed);
    self->querystart = 0;
}

When executed you can see the basic execution times and rows matches:

Query                                                        RowsU    RowsM    Dur (ms)
select * from t2                                             0        275      0
insert into t2 (select * from t2)                            0        275      9
update t2 set i=5 where i > 75                               110      110      8
update t2 set i=5 where i < 25                               254      134      12
delete from t2 where i < 5                                   0        0        0

Another alternative is to use the aggregation functions in DTrace to aggregate the execution time of
individual statements together:

#!/usr/sbin/dtrace -s

#pragma D option quiet

mysql*:::update-start, mysql*:::insert-start,
mysql*:::delete-start, mysql*:::multi-delete-start,
mysql*:::multi-delete-done, mysql*:::select-start,
mysql*:::insert-select-start, mysql*:::multi-update-start
{
    self->querystart = timestamp;
}

mysql*:::select-done
{
        @statements["select"] = sum(((timestamp - self->querystart)/1000000));
}

mysql*:::insert-done, mysql*:::insert-select-done
{
        @statements["insert"] = sum(((timestamp - self->querystart)/1000000));
}

mysql*:::update-done, mysql*:::multi-update-done
{
        @statements["update"] = sum(((timestamp - self->querystart)/1000000));
}

mysql*:::delete-done, mysql*:::multi-delete-done
{
        @statements["delete"] = sum(((timestamp - self->querystart)/1000000));
}

tick-30s
{
        printa(@statements);
}

The script just shown aggregates the times spent doing each operation, which could be used to help
benchmark a standard suite of tests.

 delete                                                            0

1071

Tracing mysqld Using DTrace

  update                                                            0
  insert                                                           23
  select                                                         2484

  delete                                                            0
  update                                                            0
  insert                                                           39
  select                                                        10744

  delete                                                            0
  update                                                           26
  insert                                                           56
  select                                                        10944

  delete                                                            0
  update                                                           26
  insert                                                         2287
  select                                                        15985

Network Probes

The network probes monitor the transfer of information from the MySQL server and clients of all types over
the network. The probes are defined as follows:

net-read-start()
net-read-done(status, bytes)
net-write-start(bytes)
net-write-done(status)

• net-read-start: Triggered when a network read operation is started.

• net-read-done: Triggered when the network read operation completes. The status is an integer
representing the return status for the operation, 0 for success and 1 for failure. The bytes argument is
an integer specifying the number of bytes read during the process.

• net-start-bytes: Triggered when data is written to a network socket. The single argument, bytes,

specifies the number of bytes written to the network socket.

• net-write-done: Triggered when the network write operation has completed. The single argument,
status, is an integer representing the return status for the operation, 0 for success and 1 for failure.

You can use the network probes to monitor the time spent reading from and writing to network clients
during execution. The following D script provides an example of this. Both the cumulative time for the read
or write is calculated, and the number of bytes. Note that the dynamic variable size has been increased
(using the dynvarsize option) to cope with the rapid firing of the individual probes for the network reads/
writes.

#!/usr/sbin/dtrace -s

#pragma D option quiet
#pragma D option dynvarsize=4m

dtrace:::BEGIN
{
   printf("%-2s %-30s %-10s %9s %18s %-s \n",
          "St", "Who", "DB", "ConnID", "Dur microsec", "Query");
}

mysql*:::query-start
{
   self->query = copyinstr(arg0);
   self->who   = strjoin(copyinstr(arg3),strjoin("@",copyinstr(arg4)));
   self->db    = copyinstr(arg2);

1072

Tracing mysqld Using DTrace

   self->connid = arg1;
   self->querystart = timestamp;
   self->netwrite = 0;
   self->netwritecum = 0;
   self->netwritebase = 0;
   self->netread = 0;
   self->netreadcum = 0;
   self->netreadbase = 0;
}

mysql*:::net-write-start
{
   self->netwrite += arg0;
   self->netwritebase = timestamp;
}

mysql*:::net-write-done
{
   self->netwritecum += (timestamp - self->netwritebase);
   self->netwritebase = 0;
}

mysql*:::net-read-start
{
   self->netreadbase = timestamp;
}

mysql*:::net-read-done
{
   self->netread += arg1;
   self->netreadcum += (timestamp - self->netreadbase);
   self->netreadbase = 0;
}

mysql*:::query-done
{
   this->elapsed = (timestamp - self->querystart) /1000000;
   printf("%2d %-30s %-10s %9d %18d %s\n",
          arg0, self->who, self->db,
          self->connid, this->elapsed, self->query);
   printf("Net read: %d bytes (%d ms) write: %d bytes (%d ms)\n",
               self->netread, (self->netreadcum/1000000),
               self->netwrite, (self->netwritecum/1000000));
}

When executing the above script on a machine with a remote client, you can see that approximately a third
of the time spent executing the query is related to writing the query results back to the client.

St Who                            DB            ConnID       Dur microsec Query
 0 root@::ffff:198.51.100.108      test              31               3495 select * from t1 limit 1000000
Net read: 0 bytes (0 ms) write: 10000075 bytes (1220 ms)

Keycache Probes

The keycache probes are triggered when using the index key cache used with the MyISAM storage engine.
Probes exist to monitor when data is read into the keycache, cached key data is written from the cache into
a cached file, or when accessing the keycache.

Keycache usage indicates when data is read or written from the index files into the cache, and can be
used to monitor how efficient the memory allocated to the keycache is being used. A high number of
keycache reads across a range of queries may indicate that the keycache is too small for size of data
being accessed.

keycache-read-start(filepath, bytes, mem_used, mem_free)
keycache-read-block(bytes)

1073

Tracing mysqld Using DTrace

keycache-read-hit()
keycache-read-miss()
keycache-read-done(mem_used, mem_free)
keycache-write-start(filepath, bytes, mem_used, mem_free)
keycache-write-block(bytes)
keycache-write-done(mem_used, mem_free)

When reading data from the index files into the keycache, the process first initializes the read operation
(indicated by keycache-read-start), then loads blocks of data (keycache-read-block), and then
the read block is either matches the data being identified (keycache-read-hit) or more data needs
to be read (keycache-read-miss). Once the read operation has completed, reading stops with the
keycache-read-done.

Data can be read from the index file into the keycache only when the specified key is not already within the
keycache.

• keycache-read-start: Triggered when the keycache read operation is started. Data is read from the
specified filepath, reading the specified number of bytes. The mem_used and mem_avail indicate
memory currently used by the keycache and the amount of memory available within the keycache.

• keycache-read-block: Triggered when the keycache reads a block of data, of the specified number

of bytes, from the index file into the keycache.

• keycache-read-hit: Triggered when the block of data read from the index file matches the key data

requested.

• keycache-read-miss: Triggered when the block of data read from the index file does not match the

key data needed.

• keycache-read-done: Triggered when the keycache read operation has completed. The mem_used
and mem_avail indicate memory currently used by the keycache and the amount of memory available
within the keycache.

Keycache writes occur when the index information is updated during an INSERT, UPDATE, or DELETE
operation, and the cached key information is flushed back to the index file.

• keycache-write-start: Triggered when the keycache write operation is started. Data is written

to the specified filepath, reading the specified number of bytes. The mem_used and mem_avail
indicate memory currently used by the keycache and the amount of memory available within the
keycache.

• keycache-write-block: Triggered when the keycache writes a block of data, of the specified number

of bytes, to the index file from the keycache.

• keycache-write-done: Triggered when the keycache write operation has completed. The mem_used
and mem_avail indicate memory currently used by the keycache and the amount of memory available
within the keycache.

1074

