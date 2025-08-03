# 技术分享 | 基于 PROXYSQL 查找从未使用过的表

**原文链接**: https://opensource.actionsky.com/20210412-proxysql/
**分类**: 技术干货
**发布时间**: 2021-04-12T01:13:21-08:00

---

作者：RAYDBA，9 年数据库实战经验，尤其专注于 MySQL 技术栈，Oracle 11g OCP，现任天天鉴宝首席 DBA，负责设计公司整体数据架构与保障数据库服务高安全，高可用与高性能地运行。本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 前言
当你半路接手一个生产业务库时，可能会发现其中很多的表命名很像废弃表、备份表或者归档表，比如以 “tmp”、“copy”、“backup” 和日期等等后缀的表名。当然这些都是最直观的判断，可能依然会有很多因为历史遗留问题产生的垃圾表，然而直接通过表命名无法准确判断是否可以清理，那么如果长时间不清理会带来什么问题吗？
首先按照生产环境的标准，这些或测试，或临时备份的表都不应该保留，并且在分析元数据时会增加额外的工作量。
其次有些表的体积过于庞大，浪费大量存储空间，最后因为这些历史遗留问题没有及时解决，随着时间的流逝导致问题会越来越复杂，越来越难以追溯。
综上所述，我需要一种可靠的技术手段去统计到底哪些表长时间没有访问过，这时有些人会说 general log 可以统计，但是生产数据库不会开启此项参数，毕竟比较影响磁盘的性能。
Proxysql 作为一款优秀的中间件，stats_mysql_query_digest 表默认记录着所有的数据库请求，可以从此表分析出从未使用过的表（时间越久分析越准确，毕竟不排除有些表的访问周期比较长）。
## 实现方法
- **导出全量表**
`mysql -uroot -pxxx -s -e "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA in ('test');" > table_name.txt
`- **循环打印最后一次访问时间和从未使用过的表名称**
```
for i in `cat table_name.txt`;do mysql -u admin -p'xxx' -h 127.0.0.1 -P6032 --default-auth=mysql_native_password -s -e "select ifnull((SELECT from_unixtime(last_seen+28800) FROM stats_mysql_query_digest where digest_text like '%${i}%'),'${i}');";done > ./unused.txt
```
查看文件输出如下：
`2021-03-23 13:42:37
2021-03-23 14:43:56
tb2
tb3
`- **删除最后一次访问时间**
```
sed '/:/d' unused.txt （不修改文件）
sed -i '/:/d' unused.txt （修改文件）
```
删除后如下图所示：
`tb2
tb3
`- **人工确认是否可以清理**
此筛选出的表需要与项目负责人确认是否可以清理，如果确认可以清理，也不是直接物理删除，需要 rename 统一的后缀名，并且再观察一段时间是否有人反馈因为访问不到表产生的问题，如果不再出现任何问题，那么就可以放心地清理了。
附批量生成 rename 语句：
`SELECT
 CONCAT( 'ALTER TABLE ', TABLE_NAME, ' RENAME ', TABLE_NAME, '_unused;' ) 
FROM
 INFORMATION_SCHEMA.TABLES 
WHERE
table_schema IN ( 'unused' ) AND  TABLE_TYPE='BASE TABLE';
SELECT
 CONCAT( 'ALTER TABLE ', TABLE_NAME, ' RENAME ', TABLE_NAME, '_unused;' ) 
FROM
 INFORMATION_SCHEMA.TABLES 
WHERE
table_name IN ( 'table1', 'table2' …) AND  TABLE_TYPE='BASE TABLE';
`注：如果筛选出的表过多，可以新建一个数据库 “unused” 包含所有未使用的表，或者使用文本编辑工具批量生成 “&#8217;table1&#8242;, &#8216;table2&#8217; …”，反之手动复制粘贴即可。
**文章推荐：**
[技术分享 | MySQL binlog 分析工具 analysis_binlog 的使用介绍](https://opensource.actionsky.com/20210331-mysql/)
[技术分享 | MySQL Load Data 的多种用法](https://opensource.actionsky.com/20210325-mysql/)
[技术分享 | MySQL 主从复制中创建复制用户的时机探讨](https://opensource.actionsky.com/20210318-mysql/)