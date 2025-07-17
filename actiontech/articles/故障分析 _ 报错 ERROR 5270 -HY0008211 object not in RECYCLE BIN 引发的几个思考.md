# 故障分析 | 报错 ERROR 5270 -HY000&#8211; object not in RECYCLE BIN 引发的几个思考

**原文链接**: https://opensource.actionsky.com/20230418-recyclebin/
**分类**: 技术干货
**发布时间**: 2023-04-17T18:19:08-08:00

---

作者：姚嵩
不知道是地球人还是外星人，知道的可以留言告诉小编&#8230;
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 现象：
通过show recyclebin中的OBJECT_NAME / ORIGINAL_NAME闪回表时，
报错：对象不在回收站中。
报错复现：
MySQL [mysql]> create table test.a (i int) ;
Query OK, 0 rows affected (0.04 sec)
MySQL [mysql]> set session recyclebin = 1 ;
Query OK, 0 rows affected (0.00 sec)
MySQL [mysql]> drop table test.a ;
Query OK, 0 rows affected (0.01 sec)
MySQL [mysql]> show recyclebin ;
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680250599065600 | a             | TABLE | 2023-03-31 16:16:39.065038 |
+-----------------------------------------+---------------+-------+----------------------------+
1 row in set (0.01 sec)
MySQL [mysql]> flashback table a to before drop ;   
ERROR 5270 (HY000): object not in RECYCLE BIN
MySQL [oceanbase]> flashback table __recycle_$_1677212890_1680250599065600 to before drop ;
ERROR 5270 (HY000): object not in RECYCLE BIN
#### 原因：
还原的时候，默认使⽤当前的database做为表的上级对象；
如果表不是当前database的对象，则需要使⽤ database.table 格式指定表；
#### 引发的⼏个思考：
1.如何获取回收站中表的database？
2.回收站中是否可以保存多个同名的表？闪回的时候是哪个？
3.关闭回收站后，是否能看到回收站中的对象？
4.回收站是全租户可⻅，还是只有当前租户可⻅？
5.关闭回收站后，是否能闪回表？
6.关闭回收站后，是否能闪回租户？
#### 测试：
1.如何获取回收站中表的database？
MySQL [oceanbase]> create table test.a(i int) ;      -- 在test库中创建表a
Query OK, 0 rows affected (0.05 sec)
MySQL [oceanbase]> set session recyclebin=1 ;        -- 开启回收站
Query OK, 0 rows affected (0.00 sec)
MySQL [oceanbase]> use oceanbase ;                   -- 切换到oceanbase库中
Database changed
MySQL [oceanbase]> drop table test.a ;               -- 删除test.a表
Query OK, 0 rows affected (0.01 sec)
MySQL [oceanbase]> show recyclebin ;                 -- 查看test.a表是否在回收站中(在)
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680257357905408 | a             | TABLE | 2023-03-31 18:09:17.904933 |
+-----------------------------------------+---------------+-------+----------------------------+
1 row in set (0.00 sec)
MySQL [oceanbase]> select rb.tenant_id, rb.database_id, db.database_name, rb.table_id,
->        rb.tablegroup_id, rb.original_name from __all_recyclebin rb
->  inner join __all_virtual_database db
->          on rb.database_id=db.database_id;    -- 查看回收站中表a对应的database_name
+-----------+---------------+---------------+---------------+---------------+---------------+
| tenant_id | database_id   | database_name | table_id      | tablegroup_id | original_name |
+-----------+---------------+---------------+---------------+---------------+---------------+
|         1 | 1099511628776 | test          | 1099511677793 |            -1 | a             |
+-----------+---------------+---------------+---------------+---------------+---------------+
1 row in set (0.00 sec)
MySQL [oceanbase]> purge recyclebin ;                -- 清理回收站
Query OK, 0 rows affected (0.02 sec)
2.回收站中是否可以保存多个同名的表？闪回的时候是哪个？
MySQL [oceanbase]> create table test.a(i int) ;      -- 在test库中创建表a
Query OK, 0 rows affected (0.05 sec)
MySQL [oceanbase]> set session recyclebin=1 ;        -- 开启回收站
Query OK, 0 rows affected (0.00 sec)
MySQL [oceanbase]> drop table test.a ;               -- 删除test.a表
Query OK, 0 rows affected (0.02 sec)
MySQL [oceanbase]> create table test.a(i int) ;insert into test.a values(1);   -- 再次在test库中创建表a，此次写⼊⼀条数据
Query OK, 0 rows affected (0.04 sec)
Query OK, 1 row affected (0.01 sec)
MySQL [oceanbase]> drop table test.a ;               -- 再次删除test.a表
Query OK, 0 rows affected (0.01 sec)
MySQL [oceanbase]> show recyclebin ;                 -- 查看2个test.a表是否都在回收站中(在)
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680258454351360 | a             | TABLE | 2023-03-31 18:27:34.351415 |
| __recycle_$_1677212890_1680258454423040 | a             | TABLE | 2023-03-31 18:27:34.422931 |
+-----------------------------------------+---------------+-------+----------------------------+
2 rows in set (0.01 sec)
MySQL [oceanbase]> flashback table test.a to before drop ;   -- 闪回test.a表
Query OK, 0 rows affected (0.02 sec)
MySQL [oceanbase]> show recyclebin ;                 -- 恢复的是最晚删除的对象，所以回收站中留存的是较早删除的对象
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680258454351360 | a             | TABLE | 2023-03-31 18:27:34.351415 |
+-----------------------------------------+---------------+-------+----------------------------+
1 row in set (0.00 sec)
MySQL [oceanbase]> select * from test.a ;            -- 确认闪回的表是否是最晚删除的表(是)
+------+
| i    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)
MySQL [oceanbase]> purge recyclebin ;                -- 清理回收站
Query OK, 0 rows affected (0.02 sec)
3.关闭回收站后，是否能看到回收站中的对象？
MySQL [oceanbase]> create table test.a(i int) ;      -- 在test库中创建表a
Query OK, 0 rows affected (0.05 sec)
MySQL [oceanbase]> set session recyclebin=1 ;        -- 开启回收站
Query OK, 0 rows affected (0.00 sec)
MySQL [oceanbase]> drop table test.a ;               -- 删除test.a表
Query OK, 0 rows affected (0.02 sec)
MySQL [oceanbase]> set session recyclebin=0 ;        -- 关闭回收站
Query OK, 0 rows affected (0.00 sec)
MySQL [oceanbase]> show recyclebin ;                 -- 确认是否能查看回收站中的对象(能)
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680259040929280 | a             | TABLE | 2023-03-31 18:37:20.928638 |
+-----------------------------------------+---------------+-------+----------------------------+
1 row in set (0.00 sec)
4.回收站是全租户可⻅，还是只有当前租户可⻅？
[root@ob-70 ~]# mysql -h10.186.63.134 -uroot@t1#oceanb_test_zhn  -P2883 -c -A -e "create table test.tb1(i int);set session
recyclebin=1;drop table test.tb1;show recyclebin;purge recyclebin ;"
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680259840925720 | tb1           | TABLE | 2023-03-31 18:50:40.924748 |
+-----------------------------------------+---------------+-------+----------------------------+
[root@ob-70 ~]# mysql -h10.186.63.134 -uroot@sys#'oceanb_test_zhn' -P2883 -c -p'aaAA__12' -A  -e "show recyclebin;"
+-----------------------------------------+---------------+-------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE  | CREATETIME                 |
+-----------------------------------------+---------------+-------+----------------------------+
| __recycle_$_1677212890_1680259040929280 | a             | TABLE | 2023-03-31 18:37:20.928638 |
+-----------------------------------------+---------------+-------+----------------------------+
5.关闭回收站后，是否能闪回表？
MySQL [oceanbase]>  -- 获取回收站中表所在database的名称
->         select rb.tenant_id, rb.database_id, db.database_name, rb.table_id,
->        rb.tablegroup_id, rb.original_name from __all_recyclebin rb
->  inner join __all_virtual_database db
->          on rb.database_id=db.database_id;
+-----------+---------------+---------------+---------------+---------------+---------------+
| tenant_id | database_id   | database_name | table_id      | tablegroup_id | original_name |
+-----------+---------------+---------------+---------------+---------------+---------------+
|         1 | 1099511628776 | test          | 1099511677792 |            -1 | a             |
+-----------+---------------+---------------+---------------+---------------+---------------+
1 row in set (0.01 sec)
MySQL [oceanbase]> set session recyclebin=0;
Query OK, 0 rows affected (0.01 sec)
MySQL [oceanbase]> flashback table test.a to before drop ;
Query OK, 0 rows affected (0.02 sec)
MySQL [oceanbase]> desc test.a ;
+-------+---------+------+-----+---------+-------+
| Field | Type    | Null | Key | Default | Extra |
+-------+---------+------+-----+---------+-------+
| i     | int(11) | YES  |     | NULL    |       |
+-------+---------+------+-----+---------+-------+
1 row in set (0.00 sec)
6.关闭回收站后，是否能闪回租户？
MySQL [oceanbase]> set session recyclebin=1;    -- 开启回收站
Query OK, 0 rows affected (0.00 sec)
MySQL [oceanbase]> drop tenant t1 ;             -- 删除租户t1
Query OK, 0 rows affected (0.01 sec)
MySQL [oceanbase]> show recyclebin ;            -- 查看租户t1是否在回收站中(在)
+-----------------------------------------+---------------+--------+----------------------------+
| OBJECT_NAME                             | ORIGINAL_NAME | TYPE   | CREATETIME                 |
+-----------------------------------------+---------------+--------+----------------------------+
| __recycle_$_1677212890_1680256737738240 | t1            | TENANT | 2023-03-31 18:03:11.107511 |
+-----------------------------------------+---------------+--------+----------------------------+
1 row in set (0.00 sec)
MySQL [oceanbase]>  alter system change tenant t1 ;   -- 切换到租户t1(因租户不存在，所以会报错)
ERROR 5160 (HY000): invalid tenant name specified in connection string
MySQL [oceanbase]> set session recyclebin=0;    -- 关闭回收站
Query OK, 0 rows affected (0.00 sec)
MySQL [oceanbase]> flashback tenant t1 to before drop ;   -- 闪回租户t1
Query OK, 0 rows affected (0.02 sec)
MySQL [oceanbase]> alter system change tenant t1 ;   -- 切换到租户t1(成功)
Query OK, 0 rows affected (0.00 sec)
#### 结论：
##### 1.如何获取回收站中，表的database？
&#8212; 获取回收站中表所在database的名称
select rb.tenant_id, rb.database_id, db.database_name, rb.table_id,
rb.tablegroup_id, rb.original_name from __all_recyclebin rb
inner join __all_virtual_database db
on rb.database_id=db.database_id;
##### 2.回收站中是否可以保存多个同名的表？闪回的时候是哪个？
回收站中可以保存多个同名的表，闪回的是最晚删除的同名表；
##### 3.关闭回收站后，是否能看到回收站中的对象？
关闭回收站后，可以看到回收站中的对象；
##### 4.回收站是全租户可⻅，还是只有当前租户可⻅？
回收站中的对象，仅租户内可⻅，其他租户不可⻅；
##### 5.关闭回收站后，是否能闪回表？
关闭回收站后，可以闪回表；
##### 6.关闭回收站后，是否能闪回租户？
关闭回收站后，可以闪回租户
#### 总结：
删除对象时，需要开启回收站，对象才会保存在回收站中；
即使回收站关闭，我们也能看到回收站中的对象；
即使回收站关闭，我们也能操作(闪回/清除)回收站中的对象；
回收站中可以保存同名的对象，根据ORIGINAL_NAME闪回时，会闪回最新删除的对象，历史对象还会保存在回收站中；
把对象从回收站中删除时，因为需要使⽤OBJECT_NAME(唯⼀属性)，所以只会命中⼀条记录；