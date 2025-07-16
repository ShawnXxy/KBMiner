# MySQL · 答疑解惑 · mysqldump tips 两则

**Date:** 2016/02
**Source:** http://mysql.taobao.org/monthly/2016/02/10/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2016 / 02
 ](/monthly/2016/02)

 * 当期文章

 MySQL · 引擎特性 · InnoDB 文件系统之文件物理结构
* MySQL · 引擎特性 · InnoDB 文件系统之IO系统和内存管理
* MySQL · 特性分析 · InnoDB transaction history
* PgSQL · 会议见闻 · PgConf.Russia 2016 大会总结
* PgSQL · 答疑解惑 · PostgreSQL 9.6 并行查询实现分析
* MySQL · TokuDB · TokuDB之黑科技工具
* PgSQL · 性能优化 · PostgreSQL TPC-C极限优化玩法
* MariaDB · 版本特性 · MariaDB 的 GTID 介绍
* MySQL · 特性分析 · 线程池
* MySQL · 答疑解惑 · mysqldump tips 两则

 ## MySQL · 答疑解惑 · mysqldump tips 两则 
 Author: 丁奇 

 ## 背景

用户在使用mysqldump导数据上云的时候碰到两个“诡异”的问题，简单分析分享下。

## TIP 1 --port端口无效?

本地有3306和3307两个端口的实例，执行命令为:

`mysqldump --host=localhost --port=300x -Ddb1 db1 -r outputfile
`

发现无论执行端口写入3306还是3307，导出的都是3306端口实例的数据。

## 代码分析

实际上不论是mysqldump还是mysql客户端，在连接数据库时都调用了 `CLI_MYSQL_REAL_CONNECT` 这个函数，里面的一段代码逻辑如下

`if(!host || !strcmp(host,LOCAL_HOST)
{
 vio_socket_connect(...
}
其中 #define LOCAL_HOST "localhost"
`

也就是说，当host参数值为localhost的时候，mysql和mysqldump客户端使用的是–socket参数，如果未指定，则使用默认的/tmp/mysql.sock。
因此上面用户的输入，不论–port 输入多少，都被忽略。而他的/tmp/mysql.sock 就是属于3306端口实例。

从代码中可以看到，必须是全小写的localhost才满足条件，若是Localhost，则解析成127.0.0.1，用的是 ip + port 的模式，此时 –socket 参数无效。

## TIP 2 导出的数据无法导入？

使用mysqldump默认参数导出5.6 的数据，无法导入到目标库。

当源库使用了GTID模式时，在dump出来的文件中为了保持目标库和源库GTID值相同，增加了两个语句, `SET @@SESSION.SQL_LOG_BIN= 0` 和 `SET @@GLOBAL.GTID_PURGED='xxxx'`。

而实际上增加这两个语句会有诸多问题：

1. 关闭binlog首先需要super权限，如果目标库只能使用普通账号，则会导致执行失败；
2. 即使有super权限，也会导致这些操作不记录到binlog，会导致主备不一致。当然也可以说，这就要求同一份dump要restore到目标库的主库和所有备库才能保持主备一致；
3. `SET @@GLOBAL.GTID_PURGED='xxxx'`这个命令要求目标库的`gtid_executed`值是空。若非空，这个命令执行失败；
4. reset master可以清空`gtid_executed`值，也需要super权限。

因此在导出5.6的数据时，有两种可选方案：

1. 在有目标库的super权限时，用默认dump参数，在导入到目标库之前，先执行reset master；这样需要在主库和所有备库都执行相同个导入动作；
2. mysqldump需要增加参数 –set-gtid-purged=off，这样不会生成上述两个语句，数据能够直接导入。但是目标库的gtid set就与源库不同。

需要根据业务需求选择。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)