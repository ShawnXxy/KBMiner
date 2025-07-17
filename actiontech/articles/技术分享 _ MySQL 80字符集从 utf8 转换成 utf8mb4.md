# 技术分享 | MySQL 8.0：字符集从 utf8 转换成 utf8mb4

**原文链接**: https://opensource.actionsky.com/20191118-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-11-17T22:20:47-08:00

---

**整理 MySQL 8.0 文档时发现一个变更：**
****默认字符集由 latin1 变为 utf8mb4。想起以前整理过字符集转换文档，升级到 MySQL 8.0 后大概率会有字符集转换的需求，在此正好分享一下。
**当时的需求背景是：**
****部分系统使用的字符集是 utf8，但 utf8 最多只能存 3 字节长度的字符，不能存放四字节的生僻字或者表情符号，因此打算迁移到 utf8mb4。
**迁移方案一****1. 准备新的数据库实例，修改以下参数：**- `[mysqld]`
- `## Character Settings`
- `init_connect='SET NAMES utf8mb4'`
- `#连接建立时执行设置的语句，对super权限用户无效`
- `character-set-server = utf8mb4`
- `collation-server = utf8mb4_general_ci`
- `#设置服务端校验规则，如果字符串需要区分大小写，设置为utf8mb4_bin`
- `skip-character-set-client-handshake`
- `#忽略应用连接自己设置的字符编码，保持与全局设置一致`
- `## Innodb Settings`
- `innodb_file_format = Barracuda`
- `innodb_file_format_max = Barracuda`
- `innodb_file_per_table = 1`
- `innodb_large_prefix = ON`
- `#允许索引的最大字节数为3072（不开启则最大为767字节，对于类似varchar(255)字段的索引会有问题，因为255*4大于767）`
**2. 停止应用，观察，确认不再有数据写入**
可通过 show master status 观察 GTID 或者 binlog position 没有变化则没有写入。
**3. 导出数据**
先导出表结构：- `mysqldump -u -p --no-data --default-character-set=utf8mb4 --single-transaction --set-gtid-purged=OFF --databases testdb > /backup/testdb.sql`
后导出数据：- `mysqldump -u -p --no-create-info --master-data=2 --flush-logs --routines --events --triggers --default-character-set=utf8mb4 --single-transaction --set-gtid-purged=OFF --database testdb > /backup/testdata.sql`
**4. 修改建表语句**
修改导出的表结构文件，将表、列定义中的 utf8 改为 utf8mb4
**5. 导入数据**
先导入表结构：- `mysql -u -p testdb < /backup/testdb.sql`
后导入数据：- `mysql -u -p testdb < /backup/testdata.sql`
**6. 建用户**
查出旧环境的数据库用户，在新数据库中创建
**7. 修改新数据库端口，启动应用进行测试**
关闭旧数据库，修改新数据库端口重启，启动应用
**迁移方案二****1. 修改表的字符编码会锁表，建议先停止应用**
**2. 停止 mysql，备份数据目录（也可以其他方式进行全备）**
**3. 修改配置文件，重启数据库**
- `[mysqld]`
- `## Character Settings`
- `init_connect='SET NAMES utf8mb4'`
- `#连接建立时执行设置的语句，对super权限用户无效`
- `character-set-server = utf8mb4`
- `collation-server = utf8mb4_general_ci`
- `#设置服务端校验规则，如果字符串需要区分大小写，设置为utf8mb4_bin`
- `skip-character-set-client-handshake`
- `#忽略应用连接自己设置的字符编码，保持与全局设置一致`
- `## Innodb Settings`
- `innodb_file_format = Barracuda`
- `innodb_file_format_max = Barracuda`
- `innodb_file_per_table = 1`
- `innodb_large_prefix = ON`
- `#允许索引的最大字节数为3072（不开启则最大为767字节，对于类似varchar(255) 字段的索引会有问题，因为255*4大于767）`
**4. 查看所有表结构，包括字段，修改库和表结构，如果字段有定义字符编码，也需要修改字段属性，sql 语句如下：**修改表的校对规则：- `alter table t convert to character set utf8mb4;`
影响：拷贝全表，速度慢，会加锁，阻塞写操作修改字段的校对规则（utfmb4 每字符占 4 字节，注意字段类型的最大字节数与字符长度关系）：
- `alter table t modify a char CHARACTER SET utf8mb4;`
影响：拷贝全表，速度慢，会加锁，阻塞写操作修改 database 的校对规则：
- `alter database sbtest CHARACTER SET utf8mb4;`
影响：只需修改元数据，速度很快
**5. 修改 JDBC url haracterEncoding=utf-8**
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