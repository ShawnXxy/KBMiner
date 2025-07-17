# 新特性解读 | MySQL 8.0 Temptable 引擎介绍

**原文链接**: https://opensource.actionsky.com/20190711-mysql8-temptable/
**分类**: MySQL 新特性
**发布时间**: 2019-07-10T22:53:00-08:00

---

提到MySQL临时表，我们都很熟悉了，一般来说，分为两类：
**1. MySQL 临时表引擎，名字叫做Memory。****比如******
- `create table tmp1(id int, str1 varchar(100) ) engine = memory;`
由参数maxheaptable_size 来控制，超过报错。
**2. 非临时表的引擎，这里又分为两类：******
- 用户自定义的临时表，比如:
- `create temporary table (id int, str1 varchar(100) );`
- SQL执行过程中产生的内部临时表，比如：union , 聚合类ORDER BY，派生表，大对象字段的查询，子查询或者半连接的固化等等场景。
那么这两种临时表的计数器通常用 **show global status like &#8216;%tmp_%tables%&#8217;** 来查看。比如
- `mysql> show status like '%tmp_%tables%';``
- ``+-------------------------+-------+``
- ``| Variable_name           | Value |``
- ``+-------------------------+-------+``
- ``| Created_tmp_disk_tables | 0     |``
- ``| Created_tmp_tables      | 0     |``
- ``+-------------------------+-------+``
- ``2 rows in set (0.00 sec)`
以上结果分别代表，只创建磁盘上的临时表计数以及临时表的总计数。这两个计数器由参数 tmp_table_size 和 max_heap_table_size 两个取最小值来控制。
那在 MySQL 5.7 之前，这个 SQL 运行中产生的临时表是 MYISAM，而且只能是 MYISAM。那 MySQL 从 5.7 开始提供了参数 Internal_tmp_mem_storage_engine 来定义内部的临时表引擎，可选值为 MYISAM 和 INNODB 。当然这里我们选择 INNODB 。并且把内部的临时表默认保存在临时表空间 ibtmp1 **(可以用参数innodb_temp_data_file_path 设置大小以及步长等)**下。当然这里我们得控制下 ibtmp1 的大小，要不然一个烂SQL就把磁盘整爆了。
但是MySQL 5.7 之前都没有解决如下问题:
- varchar的变长存储。那就是如果临时表的字段定义是varchar（200），那么映射到内存里处理的字段变为CHAR(200)。假设varchar(200) 就存里一个字符‘Y’, 那岂不是很大的浪费。
- 大对象的默认磁盘存储，比如TEXT，BLOB， JSON等，不管里面存放了啥，直接转化为磁盘存储。
MySQL 8.0 开始，专门实现了一个临时表的引擎 TempTable , 解决了VARCHAR字段的边长存储以及大对象的内存存储。由变量interal_tmp_mem_storage_engine来控制，可选值为TempTable（**默认**）和Memory；新引擎的大小由参数temp_table_max_ram 来控制，默认为1G。超过了则存储在磁盘上（ibtmp1）。并且计数器由性能字典的表 memory_summary_global_by_event_name 来存储。
- `mysql> SELECT * FROM performance_schema. memory_summary_global_by_event_name WHERE event_name like '%temptable%'\G`
- `*************************** 1. row ***************************`
- `                  EVENT_NAME: **memory/temptable/physical_disk**`
- `                 COUNT_ALLOC: 0`
- `                  COUNT_FREE: 0`
- `   SUM_NUMBER_OF_BYTES_ALLOC: 0`
- `    SUM_NUMBER_OF_BYTES_FREE: 0`
- `              LOW_COUNT_USED: 0`
- `          CURRENT_COUNT_USED: 0`
- `             HIGH_COUNT_USED: 0`
- `    LOW_NUMBER_OF_BYTES_USED: 0`
- `CURRENT_NUMBER_OF_BYTES_USED: 0`
- `   HIGH_NUMBER_OF_BYTES_USED: 0`
- `*************************** 2. row ***************************`
- `                  EVENT_NAME: **memory/temptable/physical_ram**`
- `                 COUNT_ALLOC: 1`
- `                  COUNT_FREE: 0`
- `   SUM_NUMBER_OF_BYTES_ALLOC: 1048576`
- `    SUM_NUMBER_OF_BYTES_FREE: 0`
- `              LOW_COUNT_USED: 0`
- `          CURRENT_COUNT_USED: 1`
- `             HIGH_COUNT_USED: 1`
- `    LOW_NUMBER_OF_BYTES_USED: 0`
- `CURRENT_NUMBER_OF_BYTES_USED: 1048576`
- `   HIGH_NUMBER_OF_BYTES_USED: 1048576`
- `2 rows in set (0.03 sec)`
以上memory/temptable/physical_disk 代表放入磁盘上的临时表计数情况。
memory/temptable/physical_ram 代表放入内存的临时表计数情况。
**那总结下MySQL 8.0 引入的TempTable 引擎：**
- 默认内部临时表引擎。
- 支持变长字符类型的实际存储。
- 设置变量temp_table_max_ram 来控制实际存储内存区域大小。
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)