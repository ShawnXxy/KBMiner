# 故障分析 | MySQL 8.0 解决连接满问题

**原文链接**: https://opensource.actionsky.com/20210811-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-08-10T21:45:18-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
恰好前些日子和一客户讨论 MySQL 连接数满的问题：**ERROR 1040 (HY000): Too many connections**
##### 从实践意义来讲，连接数满属于老问题， 此问题产生的原因可能有以下几种：
###### 1. 应用端不习惯受限制的用户权限，沉迷于使用 ALL 权限用户。
###### 2. DBA 为了省事儿，建立多个 ALL 权限用户，分配给开发、运维等。
###### 3. MySQL 数据库服务端没有使用连接池（类似 MySQL 企业版连接池插件），越来越多的数据库请求堆积导致连接满。
###### 4. 应用端和 MySQL 端之间也没有部署连接池，用直连 MySQL 的方式处理日常业务，进而数据库请求过多导致连接满。
###### 5. MySQL 参数 max_connections 设置不合理，与当前数据库请求存在较大偏差，导致连接不够用报错。
如果按照业务功能细分为不同权限的用户，只保留一个管理员用户，在这个问题暴露时管理员就可以使用预留连接进入数据库查看具体问题。MySQL 默认给管理员预留一个额外连接，用于处理连接满的场景；但是现实场景并非如此，大部分 MySQL 数据库都是所有业务模块共享一个管理员用户或者使用多个命名不同的具有管理员权限的用户。出问题后只能由 DBA 来调大 max_connections 值（在数据库服务器负载可控前提下）。
##### MySQL 8.0 自带的连接管理接口（administrative connection interface）可以帮DBA辅助解决这类问题。
###### 连接管理接口限制放开很多。老版本的连接预留只有一个，而连接管理则不限制连接数（硬件级别限制）。
**具体在 MySQL 8.0 里怎么用呢？ 全局设置以 admin 开头的变量：**
admin_address：连接管理接口监听IP地址或者域名，只可以设置单个值。
admin_port：连接管理接口监听端口，默认为33062，可以自己指定，不要超过65535即可。
admin_ssl开头、admin_tsl开头等都是设置安全连接相关，默认为空，可选配置。
create_admin_listener_thread：是否为连接管理接口创建一个单独监听线程，默认不创建。
**使用连接管理接口的前提条件是用户必须有 super 静态权限或者是 service_connection_admin 动态权限。**
**来看看连接管理接口具体该如何使用：**
确认参数都开启：
`localhost:(none)>select @@admin_address,@@admin_port,@@create_admin_listener_thread;
+-----------------+--------------+--------------------------------+
| @@admin_address | @@admin_port | @@create_admin_listener_thread |
+-----------------+--------------+--------------------------------+
| debian-ytt1     |        18027 |                              1 |
+-----------------+--------------+--------------------------------+
1 row in set (0.00 sec)
`
创建包含 service_connection_admin 权限的用户：
`localhost:(none)>create user ytt_admin;
Query OK, 0 rows affected (0.02 sec)
localhost:(none)>grant select, insert,update,delete,service_connection_admin on *.* to ytt_admin;
Query OK, 0 rows affected (0.02 sec)
`
为了突显效果，把 max_connections 改为最小值1，此时，MySQL 管理员可以申请的最大连接数为2，普通用户可以申请的最大连接数为1.
`localhost:(none)>select @@max_connections;
+-------------------+
| @@max_connections |
+-------------------+
|                 1 |
+-------------------+
1 row in set (0.00 sec)
`
新建立的用户 ytt_admin 虽然为普通用户，但是持有 service_connection_admin 权限，也可以享受当“副”管理员待遇，最多可以请求两个连接，当请求第三次连接时报错退出。
`root@debian-ytt1:~/sandboxes/msb_8_0_25# mysql -uytt_admin -P 8025 -h debian-ytt1 -e "select sleep(3600)" &
[1] 7474
root@debian-ytt1:~/sandboxes/msb_8_0_25# mysql -uytt_admin -P 8025 -h debian-ytt1 -e "select sleep(3600)" &
[2] 7475
root@debian-ytt1:~/sandboxes/msb_8_0_25# mysql -uytt_admin -P 8025 -h debian-ytt1 -e "select sleep(3600)" &
[3] 7477
root@debian-ytt1:~/sandboxes/msb_8_0_25# ERROR 1040 (HY000): Too many connections
[3]+  退出 1                mysql -uytt_admin -P 8025 -h debian-ytt1 -e "select sleep(3600)"
`
使用连接管理接口来连接：
`root@debian-ytt1:~/sandboxes/msb_8_0_25# mysql -h debian-ytt1 -uytt_admin -P 18027 -e "select sleep(3600)" &
[3] 8516
`
查看下当前已经连接到 MySQL 服务上的连接，依然使用连接管理接口：两个正常连接，两个额外连接
`root@debian-ytt1:~/sandboxes/msb_8_0_25# mysql -h debian-ytt1 -uytt_admin -P 18027 -e "show processlist;" -ss
8   ytt_admin   debian-ytt1:57946   NULL    Query   154 User sleep  select sleep(1000)
9   ytt_admin   debian-ytt1:57948   NULL    Query   148 User sleep  select sleep(3600)
13  ytt_admin   debian-ytt1:60718   NULL    Query   138 User sleep  select sleep(3600)
17  ytt_admin   debian-ytt1:60726   NULL    Query   0   init    show processlist
`
使用连接管理接口、以及老版本预留给管理员的额外连接功能有一个共同前提就是：这个连接必须能够建立成功。也就是得有建立这个连接所需的硬件资源，如果资源不足，MySQL 服务器会拒绝连接，比如可能会有这个错误：ERROR 2003 (HY000): Can&#8217;t connect to MySQL server on &#8216;&#8230;&#8217; (110)
虽然 MySQL 8.0 自带连接管理接口对连接满问题有一个很好的备选解决方案，但毕竟是在数据库端的一个临时解决方案。要想从根本上解决这个问题，得从请求进入数据库前就先做优化才好，毕竟数据库不是万能的。比如可以使用如下可能的方法来规避这个问题：
- 
用户权限明确划分，super 权限只能给管理员，其他的人员收回此权限。
- 
在请求进入数据库前进行限流，严格按照符合数据库的压测性能相关参数设置。
- 
优化业务 SQL 与表结构，做到性能尽量极致，不拖数据库后腿。
- 
数据库端拆库拆表，用分布式方案对大量请求进行分流。