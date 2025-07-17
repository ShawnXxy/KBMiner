# 技术分享 | MySQL 在批量插入时捕捉错误信息

**原文链接**: https://opensource.actionsky.com/20190829-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-08-29T00:58:19-08:00

---

**背景**
本篇文章来源于今天客户问的一个问题。
问题大概意思是：我正在从 Oracle 迁移到 MySQL，数据已经转换为单纯的 INSERT 语句。由于语句很多，每次导入的时候不知道怎么定位到错误的语句。 如果 INSERT 语句少也就罢了，我可以手工看，不过 INSERT 语句很多，我怎么定位到是哪些语句出错了，我好改正呢？总不能每次遇到的错误的时候改一下，再重新运行继续改正吧？有没有简单点的方法。
其实 MySQL 自身就有错误诊断区域，如果能好好利用，则事半功倍。
**演示**
下面我来简单说下怎么使用**错误诊断区域**。
比如说我要插入的表结构为 n3，保存错误信息的日志表为 error_log 两个表结构如下：
- `-- tables definition.`
- `[ytt]>create table n3 (id int not null, id2 int generated always as ((mod(id,10))));`
- `Query OK, 0 rows affected (0.04 sec)`
- 
- `[ytt]>create table error_log (sqltext text, error_no int unsigned, error_message text);`
- `Query OK, 0 rows affected (0.04 sec)`
假设插入的语句，为了演示，我这里仅仅简单写了 8 条语句。- `-- statements body.`
- `set @a1 = "INSERT INTO n3 (id) VALUES(100)";`
- `set @a2 = "INSERT INTO n3 (id) VALUES('test')";`
- `set @a3 = "INSERT INTO n3 (id) VALUES('test123')";`
- `set @a4 = "INSERT INTO n3 (id) VALUES('123test')";`
- `set @a5 = "INSERT INTO n3 (id) VALUES(200)";`
- `set @a6 = "INSERT INTO n3 (id) VALUES(500)";`
- `set @a7 = "INSERT INTO n3 (id) VALUES(null)";`
- `set @a8 = "INSERT INTO n3 (id) VALUES(10000000000000)";`
MySQL 的错误代码很多，不过总体归为三类：
- **sqlwarning SQLSTATE 代码开始为 &#8217;01&#8217;**
- **not found SQLSTATE 代码开始为 &#8217;02&#8217;**
- **sqlexception SQLSTATE 代码开始非 &#8217;00&#8217;,&#8217;01&#8217;,&#8217;02&#8217; 的所有错误代码。**
为了简单方便，我们写这些代码到存储过程里。以下为示例存储过程。
- `-- stored routines body.`
- `drop procedure if exists sp_insert_simple;`
- `delimiter ||`
- `create procedure sp_insert_simple()`
- `l1:begin`
- `  DECLARE i,j TINYINT DEFAULT 1;   -- loop counter.`
- `  DECLARE v_errcount,v_errno INT DEFAULT 0; -- error count and error number.`
- `  DECLARE v_msg TEXT; -- error details.`
- `  declare v_sql json; -- store statements list.`
- `  declare v_sql_keys varchar(100); -- array index.`
- `  declare v_sql_length int unsigned; -- array length.`
- 
- `  -- Handler declare.`
- `  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION,SQLWARNING,NOT FOUND  -- exception in mysql routines.`
- `  l2:BEGIN`
- `    get stacked diagnostics v_errcount = number;`
- `    set j = 1;`
- `    WHILE j <= v_errcount`
- `    do`
- `      GET stacked DIAGNOSTICS CONDITION j  v_errno = MYSQL_ERRNO, v_msg = MESSAGE_TEXT;`
- `      -- record error messages into table.`
- `      INSERT INTO error_log(sqltext,error_no,error_message) VALUES (@sqltext, v_errno,v_msg);`
- `      SET j = j + 1;`
- `    END WHILE;`
- `  end;`
- `  -- sample statements array.`
- `  set v_sql = '{`
- `        "a1": "INSERT INTO n3 (id) VALUES(100)",`
- `        "a2": "INSERT INTO n3 (id) VALUES(''test'')",`
- `        "a3": "INSERT INTO n3 (id) VALUES(''test123'')",`
- `        "a4": "INSERT INTO n3 (id) VALUES(''123test'')",`
- `        "a5": "INSERT INTO n3 (id) VALUES(200)",`
- `        "a6": "INSERT INTO n3 (id) VALUES(500)",`
- `        "a7": "INSERT INTO n3 (id) VALUES(null)",`
- `        "a8": "INSERT INTO n3 (id) VALUES(10000000000000)"`
- `}';`
- `  set i = 1;`
- `  set v_sql_length = json_length(v_sql);`
- `  while i <=v_sql_length  do`
- `    set v_sql_keys = concat('$.a',i);`
- `    set @sqltext = replace(json_extract(v_sql,v_sql_keys),'"','');`
- `    prepare s1 from @sqltext;`
- `    execute s1;`
- `    set i = i + 1;`
- `  end while;`
- `  drop prepare s1;`
- `  -- invoke procedure.`
- `  -- call sp_insert_simple;`
- `end;`
- `||`
- `delimiter ;`
我们来调用这个存储过程看下结果。- `[(none)]>use ytt`
- `Reading table information for completion of table and column names`
- `You can turn off this feature to get a quicker startup with -A`
- `Database changed`
- 
- `[ytt]>call sp_insert_simple;`
- `Query OK, 0 rows affected (0.05 sec)`
表N3的结果。
- `[ytt]>select  * from n3;`
- `+-----+------+`
- `| id  | id2  |`
- `+-----+------+`
- `| 100 |    0 |`
- `| 200 |    0 |`
- `| 500 |    0 |`
- `+-----+------+`
- `3 rows in set (0.00 sec)`
错误日志记录了所有错误的语句。
- `[ytt]>select * from error_log;`
- `+--------------------------------------------+----------+-------------------------------------------------------------+`
- `| sqltext                                    | error_no | error_message                                               |`
- `+--------------------------------------------+----------+-------------------------------------------------------------+`
- `| INSERT INTO n3 (id) VALUES('test')         |     1366 | Incorrect integer value: 'test' for column 'id' at row 1    |`
- `| INSERT INTO n3 (id) VALUES('test123')      |     1366 | Incorrect integer value: 'test123' for column 'id' at row 1 |`
- `| INSERT INTO n3 (id) VALUES('123test')      |     1265 | Data truncated for column 'id' at row 1                     |`
- `| INSERT INTO n3 (id) VALUES(null)           |     1048 | Column 'id' cannot be null                                  |`
- `| INSERT INTO n3 (id) VALUES(10000000000000) |     1264 | Out of range value for column 'id' at row 1                 |`
- `+--------------------------------------------+----------+-------------------------------------------------------------+`
- `5 rows in set (0.00 sec)`
其实这个问题如果用 Python 或 PHP 等外部语言来说，将会更简单，思路差不多。
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
- 技术交流群，进群后可提问
QQ群（669663113）
- 社区通道，邮件&电话
osc@actionsky.com
- 现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
- 格式：.md/.doc/.txt
- 主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
- 要求：原创且未发布过
- 奖励：作者署名；200元京东E卡+社区周边
投稿方式：
- 邮箱：osc@actionsky.com
- 格式：[投稿]姓名+文章标题
- 以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系