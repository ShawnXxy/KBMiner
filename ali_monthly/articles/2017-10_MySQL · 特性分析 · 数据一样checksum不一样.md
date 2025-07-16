# MySQL · 特性分析 · 数据一样checksum不一样

**Date:** 2017/10
**Source:** http://mysql.taobao.org/monthly/2017/10/08/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2017 / 10
 ](/monthly/2017/10)

 * 当期文章

 PgSQL · 特性分析 · MVCC机制浅析
* MySQL · 性能优化· CloudDBA SQL优化建议之统计信息获取
* MySQL · 引擎特性 · InnoDB mini transation
* MySQL · 特性介绍 · 一些流行引擎存储格式简介
* MSSQL · 架构分析 · 从SQL Server 2017发布看SQL Server架构的演变
* MySQL · 引擎介绍 · Sphinx源码剖析(三)
* PgSQL · 内核开发 · 如何管理你的 PostgreSQL 插件
* MySQL · 特性分析 · 数据一样checksum不一样
* PgSQL · 应用案例 · 经营、销售分析系统DB设计之共享充电宝
* MySQL · 捉虫动态 · 信号处理机制分析

 ## MySQL · 特性分析 · 数据一样checksum不一样 
 Author: 凌洛 

 ## 背景
有一个特殊环境需要进行人肉迁移数据，对比了表里的数据一模一样，但是无论如何checksum就是不一致，那么问题出在哪里呢？

## 问题排查

### 数据是否一致

眼睛都把屏幕盯穿了，也没发现不一致的数据。

### 导出数据的方式

![image](https://private-alipayobjects.alipay.com/alipay-rmsdeploy-image/skylark/png/5e503121-3a29-4eaf-9e6c-734c44cfa189.png)
checksum还是不一致，所以这个原因排除。

### MySQL版本

嗯，这个确实不一样，源端是5.5，目的端是5.6，但是这个是checksum函数不一样吗？还是表的结构变了？咨询了内核的同学，说checksum的源代码没变啊，接下来那应该是表结构变了？通过查手册发现：

`The checksum value depends on the table row format. If the row format changes, the 
checksum also changes. For example, the storage format for temporal types such as 
TIME, DATETIME, and TIMESTAMP changes in MySQL 5.6 prior to MySQL 5.6.5, so if a 
5.5 table is upgraded to MySQL 5.6, the checksum value may change.
`
既然这样了，那我们就来验证下是不是因为datetime的问题。
![image](https://private-alipayobjects.alipay.com/alipay-rmsdeploy-image/skylark/png/0f4f9562-e5ad-446b-bac7-7c8c489a2e25.png)
嗯，确实是datetime的格式导致的。

## 总结
这个问题总结来说是因为MySQL5.5和5.6的时间存储格式有变化，导致了checksum不一样。

这个问题知道原因后觉得非常简单，但是排查起来却不是那么简单的。遇到问题不要慌，理出要查的1，2，3，然后用排除法一步一步验证就能知道问题在哪里了。

附一详细步骤如下：

源端：

1.备份结构和数据

`mysqldump -h127.0.0.1 -P源端口 -u root --default-character-set=utf8 -B drcdb>src_lingluo.sql
`

2.拷贝文件

`scp src_lingluo.sql lingluo.sss@目的端:/tmp
`

目的端：

3.把数据导进去

`mysql>set names utf8;source /tmp/src_lingluo.sql;
`

4.在两边取checksum

`sh get_checksum.sh
`

5.目的端：

`scp table_checksum.txt lingluo.sss@目的端:/tmp
`

6.vimdiff 对比文件

如果文件内容一样的话，说明数据一样

附二get_checksum.sh

```
#!/bin/sh 
port=$1

table_list='`mysql -h127.0.0.1 -P${port} -u root -A -N << EOF | tail -n +3
 use db_name;show tables
EOF`'

for i in ${table_list}
do
 table_cs='`mysql -h127.0.0.1 -P${port} -u root -A -N -D db_name -e \"checksum 
table ${i};\"`'
 echo ${table_cs} >> table_checksum.txt
done

```

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)