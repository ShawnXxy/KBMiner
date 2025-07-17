# 技术分享 | MySQL 如何适配 AppArmor

**原文链接**: https://opensource.actionsky.com/20211213-apparmor/
**分类**: 技术干货
**发布时间**: 2021-12-13T00:13:09-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 引言
AppArmor （Debian 系平台）是一款内核级别的安全机制，通过 AppArmor  来让 Linux 系统实现严格的资源访问控制，类似 SELinux（RedHat 系列平台）。
我本地环境为：OS 版本 Ubuntu 18，DB 版本 MySQL 8.0.27。
AppArmor 通过目录/etc/apparmor.d/ 下的一系列配置文件来分别限制每个进程对 OS 资源的访问权限。
AppArmor 有两种工作模式：
- 
Enforced/Confined: 严格按照配置文件来限制对应的进程访问OS资源的行为，拒绝不在配置范围内的进程运行。
- 
Complaining/Learning:  仅记录进程行为，不对其进行限制。
#### 遇到的问题是：
我启动 MySQL ，未成功：
`root@ytt-ubuntu:~# systemctl start mysql
Job for mysql.service failed because the control process exited with error code.
See "systemctl status mysql.service" and "journalctl -xe" for details.
`
我摘出来几条核心的错误信息：
`root@ytt-ubuntu:~# journalctl -xe
-- Defined-By: systemd
-- user-122.slice 单元已结束停止操作。
11月 16 16:14:00 ytt-ubuntu kernel: audit: type=1400 audit(1637050440.395:101): apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/op
11月 16 16:14:00 ytt-ubuntu audit[7237]: AVC apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/opt/mysql/data/mysqld_tmp_file_case_i
11月 16 16:14:01 ytt-ubuntu audit[7270]: AVC apparmor="DENIED" operation="mknod" profile="/usr/sbin/mysqld" name="/opt/mysql/log/error.log" pid=7270 com
11月 16 16:14:01 ytt-ubuntu systemd[1]: mysql.service: Main process exited, code=exited, status=1/FAILURE
11月 16 16:14:01 ytt-ubuntu systemd[1]: mysql.service: Failed with result 'exit-code'.
11月 16 16:14:01 ytt-ubuntu systemd[1]: Failed to start MySQL Community Server.
-- Subject: mysql.service 单元已失败
`
由错误信息可以看到，AppArmor 阻止了 MySQL 服务启动，可能的原因是启动 MySQL 服务需要访问的目录在 AppArmor 里没有配置。
#### 想起来我动过配置文件：
###### 源配置内容：
`[mysqld]
pid-file       = /var/run/mysqld/mysqld.pid
socket         = /var/run/mysqld/mysqld.sock 
datadir        = /var/lib/mysql
log-error      = /var/log/mysql/error.log
`
###### 我改后的配置内容：
`[mysqld]           
pid-file        = /opt/mysql/mysqld.pid
socket          = /opt/mysql/mysqld.sock
datadir         = /opt/mysql/data
log-error       = /opt/mysql/log/error.log
`
#### 此时有两种方法来解决这个问题。
##### 第一， 直接更改AppArmor 的配置文件：
给/etc/apparmor.d/user.sbin.mysqld里添加如下内容：(或者把原来MySQL相关的目录替换掉也行)
`
# pid，socket等文件目录
/opt/mysql/* rw,
# 数据目录内容 
/opt/mysql/data/ r,
/opt/mysql/data/** rwk,
#日志文件内容
/opt/mysql/log/ r,
/opt/mysql/log** rw,
`
重载 AppArmor 服务
`root@ytt-ubuntu:~# systemctl reload apparmor
`
再次重启 MySQL ，启动成功。
`root@ytt-ubuntu:/opt/mysql# systemctl start mysql
`
查看状态
`root@ytt-ubuntu:/home/ytt# systemctl status mysql
● mysql.service - MySQL Community Server
Loaded: loaded (/lib/systemd/system/mysql.service; disabled; vendor preset: enabled)
Active: activating (start) since Tue 2021-11-16 16:49:12 CST; 40s ago
Docs: man:mysqld(8)
http://dev.mysql.com/doc/refman/en/using-systemd.html
Process: 3137 ExecStartPre=/usr/share/mysql-8.0/mysql-systemd-start pre (code=exited, status=0/SUCCESS)
Main PID: 3191 (mysqld)
Status: "Server startup in progress"
Tasks: 24 (limit: 4915)
CGroup: /system.slice/mysql.service
└─3191 /usr/sbin/mysqld
11月 16 16:49:12 ytt-ubuntu systemd[1]: Starting MySQL Community Server...
11月 16 16:49:54 ytt-ubuntu systemd[1]: Started MySQL Community Server.
`
##### 第二， 改变 AppArmor 的默认工作模式，由强制模式改为抱怨模式：
得先安装 apparmor-utils 包，里面包含了很多有用的程序来操作 AppArmor .
`root@ytt-ubuntu:~# apt-get install apparmor-utils
`
单独配置 MySQL 服务进入抱怨模式：
`root@ytt-ubuntu:~# aa-complain /etc/apparmor.d/usr.sbin.mysqld 
Setting /etc/apparmor.d/usr.sbin.mysqld to complain mode.
`
重载 AppArmor
`root@ytt-ubuntu:~# systemctl reload apparmor
`
启动 MySQL 服务
`root@ytt-ubuntu:~# systemctl restart mysql
`
查看状态
`root@ytt-ubuntu:~# systemctl status mysql
● mysql.service - MySQL Community Server
Loaded: loaded (/lib/systemd/system/mysql.service; disabled; vendor preset: enabled)
Active: active (running) since Tue 2021-11-16 17:11:12 CST; 12s ago
Docs: man:mysqld(8)
http://dev.mysql.com/doc/refman/en/using-systemd.html
Process: 3712 ExecStartPre=/usr/share/mysql-8.0/mysql-systemd-start pre (code=exited, status=0/SUCCESS)
Main PID: 3767 (mysqld)
Status: "Server is operational"
Tasks: 41 (limit: 4915)
CGroup: /system.slice/mysql.service
└─3767 /usr/sbin/mysqld
11月 16 17:10:45 ytt-ubuntu systemd[1]: Starting MySQL Community Server...
11月 16 17:11:12 ytt-ubuntu systemd[1]: Started MySQL Community Server.
`
##### 以上MySQL的行为基   zat于APT包安装产生，如果采用MySQL二进制包安装，则可以规避这个问题。