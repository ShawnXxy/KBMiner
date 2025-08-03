# 技术分享 | MySQL 在 NoSQL 领域冲锋陷阵

**原文链接**: https://opensource.actionsky.com/20190109-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-01-09T18:29:21-08:00

---

**背景**> 文章内容又是来源于客户的一个问题。
**本文建议在PC端阅读**
**问题描述：**我们现在后台数据库全部为 MySQL，前端开发也非常熟悉 MySQL。但是现在有新的的业务进来。数据模型非常灵活，没有固定的表结构。起初我们考虑过 MySQL 的 memcached API。但是说实话非常鸡肋，没法全面的放开使用。这部分我们有考虑过 NoSQL 数据库，但是如果要部署 NoSQL 数据库，我们又得经过一系列的测试验证。请问 MySQL 关于这一块有没有好的解决方案？
**我的答案：**
**可以，完全可以！** MySQL X API 完全可以取代 NoSQL 数据库。而且这个功能从 MySQL 5.7 就有了。MySQL 5.7 也发布几年了，完全可以直接拿来用。
**MySQL X**
要使用 MySQL X 协议，必须在 MySQL 启动的时候，在配置文件中加入参数 mysqlx_port。- `#my.cnf`
- `[mysqld]`
- `port=3305 --原始传统的 mysql 端口`
- `mysqlx_port=33050　--mysql x 协议端口`
拿最火的 NoSQL 数据库 mongoDB 和 MySQL 来做对比。先举个插入表的简单例子：在 mongoDB 的表 f1 (字段 x y z) 中插入 10 条记录，- `# mongodb shell`
- `> use ytt`
- `> switched to db ytt`
- 
- `# 定义一个 js 数组，`
- `> var c1 = []`
- `> for (var i = 0;i < 10;i++){`
- `> ... c1.push({'x':i,'y':i*2,'z':i+100})`
- `> ... }`
- `> 10`
- 
- `# 插入刚才的数组`
- `> db.f1.insert(c1);`
- `> BulkWriteResult({`
- `> "writeErrors" : [ ],`
- `> "writeConcernErrors" : [ ],`
- `> "nInserted" : 10,`
- `> "nUpserted" : 0,`
- `> "nMatched" : 0,`
- `> "nModified" : 0,`
- `> "nRemoved" : 0,`
- `> "upserted" : [ ]`
- `> })`
- 
- `# 现在记录数为 10`
- `> db.f1.count()`
- `> 10`
- 
- `# 拿出第一条`
- `> db.f1.find().limit(1).pretty();`
- `{`
- `    "_id" : ObjectId("5e0066a54af3d32384342edd"),`
- `    "x" : 0,`
- `    "y" : 0,`
- `    "z" : 100`
- `}`
刚才 mongoDB 的例子，在 MySQL 里的实现也非常非常的简单。- `# mysql-shell`
- `# 创建一张表 f1`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.createCollection('f1')`
- `<Collection:f1>`
- 
- `# 依然定义同样的数组c1`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > var c1 = []`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > for (var i = 0;i<10;i++) { c1.push({'x':i,'y':i*2,'z':i+100})}`
- `10`
- 
- `# 插入刚才的记录`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.add(c1)`
- `Query OK, 10 items affected (0.0058 sec)`
- `Records: 10  Duplicates: 0  Warnings: 0`
- 
- `# 查看总行数`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.count();`
- `10`
- 
- `# 拿出一条记录`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find().limit(1);`
- `{`
- `    "x": 0,`
- `    "y": 0,`
- `    "z": 100,`
- `    "_id": "00005e006018000000000000000b"`
- `}`
- `1 document in set (0.0003 sec)`
那上面是一个基础的插入，再来看下其他操作，比如更新、删除。- `# mysql-shell`
- `# 把字段 x 值为 1 的记录更新为 MySQL`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.modify('x=1').set('x','mysql')`
- `Query OK, 1 item affected (0.0047 sec)`
- `Rows matched: 1  Changed: 1  Warnings: 0`
- 
- `# 检索 x='mysql' 的记录`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find("x='mysql'")`
- `{`
- `    "x": "mysql",`
- `    "y": 2,`
- `    "z": 101,`
- `    "_id": "00005e006018000000000000000c"`
- `}`
- `1 document in set (0.0006 sec)`
- 
- `# 更新字段 y 值为 'dble' 没有 where 过滤条件，也就是更新全表`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.modify("true").set('x','dble')`
- `Query OK, 10 items affected (0.0075 sec)`
- `Rows matched: 10  Changed: 10  Warnings: 0`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find();`
- `{`
- `    "x": "dble",`
- `    "y": 0,`
- `    "z": 100,`
- `    "_id": "00005e006018000000000000000b"`
- `}`
- `...`
- `{`
- `    "x": "dble",`
- `    "y": 18,`
- `    "z": 109,`
- `    "_id": "00005e0060180000000000000014"`
- `}`
- `10 documents in set (0.0010 sec)`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS >`
- 
- `# 比如现在要把刚才的 c1 数组嵌入到字段 x 中，该怎么做呢？`
- 
- `# 把 x 置为空数组`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.modify("true").set("x",[])`
- `Query OK, 10 items affected (0.0048 sec)`
- `Rows matched: 10  Changed: 10  Warnings: 0`
- 
- `# 用 array push 的方法更新字段 x`
- 
- ` MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.modify("true").arrayAppend("$.x",c1);`
- `Query OK, 10 items affected (0.0064 sec)`
- 
- `Rows matched: 10  Changed: 10  Warnings: 0`
- 
- `# 查看刚才更新的结果（简化显示）`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find()`
- `{`
- `    "x": [`
- `        [`
- `            {"x": 0, "y": 0, "z": 100},`
- `            { "x": 1,"y": 2,"z": 101},`
- `            {"x": 2,"y": 4,"z": 102},`
- `            {"x": 3,"y": 6,"z": 103},`
- `            {"x": 4,"y": 8,"z": 104},`
- `            {"x": 5,"y": 10,"z": 105},`
- `            {"x": 6,"y": 12,"z": 106},`
- `            {"x": 7,"y": 14,"z": 107},`
- `            {"x": 8, "y": 16,"z": 108},`
- `            {"x": 9,"y": 18,"z": 109}`
- `        ]`
- `    ],`
- `    "y": 0,`
- `    "z": 100,`
- `    "_id": "00005e006018000000000000000b"`
- `},`
- `...`
- `10 document in set (0.0003 sec)`
- 
- `# 那看下删除操作`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.remove('true');`
- `Query OK, 10 items affected (0.0032 sec)`
- 
- `# 数据已全部清空`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find()`
- `Empty set (0.0003 sec)`
- 
- `那最重要的是查询。查询通过 find() 方法过滤。看下面的例子。`
- 
- `#mysql-shell`
- `# 重新插入 10W 条记录`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.remove('true');`
- `Query OK, 10 items affected (0.0043 sec)`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > var c1 = []`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > for (var i =0;i< 100000;i++){c1.push({'x':i,'y':2*i,'z':i+100})}`
- `100000`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.add(c1)`
- `Query OK, 100000 items affected (2.5686 sec)`
- `Records: 100000  Duplicates: 0  Warnings: 0`
- 
- `# 拿出过滤条件为 x>100 and x < 200 的记录，倒序输出前两条记录`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find('x >100 and x < 200').sort(' x desc').limit(2)`
- `{`
- `    "x": 199,`
- `    "y": 398,`
- `    "z": 299,`
- `    "_id": "00005e00601800000000000000e6"`
- `}`
- `{`
- `    "x": 198,`
- `    "y": 396,`
- `    "z": 298,`
- `    "_id": "00005e00601800000000000000e5"`
- `}`
- `2 documents in set (0.0766 sec)`
- 
- `# 查询时间 0.0766 秒`
- 
- `# 给字段 x 加一个索引，也非常方便`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.createIndex('idx_x',{fields:[{'field':'$.x','type':'int'}]});`
- `Query OK, 0 rows affected (0.2854 sec)`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find('x >100 and x < 200').sort(' x desc').limit(2)`
- `{`
- `    "x": 199,`
- `    "y": 398,`
- `    "z": 299,`
- `    "_id": "00005e00601800000000000000e6"`
- `}`
- `{`
- `    "x": 198,`
- `    "y": 396,`
- `    "z": 298,`
- `    "_id": "00005e00601800000000000000e5"`
- `}`
- `2 documents in set (0.0004 sec)`
- `# 查询时间0.0004秒`
- 
- 
- `# 执行事物块更简单，转而使用 session 对象`
- `# 类似 start transaction 语句`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > session.startTransaction()`
- `Query OK, 0 rows affected (0.0002 sec)`
- 
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.remove('x=1')`
- `Query OK, 1 item affected (0.0004 sec)`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find('x=1')`
- `Empty set (0.0004 sec)`
- 
- `# 类似 rollback 语句`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > session.rollback()`
- `Query OK, 0 rows affected (0.0014 sec)`
- 
- `# 这条记录还在`
- `MySQL  ytt-pc:33050+ ssl  ytt  JS > db.f1.find('x=1')`
- `{`
- `    "x": 1,`
- `    "y": 2,`
- `    "z": 101,`
- `    "_id": "00005e0060180000000000000020"`
- `}`
- `1 document in set (0.0004 sec)`
**总结**以上我举了几个经典的例子来说明 MySQL 可以直接做为 NoSQL 数据库来使用，具备了本该有的功能。比如增删改查、建索引、事务等等。甚至可以说完全替代 mongoDB。
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
技术交流群，进群后可提问
QQ群（669663113）
社区通道，邮件&电话
osc@actionsky.com
现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
格式：.md/.doc/.txt
主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
要求：原创且未发布过
奖励：作者署名；200元京东E卡+社区周边
投稿方式：
邮箱：osc@actionsky.com
格式：[投稿]姓名+文章标题
以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系