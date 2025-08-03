# 故障分析 | 如何提高 MHA 的网络容忍能力？（下）

**原文链接**: https://opensource.actionsky.com/20210322-mha-%e7%9a%84%e7%bd%91%e7%bb%9c%e5%ae%b9%e5%bf%8d%e8%83%bd%e5%8a%9b%ef%bc%9f%ef%bc%88%e4%b8%8b%ef%bc%89/
**分类**: 技术干货
**发布时间**: 2021-03-22T00:37:48-08:00

---

作者：刘开洋
爱可生交付服务部团队北京 DBA，主要负责处理 MySQL 的 troubleshooting 和我司自研数据库自动化管理平台 DMP 的日常运维问题，对数据库及周边技术有浓厚的学习兴趣，喜欢看书，追求技术。
本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 说明
本节主要介绍对 secondary_check_script 调用 masterha_secondary_check 脚本的说明。
`[root@yang-03 ~]# cat /usr/bin/masterha_secondary_check
#!/usr/bin/env perl
···
$| = 1;
GetOptions(
  'help'              => \$help,
  'version'           => \$version,
  'secondary_host=s'  => \@monitoring_servers,
  'user=s'            => \$ssh_user,
  'port=s'            => \$ssh_port,
  'options=s'         => \$ssh_options,
  'master_host=s'     => \$master_host,
  'master_ip=s'       => \$master_ip,
  'master_port=i'     => \$master_port,
  'master_user=s'     => \$master_user,
  'master_password=s' => \$master_password,
  'ping_type=s'       => \$ping_type,
  'timeout=i'         => \$timeout,
);
 
if ($version) {
  print "masterha_secondary_check version $MHA::ManagerConst::VERSION.\n";
  exit 0;
}
 
if ($help) {
  pod2usage(0);
}
 
unless ($master_host) {
  pod2usage(1);
}
 
sub exit_by_signal {
  exit 1;
}
local $SIG{INT} = $SIG{HUP} = $SIG{QUIT} = $SIG{TERM} = \&exit_by_signal;
 
$ssh_user    = "root" unless ($ssh_user);
$ssh_port    = 22     unless ($ssh_port);
$master_port = 3306   unless ($master_port);
 
if ($ssh_options) {
  $MHA::ManagerConst::SSH_OPT_CHECK = $ssh_options;
}
$MHA::ManagerConst::SSH_OPT_CHECK =~ s/VAR_CONNECT_TIMEOUT/$timeout/;
 
# 0: master is not reachable from all monotoring servers
# 1: unknown errors
# 2: at least one of monitoring servers is not reachable from this script
# 3: master is reachable from at least one of monitoring servers
my $exit_code = 0;
 
foreach my $monitoring_server (@monitoring_servers) {
  my $ssh_user_host = $ssh_user . '@' . $monitoring_server;
  my $command =
"ssh $MHA::ManagerConst::SSH_OPT_CHECK -p $ssh_port $ssh_user_host \"perl -e "
    . "\\\"use IO::Socket::INET; my \\\\\\\$sock = IO::Socket::INET->new"
    . "(PeerAddr => \\\\\\\"$master_host\\\\\\\", PeerPort=> $master_port, "
    . "Proto =>'tcp', Timeout => $timeout); if(\\\\\\\$sock) { close(\\\\\\\$sock); "
    . "exit 3; } exit 0;\\\" \"";
  my $ret = system($command);
  $ret = $ret >> 8;
  if ( $ret == 0 ) {
    print
"Monitoring server $monitoring_server is reachable, Master is not reachable from $monitoring_server. OK.\n";
    next;
  }
  if ( $ret == 3 ) {
    if ( defined $ping_type
      && $ping_type eq $MHA::ManagerConst::PING_TYPE_INSERT )
    {
      my $ret_insert;
      my $command_insert =
          "ssh $MHA::ManagerConst::SSH_OPT_CHECK -p $ssh_port $ssh_user_host \'"
        . "/usr/bin/mysql -u$master_user -p$master_password -h$master_host "
        . "-e \"CREATE DATABASE IF NOT EXISTS infra; "
        . "CREATE TABLE IF NOT EXISTS infra.chk_masterha (\\`key\\` tinyint NOT NULL primary key,\\`val\\` int(10) unsigned NOT NULL DEFAULT '0'\) engine=InnoDB; "
        . "INSERT INTO infra.chk_masterha values (1,unix_timestamp()) ON DUPLICATE KEY UPDATE val=unix_timestamp()\"\'";
      my $sigalrm_timeout = 3;
      eval {
        local $SIG{ALRM} = sub {
          die "timeout.\n";
        };
        alarm $sigalrm_timeout;
        $ret_insert = system($command_insert);
        $ret_insert = $ret_insert >> 8;
        alarm 0;
      };
      if ( $@ || $ret_insert != 0 ) {
        print
"Monitoring server $monitoring_server is reachable, Master is not writable from $monitoring_server. OK.\n";
        next;
      }
    }
    print "Master is reachable from $monitoring_server!\n";
    $exit_code = 3;
    last;
  }
  else {
    print "Monitoring server $monitoring_server is NOT reachable!\n";
    $exit_code = 2;
    last;
  }
}
 
exit $exit_code;
···
`看到上面的脚本有点头大，作为一个专一的 DBA，一直追求着 shell，Perl 语言不熟啊，细看之后发现与 shell 脚本有异曲同工之妙，从相应的注释中，我们找到了该检查脚本的返回值，即 0,1,2,3，分别代表的含义如下：
`# 0: master is not reachable from all monotoring servers
# 1: unknown errors
# 2: at least one of monitoring servers is not reachable from this script
# 3: master is reachable from at least one of monitoring servers
`下面就让我们做几个测试体会体会吧。
## 验证
本实验使用 iptables 进行网络故障场景的模拟，以下图中四条链路是否连通来进行测试，查看对应监控脚本的返回值是否和上面讲的一致。
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片1-1.png)											
检查命令：
`shell > masterha_secondary_check -s remote_host1 -s remote_host2 .. --user=root  --master_host=master_ip  --master_ip=master_ip  --master_port=3306 --master_user=mha --master_password=*** --ping_type=SELECT`
#### test 1
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片2-2.png)											
**output：**
Master is reachable from remote_host1!
#### test 2
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片3-3.png)											
**output：**
Master is reachable from remote_host1!
#### test 3
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片4-4.png)											
**output：**
ssh: connect to host remote_host1 port 22: Connection timed out.
Monitoring server remote_host1 is NOT reachable!
#### test 4
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片5-5.png)											
**output：**
Master is reachable from remote_host1!
#### test 5
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片6-6.png)											
**output：**
Monitoring server remote_host1 is reachable, Master is not reachable from remote_host1. OK.
Master is reachable from remote_host2!
#### test 6
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片7-7.png)											
**output：**
ssh: connect to host remote_host1 port 22: Connection timed out.
Monitoring server remote_host1 is NOT reachable!
#### test 7
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片8.png)											
**output：**
当输入的命令有误时，即符合 unknown errors，返回值为 1。
#### test 8
![](https://opensource.actionsky.com/wp-content/uploads/2021/03/图片9-9.png)											
**output：**
Monitoring server remote_host1 is reachable, Master is not reachable from remote_host1. OK.
Monitoring server remote_host2 is reachable, Master is not reachable from remote_host2. OK.
> PS：这里有一个问题，在使用监控服务器 slave 检查主从之间网络连通性时，masterha_secondary_check 脚本对监控主机的使用存在优先级，它会优先使用 remote_host1，如果 remote_host1 与 master 之间网络不同，才会使用 remote_host2 检查与 master 之间的网络连通性。
## 总结
通过测试验证，发现 MHA 通过调用 secondary_check_script 参数对于网络问题具有一定的容忍能力，只是相关文档描述过于简略，如需继续使用，需要不断进行验证测试，总体来讲，MHA 的功能还是及其强大的。
**相关推荐：**
[故障分析 | 如何提高 MHA 的网络容忍能力？（上）](https://opensource.actionsky.com/20210315-mha/)