# MySQL · 源码解析 · mysql 子查询执行方式介绍

**Date:** 2023/06
**Source:** http://mysql.taobao.org/monthly/2023/06/02/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2023 / 06
 ](/monthly/2023/06)

 * 当期文章

 MySQL · 源码解析 · 并发Replace into导致死锁
* MySQL · 源码解析 · mysql 子查询执行方式介绍
* 极致性价比:自研数据库PolarDB on 自研芯片倚天

 ## MySQL · 源码解析 · mysql 子查询执行方式介绍 
 Author: 陈江(恬泰) 

 # mysql共有如下几种子查询
* Item_singlerow_subselect
* Item_exists_subselect
* Item_in_subselect
* Item_allany_subselect

本文在不讨论查询变换的情况下，我们我们将逐一介绍上述子查询原生的执行方式，本文注重归纳总结，理解思想的情况下，看源码简单多了。

# 标量子查询（Item_singlerow_subselect）
例子如下，可以出现在投影， where condition, join condition, project list里面。

`desc format=tree select * from t2 where a > (select max(a) from t1);
| -> Filter: (t2.a > (select #2)) (cost=0.35 rows=1)
 -> Table scan on t2 (cost=0.35 rows=2)
 -> Select #2 (subquery in condition; run only once)
 -> Aggregate: max(t1.a)
 -> Table scan on t1 (cost=0.35 rows=1)

`
由plan可以以看到left expr+子查询被解释成为了一个filter predict（t2.a > (select #2)）。在mysql 内存中的对象为：

`$m0 (Item_func_gt *) 0x7ff5abdc82b0
|--$m1 (Item_field *) 0x7ff5ac240c28 field = test.t2.a
`--$m2 (Item_singlerow_subselect *) 0x7ff5abdc80d0

`

## 执行方式
先对select #2进行求值，本例子是max(t1.a)算子求值，存储到Item_singlerow_subselect一个cache里面，run only once嘛，只需求值一次。
对外层t2表进行scan，拿到每一行，应用Item_func_gt 算子，判断t2.a > Item_singlerow_subselect->val_int(),实际调用的是t2.a > Item_cache_int->value. Item_cache_int 就是步骤1的求值。

# exists子查询(Item_exists_subselect)
场景：exists表达式是一个bool求值，允许出现bool值的地方都可以出现该子查询

例子：

`set @@optimizer_switch='materialization=off,semijoin=off';
desc format=tree select * from t2 where exists (select 1 from t3 where t2.a=t3.a);
| -> Filter: exists(select #2) (cost=0.45 rows=2)
 -> Table scan on t2 (cost=0.45 rows=2)
 -> Select #2 (subquery in condition; dependent)
 -> Limit: 1 row(s)
 -> Filter: (t2.a = t3.a) (cost=0.35 rows=1)
 -> Table scan on t3 (cost=0.35 rows=2)

`
注意：这个sql会做semi-join转换，需要关闭semi join就能出exist计划

## 内存中的数据结构
`(gdb) p $ac1->m_where_cond
$45 = (Item_exists_subselect *) 0x7ff5aabc1478
`

where_cond直接就是Item_exists_subselect，没有left expr。Item_exists_subselect负责求值

## 执行过程：
* 外层scan t2表的每一行都需要做一下filter
* filter算子是Item_exists_subselect求值，先执行select 1 from t3 where t2.a=t3.a 子语句求值，这个unit执行结果会存放在Item_exists_subselect.value里面。
* value将作为 Item_exists_subselect->val_bool() 结果返回。

上面介绍的两种子查询优化执行都比较简单，下面我们介绍一下mysql是怎么处理in子查询的, 这个会比较复杂。in子查询有些开关，可以做查询变换，这节里面我们不展开讨论，只专注于原生执行方式

# IN子查询(Item_in_subselect)
这基本上是子查询里面最复杂的了

场景：in子查询本质上也是一个bool函数求值，允许bool值的地方都允许IN子查询，所以可以出现在where_cond,

join条件，having条件，投用列里面。

例子:

`desc format=tree select * from t2 where t2.a in (select sum(a) from t3 group by b);
| -> Filter: <in_optimizer>(t2.a,<exists>(select #2)) (cost=0.45 rows=2)
 -> Table scan on t2 (cost=0.45 rows=2)
 -> Select #2 (subquery in condition; dependent)
 -> Limit: 1 row(s)
 -> Filter: (<cache>(t2.a) = <ref_null_helper>(sum(t3.a)))
 -> Table scan on <temporary>
 -> Aggregate using temporary table
 -> Table scan on t3 (cost=0.45 rows=2)
==>
select t2.a AS a, t2.b AS b
from t2
where < in_optimizer >(
 t2.a,
 < exists >(
 /* select#2 */
 select 1
 from t3
 group by t3.b
 having (< cache >(t2.a) = < ref_null_helper >(sum(t3.a)))
 )
 )
`

## 内存数据结构
执行时会被替换为Item_in_optimizer，重要的数据结构就是左右两个孩子

`$ai0 (Item_in_optimizer *) 0x7ff5aaaad7e0
|--$ai1 (Item_field *) 0x7ff5ac240de8 field = test.t2.a
`--$ai2 (Item_in_subselect *) 0x7ff5ac23fdb8

(gdb) my e optimizer->args[0]
$aj0 (Item_field *) 0x7ff5ac240de8 field = test.t2.a
(gdb) my e optimizer->args[1]
$ak0 (Item_in_subselect *) 0x7ff5ac23fdb8
(gdb) p optimizer->arg_count
$56 = 2
`

## 优化过程
### prepare期间的一些优化
* 先设置Item_in_subselect 的strategy = Subquery_strategy::CANDIDATE_FOR_IN2EXISTS_OR_MAT。在optimize期间会决定是否使用exists方式执行还是materialize方式执行。
* 做IN to Exists执行的变换，这个变换只是辅助，如果optimize期间选择了exists，这些变换才是有用的
* 子查询添加having (< cache >(t2.a) = < ref_null_helper >(sum(t3.a))条件，变成相关的了
* 递归到parent Query_block里面将Item_in_subselect 替换为Item_in_optimizer。

可能有同学会奇怪为啥要添加< ref_null_helper >算子或者in子查询替换为Item_in_optimizer。exists跟in子查询语义是不一样的，exists是bool语义，返回（0,1）IN可以返回NULL的，结果可以是(0,1, NULL）。这点在子查询Unnest里面要尤为注意，请查阅下列例子

`mysql> select null in (0);
+-------------+
| null in (0) |
+-------------+
| NULL |
+-------------+
1 row in set (0.00 sec)

mysql> select exists (select 1 from dual where NULL = 1);
+--------------------------------------------+
| exists (select 1 from dual where NULL = 1) |
+--------------------------------------------+
| 0 |
+--------------------------------------------+
`

## optimize优化
* 在JOIN::decide_subquery_strategy基于cost选择哪种执行更优，exists还是materialize
* 选择exists的话，设置strategy=Subquery_strategy::SUBQ_EXISTS, 投影列替换为”1”, 因为返回bool值就行. 同时子查询的内部block添加limit 1
* 选择mat的话，设置 strategy = Subquery_strategy::SUBQ_MATERIALIZATION; 去掉where_cond或having_cond中新添加的相关列< cache >(t2.a) = < ref_null_helper >(sum(t3.a)， 子查询重新变成非相关的，这样才能做物化。

## 执行过程
从执行计划树可以看到有个filter算子，其实就是Item_in_optimizer::val_int求值， Item_in_optimizer算子右child就是替换好的exists子查询，代入当前的t2.a作为，进行exists子查询求值，能得到bool值，从而知晓过滤与否

## in子查询变种
如果子查询t3在相关列a列有索引，正好可以使用ref access，Item_in_subselect在optimize阶段会创建subselect_indexsubquery_engine，然后子查询求值，只需要在子查询的单表进行索引查找即可。

限定条件：

* 子查询必须是单表，简单的spj，没有groupby
* 内表相关列必须是索引列，形如：
 `outer_expr IN (SELECT tbl.key FROM tbl WHERE subq_where)
` 
 复现case：

 `mysql> alter table t3 add index idx_a(a);
mysql> desc select * from t2 where t2.a in (select a from t3);
+----+--------------------+-------+------------+----------------+---------------+-------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
+----+--------------------+-------+------------+----------------+---------------+-------+---------+------+------+----------+-------------+
| 1 | PRIMARY | t2 | NULL | ALL | NULL | NULL | NULL | NULL | 2 | 100.00 | Using where |
| 2 | DEPENDENT SUBQUERY | t3 | NULL | index_subquery | idx_a | idx_a | 5 | func | 1 | 100.00 | Using index |
+----+--------------------+-------+------------+----------------+---------------+-------+---------+------+------+----------+-------------+
`

执行期执行栈

`#0 RefIterator<false>::Read (this=0x7ff5aabc2ac8) 
#1 0x0000000009876fc6 in LimitOffsetIterator::Read (this=0x7ff5aabc2ba0)
#2 0x0000000009726579 in ExecuteExistsQuery (thd=0x7ff5ad009180, unit=0x7ff5ac2409c8, iterator=0x7ff5aabc2ba0, found=0x7ff60d1b0237) 
#3 0x0000000009726688 in subselect_indexsubquery_engine::exec (this=0x7ff5aabc2a90, thd=0x7ff5ad009180) 
#4 0x000000000971b614 in Item_subselect::exec (this=0x7ff5ac23f828, thd=0x7ff5ad009180) 
#5 0x000000000971ba94 in Item_in_subselect::exec (this=0x7ff5ac23f828, thd=0x7ff5ad009180) 
#6 0x000000000971f85f in Item_in_subselect::val_bool_naked (this=0x7ff5ac23f828) 
#7 0x00000000094c9bf6 in Item_in_optimizer::val_int (this=0x7ff5aab18fd0) 
#8 0x000000000987669e in FilterIterator::Read (this=0x7ff5aab1a898) 
`

## IN子查询变种2-物化执行
上文提到过，IN子查询默认执行方式有两种，上章节介绍了exists，下面就是物化执行的plan。子查询一定是非相关的，先添加索引物化成临时表，然后在执行in算子，在物化表里面进行索引查找

`set @@optimizer_switch='subquery_materialization_cost_based=off';
set @@optimizer_switch='semijoin=off';
 desc format=tree select * from t2 where t2.a in (select a from t3);
 -> Filter: <in_optimizer>(t2.a,t2.a in (select #2)) (cost=0.45 rows=2)
 -> Table scan on t2 (cost=0.45 rows=2)
 -> Select #2 (subquery in condition; run only once)
 -> Filter: ((t2.a = `<materialized_subquery>`.a))
 -> Limit: 1 row(s)
 -> Index lookup on <materialized_subquery> using <auto_distinct_key> (a=t2.a)
 -> Materialize with deduplication
 -> Index scan on t3 using idx_a (cost=0.45 rows=2)
`

# Item_allany_subselect
```
 select * from t2 where t2.a > all(select a from t3);
==>强行改写成Item_maxmin_subselect
select * from t2
where
 < not >(
 (t2.a <= < max >(
 /* select#2 */
 select t3.a
 from t3
 ))
 )

```

## prepare阶段

Item_allany_subselect 被替换为Item_maxmin_subselect，Item_allany_subselect是Item_in_subselect的子类，也复用in_subselect诸多逻辑，比如设置strategy = CANDIDATE_FOR_IN2EXISTS_OR_MAT， optimize里面再通过代价决定是物化还是exists执行

外层的where_cond相当于被改写为:

`t2.a > max(select a from t3);#max被解析为Item_maxmin_subselect算子
`
这个执行方式是内层扫描所有t3.a，外部有个max算子求最大值，扫t3全表不可避免。

## 内存数据结构
`(gdb) my e $dl1->m_where_cond //$dl1为select#1的指针
$do0 (Item_func_not_all *) 0x7ff5aab18c18
`--$do1 (Item_func_le *) 0x7ff5aab19660
 |--$do2 (Item_field *) 0x7ff5ac240768 field = test.t2.a
 `--$do3 (Item_maxmin_subselect *) 0x7ff5aab19480
`

## 执行期求值流程：

* Item_maxmin_subselect算子进行求值，会读取内层unit所有的值，对于每个tuple 发送到* Query_result_max_min_subquery, 这个对象会有个比较函数，进行最大，最小函数求值，然后暂存到* Item_singlerow_subselect cache对象上，逻辑比较简单，可以看下下列函数

```
->Item_maxmin_subselect::val_int
->SELECT_LEX_UNIT::ExecuteIteratorQuery
for (;;) {
 int error = m_root_iterator->Read();
 -->Query_result_max_min_subquery::send_data
 ---->Query_result_max_min_subquery::cmp_int
 ---->Item_singlerow_subselect::store
}

```

本文介绍了mysql 全部的子查询原生的执行方式，下一篇我们将重点介绍mysql子查询解嵌套以及相关的变换，敬请期待。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)