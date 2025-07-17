# 技术分享 | HASH_SCAN BUG 之迷惑行为大赏

**原文链接**: https://opensource.actionsky.com/20190531-hash_scan-bug/
**分类**: 技术干货
**发布时间**: 2019-05-31T02:43:03-08:00

---

## 迷惑行为大赏背景
我们知道，MySQL 有一个老问题，当表上无主键时，那么对于在该表上做的DML，如果是以ROW模式复制，则每一个行记录前镜像在备库都可能产生一次全表扫描（或者二级索引扫描），大多数情况下，这种开销都是非常不可接受的，并且产生大量的延迟。
在MySQL 5.6 中提供了一个新的参数：slave_rows_search_algorithms, 可以部分解决无主键表导致的复制延迟问题，其基本思路是对于在一个ROWS EVENT中的所有前镜像收集起来，然后在一次扫描全表时，判断HASH中的每一条记录进行更新。
> 
以上摘自印风大神的文章，具体效果和使用方式可以查看文章：
https://yq.aliyun.com/articles/41058。
### HASH_SCAN BUG 的迷惑行为
本文不是要继续讨论 slave_rows_search_algorithms 的原理，而是在使用 slave_rows_search_algorithms 参数时遇到一个坑，扑朔迷离的地方在于这不像一个bug，这又是一个bug，最后官方的操作更是让人看不懂。
#### 问题描述
row-based replication，主从数据一致情况下，slave sql 线程报错 Can&#8217;t find record。
#### 如何复现
**配置：**
slave_rows_search_algorithms = &#8216;INDEX_SCAN,HASH_SCAN&#8217;
binlog_format = ROW
**在主库上：**
- CREATE TABLE t1 ( A INT UNIQUE KEY, B INT ); insert into t1 values (1,2);
- 
replace into t1 values (1,3),(1,4);
- 
然后从库就会出现报错了。
- 
在从库上：set global slave_rows_search_algorithms=&#8217;INDEX_SCAN,TABLE_SCAN&#8217;; start slave; 问题解决
#### 或者用如下方法避免：
- 
将 UNIQUE KEY 调整为 PRIMARY KEY；
- 
将 replace into tt.t1 values (1,3),(1,4); 调整为 replace into tt.t1 values (1,3);replace into tt.t1 values (1,4);
#### 分析过程：
查看 slaverowssearch_algorithms 参数定义：
The default value is INDEX_SCAN,TABLE_SCAN, which means that all searches that can use indexes do use them, and searches without any indexes use table scans.
To use hashing for any searches that do not use a primary or unique key, set INDEX_SCAN,HASH_SCAN. Specifying INDEX_SCAN,HASH_SCAN has the same effect as specifying INDEX_SCAN,TABLE_SCAN,HASH_SCAN, which is allowed.
Do not use the combination TABLE_SCAN,HASH_SCAN. This setting forces hashing for all searches. It has no advantage over INDEX_SCAN,HASH_SCAN, and it can lead to “record not found” errors or duplicate key errors in the case of a single event containing multiple updates to the same row, or updates that are order-dependent.
**（1）根据手册描述，可以理解为：**
从库定位数据可选项有 INDEX_SCAN、HASH_SCAN、TABLE_SCAN，优先级是依次递减的。也就是说如果有主键，走 INDEX_SCAN，没主键则根据设置走 HASH_SCAN 还是 TABLE_SCAN（而且如果两者都配了，则优先 HASH_SCAN）；
无主键设置 INDEX_SCAN,HASH_SCAN，可以提升从库回访效率，降低延迟；
如果走了 HASH_SCAN，当对同一行数据同时更新多次时，会导致无法找到行记录。
看到这里，手册已经说明原因了。但是矛盾的地方在于手册有推荐使用 INDEX_SCAN,HASH_SCAN 的意思，并且 8.0.2 版本开始的默认值已经修改为：INDEX_SCAN,HASH_SCAN
**（2）针对上面的疑问提交SR**
Oracle 工程师回应这是 HASH_SCAN 的 bug，修复到了 MySQL8.0.17（还没有正式发布）：
It happens when one row is updated twice within an Update_rows_log_event. HASH_SCAN will put both rows in a hash map. Then it iterates over the rows of the table, looks up each row in the hash. If any row is found, it applies the update. Since it only makes one lookup per row, it will miss the second update. In the end, it checks that all rows in the hash were applied and generates an error otherwise. This is what is seen in the bug report.
等等，为什么只修复到 8.0 而没在 5.7 修复？再根据之前就有的疑问，我来脑补一波：
- 文档写了在某些情况 HASH_SCAN 有这个问题（吐槽：HASH_SCAN 就是优化无主键情况从库复制效率的，但是无主键且对同一行数据同时更新多次时 HASH_SCAN 又会导致从库无法找到记录，那我用还是不用呢？黑人问号.gif），所以暂时我先假设“这不是个 bug”；
- 
Oracle 工程师反手甩给我一个 bug 报告，啪啪打脸，官方承认这就是一个 bug；
- 
官方好像也认为有点不对劲，一拍脑袋，咱们只在 8.0 修复，把锅甩给 “8.0.2 的默认值修改成了 HASH_SCAN”。
这个迷惑行为可以用一句经典总结：it&#8217;s not a bug,it&#8217;s a feature!
#### 解决方案
- 给表添加主键（规范必须有主键才是王道）；
- 
修改参数 slave_rows_search_algorithms=&#8217;INDEX_SCAN,TABLE_SCAN&#8217;；
- 
最符合初衷的做法是升级到 8.0.17，可惜这步对于绝大多数生产环境来说都太大了。
##### 社区近期动态
[![](.img/dfabe8a3.jpg)](https://i.loli.net/2019/05/28/5cecd1ad59d4c73631.jpg)
**报名详情 ↓**
**[6月15日 上海站 | 分布式中间件DBLE用户见面会](http://https://event.31huiyi.com/1633790994)**
本次举办的DBLE用户见面会，是自2017年10月24日数据库中间件DBLE发布以来，**首次线下互动式分享会议**。
来爱可生总部研发中心，与研发、测试、产品、社区团队面对面，遇到志同道合的朋友，更有丰富精美的周边产品等着你！
**会议时间：2019年06月15日13:00—17:00
会议地点：爱可生研发中心，上海市徐汇区虹梅路1905号远中科研楼甲幢7层**