# MySQL · 引擎特性 · Inspecting the Content of a MySQL Histogram

**Date:** 2019/02
**Source:** http://mysql.taobao.org/monthly/2019/02/02/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2019 / 02
 ](/monthly/2019/02)

 * 当期文章

 POLARDB · 性能优化 · 敢问路在何方 — 论B+树索引的演进方向（中）
* MySQL · 引擎特性 · Inspecting the Content of a MySQL Histogram
* Database · 原理介绍 · Snapshot Isolation 综述
* MSSQL · 最佳实践 · 数据库备份加密
* MySQL · 引擎特性 · The design of mysql8.0 redolog
* MySQL · 源码分析 · 8.0 Functional index的实现过程
* PgSQL · 源码解析 · Json — 从使用到源码
* MySQL · 最佳实践 · 如何使用C++实现 MySQL 用户定义函数
* MySQL · 最佳实践 · MySQL多队列线程池优化
* PgSQL · 应用案例 · PostgreSQL 时间线修复

 ## MySQL · 引擎特性 · Inspecting the Content of a MySQL Histogram 
 Author: Øystein 

 In my [FOSDEM 2018 presentation](https://archive.fosdem.org/2018/schedule/event/mysql_histogram/), I showed how you can inspect the content of a [histogram](https://mysqlserverteam.com/histogram-statistics-in-mysql/) using the information schema table *column_statistics*. For example, the following query will show the content of the histogram for the column *l_linenumber* in the table *lineitem* of the *dbt3_sf1* database:

`SELECT JSON_PRETTY(histogram)
 FROM information_schema.column_statistics
 WHERE schema_name = 'dbt3_sf1'
 AND table_name ='lineitem'
 AND column_name = 'l_linenumber';
`
The histogram is stored as a JSON document:

`{
 "buckets": [[1, 0.24994938524948698], [2, 0.46421066400720523],
 [3, 0.6427401784471978], [4, 0.7855470933802572],
 [5, 0.8927398868395817], [6, 0.96423707532558], [7, 1] ],
 "data-type": "int",
 "null-values": 0.0,
 "collation-id": 8,
 "last-updated": "2018-02-03 21:05:21.690872",
 "sampling-rate": 0.20829115437457252,
 "histogram-type": "singleton",
 "number-of-buckets-specified": 1024
}
`

The distribution of values can be found in the buckets array of the JSON document. In the above case, the histogram type is *singleton*. That means that each bucket contains the frequency of a single value. For the other type of histogram, *equi-height*, each bucket will contain the minimum and maximum value for the range covered by the bucket. The frequency value recorded, is the *cumulative frequency*. That is, it gives the frequency of values smaller than the maximum value of the bucket. In the example above, 64.27% of the values in the *l_linenumber* column is less than or equal to 3.

In other words, if you have created a histogram for a column, you can query the information schema table to get estimates on column values. This will normally be much quicker than to get an exact result by querying the actual table.

As discussed in my FOSDEM presentation, string values are [base64](https://dev.mysql.com/doc/refman/8.0/en/string-functions.html#function_to-base64) encoded in the histogram. At the time of the presentation, using MySQL 8.0.11, it was a bit complicated to decode these string values. However, from MySQl 8.0.12 on, this has become simpler. As stated in the release notes for MySQL 8.0.12:

 The JSON_TABLE() function now automatically decodes base-64 values and prints them using the character set given by the column specification.

[JSON_TABLE](https://www.slideshare.net/oysteing/jsontable-the-best-of-both-worlds) is a *table function* that will convert a JSON array to a relational table with one row per element of the array. We can use JSON_TABLE to extract the buckets of the histogram into a relational table:

`SELECT v value, c cumulfreq
FROM information_schema.column_statistics,
 JSON_TABLE(histogram->'$.buckets', '$[*]'
 COLUMNS(v VARCHAR(60) PATH '$[0]',
 c double PATH '$[1]')) hist
 WHERE schema_name = 'dbt3_sf1'
 AND table_name ='orders'
 AND column_name = 'o_orderstatus';
`
Running the above query on my DBT3 database, I get the following result:

`+-------+---------------------+
| value | cumulfreq |
+-------+---------------------+
| F | 0.48544670343055835 |
| O | 0.9743427900693199 |
| P | 1 |
+-------+---------------------+
`
The above gives the cumulative frequencies. Normally, I would rather want to see the actual frequencies of each value, and to get that I will need to subtract the value of the previous row. We can use a [window function](http://www.mysqltutorial.org/mysql-window-functions/) to do that:

`mysql> SELECT v value, c cumulfreq, c - LAG(c, 1, 0) OVER () freq
 -> FROM information_schema.column_statistics,
 -> JSON_TABLE(histogram->'$.buckets', '$[*]'
 -> COLUMNS(v VARCHAR(60) PATH '$[0]',
 -> c double PATH '$[1]')) hist
 -> WHERE schema_name = 'dbt3_sf1'
 -> AND table_name ='orders'
 -> AND column_name = 'o_orderstatus';
 +-------+---------------------+----------------------+
 | value | cumulfreq | freq |
 +-------+---------------------+----------------------+
 | F | 0.48544670343055835 | 0.48544670343055835 |
 | O | 0.9743427900693199 | 0.48889608663876155 |
 | P | 1 | 0.025657209930680103 |
 +-------+---------------------+----------------------+
3 rows in set (0.00 sec)
`

So by combining three new features in MySQL 8.0, histogram, JSON_TABLE, and window functions, I am able to quickly get an estimate for the frequencies of the possible values for my column.

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)