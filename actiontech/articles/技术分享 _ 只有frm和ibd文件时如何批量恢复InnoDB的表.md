# 技术分享 | 只有.frm和.ibd文件时如何批量恢复InnoDB的表

**原文链接**: https://opensource.actionsky.com/20200718-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-07-29T01:19:59-08:00

---

作者：姚远
专注于 Oracle、MySQL 数据库多年，Oracle 10G 和 12C OCM，MySQL 5.6 ，5.7，8.0 OCP。现在鼎甲科技任顾问，为同事和客户提高数据库培训和技术支持服务。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**背景**
很多时候因为 MySQL 数据库不能启动而造成数据无法访问，但应用的数据通常没有丢失，只是系统表空间等其它文件损坏了，或者遇到 MySQL 的 bug。这个时候如果没有备份，很多人就以为数据丢失了，但实际上大部分时候数据还是有救的。对于 MyISAM 引擎的表空间，直接把对应的数据文件拷贝到一个新的数据库就行了，数据就可以恢复了。对于 InnoDB 引擎的数据库表空间可以采用传输表空间的方式把数据救回来。
**创建已经丢失的表结构**
先要安装 mysql-utilities。- `// RedHat`
- `yum -y install mysql-server mysql-utilities`
- 
- `// Debian`
- `apt install mysql-utilities`
使用 mysqlfrm 从 .frm 文件里面找回建表语句。- `// 分析一个 .frm 文件生成建表的语句`
- `mysqlfrm --diagnostic /var/lib/mysql/test/t1.frm`
- 
- `// 分析一个目录下的全部.frm文件生成建表语句`
- `root@username:~# mysqlfrm --diagnostic /var/lib/mysql/my_db/bk/ >createtb.sql`
- `root@username:~# grep "^CREATE TABLE" createtb.sql |wc -l`
- `124`
可以看到一共生成了 124 个建表语句。
有很多时候也可以从其它库里面生成建表语句，如同一个应用的其它数据库或不同的测试环境，采用下面的 mysqldump 生成建表语句：- `mysqldump --no-data --compact my_db>createtb.sql`
登录 MySQL 生成表。- `mysql> create database my_db;`
- `mysql> use my_db`
- `Database changed`
- `mysql> source createtb.sql`
- `Query OK, 0 rows affected (0.07 sec)`
- `......`
# 导入旧的数据文件
将新建的没有包括数据的 .ibd 文件抛弃- `root@username:/var/lib/mysql/my_db# ll *.ibd|wc`
- `12411167941`
- `root@username:/var/lib/mysql/my_db# mysql -e "show tables from my_db" \`
- `| grep -v  Tables_in_my_db  \`
- `| while read a; do mysql -e "ALTER TABLE my_db.$a DISCARD TABLESPACE"; done`
- `root@username:/var/lib/mysql/my_db# ll *.ibd|wc`
- `ls: cannot access '*.ibd': No such file or directory`
- `000`
可以看到所有的 .idb 文件都已经被抛弃了。然后把旧的有数据的 .ibd 文件拷贝到这个 my_db 目录下面，别忘了把属主改过来：chown mysql. *，再把这些数据文件 import 到数据库中。- `root@username:/var/lib/mysql/my_db# mysql -e "show tables from my_db" \`
- `| grep -v  Tables_in_my_db  \`
- `| while read a; \`
- `do mysql -e "ALTER TABLE my_db.$a import TABLESPACE"; done`
# 导入完成后检查表
使用 mysqlcheck 对数据库 my_db 下的所有表进行检查：- `root@username:/var/lib/mysql/my_db# mysqlcheck -c my_db`
- `my_db.cdp_backup_point                             OK`
- `......`
所有的表都导入成功。