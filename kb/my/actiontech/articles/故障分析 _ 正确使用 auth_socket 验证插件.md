# 故障分析 | 正确使用 auth_socket 验证插件

**原文链接**: https://opensource.actionsky.com/20201123-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-11-23T00:42:07-08:00

---

作者：姚远
专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6，5.7，8.0 OCP。现在鼎甲科技任技术顾问，为同事和客户提供数据库培训和技术支持服务。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**现象**
v一线的工程师反映了一个奇怪的现象，刚刚从 MySQL 官网上下载了一个 MySQL 5.7.31。安装完成后，发现使用任何密码都能登陆 MySQL，修改密码也不管用，重新启动 MySQL 也不能解决。
**分析**
怀疑使用了 **&#8211;skip-grant-tables** 使用 **mysqld &#8211;print-defaults** 检查，没有发现。
检查登陆用户，都是 root@localhost，说明和 proxy user 没有关系。- 
- 
- 
- 
- 
- 
- 
`mysql> select user(),current_user();``+----------------+----------------+``| user()         | current_user() |``+----------------+----------------+``| root@localhost | root@localhost |``+----------------+----------------+``1 row in set (0.01 sec)`
使用 **mysql  &#8211;print-defaults** 检查客户端是否设置默认的用户和密码，没有发现。
检查数据库中的用户和密码的相关字段：- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
`mysql> select user,host,authentication_string from mysql.user;``+------------------+-----------+------------------------------------------------------------------------+``| user             | host      | authentication_string                                                  |``+------------------+-----------+------------------------------------------------------------------------+``| lisi             | %         | *52BCD17AD903BEC378139B11966C9B91AC4DED7C |``| mysql.session    | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |``| mysql.sys        | localhost | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |``| root             | localhost | *1840214DE27E4E262F5D981E13317691BA886B76 |``+------------------+-----------+------------------------------------------------------------------------+``5 rows in set (0.01 sec)`
现一切都正常，再检查 plugin 字段，发现只有 root 用户是 auth_socket ，其它的用户都是 mysql_native_password，问题可能就出在这儿。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
mysql> select user,host,plugin  from mysql.user;`+------------------+-----------+-----------------------+``| user             | host      | plugin                |``+------------------+-----------+-----------------------+``| lisi             | %         | mysql_native_password |``| mysql.session    | localhost | mysql_native_password |``| mysql.sys        | localhost | mysql_native_password |``| root             | localhost | auth_socket           |``+------------------+-----------+-----------------------+``5 rows in set (0.02 sec)
```
**问题解决**
对 auth_socket 验证插件不了解，感觉是这个插件不安全，使用下面的命令修改后，问题解决：- 
update user set plugin="mysql_native_password" where user='root';`
**auth_socket 验证插件的使用场景**
问题解决后，又仔细研究了一下  auth_socket 这个插件，发现这种验证方式有以下特点：- 首先，这种验证方式不要求输入密码，即使输入了密码也不验证。这个特点让很多人觉得很不安全，实际仔细研究一下这种方式，发现还是相当安全的，因为它有另外两个限制；
- 只能用 UNIX 的 socket 方式登陆，这就保证了只能本地登陆，用户在使用这种登陆方式时已经通过了操作系统的安全验证；
- 操作系统的用户和 MySQL 数据库的用户名必须一致，例如你要登陆  MySQL 的 root 用户，必须用操作系统的 root 用户登陆。
auth_socket 这个插件因为有这些特点，它很适合我们在系统投产前进行安装调试的时候使用，而且也有相当的安全性，因为系统投产前通常经常同时使用操作系统的 root 用户和 MySQL 的 root 用户。当我们在系统投产后，操作系统的 root 用户和 MySQL 的 root 用户就不能随便使用了，这时可以换成其它的验证方式，可以使用下面的命令进行切换：- 
`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'test';`
相关推荐：
[技术分享 | 客户端连接 MySQL 失败故障排除](https://opensource.actionsky.com/20201116-mysql/)
技[术分享 | MySQL 启动失败的常见原因](https://opensource.actionsky.com/20201109-mysql/)
[技术分享 | 使用 Python 解析并“篡改”MySQL 的 Binlog](https://opensource.actionsky.com/20201027-mysql/)