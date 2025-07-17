# 故障分析 | MySQL 管理端口登录异常排查及正确使用技巧

**原文链接**: https://opensource.actionsky.com/%e6%95%85%e9%9a%9c%e5%88%86%e6%9e%90-mysql-%e7%ae%a1%e7%90%86%e7%ab%af%e5%8f%a3%e7%99%bb%e5%bd%95%e5%bc%82%e5%b8%b8%e6%8e%92%e6%9f%a5%e5%8f%8a%e6%ad%a3%e7%a1%ae%e4%bd%bf%e7%94%a8%e6%8a%80%e5%b7%a7/
**分类**: MySQL 新特性
**发布时间**: 2023-07-04T00:51:13-08:00

---

本文主要记录了MySQL管理端口无法登录的排查过程，以及预防 too many connections 的一些建议。
> 作者：吕虎桥
爱可生DBA 团队成员，主要负责 DMP 平台和 MySQL 数据库的日常运维及故障处理。
本文来源：原创投稿
- 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# 背景描述
MySQL 8.0.14 版本中引入了 `admin_port` 参数，用于提供一个管理端口来处理 `too many connections` 报错。最近一套 MySQL 8.0 实例出现 `too many connections` 报错，尝试通过管理端口登录，但是仍然提示该报错。跟业务部门协商之后，调大了连接数，重启数据库恢复业务。为什么配置了 `admin_port` 却没有生效呢，带着疑问做了如下测试。
# 场景复现
## 管理端口相关参数
`--创建一个单独的 listener 线程来监听 admin 的连接请求
create_admin_listener_thread    = 1           
--监听地址
admin_address = localhost   
--监听端口，默认为 33062，也可以自定义端口
admin_port = 33062        
--配置好参数，重启数据库生效
systemctl restart mysqld_3306
--测试 root 账号是否可以通过 33062 端口登录
[root@mysql ~]# mysql -uroot -p -S /data/mysql/data/3306/mysqld.sock -P33062 -e 'select version()'
Enter password:
+-----------+
| version() |
+-----------+
| 8.0.33    |
+-----------+
`
## 模拟故障现象
调小 `max_connections` 参数，模拟出现 `too many connections` 报错。
`--更改 max_connections 参数为 1
mysql> set global max_connections = 1;
--模拟连接数被打满
[root@mysql ~]# mysql -uroot -p -S /data/mysql/data/3306/mysqld.sock -e 'select version()'
Enter password:
ERROR 1040 (HY000): Too many connections
--root 账号使用 33062 端口登录依然报错
[root@mysql ~]# mysql -uroot -p -S /data/mysql/data/3306/mysqld.sock -P33062 -e 'select version()'
Enter password:
ERROR 1040 (HY000): Too many connections
`
# 故障分析
## 疑问
为啥连接数没打满的情况下，`root` 账号可以通过 33062 端口登录？
`[root@mysql ~]# mysql -uroot -p -S /data/mysql/data/3306/mysqld.sock -P33062
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 16
Server version: 8.0.33 MySQL Community Server - GPL
Copyright (c) 2000, 2023, Oracle and/or its affiliates.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> \s
--------------
mysql  Ver 8.0.33 for Linux on x86_64 (MySQL Community Server - GPL)
Connection id:          16
Current database:
Current user:           root@localhost
SSL:                    Not in use
Current pager:          stdout
Using outfile:          ''
Using delimiter:        ;
Server version:         8.0.33 MySQL Community Server - GPL
Protocol version:       10
Connection:             Localhost via UNIX socket            --使用的socket连接
Server characterset:    utf8mb4
Db     characterset:    utf8mb4
Client characterset:    utf8mb4
Conn.  characterset:    utf8mb4
UNIX socket:            /data/mysql/data/3306/mysqld.sock
Binary data as:         Hexadecimal
Uptime:                 1 hour 6 min 54 sec
Threads: 3  Questions: 25  Slow queries: 0  Opens: 142  Flush tables: 3  Open tables: 74  Queries per second avg: 0.006
`
socket 连接会忽略指定的端口，即便是指定一个不存在的端口也是可以登录的，也就是说 socket 连接并没有通过管理端口登录，所以在连接数打满的情况下，使用 socket 登录依然会报错。
`[root@mysql ~]# netstat -nlp |grep 33063
[root@mysql ~]# mysql -uroot -p -S /data/mysql/data/3306/mysqld.sock -P33063 -e 'select version()'
Enter password:
+-----------+
| version() |
+-----------+
| 8.0.33    |
+-----------+
`
## 登录地址
`netstat` 查看 33062 端口是监听在 `127.0.0.1`，并不是参数里边配置的 `localhost`。
`[root@mysql ~]# netstat -nlp |grep 33062
tcp        0      0 127.0.0.1:33062         0.0.0.0:*               LISTEN      2204/mysqld
`
查看 MySQL 官方文档发现 `admin_address` 支持设置为 **IPv4**、**IPv6** 或者 **hostname**。如果该值是主机名，则服务器将该名称解析为 IP 地址并绑定到该地址。如果一个主机名可以解析多个 IP 地址，如果有 IPv4 地址，服务器使用第一个 IPv4 地址，否则使用第一个 IPv6 地址，所以这里把 `localhost` 解析为了 `127.0.0.1`。
> If admin_address is specified, its value must satisfy these requirements:
- The value must be a single IPv4 address, IPv6 address, or host name.
- The value cannot specify a wildcard address format (*, 0.0.0.0, or ::).
- As of MySQL 8.0.22, the value may include a network namespace specifier.
An IP address can be specified as an IPv4 or IPv6 address. If the value is a host name, the server resolves the name to an IP address and binds to that address. If a host name resolves to multiple IP addresses, the server uses the first IPv4 address if there are any, or the first IPv6 address otherwise.
指定 `admin_address` 为主机名，测试效果。
`--修改 admin_address 值为主机名 mysql
vim /data/mysql/etc/3306/my.cnf
admin_address                               = mysql
--hosts 配置
[root@mysql ~]# grep -i mysql /etc/hosts
192.168.100.82 mysql
--重启数据库
systemctl restart mysql_3306
--查看管理端口监听的地址，监听地址变更为主机名 mysql 对应的IP地址
[root@mysql ~]# netstat -nlp |grep 33062
tcp        0      0 192.168.100.82:33062    0.0.0.0:*               LISTEN      1790/mysqld
`
## 再次尝试
尝试使用 `127.0.0.1` 地址登录。
`--root 账号无法通过 127.0.0.1 地址登录，因为没有授权 root 账号从 127.0.0.1 地址登录
[root@mysql ~]# mysql -uroot -p -h127.0.0.1 -P33062 -e 'select version()'                                  
Enter password:
ERROR 1130 (HY000): Host '127.0.0.1' is not allowed to connect to this MySQL server
--默认 root 账号只允许从 localhost 登录
mysql> select user,host from mysql.user where user='root';
+------+-----------+
| user | host      |
+------+-----------+
| root | localhost |
+------+-----------+
`
# 故障解决
设置 `admin_address` 为 `127.0.0.1`，并添加管理账号。
```
--创建一个单独的 listener 线程来监听 admin 的里连接请求
create_admin_listener_thread = 1
--监听地址，建议设置为一个固定的 IP 地址
admin_address = 127.0.0.1    
--监听端口，默认为 33062，也可以自定义端口
admin_port = 33062 
--新建管理账号
create user root@'127.0.0.1' identified by 'xxxxxxxxx';
grant all on *.* to root@'127.0.0.1' with grant option;
flush privileges;
--测试登陆成功
[root@mysql ~]# mysql -uroot -p -h127.0.0.1 -P33062 -e 'select version()'
Enter password:
+-----------+
| version() |
+-----------+
| 8.0.33    |
+-----------+
```
# MySQL 管理端口配置总结
- 通过 `admin_address` 设置为固定的 IP 地址，例如 `127.0.0.1`，避免设置为 `hostname` 引起的不确定因素。
- MySQL 部署好之后，新建可以通过 `admin_address` 地址登录的管理员账号，例如 `root@'127.0.0.1'`。
# 一些优化建议
- 最小化权限配置，除管理员之外其他账号一律不允许配置 `super` 或者 `service_connection_admin` 权限。
- 应用端（Tomcat、JBoss 、Wildfly 等）配置数据源连接池，声明 `initialSize`、`maxActive` 属性值，控制连接数的无限增长。
- 及时优化 SQL，防止因性能问题引起的并发操作导致数据库连接数打满。