# 技术分析 | MySQL TEXT 字段的限制

**原文链接**: https://opensource.actionsky.com/20200226-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-02-26T01:34:03-08:00

---

> **作者：****kay**
擅长 Oracle、MySQL、PostgresSQL 等多种数据库领域；
擅长 Oracle、MySQL 性能优化、数据库架构设计、数据库故障修复、数据迁移以及恢复；
热衷于研究 MySQL 数据库内核源码、分享技术文章，并拥有 Oracle OCP 认证；
就职于江苏国泰新点软件有限公司，DBA 技术团队成员。
**一、背景说明**
项目中有一个数据交换的场景，由于使用了很多个 `varchar(1000)`、 `varchar(2000)`，导致在创建表的时候，MySQL 提示：- `ERROR 1118 (42000): Row size too large (> 8126). Changing some columns to TEXT or BLOB may help.`
该表有 242 个字段，都是 varchar 类型，只是长度上有所区别。
**二、MySQL 的限制**
**说明：本文仅讨论 MySQL 中，单条记录最大长度的限制，其他的暂且搁置。**
无论是 MySQL 还是 Oracle，或者是 SQL Server，其实都有这么两层存在，一个是** Server 层**，另一个是**存储引擎层**。
其实也很好理解，可以类比一下我们 Windows 操作系统，比如常说的把 D 盘格式化成 NTFS 或者 FAT32，这个 NTFS 或者 FAT32 就可以理解成数据库中的存储引擎。
那为什么以前在用 SQL Server 或者 Oracle 的时候几乎没什么接触存储引擎这个概念呢？因为这两家都是闭源数据库，底层怎么实现的你也不知道，装好了就用呗！但是 MySQL 不一样，开源的东西，人人都可以看源码。只要你实现了那些接口，你就可以接入到 MySQL 中，作为一个存储引擎供 MySQL 的 Server 层使用。
说完这个概念，下面我们再说一下这个最大长度的限制。
> 官方文档相关说明 &#8211; Limits on Table Column Count and Row Size https://dev.mysql.com/doc/refman/5.7/en/column-count-limit.html)
2.1 MySQL Server 的长度限制
> The internal representation of a MySQL table has a maximum row size limit of 65,535 bytes.
MySQL Server 层的限制比较宽，你的一条记录不要超过 65535 个字节即可。
有的人就问了，怎么可能啊？我明明可以往 MySQL 里面放好几百兆的附件啊，咳咳&#8230;这个后面会提到。
2.2 InnoDB 的长度限制
InnoDB 作为现在官方唯一还在继续开发和支持的存储引擎（下一个版本 MySQL 8.0 中就默认看不到原先的 MyISAM 了），其长度限制比较严格，其大致的算法如下
**一条记录的长度，不能超过 innodb_page_size 大小的一半（实际上还要小一点，因为要扣除一些页中元数据信息）**
> 即默认MySQL官方推荐的 16K 的页大小，单条记录的长度不能超过 8126Byte。
为什么会有这种限制呢，其实也很好理解，InnoDB 是**以 B+ 树来组织数据**的，假设允许一行数据填满整个页，那么 InnoDB 中的数据结构将会从 B+树退化为单链表，所以 InnoDB 规定了一个页至少包含两行数据。
那这就好理解了，项目中给出的建表语句的字段中，有好几十个 varhcar(1000) 或者 varchar(2000)，累加起来已经远远超过了 8126 的限制。
2.3 字段个数的限制
同样，除了长度，对每个表有多少个列的个数也是有限制的，这里简单说一下：1. **MySQL Server 层**规定一个表的字段个数最大为 4096；2. **InnoDB 层**规定一个表的字段个数最大为 1017；
> [官方文档相关说明 &#8211; Limits on InnoDB Tables] https://dev.mysql.com/doc/refman/5.7/en/innodb-restrictions.html
至于为什么有这个限制，其实可以不用深究，因为是代码中写死的。
至于原因，个人猜测和 MySQL 的定位有关系，MySQL 一直定位于 OLTP 业务，OLTP 业务的特点就是短平快，字段数过多或者长度太长，都会影响 OLTP 业务的 TPS（所以那些拿 MySQL 存附件的同时，还在抱怨 MySQL 性能差的同学，是不是该反思一下了？）
**三、TEXT 类型的字段**
回到我们项目中的问题，既然那么多 varchar 超过了限制，那按照提示，我们直接把所有字段改成 `TEXT`是不是就可以了呢？
我们做了测试，发现依然失败，提示和之前一样。
3.1 TEXT 字段介绍
> 官方文档说明 &#8211; innodb-row-format-dynamic https://dev.mysql.com/doc/refman/5.7/en/innodb-row-format-dynamic.html
关于 TEXT 字段的存储的方式和很多因素有关，他除了和本身记录的格式（参数 INNODB_ROW_FORMART，当前默认格式为 DYNAMIC）有关系，同时和当前记录所在的页的存储长度也有关系，简单归纳一下：
1. 在 COMPACT 格式下，TEXT 字段的前 768 个字节存储在当前记录中，超过的部分存储在溢出页(overflow page)中，同时当前页中增加一个 20 个字节的指针（即 SPACEID + PAGEID + OFFSET）和本地长度信息（2 个字节），共计 768 + 20 + 2 = 790 个字节存储在当前记录。
2. 在 DYNAMIC 格式下，一开始会尽可能的存储所有内容，当该记录所在的页快要被填满时，InnoDB 会选择该页中一个最长的字段（所以也有可能是 BLOB 之类的类型），将该字段的所有内容存储到溢出页（overflow page）中，同时在原记录中保留 20 个字节的指针`。
3. 当 TEXT 字段存储的内容不大于 40 个字节时，这 40 个字节都会存储在该记录中，此时该字段的长度为 40 + 1（本地长度信息）= 41 个字节。> 这里提到一个溢出页的概念，其实就是 MySQL 中的一种数据存储机制，当一条记录中的内容，无法存储在单独的一个页内（比如存储一些大的附件），MySQL 会选择部分列的内容存储到其他数据页中，这种仅保存数据的页就叫溢出页（overflow page）。
3.2 计算 TEXT 字段的最大列数
有了上述概念，现在我们可以来算一下 TEXT 字段一共可以存储多少列（以目前默认的 DYNAMIC 格式，且 innodb_strict_mode=on 为例），假设可以存储 x 列。
除了我们创建的字段，每个记录（ROW）中还存在元信息：1. header 信息（5 个字节）；
2. 列是否为 null 的 bitmap 信息（ceil(x/8) 即向上取整）
3. 系统字段：主键 ID（6 个字节）、事物 ID（6个字节）、回滚指针（7 个字节）；
那么计算公式就是：
- `$5 + ceil(x/8) + 6 + 6 + 7 + x * 41 <= 8126，求 x 的解 $。`
最终我们可以计算出符合该公式的 x 的解为 197。
那是不是就可以插入 197 个的 text 呢？我们又做了一个测试，发现还是失败的（What&#8217;s The F**K？）。
最终通过源码我们找到了问题的答案（以当前最新的 5.7.20 为例）：
- `/* Filename:./storage/innobase/dict/dict0dict.cc 第 2504 行 */`
- `if (rec_max_size >= page_rec_max) {   /* 居然是 >= */`
- `    ib::error_or_warn(strict)`
- `        << "Cannot add field " << field->name`
- `        << " in table " << table->name`
- `        << " because after adding it, the row size is "`
- `        << rec_max_size`
- `        << " which is greater than maximum allowed"`
- `        " size (" << page_rec_max`
- `        << ") for a record on index leaf page.";`
- 
- `    return(TRUE);`
- `}`
通过代码我们可以发现，不能刚好等于最大值，所以在当前 MySQL 版本（5.7.x）中，极端情况下，可以存储 196 个 TEXT 字段。
同时我们也进行了测试，的确可以创建有且仅含有 196 个 TEXT 字段的表。
我们可以构造一下 `create table` 的测试语句，包含 196 个 TEXT 字段的 sql 文件 `c_196.sql` 和 197 个 TEXT 字段的 sql 文件 `c_197.sql`- `create table c_196( f1 text,`
- `f2 text,`
- `f3 text,`
- `......`
- `f196 text`
- `);`
- `-- 197 个字段的的类似，多增加 f197 text 字段`
- 
- `mysql> source c_197.sql`
- `ERROR 1118 (42000): Row size too large (> 8126). Changing some columns to TEXT or BLOB may help. In current row format, BLOB prefix of 0 bytes is stored inline.`
- 
- `mysql> source c_196.sql`
- `Query OK, 0 rows affected (0.01 sec)`
- 
- `mysql> select count(*) from information_schema.columns where table_name='c_196' and data_type='text';`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|      196 |  -- 共 196 个字段`
- `+----------+`
- `1 row in set (0.00 sec)`
> 备注：能这样保存 196 个 TEXT 字段，并不代表我们推荐这样做，如果业务上达到了这种限制，建议业务上做一定的拆分。
3.3 关于 innodb_strict_mode
细心的同学可能会想，如果所有 TEXT 字段都是以溢出页（overflow page）的方式存储，本地记录都是以指针（20 个字节）进行存储，那不是可以存储更多的字段呢？
确实是的，但是 MySQL 现在开启了严格模式（innodb_strict_mode=on），由于 MySQL 层面无法保证所有数据都是存储在溢出页（业务才能决定），所以在严格模式下，宁愿牺牲字段个数的上限，也要确保所有的 insert 或者 update 能成功执行。
那我们关闭严格模式，看一下，究竟能存储多少个 TEXT 字段呢？继续套公式
- `$5 + ceil(x/8) + 6 + 6 + 7 + x * 20 <= 8126，求 x 的解 $。`
最终我们可以计算出符合该公式的 x 的解为 402。**但是事实真的如此么？**
同样我们也可以构造一下 `create table` 的测试语句，包含 402 个 TEXT 字段的 sql 文件 `c_402.sql`
- `create table c_402( f1 text,`
- `f2 text,`
- `f3 text,`
- `......`
- `f402 text`
- `);`
- 
- `mysql> source c_402.sql`
- `Query OK, 0 rows affected, 1 warning (0.02 sec)`
- `-- 虽然成功了，但是有一个警告`
- 
- `mysql> show warnings\G`
- `*************************** 1. row ***************************`
- `  Level: Warning`
- `   Code: 139`
- `Message: Row size too large (> 8126). Changing some columns to TEXT or BLOB may help. In current row format, BLOB prefix of 0 bytes is stored inline.`
- `1 row in set (0.00 sec)`
- 
- `mysql> show tables;`
- `+---------------+`
- `| Tables_in_db2 |`
- `+---------------+`
- `| c_402         |`
- `+---------------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> select count(*) from information_schema.columns where table_name='c_402' and data_type='text';`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|      402 |`
- `+----------+`
- `1 row in set (0.00 sec)`
看到上面的执行结果，虽然 create table 执行成功了，通过 `show table` 也的确看了 c_402 这个 table，但是出现了** warnings**。
warnings 的内容我们应该很熟悉了，因为没有了严格模式的保护，mysql 允许你创建成功，但是给了一个 warning。
有兴趣的同学其实可以继续测试，其创建的 text 字段可以更多，可以达到 innodb 的最大限制 1017 个字段，如下所示：
- `mysql> source c_1017.sql`
- `Query OK, 0 rows affected, 1 warning (0.04 sec) -- 一如既往的Warnings`
- 
- `mysql> select count(*) from information_schema.columns where table_name='c_1017' and data_type='text';`
- `+----------+`
- `| count(*) |`
- `+----------+`
- `|     1017 |`
- `+----------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> source c_1018.sql`
- `ERROR 1117 (HY000): Too many columns`
但是这样做了以后，虽然建立了 1017 个 text 列，如果业务上进行 insert 或者 update 的时候，mysql 无法保证能执行。
所以项目上建议还是保持默认值，将 innodb_strict_mode 设置为 on（公司的 bin 包中已经默认开启）
**四、总结**
很多同学看到这里，可能会想，MySQL 弱暴啦，怎么这么多限制啊，你看 Oracle 多强啊&#8230;&#8230;
其实，针对项目中这种超多字段，同时又只能用 MySQL 的场景下，我们可以使用 MySQL 5.7 中最新推出的 JSON 类型的字段，这样 N 多数据只算在一个 JSON 字段哦，同时还有丰富的 JSON 函数予以支持，业务上使用起来其实还是比较方便的（5.6 等版本可以存在 blob 中，只是需要业务自己做 json_encode/json_decode 等操作）。
这里更要强调的是，MySQL 作为一个绝大部分互联网公司都在广泛使用的 OLTP 型数据库（微信支付的交易库就运行在 MySQL 社区版之上），这些成功案例已经证明了 MySQL 是一个优秀的工业级数据库。
当然除了他自身在不断进步以外，同样需要我们从业务上进行良好的表结构设计，编写规范的 SQL 语句以及采用合适的集群的架构，才能发挥出 MySQL 自身的潜力，而不是一味的和 Oracle 进行对比，拿 Oracle 的优点和 MySQL 的缺点进行比较，这样无法做到客观和公正。