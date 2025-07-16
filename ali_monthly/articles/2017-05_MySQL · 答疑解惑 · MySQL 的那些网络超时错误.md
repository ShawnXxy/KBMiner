# MySQL · 答疑解惑 · MySQL 的那些网络超时错误

**Date:** 2017/05
**Source:** http://mysql.taobao.org/monthly/2017/05/04/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2017 / 05
 ](/monthly/2017/05)

 * 当期文章

 MySQL · 引擎特性 · InnoDB Buffer Pool
* AliSQL · 特性介绍 · 动态加字段
* PgSQL · 特性分析 · 数据库崩溃恢复（上）
* MySQL · 答疑解惑 · MySQL 的那些网络超时错误
* HybridDB · 最佳实践 · HybridDB 数据合并的方法与原理
* MSSQL · 应用案例 · 构建死锁自动收集系统
* PostgreSQL · 实现分析 · PostgreSQL 10.0 并行查询和外部表的结合
* RocksDB · 特性介绍 · HashLinkList 内存表
* MySQL · myrocks · fast data load
* PgSQL · 应用案例 · "写入、共享、存储、计算" 最佳实践

 ## MySQL · 答疑解惑 · MySQL 的那些网络超时错误 
 Author: xiangluo 

 ## 前言

我们在使用/运维 MySQL 过程中，经常会遇到一些网络相关的错误，比如：

`Aborted connection 134328328 to db: 'test' user: 'root' host: '127.0.0.1' (Got timeout reading communication packets)
`

MySQL 的网络超时相关参数有好几个，这个超时到底是对应哪个参数呢？

在之前的月报中，我们介绍过 MySQL 的 [网络通信模块](http://mysql.taobao.org/monthly/2016/07/04/) ，包括各模块间的关系，数据网络包是如何发送接受的，以及结果集的数据格式，大家可以先回顾下。

这里我们对 mysqld 处理网络包时，遇到的超时异常情况进行分析，希望大家在遇到网络相关的报错时，能更好理解和排查问题。

## 问题分析

MySQL 是平等网络协议，就是说 client 和 server 之间的网络交互是一来一回的，client 发送完请求后，必须等待 server 响应包回来，才能发下一个请求。
对 mysqld 来说，就是接收网络请求，然后内部处理，将结果集返回给客户端，然后等待下一个请求：

先看下 mysqld server 和网络超时相关的参数有哪些：

* interactive_timeout
* wait_timeout
* net_read_timeout
* net_write_timeout
* connect_timeout

在底层实现上，不管是读还是写操作，超时都是通过 `poll(&pfd, 1, timeout)` 做的，参数之间的区别是针对连接的不同状态。

**读超时**

wait_timeout 是给读请求用的，在 `do_command` 开始就做设置:

`my_net_set_read_timeout(net, thd->variables.net_wait_timeout);
`

这个时候，连接是空闲的，等待用户的请求。

等读完用户的请求包后，连接就变成 active 的，在调用 `dispatch_command` 执行 SQL 前，通过

`my_net_set_read_timeout(net, thd->variables.net_read_timeout);
`

把超时设置回 `net_read_timeout`，之后在执行 SQL 请求过程中，server 和 client 基本不会有网络交互，所以这个超时基本用不上。

有一个特殊的情况是 `LOAD DATA LOCAL FILE` 命令，server 在执行过程中，需要和 client 再做网络交互。

interactive_timeout 是给交互模式的客户端使用的，比如我们常用的 mysql client 工具，这个是在认证过程中设置的，逻辑如下：

`static void
server_mpvio_update_thd(THD *thd, MPVIO_EXT *mpvio)
{
 thd->client_capabilities= mpvio->client_capabilities;
 thd->max_client_packet_length= mpvio->max_client_packet_length;
 if (mpvio->client_capabilities & CLIENT_INTERACTIVE)
 thd->variables.net_wait_timeout= thd->variables.net_interactive_timeout;
 thd->security_ctx->user= mpvio->auth_info.user_name;
 if (thd->client_capabilities & CLIENT_IGNORE_SPACE)
 thd->variables.sql_mode|= MODE_IGNORE_SPACE;
}
`

如果客户端的能力位上设置了 CLIENT_INTERACTIVE，会用 `interactive_timeout` 的值覆盖 `wait_timeout` 的值。
而一般情况下，我们应用在建立连接时，是不会设置这个能力位的。

**写超时**
`net_write_timeout` 对应写超时，在连接认证完成后，server 和 client 交互过程中写超时一真是不变的。

**认证超时**

`connect_timeout` 是给连接认证过程用的，读和写都用这个值，认证完成后，读和写分别设置为 `net_read_timeout` 和 `net_write_timeout`。

## 总结

可以看到和读相关的超时参数是最多的，也比较容易搞混乱。

1. 如果是认证过程中超时，不管是读还是，都是 connect_timeout；
2. 对于读网络超时，一般是 wait_timeout/interactive_timeout，基本不会是 net_read_timeout（特例是业务用到 LOAD DATA LOCAL FILE）；
3. 对于写网络超时，都是 net_write_timeout。

在遇到超时情况下，可以根据这些原则判断对那个参数做调整。

比如下面这种情况：

`2017-05-15 19:32:41 47930 [Warning] Aborted connection 6 to db: 'unconnected' user: 'root' host: 'localhost' (Got timeout reading communication packets)
`

很可能需要调整的 wait_timeout/interactive_timeout。

`2017-05-15 20:06:27 5063 [Warning] Aborted connection 12 to db: 'test' user: 'root' host: 'localhost' (Got timeout writing communication packets)
`

需要调整 net_write_timeout

需要注意的是，MySQL 的关于网络的错误，除了超时以外都认为是 error，没有做进一步的细分，比如可能会看到下面这种日志，有可能是客户端异常退出了，也有可能是网络链路异常。

```
2017-05-15 19:34:57 47930 [Warning] Aborted connection 8 to db: 'unconnected' user: 'root' host: 'localhost' (Got an error reading communication packets)

2017-05-15 20:07:39 5063 [Warning] Aborted connection 13 to db: 'test' user: 'root' host: 'localhost' (Got an error writing communication packets)

```

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)