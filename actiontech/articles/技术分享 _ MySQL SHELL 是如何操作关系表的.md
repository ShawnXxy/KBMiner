# 技术分享 | MySQL SHELL 是如何操作关系表的？

**原文链接**: https://opensource.actionsky.com/20210414-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-04-13T21:51:24-08:00

---

作者：杨涛涛资深数据库专家，专研 MySQL 十余年。擅长 MySQL、PostgreSQL、MongoDB 等开源数据库相关的备份恢复、SQL 调优、监控运维、高可用架构设计等。目前任职于爱可生，为各大运营商及银行金融企业提供 MySQL 相关技术支持、MySQL 相关课程培训等工作。本文来源：原创投稿* 爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 前言
我之前有一篇介绍在 MySQL SHELL 环境中如何对文档类数据进行操作的文章[（](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247486620&idx=1&sn=f90240b8c6e64d760b8064db4bb9126f&chksm=fc96ee03cbe1671565728c9f07169fdc369fa9bd1c47538b524c93c6a15bb9b04d26331558b9&scene=21#wechat_redirect)[MySQL 在NOSQL 领域冲锋陷阵](https://opensource.actionsky.com/20190109-mysql/)[）](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247486620&idx=1&sn=f90240b8c6e64d760b8064db4bb9126f&chksm=fc96ee03cbe1671565728c9f07169fdc369fa9bd1c47538b524c93c6a15bb9b04d26331558b9&scene=21#wechat_redirect)，但是 MySQL SHELL 功能很多，除了可以操作文档类数据，也可以对关系表进行各种 DDL,DML 等操作。这里我就用几个简单例子来示范下如何用 MySQL SHELL 操作关系表。
此处引用的数据库示例基于官方的 SAMPLE DATABASE：WORLD，表结构以及数据可以自行下载。
## MySQL SHELL 对关系型数据库的操作涉及到三个组件：
- **MySQL：**传统 mysql，操作比较简单，除了写法有些差异外，基本上等同于 SQL 操作。
- **MySQL X：**基于 X DEV 协议操作 mysql，其中包含很多类，除了可以操作文档数据，也可以操作关系表。
- **SHELL：**包含了以上两个组件，可以随意切换，重点在于如何选择连接协议。
我们来依次看看各个组件对关系表的常用检索方式。
#### 一、mysql 组件
连接数据库：mysql.get_session 或者 mysql.get_classic_session
可以用如下传统拼串方式连接数据库：
`MySQL  Py > connection_url="mysql://root:root@localhost/world?socket=(/var/lib/mysql/official/mysql.sock)"MySQL  Py > ytt_cn1 = mysql.get_session(connection_url);
MySQL  Py > ytt_cn1
<ClassicSession:root@localhost>
`也可以用字典的方式连接数据库：
`MySQL  Py > connection_url={"schema":"world","user":"root","password":"root","socket":"/var/lib/mysql/official/mysql.sock"}
MySQL  Py > ytt_cn1=mysql.get_session(connection_url);
MySQL  Py > ytt_cn1
<ClassicSession:root@/var%2Flib%2Fmysql%2Fofficial%2Fmysql.sock>
`接下来可以用 ClassicSession 类提供的各种方法对关系表进行相关操作，所有的操作都可以直接用函数 run_sql 来执行：
对表 city 查询：
`MySQL  Py > ytt_cn1.run_sql("table city limit 1")
+----+-------+-------------+----------+------------+
| ID | Name  | CountryCode | District | Population |
+----+-------+-------------+----------+------------+
|  1 | Kabul | AFG         | Kabol    |    1780000 |
+----+-------+-------------+----------+------------+
1 row in set (0.0005 sec)
`对表 city 插入：
`MySQL  Py > ytt_cn1.run_sql("insert into city(name,countrycode,population,district) values ('test','CHN',1000000,'dd')")
Query OK, 1 row affected (0.0079 sec)
MySQL  Py > ytt_cn1.run_sql("select * from city where name ='test'")
+------+------+-------------+----------+------------+
| ID   | Name | CountryCode | District | Population |
+------+------+-------------+----------+------------+
| 4097 | test | CHN         | dd       |    1000000 |
+------+------+-------------+----------+------------+
1 row in set (0.0032 sec)
`对表 city 更新：
`MySQL  Py > ytt_cn1.run_sql("update city set name='who know ?' where id=4097")
Query OK, 1 row affected (0.0894 sec)
Rows matched: 1  Changed: 1  Warnings: 0
MySQL  Py > ytt_cn1.run_sql("select * from city where id=4097")
+------+------------+-------------+----------+------------+
| ID   | Name       | CountryCode | District | Population |
+------+------------+-------------+----------+------------+
| 4097 | who know ? | CHN         | dd       |    1000000 |
+------+------------+-------------+----------+------------+
1 row in set (0.0005 sec)
`对表 city 删除：
`MySQL  Py > ytt_cn1.run_sql("delete from city where id=4097")
Query OK, 1 row affected (0.0739 sec)
MySQL  Py > ytt_cn1.run_sql("select * from city where id=4097")
Empty set (0.0004 sec)
`开启一个事务块：
`MySQL  Py > ytt_cn1.start_transaction();
Query OK, 0 rows affected (0.0003 sec)
MySQL  Py > ytt_cn1.run_sql("delete from city where id =1")
Query OK, 1 row affected (0.0006 sec)
MySQL  Py > ytt_cn1.rollback();
Query OK, 0 rows affected (0.2070 sec)
MySQL  Py > ytt_cn1.run_sql("select * from city where id = 1")
+----+-------+-------------+----------+------------+
| ID | Name  | CountryCode | District | Population |
+----+-------+-------------+----------+------------+
|  1 | Kabul | AFG         | Kabol    |    1780000 |
+----+-------+-------------+----------+------------+
1 row in set (0.0004 sec)
`关闭连接：
`MySQL  Py > ytt_cn1.close();
MySQL  Py > ytt_cn1
<ClassicSession:disconnected>`
#### 二、mysqlx 组件
MySQL X 组件包含了很多类，下面我来举几个常用的例子：
依然是先连接数据库 world：X 协议端口 33060 或者 X SOCKET（用 mysqlx.get_session 方法）。
`MySQL  Py > connection_urlx="mysqlx://root:root@localhost/world?socket=(/var/lib/mysql/official/mysqlx.sock)"
MySQL  Py > ytt_cnx1=mysqlx.get_session(connection_urlx);
`比如找出人口小于800的城市并且列出对应的国家名字：
`SQL： select a.id,a.name,b.name country_name, a.population from city a join country b on (a.countrycode = b.code and a.population < 800);
`##### 2.1 SQLRESULT 类：类似于 mysql 游标用法
```
MySQL  Py > sql1="select a.id,a.name,b.name country_name, a.population from city a join country b on (a.countrycode = b.code and a.population < 800)"
MySQL  Py > sql_result1=ytt_cnx1.run_sql(sql1)
```
获取前两行：默认不带字段名
`MySQL  Py > sql_result1.fetch_one()
[
62,
"The Valley",
"Anguilla",
595
]
MySQL  Py > sql_result1.fetch_one()
[
1791,
"Flying Fish Cove",
"Christmas Island",
700
]
`获取带字段名的记录：
`MySQL  Py > sql_result1.fetch_one_object();
{
"country_name": "Cocos (Keeling) Islands", 
"id": 2316, 
"name": "Bantam", 
"population": 503
}
`一次性获取剩余的行：
`MySQL  Py > sql_result1.fetch_all()
[
[
2317,
"West Island",
"Cocos (Keeling) Islands",
167
], 
[
2728,
"Yaren",
"Nauru",
559
], 
[
2805,
"Alofi",
"Niue",
682
], 
[
2912,
"Adamstown",
"Pitcairn",
42
], 
[
3333,
"Fakaofo",
"Tokelau",
300
], 
[
3538,
"Città del Vaticano",
"Holy See (Vatican City State)",
455
]
]
`##### 2.2 SqlExecute 类：类似于 prepare 语句用法
比如把之前的人口判断条件替换为绑定变量（？或者变量(:a)），这样可以方便多个条件一起查询。
` MySQL  Py > sql2="select a.id,a.name,b.name country_name, a.population from city a join country b on (a.countrycode = b.code and a.population < ?)"
MySQL  Py > sql_result2=ytt_cnx1.sql(sql2);
`给定两个不同的人口条件：
`MySQL  Py > a=800
MySQL  Py > b=500
`绑定变量执行结果：
`MySQL  Py > sql_result2.bind(a)
+------+--------------------+-------------------------------+------------+
| id   | name               | country_name                  | population |
+------+--------------------+-------------------------------+------------+
|   62 | The Valley         | Anguilla                      |        595 |
| 1791 | Flying Fish Cove   | Christmas Island              |        700 |
| 2316 | Bantam             | Cocos (Keeling) Islands       |        503 |
| 2317 | West Island        | Cocos (Keeling) Islands       |        167 |
| 2728 | Yaren              | Nauru                         |        559 |
| 2805 | Alofi              | Niue                          |        682 |
| 2912 | Adamstown          | Pitcairn                      |         42 |
| 3333 | Fakaofo            | Tokelau                       |        300 |
| 3538 | Città del Vaticano | Holy See (Vatican City State) |        455 |
+------+--------------------+-------------------------------+------------+
9 rows in set (0.0022 sec)
MySQL  Py > sql_result2.bind(b)
+------+--------------------+-------------------------------+------------+
| id   | name               | country_name                  | population |
+------+--------------------+-------------------------------+------------+
| 2317 | West Island        | Cocos (Keeling) Islands       |        167 |
| 2912 | Adamstown          | Pitcairn                      |         42 |
| 3333 | Fakaofo            | Tokelau                       |        300 |
| 3538 | Città del Vaticano | Holy See (Vatican City State) |        455 |
+------+--------------------+-------------------------------+------------+
4 rows in set (0.0023 sec)
`##### 2.3 Table 类：获取当前连接数据库下单张表，可以对这张表进行任何 DML 操作。（获取 Table 类之前，得先获取 Schema 类）
```
MySQL  Py > ytt_schema1=ytt_cnx1.get_schema('world')
MySQL  Py > ytt_tbname1=ytt_schema1.get_table('city');
```
查找人口少于 800 的记录：
`MySQL  Py > ytt_tbname1.select().where("population<800")
+------+--------------------+-------------+-------------+------------+
| ID   | Name               | CountryCode | District    | Population |
+------+--------------------+-------------+-------------+------------+
|   62 | The Valley         | AIA         | –           |        595 |
| 1791 | Flying Fish Cove   | CXR         | –           |        700 |
| 2316 | Bantam             | CCK         | Home Island |        503 |
| 2317 | West Island        | CCK         | West Island |        167 |
| 2728 | Yaren              | NRU         | –           |        559 |
| 2805 | Alofi              | NIU         | –           |        682 |
| 2912 | Adamstown          | PCN         | –           |         42 |
| 3333 | Fakaofo            | TKL         | Fakaofo     |        300 |
| 3538 | Città del Vaticano | VAT         | –           |        455 |
+------+--------------------+-------------+-------------+------------+
9 rows in set (0.0024 sec)
`还可以继续排序以及限制记录数输出：
`MySQL  Py > ytt_tbname1.select().where("population<800").order_by("population desc ").limit(3)
+------+------------------+-------------+----------+------------+
| ID   | Name             | CountryCode | District | Population |
+------+------------------+-------------+----------+------------+
| 1791 | Flying Fish Cove | CXR         | –        |        700 |
| 2805 | Alofi            | NIU         | –        |        682 |
|   62 | The Valley       | AIA         | –        |        595 |
+------+------------------+-------------+----------+------------+
3 rows in set (0.0024 sec)
`##### 2.4 Table 类包含几个子类：TableSelect、TableInsert、TableUpdate、TableDelete。
**1）TableSelect：保存查询结果**
之前查找人口小于 800 的记录结果即为 TableSelect，可以基于此类来后续操作。
`MySQL  Py > tbselect1=ytt_tbname1.select().where("population<800")
`只拿出部分字段：
`MySQL  Py > tbselect1.select("[id,name]").order_by("population desc").limit(2);
+----------------------------+
| JSON_ARRAY(`id`,`name`)    |
+----------------------------+
| [1791, "Flying Fish Cove"] |
| [2805, "Alofi"]            |
+----------------------------+
2 rows in set (0.0031 sec)
`**2）TableInsert：执行插入语句**
插入一行：
`MySQL  Py > ytt_tbname1.count()
4081
MySQL  Py > tbinsert1=ytt_tbname1.insert(["name","population","countrycode","district"]).values('test',1000000,'CHN','dd');
MySQL  Py > tbinsert1.execute();
Query OK, 1 item affected (0.0054 sec)
MySQL  Py > ytt_tbname1.count()
4082
`插入多行：有两种方法。
多 VALUES 形式：
`MySQL  Py > tbinsert1=ytt_tbname1.insert(["name","population","countrycode","district"]).values('test',1000000,'CHN','dd').values('test',1000000,'CHN','dd');
MySQL  Py > tbinsert1.execute()
Query OK, 2 items affected (0.0325 sec)
Records: 2  Duplicates: 0  Warnings: 0
MySQL  Py > 
MySQL  Py > ytt_tbname1.count()
4084
`多次执行或者包含在事务块里：
`MySQL  Py > ytt_cnx1.start_transaction();
Query OK, 0 rows affected (0.0004 sec)
MySQL  Py > tbinsert1=ytt_tbname1.insert(["name","population","countrycode","district"]).values('test',1000000,'CHN','dd');
MySQL  Py > tbinsert1
Query OK, 1 item affected (0.0008 sec)
MySQL  Py > tbinsert1
Query OK, 1 item affected (0.0006 sec)
MySQL  Py > tbinsert1
Query OK, 1 item affected (0.0008 sec)
MySQL  Py > tbinsert1
Query OK, 1 item affected (0.0006 sec)
MySQL  Py > ytt_cnx1.commit();
Query OK, 0 rows affected (0.2737 sec)
MySQL  Py > ytt_tbname1.count()
4088
`**3）TableUpdate：执行更新语句**
`MySQL  Py > tbupdate1=ytt_tbname1.update().set('district','nothing').where("name='test'")
MySQL  Py > tbupdate1
Query OK, 0 items affected (0.0048 sec)
Rows matched: 9  Changed: 9  Warnings: 0
`**4）TableDelete：执行删除语句**
`MySQL  Py > tbdelete1=ytt_tbname1.delete().where("district='nothing'");
MySQL  Py > tbdelete1
Query OK, 9 items affected (0.0112 sec)
MySQL  Py > ytt_tbname1.count()
4079`
#### 三、SHELL 组件
SHELL 组件可以在 MySQL 和 MySQL X 间随意切换，并且连接后，包含了一个默认数据库类 “db” ，db 等价于 ytt_cnx1.get_current_schema()
`MySQL  Py > ytt_cnx_shell1=shell.connect(connection_urlx)
Creating an X protocol session to 'root@localhost/world'
Fetching schema names for autocompletion... Press ^C to stop.
Your MySQL connection id is 10 (X protocol)
Server version: 8.0.23 MySQL Community Server - GPL
Default schema `world` accessible through db
`依然还是操作表 city，
` MySQL  localhost+ ssl  world  Py > ytt_tbname2=db.get_table("city")
MySQL  localhost+ ssl  world  Py > ytt_tbname2
<Table:city>
`之后的操作和之前 mysqlx 的一样。
`MySQL  localhost+ ssl  world  Py > ytt_tbname2.select(['id','name']).where("population<800").order_by("id desc").limit(3);
+------+--------------------+
| id   | name               |
+------+--------------------+
| 3538 | Città del Vaticano |
| 3333 | Fakaofo            |
| 2912 | Adamstown          |
+------+--------------------+
3 rows in set (0.0011 sec)
`所以如果用 MySQL SHELL 来操作 mysql 关系表，推荐用 SHELL 组件的方式，非常灵活。
**文章推荐：**
[技术分享 | MySQL 在 NoSQL 领域冲锋陷阵](https://opensource.actionsky.com/20190109-mysql/)[](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247491537&idx=1&sn=9de3fe010dee07d735c73be344418632&chksm=fc96fd4ecbe17458ad5765cd4364381a133890be80e7e77adb938bf5d7bb568cf5fce8329ced&scene=21#wechat_redirect)
[新特性解读 | 高效获取不连续主键区间](https://opensource.actionsky.com/20210112-mysql/)
[新特性解读 | MySQL 8.0.22 任意格式数据导入](https://opensource.actionsky.com/20201110-mysql/)