# 技术分享 | 客户端连接 MySQL 失败故障排除

**原文链接**: https://opensource.actionsky.com/20201116-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-11-16T00:31:05-08:00

---

作者：姚远
专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6，5.7，8.0 OCP。现在鼎甲科技任技术顾问，为同事和客户提供数据库培训和技术支持服务。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
在 MySQL 的日常运维中，客户端连接 MySQL 失败的现象也很常见。对于这种情况，分下面的三类进行排查。
**一、mysqld 进程没有正常运行**
遇到这种情况首先到服务器上看看 mysqld 进程是否活着，采用的命令：- 
- 
- 
`mysqladmin ping ``或 ``ps -ef | grep mysqld`
**二、客户端不能和进程 mysqld 通信**
如果 MySQL 服务器上的 mysqld 进程运行正常，我们再看看客户端能不能和 mysqld 进行通信，使用下面的命令进行网络连通的测试：- 
`telnet localhost 3306`
如果本地能通，再到客户端的机器上把 localhost 换成  MySQL 服务器的 ip 地址进行测试。如果不能通，通常有两种原因，一种原因是 OS 或网络的问题，或者是防火墙；另一种原因是 mysqld 自身根本没有侦听客户端的连接请求， mysqld 启动后对于客户端的侦听是分三种情况。
第一种情况
是使用参数 **&#8211;skip-networking** 跳过侦听客户端的网络连接，用下面的命令我们可以看到  MySQL 根本没有侦听 3306 端口。- 
- 
`mysqld --no-defaults --console --user mysql  --skip-networking &``netstat -plunt|grep 3306`
第二种情况
使用参数 **&#8211;bind-address** 后面增加对客户端访问 IP 地址的限制，例如只侦听本地的连接：- 
- 
- 
- 
- 
- 
- 
- 
`mysqld --no-defaults --user mysql  --bind-address=127.0.0.1 &``netstat -plunt|grep 3306``tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      22767/mysqld        ``tcp6       0      0 :::33060                :::*                    LISTEN      22767/mysqld  ``mysqld --no-defaults --user mysql  --bind-address='192.168.17.40' &``netstat -plunt|grep 3306``tcp        0      0 192.168.17.40:3306      0.0.0.0:*               LISTEN      23053/mysqld        ``tcp6       0      0 :::33060                :::*                    LISTEN      23053/mysqld   `
第三种情况对客户端访问 IP 地址的不进行限制。- 
- 
- 
- 
```
mysqld --no-defaults --user mysql  &`netstat -plunt|grep 3306``tcp6       0      0 :::33060                :::*                    LISTEN      23582/mysqld        ``tcp6       0      0 :::3306                 :::*                    LISTEN      23582/mysqld
```
我们通过查看网络端口侦听的情况可以推测 mysqld 进程的参数设置。
**三、账户密码的问题**
最后一种情况是账户密码的问题，应付这种情况我们有个有力的工具就是查看 MySQL 的 error log， error log 记载信息的详细程度上由参数 **&#8211;log-error-verbosity** 进行控制的，这个参数的作用如下：
![](https://opensource.actionsky.com/wp-content/uploads/2020/11/yaoyuan表格.png)											
默认为 2，设置为 3 可以记录更多的信息，这个参数可以联机设置：- 
- 
mysql>  set global log_error_verbosity=3;``Query OK, 0 rows affected (0.00 sec)`
**当密码错误**
- 
- 
- 
`mysql -uroot -perrorpassword``mysql: [Warning] Using a password on the command line interface can be insecure.``ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)`在 MySQL 的 error log 里有这样的记录：- 
```
2020-11-03T07:59:40.720835Z 7 [Note] [MY-010926] [Server] Access denied for user 'root'@'localhost' (using password: YES)
```
看到这样的记录我们至少知道了客户端是连接上了 MySQL 的服务的。如果把参数 &#8211;log-error-verbosity 设置成的默认值 2 时是没有这个提示的，也就说没有 note 类型的信息。
**账户错误**
- 
`ERROR 1130 (HY000): Host '192.168.17.149' is not allowed to connect to this MySQL server`注意账户错误时，提示是 “is not allowed to connect to this MySQL server”，而密码错误时是 “Access denied for user”。MySQL 中的一个账户是由 user 和 host 两个部分组成，在 MySQL 中有个 mysql 数据库，里面有个 user 表，表中 Host 和 User 为两个主键列（primary key），唯一表示一个用户。像这种情况通常是 host 字段部分是 localhost，把它改成通配符 &#8220;%&#8221; 即可。
相关推荐：
[技术分享 | MySQL 启动失败的常见原因](https://opensource.actionsky.com/20201109-mysql/)
[技术分享 | 使用 Python 解析并“篡改”MySQL 的 Binlog](https://opensource.actionsky.com/20201027-mysql/)
[技术分享 | MySQL 使用 MariaDB 审计插件](https://opensource.actionsky.com/20200908-mysql/)