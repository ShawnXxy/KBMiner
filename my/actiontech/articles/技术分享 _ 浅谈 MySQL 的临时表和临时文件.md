# 技术分享 | 浅谈 MySQL 的临时表和临时文件

**原文链接**: https://opensource.actionsky.com/20210716-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-07-15T23:55:11-08:00

---

作者：姚嵩
爱可生南区交付服务部经理，爱好音乐，动漫，电影，游戏，人文，美食，旅游，还有其他。虽然都很菜，但毕竟是爱好。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文内容来源于对客户的三个问题的思考：
- 
哪些 SQL 会产生临时表/临时文件
- 
如何查看已有的临时表
- 
如何控制临时表/临时文件的总大小
## 说明：
以下测试都是在 MySQL 8.0.21 版本中完成，不同版本可能存在差异，可自行测试；
## 首先，让我们了解下什么是临时表|临时文件？
临时表和临时文件都是用于临时存放数据集的地方；
一般情况下，需要临时存放在临时表或临时文件中的数据集应该符合以下特点：
- 
数据集较小(较大的临时数据集一般意味着 SQL 较烂，当然有例外项)
- 
用完就清理(因为是临时存储数据集的地方，所以生命周期和 SQL 或者会话生命周期相同)
- 
会话隔离(因为是临时数据集，不涉及到与其他会话交互)
- 
不产生 GTID
从临时表|临时文件产生的主观性来看，分为2类：
- 
用户创建的临时表
- 
SQL 产生的临时表|临时文件
**用户创建临时表：**
用户创建临时表(只有创建临时表的会话才能查看其创建的临时表的内容)
`create database if not exists db_test ;
use db_test ;
CREATE TEMPORARY TABLE t1 (c1 INT PRIMARY KEY) ENGINE=INNODB;
select * from db_test.t1 ;
`
注意：
可以创建和普通表同名临时表，其他会话可以看到普通表(因为看不到其他会话创建的临时表)；
创建临时表的会话会优先看到临时表；
同名表的创建的语句如下
`CREATE TABLE t1 (c1 INT PRIMARY KEY) ENGINE=INNODB;
insert into  t1 values(1);
`
当存在同名的临时表时，会话都是优先处理临时表(而不是普通表)，包括：select、update、delete、drop、alter 等操作；
**查看用户创建的临时表：**
任何 session 都可以执行下面的语句，
&#8211; 查看用户创建的当前 active 的临时表(不提供 optimizer 使用的内部 InnoDB 临时表信息)
`SELECT * FROM INFORMATION_SCHEMA.INNODB_TEMP_TABLE_INFO\G
`
注意
用户创建的临时表，表名为t1，
但是通过 INNODB_TEMP_TABLE_INFO 查看到的临时表的 NAME 是#sql开头的名字，例如：#sql45aa_7c69_2 ；
另外 information_schema.tables 表中是不会记录临时表的信息的。
**用户创建的临时表的回收：**
- 
会话断开，自动回收用户创建的临时表；
- 
可以通过 drop table 删除用户创建的临时表，例如：drop table t1;
**用户创建的临时表的其他信息&#038;参数：**
会话临时表空间存储 用户创建的临时表和优化器 optimizer 创建的内部临时表(当磁盘内部临时表的存储引擎为 InnoDB 时)；
innodb_temp_tablespaces_dir 变量定义了创建 会话临时表空间的位置，默认是数据目录下的#innodb_temp 目录；
文件类似temp_[1-20].ibt ；
查看会话临时表空间的元数据：
`select * from information_schema.innodb_session_temp_tablespaces ;
`
用户创建的临时表删除后，其占用的空间会被释放(temp_[1-20].ibt文件会变小)。
在 MySQL 8.0.16 之前，internal_tmp_disk_storage_engine 变量定义了用户创建的临时表和 optimizer 创建的内部临时表的引擎，可选 INNODB 和 MYISAM ；
从 MySQL 8.0.16 开始，internal_tmp_disk_storage_engine参数被移除，默认使用InnoDB存储引擎；
innodb_temp_data_file_path 定义了用户创建的临时表使用的回滚段的存储文件的相对路径、名字、大小和属性，该文件是全局临时表空间(ibtmp1)；
可以使用语句查询全局临时表空间的数据文件大小：
`SELECT FILE_NAME, TABLESPACE_NAME, ENGINE, INITIAL_SIZE, TOTAL_EXTENTS*EXTENT_SIZE
AS TotalSizeBytes, DATA_FREE, MAXIMUM_SIZE FROM INFORMATION_SCHEMA.FILES
WHERE TABLESPACE_NAME = 'innodb_temporary'\G 
`
**SQL 什么时候产生临时表|临时文件呢？**
需要用到临时表或临时文件的时候，optimizer 自然会创建使用(感觉是废话，但是又觉得有道理=.=!)；
(想象能力强的，可以牢记上面这句话；想象能力弱的，只能死记下面的 SQL 了。我也弱，此处有个疲惫的微笑😊)
下面列举一些 server 在处理 SQL 时，可能会创建内部临时表的 SQL ：
SQL 包含 union | union distinct 关键字
SQL 中存在派生表
SQL 中包含 with 关键字
SQL 中的order by 和 group by 的字段不同
SQL 为多表 update
SQL 中包含 distinct 和 order by 两个关键字
我们可以通过下面两种方式判断 SQL 语句是否使用了临时表空间：
# 如果 explain 的 Extra 列包含 Using temporary ，那么说明会使用临时空间，如果包含 Using filesort ，那么说明会使用文件排序(临时文件)；
`explain xxx ; 
`
# 如果执行 SQL 后，表的 ID 列变为了show processlist 中的 id 列的值，那么说明 SQL 语句使用了临时表空间
`select * from information_schema.innodb_session_temp_tablespaces ;   
`
**SQL创建的内部临时表的存储信息：**
SQL 创建内部临时表时，优先选择在内存中，默认使用 TempTable 存储引擎(由参数 internal_tmp_mem_storage_engine 确定)，
当 temptable 使用的内存量超过 temptable_max_ram 定义的大小时，
由 temptable_use_mmap 确定是使用内存映射文件的方式还是 InnoDB 磁盘内部临时表的方式存储数据
(temptable_use_mmap 参数在 MySQL 8.0.16 引入，MySQL 8.0.26 版本不推荐，后续应该会移除)；
temptable_use_mmap 的功能将由MySQL 8.0.23 版本引入的 temptable_max_mmap 代替，
当 temptable_max_mmap=0 时，说明不使用内存映射文件，等价于 temptable_use_mmap=OFF ；
当 temptable_max_mmap=N 时，N为正整数，包含了 temptable_use_mmap=ON 以及声明了允许为内存映射文件分配的最大内存量。
该参数的定义解决了这些文件使用过多空间的风险。
内存映射文件产生的临时文件会存放于 tmpdir 定义的目录中，在 TempTable 存储引擎关闭或 mysqld 进程关闭时，回收空间；
当 SQL 创建的内部临时表，选择 MEMORY 存储引擎时，如果内存中的临时表变的太大，MySQL 将自动将其转为磁盘临时表；
其能使用的内存上限为 min(tmp_table_size,max_heap_table_size)；
**监控 TempTable 从内存和磁盘上分配的空间：**
`select * from performance_schema.memory_summary_global_by_event_name \
where event_name in('memory/temptable/physical_ram','memory/temptable/physical_disk') \G
`
具体的字段含义见：Section 27.12.20.10, “Memory Summary Tables”.
**监控内部临时表的创建：**
当在内存或磁盘上创建内部临时表，服务器会增加 Created_tmp_tables 的值；
当在磁盘上创建内部临时表时，服务器会增加 Created_tmp_disk_tables 的值，
如果在磁盘上创建了太多的内部临时表，请考虑增加 tmp_table_size 和 max_heap_table_size 的值；
created_tmp_disk_tables 不计算在内存映射文件中创建的磁盘临时表；
**例外项：**
临时表/临时文件一般较小，但是也存在需要大量空间的临时表/临时文件的需求：
- 
load data local 语句，客户端读取文件并将其内容发送到服务器，服务器将其存储在 tmpdir 参数指定的路径中；
- 
在 replica 中，回放 load data 语句时，需要将从 relay log 中解析出来的数据存储在slave_load_tmpdir(replica_load_tmpdir)指定的目录中，该参数默认和 tmpdir 参数指定的路径相同；
- 
需要 rebuild table 的在线 alter table 需要使用 innodb_tmpdir 存放排序磁盘排序文件，如果 innodb_tmpdir 未指定，则使用 tmpdir 的值；
因为这些例外项一般需要较大的空间，所以需要考虑是否要将其存放在独立的挂载点上。
**其他：**
列出由失败的 alter table 创建的隐藏临时表，这些临时表以#sql开头，可以使用 drop table 删除；
`show extended tables ; 
`
通过 lsof +L1 可以查看标识为 delete ，但还未释放空间的文件。
如果想释放这些 delete 状态的文件，可以尝试下面的方法(不推荐，后果自负)：
`cd /proc/${pid}/fd   # ${pid} 表示你想释放的delete状态的文件持有者的进程号
ls -al | grep '${file_name}'    # 假设${file_name}是/opt/mysql/tmp/3306/ibBATOn8 (deleted)
echo "" > ${fd_number}    # ${fd_number} 表示你想释放的delete状态的文件的fd，倒数第三个字段，如echo "" > 6
`
## 总结：
普通的磁盘临时表|临时文件(一般需要较小的空间)：
临时表|临时文件的一般所需的空间较小，会优先存放于内存中，若超过一定的大小，则会转换为磁盘临时表|临时文件；
磁盘临时表默认为 InnoDB 引擎，其存放在临时表空间中，由 innodb_temp_tablespaces_dir 定义表空间的存放目录，表空间文件类似：temp_[1-20].ibt ；MySQL 未定义 InnoDB 临时表空间的最大使用上限；
当临时表|临时文件使用完毕后，会自动回收临时表空间文件的大小；
innodb_temp_data_file_path 定义了用户创建的临时表使用的回滚段的存储文件的相对路径、名字、大小和属性，该文件是全局临时表空间(ibtmp1)，该文件可以设置文件最大使用大小；
**例外项(一般需要较大的空间)：**
load data local 语句，客户端读取文件并将其内容发送到服务器，服务器将其存储在 tmpdir 参数指定的路径中；
在 replica 中，回放 load data 语句时，需要将从 relay log 中解析出来的数据存储在 slave_load_tmpdir(replica_load_tmpdir) 指定的目录中，该参数默认和 tmpdir 参数指定的路径相同；
需要 rebuild table 的在线 alter table 需要使用 innodb_tmpdir 存放排序磁盘排序文件，如果 innodb_tmpdir 未指定，则使用 tmpdir 的值；
若用户判断产生的临时表|临时文件一定会转换为磁盘临时表|临时文件，那么可以设置 set session big_tables=1;让产生的临时表|临时文件直接存放在磁盘上；
## 猜测其设计：
对于需要较小空间的临时表|临时文件，MySQL 要么将其存储于内存，要么放在统一的磁盘临时表空间中，用完即释放；
对于需要较大空间的临时表|临时文件，可以通过设置参数，将其存储于单独的目录|挂载点；例如：load local data 语句或需要重建表的在线 alter table 语句，都有对应的参数设置其存放临时表|临时文件的路径；
当前只有 innodb_temp_data_file_path 参数可以限制 用户创建的临时表使用的回滚段的存储文件的大小，无其他参数可以限制临时表|临时文件可使用的磁盘空间；