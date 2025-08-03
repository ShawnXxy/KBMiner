# 47 期：插入记录的 Undo 日志

**原文链接**: https://opensource.actionsky.com/47-%e6%9c%9f%ef%bc%9a%e6%8f%92%e5%85%a5%e8%ae%b0%e5%bd%95%e7%9a%84-undo-%e6%97%a5%e5%bf%97/
**分类**: 技术干货
**发布时间**: 2025-01-05T22:01:47-08:00

---

插入记录产生的 Undo 日志格式。
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 准备工作
创建测试表：
`CREATE TABLE `t1` (
`id` int unsigned NOT NULL AUTO_INCREMENT,
`i1` int DEFAULT '0',
PRIMARY KEY (`id`) USING BTREE,
KEY `idx_i1` (`i1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
`
示例 SQL：
`INSERT INTO `t1` (`id`, `i1`)
VALUES (50, 501);
`
## 2. Insert Undo 日志格式
插入一条记录到表中，首先会插入记录到主键索引，然后遍历二级索引，把记录插入到各个二级索引中。
插入记录到主键索引之前，会生成 Undo 日志，并写入 Undo 页。插入记录到二级索引，不会生成 Undo 日志。插入记录的 Undo 日志格式比较简单，如下图所示。
![](asserts/47/1-format.png)
各属性详细说明如下：
- **next_record_offset**，占用 2 字节，表示下一条 Undo 日志在 Undo 页中的偏移量。
- **undo_type**，占用 1 字节，表示这条 Undo 日志的类型。插入记录产生的 Undo 日志，类型为 `TRX_UNDO_INSERT_REC`。
- **undo_no**，64 位整数，压缩之后占用 1 ~ 11 字节，表示这条 Undo 日志的编号。
- **table_id**，64 位整数，压缩之后占用 1 ~ 11 字节，这个属性值是表 ID，表示事务插入记录到哪个表产生的这条 Undo 日志。
- **len**，32 位整数，压缩之后占用 1 ~ 5 字节，表示主键字段值的长度。
- **value**，占用多少字节的存储空间，取决于主键字段的数据类型和具体值，这个属性中存储的就是主键字段值，存储时不会压缩。
- **current_record_offset**，这条 Undo 日志在 Undo 页中的偏移量。
如果主键是由多个字段组成的联合主键，插入记录产生的 Undo 日志中，会按照联合主键定义的字段顺序写入所有主键字段的长度和值：len_1、value_1、len_2、value_2、&#8230;、len_N、value_N。
## 3. Insert Undo 日志内容
示例 SQL 插入记录到 t1 表中产生的 Undo 日志，如下图所示。
![](asserts/47/5_insert.png)
各属性值详细说明如下：
- **285**，下一条 Undo 日志在 Undo 页中的偏移量。这个值不会压缩，固定占用 2 字节。
- **11**，表示这条 Undo 日志是插入记录产生的，代码里定义为 `TRX_UNDO_INSERT_REC`。这个值不会压缩，固定占用 1 字节。
- **0**，这条 Undo 日志的编号。压缩之后占用 1 字节。
这个值来源于事务对象的 `undo_no` 属性。事务产生的第一条 Undo 日志编号为 0，第二条 Undo 日志编号为 1，依此类推。
- **1412**，这是 t1 表的 ID。压缩之后占用 2 字节。
- **4**，主键字段值的长度。压缩之后占用 1 字节。
- **50**，主键字段值。主键字段类型为 `int unsigned`，占用 4 字节。
- **272**，这条 Undo 日志在 Undo 页中的偏移量。这个值不会压缩，固定占用 2 字节。
## 4. Insert Undo 日志地址
InnoDB 存储引擎的表中，每条记录都有个隐藏字段 `DB_ROLL_PTR`，字段长度固定为 7 字节。通过这个字段值可以找到 Undo 日志（也是 MVCC 中记录的历史版本）。
从整体上来看，我们可以认为它是 Undo 日志的地址。但是，这个字段值实际上由 4 部分组成，如下图所示。
![](asserts/47/10_db_roll_ptr.png)
各属性详细说明如下：
- **is_insert**，表示这条 Undo 日志是否是插入记录产生的。
- **undo_space_id**，这条 Undo 日志所属 Undo 表空间的 ID。
InnoDB 最多支持 127 个 Undo 表空间，ID 范围是 0 ~ 127。7 bit 可以表示的最大数字正好是 127。
- **page_no**，这条 Undo 日志所属 Undo 页的页号。
- **offset**，这条 Undo 日志在 Undo 页中的偏移量。
DB_ROLL_PTR 的计算公式如下：
`is_insert << 55 | undo_space_id << 48 | page_no << 16 | offset
`
以示例 SQL 为例，插入记录时产生 Undo 日志得到的各属性值如下：
- is_insert = true, 转换成整数就是 1。
- undo_space_id = 2。
- page_no = 573。
- offset = 272。
用 Shell 按照以上公式计算得到 DB_ROLL_PTR，如下：
```
# 输出结果为 36591747009937680
echo $((1 << 55 | 2 << 48 | 573 << 16 | 272))
```