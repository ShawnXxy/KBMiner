# 技术分享 | MySQL 编写脚本时避免烦人的警告

**原文链接**: https://opensource.actionsky.com/20220615-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-06-15T17:29:17-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
有客户在编写前期数据库安全规范时，就如何更安全的在 Linux Shell 端操作 MySQL 这一块，让我们帮忙出一份详尽的说明文档。其中有一项内容就是如何在 Linux Shell 下调用 MySQL 各种命令行工具时屏蔽掉烦人的告警信息输出，诸如下面这样：
root@ytt-ubuntu18:/home/ytt# mysql -uytt -proot -e "select version()"mysql: [Warning] Using a password on the command line interface can be insecure.+-----------+| version() |+-----------+| 8.0.29    |+-----------+
其实这是一个非常古老的问题！百度随便一搜，各种解决方法都有，但都写的不是很完善。
这样的告警信息对命令执行结果的输出非常不友好，那么我们如何屏蔽掉它？下面我来罗列下几种我能想到的方法，以供参考。
#### 1、给用户空密码（不推荐）
给用户赋予空密码虽然可以屏蔽掉警告信息，但是极不安全，类似于 MySQL 服务初始化时的 **&#8211;initialize-insecure** 选项。
root@ytt-ubuntu18:/home/ytt# mysql -u ytt_no_pass -e "select user()"
+-----------------------+
| user()                |
+-----------------------+
| ytt_no_pass@localhost |
+-----------------------+
#### 2、配置文件不同块加入用户名密码（不推荐）
MySQL 的配置文件有 my.cnf、mysql.cnf、mysqld.cnf 等等，只要在这些配置文件里的不同块下添加对应的用户名和密码即可。
root@ytt-ubuntu18:/home/ytt# cat /etc/mysql/conf.d/mysql.cnf[mysql]prompt=mysql:\d:\v>user=yttpassword=rootport=3340[mysqldump]user=yttpassword=rootport=3340   [mysqladmin]user=yttpassword=rootport=3340
以上[mysql]块下的内容表示对 mysql 命令行生效，[mysqldump]块下的内容表示对 mysqldump 工具生效，[mysqladmin]块下的内容表示对 mysqladmin 工具生效。
或者写简单点，统一加到**【client】** 里，表示对所有客户端生效。注意只能把共享的部分内容加到这里。
root@ytt-ubuntu18:/home/ytt# cat /etc/mysql/conf.d/mysql.cnf[mysql]prompt=mysql:\d:\v>[client]user=yttpassword=rootport=3340
由于这些块都是针对客户端设置，不需要重启 MySQL 服务，可立即生效。
root@ytt-ubuntu18:/home/ytt# mysql -e "select user()"+---------------+| user()        |+---------------+| ytt@localhost |+---------------+
#### 3、设置 MySQL 环境变量（不推荐）
MySQL 有一些内置环境变量，对所有客户端生效。官方的环境变量列表如下：
[https://dev.mysql.com/doc/refman/8.0/en/environment-variables.html](https://dev.mysql.com/doc/refman/8.0/en/environment-variables.html)
给当前用户设置所需的环境变量，之后再调用命令行工具即可。比如设置密码环境变量 MYSQL_PWD 、传统 TCP 端口环境变量 MYSQL_TCP_PORT 等。
root@ytt-ubuntu18:/home/ytt# export MYSQL_PWD=root MYSQL_TCP_PORT=3340    root@ytt-ubuntu18:/home/ytt# mysql -uytt -e "select user()"+---------------+| user()        |+---------------+| ytt@localhost |+---------------+
此方法也不推荐使用，环境变量 MYSQL_PWD 容易被其他用户获取。比如直接用 ps 命令就可以轻易获取 MYSQL_PWD 的值。
用户1执行如下命令：
root@ytt-ubuntu18:/home/ytt# mysql -uytt -e "select sleep(1000)"
用户2执行 ps aex 就可以打印出环境变量 MYSQL_PWD 和 MYSQL_TCP_PORT 的值：
root@ytt-ubuntu18:/home/ytt# ps aex| grep MYSQL_PWD| grep -v 'grep'7592 pts/0    S+     0:00 mysql -uytt -e select sleep(1000) LS_COLORS=rs=0:... MYSQL_PWD=root ...MYSQL_TCP_PORT=3340 ...
#### 4、屏蔽标准错误输出内容，重定向到空设备文件（推荐）
root@ytt-ubuntu18:/home/ytt# mysql -uytt -proot -P3340 -e"select version()"  2>/dev/null+-----------+| version() |+-----------+| 8.0.29    |+-----------+
这里利用 Linux 系统本身的特性来重定向 MySQL 错误信息，其中数字2代表错误输出的文件描述符；/dev/null 代表空设备。也就是说把执行这条命令的错误信息重定向到空设备而不是标准输出，这样就可以变相的把警告信息屏蔽掉。
#### 5、使用 mysql_config_edit 工具生成不同的 login_path （推荐）
mysql_config_edit 是 MySQL 官方发布的一款工具，专门处理这类必须暴露用户密码的问题，可以进行一次设置，多次安全使用。
使用方法如下：设置一个 login_path ，名字为 user_ytt ，密码按提示输入即可。
root@ytt-ubuntu18:/home/ytt# mysql_config_editor set -G user_ytt -S /var/run/mysqld/mysqld.sock -u ytt -pEnter password: 
接下来，调用任何 MySQL 命令行工具只需要带上 &#8211;login-path 选项即可使用。
root@ytt-ubuntu18:/home/ytt# mysql --login-path=user_ytt -e 'select user()'+---------------+| user()        |+---------------+| ytt@localhost |+---------------+   root@ytt-ubuntu18:/home/ytt# mysqladmin  --login-path=user_ytt pingmysqld is alive
mysql_config_editor 工具也有一个缺点：同样的 login_path 不能分享给所有系统用户，其他用户得重新添加自己的 login_path 才能正常使用。
#### 6、使用 Unix socket 插件（推荐，仅限本地）
auth_socket 插件只根据本地 OS 登录用户名和本地 linux socket 文件来授权认证。比如修改用户 ytt@localhost 插件为 auth_socket ：
mysql> alter user ytt@localhost identified with auth_socket ;
Query OK, 0 rows affected (0.00 sec)
mysql> \q
Bye
切换到 OS 用户 ytt ：
root@ytt-pc-big:/home/ytt# su ytt      ytt@ytt-pc-big:~$ mysql -e "select user(),current_user()"   +---------------+----------------+   | user()        | current_user() |   +---------------+----------------+   | ytt@localhost | ytt@localhost  |   +---------------+----------------+
#### 这里需要提醒一句： 为了安全，操作 MySQL 的用户权限一定要做到按需分配。