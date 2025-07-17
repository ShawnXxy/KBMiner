# 故障分析 | MySQL 相同 SQL 不同环境执行时间不一样案例分析

**原文链接**: https://opensource.actionsky.com/20230213-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-02-12T21:37:55-08:00

---

作者：付祥
现居珠海，主要负责 Oracle、MySQL、mongoDB 和 Redis 维护工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 1、问题现象
开发反馈同一条SQL在qa环境执行需要0.1s,而在dev环境需要0.3~0.5s，SQL如下：
SELECT machine.id,
machine.asset_number,
machine.sn,
machine.state,
machine.idc_id,
machine.cabinet_id,
machine.cabinet_order,
machine.unit_size,
machine.brand_model,
machine.buy_time,
machine.expiration_time,
machine.warranty,
machine.renewstart_time,
machine.renewend_time,
machine.warranty_company_id,
machine.renewal_type,
machine.check_hardware,
machine.machine_purchase_price,
machine.tags,
machine.memo,
machine.cpu_core_count,
machine.cpu_model,
machine.cpu_count,
machine.memory_count,
machine.memory_size,
machine.wire_standard,
machine.disk_num,
machine.netcard_total_count,
machine.netcard_1g,
machine.netcard_10g,
machine.os_version,
machine.kernel_version,
machine.raid,
machine.power,
machine.firmware,
machine.manage_card_ip,
machine.hostname,
machine.private_mac,
machine.public_mac,
machine.private_ip,
machine.public_ip,
machine.other_ips,
machine.create_time,
machine.update_time,
machine.creator,
machine.updater,
machine.delete_flag,
machine.disk_desc_id,
res.id res_id,
res.owner_company_code,
res.owner_company_name,
res.project_id,
res.project_group_id,
res.sub_project_id,
res.finance_product_id,
res.finance_product_name,
res.sub_project_name,
res.admin_id,
res.admin_name,
res.owner_id,
res.owner_name,
2 AS resource_type,
res.resource_id,
res.machine_usage_types,
res.machine_usage_names,
cdl1.display AS check_hardware_name,
cdl2.display AS state_name,
cdl3.display AS brand_model_name,
cdl4.display AS renewal_type_name,
cdl5.display AS power_name,
cdl6.display AS unit_size_name,
cec.company_name AS warranty_company_name,
cc.serial_number AS cabinet_name,
ci.name AS idc_name,
dd.disk_desc AS disk_desc_name,
machine.virtual_ip,
machine.qingteng_binded,
machine.qingteng_id,
machine.remark
FROM CMDB_PHYSICAL_MACHINE machine
LEFT JOIN cmdb_dropdown_list cdl1
ON (machine.check_hardware=cdl1.code and cdl1.type="HardwareCheck")
LEFT JOIN cmdb_dropdown_list cdl2
ON (machine.state=cdl2.code and cdl2.type="DeviceStatus")
LEFT JOIN cmdb_dropdown_list cdl3
ON (machine.brand_model=cdl3.code and cdl3.type="BrandModels")
LEFT JOIN cmdb_dropdown_list cdl4
ON (machine.renewal_type=cdl4.code and cdl4.type="RenewalType")
LEFT JOIN cmdb_dropdown_list cdl5
ON (machine.power=cdl5.code and cdl5.type="PowerInfo")
LEFT JOIN cmdb_dropdown_list cdl6
ON (machine.unit_size=cdl6.code and cdl6.type="UnitSize")
LEFT JOIN cmdb_external_company cec
ON (machine.warranty_company_id=cec.id)
LEFT JOIN cmdb_cabinet cc
ON (machine.cabinet_id=cc.id)
LEFT JOIN cmdb_disk_desc dd
ON (machine.disk_desc_id=dd.id)
inner JOIN cmdb_idc ci
ON (machine.idc_id=ci.id and ci.delete_flag=0)
left join cmdb_resource_group res
on (machine.id = res.resource_id and res.resource_type = 2)
where 1=1
AND machine.delete_flag=0
order by id desc
LIMIT 0,30
#### 2、分析
查看SQL执行计划，发现2个环境执行计划不一样，导致执行效率不同。
qa环境SQL执行计划：
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
| id | select_type | table   | partitions | type   | possible_keys               | key           | key_len | ref                              | rows | filtered | Extra       |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
|  1 | SIMPLE      | machine | NULL       | index  | NULL                        | PRIMARY       | 4       | NULL                             |    1 |    10.00 | Using where |
|  1 | SIMPLE      | cdl1    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where |
|  1 | SIMPLE      | cdl2    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    9 |   100.00 | Using where |
|  1 | SIMPLE      | ci      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.idc_id              |    1 |    10.00 | Using where |
|  1 | SIMPLE      | res     | NULL       | eq_ref | resource_id,idx_resource_id | resource_id   | 5       | omms.machine.id,const            |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | cdl3    | NULL       | ref    | idx_type_code               | idx_type_code | 124     | const,omms.machine.brand_model   |    1 |   100.00 | Using where |
|  1 | SIMPLE      | cdl4    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where |
|  1 | SIMPLE      | cdl5    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    2 |   100.00 | Using where |
|  1 | SIMPLE      | cdl6    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |   10 |   100.00 | Using where |
|  1 | SIMPLE      | cec     | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.warranty_company_id |    1 |   100.00 | Using where |
|  1 | SIMPLE      | cc      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.cabinet_id          |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | dd      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.disk_desc_id        |    1 |   100.00 | NULL        |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
12 rows in set, 1 warning (0.01 sec)
dev环境SQL执行计划：
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+----------------------------------------------------+
| id | select_type | table   | partitions | type   | possible_keys               | key           | key_len | ref                              | rows | filtered | Extra                                              |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+----------------------------------------------------+
|  1 | SIMPLE      | ci      | NULL       | ALL    | PRIMARY                     | NULL          | NULL    | NULL                             |    8 |    12.50 | Using where; Using temporary; Using filesort       |
|  1 | SIMPLE      | machine | NULL       | ALL    | NULL                        | NULL          | NULL    | NULL                             | 1976 |     1.00 | Using where; Using join buffer (Block Nested Loop) |
|  1 | SIMPLE      | res     | NULL       | eq_ref | resource_id,idx_resource_id | resource_id   | 5       | omms.machine.id,const            |    1 |   100.00 | NULL                                               |
|  1 | SIMPLE      | cdl1    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cdl2    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    9 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cdl3    | NULL       | ref    | idx_type_code               | idx_type_code | 124     | const,omms.machine.brand_model   |    1 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cdl4    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cdl5    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    2 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cdl6    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |   10 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cec     | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.warranty_company_id |    1 |   100.00 | Using where                                        |
|  1 | SIMPLE      | cc      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.cabinet_id          |    1 |   100.00 | NULL                                               |
|  1 | SIMPLE      | dd      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.disk_desc_id        |    1 |   100.00 | NULL                                               |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+----------------------------------------------------+
其中，qa环境选择machine作为驱动表，ci作为被驱动表，ci.id有主键索引，故表关联采用Index Nested Loop 算法，并利用主键索引有序性避免了排序，这里驱动表machine基数为1，实际上应该为30，而dev环境选择ci作为驱动表，machine是被驱动表，由于machine.idc_id列无索引，故表关联采用Block Nested Loop算法，且需要排序，导致了SQL执行效率不一样。
为何相同SQL不同环境执行计划不一样，带着这个疑问做了如下操作：
##### 2.1、检查表、索引、数据分布
结果：基本一致
##### 2.2、重新收集统计信息
结果：重新收集了dev环境表machine、ci统计信息，还是同样执行计划。
##### 2.3、数据库版本
结果：qa环境为5.7.34，dev环境为5.7.25，会不会因为版本差异，查看了参数optimizer_switch，发现5.7.34多了一个选项：prefer_ordering_index=on，官方文档解释如下：
Controls whether, in the case of a query having an ORDER BY or GROUP BY with a LIMIT clause, the optimizer tries to use an ordered index instead of an unordered index, a filesort, or some other optimization. This optimzation is performed by default whenever the optimizer determines that using it would allow for faster execution of the query.
Because the algorithm that makes this determination cannot handle every conceivable case (due in part to the assumption that the distribution of data is always more or less uniform), there are cases in which this optimization may not be desirable. Prior to MySQL 5.7.33, it ws not possible to disable this optimization, but in MySQL 5.7.33 and later, while it remains the default behavior, it can be disabled by setting the prefer_ordering_index flag to off.
当参数prefer_ordering_index为on，order by 带有limit时，优化器倾向于使用索引去避免排序，5.7.33以前默认就是打开的，5.7.33以后可以关闭。似乎也排除了版本差异，但心有不甘，抱着试试看态度把dev环境升级到了5.7.34，果然和版本差异无关，还是同样执行计划。
##### 2.4、STRAIGHT_JOIN人工干预执行计划
通过STRAIGHT_JOIN提示选择machine作为驱动表，利用其主键索引有序性避免排序
SELECT ......省略输出......
STRAIGHT_JOIN cmdb_idc ci
ON (machine.idc_id=ci.id and ci.delete_flag=0)
left join cmdb_resource_group res
on (machine.id = res.resource_id and res.resource_type = 2)
where 1=1
AND machine.delete_flag=0
order by id desc
LIMIT 0,30
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
| id | select_type | table   | partitions | type   | possible_keys               | key           | key_len | ref                              | rows | filtered | Extra       |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
|  1 | SIMPLE      | machine | NULL       | index  | NULL                        | PRIMARY       | 4       | NULL                             |    1 |    10.00 | Using where |
|  1 | SIMPLE      | res     | NULL       | eq_ref | resource_id,idx_resource_id | resource_id   | 5       | omms.machine.id,const            |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | cdl1    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where |
|  1 | SIMPLE      | cdl2    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    9 |   100.00 | Using where |
|  1 | SIMPLE      | cdl3    | NULL       | ref    | idx_type_code               | idx_type_code | 124     | const,omms.machine.brand_model   |    1 |   100.00 | Using where |
|  1 | SIMPLE      | cdl4    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where |
|  1 | SIMPLE      | cdl5    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    2 |   100.00 | Using where |
|  1 | SIMPLE      | cdl6    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |   10 |   100.00 | Using where |
|  1 | SIMPLE      | cec     | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.warranty_company_id |    1 |   100.00 | Using where |
|  1 | SIMPLE      | cc      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.cabinet_id          |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | dd      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.disk_desc_id        |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | ci      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.idc_id              |    1 |    12.50 | Using where |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
12 rows in set, 1 warning (0.00 sec)
这样虽然能解决问题，但是解决问题的方式并不优雅。
##### 2.5、分析SQL、改写SQL
为了排除干扰，将无关紧要left join表去掉，简化SQL如下：
SELECT *
FROM CMDB_PHYSICAL_MACHINE machine
JOIN cmdb_idc ci 
ON (machine.idc_id=ci.id and ci.delete_flag=0)
where 1=1
AND machine.delete_flag=0
order by machine.id desc
LIMIT 0,30;
dev和qa环境执行计划一致：
root@3306 omms>  explain SELECT *
->       FROM CMDB_PHYSICAL_MACHINE machine
->       JOIN cmdb_idc ci 
->         ON (machine.idc_id=ci.id and ci.delete_flag=0)
->      where 1=1
->        AND machine.delete_flag=0
->      order by machine.id desc
->      LIMIT 0,30;
+----+-------------+---------+------------+------+---------------+------+---------+------+------+----------+----------------------------------------------------+
| id | select_type | table   | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                                              |
+----+-------------+---------+------------+------+---------------+------+---------+------+------+----------+----------------------------------------------------+
|  1 | SIMPLE      | machine | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 2087 |    10.00 | Using where; Using temporary; Using filesort       |
|  1 | SIMPLE      | ci      | NULL       | ALL  | PRIMARY       | NULL | NULL    | NULL |   21 |     4.76 | Using where; Using join buffer (Block Nested Loop) |
+----+-------------+---------+------------+------+---------------+------+---------+------+------+----------+----------------------------------------------------+
2 rows in set, 1 warning (0.00 sec)
虽然选择machine作为驱动表，但是却选择了Block Nested Loop算法，也产生了排序，仔细分析SQL，其实条件ci.delete_flag=0是多余的，因为有效的机器所在机房一定是有效的，可以去跟开发核实，这个条件可以去掉，正是因为这个条件影响了驱动表选择，使得执行计划不稳定，将ci.delete_flag=0去掉后执行计划：
root@3306 omms>  explain SELECT *
->       FROM CMDB_PHYSICAL_MACHINE machine
->       JOIN cmdb_idc ci 
->         ON (machine.idc_id=ci.id)
->      where 1=1
->        AND machine.delete_flag=0
->      order by machine.id desc
->      LIMIT 0,30;
+----+-------------+---------+------------+--------+---------------+---------+---------+---------------------+------+----------+-------------+
| id | select_type | table   | partitions | type   | possible_keys | key     | key_len | ref                 | rows | filtered | Extra       |
+----+-------------+---------+------------+--------+---------------+---------+---------+---------------------+------+----------+-------------+
|  1 | SIMPLE      | machine | NULL       | index  | NULL          | PRIMARY | 4       | NULL                |   30 |    10.00 | Using where |
|  1 | SIMPLE      | ci      | NULL       | eq_ref | PRIMARY       | PRIMARY | 4       | omms.machine.idc_id |    1 |   100.00 | NULL        |
+----+-------------+---------+------------+--------+---------------+---------+---------+---------------------+------+----------+-------------+
2 rows in set, 1 warning (0.01 sec)
原始SQL，去掉ci.delete_flag=0条件后执行计划如下：
root@3306 omms> explain SELECT machine.id,
......省略输出......
->  inner JOIN cmdb_idc ci
->     ON (machine.idc_id=ci.id)
->   left join cmdb_resource_group res
->     on (machine.id = res.resource_id and res.resource_type = 2)
->  where 1=1
->    AND machine.delete_flag=0
->  order by id desc
->  LIMIT 0,30;
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
| id | select_type | table   | partitions | type   | possible_keys               | key           | key_len | ref                              | rows | filtered | Extra       |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
|  1 | SIMPLE      | machine | NULL       | index  | NULL                        | PRIMARY       | 4       | NULL                             |    1 |    10.00 | Using where |
|  1 | SIMPLE      | ci      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.idc_id              |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | res     | NULL       | eq_ref | resource_id,idx_resource_id | resource_id   | 5       | omms.machine.id,const            |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | cdl1    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where |
|  1 | SIMPLE      | cdl2    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    9 |   100.00 | Using where |
|  1 | SIMPLE      | cdl3    | NULL       | ref    | idx_type_code               | idx_type_code | 124     | const,omms.machine.brand_model   |    1 |   100.00 | Using where |
|  1 | SIMPLE      | cdl4    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    3 |   100.00 | Using where |
|  1 | SIMPLE      | cdl5    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |    2 |   100.00 | Using where |
|  1 | SIMPLE      | cdl6    | NULL       | ref    | idx_type_code               | idx_type_code | 62      | const                            |   10 |   100.00 | Using where |
|  1 | SIMPLE      | cec     | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.warranty_company_id |    1 |   100.00 | Using where |
|  1 | SIMPLE      | cc      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.cabinet_id          |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | dd      | NULL       | eq_ref | PRIMARY                     | PRIMARY       | 4       | omms.machine.disk_desc_id        |    1 |   100.00 | NULL        |
+----+-------------+---------+------------+--------+-----------------------------+---------------+---------+----------------------------------+------+----------+-------------+
12 rows in set, 1 warning (0.01 sec)
#### 3、总结
书写SQL时，心里要明白哪种执行计划是最优的，比如多张表关联时，是否可以适当利用标量子查询、排除干扰驱动表选择因素，使执行计划简单稳定。