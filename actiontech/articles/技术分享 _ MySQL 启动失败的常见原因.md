# 技术分享 | MySQL 启动失败的常见原因

**原文链接**: https://opensource.actionsky.com/20201109-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-11-09T01:21:13-08:00

---

作者：姚远
专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6，5.7，8.0 OCP。现在鼎甲科技任技术顾问，为同事和客户提供数据库培训和技术支持服务。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
MySQL 启动失败的最常见的原因有两类，分别是无法访问系统资源和参数设置错误造成的，下面分别分析如下。
**一、无法访问系统资源**
MySQL 不能访问启动需要的资源是造成而 MySQL 无法启动的一个常见原因，如：文件，端口等。由于 linux 中用于启动 mysqld 进程的 mysql 用户通常是不能登陆的，可以使用类似下面的命令检查文件的访问权限。
- 
`sudo -u mysql touch /var/lib/mysql/b`
找出问题后，修改对应文件或目录的权限或属主后通常可以解决问题。但有时 mysql 用户有访问文件和目录的权限，但仍然会被拒绝访问，例如下面这个例子：
- 
- 
- 
- 
- 
`mysql> system sudo -u mysql touch  /home/mysql/data/a``mysql> create table t1 (``    id int primary key,n varchar(10``    ) data directory``ERROR 1030 (HY000): Got error 168 from storage engine`
测试说明 mysql 用户有这个目录的访问权限，但创建文件还是失败，这种情况让很多人困惑，这个时候通常是 mysqld 进程的访问被 linux 的 selinux 或 apparmor 给阻止了，大家可以看到创建的表不是在 mysql 的默认目录下面，因此 selinux 或 apparmor 的 policy 里面没有包含这个目录的访问权限，此时只要对应的修改 policy 就行了，当然把  selinux 或 apparmor 停了也行。
有时虽然对系统资源有访问的权限，但系统资源已经被占用：
- 
- 
- 
`mysqld --no-defaults --console --user mysql``2020-11-03T03:36:07.519419Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.19) starting as process 21171``2020-11-03T03:36:07.740347Z 1 [ERROR] [MY-012574] [InnoDB] Unable to lock ./ibdata1 error: 11`这个故障产生的原因是另外一个 mysqld 进程已经启动并占用了对应的文件。
**二、参数设置错误**
参数设置错误造成 MySQL 无法启动的原因也非常常见，此时先要检查 MySQL 启动时会调用的参数，下面的命令可以查询 MySQL 启动时调用参数文件的顺序：
- 
- 
- 
`$ mysqld --verbose --help | grep "Default options "  -A 1``Default options are read from the following files in the given order:``/etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf`
知道了 MySQL 参数文件的调用顺序，我们就可以检查对应的参数文件，找出其中的错误，如果觉得参数文件的可读性不强，可以使用下面的命令显示 mysqld 程序将要调用的参数：
- 
- 
- 
`$ mysqld --print-defaults``/usr/sbin/mysqld would have been started with the following arguments:``......`
注意这个命令显示完参数后就退出，不会真正运行 mysqld。这个命令和 my_print_defaults mysqld 完全是等价的，只不过后者的显示方式是一行一个参数。
然后开始对可疑的参数进行调试，我个人喜欢加的参数和顺序如下：
1. 在 mysqld 后加上第一个参数 &#8211;no-defaults ，这个参数的作用是通知 mysqld 在启动的时候不要读任何参数文件；
2. 第二个参数是 &#8211;console，这个参数会把错误信息输出到屏幕上，这个参数带来的一个弊端是所有的信息都输出到屏幕上，让屏幕显得比较乱，但对于我们调试却是很方便的；
3. 第三个参数是 &#8211;log-error-verbosity=3，这个参数会显示详细的日志；
4. 然后再在后面加上有把握的参数，可以一次只加一个参数，然后启动 mysqld，采用排除法逐步找出错误的参数。
看这个例子：
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysqld --no-defaults --console  --log-error-verbosity=3 --user mysql --gtid_mode=on``2020-11-03T07:14:20.384223Z 0 [Note] [MY-010949] [Server] Basedir set to /usr/.``2020-11-03T07:14:20.384254Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.19) starting as process 22617``2020-11-03T07:14:20.400221Z 0 [Note] [MY-012366] [InnoDB] Using Linux native AIO``……``2020-11-03T07:14:21.632851Z 0 [ERROR] [MY-010912] [Server] GTID_MODE = ON requires ENFORCE_GTID_CONSISTENCY = ON.``2020-11-03T07:14:21.634183Z 0 [ERROR] [MY-010119] [Server] Aborting``……``2020-11-03T07:14:23.026551Z 0 [System] [MY-010910] [Server] /usr/sbin/mysqld: Shutdown complete (mysqld 8.0.19)  MySQL Community Server - GPL.``root@scutech:~#`
看这个例子，我们很容易知道是需要我们同时设置参数 GTID_MODE 和 ENFORCE_GTID_CONSISTENCY 同时为 on 才行。
相关推荐：
[技术分享 | 使用 Python 解析并“篡改”MySQL 的 Binlog](https://opensource.actionsky.com/20201027-mysql/)
[技术分享 | MySQL 使用 MariaDB 审计插件](https://opensource.actionsky.com/20200908-mysql/)
[技术分享 | 只有.frm和.ibd文件时如何批量恢复InnoDB的表](https://opensource.actionsky.com/20200718-mysql/)