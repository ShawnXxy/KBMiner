# 新特性解读 | MySQL 8.0 关于 json 到表的转换的新特性

**原文链接**: https://opensource.actionsky.com/20190621-mysql-json/
**分类**: MySQL 新特性
**发布时间**: 2019-06-21T01:22:49-08:00

---

我们知道，JSON是一种轻量级的数据交互的格式，大部分NO SQL数据库的存储都用JSON。MySQL从5.7开始支持JSON格式的数据存储的新特性，并且新增了很多JSON相关函数。MySQL 8.0 又带来了一个新的把JSON转换为TABLE的函数JSON_TABLE，实现了JSON到表的转换。
**举例一**
我们看下简单的例子：
简单定义一个两级JSON 对象
mysql> set @ytt='{"name":[{"a":"ytt","b":"action"},  {"a":"dble","b":"shard"},{"a":"mysql","b":"oracle"}]}';
Query OK, 0 rows affected (0.00 sec)
第一级：
mysql> select json_keys(@ytt);
+-----------------+
| json_keys(@ytt) |
+-----------------+
| ["name"]        |
+-----------------+
1 row in set (0.00 sec)
第二级：
mysql> select json_keys(@ytt,'$.name[0]');
+-----------------------------+
| json_keys(@ytt,'$.name[0]') |
+-----------------------------+
| ["a", "b"]                  |
+-----------------------------+
1 row in set (0.00 sec)
我们使用MySQL 8.0 的JSON_TABLE 来转换 @ytt。
mysql> select * from json_table(@ytt,'$.name[*]' columns (f1 varchar(10) path '$.a', f2 varchar(10) path '$.b')) as tt;
+-------+--------+
| f1    | f2     |
+-------+--------+
| ytt   | action |
| dble  | shard  |
| mysql | oracle |
+-------+--------+
3 rows in set (0.00 sec)
**举例二**
再来一个复杂点的例子，用的是EXPLAIN 的JSON结果集。
JSON 串 @json_str1。
set @json_str1 = ' {
"query_block": {
"select_id": 1,
"cost_info": {
"query_cost": "1.00"
},
"table": {
"table_name": "bigtable",
"access_type": "const",
"possible_keys": [
"id"
],
"key": "id",
"used_key_parts": [
"id"
],
"key_length": "8",
"ref": [
"const"
],
"rows_examined_per_scan": 1,
"rows_produced_per_join": 1,
"filtered": "100.00",
"cost_info": {
"read_cost": "0.00",
"eval_cost": "0.20",
"prefix_cost": "0.00",
"data_read_per_join": "176"
},
"used_columns": [
"id",
"log_time",
"str1",
"str2"
]
}
}
}';
第一级：
mysql> select json_keys(@json_str1) as 'first_object';
+-----------------+
| first_object    |
+-----------------+
| ["query_block"] |
+-----------------+
1 row in set (0.00 sec)
第二级：
mysql> select json_keys(@json_str1,'$.query_block') as 'second_object';
+-------------------------------------+
| second_object                       |
+-------------------------------------+
| ["table", "cost_info", "select_id"] |
+-------------------------------------+
1 row in set (0.00 sec)
第三级：
mysql>  select json_keys(@json_str1,'$.query_block.table') as 'third_object'\G
*************************** 1. row ***************************
third_object: 
[
"key",
"ref",
"filtered",
"cost_info",
"key_length",
"table_name",
"access_type",
"used_columns",
"possible_keys",
"used_key_parts",
"rows_examined_per_scan",
"rows_produced_per_join"
]
1 row in set (0.01 sec)
第四级：
mysql> select json_extract(@json_str1,'$.query_block.table.cost_info') as 'forth_object'\G
*************************** 1. row ***************************
forth_object: {
"eval_cost":"0.20",
"read_cost":"0.00",
"prefix_cost":"0.00",
"data_read_per_join":"176"
}
1 row in set (0.00 sec)
那我们把这个JSON 串转换为表。
SELECT * FROM JSON_TABLE(@json_str1,
"$.query_block"
COLUMNS(
rowid FOR ORDINALITY,
NESTED PATH '$.table' 
COLUMNS (
a1_1 varchar(100) PATH '$.key',
a1_2 varchar(100) PATH '$.ref[0]',
a1_3 varchar(100) PATH '$.filtered',
nested path '$.cost_info' 
columns (
a2_1 varchar(100) PATH '$.eval_cost' ,
a2_2 varchar(100) PATH '$.read_cost',
a2_3 varchar(100) PATH '$.prefix_cost',
a2_4 varchar(100) PATH '$.data_read_per_join'
),
a3 varchar(100) PATH '$.key_length',
a4 varchar(100) PATH '$.table_name',
a5 varchar(100) PATH '$.access_type',
a6 varchar(100) PATH '$.used_key_parts[0]',
a7 varchar(100) PATH '$.rows_examined_per_scan',
a8 varchar(100) PATH '$.rows_produced_per_join',
a9 varchar(100) PATH '$.key'
),
NESTED PATH '$.cost_info' 
columns (
b1_1 varchar(100) path '$.query_cost'
),
c INT path "$.select_id"
)
) AS tt;
+-------+------+-------+--------+------+------+------+------+------+----------+-------+------+------+------+------+------+------+
| rowid | a1_1 | a1_2  | a1_3   | a2_1 | a2_2 | a2_3 | a2_4 | a3   | a4       | a5    | a6   | a7   | a8   | a9   | b1_1 | c    |
+-------+------+-------+--------+------+------+------+------+------+----------+-------+------+------+------+------+------+------+
|     1 | id   | const | 100.00 | 0.20 | 0.00 | 0.00 | 176  | 8    | bigtable | const | id   | 1    | 1    | id   | NULL |    1 |
|     1 | NULL | NULL  | NULL   | NULL | NULL | NULL | NULL | NULL | NULL     | NULL  | NULL | NULL | NULL | NULL | 1.00 |    1 |
+-------+------+-------+--------+------+------+------+------+------+----------+-------+------+------+------+------+------+------+
2 rows in set (0.00 sec)
当然，JSON_table 函数还有其他的用法，我这里不一一列举了，详细的参考手册。
### 社区近期动态
**[第三期 社区技术内容征稿](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247484778&idx=2&sn=0050d6c324e4d958950d34a29c2f8994&chksm=fc96e7f5cbe16ee3eb36d47a15e19a89ed459c8d24588a080d1bb849dc6d5f0816a72aafe35f&scene=21#wechat_redirect)****![👈](.img/e89bf7c8.svg)**
**所有稿件，一经采用，均会为作者署名。**
**征稿主题：**MySQL、分布式中间件DBLE、数据传输组件DTLE相关的技术内容
**活动时间：**2019年6月11日 – 7月11日
**本期投稿奖励**
投稿成功：京东卡200元*1
优秀稿件：京东卡200元*1+社区定制周边（包含：定制文化衫、定制伞、鼠标垫）
**优秀稿件评选，文章获得****“好看****”****数量排名前三****的稿件为本期优秀稿件。**
![](https://opensource.actionsky.com/wp-content/uploads/2019/06/第三期-社区征稿-海报-1.png)