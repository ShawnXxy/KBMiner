# 技术分享 | SELinux 与 MySQL

**原文链接**: https://opensource.actionsky.com/20210108-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-01-08T00:51:04-08:00

---

作者：姚远MySQL ACE，华为云MVP，专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6，5.7，8.0 OCP。现在鼎甲科技任技术顾问，为同事和客户提供数据库培训和技术支持服务。本文来源：原创投稿* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
为了提高 Linux 系统的安全性，在 Linux 上通常会使用 SELinux 或 AppArmor 实现强制访问控制（Mandatory Access Control  MAC）。对于 MySQL 数据库的强制访问控制策略通常是激活的，如果用户采用默认的配置，并不会感到强制访问控制策略对 MySQL 数据库的影响，一旦用户修改了 MySQL 数据库的默认配置，例如默认的数据目录或监听端口，MySQL 数据库的活动就会被 SELinux 或 AppArmor 阻止，数据库无法启动，本文简单介绍 SELinux 对 MySQL 数据库的影响。
# 一、简介
SELinux（Secure Enhanced Linux）是一个内核级的安全机制，从 2.6 内核之后，集成到 Linux 内核中。它允许管理员细粒度地定义访问控制，未经定义的访问一律禁止。
SELinux 有三种工作模式：
- enforcing：强制模式。任何违反策略的行为都会被禁止，并且产生警告信息。
- permissive：允许模式。违反策略的行为不会被禁止，只产生警告信息。
- disabled：关闭 SELinux。
使用 getenforce 命令来显示 SELinux 的当前模式。更改模式使用 setenforce 0（设置为允许模式）或 setenforce 1（强制模式）。这些设置重启后就会失效，可以编辑 `/etc/selinux/config` 配置文件并设置 SELINUX 变量为 enforcing、permissive 或 disabled，保存设置让其重启后也有效。
使用下面的命令查看 SELinux 的状态：`[root@redhat7 ~]# sestatus
SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Max kernel policy version:      28`
## 二、查看 MySQL 的 SELinux 的上下文
可以使用 `ps -Z` 查看 mysqld 进程的 SELinux 的上下文：
`[root@redhat7 ~]# ps -eZ | grep mysqld
system_u:system_r:mysqld_t:s0    2381 ?        00:01:00 mysqld`
也可以使用 `ls -Z` 查看 MySQL 数据目录的 SELinux 的上下文：
`[root@redhat7 ~]# ls -dZ /var/lib/mysql
drwxr-x--x. mysql mysql system_u:object_r:mysqld_db_t:s0 /var/lib/mysql`
参数说明：
- system_u 是系统进程和对象的 SELinux 用户标识。
- system_r 是用于系统进程的 SELinux 角色。
- objects_r 是用于系统对象的 SELinux 角色。
- mysqld_t 是与 mysqld 进程相关的 SELinux 类型。
- mysqld_db_t 是与 MySQL 数据目录相关的 SELinux 类型。
## 三、修改对 MySQL 数据目录的访问控制
如果我们把 MySQL 数据目录从默认的 `/var/lib/mysql` 改成其他目录，SELinux 将会阻止 mysqld 进程访问 MySQL 数据目录，从而造成 MySQL 无法启动，相关拒绝访问的信息记录在 `/var/log/audit/audit.log` 文件中：
`[root@redhat7 ~]# grep mysql /var/log/audit/audit.log  |grep denied
type=AVC msg=audit(1609212427.622:104): avc:  denied  { write } for  pid=2218 comm="mysqld" name="data" dev="dm-0" ino=217976179 scontext=system_u:system_r:mysqld_t:s0 tcontext=system_u:object_r:default_t:s0 tclass=dir
type=AVC msg=audit(1609212427.627:105): avc:  denied  { write } for  pid=2218 comm="mysqld" name="data" dev="dm-0" ino=217976179 scontext=system_u:system_r:mysqld_t:s0 tcontext=system_u:object_r:default_t:s0 tclass=dir
type=AVC msg=audit(1609212427.628:106): avc:  denied  { read write } for  pid=2218 comm="mysqld" name="binlog.index" dev="dm-0" ino=202759631 scontext=system_u:system_r:mysqld_t:s0 tcontext=system_u:object_r:default_t:s0 tclass=file`
我们可以 SELinux 关闭或改成允许模式后再启动 MySQL 数据库，但这种方法通常不推荐，因为这样会把所有的 SELinux 的安全策略都终止了，留下了安全隐患。专业的做法是把新的 MySQL 数据目录增加到mysqld_db_t 这个 SELinux 类型中，例如使用 `semanage fcontext` 命令的 `-a` 选项增加一个目录为 `/disk1/data` 的 MySQL 数据目录，然后使用命令 `restorecon` 恢复这个数据目录对应的 SELinux 上下文，代码如图所示：
`root@redhat7 ~]# semanage fcontext -a -t mysqld_db_t “/disk1/data(/.*)?”
root@redhat7 ~]# restorecon -Rv /disk1/data`
然后可以用  `semanage fcontext` 命令的 `-l` 选项进行检查，发现 mysqld_db_t 这个类型现在有两条记录，分别是系统默认的和刚才增加的：
`[root@redhat7 ~]# semanage fcontext -l|grep mysqld_db_t
/var/lib/mysql(/.*)?                               all files          system_u:object_r:mysqld_db_t:s0 
/disk1/data(/.*)?                                  all files          system_u:object_r:mysqld_db_t:s0`
再启动 mysqld 即可成功！
## 四、修改对 MySQL 其他对象的访问控制
除了可以修改对 MySQL 数据目录的访问控制外，还可以采用类似的方法修改对其他 MySQL 对象的访问控制，例如：控制 MySQL 的错误日志的类型是 mysqld_log_t，采用下面的命令增加 MySQL 的错误日志的记录：
`semanage fcontext -a -t mysqld_log_t "/path/to/my/custom/error.log"
restorecon -Rv /path/to/my/custom/error.log`
控制 MySQL 的 PID 文件的类型是 mysqld_var_run_t，采用下面的命令增加 MySQL 的 PID 文件的记录：
`semanage fcontext -a -t mysqld_var_run_t "/path/to/my/custom/pidfile/directory/.*?"
restorecon -Rv /path/to/my/custom/pidfile/directory`
控制 MySQL 的监听端口的类型是 mysqld_port_t，采用下面的命令增加一个 3307 的监听端口：
`semanage port -a -t mysqld_port_t -p tcp 3307`
**文章推荐：**
[故障分析 |  正确使用 auth_socket 验证插件](https://opensource.actionsky.com/20201123-mysql/)
[技术分享 | 客户端连接 MySQL 失败故障排除](https://opensource.actionsky.com/20201116-mysql/)
[技术分享 | MySQL 启动失败的常见原因](https://opensource.actionsky.com/20201109-mysql/)