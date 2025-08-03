# 技术分享 | MySQL 大对象一例

**原文链接**: https://opensource.actionsky.com/20190716-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-07-15T22:00:25-08:00

---

**背景******
MySQL 一直以来都有 TEXT、BLOB 等类型用来存储图片、视频等大对象信息。比如一张图片，随便一张都 5M 以上。视频也是，随便一部视频就是 2G 以上。
假设用 MySQL 来存放电影视频等信息，一部是 2G，那么存储 1000 部就是 2TB，2TB 也就是 1000 条记录而已，但是对数据库性能来说，不仅仅是看记录数量，更主要的还得看占用磁盘空间大小。空间大了，所有以前的经验啥的都失效了。
所以一般来说存放这类信息，也就是存储他们的存放路径，至于文件本身存放在哪里，那这就不是数据库考虑的范畴了。数据库只关心怎么来的快，怎么来的小。
**举例**
虽然不推荐 MySQL 这样做，但是也得知道 MySQL 该怎么做才行，做到心里有数。比如下面一张微信图片，大概 5M 的样子。
- `root@ytt:/var/lib/mysql-files# ls -sihl 微信图片_20190711095019.jpg`
- `274501 5.4M -rw-r--r-- 1 root root 5.4M Jul 11 07:17 微信图片_20190711095019.jpg`
拷贝 100 份这样的图片来测试
- `root@ytt:/var/lib/mysql-files# for i in `seq 1 100`; do cp 微信图片_20190711095019.jpg "$i".jpg;done;`
- 
- `root@ytt:/var/lib/mysql-files# ls`
- `100.jpg   17.jpg  25.jpg  33.jpg  41.jpg  4.jpg   58.jpg  66.jpg  74.jpg  82.jpg  90.jpg  99.jpg  f8.tsv`
- `10.jpg    18.jpg  26.jpg  34.jpg  42.jpg  50.jpg  59.jpg  67.jpg  75.jpg  83.jpg  91.jpg  9.jpg   微信图片_20190711095019.jpg`
- `1111.jpg  19.jpg  27.jpg  35.jpg  43.jpg  51.jpg  5.jpg   68.jpg  76.jpg  84.jpg  92.jpg  f1.tsv`
- `11.jpg    1.jpg   28.jpg  36.jpg  44.jpg  52.jpg  60.jpg  69.jpg  77.jpg  85.jpg  93.jpg  f2.tsv`
- `12.jpg    20.jpg  29.jpg  37.jpg  45.jpg  53.jpg  61.jpg  6.jpg   78.jpg  86.jpg  94.jpg  f3.tsv`
- `13.jpg    21.jpg  2.jpg   38.jpg  46.jpg  54.jpg  62.jpg  70.jpg  79.jpg  87.jpg  95.jpg  f4.tsv`
- `14.jpg    22.jpg  30.jpg  39.jpg  47.jpg  55.jpg  63.jpg  71.jpg  7.jpg   88.jpg  96.jpg  f5.tsv`
- `15.jpg    23.jpg  31.jpg  3.jpg   48.jpg  56.jpg  64.jpg  72.jpg  80.jpg  89.jpg  97.jpg  f6.tsv`
- `16.jpg    24.jpg  32.jpg  40.jpg  49.jpg  57.jpg  65.jpg  73.jpg  81.jpg  8.jpg   98.jpg  f7.tsv`
我们建三张表，分别用 LONGBLOB、LONGTEXT 和 VARCHAR 来存储这些图片信息
- `mysql> show create table tt_image1\G`
- `*************************** 1. row ***************************`
- `       Table: tt_image1`
- `Create Table: CREATE TABLE `tt_image1` (`
- `  `id` int(11) NOT NULL AUTO_INCREMENT,`
- `  `image_file` longblob,`
- `  PRIMARY KEY (`id`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci`
- `1 row in set (0.00 sec)`
- ``
- 
- `mysql> show create table tt_image2\G`
- `*************************** 1. row ***************************`
- `       Table: tt_image2`
- `Create Table: CREATE TABLE `tt_image2` (`
- `  `id` int(11) NOT NULL AUTO_INCREMENT,`
- `  `image_file` longtext,`
- `  PRIMARY KEY (`id`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci`
- `1 row in set (0.00 sec)`
- ``
- 
- `mysql> show create table tt_image3\G`
- `*************************** 1. row ***************************`
- `       Table: tt_image3`
- `Create Table: CREATE TABLE `tt_image3` (`
- `  `id` int(11) NOT NULL AUTO_INCREMENT,`
- `  `image_file` varchar(100) DEFAULT NULL,`
- `  PRIMARY KEY (`id`)`
- `) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci`
- `1 row in set (0.00 sec)`
我们来给三张表插入 100 张图片**（插入前，建议把 max_allowed_packet 设置到最大）**
- `tt_image1`
- `root@ytt:/var/lib/mysql-files# for i in `seq 1 100`; \`
- `do mysql -S /var/run/mysqld/mysqld.sock -e "insert into ytt.tt_image1(image_file)  \`
- `values (load_file('/var/lib/mysql-files/$i.jpg'))";done;`
- ``
- 
- `tt_image2`
- `root@ytt:/var/lib/mysql-files# for i in `seq 1 100`; \`
- `do mysql -S /var/run/mysqld/mysqld.sock -e "insert into ytt.tt_image2(image_file)  \`
- `values (hex(load_file('/var/lib/mysql-files/$i.jpg')))";done;`
- ``
- 
- `tt_image3`
- `root@ytt:/var/lib/mysql-files# aa='begin;';for i in `seq 1 100`; \`
- `do aa=$aa"insert into ytt.tt_image3(image_file) values  \`
- `('/var/lib/mysql-files/$i.jpg');"; \`
- `done;aa=$aa'commit;';mysql -S /var/run/mysqld/mysqld.sock -e "`echo $aa`";`
检查下三张表记录数
- `mysql> select 'tt_image1' as name ,count(*) from tt_image1 union all \`
- `select 'tt_image2',count(*) from tt_image2 union all select 'tt_image3', count(*) from tt_image3;`
- `+-----------+----------+`
- `| name      | count(*) |`
- `+-----------+----------+`
- `| tt_image1 |      100 |`
- `| tt_image2 |      100 |`
- `| tt_image3 |      100 |`
- `+-----------+----------+`
- `3 rows in set (0.00 sec)`
看下文件大小，可以看到实际大小排名，LONGTEXT 字段存储的最大，LONGBLOB 字段缩小到一半，最小的是存储图片路径的表 tt_image3。**所以这里从存储空间来看，存放路径最占优势。**
- `root@ytt:/var/lib/mysql/ytt# ls -silhS tt_image*`
- `274603 1.1G -rw-r----- 1 mysql mysql 1.1G Jul 11 07:27 tt_image2.ibd`
- `274602 545M -rw-r----- 1 mysql mysql 544M Jul 11 07:26 tt_image1.ibd`
- `274605  80K -rw-r----- 1 mysql mysql 112K Jul 11 07:27 tt_image3.ibd`
**那么怎么把图片取出来呢？******
tt_image3 肯定是最容易的
- `mysql> select * from tt_image3;`
- `+----+----------------------------+`
- `| id | image_file                 |`
- `+----+----------------------------+`
- `|  1 | /var/lib/mysql-files/1.jpg |`
- `+----+----------------------------+`
- `...`
- `100 rows in set (0.00 sec)`
tt_image1 直接导出来二进制文件即可，下面我写了个存储过程，导出所有图片。
- `mysql> DELIMITER $$`
- `mysql> USE `ytt`$$`
- `mysql> DROP PROCEDURE IF EXISTS `sp_get_image`$$`
- `mysql> CREATE DEFINER=`ytt`@`localhost` PROCEDURE `sp_get_image`()`
- `mysql> BEGIN`
- `      DECLARE i,cnt INT DEFAULT 0;`
- `      SELECT COUNT(*) FROM tt_image1 WHERE 1 INTO cnt;`
- `      WHILE i < cnt DO`
- `        SET @stmt = CONCAT('select image_file from tt_image1  limit ',i,',1 into dumpfile ''/var/lib/mysql-files/image',i,'.jpg''');`
- `        PREPARE s1 FROM @stmt;`
- `        EXECUTE s1;`
- `        DROP PREPARE s1;`
- `      SET i = i + 1;`
- `      END WHILE;`
- `      END$$`
- `mysql> DELIMITER ;`
- `mysql> call sp_get_image;`
tt_image2 类似，把 select 语句里 image_file 变为 unhex(image_file) 即可。
**总结**
这里我举了个用 MySQL 来存放图片的例子，总的来说有以下三点：
- 占用磁盘空间大（这样会带来各种各样的功能与性能问题，比如备份，写入，读取操作等）
- 使用不易
- 还是推荐用文件路径来代替实际的文件内容存放
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)