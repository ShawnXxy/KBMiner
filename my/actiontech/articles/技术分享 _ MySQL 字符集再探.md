# 技术分享 | MySQL 字符集再探

**原文链接**: https://opensource.actionsky.com/20220328-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-03-27T22:41:51-08:00

---

作者：傅同学
爱可生研发部成员，主要负责中间件产品开发，热衷技术原理。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。作者：傅同学
本公众号之前发表了一些关于MySQL字符集的文章: [从utf8转换成utf8mb4](https://mp.weixin.qq.com/s/ShPtwC0dwcxOLg16gokNUA) 、 [字符集相关概念](https://mp.weixin.qq.com/s/MdWFPF1xoPoTaoqtWnAjLw) 、 [有关SQL 语句](https://mp.weixin.qq.com/s/4Ed5Iw-wUqCEi9GjHZjQ1Q) 、 [字符集注意事项](https://mp.weixin.qq.com/s/gGQ3CLvn9FX5zhoIh-_sSw) 、 [乱码问题](https://mp.weixin.qq.com/s/-xTGr_XvkDiGDgwhoevyuQ).
近日, 在为 [爱可生开源数据传输工具dtle](https://github.com/actiontech/dtle) 增加UTF-32字符集支持过程中，笔者又了解了一下 MySQL 字符集机制。下面补充说明一些内容：
## 1 字符集
- 
ASCII 是最基础的字符集，每个 ASCII 字符占用1字节，ASCII 仅利用了8位编码能力的一半，最高位恒为 0 。
Latin1 字符集利用剩下的一半编码了西欧常用字母。
- 
UCS-2 使用2字节编码，容量为65536 。
UTF-16 在这基础上, 增加了临时使用2个2字节，编码特殊字符的能力。
- 
UTF-32 使用定长4字节编码。
- 
GB 系列、UTF-8 等字符集，0~127编码和 ASCII 一样，使用单字节。在最高位不为0时，额外使用1~3字节编码。
即它们是变长编码，每个字符占用1~4字节
只表达 ASCII 0~127字符的话，Latin1、GB系列、UTF8 等编码是完全相同的. 而 UTF16 和 UTF32 则会有额外的空白。
`mysql> select
hex(convert("sql" using latin1)) as a,
hex(convert("sql" using gbk)) as b,
hex(convert("sql" using utf8mb4)) as c,
hex(convert("sql" using utf16)) as d,
hex(convert("sql" using utf32)) as e;
| a      | b      | c      | d            | e                        |
+--------+--------+--------+--------------+--------------------------+
| 73716C | 73716C | 73716C | 00730071006C | 00000073000000710000006C |
`
使用如下 SQL 语句可以看到当前 MySQL 实例支持的字符集(和collation)。
`mysql> SELECT CHARACTER_SET_NAME, COLLATION_NAME, ID FROM INFORMATION_SCHEMA.COLLATIONS
ORDER BY CHARACTER_SET_NAME, ID;
...
| gb18030            | gb18030_chinese_ci       | 248 |
| gb18030            | gb18030_bin              | 249 |
| gb18030            | gb18030_unicode_520_ci   | 250 |
...
| utf8mb4            | utf8mb4_general_ci       |  45 |
| utf8mb4            | utf8mb4_bin              |  46 |
| utf8mb4            | utf8mb4_unicode_ci       | 224 |
...
`
#### 题外：什么是 collation
> 
A collation is a set of rules that defines how to compare and sort character strings.
[MySQL文档](https://dev.mysql.com/doc/refman/8.0/en/adding-collation.html): collation是进行字符串比较或排序时使用的规则. 例如:
- 
大小写是否敏感(case sensitive / insensitive)
- 
特殊的相等规则: `ij = ĳ`
## 2 MySQL 系列参数
执行 SQL `show variables like 'character%'` 可以获得MySQL中关于字符集的几个参数。
`character_set_client
character_set_connection
character_set_results
character_set_server
-- 注: 下面3个参数一般无需关心
character_set_filesystem
character_set_database
character_set_system
`
[第06期：梳理 MySQL 字符集的相关概念](https://mp.weixin.qq.com/s/MdWFPF1xoPoTaoqtWnAjLw) 中“ 六、字符集系统参数”一节进行了解释，但稍有误差。
#### 2.1 参数 character_set_client
- 
`character_set_client` 并不是客户端使用的字符集.
- 
用户输入什么数据, 客户端就发送什么数据. 字符集由用户输入决定.
- 
`character_set_client` 是服务端的参数.
- 
服务端认为客户端发来的数据是以 `character_set_client` 编码的.
`character_set_client`不能被设置为以下几个字符集 [(参考链接)](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-impermissible-client-charset):
`ucs2
utf16 / utf16le
utf32
`
不难发现其共同点为: 都是多字节编码. 至于限制的原因本文不作展开。
#### 2.2 参数 character_set_connection
根据[MySQL文档](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html)
> 
(after receiving them) The server converts statements sent by the client from `character_set_client` to `character_set_connection`. Exception: For string literals that have an introducer such as `_utf8mb4` or `_latin2`&#8230;
即收到客户端发来的语句后，服务端(mysqld)会将语句从`character_set_client`转换为`character_set_connection`。(除了指明字符集的字符串字面量, 如 `_utf8mb4"中文字符串"`.)
#### 2.3 SET NAMES 语句
`mysql> SET NAMES gb2312;
`
[MySQL文档](https://dev.mysql.com/doc/refman/8.0/en/set-names.html): 该语句设定3个关于 character set 的变量：`character_set_client`, `character_set_connection` 和 `character_set_results`. **该语句不设置** `character_set_server` 。
注： MySQL客户端的`--default-character-set`参数效果和`SET NAMES`语句一样。
`$ mysql -h ... --default-character-set=gb2312
`
## 3 一个乱码原因的勘误
之前发表的 [第09期：有关 MySQL 字符集的乱码问题](https://mp.weixin.qq.com/s/-xTGr_XvkDiGDgwhoevyuQ) “一、转码失败”一节中有如下案例
`-- 我的终端字符集是 utf8
...
-- 新建立一个连接，客户端这边字符集为 gb2312
root@ytt-pc:/home/ytt# mysql --default-character-set=gb2312 ...
...
-- 表的字符集为 utf8
mysql> create database ytt_new10;
mysql> create table ytt_new10.t1(a1 varchar(100)) charset utf8mb4;
-- 插入一条数据，有两条警告信息
mysql> insert into ytt_new10.t1 values ("病毒滚吧！");
Query OK, 1 row affected, 2 warnings (0.01 sec)
...
-- 那检索出来看到，数据已经不可逆的乱码了。
mysql> select * from ytt_new10.t1;
| a1        |
+-----------+
| ???▒??▒ |
`
该文认为乱码原因是“客户端编码设置成和表编码不一致”。
但可以发现：即使客户端和表的编码都是 gb2312 ，仍然会产生乱码。
`-- 在上述gb2312 MySQL session中
mysql> create table ytt_new10.t2(a1 varchar(100)) charset gb2312;
mysql> insert into ytt_new10.t2 values ("病毒滚吧！");
Query OK, 1 row affected, 2 warnings (0.02 sec)
mysql> select * from ytt_new10.t2;
+------+
| a1   |
+------+
|      |
`
事实上，MySQL 知道`character_set_client = gb2312`，也知道`t1`表编码为utf8。写入过程中，MySQL 会进行转换，不应当发生乱码。
发生乱码的真正原因是: 我们发送给 MySQL 的数据 ，并不是以 gb2312 编码的。是我们欺骗了 MySQL 。
`insert ... "("病毒滚吧！")`这个语句, 是以终端字符集 utf8 编码的. MySQL 把 utf8 数据当作 gb2312 数据, 转换成 utf8 数据, 自然产生了乱码.
让我们以 gb2312 发送数据:
`# 终端编码为UTF-8. 使用iconv转换文件编码.
$ echo 'insert into ytt_new10.t1 val("病毒滚吧！");' | iconv -f utf8 -t gb2312 > insert-gb.txt
$ cat insert-gb.txt # 终端无法正常显示GB2312字符
insert into t1 val("???????ɣ?");
$ mysql -h ... --default-character-set=gb2312 < insert-gbk.txt
`
SELECT 时, MySQL 会把数据转换成`character_set_results`再返回给客户端. 终端可能不支持非 UTF8 字符的显示, 需要转换.
`$ mysql ... --default-character-set=utf8 -e 'select * from ytt_new10.t1'
病毒滚吧！
$ mysql ... --default-character-set=gb2312 -e 'select...' | iconv -f gb2312 -t utf8
病毒滚吧！
`
## 4 字符集 client 到 connection转换的意义
> 
收到客户端发来的语句后, 服务端会将语句从 `character_set_client` 转换为 `character_set_connection`
这个步骤乍一看多此一举
- 
直接以`client`字符集执行, MySQL也会正常转换到表字符集.
- 
也可以让客户端直接以`connection`字符集发送语句.
那么，为什么不将两个参数合并呢? 搜索发现, 使用转换层的潜在原因如下:
不同字符集的某些行为是完全不同的
`mysql> set character_set_connection = 'utf8';
mysql> select length("hello");
|               5 |
mysql> set character_set_connection = 'utf32';
mysql> select length("hello");
|              20 |
`
由于`character_set_client`的限制，客户端不能直接以 UTF32 等字符集发送语句。如果我们就是想要 UTF32 下的行为（函数结果、排序规则等），就需要由 MySQL 进行一层转换。