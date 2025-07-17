# 技术分享 | MHA-MasterFailover 分析

**原文链接**: https://opensource.actionsky.com/20210508-mha/
**分类**: 技术干货
**发布时间**: 2021-05-08T00:58:11-08:00

---

作者：王向爱可生 DBA 团队成员，负责公司 DMP 产品的运维和客户 MySQL 问题的处理。擅长数据库故障处理。对数据库技术和 python 有着浓厚的兴趣。本文来源：原创投稿* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 前言
MHA 出来将近 10 年的时间，作为一个开源产品，能活这么久，还有这么多人追捧。基本上可以说是一种 mysql 中的标准解决方案。
不过 MHA 已经不适合这个时代了。。。但是这不影响我们对他进行一波研究。
## 发生 master crash 源码分析
下面的内容比较淦，没有兴趣的同学直接跳到：总结。
关于源码可以直接去 github.com 然后搜 MHA。
`
sub main {
 .....
 eval { $error_code = do_master_failover(); };
   if ($@) {
  $error_code = 1;
   }
   if ($error_code) {
  finalize_on_error();
   }
   return $error_code;
 ....
 
sub do_master_failover {
  my $error_code = 1;  #错误码
  my ( $dead_master, $new_master );
  # $dead_master 去世的master
  # $new_master  新生的master
  eval {
    # 第一步： 检查配置
    my ( $servers_config_ref, $binlog_server_ref ) = init_config();
    $log->info("Starting master failover.");
    $log->info();
    $log->info("* Phase 1: Configuration Check Phase..\n");
    $log->info();
    # 初始化 Binlog server
    MHA::ServerManager::init_binlog_server( $binlog_server_ref, $log );
        # ssh_check_simple 检查SSH的连通性
        # get_node_version 获取node的版本号
        #    实际使用命令拿到版本号 apply_diff_relay_logs --version
            # 拿到版本号 Binlog server可达，否则不可达
    $dead_master = check_settings($servers_config_ref);
          # MHA::ManagerUtil::check_node_version($log); # 检查mha的版本信息
                                              # 结果1：没有安装mha
                                              # 结果2： $node_version < $MHA::ManagerConst::NODE_MIN_VERSION
                                              # our $NODE_MIN_VERSION = '0.54';
                                              # 节点版本号必须等于或者高于0.54
          # $_server_manager->connect_all_and_read_server_status(); # 检查各实例是否可以连接
          # my @dead_servers  = $_server_manager->get_dead_servers();
    # my @alive_servers = $_server_manager->get_alive_servers();
    # my @alive_slaves  = $_server_manager->get_alive_slaves();
          # get_dead_servers/get_alive_servers/get_alive_slaves：double check各个node的死活状态
          # g$_server_manager->start_sql_threads_if(); 查看Slave_SQL_Running是否为Yes，若不是则启动SQL thread
    if ( $_server_manager->is_gtid_auto_pos_enabled() ) {
      $log->info("Starting GTID based failover.");
    }
    else {
      $_server_manager->force_disable_log_bin_if_auto_pos_disabled();
      $log->info("Starting Non-GTID based failover.");
    }
    $log->info();
    $log->info("** Phase 1: Configuration Check Phase completed.\n");
    $log->info();
    # 第二步：关闭当前失败的IO复制线程，并执行脚本切换VIP
    $log->info("* Phase 2: Dead Master Shutdown Phase..\n");
    $log->info();
    force_shutdown($dead_master);
    # 判断ssh是否可达
        # MHA::HealthCheck::ssh_check_simple()
        # MHA::ManagerUtil::get_node_version()
    # my $rc = $target->stop_io_thread(); 停止所有slave复制IO线程
    # force_shutdown_internal()  执行配置文件中的master_ip_failover_script/shutdown_script，如果没有就不执行
        # master_ip_failover_script：如果设置了VIP，则首先切换VIP
        # shutdown_script：如果设置了shutdown脚本，则执行shutdown脚本
    $log->info("* Phase 2: Dead Master Shutdown Phase completed.\n");
    $log->info();
    # 第三步 新主恢复
    $log->info("* Phase 3: Master Recovery Phase..\n");
    $log->info();
    # 获取新的主从信息
    $log->info("* Phase 3.1: Getting Latest Slaves Phase..\n");
    $log->info();
    check_set_latest_slaves();
          # $_server_manager->read_slave_status(); 获取各个slave的binlog file和position点
            # my %status = $target->check_slave_status(); 执行show slave status来获取从库信息
                         Slave_IO_State,
                         Master_Host,
                         Master_Port,
                         Master_User,
                         Slave_IO_Running,
                         Slave_SQL_Running,
                         Master_Log_File,
                         Read_Master_Log_Pos,
                         Relay_Master_Log_File,
                         Last_Errno,
                         Last_Error,
                         Exec_Master_Log_Pos,
                         Relay_Log_File,
                         Relay_Log_Pos,
                         Seconds_Behind_Master,
                         Retrieved_Gtid_Set,
                         Executed_Gtid_Set,
                         Auto_Position,
                         Replicate_Do_DB,
                         Replicate_Ignore_DB,
                         Replicate_Do_Table,
                         Replicate_Ignore_Table,
                         Replicate_Wild_Do_Table,
                         Replicate_Wild_Ignore_Table
          #其中重要的信息
          $target->{Relay_Master_Log_File} = $status{Relay_Master_Log_File};
          $target->{Exec_Master_Log_Pos}   = $status{Exec_Master_Log_Pos};
          $target->{Relay_Log_File}        = $status{Relay_Log_File};
          $target->{Relay_Log_Pos}         = $status{Relay_Log_Pos};
          # $_server_manager->identify_latest_slaves();  比较各个slave的Master_Log_File和Read_Master_Log_Pos,寻找latest的slave
          # $_server_manager->identify_oldest_slaves();  比较各个slave中的Master_Log_File和Read_Master_Log_Pos,寻找Oldest的slave
    if ( !$_server_manager->is_gtid_auto_pos_enabled() ) {
      $log->info();
      # 进行binlog补充
      $log->info("* Phase 3.2: Saving Dead Master's Binlog Phase..\n");
      $log->info();
      save_master_binlog($dead_master);
      # 判断dead master是否可以ssh连接
      # if ( $_real_ssh_reachable && !$g_skip_save_master_binlog ) {
        # 如果dead master可以ssh连接
        # MHA::ManagerUtil::check_node_version();
        # my $latest_pos = ( $_server_manager->get_latest_slaves() )[0]->{Read_Master_Log_Pos}; save_master_binlog_internal( $latest_file, $latest_pos, $dead_master, );
        # 使用node节点的save_binary_logs脚本在dead master上做拷贝
        # save_binary_logs --command=save --start_file=$master_log_file  --start_pos=$read_master_log_pos --binlog_dir=$dead_master->{master_binlog_dir} --output_file=$_diff_binary_log_remote --handle_raw_binlog=$dead_master->{handle_raw_binlog} --disable_log_bin=$dead_master->{disable_log_bin} --manager_version=$MHA::ManagerConst::VERSION";
        # generate_diff_binary_log()：
            # $_binlog_manager->concat_all_binlogs_from($start_binlog_file, $start_binlog_pos, $out_diff_file)
            # dump_binlog() 拷贝binlog文件到到manage节点的manager_workdir目录下，如果dead master无法ssh登录，则master上未同步到slave的txn丢失
    }
    $log->info();
    # 确定新主
    $log->info("* Phase 3.3: Determining New Master Phase..\n");
    $log->info();
    my $latest_base_slave;
    if ( $_server_manager->is_gtid_auto_pos_enabled() ) {
      $latest_base_slave = $_server_manager->get_most_advanced_latest_slave();
    }
    else {
      $latest_base_slave = find_latest_base_slave($dead_master); #寻找最新的有所有中继日志的slave，用于恢复其他slave
        # my $latest_base_slave = find_latest_base_slave_internal();
        # my $oldest_mlf    = $oldest_slave->{Master_Log_File};
        # my $oldest_mlp    = $oldest_slave->{Read_Master_Log_Pos};
        # my $latest_mlf    = $latest_slaves[0]->{Master_Log_File};
        # my $latest_mlp    = $latest_slaves[0]->{Read_Master_Log_Pos};
        # if ($_server_manager->pos_cmp( $oldest_mlf, $oldest_mlp, $latest_mlf,$latest_mlp ) >= 0 # 判断latest和oldest slave上binlog位置是不是相同，相同就不需要同步relay log
        # apply_diff_relay_logs --command=find --latest
        # 查看latest slave中是否有oldest缺少的relay log，若无则继续,否则failover失败
        # 查找的方法：逆序的读latest slave的relay log文件，一直找到binlog file的position为止
    }
    $new_master = select_new_master( $dead_master, $latest_base_slave ); #选出新的master节点
           # 比较master_log_file:read_master_log_pos
           # 识别优先从库，在线的并带有candidate_master标记
           # 识别应该忽略的从库，带有no_master标记、或者未开启log_bin、与最新从库相比数据延迟比较大(slave与master的binlog position差距大于100000000)
           # 选择优先级依次为：优先列表、最新从库列表、所有从库列表，但一定排除忽略列表
           # 检查新老主库的复制过滤规则是否一致Replicate_Do_DB,Replicate_Ignore_DB,Replicate_Do_Table,Replicate_Ignore_Table
    my ( $master_log_file, $master_log_pos, $exec_gtid_set ) =
      recover_master( $dead_master, $new_master, $latest_base_slave,
      $binlog_server_ref );
    $new_master->{activated} = 1;
    $log->info("* Phase 3: Master Recovery Phase completed.\n");
    $log->info();
    # 恢复从库 类似单独恢复主库的过程
    $log->info("* Phase 4: Slaves Recovery Phase..\n");
    $log->info();
    $error_code = recover_slaves(
      $dead_master,     $new_master,     $latest_base_slave,
      $master_log_file, $master_log_pos, $exec_gtid_set
    ); # 中继补偿（生成Slave与New Slave之间的差异日志，将该日志拷贝到各Slave的工作目录下），指向新主库&启动复制（change_master_and_start_slave），清理新主库的slave复制通道（reset slave all）
    if ( $g_remove_dead_master_conf && $error_code == 0 ) {
      MHA::Config::delete_block_and_save( $g_config_file, $dead_master->{id},
        $log );
    }
    cleanup();
  };
  if ($@) {
    if ( $dead_master && $dead_master->{not_error} ) {
      $log->info($@);
    }
    else {
      MHA::ManagerUtil::print_error( "Got ERROR: $@", $log );
      $mail_body .= "Got Error so couldn't continue failover from here.\n"
        if ($mail_body);
    }
    $_server_manager->disconnect_all() if ($_server_manager);
    undef $@;
  }
  eval {
    send_report( $dead_master, $new_master );
    MHA::NodeUtil::drop_file_if( $_status_handler->{status_file} )
      unless ($error_code);
    if ($_create_error_file) {
      MHA::NodeUtil::create_file_if($_failover_error_file);
    }
  };
  if ($@) {
    MHA::ManagerUtil::print_error( "Got ERROR on final reporting: $@", $log );
    undef $@;
  }
  return $error_code;
}`
## 总结
切换过程：
- **检查配置**
- 检查 mha node 的节点版本信息（get_node_version，实际使用 apply_diff_relay_logs &#8211;version 命令）
- 检查所有 node 节点的 SSH 的连通性
- 检查所有 node 节点的存活状态
- 检查所有从库的 slave sql 线程是否已经启动，没有启动则启动
- **关闭当前失败的 IO 复制线程，并执行脚本切换 VIP**
- 检查所有 node 节点的 SSH 的连通性
- 停止所有从库的 slave io 线程，只要有一个在线从库的 salve io 线程停止失败，那么就终止切换
- 执行 master_ip_failover_script，保证崩溃主库所在主机的 VIP 失活防脑裂，并执行脚本切换 VIP
- **新主恢复**
- 获取新的主从信息
- 获取各个 slave 的复制信息（show slave status）
- 获取复制延迟最小的从库、复制延迟最大的从库
- 如果没有用来补偿的基准从库，终止切换
- 检查去世的 master 的 SSH 的连通性
- 不可达，就会丢失 binlog
- 可达，执行 save_binary_logs &#8211;command=save，将保存后的 binlog 拷贝到 manage 节点的 manager_workdir 目录下
- **选择新主库**
- 比较 master_log_file:read_master_log_pos
- 识别优先从库，在线的并带有 candidate_master 标记
- 识别应该忽略的从库，带有 no_master 标记、或者未开启 log_bin、与最新从库相比数据延迟比较大（slave 与 master 的 binlog position 差距大于 100000000）
- 选择优先级依次为：优先列表、最新从库列表、所有从库列表，但一定排除忽略列表
- 检查新老主库的复制过滤规则是否一致 Replicate_Do_DB,Replicate_Ignore_DB,Replicate_Do_Table,Replicate_Ignore_Table
- 恢复新主库
- 新主库落后于最新从库，那么 ssh 连接上最新从库，执行 apply_diff_relay_logs &#8211;command=generate_and_send
- 等待新主库上已经有的 relaylog 都重放完毕，停止 slave sql 线程
- 执行主控机上的 master_ip_failover &#8211;command=start 脚本，激活新主库的 VIP
- 关闭新主库的只读，开启可写模式
- **恢复从库 & 清理新主库**
- 恢复新从库
- 中继补偿（生成 Slave 与 New Slave 之间的差异日志，将该日志拷贝到各 Slave 的工作目录下）
- 指向新主库 & 启动复制（change_master_and_start_slave）
- 清理新主库的 slave 复制通道（reset slave all）