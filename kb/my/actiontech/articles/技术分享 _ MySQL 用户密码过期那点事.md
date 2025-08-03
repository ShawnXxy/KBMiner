# 技术分享 | MySQL 用户密码过期那点事

**原文链接**: https://opensource.actionsky.com/20210514-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-05-14T00:41:24-08:00

---

作者：耿进
爱可生 DBA 团队成员，负责公司 DMP 产品的运维和客户 MySQL 问题的处理。对数据库技术有着浓厚的兴趣。你见过凌晨四点 MySQL 的 error 吗？
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
`    <h2 data-tool="mdnice编辑器" style="margin-top: 30px; padding: 0px; font-weight: bold; font-size: 22px; max-width: 100%; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; overflow-wrap: break-word !important;">概述：</h2><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">我们先来重新认识一下 mysql.user 表中关于密码过期的字段，</p><pre data-tool="mdnice编辑器" style="margin-top: 10px; margin-bottom: 10px; padding: 0px; max-width: 100%; color: rgb(0, 0, 0); font-size: 16px; background-color: rgb(255, 255, 255); border-radius: 5px; box-shadow: rgba(0, 0, 0, 0.55) 0px 2px 10px;"><code>mysql> use mysql
Database changed
mysql> desc user;
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
| Field                  | Type                              | Null | Key | Default               | Extra |
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
。。。。
| password_expired       | enum('N','Y')                     | NO   |     | N                     |       |
| password_last_changed  | timestamp                         | YES  |     | NULL                  |       |
| password_lifetime      | smallint(5) unsigned              | YES  |     | NULL                  |       |
+------------------------+-----------------------------------+------+-----+-----------------------+-------+
45 rows in set (0.01 sec)
mysql> </code></pre><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">password_expired：从 MySQL 5.6.6 版本开始，添加了 password_expired 功能，它允许设置用户的过期时间。</p><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">password_last_changed：密码最后一次修改的时间。</p><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">password_lifetime：该用户密码的生存时间，默认值为 NULL，除非手动修改此用户密码过期机制，否则都是 NULL。</p><p style="margin-top: 20px; margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">另外解释一个参数：</p><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">default_password_lifetime：从 MySQL 5.7.4 版本开始，此全局变量可以设置一个全局的自动密码过期策略。</p>        
<h2 data-tool="mdnice编辑器" style="margin-top: 30px; padding: 0px; font-weight: bold; font-size: 22px; max-width: 100%; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; overflow-wrap: break-word !important;">测试：</h2><h4 data-tool="mdnice编辑器" style="margin-top: 30px; padding: 0px; font-weight: bold; font-size: 18px; max-width: 100%; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; overflow-wrap: break-word !important;">一、password_expired：手动设置过期</h4><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;"><strong style="margin: 0px; padding: 0px; max-width: 100%; overflow-wrap: break-word !important;">1. 设置密码永不过期</strong></p><pre data-tool="mdnice编辑器" style="margin-top: 10px; margin-bottom: 10px; padding: 0px; max-width: 100%; color: rgb(0, 0, 0); font-size: 16px; background-color: rgb(255, 255, 255); border-radius: 5px; box-shadow: rgba(0, 0, 0, 0.55) 0px 2px 10px;"><code>mysql> grant all on *.* to test@'localhost' identified by '123';
Query OK, 0 rows affected, 2 warnings (0.03 sec)
mysql> select User,password_last_changed,password_lifetime,password_expired from mysql.user;
+---------------+-----------------------+-------------------+------------------+
| User          | password_last_changed | password_lifetime | password_expired |
+---------------+-----------------------+-------------------+------------------+
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| mysql.session | 2021-03-31 14:11:06   |              NULL | N                |
| mysql.sys     | 2021-03-31 14:11:06   |              NULL | N                |
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| universe_op   | 2021-03-31 14:11:10   |              NULL | N                |
| kobe          | 2021-04-01 16:45:20   |              NULL | N                |              |
| test          | 2021-04-16 17:30:18   |              NULL | N                |
+---------------+-----------------------+-------------------+------------------+
7 rows in set (0.00 sec)
mysql> ALTER USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
Query OK, 0 rows affected (0.00 sec)
mysql> 
mysql> select User,password_last_changed,password_lifetime,password_expired from mysql.user;
+---------------+-----------------------+-------------------+------------------+
| User          | password_last_changed | password_lifetime | password_expired |
+---------------+-----------------------+-------------------+------------------+
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| mysql.session | 2021-03-31 14:11:06   |              NULL | N                |
| mysql.sys     | 2021-03-31 14:11:06   |              NULL | N                |
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| universe_op   | 2021-03-31 14:11:10   |              NULL | N                |
| kobe          | 2021-04-01 16:45:20   |              NULL | N                |                |
| test          | 2021-04-16 17:30:18   |                 0 | N                |
+---------------+-----------------------+-------------------+------------------+
7 rows in set (0.00 sec)
mysql>
注：如果该参数设置为0，即表示密码永不过期。</code></pre><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;"><strong style="margin: 0px; padding: 0px; max-width: 100%; overflow-wrap: break-word !important;">2. 手动设置该用户密码为 30 day（它会自动覆盖密码过期的全局策略）</strong></p>
`
```
mysql> ALTER USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 30 DAY;
Query OK, 0 rows affected (0.01 sec)
mysql> select User,password_last_changed,password_lifetime,password_expired from mysql.user;
+---------------+-----------------------+-------------------+------------------+
| User          | password_last_changed | password_lifetime | password_expired |
+---------------+-----------------------+-------------------+------------------+
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| mysql.session | 2021-03-31 14:11:06   |              NULL | N                |
| mysql.sys     | 2021-03-31 14:11:06   |              NULL | N                |
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| universe_op   | 2021-03-31 14:11:10   |              NULL | N                |
| kobe          | 2021-04-01 16:45:20   |              NULL | N                |                |
| test          | 2021-04-16 17:30:18   |                30 | N                |
+---------------+-----------------------+-------------------+------------------+
7 rows in set (0.00 sec)
mysql> 
```
**3. 设置密码立马过期**
`mysql> ALTER USER 'hhh'@'%' PASSWORD EXPIRE;
Query OK, 0 rows affected (0.01 sec)
mysql> 
mysql> select User,password_last_changed,password_lifetime,password_expired from mysql.user;
+---------------+-----------------------+-------------------+------------------+
| User          | password_last_changed | password_lifetime | password_expired |
+---------------+-----------------------+-------------------+------------------+
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| mysql.session | 2021-03-31 14:11:06   |              NULL | N                |
| mysql.sys     | 2021-03-31 14:11:06   |              NULL | N                |
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| universe_op   | 2021-03-31 14:11:10   |              NULL | N                |
| kobe          | 2021-04-01 16:45:20   |              NULL | N                |                |
| test          | 2021-04-16 17:30:18   |                30 | Y                |
| gengjin       | 2021-04-16 17:42:33   |              NULL | N                |
| hhh           | 2021-04-16 18:00:32   |              NULL | Y                |
| kkk           | 2021-04-16 18:26:06   |              NULL | N                |
+---------------+-----------------------+-------------------+------------------+
10 rows in set (0.00 sec)
mysql> exit
Bye
[root@manage01 ~]# /opt/mysql/base/5.7.25/bin/mysql -uhhh -p -S /opt/mysql/data/3306/mysqld.sock
Logging to file '/mysqldata/mysql_3306/log/test.log'
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or g.
Your MySQL connection id is 39469
Server version: 5.7.25-log
Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or 'h' for help. Type 'c' to clear the current input statement.
mysql> show databases;
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
mysql> `
#### 二、default_password_lifetime：自动过期的机制
**1. 设置全局密码过期时间：**
`#配置文件
[mysqld]
default_password_lifetime=90
or
#命令行全局修改
mysql> SET GLOBAL default_password_lifetime = 90;
Query OK, 0 rows affected (0.00 sec)
mysql>
mysql> show variables like "default_password_lifetime";
+---------------------------+-------+
| Variable_name             | Value |
+---------------------------+-------+
| default_password_lifetime | 90    |
+---------------------------+-------+
1 row in set (0.00 sec)
mysql> `
**2. 创建用户：**
`mysql> grant all on *.* to hhh@'%' identified by '123';
Query OK, 0 rows affected, 1 warning (0.04 sec)
mysql> select User,password_last_changed,password_lifetime,password_expired from mysql.user;
+---------------+-----------------------+-------------------+------------------+
| User          | password_last_changed | password_lifetime | password_expired |
+---------------+-----------------------+-------------------+------------------+
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| mysql.session | 2021-03-31 14:11:06   |              NULL | N                |
| mysql.sys     | 2021-03-31 14:11:06   |              NULL | N                |
| root          | 2021-03-31 14:11:10   |              NULL | N                |
| universe_op   | 2021-03-31 14:11:10   |              NULL | N                |
| kobe          | 2021-04-01 16:45:20   |              NULL | N                |                |
| test          | 2021-04-16 17:30:18   |                30 | Y                |
| gengjin       | 2021-04-16 17:42:33   |              NULL | N                |
| hhh           | 2021-04-16 18:00:32   |              NULL | N                |
+---------------+-----------------------+-------------------+------------------+
9 rows in set (0.00 sec)
mysql> `
注：很多人一看这个 password_lifetime 为什么没有变，不应该变成 90 吗，是不是 mysql 的 bug，其实不然。
> 
顺便贴一个这个“bug”的地址：
https://bugs.mysql.com/bug.php?id=89349
`                                    <img width="750" height="138" src="https://opensource.actionsky.com/wp-content/uploads/2021/05/20210513-gj-01-1024x189.png" alt="" srcset="https://opensource.actionsky.com/wp-content/uploads/2021/05/20210513-gj-01-1024x189.png 1024w, https://opensource.actionsky.com/wp-content/uploads/2021/05/20210513-gj-01-300x55.png 300w, https://opensource.actionsky.com/wp-content/uploads/2021/05/20210513-gj-01-768x142.png 768w" sizes="(max-width: 750px) 100vw, 750px" />                                           
<p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">它的工作方式如下：</p><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">有一个全局系统变量 default_password_lifetime，它为使用默认密码生存期的所有帐户指定策略。在系统表中这将存储一个 NULL。NULL 值被用作一个标志，表明所涉及的帐户没有每个用户密码的特殊生存期。通过 ALTER USER password EXPIRE NEVER(将列设置为0)或 ALTER USER password EXPIRE INTERVAL N DAY(将列设置为 N)设置每个用户的特殊密码生存期。</p><p data-tool="mdnice编辑器" style="margin-bottom: 0px; padding: 8px 0px; max-width: 100%; clear: both; min-height: 1em; color: rgb(0, 0, 0); font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; line-height: 26px; overflow-wrap: break-word !important;">因此，没有设置特定密码生存期的所有用户的所有密码生存期都将跟随全局变量的值。</p>        
<p style="margin-top: 25px; margin-bottom: 0px; padding: 8px 10px; max-width: 100%; overflow-wrap: break-word; clear: both; min-height: 1em; color: black; font-family: Optima-Regular, Optima, PingFangSC-light, PingFangTC-light, "PingFang SC", Cambria, Cochin, Georgia, Times, "Times New Roman", serif; font-size: 16px; letter-spacing: 0px; word-break: break-word; line-height: normal;"><strong style="margin: 0px; padding: 0px; max-width: 100%; overflow-wrap: break-word !important;">文章推荐：</strong></p>
`
[技术分享 | 数据校验工具 pt-table-checksum](https://opensource.actionsky.com/20201229-mysql/)