# 新特新解读 | MySQL 8.0 对  count(*)的优化

**原文链接**: https://opensource.actionsky.com/20190802-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-08-02T00:48:07-08:00

---

> 摘要：MySQL 8.0 取消了 sql_calc_found_rows 的语法，以后求表 count(*) 的写法演进为直接 select。
我们知道，MySQL 一直依赖对 count(*) 的执行很头疼。很早的时候，MyISAM 引擎自带计数器，可以秒回；不过 InnoDB 就需要实时计算，所以很头疼。以前有多方法可以变相解决此类问题，比如：
**1. 模拟 MyISAM 的计数器**比如表 ytt1，要获得总数，我们建立两个触发器分别对 insert/delete 来做记录到表 ytt1_count，这样只需要查询表 ytt1_count 就能拿到总数。ytt1_count 这张表足够小，可以长期固化到内存里。不过缺点就是有多余的触发器针对 ytt1 的每行操作，写性能降低。这里需要权衡。
**2. 用 MySQL 自带的 sql_calc_found_rows 特性来隐式计算**依然是表 ytt1，不过每次查询的时候用 sql_calc_found_rows 和 found_rows() 来获取总数，比如：
- `   mysql> select sql_calc_found_rows * from ytt1 where 1  order by id desc limit 1;`
- `    +------+------+`
- `    | id   | r1   |`
- `    +------+------+`
- `    | 3072 |   73 |`
- `    +------+------+`
- `    1 row in set, 1 warning (0.00 sec)`
- 
- `    mysql> show warnings;`
- `    +---------+------+-------------------------------------------------------------------------------------------------------------------------+`
- `    | Level   | Code | Message                                                                                                                 |`
- `    +---------+------+-------------------------------------------------------------------------------------------------------------------------+`
- `    | Warning | 1287 | SQL_CALC_FOUND_ROWS is deprecated and will be removed in a future release. Consider using two separate queries instead. |`
- `    +---------+------+-------------------------------------------------------------------------------------------------------------------------+`
- `    1 row in set (0.00 sec)`
- 
- `    mysql> select found_rows() as 'count(*)';`
- `    +----------+`
- `    | count(*) |`
- `    +----------+`
- `    |     3072 |`
- `    +----------+`
- `    1 row in set, 1 warning (0.00 sec)`
这样的好处是写法简单，用的是 MySQL 自己的语法。缺点也有，大概有两点：1. sql_calc_found_rows 是全表扫。2. found_rows() 函数是语句级别的存储，有很大的不确定性，所以在 MySQL 主从架构里，语句级别的行级格式下，从机数据可能会不准确。不过行记录格式改为 ROW 就 OK。所以最大的缺点还是第一点。**从 warnings 信息看，这种是 MySQL 8.0 之后要淘汰的语法。**
**3. 从数据字典里面拿出来粗略的值**
- `   mysql> select table_rows from information_schema.tables where table_name = 'ytt1';`
- `    +------------+`
- `    | TABLE_ROWS |`
- `    +------------+`
- `    |       3072 |`
- `    +------------+`
- `    1 row in set (0.12 sec)`
那这样的适合新闻展示，比如行数非常多，每页显示几行，一般后面的很多大家也都不怎么去看。缺点是数据不是精确值。
**4. 根据表结构特性特殊的取值**
这里假设表 ytt1 的主键是连续的，并且没有间隙，那么可以直接- `  mysql> select max(id) as cnt from ytt1;`
- `    +------+`
- `    | cnt  |`
- `    +------+`
- `    | 3072 |`
- `    +------+`
- `    1 row in set (0.00 sec)`
不过这种对表的数据要求比较高。
**5. 标准推荐取法（MySQL 8.0.17 建议）**
MySQL 8.0 建议用常规的写法来实现。- `   mysql> select * from ytt1 where 1 limit 1;`
- `    +----+------+`
- `    | id | r1   |`
- `    +----+------+`
- `    | 87 |    1 |`
- `    +----+------+`
- `    1 row in set (0.00 sec)`
- 
- `    mysql> select count(*) from ytt1;`
- `    +----------+`
- `    | count(*) |`
- `    +----------+`
- `    |     3072 |`
- `    +----------+`
- `    1 row in set (0.01 sec)`
第五种写法是 MySQL 8.0.17 推荐的，也就是说以后大部分场景直接实时计算就 OK 了。MySQL 8.0.17 以及在未来的版本都取消了sql_calc_found_rows 特性，可以查看第二种方法里的 warnings 信息。相比 MySQL 5.7，8.0 对 count(*) 做了优化，没有必要在用第二种写法了。我们来看看 8.0 比 5.7 在此类查询是否真的有优化？MySQL 5.7- `    mysql> select version();`
- `    +------------+`
- `    | version()  |`
- `    +------------+`
- `    | 5.7.27-log |`
- `    +------------+`
- `    1 row in set (0.00 sec)`
- 
- `    mysql> explain format=json select count(*) from ytt1\G`
- `    *************************** 1. row ***************************`
- `    EXPLAIN: {`
- `      "query_block": {`
- `        "select_id": 1,`
- `        "cost_info": {`
- `          "query_cost": "622.40"`
- `        },`
- `        "table": {`
- `          "table_name": "ytt1",`
- `          "access_type": "index",`
- `          "key": "PRIMARY",`
- `          "used_key_parts": [`
- `            "id"`
- `          ],`
- `          "key_length": "4",`
- `          "rows_examined_per_scan": 3072,`
- `          "rows_produced_per_join": 3072,`
- `          "filtered": "100.00",`
- `          "using_index": true,`
- `          "cost_info": {`
- `            "read_cost": "8.00",`
- `            "eval_cost": "614.40",`
- `            "prefix_cost": "622.40",`
- `            "data_read_per_join": "48K"`
- `          }`
- `        }`
- `      }`
- `    }`
- `    1 row in set, 1 warning (0.00 sec)`
MySQL 8.0 下执行同样的查询- `   mysql> select version();`
- `    +-----------+`
- `    | version() |`
- `    +-----------+`
- `    | 8.0.17    |`
- `    +-----------+`
- `    1 row in set (0.00 sec)`
- 
- `    mysql> explain format=json select count(*) from ytt1\G`
- `    *************************** 1. row ***************************`
- `    EXPLAIN: {`
- `      "query_block": {`
- `        "select_id": 1,`
- `        "cost_info": {`
- `          "query_cost": "309.95"`
- `        },`
- `        "table": {`
- `          "table_name": "ytt1",`
- `          "access_type": "index",`
- `          "key": "PRIMARY",`
- `          "used_key_parts": [`
- `            "id"`
- `          ],`
- `          "key_length": "4",`
- `          "rows_examined_per_scan": 3072,`
- `          "rows_produced_per_join": 3072,`
- `          "filtered": "100.00",`
- `          "using_index": true,`
- `          "cost_info": {`
- `            "read_cost": "2.75",`
- `            "eval_cost": "307.20",`
- `            "prefix_cost": "309.95",`
- `            "data_read_per_join": "48K"`
- `          }`
- `        }`
- `      }`
- `    }`
- `    1 row in set, 1 warning (0.00 sec)`
从以上结果看出，第二个 SQL 性能（cost_info）相对第一个提升了一倍。
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)