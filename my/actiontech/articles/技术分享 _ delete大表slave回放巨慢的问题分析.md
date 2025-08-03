# 技术分享 | delete大表slave回放巨慢的问题分析

**原文链接**: https://opensource.actionsky.com/20190625-delete-slave/
**分类**: 技术干货
**发布时间**: 2019-06-25T19:34:41-08:00

---

**问题**
在master上执行了一个无where条件delete操作，该表50多万记录。binlog_format是mixed模式，但transaction_isolation是RC模式,所以dml语句会以row模式记录。此表没有主键有非唯一索引。在slave重放时超过10小时没有执行完成。
**分析**
首先来了解下slave在row模式下是如何重放relay log的。在row模式下，binlog中会记录DML变更操作的事件描述信息、BEFORE IMAGE、AFTER IMAGE。
+----------------------------+
| Header: table id |
| column information etc. |
+--------------+-------------+
| BEFORE IMAGE | AFTER IMAGE |
+--------------+-------------+
| BEFORE IMAGE | AFTER IMAGE |
+--------------+-------------+
DML事件类型与image的关系矩阵
+------------------+--------------+-------------+
| EVENT TYPE | BEFORE IMAGE | AFTER IMAGE |
+------------------+--------------+-------------+
| WRITE_ROWS_EVENT | No | Yes |
+------------------+--------------+-------------+
| DELETE_ROWS_EVENT| Yes | No |
+------------------+--------------+-------------+
| UPDATE_ROWS_EVENT| Yes | Yes |
+------------------+--------------+-------------+
delete和update包含了查找操作，基于BI内容搜索找到对应的记录执行相应操作。
基于row模式binlog的重放主要在此函数中进行Rows_log_event::do_apply_event，它根据事件类型调用相应的do_before_row_operations 以delete操作为例
Delete_rows_log_event::do_before_row_operations，此函数会更新sql command计数器(com_delete)
接下来调用Rows_log_event::row_operations_scan_and_key_setup分配需要的内存空间
Prepare memory structures for search operations. If
search is performed：
1.using hash search => initialize the hash
2.using key => decide on key to use and allocate mem structures
3.using table scan => do nothing
选择何种搜索策略取决于Rows_log_event::decide_row_lookup_algorithm_and_key的结果，其决策矩阵依赖表的索引信息和slave_rows_search_algorithms参数的设置。
Decision table：
- I &#8211;> Index scan / search
- T &#8211;> Table scan
- H &#8211;> Hash scan
- Hi &#8211;> Hash over index
- Ht &#8211;> Hash over the entire table
|--------------+-----------+------+------+------|
| Index\Option | I , T , H | I, T | I, H | T, H |
|--------------+-----------+------+------+------|
| PK / UK | I | I | I | Hi |
| K | Hi | I | Hi | Hi |
| No Index | Ht | T | Ht | Ht |
|--------------+-----------+------+------+------|
默认slave_rows_search_algorithms是TABLE_SCAN，INDEX_SCAN，对应函数Rows_log_event::do_index_scan_and_update
如果是INDEX_SCAN，HASH_SCAN，对应函数Rows_log_event::do_hash_scan_and_update
在没有主键的情况下，会遍历binlog每行事件，再用该事件的BI去查找对应的记录，然后变更成对应AI信息。
for each row in the event do
{
search for the correct row to be modified using BI
replace the row in the table with the corresponding AI
}
如果是HASH SCAN over table，会先对binlog事件中的记录执行hash，放到hash表中，再对表中每行记录进行hash，与hash表中的记录对比，条件匹配回放AI部分。
}
for each row in the table do
{
key= hash the row;
if (key is present in the hash)
{
apply the AI to the row.
}
}
如果是HASH SCAN over index，在有非唯一索引的情况下，对binlog事件中的记录执行hash时，也会将该记录的key保存在一个去重的key列表集合中，然后根据该索引集合去查找记录，对找到的记录执行hash操作并与hash表中的记录对比，如果匹配则回放AI部分。
for each row in the event do
{
hash the row.
store the key in a list of distinct key.
}
for each row corresponding key values in the key list do
{
key= hash the row;
if (key is present in the hash)
{
apply the AI to the row.
}
}
从上述分析可以推测在没有主键的情况下Hi的扫描方式会快于Ht和Index scan。
**测试**
对比slave_rows_search_algorithms在TABLE_SCAN,INDEX_SCAN和INDEX_SCAN,HASH_SCAN两种参数设置下，delete大表哪个效率更高。
CREATE TABLE `ants_bnzbw_temp` (
`accrued_status` varchar(1) COLLATE utf8_bin DEFAULT NULL,
`contract_no` varchar(32) COLLATE utf8_bin DEFAULT NULL,
`business_date` date DEFAULT NULL,
`prin_bal` int(11) DEFAULT NULL COMMENT,
`ovd_prin_bal` int(11) DEFAULT NULL COMMENT ,
`ovd_int_bal` int(11) DEFAULT NULL COMMENT ,
`int_amt` int(11) DEFAULT NULL COMMENT ,
`ovd_prin_pnlt_amt` int(11) DEFAULT NULL COMMENT ,
`ovd_int_pnlt_amt` int(11) DEFAULT NULL COMMENT,
KEY `accrued_status` (`accrued_status`) USING BTREE,
KEY `contract_no` (`contract_no`) USING BTREE,
KEY `business_date` (`business_date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
master [localhost] {msandbox} (test) > select count(*) from ants_bnzbw_temp;
+----------+
| count(*) |
+----------+
| 522490 |
+----------+
1 row in set (0.15 sec)
master [localhost] {msandbox} (test) > delete from ants_bnzbw_temp;
Query OK, 522490 rows affected (25.86 sec)
主机slave1
slave_rows_search_algorithms='INDEX_SCAN,HASH_SCAN'
事务执行大约2000s（没有实时追踪事务执行时间）
SET @@SESSION.GTID_NEXT= '00020594-1111-1111-1111-111111111111:237'/*!*/;
# at 221356832
#180102 14:04:48 server id 1 end_log_pos 221356895 CRC32 0xafdd018f Query thread_id=20 exec_time=25 error_code=0
---TRANSACTION 5582, ACTIVE 1447 sec
mysql tables in use 1, locked 1
2581 lock struct(s), heap size 319696, 799680 row lock(s), undo log entries 399840
调用栈采样
frame #0: 0x000000010f94f331 mysqld`page_rec_get_next_low(unsigned char const*, unsigned long) + 81
frame #1: 0x000000010f94bc28 mysqld`row_search_mvcc(unsigned char*, page_cur_mode_t, row_prebuilt_t*, unsigned long, unsigned long) + 9192
frame #2: 0x000000010f86d27e mysqld`ha_innobase::index_read(unsigned char*, unsigned char const*, unsigned int, ha_rkey_function) + 734
frame #3: 0x000000010f036b6c mysqld`handler::ha_index_read_map(unsigned char*, unsigned char const*, unsigned long, ha_rkey_function) + 140
frame #4: 0x000000010f6d5a94 mysqld`Rows_log_event::next_record_scan(bool) + 324
frame #5: 0x000000010f6d66cf mysqld`Rows_log_event::do_scan_and_update(Relay_log_info const*) + 159
frame #6: 0x000000010f6d7198 mysqld`Rows_log_event::do_apply_event(Relay_log_info const*) + 1064
frame #7: 0x000000010f718d42 mysqld`apply_event_and_update_pos(Log_event**, THD*, Relay_log_info*) + 530
frame #8: 0x000000010f711f46 mysqld`handle_slave_sql + 4438
主机slave2
slave_rows_search_algorithms='TABLE_SCAN,INDEX_SCAN'
事务执行超过11145s，还没执行完成
---TRANSACTION 4520, ACTIVE 11145 sec
mysql tables in use 1, locked 1
622 lock struct(s), heap size 90320, 191792 row lock(s), undo log entries 95896
调用栈采样
* frame #0: 0x0000000109fd9c3a mysqld`btr_search_s_lock(dict_index_t const*) + 58
frame #1: 0x0000000109fdb37f mysqld`btr_search_guess_on_hash(dict_index_t*, btr_search_t*, dtuple_t const*, unsigned long, unsigned long, btr_cur_t*, unsigned long, mtr_t*) + 479
frame #2: 0x0000000109fc84a9 mysqld`btr_cur_search_to_nth_level(dict_index_t*, unsigned long, dtuple_t const*, page_cur_mode_t, unsigned long, btr_cur_t*, unsigned long, char const*, unsigned long, mtr_t*) + 649
frame #3: 0x000000010a177324 mysqld`row_search_on_row_ref(btr_pcur_t*, unsigned long, dict_table_t const*, dtuple_t const*, mtr_t*) + 164
frame #4: 0x000000010a17746f mysqld`row_get_clust_rec(unsigned long, unsigned char const*, dict_index_t*, dict_index_t**, mtr_t*) + 175
frame #5: 0x000000010a1988e5 mysqld`row_vers_impl_x_locked(unsigned char const*, dict_index_t*, unsigned long const*) + 293
frame #6: 0x000000010a0f39db mysqld`lock_rec_convert_impl_to_expl(buf_block_t const*, unsigned char const*, dict_index_t*, unsigned long const*) + 603
frame #7: 0x000000010a0f4914 mysqld`lock_sec_rec_read_check_and_lock(unsigned long, buf_block_t const*, unsigned char const*, dict_index_t*, unsigned long const*, lock_mode, unsigned long, que_thr_t*) + 596
frame #8: 0x000000010a1802f1 mysqld`sel_set_rec_lock(btr_pcur_t*, unsigned char const*, dict_index_t*, unsigned long const*, unsigned long, unsigned long, que_thr_t*, mtr_t*) + 193
frame #9: 0x000000010a17e280 mysqld`row_search_mvcc(unsigned char*, page_cur_mode_t, row_prebuilt_t*, unsigned long, unsigned long) + 6720
frame #10: 0x000000010a0a027e mysqld`ha_innobase::index_read(unsigned char*, unsigned char const*, unsigned int, ha_rkey_function) + 734
frame #11: 0x0000000109869b6c mysqld`handler::ha_index_read_map(unsigned char*, unsigned char const*, unsigned long, ha_rkey_function) + 140
frame #12: 0x0000000109f09065 mysqld`Rows_log_event::do_index_scan_and_update(Relay_log_info const*) + 821
frame #13: 0x0000000109f0a198 mysqld`Rows_log_event::do_apply_event(Relay_log_info const*) + 1064
frame #14: 0x0
- `* frame #0: 0x0000000109fd9c3a mysqld`btr_search_s_lock(dict_index_t const*) + 58`
- `    frame #1: 0x0000000109fdb37f mysqld`btr_search_guess_on_hash(dict_index_t*, btr_search_t*, dtuple_t const*, unsigned long, unsigned long, btr_cur_t*, unsigned long, mtr_t*) + 479`
- `    frame #2: 0x0000000109fc84a9 mysqld`btr_cur_search_to_nth_level(dict_index_t*, unsigned long, dtuple_t const*, page_cur_mode_t, unsigned long, btr_cur_t*, unsigned long, char const*, unsigned long, mtr_t*) + 649`
- `    frame #3: 0x000000010a177324 mysqld`row_search_on_row_ref(btr_pcur_t*, unsigned long, dict_table_t const*, dtuple_t const*, mtr_t*) + 164`
- `    frame #4: 0x000000010a17746f mysqld`row_get_clust_rec(unsigned long, unsigned char const*, dict_index_t*, dict_index_t**, mtr_t*) + 175`
- `    frame #5: 0x000000010a1988e5 mysqld`row_vers_impl_x_locked(unsigned char const*, dict_index_t*, unsigned long const*) + 293`
- `    frame #6: 0x000000010a0f39db mysqld`lock_rec_convert_impl_to_expl(buf_block_t const*, unsigned char const*, dict_index_t*, unsigned long const*) + 603`
- `    frame #7: 0x000000010a0f4914 mysqld`lock_sec_rec_read_check_and_lock(unsigned long, buf_block_t const*, unsigned char const*, dict_index_t*, unsigned long const*, lock_mode, unsigned long, que_thr_t*) + 596`
- `    frame #8: 0x000000010a1802f1 mysqld`sel_set_rec_lock(btr_pcur_t*, unsigned char const*, dict_index_t*, unsigned long const*, unsigned long, unsigned long, que_thr_t*, mtr_t*) + 193`
- `    frame #9: 0x000000010a17e280 mysqld`row_search_mvcc(unsigned char*, page_cur_mode_t, row_prebuilt_t*, unsigned long, unsigned long) + 6720`
- `    frame #10: 0x000000010a0a027e mysqld`ha_innobase::index_read(unsigned char*, unsigned char const*, unsigned int, ha_rkey_function) + 734`
- `    frame #11: 0x0000000109869b6c mysqld`handler::ha_index_read_map(unsigned char*, unsigned char const*, unsigned long, ha_rkey_function) + 140`
- `    frame #12: 0x0000000109f09065 mysqld`Rows_log_event::do_index_scan_and_update(Relay_log_info const*) + 821`
- `    frame #13: 0x0000000109f0a198 mysqld`Rows_log_event::do_apply_event(Relay_log_info const*) + 1064`
- `    frame #14: 0x0000000109f4bd42 mysqld`apply_event_and_update_pos(Log_event**, THD*, Relay_log_info*) + 530`
- `    frame #15: 0x0000000109f44f46 mysqld`handle_slave_sql + 4438`
**结论**
通过测试发现使用slave_rows_search_algorithms= INDEX_SCAN,HASH_SCAN 配置在此场景下回放binlog会有大幅性能改善，这种方式会有一定内存开销，所以要保障内存足够创建hash表，才会看到性能提升。
对于此问题的改进建议：
1. 避免无where条件的delete或update操作大表，如果需要全表delete请使用truncate操作
2. 在binlog row模式下表结构最好能有主键
3. 将slave_rows_search_algorithms设置为 INDEX_SCAN,HASH_SCAN ，会有一定性能改善。
**近期社区动态**
[**第三期 社区技术内容征稿**](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247484778&idx=2&sn=0050d6c324e4d958950d34a29c2f8994&chksm=fc96e7f5cbe16ee3eb36d47a15e19a89ed459c8d24588a080d1bb849dc6d5f0816a72aafe35f&scene=21#wechat_redirect)
**所有稿件，一经采用，均会为作者署名。**
**征稿主题：**MySQL、分布式中间件DBLE、数据传输组件DTLE相关的技术内容
**活动时间：**2019年6月11日 &#8211; 7月11日
**本期投稿奖励**
投稿成功：京东卡200元*1
优秀稿件：京东卡200元*1+社区定制周边（包含：定制文化衫、定制伞、鼠标垫）
**优秀稿件评选，文章获得****“好看****”****数量排名前三****的稿件为本期优秀稿件。**
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/征稿海报.jpg)