# 故障分析 | MHA 切换的一个“坑”

**原文链接**: https://opensource.actionsky.com/20210820-mha/
**分类**: 技术干货
**发布时间**: 2021-08-19T00:24:15-08:00

---

作者：张洛丹
原爱可生 DBA 团队成员，现陆金所 DBA 团队成员，对技术执著有追求！
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 背景
在一次变更中使用 MHA 进行主从切换，命令如下：
`masterha_master_switch --master_state=alive --conf=/etc/mha/mha3306.cnf --new_master_host=xx.xx.xx.xx --new_master_port=3306 --interactive=0 --orig_master_is_new_slave
`
然而却遇到了报错，如下：
`[error][/usr/share/perl5/vendor_perl/MHA/ServerManager.pm, ln1213] XX.XX.XX.XX is bad as a new master!
[error][/usr/share/perl5/vendor_perl/MHA/MasterRotate.pm, ln232] Failed to get new master!
[error][/usr/share/perl5/vendor_perl/MHA/ManagerUtil.pm, ln177] Got ERROR:  at /bin/masterha_master_switch line 53.
`
看报错是认为指定的新主是一个`bad new master`。
遇到这个报错内心是懵的，明明切换前检查集群状态、masterha_check_repl都是正常的。嗯……还是对 MHA 的原理了解不够深入。
当时也没时间去研究为什么报错了，于是就手工切换了，接下来就让我们一起去探索为什么会出现这个报错吧！
说明一下，线上主从集群的环境是这样的：
| 角色 | MySQL版本 |
| --- | --- |
| M | MySQL 5.6.40 |
| S1 | MySQL 5.6.40 |
| S2 | MySQL 5.7.29 |
| S3 | MySQL 5.7.29 |
> 
PS：为什么主从版本会不一致呢？
是因为正在做升级，本次切换就是为了将 S2 切换为主，然后将低版本的两个实例升级上去。
## 测试场景
线上通过手工切换绕过了 MHA 的报错，后面要进行分析具体原因。因为现场环境新主的版本和老主库版本是不一样的，猜想是否 MHA 不支持跨版本切换，之前也没有留意这个问题。于是在测试环境中进行了一波测试，下面列出测试场景和测试结论，有兴趣的可以自己测试一下：
| 测试场景 | 原master版本 | 新master版本 | 其他slaves 版本 | 切换结果 |
| --- | --- | --- | --- | --- |
| 场景1 | 5.6.40 | 5.7.29 | 无 | 切换成功 |
| 场景2 | 5.7.29 | 5.6.40 | 无 | 切换成功 |
| 场景3 | 5.6.40 | 5.7.29 | 5.6.38 | 切换失败 |
| 场景4 | 5.6.38 | 5.7.29 | 5.6.40 | 切换失败 |
| 场景5 | 5.6.38 | 5.7.29 | 5.7.29 | 切换成功 |
现象是这么个现象，是不是很好奇，为什么只有一个从库的时候，跨版本可以切换成功，当还有其他从库的时候某些情况可以切换成功，某些情况又切换失败，往下看吧！
## 问题分析
先去google一下，搜索关键词：`mha .. is bad as a new master`，
然后搜出来的并没有我想要的结果，有些参考价值的文章如下：
- 
https://blog.51cto.com/u_860143/2431044 【和我的场景相似，但什么解释也没说】
- 
https://www.modb.pro/db/50655【不太明确，当时没理解】
穷途末路，只能去源码中翻翻了，毕竟 MHA 一款开源的工具【不逼自己一把就不知道自己英文还是不错的】
找到 MHA 选主的相关代码，首先定义了几个数组：
- 
slaves 数组：选取 alive 的 slaves
- 
latest 数组：从 alive slave 中选取复制位点最新的 slaves
- 
pref 数组：配置文件中配置了 candidate_master 的 slaves
- 
bad 数组：后面解释
接着在进行选主的时候按照以下的顺序进行选举：
- 
选举优先级最高的 slave 作为新主（通常是手工切换指定的 new master），如果该 slave 不能作为新主，则报错退出，否则如果是故障切换，则进行下面的步骤
- 
选择复制位点最新并且在 pref 数组里的 slave 作为新主，如果复制位点最新的 slave 不在 pref 数组中，则继续下面步骤
- 
从 pref 中选择一个 slave 作为新主，如果没有选出则继续
- 
选择复制位点最新的 slave 作为新主，如果没有选出则继续
- 
从所有的 slave 中进行选择
- 
经过以上步骤仍然选择不出主则选举失败
`注意`：前面的6个选举步骤，都需要保证新主不在 bad 数组中
`# Picking up new master
# If preferred node is specified, one of active preferred nodes will be new master.
# If the latest server behinds too much (i.e. stopping sql thread for online backups), we should not use it as a new master, but we should fetch relay log there. Even though preferred master is configured, it does not become a master if it's far behind.
sub select_new_master {
  my $self                    = shift;
  my $prio_new_master_host    = shift;
  my $prio_new_master_port    = shift;
  my $check_replication_delay = shift;
  $check_replication_delay = 1 if ( !defined($check_replication_delay) );
  my $log    = $self->{logger};
  my @latest = $self->get_latest_slaves();
  my @slaves = $self->get_alive_slaves();
  my @pref = $self->get_candidate_masters();
  my @bad =
    $self->get_bad_candidate_masters( $latest[0], $check_replication_delay );
  if ( $prio_new_master_host && $prio_new_master_port ) {
    my $new_master =
      $self->get_alive_server_by_hostport( $prio_new_master_host,
      $prio_new_master_port );
    if ($new_master) {
      my $a = $self->get_server_from_by_id( \@bad, $new_master->{id} );
      unless ($a) {
        $log->info("$prio_new_master_host can be new master.");
        return $new_master;
      }
      else {
        $log->error("$prio_new_master_host is bad as a new master!");
        return;
      }
    }
    else {
      $log->error("$prio_new_master_host is not alive!");
      return;
    }
  }
$log->info("Searching new master from slaves..");
  $log->info(" Candidate masters from the configuration file:");
  $self->print_servers( \@pref );
  $log->info(" Non-candidate masters:");
  $self->print_servers( \@bad );
  return $latest[0]
    if ( $#pref < 0 && $#bad < 0 && $latest[0]->{latest_priority} );
  if ( $latest[0]->{latest_priority} ) {
    $log->info(
" Searching from candidate_master slaves which have received the latest relay log events.."
    ) if ( $#pref >= 0 );
    foreach my $h (@latest) {
      foreach my $p (@pref) {
        if ( $h->{id} eq $p->{id} ) {
          return $h
            if ( !$self->get_server_from_by_id( \@bad, $p->{id} ) );
        }
      }
    }
    $log->info("  Not found.") if ( $#pref >= 0 );
  }
  #new master is not latest
  $log->info(" Searching from all candidate_master slaves..")
    if ( $#pref >= 0 );
  foreach my $s (@slaves) {
    foreach my $p (@pref) {
      if ( $s->{id} eq $p->{id} ) {
        my $a = $self->get_server_from_by_id( \@bad, $p->{id} );
        return $s unless ($a);
      }
    }
  }
  $log->info("  Not found.") if ( $#pref >= 0 );
if ( $latest[0]->{latest_priority} ) {
    $log->info(
" Searching from all slaves which have received the latest relay log events.."
    );
    foreach my $h (@latest) {
      my $a = $self->get_server_from_by_id( \@bad, $h->{id} );
      return $h unless ($a);
    }
    $log->info("  Not found.");
  }
  # none of latest servers can not be a master
  $log->info(" Searching from all slaves..");
  foreach my $s (@slaves) {
    my $a = $self->get_server_from_by_id( \@bad, $s->{id} );
    return $s unless ($a);
  }
  $log->info("  Not found.");
  return;
}
`
因为报错是说新主是 bad ，那我们重点看下新主为什么会被判定为 bad ，如何判定的。获取 bad 列表的函数是`get_bad_candidate_masters`，如下，可以看出具有以下五种情况的 slave 会被判定为 bad ：
- 
dead servers
- 
{no_master} >= 1【在配置文件中设置了no_master】
- 
log_bin is disabled【未开启binlog】
- 
{oldest_major_version} eq &#8216;0&#8217;【MySQL major 版本不是最旧的】
- 
too much replication delay【延迟大，与 master 的 binlog position 差距大于 100000000】
`# The following servers can not be master:
# - dead servers
# - Set no_master in conf files (i.e. DR servers)
# - log_bin is disabled
# - Major version is not the oldest
# - too much replication delay
sub get_bad_candidate_masters($$$) {
  my $self                    = shift;
  my $latest_slave            = shift;
  my $check_replication_delay = shift;
  my $log                     = $self->{logger};
  my @servers     = $self->get_alive_slaves();
  my @ret_servers = ();
  foreach (@servers) {
    if (
         $_->{no_master} >= 1
      || $_->{log_bin} eq '0'
      || $_->{oldest_major_version} eq '0'
      || (
        $latest_slave
        && ( $check_replication_delay
          && $self->check_slave_delay( $_, $latest_slave ) >= 1 )
      )
      )
    {
      push( @ret_servers, $_ );
    }
  }
  return @ret_servers;
}
`
对于1-3，5很好理解，而且线上后来通过监控进行了排查，并不存在这些问题，于是重点看下4是如何来进行定义的。
找到相关的函数：
`sub compare_slave_version($) {
  my $self    = shift;
  my @servers = $self->get_alive_servers();
  my $log     = $self->{logger};
  $log->debug(" Comparing MySQL versions..");
  my $min_major_version;
  foreach (@servers) {
    my $dbhelper = $_->{dbhelper};
    -- 如果dead或不为从库，则跳过判断
    next if ( $_->{dead} || $_->{not_slave} );
    my $parsed_major_version =
      MHA::NodeUtil::parse_mysql_major_version( $_->{mysql_version} );
    if (!$min_major_version
      || $parsed_major_version < $min_major_version )
    {
      $min_major_version = $parsed_major_version;
    }
  }
  foreach (@servers) {
    my $dbhelper = $_->{dbhelper};
    next if ( $_->{dead} || $_->{not_slave} );
    my $parsed_major_version =
      MHA::NodeUtil::parse_mysql_major_version( $_->{mysql_version} );
    if ( $min_major_version == $parsed_major_version ) {
      $_->{oldest_major_version} = 1;
    }
    else {
      $_->{oldest_major_version} = 0;
    }
  }
  $log->debug("  Comparing MySQL versions done.");
}
`
可以看到，这里首先会从 alive_servers 中获取最小的版本，也就是`min_major_version`：
- 
如果实例是 dead 或非从库，则不比较该实例，否则进行比较，关键代码`next if ( $_->{dead} || $_->{not_slave} );`
接下来，根据传入的 server 的`parsed_major_version`【MySQL 的主版本，例如，5.6，5.7】和`min_major_version`进行对比：
- 
如果`parsed_major_version==min_major_version`，则`oldest_major_version`=1；否则`oldest_major_version`=0
综上可以看出，新主的版本号，需要是所有从库中版本最低的才能作为新的主库，否则将不能作为新的主库。
到这里，问题就水落石出了，回到我们前面测试的场景中，就弄明白了：
- 
场景1和场景2只有一个从库的时候，跨版本切换可以切换成功，是因为这个从库的主版本就是 min_major_version
- 
场景3和场景4中切换失败的原因是，新主的主版本为5.7，而所有从库中最小的主版本号为5.6，因此不能切换
但是，MHA 为什么会这样设计呢？
- 
MySQL 高版本到低版本的复制是没有问题的，但是低版本向高版本复制可能会出现问题。这个在官方有介绍：https://dev.mysql.com/doc/refman/5.7/en/replication-compatibility.html
- 
不过 MHA 在比较最小版本的时候没有比较原主库的版本，这在切换的时候还是可能会出现低版本向高版本复制的情况，比如测试场景1，不知道是基于什么考虑，欢迎大家留言讨论。
## 小结
MHA 选主逻辑：
- 
选举优先级最高的 slave 作为新主（通常是手工切换指定的 new master），如果该 slave 不能作为新主，则报错退出，否则如果是故障切换，则进行下面的步骤
- 
选择复制位点最新并且在设置了 candidate_master 的 slave 作为新主，如果复制位点最新的 slave 没有设置 candidate_master ，则继续下面步骤
- 
从设置了 candidate_master 中选择一个 slave 作为新主，如果没有选出则继续
- 
选择复制位点最新的 slave 作为新主，如果没有选出则继续
- 
从所有的 slave 中进行选择
- 
经过以上步骤仍然选择不出主则选举失败
`注意`：前面的6个选举步骤，都需要保证新主不在bad数组中
bad数组定义如下：
- 
dead servers
- 
{no_master} >= 1【在配置文件中设置了no_master】
- 
log_bin is disabled【未开启binlog】
- 
{oldest_major_version} eq &#8216;0&#8217;【MySQL major 版本不是最旧的】
- 
too much replication delay【延迟大，与 master 的 binlog position 差距大于 100000000】
其中4这个是比较容易忽视的一点，需要注意！