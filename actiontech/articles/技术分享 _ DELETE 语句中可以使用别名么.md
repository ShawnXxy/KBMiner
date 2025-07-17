# 技术分享 | DELETE 语句中可以使用别名么？

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-delete-%e8%af%ad%e5%8f%a5%e4%b8%ad%e5%8f%af%e4%bb%a5%e4%bd%bf%e7%94%a8%e5%88%ab%e5%90%8d%e4%b9%88%ef%bc%9f/
**分类**: 技术干货
**发布时间**: 2023-11-21T23:57:43-08:00

---

某天，正按照业务的要求删除不需要的数据，在执行 DELETE 语句时，竟然出现了报错！
> 
作者：林靖华，开源数据库技术爱好者，擅长MySQL和Redis的运维
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文约 650 字，预计阅读需要 2 分钟。
# 背景
某天，正按照业务的要求删除不需要的数据，在执行 DELETE 语句时，竟然出现了报错（MySQL 数据库版本 5.7.34）：
`mysql> delete from test1 t1 where not exists (select 1 from test2 t2 where t1.id=t2.id);
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 't1 where not exists (select 1 from test2 t2 where t1.id=t2.id)' at line 1
`
这就有点奇怪了，因为我在执行删除语句之前，执行过同样条件的 SELECT 语句，只是把其中的 `select *` 换成了 `delete` 而已，毕竟这个语法的报错一般来说原因很大可能是 **关键字拼写错误** 或者 **存在中文符号**。
排除了上面的原因后，再从语句本身的逻辑来排查，难道说 DELETE 语句不支持 `not exists` 这种写法？好像之前也没听说过这个限制。我们还是以语法错误这个原因为起点，去查查官方文档看下能不能找出答案。
# 分析
DELETE 的语法如下：
### 5.7 单表删除格式
`DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name
[PARTITION (partition_name [, partition_name] ...)]
[WHERE where_condition]
[ORDER BY ...]
[LIMIT row_count]
`
仔细对比了以下，发现了一些端倪，这里的语法并没有写出表名的别名用法，难道是使用了别名的原因？
`mysql> delete from test1 where not exists (select 1 from test2 where test1.id=test2.id);
Query OK, 1 row affected (0.00 sec)
`
经测试去掉了别名还真的执行成功了，但我印象中之前删除数据的时候用过别名，于是我再继续深挖文档查查看。
对比不同地方和不同版本的格式差异后，我终于明白了问题的起因。在不同版本，甚至不同情况下都有差异。
### 8.0 单表删除格式
`DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name [[AS] tbl_alias]
[PARTITION (partition_name [, partition_name] ...)]
[WHERE where_condition]
[ORDER BY ...]
[LIMIT row_count]
`
### 5.7 和 8.0 多表删除格式
```
DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
tbl_name[.*] [, tbl_name[.*]] ...
FROM table_references
[WHERE where_condition]
DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
FROM tbl_name[.*] [, tbl_name[.*]] ...
USING table_references
[WHERE where_condition]
```
经过上面语法对比的不同发现，5.7 的单表删除确实不支持别名的使用，但是多表删除却支持（`table_references` 里包含别名的使用）。
并且在 8.0.16 开始，单表删除已经支持使用别名了。
> 
For consistency with the SQL standard and other RDBMS, table aliases are now supported in single-table as well as multi-table DELETE statements. (Bug #27455809)
# 结论
- MySQL 5.7 使用单表删除语句时，不能使用别名，多表删除可以使用别名。
- MySQL 8.0.16 开始单表多表都可以使用别名。