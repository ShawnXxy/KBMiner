# 新特性解读 | 来聊聊 MySQL8.0 的 json 模式校验

**原文链接**: https://opensource.actionsky.com/20211013-json/
**分类**: 技术干货
**发布时间**: 2021-10-12T21:44:19-08:00

---

作者：杨涛涛
资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 引言
MySQL 从 8.0.17 开始，支持对 json 模式定义做严格匹配校验。首先要了解什么是 json 模式？ json 模式类似于关系表结构，诸如字段数据类型、默认值、字符集等等的约束规则。更加深入了解请参考：https://json-schema.org/understanding-json-schema/
## 正文
比如下面一个 json 模式定义：此模式所包含内容是一个数组，数据元素分别是整型和字符串，整型必须大于等于5；字符串长度必须大于等于5；元素个数限定在2和5之间；并且每个元素要唯一，不能重复。
`'{
"$schema": "http://json-schema.org/draft-04/schema#",
"title":"ytt array",
"description": "ytt array",
"type": "array",
"items": [
{
"type": "number",
"minimum": 5
},
{
"type": "string",
"minLength": 5
}
],
"minItems": 2,
"maxItems": 5,
"uniqueItems": true
}'
`
##### MySQL 8.0 内置的 json 模式校验函数可以在 json 串入库前根据预定义模式来提前严格校验，减少后期工作量。
##### 目前有两个相关函数：
- 
###### json_schema_valid
来校验指定 json 串是否符合预定义模式，符合则返回1，不符合返回0.
- 
###### json_schema_validation_report
来校验指定 json 串是否符合预定义模式，并且给出详细报告，并不只是简单的返回1和0.
校验成功则结果为：{&#8220;valid&#8221;: true}
校验失败则结果为一个json对象：
{&#8220;valid&#8221;:false，
&#8220;reason&#8221;: 失败详细原因表述,
&#8220;schema-location&#8221;: 失败的模式具体path，
“document-location”: 失败的检测json对象或者数组具体path，
“schema-failed-keyword”：失败对应的模式种的key
}
##### 接下来看看这两个函数的具体用法：分别定义一个数组和一个对象。
###### 先是数组：我把开头那个模式定义稍微改了下，加了一个枚举元素，其他没变，为了好看，用 json_pretty 函数打出来。
`mysql:ytt>select json_pretty(@schema)\G
*************************** 1. row ***************************
json_pretty(@schema): {
"type": "array",
"items": [
{
"type": "number",
"minimum": 5
},
{
"type": "string",
"minLength": 5
},
{
"enum": [
"postgresql",
"oracle",
"uguard",
"tidb"
]
}
],
"title": "ytt array",
"$schema": "http://json-schema.org/draft-04/schema#",
"maxItems": 5,
"minItems": 3,
"description": "ytt array",
"uniqueItems": true
}
1 row in set (0.01 sec)
`
接下来分别看看以下 json 数组是否符合预定义模式：
`mysql:ytt>set @a='[]';
Query OK, 0 rows affected (0.00 sec)
mysql:ytt>set @b='["mysql",100,"tidb"]';
Query OK, 0 rows affected (0.00 sec)
mysql:ytt>set @c='[100,"mysql","uguard"]';
Query OK, 0 rows affected (0.00 sec)
mysql:ytt>set @d='[200,"database","postgresql","others"]';
Query OK, 0 rows affected (0.00 sec)
mysql:ytt>select json_schema_valid(@schema,@a) "@a",json_schema_valid(@schema,@b) "@b", json_schema_valid(@schema,@c) "@c", json_schema_valid(@schema,@d) "@d";
+------+------+------+------+
| @a   | @b   | @c   | @d   |
+------+------+------+------+
|    0 |    0 |    1 |    1 |
+------+------+------+------+
1 row in set (0.00 sec)
`
从结果中看@a和@b不符合模式定义，@c和@d都符合模式定义；来看下校验失败原因，用函数 json_schema_validation_report 来验证下：
`mysql:ytt>select json_pretty(json_schema_validation_report(@schema,@a)) "@a result"\G
*************************** 1. row ***************************
@a result: {
"valid": false,
"reason": "The json document location '#' failed requirement 'minItems' at json Schema location '#'",
"schema-location": "#",
"document-location": "#",
"schema-failed-keyword": "minItems"
}
1 row in set (0.00 sec)
`
由函数 json_schema_validation_report 报告结果可以得出，@a不满足最小元素数目这一项定义。那再来看看@b为什么不符合：
`mysql:ytt>select json_pretty(json_schema_validation_report(@schema,@b)) "@b result"\G
*************************** 1. row ***************************
@b result: {
"valid": false,
"reason": "The json document location '#/0' failed requirement 'type' at json Schema location '#/items/0'",
"schema-location": "#/items/0",
"document-location": "#/0",
"schema-failed-keyword": "type"
}
1 row in set (0.00 sec)
`
同样由函数 json_schema_validation_report 报告结果可以得出，@b不符合的原因是不满足模式定义里数组第一个元素的数据类型，指定类型为整型，@b的第一个元素是字符串。
@c和@d 完全符合模式定义，数组元素类型、元素最小个数、元素最大个数等都符合。
###### 再来看一个对象：依然用 json_pretty 函数打印出来，这个模式定义内容为对象，有几点需要说明：对象的key分别为x,y,z，key对应的 value 数据类型分别为整型，字符串，枚举；另外还规定最小key为2个，最大为3个，并且x、y这两个key必须同时出现。
`mysql:ytt>select json_pretty(@schema)\G
*************************** 1. row ***************************
json_pretty(@schema): {
"type": "object",
"title": "ytt object",
"$schema": "http://json-schema.org/draft-04/schema#",
"required": [
"x",
"y"
],
"properties": {
"x": {
"type": "number"
},
"y": {
"type": "string"
},
"z": {
"enum": [
"mysql",
"ugurad",
"postgresql"
]
}
},
"description": "ytt object",
"maxProperties": 3,
"minProperties": 2
}
1 row in set (0.00 sec)
`
接下来，定义两个 json 对象，来看下对于模式定义为对象的校验。
`mysql:ytt>set @a='{"x":"mysql","y":"oracle"}';
Query OK, 0 rows affected (0.00 sec)
mysql:ytt>set @b='{"x":10,"y":"uguard","z":"mysql"}' ;
Query OK, 0 rows affected (0.00 sec)
mysql:ytt>select json_schema_valid(@schema,@a) "@a", json_schema_valid(@schema,@b) "@b";
+------+------+
| @a   | @b   |
+------+------+
|    0 |    1 |
+------+------+
1 row in set (0.00 sec)
`
从函数 json_schema_valid 的校验结果可以得到@a不符合模式定义， @a第一个 key 对应的 value 为字符串，不符合模式定义中的 key 为x的数据类型。 用函数 json_schema_validation_report 来验证下我们的猜测：
`mysql:ytt>select json_pretty(json_schema_validation_report(@schema,@a)) "@a result"\G
*************************** 1. row ***************************
@a result: {
"valid": false,
"reason": "The json document location '#/x' failed requirement 'type' at json Schema location '#/properties/x'",
"schema-location": "#/properties/x",
"document-location": "#/x",
"schema-failed-keyword": "type"
}
1 row in set (0.00 sec)
`
函数 json_schema_validation_report 的结果刚好验证我们的猜测，key 为x对应的 value 数据类型不匹配。
json 模式定义的验证也可以用到约束表的 check 定义，我们就用第二个包含对象的模式定义来约束表的 json 字段，定义表t10:
`create table t10
(str1 json,
check(json_schema_valid(
'{
"$schema": "http://json-schema.org/draft-04/schema#",
"title":"ytt object",
"description": "ytt object",
"type": "object",
"properties": {
"x": { "type": "number" },
"y": { "type": "string" },
"z": { "enum": ["mysql", "ugurad", "postgresql"] }
},
"required": ["x", "y"],
"minProperties": 2,
"maxProperties": 3
}',str1)));
`
分别把 json 对象@a和@b写入表t10:  插入@a失败，show warnings 报告失败具体原因。
`mysql:ytt>insert t10 values (@a);
ERROR 3819 (HY000): Check constraint 't10_chk_1' is violated.
mysql:ytt>show errors\G
*************************** 1. row ***************************
Level: Error
Code: 3934
Message: The json document location '#/x' failed requirement 'type' at json Schema location '#/properties/x'.
*************************** 2. row ***************************
Level: Error
Code: 3819
Message: Check constraint 't10_chk_1' is violated.
2 rows in set (0.00 sec)
mysql:ytt>insert t10 values (@b);
Query OK, 1 row affected (0.50 sec)
`
## 结语
json_schema_valid 和 json_schema_validation_report 这两个函数可以在使用 json 数据类型前做一个预判，避免实际数据写入后再次整理不规范的数据，在使用 json 数据类型的场景中非常有用。