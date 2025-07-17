# 技术分享 | 从 MySQL 到 OBOracle：如何处理自增列？

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e5%88%86%e4%ba%ab-%e4%bb%8e-mysql-%e5%88%b0-oboracle%ef%bc%9a%e5%a6%82%e4%bd%95%e5%a4%84%e7%90%86%e8%87%aa%e5%a2%9e%e5%88%97%ef%bc%9f/
**分类**: MySQL 新特性
**发布时间**: 2023-06-05T01:17:54-08:00

---

本文给出了四种 OBOracle 创建并使用序列的方法。
> 作者：杨敬博
爱可生 DBA 团队成员，一位会摄影、会铲屎、会打球、会骑车、生活可以自理的 DBA。
# 背景描述
OceanBase 数据库中分为 MySQL 租户与 Oracle 租户，本文针对 OceanBase 中 Oracle 租户怎样创建自增列，以及如何更简单方便的处理自增列的问题展开介绍。OceanBase 的 Oracle 租户以下简称：**OBOracle**。
#### 发现问题场景
业务需要将数据库转换为 OceanBase 数据库，但源端涉及到 Oracle 及 MySQL 两种不同数据库，需要合并为 OceanBase 中单一的 Oracle 模式，其中源端 MySQL 数据库需要改造为 OB Oracle 并做异构数据迁移。
在数据迁移中发现，MySQL 中的自增列（`AUTO_INCREMENT`）在 OB Oracle 中是不支持的，在 OB Oracle 对应 MySQL 自增列的功能是通过序列实现的。通过测试以及阅读相关文章，共测试完成了以下四种 OB Oracle 创建并使用序列的方法。
# 四种 OBOracle 创建序列方法
## 方法一：SEQUENCE + DML
在 OceanBase 中 Oracle 数据库，我们可以通过以下语法创建序列：
CREATE SEQUENCE sequence_name
[
MINVALUE value -- 序列最小值
MAXVALUE value -- 序列最大值
START WITH value -- 序列起始值
INCREMENT BY value -- 序列增长值
CACHE cache -- 序列缓存个数
CYCLE | NOCYCLE -- 序列循环或不循环
]
语法解释：
- `sequence_name` 是要创建的序列名称
- `START WITH` 指定使用该序列时要返回的第一个值，默认为 1
- `INCREMENT BY` 指定序列每次递增的值，默认为 1
- `MINVALUE` 和 `MAXVALUE` 定义序列值的最小值和最大值
- 如果序列已经递增到最大值或最小值，则会根据你的设置进行循环或停止自增长。`CACHE`设置序列预读缓存数量。
- `CYCLE` 表示循环序列
- `NOCYCLE` 则表示不循环序列
通过 OB 官方文档操作，创建序列，实现表的列自增，示例如下：
obclient [oboracle]> CREATE TABLE test (
-> ID NUMBER NOT NULL PRIMARY KEY,
-> NAME VARCHAR2(480),
-> AGE NUMBER(10,0)
-> );
Query OK, 0 rows affected (0.116 sec)
obclient [oboracle]> CREATE SEQUENCE seq_test START WITH 100 INCREMENT BY 1;
Query OK, 0 rows affected (0.026 sec)
obclient [oboracle]> INSERT INTO test(ID,NAME,AGE) VALUES(seq_test.nextval, 'A',18);
Query OK, 1 row affected (0.035 sec)
obclient [oboracle]> INSERT INTO test(ID,NAME,AGE) VALUES(seq_test.nextval, 'B',19);
Query OK, 1 row affected (0.001 sec)
obclient [oboracle]> INSERT INTO test(ID,NAME,AGE) VALUES(seq_test.nextval, 'C',20);
Query OK, 1 row affected (0.001 sec)
obclient [oboracle]> select * from test;
+-----+------+------+
| ID  | NAME | AGE  |
+-----+------+------+
| 100 | A    |   18 |
| 101 | B    |   19 |
| 102 | C    |   20 |
+-----+------+------+
3 rows in set (0.006 sec)
## 方法二：SEQUENCE + DDL
1、首先创建一个需要自增列的表
obclient [oboracle]> CREATE TABLE Atable (
->         ID NUMBER(10,0),
->            NAME VARCHAR2(480),
->         AGE NUMBER(10,0),
->         PRIMARY KEY (id)
-> );
Query OK, 0 rows affected (0.105 sec)
obclient [oboracle]> desc Atable;
+-------+---------------+------+-----+---------+-------+
| FIELD | TYPE          | NULL | KEY | DEFAULT | EXTRA |
+-------+---------------+------+-----+---------+-------+
| ID    | NUMBER(10)    | NO   | PRI | NULL     | NULL  |
| NAME  | VARCHAR2(480) | YES  | NULL | NULL    | NULL  |
| AGE   | NUMBER(10)    | YES  | NULL | NULL    | NULL  |
+-------+---------------+------+-----+---------+-------+
3 rows in set (0.037 sec)
2、创建一个序列并更改表中 `ID` 列的 DEFAULT 属性为 `sequence_name.nextval`。
obclient [oboracle]> CREATE SEQUENCE A_seq
-> MINVALUE 1
-> MAXVALUE 999999
-> START WITH 10
-> INCREMENT BY 1;
Query OK, 0 rows affected (0.022 sec)
obclient [oboracle]> ALTER TABLE Atable MODIFY id DEFAULT A_seq.nextval;
Query OK, 0 rows affected (0.065 sec)
obclient [oboracle]> desc Atable;
+-------+---------------+------+-----+-------------------+-------+
| FIELD | TYPE          | NULL | KEY | DEFAULT           | EXTRA |
+-------+---------------+------+-----+-------------------+-------+
| ID    | NUMBER(10)    | NO   | PRI | "A_SEQ"."NEXTVAL" | NULL  |
| NAME   | VARCHAR2(480) | YES  | NULL | NULL              | NULL  |
| AGE   | NUMBER(10)    | YES  | NULL | NULL              | NULL  |
+-------+---------------+------+-----+-------------------+-------+
3 rows in set (0.013 sec)
此处为修改表 `tablename` 中的 `ID` 值为序列 `sequence_name` 的下一个值。具体而言，`sequence_name.nextval` 表示调用 `sequence_name` 序列的 `nextval` 函数，该函数返回序列的下一个值。因此，执行述语句后，当 `tablename` 表中插入一行数据时，会自动为 `ID` 列赋值为 `sequence_name` 序列的下一个值。
3、验证该方法是否达到自增列的效果
obclient [oboracle]> INSERT INTO Atable(NAME,AGE) VALUES('zhangsan', 18);
Query OK, 1 row affected (0.047 sec)
obclient [oboracle]> INSERT INTO Atable(NAME,AGE) VALUES('lisi', 19);
Query OK, 1 row affected (0.002 sec)
obclient [oboracle]> select * from Atable;
+----+----------+------+
| ID | AME      | AGE  |
+----+----------+------+
| 10 | zhangsan |   18 |
| 11 | lisi     |   19 |
+----+----------+------+
2 rows in set (0.013 sec)
## 方法三：SEQUENCE + 触发器
OB 延用 Oracle 中创建触发器的方法达到自增列的效果，具体步骤如下：
1、首先创建一个序列：
obclient [oboracle]> CREATE SEQUENCE B_seq
-> MINVALUE 1
-> MAXVALUE 999999
-> START WITH 1
-> INCREMENT BY 1;
Query OK, 0 rows affected (0.023 sec)
2、创建一个表：
obclient [oboracle]> CREATE TABLE Btable (
->   ID NUMBER,
->   NAME VARCHAR2(480),
->   AGE NUMBER(10,0)
-> );
Query OK, 0 rows affected (0.129 sec)
3、创建一个触发器，在每次向表中插入行时，触发器将自动将新行的 `ID` 列设置为序列的下一个值。
obclient [oboracle]> CREATE OR REPLACE TRIGGER set_id_on_Btable
-> BEFORE INSERT ON Btable
-> FOR EACH ROW
-> BEGIN
->   SELECT B_seq.NEXTVAL INTO :new.id FROM dual;
-> END;
-> /
Query OK, 0 rows affected (0.114 sec)
该触发器在每次向 `Btable` 表中插入行之前触发，通过 `SELECT B_seq.NEXTVAL INTO :new.id FROM dual;` 将 `ID` 列设置为 `B_seq` 序列的下一个值。`:new.id` 表示新插入行的 `id` 列，`dual` 是一个虚拟的表，用于生成一行数据用以存储序列的下一个值。
4、验证该方法是否达到自增列的效果
obclient [oboracle]> INSERT INTO Btable(NAME,AGE) VALUES('zhangsan', 18);
Query OK, 1 row affected (0.111 sec)
obclient [oboracle]> INSERT INTO Btable(NAME,AGE) VALUES('lisi', 19);
Query OK, 1 row affected (0.002 sec)
obclient [oboracle]> select * from Btable;
+------+----------+------+
| ID   | NAME     | AGE  |
+------+----------+------+
|    1 | zhangsan |   18 |
|    2 | lisi     |   19 |
+------+----------+------+
2 rows in set (0.008 sec)
## 方法四：GENERATED BY DEFAULT AS IDENTITY 语法
1、在创建表时使用 `GENERATED BY DEFAULT AS IDENTITY` 语法来创建自增长的列
obclient [oboracle]> CREATE TABLE Ctable (
-> ID NUMBER GENERATED BY DEFAULT AS IDENTITY MINVALUE 1 MAXVALUE 999999 INCREMENT BY 1 START WITH 1 primary key,
-> NAME VARCHAR2(480),
-> AGE NUMBER(10,0)
-> );
Query OK, 0 rows affected (0.121 sec)
obclient [oboracle]> desc Ctable;
+-------+---------------+------+-----+------------------+-------+
| FIELD | TYPE          | NULL | KEY | DEFAULT          | EXTRA |
+-------+---------------+------+-----+------------------+-------+
| ID    | NUMBER        | NO   | PRI | SEQUENCE.NEXTVAL | NULL  |
| NAME  | VARCHAR2(480) | YES  | NULL | NULL             | NULL  |
| AGE   | NUMBER(10)    | YES  | NULL | NULL             | NULL  |
+-------+---------------+------+-----+------------------+-------+
3 rows in set (0.011 sec)
2、验证该方法是否达到自增列的效果
obclient [oboracle]> INSERT INTO Ctable(NAME,AGE) VALUES('zhangsan', 18);
Query OK, 1 row affected (0.015 sec)
obclient [oboracle]> INSERT INTO Ctable(NAME,AGE) VALUES('lisi', 19);
Query OK, 1 row affected (0.001 sec)
obclient [oboracle]> select * from Ctable;
+----+----------+------+
| ID | NAME     | AGE  |
+----+----------+------+
| 1  | zhangsan |   18 |
| 2  | lisi     |   19 |
+----+----------+------+
2 rows in set (0.008 sec)
3、通过验证，使用 `GENERATED BY DEFAULT AS IDENTITY` 可以非常简单地创建自增长列，无需使用其他手段，例如触发器。此方法不需要手动创建序列，会自动创建一个序列，在内部使用它来生成自增长列的值。
obclient [SYS]>  select * from dba_objects where OBJECT_TYPE='SEQUENCE';
+-------+-----------------+----------------+------------------+----------------+-------------+-----------+---------------+------------------------------+--------+-----------+-----------+-----------+-----------+--------------+
| OWNER | OBJECT_NAME     | SUBOBJECT_NAME | OBJECT_ID        | DATA_OBJECT_ID | OBJECT_TYPE | CREATED   | LAST_DDL_TIME | TIMESTAMP                    | STATUS | TEMPORARY | GENERATED | SECONDARY | NAMESPACE | EDITION_NAME |
+-------+-----------------+----------------+------------------+----------------+-------------+-----------+---------------+------------------------------+--------+-----------+-----------+-----------+-----------+--------------+
| MYSQL | A_SEQ           | NULL           | 1100611139403783 |           NULL | SEQUENCE    | 31-MAY-23 | 31-MAY-23     | 31-MAY-23 02.21.42.603005 PM | VALID  | N         | N         | N         |         0 | NULL         |
| MYSQL | B_SEQ           | NULL           | 1100611139403784 |           NULL | SEQUENCE    | 31-MAY-23 | 31-MAY-23     | 31-MAY-23 03.28.39.222090 PM | VALID  | N         | N         | N         |         0 | NULL         |
| MYSQL | ISEQ$$_50012_16 | NULL           | 1100611139403785 |           NULL | SEQUENCE    | 31-MAY-23 | 31-MAY-23     | 31-MAY-23 04.01.23.577766 PM | VALID  | N         | N         | N         |         0 | NULL         |
| MYSQL | SEQ_TEST        | NULL           | 1100611139403786 |           NULL | SEQUENCE    | 31-MAY-23 | 31-MAY-23     | 31-MAY-23 05.09.33.981039 PM | VALID  | N         | N         | N         |         0 | NULL         |
+-------+-----------------+----------------+------------------+----------------+-------------+-----------+---------------+------------------------------+--------+-----------+-----------+-----------+-----------+--------------+
6 rows in set (0.042 sec)
查看数据库对象视图 `dba_objects`，发现该方法通过创建对象内部命名方式为 `ISEQ$$_5000x_16`。
测试发现，关于序列对象的名称在OB中不论是通过 `GENERATED BY DEFAULT AS IDENTITY` 自动创建，还是手动创建，都会占用 `ISEQ$$_5000x_16` 中 `x` 的位置，若删除序列或删除表，该对象名称也不会复用，只会单调递增。
> Tips：
在 Oracle 12c 及以上版本中，可以使用 `GENERATED BY DEFAULT AS IDENTITY` 关键字来创建自增长的列；
在 PostgreSQL 数据库中 `GENERATED BY DEFAULT AS IDENTITY` 也是适用的。
# 总结
- 方法一（SEQUENCE + DML）：也就是 OB 的官方文档中创建序列的操作，在每次做 `INSERT` 操作时需要指定自增列并加入 `sequence_name` ，对业务不太友好，**不推荐**。 
- 方法二（SEQUENCE + DDL）：相较于第一种该方法只需要指定 DDL 改写 DEFAULT 属性省去了 DML 的操作，但仍需再指定自己创建的序列名 `sequence_name`，每个表的序列名都不一致，管理不方便，**不推荐**。
- 方法三（SEQUENCE + 触发器）延用 Oracle 的序列加触发器的方法，触发器会占用更多的计算资源和内存，对性能会有影响，因此也**不推荐**。
- 方法四（`GENERATED BY DEFAULT AS IDENTITY` 语法）：既方便运维人员管理，对业务也很友好，还不影响性能。**强烈推荐！！！**
以上就是对 OBOracle 中如何创建自增列的几种方法的总结。有需要的小伙伴可以试试(●&#8217;◡&#8217;●)。
本文关键字：#Oceanbase# #Oracle# #创建自增#