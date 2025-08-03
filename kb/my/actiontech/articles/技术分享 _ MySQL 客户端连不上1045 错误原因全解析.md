# 技术分享 | MySQL 客户端连不上（1045 错误）原因全解析

**原文链接**: https://opensource.actionsky.com/20190715-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-07-15T00:42:02-08:00

---

> 
作者：Carlos Tutte、Marcos Albe
翻译：管长龙
在我们学习 MySQL 或从事 MySQL DBA 工作期间，时常会遇到：“我尝试连接到 MySQL 并且收到1045 错误，但我确定我的用户和密码都没问题”。
不管你现在是否是高手还是高高手，都不可避免曾经在初学的时候犯过一些很初级的错误，例如：用户名密码都填错了。而且工作一段时间后也偶尔会遇到一些不常见错误原因。
## 一、连接错误的主机
- `[root@localhost ~]# mysql -u root -p123456`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)`
如果未指定要连接的主机（使用 -h 标志），则 MySQL 客户端将尝试连接到 localhost 实例，同时您可能尝试连接到另一个主机端口实例。
**修复**：仔细检查您是否尝试连接到 localhost，或者确保指定主机和端口（如果它不是 localhost）：
- `[root@localhost ~]# mysql -u root -p123456 -h <IP> -P 3306`
## 二、用户不存在
- `[root@localhost ~]# mysql -u nonexistant -p123456 -h localhost`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `ERROR 1045 (28000): Access denied for user 'nonexistant'@'localhost' (using password: YES)`
**修复**：仔细检查用户是否存在：
- `mysql> SELECT User FROM mysql.user WHERE User='nonexistant';`
- `Empty set (0.00 sec)`
如果用户不存在，请创建一个新用户：
- `mysql> CREATE USER 'nonexistant'@'localhost' IDENTIFIED BY 'sekret';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> FLUSH PRIVILEGES;`
- `Query OK, 0 rows affected (0.01 sec)`
## 三、用户存在但客户端主机无权连接
- `[root@localhost ~]# mysql -u nonexistant -p123456`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `ERROR 1045 (28000): Access denied for user 'nonexistant'@'localhost' (using password: YES)`
**修复**：您可以通过以下查询检查 MySQL 允许连接的主机用户/主机：
- `mysql> SELECT Host, User FROM mysql.user WHERE User='nonexistant';`
- `+-------------+-------------+`
- `| Host        | User        |`
- `+-------------+-------------+`
- `| 192.168.0.1 | nonexistant |`
- `+-------------+-------------+`
- `1 row in set (0.00 sec)`
如果需要检查客户端连接的 IP，可以使用以下 Linux 命令来获取服务器 IP：
- `[root@localhost ~]# ip address | grep inet | grep -v inet6`
- `    inet 127.0.0.1/8 scope host lo`
- `    inet 192.168.0.20/24 brd 192.168.0.255 scope global dynamic wlp58s0`
或公共IP：
- `[root@localhost ~]# dig +short myip.opendns.com @resolver1.opendns.com`
- `177.128.214.181`
然后，您可以创建具有正确主机（客户端 IP）的用户，或使用&#8217;％&#8217;（通配符）来匹配任何可能的 IP：
- `mysql> CREATE USER 'nonexistant'@'%' IDENTIFIED BY '123456';`
- `Query OK, 0 rows affected (0.00 sec)`
## 四、密码错误，或者用户忘记密码
- `mysql> CREATE USER 'nonexistant'@'%' IDENTIFIED BY '123456';`
- `Query OK, 0 rows affected (0.00 sec)`
**修复**：检查和/或重置密码：
您无法从 MySQL 以纯文本格式读取用户密码，因为密码哈希用于身份验证，但您可以将哈希字符串与“PASSWORD”函数进行比较：
- `mysql> SELECT Host, User, authentication_string, PASSWORD('forgotten') FROM mysql.user WHERE User='nonexistant';`
- `+-------------+-------------+-------------------------------------------+-------------------------------------------+`
- `| Host        | User        | authentication_string                     | PASSWORD('forgotten')                     |`
- `+-------------+-------------+-------------------------------------------+-------------------------------------------+`
- `| 192.168.0.1 | nonexistant | *AF9E01EA8519CE58E3739F4034EFD3D6B4CA6324 | *70F9DD10B4688C7F12E8ED6C26C6ABBD9D9C7A41 |`
- `| %           | nonexistant | *AF9E01EA8519CE58E3739F4034EFD3D6B4CA6324 | *70F9DD10B4688C7F12E8ED6C26C6ABBD9D9C7A41 |`
- `+-------------+-------------+-------------------------------------------+-------------------------------------------+`
- `2 rows in set, 1 warning (0.00 sec)`
我们可以看到 PASSWORD（&#8217;forgotten&#8217;）哈希与 authentication_string 列不匹配，这意味着 password string =&#8217;forgotten&#8217; 不是正确的登录密码。
如果您需要覆盖密码，可以执行以下查询：
- `mysql> set password for 'nonexistant'@'%' = 'hello$!world';`
- `Empty set (0.00 sec)`
## 五、Bash 转换密码中的特殊字符
- `[root@localhost ~]# mysql -u nonexistant -phello$!world`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `ERROR 1045 (28000): Access denied for user 'nonexistant'@'localhost' (using password: YES)`
**修复**：通过在单引号中包装密码来防止 bash 解释特殊字符：
- `[root@localhost ~]# mysql -u nonexistant -p'hello$!world'`
- `mysql: [Warning] Using a password on the command line interface can be insecure`
- `...`
- `mysql>`
## 六、SSL 是必须的，但客户没有使用
- `mysql> create user 'ssluser'@'%' identified by '123456';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> alter user 'ssluser'@'%' require ssl;`
- `Query OK, 0 rows affected (0.00 sec)`
- `...`
- `[root@localhost ~]# mysql -u ssluser -p123456`
- `mysql: [Warning] Using a password on the command line interface can be insecure.`
- `ERROR 1045 (28000): Access denied for user 'ssluser'@'localhost' (using password: YES)`
**修复**：添加 -ssl-mode 标志（-ssl 标志已弃用但也可以使用）
[https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-11.html]
- `[root@localhost ~]# mysql -u ssluser -p123456 --ssl-mode=REQUIRED`
- `...`
- `mysql>`
**最后**，如果您真的被锁定并需要绕过身份验证机制以重新获得对数据库的访问权限，请执行以下几个简单步骤：
- 停止实例
- 编辑 my.cnf 并在 [mysqld] 下添加 skip-grant-tables（这样可以在不提示输入密码的情况下访问 MySQL）。在 MySQL 8.0 上，跳过网络是自动启用的（只允许从 localhost 访问 MySQL），但对于以前的 MySQL 版本，建议在 [mysqld] 下添加 -skip-networking
- 启动实例
- 使用 root 用户访问（mysql -uroot -hlocalhost）;
- 发出必要的 GRANT / CREATE USER / SET PASSWORD 以纠正问题（可能设置一个已知的 root 密码将是正确的事情：SET PASSWORD FOR &#8216;root&#8217;@&#8217;localhost&#8217;=&#8217;S0vrySekr3t&#8217;
- 停止实例
- 编辑 my.cnf 并删除 skip-grant-tables 和 skip-networking
- 再次启动 MySQL
- 您应该能够使用 roothost 从 root 用户登录，并对 root 用户执行任何其他必要的纠正操作。
本文按常见到复杂的顺序将可能报 1045 的错误原因全部列举出来，看完了还不赶快收藏！
> 参考：https://www.percona.com/blog/2019/07/05/fixing-a-mysql-1045-error/
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)