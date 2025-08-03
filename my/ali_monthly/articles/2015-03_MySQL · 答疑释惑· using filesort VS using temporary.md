# MySQL · 答疑释惑· using filesort VS using temporary

**Date:** 2015/03
**Source:** http://mysql.taobao.org/monthly/2015/03/04/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2015 / 03
 ](/monthly/2015/03)

 * 当期文章

 MySQL · 答疑释惑· 并发Replace into导致的死锁分析
* MySQL · 性能优化· 5.7.6 InnoDB page flush 优化
* MySQL · 捉虫动态· pid file丢失问题分析
* MySQL · 答疑释惑· using filesort VS using temporary
* MySQL · 优化限制· MySQL index_condition_pushdown
* MySQL · 捉虫动态·DROP DATABASE外键约束的GTID BUG
* MySQL · 答疑释惑· lower_case_table_names 使用问题
* PgSQL · 特性分析· Logical Decoding探索
* PgSQL · 特性分析· jsonb类型解析
* TokuDB ·引擎机制· TokuDB线程池

 ## MySQL · 答疑释惑· using filesort VS using temporary 
 Author: 

 **背景**

MySQL 执行查询语句， 对于order by谓词，可能会使用filesort或者temporary。比如explain一条语句的时候，会看到Extra字段中可能会出现，using filesort和using temporary。下面我们就来探讨下两个的区别和适用场景。

**解释**

1. using filesort

filesort主要用于查询数据结果集的排序操作，首先MySQL会使用sort_buffer_size大小的内存进行排序，如果结果集超过了sort_buffer_size大小，会把这一个排序后的chunk转移到file上，最后使用多路归并排序完成所有数据的排序操作。

MySQL filesort有两种使用模式:

模式1: sort的item保存了所需要的所有字段，排序完成后，没有必要再回表扫描。

模式2: sort的item仅包括，待排序完成后，根据rowid查询所需要的columns。

很明显，模式1能够极大的减少回表的随机IO。

2. using temporary

MySQL使用临时表保存临时的结构，以用于后续的处理，MySQL首先创建heap引擎的临时表，如果临时的数据过多，超过max_heap_table_size的大小，会自动把临时表转换成MyISAM引擎的表来使用。

从上面的解释上来看，filesort和temporary的使用场景的区别并不是很明显，不过，有以下的原则:

filesort只能应用在单个表上，如果有多个表的数据需要排序，那么MySQL会先使用using temporary保存临时数据，然后再在临时表上使用filesort进行排序，最后输出结果。

**适用场景**

我们看一下下面的三个case:

`create table t1( 
id int, col1 int, col2 varchar(10),
key(id, col1));
`

```
create table t2(
id int, col1 int, col2 varchar(10),
key(col1));

```

case 1:

`mysql&gt; explain select * from t1 force index(id), t2 where t1.id=1 and t1.col1 = t2.col2 order by t1.col1 ;
+----+-------------+-------+------+---------------+------+---------+-------+------+-------------+
| id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
+----+-------------+-------+------+---------------+------+---------+-------+------+-------------+
| 1 | SIMPLE | t1 | ref | id | id | 5 | const | 1 | Using where |
| 1 | SIMPLE | t2 | ALL | NULL | NULL | NULL | NULL | 1 | Using where |
+----+-------------+-------+------+---------------+------+---------+-------+------+-------------+
`

case1: order by字段能够使用index的有序性，所以没有使用filesort，也没有使用temporary。

case 2:

`mysql&gt; explain select * from t1 force index(id), t2 where t1.id=1 and t1.col1 = t2.col2 order by t1.col2;
+----+-------------+-------+------+---------------+------+---------+-------+------+-----------------------------+
| id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
+----+-------------+-------+------+---------------+------+---------+-------+------+-----------------------------+
| 1 | SIMPLE | t1 | ref | id | id | 5 | const | 1 | Using where; Using filesort |
| 1 | SIMPLE | t2 | ALL | NULL | NULL | NULL | NULL | 1 | Using where |
+----+-------------+-------+------+---------------+------+---------+-------+------+-----------------------------+
`

case2: order by谓词，是在第一个表t1上完成，所以只需要在t1表上使用filesort，然后排序后的结果集join t2表。

case 3:

`mysql&gt; explain select * from t1 force index(id), t2 where t1.id=1 and t1.col1 = t2.col2 order by t2.col1 ;
+----+-------------+-------+------+---------------+------+---------+-------+------+----------------------------------------------+
| id | select_type | table | type | possible_keys | key | key_len | ref | rows | Extra |
+----+-------------+-------+------+---------------+------+---------+-------+------+----------------------------------------------+
| 1 | SIMPLE | t1 | ref | id | id | 5 | const | 1 | Using where; Using temporary; Using filesort |
| 1 | SIMPLE | t2 | ALL | NULL | NULL | NULL | NULL | 1 | Using where; Using join buffer |
+----+-------------+-------+------+---------------+------+---------+-------+------+----------------------------------------------+
`

case 3: order by的字段在t2表上，所以需要把t1，t2表join的结果保存到temporary表上，然后对临时表进行filesort，最后输出结果。

**特别优化**

MySQL对order by + limit的filesort做了特别优化，使用Priority queue来保存结果，即一个堆的结构，只保留top n的数据满足limit条件。

**另外**

filesort和temporary都会在tmp目录下创建文件，temporary创建的是MYI，MYD文件。但filesort的文件, 因为MySQL使用了create->open->unlink->使用->close的方式，隐藏了文件，以便进程异常结束的时候，临时文件能够自动回收掉，所以在评估tmp目录空间的时候，需要特别注意。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)