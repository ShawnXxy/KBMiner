# 故障分析 | MySQL 启动遭遇 Permission denied 失败案例一则

**原文链接**: https://opensource.actionsky.com/20221031-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-10-30T21:45:03-08:00

---

作者：任坤
现居珠海，先后担任专职 Oracle 和 MySQL DBA，现在主要负责 MySQL、mongoDB 和 Redis 维护工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 背景
> OS：centos 7.9
MySQL：5.7
首次使用某海外云，申请云主机自建 mysql ，service mysqld start 启动报错
Job for mysqld.service failed because the control process exited with err
or code. See "systemctl status mysqld.service" and "journalctl ‐xe" for details.
#### 诊断
journalctl -xe 查看详细日志。
Oct 09 06:57:42 mysqld[30507]: 2022‐10‐09T06:57:42.953987Z 0 [Warning] Ca
n't create test file /data/var/.lower‐test
Oct 09 06:57:42 mysqld[30507]: 2022‐10‐09T06:57:42.954069Z 0 [Note]
/usr/sbin/mysqld (mysqld 5.7.34‐log) starting as process 30510 ...
Oct 09 06:57:42 mysqld[30507]: 2022‐10‐09T06:57:42.956924Z 0 [Warning] Ca
n't create test file /data/var/.lower‐test
Oct 09 06:57:42 mysqld[30507]: 2022‐10‐09T06:57:42.956958Z 0 [Warning] Ca
n't create test file /data/var/.lower‐test
Oct 09 06:57:42 mysqld[30507]: 2022‐10‐09T06:57:42.957892Z 0 [ERROR] Coul
d not open file './err.log' for error logging: Permission denied
Oct 09 06:57:42 mysqld[30507]: 2022‐10‐09T06:57:42.957954Z 0 [ERROR] Abor
ting
查看文件权限，属主都是 mysql 。
# ll ‐ld /data/var
drwxr‐xr‐x. 5 mysql mysql 4096 Oct 9 06:14 /data/var
# ll /data/var/err.log
‐rw‐r‐‐‐‐‐. 1 mysql mysql 33067 Oct 9 06:14 /data/var/err.log
service mysqld start 尝试好几次都以失败告终，手工执行 mysqld &#8211;defaults-file=/etc/my.cnf 能成功启动，说明 mysql 的配置是正常的，问题应该出现在 OS 系统设置。
采用 strace 跟踪一下，
strace ‐tt ‐T ‐f ‐e trace=file ‐o service.log service mysqld start
输出内容
socket(AF_UNIX, SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK, 0) = 3
....
connect(3, {sa_family=AF_UNIX, sun_path="/run/systemd/private"}, 22) = 0
getsockopt(3, SOL_SOCKET, SO_PEERCRED, {pid=1, uid=0, gid=0}, [12]) = 0
getsockopt(3, SOL_SOCKET, SO_PEERSEC, "system_u:system_r:init_t:s0‐
s0:c"..., [64‐>40]) = 0
....
recvmsg(3, {msg_namelen=0}, MSG_DONTWAIT|MSG_NOSIGNAL|MSG_CMSG_CLOEXEC) = ‐1 EAGAIN (Resource temporarily unavailable)
socket 设置出现了 selinux context 相关信息，应该是与 selinux 设置有关。
查看系统日志 /var/log/audit/audit.log 复核，明确记录了 err.log 权限验证失败信息。
type=SYSCALL msg=audit(1665296076.671:725): arch=c000003e syscall=2 succe
ss=no exit=‐13 a0=1fd7900 a1=441 a2=1b6 a3=1aeb8380 items=0 ppid=1 pid=3616
auid=4294967295 uid=27 gid=27 euid=27 suid=27 fsuid=27 egid=27 sgid=27 fsgi
d=27 tty=(none) ses=4294967295 comm="mysqld" exe="/usr/sbin/mysqld" subj=sy
stem_u:system_r:mysqld_t:s0 key=(null)
type=PROCTITLE msg=audit(1665296076.671:725): proctitle=2F7573722F7362696
E2F6D7973716C64002D2D6461656D6F6E697A65002D2D7069642D66696C653D2F7661722F72
756E2F6D7973716C642F6D7973716C642E706964
type=AVC msg=audit(1665296076.671:726): avc: denied { append } for pid=36
16 comm="mysqld" name="err.log" dev="sdb1" ino=5505026 scontext=system_u:sy
stem_r:mysqld_t:s0 tcontext=unconfined_u:object_r:unlabeled_t:s0 tclass=fil
e permissive=0
确认机器开启了 selinux 。
# getenforce
Enforcing
# grep ‐v '^#' /etc/selinux/config
SELINUX=enforcing
SELINUXTYPE=targeted
linux提供两种鉴权认证体系，**DAC(Discretionary Access control) **自主访问控制和 **MAC(Mandatory Access control)** 强制性访问控制，平时最常使用的是 DAC 。
DAC 将资源访问者分成三类，分别是 Owner 、Group 、Other ，针对这三类访问者设置访问权限，权限分成 read、write、execute ，访问者通过自己 uid/gid 和文件权限匹配，来确定是否可以访问。
**这种策略有2个明显缺陷：**
- 某个OS账号启动的任意进程，都拥有这个账号的所有权限，可以改动/删除这个账号下的所有文件资源。
- Root 账号拥有最高权限几乎可以做任意事情，一旦入侵者拿到root 权限，就能完全掌控该机器。
MAC 对权限做了细化，每访问一个文件资源都需要进行验证，并且限制了 Root 账号权限，即使你有 root 权限，如果无法通过 MAC 验证，同样无法执行相关操作。
**DAC的权限访问粒度的用户级别，MAC则是文件级别。**
SELinux context是一个冒号分隔的字符串，包含4个部分：user:role:type:range
上面的 avc: denied 报错信息可以做如下解读：
- denied -> append //缺少什么权限
- scontext -> mysqld_t //谁缺少权限
- tcontext -> unlabeled_t //对哪个文件缺少权限
- tclass -> file //什么类型的文件
这条信息可以解读为 mysqld_t 对 unlabeled_t 的 file 类型文件 err.log 缺少 append 权限。
#### 解决方案
我们线上的机器默认都是关闭 selinux ，因此该问题最简单的解决方案就是关闭 selinux 。
修改 /etc/selinux/config 文件，设置 SELINUX=disabled ，重启机器，mysqld可以正常启动。