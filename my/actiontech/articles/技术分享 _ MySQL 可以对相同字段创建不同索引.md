# 技术分享 | MySQL 可以对相同字段创建不同索引？

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-mysql-%e5%8f%af%e4%bb%a5%e5%af%b9%e7%9b%b8%e5%90%8c%e5%ad%97%e6%ae%b5%e5%88%9b%e5%bb%ba%e4%b8%8d%e5%90%8c%e7%b4%a2%e5%bc%95%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2023-11-13T22:14:37-08:00

---

Oracle 不允许同一个字段存在两个相同索引，但这个和 MySQL 的设计不太相同，通过实验，了解一下 MySQL 这种场景的情况。
> 
作者：刘晨，网名 bisal ，具有十年以上的应用运维工作经验，目前主要从事数据库应用研发能力提升和技术管理相关的工作，Oracle ACE（Alumni），腾讯云TVP，拥有 Oracle OCM & OCP 、EXIN DevOps Master 、SCJP 等国际认证，国内首批 Oracle YEP 成员，OCMU 成员，《DevOps 最佳实践》中文译者之一，CSDN & ITPub 专家博主，公众号”bisal的个人杂货铺”，长期坚持分享技术文章，多次在线上和线下分享技术主题。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 900 字，预计阅读需要 3 分钟。
同事问了个问题，MySQL 的某个测试库，发现有这种情况：
- 给已设置为主键的列又加了一次索引，如下前两条 SQL 语句。
- 给同一个字段加了 2 次索引，如下后两条 SQL 语句。
`# 情况 1
ALTER TABLE test ADD PRIMARY KEY USING BTREE(ID);
ALTER TABLE test ADD INDEX idx_test01 USING BTREE(ID);
# 情况 2
ALTER TABLE test ADD INDEX idx_test02 USING BTREE(UPDATED):
ALTER TABLE test ADD INDEX idx_test03 USING BTREE(UPDATED);
`
正常情况只需要一条 SQL 就行？
**这种情况是不是没有意义？**
这两个问题考察的都是关于索引的基础知识，如果对此很熟悉，答案不言自明，即使不熟悉，只需要做些简单的测试，就可以了解，加深印象。
# 测试一
数据库版本：MySQL 8.0，为表 `t` 设置主键，再对同字段加个索引可以执行成功。
`alter table t add primary key using btree(id);
alter table t add index idx_t_id using btree(id);
`
对字段 `c1` 创建两个索引，都可以执行成功。
`alter table tbl add index idx_t_001 using btree(c1);
alter table tbl add index idx_t_002 using btree(c1);
`
以上实验说明：**MySQL 中可以对相同的字段创建多次相同的索引。**
# 测试二
通过 `explain`，可以验证出对于同时存在 PRIMARY KEY 和普通索引的字段作为检索条件时，优化器会选择 PRIMARY KEY 作为 key，这种选择应该和 MySQL 以索引组织表存储的形式有关，对于同时存在两个索引名称的相同字段作为检索条件时，优化器会选择先创建的索引作为 key，这倒是很像 Oracle 中 RBO 对于索引选择的顺序判断逻辑（可能有些不严谨，但是因为完全是两个相同的索引（Oracle 终不会允许此种情况），cost 应该完全一致，所以选择谁，好像无所谓）。
`bisal@mysqldb 13:02:  [test]> explain select * from tbl where id=1;
+----+-------------+-------+------------+-------+------------------+---------+---------+-------+------+----------+-------+
| id | select_type | table | partitions | type  | possible_keys    | key     | key_len | ref   | rows | filtered | Extra |
+----+-------------+-------+------------+-------+------------------+---------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | tbl   | NULL       | const | PRIMARY,idx_t_id | PRIMARY | 4       | const |    1 |   100.00 | NULL  |
+----+-------------+-------+------------+-------+------------------+---------+---------+-------+------+----------+-------+
1 row in set, 1 warning (0.07 sec)
bisal@mysqldb 13:03:  [test]> explain select * from tbl where c1='a';
+----+-------------+-------+------------+------+---------------------+-----------+---------+-------+------+----------+-------+
| id | select_type | table | partitions | type | possible_keys       | key       | key_len | ref   | rows | filtered | Extra |
+----+-------------+-------+------------+------+---------------------+-----------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | tbl   | NULL       | ref  | idx_t_001,idx_t_002 | idx_t_001 | 7       | const |    3 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------------+-----------+---------+-------+------+----------+-------+
1 row in set, 1 warning (0.00 sec)
`
以上实验说明 MySQL 对于相同字段的相同索引选择方面的逻辑。
# 测试三
从效果上看，这两个索引，保留一个即可，因为这两个索引只是名称不同，索引字段相同的，实际上就是相同的索引。
`ALTER TABLE test ADD INDEX idx_test02 USING BTREE(UPDATED):
ALTER TABLE test ADD INDEX idx_test03 USING BTREE(UPDATED);
`
但对于主键和索引的这两个，需要用主键这个。因为这两个最主要的区别就是主键除了包含索引外，还需保证唯一，而此处的索引，就是普通索引，不是唯一索引，因此从逻辑上，这两个是不等价。但是由于主键包含了索引，因此可以删除第二个索引，它属于重复的，主键的定义包含了索引的定义。
`ALTER TABLE test ADD PRIMARY KEY USING BTREE(ID);
ALTER TABLE test ADD INDEX idx_test01 USING BTREE(ID);
`
MySQL 之所以存在上面的这些问题，因为它允许创建不同名称相同索引字段的索引，但是如果是 Oracle，情况会是相同？
Oracle 19c，在主键字段上创建索引，会提示 **此列列表已索引** 的错误。在相同字段上创建第二个索引，也是提示 **此列列表已索引** 的错误。说明 Oracle 中根本不允许同一个字段存在两个相同索引的情况。
# 总结
因此只能说不同的数据库，设计理念不同，Oracle 更严谨些，MySQL 的容错性鲁棒性更突出（可能不太准确）。使用的时候，需要对这些基础能够有所了解，才可以针对合适的场景选择合适的操作。