# MySQL · 参数故事 · max_prepared_stmt_count

**Date:** 2023/03
**Source:** http://mysql.taobao.org/monthly/2023/03/04/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2023 / 03
 ](/monthly/2023/03)

 * 当期文章

 PolarDB auto_inc 场景性能优化之路
* PolarDB MySQL · 持续补强的全局二级索引
* PolarDB for MySQL 优化器查询变换系列 - 条件下推
* MySQL · 参数故事 · max_prepared_stmt_count

 ## MySQL · 参数故事 · max_prepared_stmt_count 
 Author: zhongbei 

 # 前情提要

SysBench压测过程经常遇见max_prepared_stmt_count过小的问题，本文分析SysBench压测中的prepare语句数量，给SysBench压测过程max_prepared_stmt_count参数的设置提供依据。

# 参数背景

SysBench压测过程会产生prepare语句，主要由db-ps-mode选项控制，该选项取值为{auto, disable}，默认值为auto。取值为auto时，允许使用prepare语句。取值为disable时，表示禁用prepare语句。SysBench压测过程可能会产生大量的prepare语句，并且可能会超出max_prepared_stmt_count参数限制，出现报错：

`FATAL: MySQL error: 1461 "Can't create more than max_prepared_stmt_count statements (current value: 16382)"
`

为此，在SysBench压测过程中，我们需要调整max_prepared_stmt_count参数以满足测试需求。

max_prepared_stmt_count参数限制了MySQL中prepare语句的数量，超过max_prepared_stmt_count数量后不能准备新的prepare语句，需要等之前的prepare语句被释放。该参数是一个全局动态参数，官方默认值为16382，取值范围为[0, 4194304]。关于参数的详细描述，可参见[文档](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_prepared_stmt_count)。

那么调整这个参数会产生什么风险？

* 调大的风险：一个prepare语句最少需要占用8k的内存，prepare语句太多会占用过多的实例内存资源，增加MySQL OOM的风险。
* 调小的风险：风险较小，现有prepare语句不受影响，超过max_prepared_stmt_count数量后不能准备新的prepare语句，需要等之前的prepare语句被释放。

# SysBench源码分析

在SysBench测试场景下，如何根据需要确定max_prepared_stmt_count参数取值？

下面以SysBench 1.0.20为例（阿里云RDS官网推荐的测试版本，不同版本会有差异），分析了SysBench的代码。在SysBench测试场景下，prepare语句的数量主要与SysBench的测试参数相关，涉及三个参数：表数量、线程数、测试模型。以oltp_read_only测试模型为例，分析prepare语句的数量，最后给出prepare语句的计算公式，给max_prepared_stmt_count参数设置提供依据。

`-- ----------------------------------------------------------------------
-- Read-Only OLTP benchmark
-- ----------------------------------------------------------------------

require("oltp_common")

function prepare_statements()
 prepare_point_selects() -- 每张表执行一次

 if not sysbench.opt.skip_trx then
 prepare_begin() -- 每个线程执行一次
 prepare_commit() -- 每个线程执行一次
 end

 if sysbench.opt.range_selects then
 prepare_simple_ranges() -- 每张表执行一次
 prepare_sum_ranges() -- 每张表执行一次
 prepare_order_ranges() -- 每张表执行一次
 prepare_distinct_ranges() -- 每张表执行一次
 end
end
`

SysBench中prepare语句在prepare_statements()函数中，其中prepare_begin 、prepare_commit每个线程执行一次：

`function prepare_begin()
 stmt.begin = con:prepare("BEGIN")
end

function prepare_commit()
 stmt.commit = con:prepare("COMMIT")
end
`

prepare_point_selects、prepare_simple_ranges、prepare_sum_ranges、prepare_order_ranges、prepare_distinct_ranges每个线程每张表都需要执行一次：

`function prepare_point_selects()
 prepare_for_each_table("point_selects")
end

function prepare_simple_ranges()
 prepare_for_each_table("simple_ranges")
end

function prepare_sum_ranges()
 prepare_for_each_table("sum_ranges")
end

function prepare_order_ranges()
 prepare_for_each_table("order_ranges")
end

function prepare_distinct_ranges()
 prepare_for_each_table("distinct_ranges")
end
`

那么每个线程对每个表就需要执行5个prepare语句，再加上线程本身需要执行begin、commit的2个prepare语句，可以得出oltp_read_only测试模型需要的prepare语句总数计算公式为：

`read_only_ps_total = 线程数 * 表数量 * 5 + 线程数 * 2
`

**然而**，需要注意的是，MySQL官方并不支持begin类型的prepare语句！见[文档](https://dev.mysql.com/doc/refman/8.0/en/sql-prepared-statements.html)。在执行begin类型的prepare语句时会失败，所以需要从上述公式中减去一个“线程数”，于是oltp_read_only测试模型正确的prepare语句总数公式为：

`read_only_ps_total = 线程数 * 表数量 * 5 + 线程数
`

# SysBench prepare语句计算公式

类似的可以分析oltp_write_only、oltp_read_write、oltp_insert的源码，在此总结了不同的测试模型prepare语句计算公式，计算汇总在如下表格：

 测试模型
 prepare语句数量计算公式

 oltp_read_only
 线程数 * 表数量 * 5 + 线程数

 oltp_write_only
 线程数 * 表数量 * 4 + 线程数

 oltp_read_write
 线程数 * 表数量 * 9 + 线程数

 oltp_insert
 0. (oltp_insert场景没有prepare语句)

# 公式正确性验证

利用show global status like ’Prepared_stmt_count’;命令，可以获取SysBench测试过程中实际的prepare语句数量。注意：Prepared_stmt_count变量表示当前MySQL总的prepare语句数量，这是一个准确值，当SysBench测试结束，prepare语句结束，该值会变成0。

`mysql> show global status like 'prepared_stmt_count';
+---------------------+-------+
| Variable_name | Value |
+---------------------+-------+
| Prepared_stmt_count | 0 |
+---------------------+-------+
`
测试了几组数据，结果如下：

 测试模型
 表数量
 线程数
 prepare语句实际值
 根据公式计算的prepare语句数量

 oltp_read_only
 50
 32
 8032
 8032

 100
 32
 16032
 16032

 100
 64
 32064
 32064

 oltp_write_only
 50
 32
 6432
 6432

 100
 32
 12832
 12832

 100
 64
 25664
 25664

 oltp_read_write
 50
 32
 14432
 14432

 100
 32
 28832
 28832

 100
 64
 57664
 57664

 oltp_insert
 50
 32
 0
 0

 100
 32
 0
 0

 100
 64
 0
 0

可以看到，prepare语句实际值和理论值完全吻合，证明了公式的正确性。

利用show global status like ’com_stmt%’;命令，可以获取prepare语句累计数量。

`mysql> show global status like 'com_stmt%';
+-------------------------+-------+
| Variable_name | Value |
+-------------------------+-------+
| Com_stmt_execute | 0 |
| Com_stmt_close | 0 |
| Com_stmt_fetch | 0 |
| Com_stmt_prepare | 0 |
| Com_stmt_reset | 0 |
| Com_stmt_send_long_data | 0 |
| Com_stmt_reprepare | 0 |
+-------------------------+-------+
`
其中，Com_stmt_prepare表示累计prepare语句数量，Com_stmt_close表示累计关闭的prepare语句数量。Com_stmt_prepare中包含了prepare语句执行失败的数量，感兴趣的读者可以利用Com_stmt_prepare - Com_stmt_close来验证SysBench测试过程中，begin语句是否prepare失败。笔者已经对此进行了验证。

# 参数设置建议

根据上述分析，SysBench压测中prepare语句数量与SysBench的测试参数相关，涉及三个参数：**表数量、线程数、测试模型。**只要max_prepared_stmt_count参数大于等于SysBench测试的prepare语句理论值，就可以保证满足测试要求。

不同的测试参数配置会对prepare语句数量有着较大的影响，同时max_prepared_stmt_count参数不应该影响用户正常业务，对于有SysBench测试需求的用户，根据**本文计算公式**来提供max_prepared_stmt_count参数的设置依据，由用户自行根据测试需求来设置这个参数。同时建议客户在测试完毕后，**调小max_prepared_stmt_count参数。**对于业务中的prepare语句数量，由用户自己评估来设置max_prepared_stmt_count参数。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)