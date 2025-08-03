# 技术分享 | explain format=json 详解

**原文链接**: https://opensource.actionsky.com/20210301-explain/
**分类**: 技术干货
**发布时间**: 2021-03-01T00:41:53-08:00

---

作者：胡呈清
爱可生 DBA 团队成员，擅长故障分析、性能优化，个人博客：https://www.jianshu.com/u/a95ec11f67a8，欢迎讨论。
本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
explain format=json 可以打印详细的执行计划成本，下面两个示例将告诉你如何查看成本输出，以及如何计算成本。
表结构如下：
`mysql> show create table sbtest1\G
*************************** 1. row ***************************
       Table: sbtest1
Create Table: CREATE TABLE `sbtest1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` varchar(90) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4316190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
##注意sbtest3无主键
mysql> show create table sbtest3\G
*************************** 1. row ***************************
       Table: sbtest3
Create Table: CREATE TABLE `sbtest3` (
  `id` int(11) NOT NULL,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` varchar(66) COLLATE utf8mb4_bin DEFAULT NULL,
  KEY `k_3` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin`
## 示例 1
```
mysql> explain format=json select * from sbtest3 where id<100 and k<200\G
*************************** 1. row ***************************
EXPLAIN: {
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "26.21"            ##查询总成本
    },
    "table": {
      "table_name": "sbtest3",        ##表名
      "access_type": "range",         ##访问数据的方式是range，即索引范围查找
      "possible_keys": [
        "k_3"
      ],
      "key": "k_3",                   ##使用索引
      "used_key_parts": [
        "k"
      ],
      "key_length": "4",
      "rows_examined_per_scan": 18,   ##扫描 k_3 索引的行数：18（满足特定条件时使用index dive可得到真实行数）
      "rows_produced_per_join": 5,    ##在扫描索引后估算满足id<100条件的行数：5
      "filtered": "33.33",            ##在扫描索引后估算满足其他条件id<100的数据行占比
      "index_condition": "(`sbtest`.`sbtest3`.`k` < 200)",     ##索引条件
      "cost_info": {
        "read_cost": "25.01",         ##这里包含了所有的IO成本+部分CPU成本
        "eval_cost": "1.20",          ##计算扇出的CPU成本
        "prefix_cost": "26.21",       ##read_cost+eval_cost
        "data_read_per_join": "4K"
      },
      "used_columns": [
        "id",
        "k",
        "c",
        "pad"
      ],
      "attached_condition": "(`sbtest`.`sbtest3`.`id` < 100)"
    }
  }
}
```
#### eval_cost
这个很简单，就是计算扇出的 CPU 成本。应用条件 k<200 时，需要扫描索引 18行，这里 18 是精确值（index dive），然后优化器用了一种叫启发式规则（heuristic）的算法估算出其中满足条件 id<100 的比例为 33.33%，进行 `18*33.33%` 次计算的 CPU 成本等于 `18*33.33%*0.2=1.2`，这里 0.2 是成本常数（即 row_evaluate_cost ）。
**注意：rows_examined_per_scan*filtered 才是扇出数，不能简单的用 rows_produced_per_join 来表示。**
#### read_cost
这里包含了所有的 IO 成本 +（CPU 成本 &#8211; eval_cost）。我们先看下这个SQL的总成本应该怎么算：
访问二级索引 k_3 的成本：
- IO 成本 = `1*1.0`
查询优化器粗暴的认为读取索引的一个范围区间的 I/O 成本和读取一个页面是相同的，这个 SQL 中 k 字段的筛选范围只有 1 个：k < 200，而读取一个页面的 IO 成本为 1.0（即 io_block_read_cost）；
- CPU 成本 = `18*0.2`
从 k 索引中取出 18 行数据后，实际还要再计算一遍，每行计算的成本为 0.2。
然后因为 select * 以及 where id<100 需要的数据都不在索引 k_3 中，所以还需要回表，回表成本：
- IO 成本 = `18*1.0`
从索引中取出满足 k<200 的数据一共是 18 行，所以 = `18*1.0`；
- CPU 成本 = `18*0.2`
从这 18 行完整的数据中计算满足 id<100 的数据，所以也需要计算 18 次。
总成本 = `1*1.0+18*0.2+18*1+18*02=26.2`。因为 eval_cost 算的是扇出的 CPU 成本：`18*33.33%*0.2`，所以 `read_cost = 回表的 CPU 成本 - eval_cost`，也可以这么算 `rows_examined_per_scan*(1-filtered)*0.2`。
## 示例 2
`mysql> explain format=json select t1.id from sbtest1 t1 join sbtest3 t3 \
on t1.id=t3.id and t3.k<200 and t3.id<100\G
*************************** 1. row ***************************
EXPLAIN: {
  "query_block": {
    "select_id": 1,
    "cost_info": {
      "query_cost": "33.41"                      ##查询总成本
    },
    "nested_loop": [                            ##join算法：NLJ
      {
        "table": {
          "table_name": "t3",                   ##t3是驱动表
          "access_type": "range",               ##访问数据的方式是range，即索引范围查找
          "possible_keys": [
            "k_3"
          ],
          "key": "k_3",                         ##使用的索引：k_3
          "used_key_parts": [                   ##索引字段：k
            "k"
          ],
          "key_length": "4",
          "rows_examined_per_scan": 18,         ##k_3索引扫描行数：18
          "rows_produced_per_join": 5,          ##（估算值）扫描索引18行后，满足条件id<200的行数
          "filtered": "33.33",                  ##（估算值）扫描索引18行后，满足条件id<200的数据占扫描行数的比例，即驱动表扇出
          "index_condition": "(`sbtest`.`t3`.`k` < 200)",
          "cost_info": {
            "read_cost": "25.01",              ##这里包含了所有的IO成本+部分CPU成本
            "eval_cost": "1.20",               ##计算扇出的CPU成本
            "prefix_cost": "26.21",            ##驱动表的总成本：read_cost+eval_cost
            "data_read_per_join": "4K"
          },
          "used_columns": [
            "id",
            "k"
          ],
          "attached_condition": "(`sbtest`.`t3`.`id` < 100)"
        }
      },
      {
        "table": {
          "table_name": "t1",                  ##t1为被驱动表
          "access_type": "eq_ref",             ##关联查询时访问驱动表方式是通过主键或唯一索引的等值查询
          "possible_keys": [
            "PRIMARY"
          ],
          "key": "PRIMARY",                    ##使用索引为主键
          "used_key_parts": [                  ##索引字段为id
            "id"
          ],
          "key_length": "4",
          "ref": [
            "sbtest.t3.id"
          ],
          "rows_examined_per_scan": 1,         ##关联查询时，每次扫描被驱动表1行数据（使用主键）
          "rows_produced_per_join": 5,         ##被驱动表需要查询的次数，不是准确的驱动表扇出数
          "filtered": "100.00",                ##满足关联条件数据占扫描行数的比例，被驱动表上看这个没啥意义
          "using_index": true,
          "cost_info": {                       ##驱动表扇出数：rows_examined_per_scan*filtered,即18*33.33%=6行
            "read_cost": "6.00",               ##单次查询被驱动表的IO成本*驱动表扇出数。6*1.0=6，1.0为成本常数
            "eval_cost": "1.20",               ##单次查询被驱动表的CPU成本*驱动表扇出数。6*0.2=1.2，0.2位成本常数
            "prefix_cost": "33.41",            ##查询总成本=驱动表的总成本+被驱动表的(read_cost+eval_cost)
            "data_read_per_join": "5K"
          },
          "used_columns": [
            "id"
          ]
        }
      }
    ]
  }
}`
join 查询的总成本计算公式简化：`连接查询总成本 = 访问驱动表的成本 + 驱动表扇出数 * 单次访问被驱动表的成本`。**[explain 执行计划详解 1 ](https://opensource.actionsky.com/20210202-explain/)**中有解释 filtered 在关联查询中的重要性。
在上面示例中：访问驱动表的成本 = 26.21，驱动表扇出数 = 18*33.33% = 6，单次访问驱动表的成本 = 1.0+0.2 总成本=26.21+6(1.0+0.2)=33.41
**注意：驱动表和被驱动表的 read_cost、eval_cost 代表不一样的成本。**
**相关推荐：**
[技术分享 | EXPLAIN 执行计划详解（2）&#8211;Extra](https://opensource.actionsky.com/20210208-explain/)
[技术分享 | EXPLAIN 执行计划详解（1）](https://opensource.actionsky.com/20210202-explain/)
[技术分享 | mysqlsh 命令行模式 & 密码保存](https://opensource.actionsky.com/20210126-mysqlsh/)