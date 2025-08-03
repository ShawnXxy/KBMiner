# 技术分享 | 详解SQL加密函数：AES_ENCRYPT()

**原文链接**: https://opensource.actionsky.com/20221102-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-11-03T23:38:08-08:00

---

作者：岳明强
爱可生北京分公司 DBA 团队成员，人称强哥，负责数据库管理平台的运维和 MySQL 问题处理。擅长对 MySQL 的故障定位。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
最近由于客户对于 MySQL 数据加密有一些要求，特地对于 MySQL 的数据加密研究了一下。当前 MySQL 原生的数据加密有静态加密，即加密数据库的物理文件，防止直接拖库后读取敏感数据，还有 SQL 级别的加密，只加密部分字段，即使获取到数据，也无法进行解读。下面主要是对于 SQL 加密函数 AES_ENCRYPT() 的一些说明
#### 参数说明
解密：AES_DECRYPT()：AES_DECRYPT(crypt_str,key_str[,init_vector][,kdf_name][,salt][,info | iterations])
加密：AES_ENCRYPT(str,key_str[,init_vector][,kdf_name][,salt][,info | iterations])
srt：加密之后的字符串
crypt_str：用来加密的字符串，加密后的字段长度可以用以下公式计算，其中 trunc() 表示小数部分舍弃，即如果输入单个字符，那么存储的字段长度即为最短长度16
16 * (trunc(string_length / 16) + 1)
key_str：加密密钥，不建议使用明文密钥，应该先用hash处理一下
init_vector 初始向量，用于块加密的模式（block_encryption_mode），默认的加密模式为aes-128-ecb，不需要初始向量，其它的加密模式（CBC、CFB1、CFB8、CFB128 和 OFB）都需要初始向量，其中 ecb 的加密模式并不安全，建议使用其它的加密模式，使用 init_vector 加密后 也要使用相同的 init_vector 解密
kdf_name,salt,info,iterations：为 KDF 的相关参数，相对于更加安全，官方建议使用，但由于版本要求过高（5.7.40以及8.0.30之后），这里就先不考虑了
#### 使用说明
使用官方 AES（高级加密标准）算法解密数据，默认使用128-bit也可以使用196或者256，密钥的长度与性能和安全度有关，
使用 AES_ENCRYPT(）对于基于 statement 的 binlog 类型是不安全的，建议使用 SSL 连接，防止将加密函数的密码和其它敏感值作为明文发送到服务器。
简单示例：
mysql [localhost:5734] {root} (test) > show create table test;
+-------+-----------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                          |
+-------+-----------------------------------------------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (
`n` char(200) DEFAULT NULL,
`t` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+-----------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
mysql [localhost:5734] {root} (test) > insert into test values(aes_encrypt('b','test'),1);
Query OK, 1 row affected (0.00 sec)
mysql [localhost:5734] {root} (test) > select * from test;
+----------------------------+------+
| n                          | t    |
+----------------------------+------+
| x                          |    0 |
| y                          |    0 |
| ùpñU!ã¿§ÒŸWHƒôò           |    1 |
+----------------------------+------+
3 rows in set (0.00 sec)
mysql [localhost:5734] {root} (test) > select aes_decrypt(n,'test') from test where t = 1;
+-----------------------+
| aes_decrypt(n,'test') |
+-----------------------+
| b                     |
+-----------------------+
1 row in set (0.00 sec)
经过加密和压缩的结果返回二进制字符，所以建议配置为VARBINARY或BLOB二进制字符串数据类型的列，防止字符集转换从而导致插入失败
mysql [localhost:5729] {msandbox} (test) > create table test (a int ,n varchar(60));
Query OK, 0 rows affected (0.06 sec)
mysql [localhost:5729] {msandbox} (test) > insert into test values(1,AES_ENCRYPT('test','test'));
ERROR 1366 (HY000): Incorrect string value: '\x87\xBD\x908\x85\x94...' for column 'name' at row 1
mysql [localhost:5729] {msandbox} (test) > alter table test MODIFY `n` VARBINARY(180);
Query OK, 0 rows affected (0.13 sec)
Records: 0  Duplicates: 0  Warnings: 0
mysql [localhost:5729] {msandbox} (test) > insert into test values(1,AES_ENCRYPT('test','test'));
Query OK, 1 row affected (0.00 sec)
mysql [localhost:5729] {msandbox} (test) > select a,AES_decrypt(n,'test') from test;
+------+--------------------------+
| a   | AES_decrypt(n,'test') |
+------+--------------------------+
|    1 | test                     |
+------+--------------------------+
1 row in set (0.00 sec)
mysql [localhost:5729] {msandbox} (test) > select * from test;
+------+------------------+
| a   | n             |
+------+------------------+
|    1 | ���8��;�h�c��          |
+------+------------------+
避免插入失败，也可以将值转换为16进制，然后再进行存储，查看的时候也需要先用 unhex 解析出来，然后再进行解密
mysql [localhost:5729] {msandbox} (test) > insert into test1 values(1,AES_ENCRYPT('test','test'));
ERROR 1366 (HY000): Incorrect string value: '\x87\xBD\x908\x85\x94...' for column 'name' at row 1
mysql [localhost:5729] {msandbox} (test) > insert into test1 values(1,hex(AES_ENCRYPT('test','test')));
Query OK, 1 row affected (0.02 sec)
mysql [localhost:5729] {msandbox} (test) > select AES_DECRYPT(unhex(n),'test') from test1
-> ;
+---------------------------------+
| AES_DECRYPT(unhex(n),'test') |
+---------------------------------+
| test                            |
+---------------------------------+
1 row in set (0.00 sec)
加密方法示例
mysql [localhost:5729] {msandbox} (test) > SET block_encryption_mode = 'aes-256-cbc';
Query OK, 0 rows affected (0.00 sec)
mysql [localhost:5729] {msandbox} (test) > SET @key_str = SHA2('mysql passphrase',512);
Query OK, 0 rows affected (0.00 sec)
mysql [localhost:5729] {msandbox} (test) > SET @init_vector = 'It is very very safe';
Query OK, 0 rows affected (0.00 sec)
mysql [localhost:5729] {msandbox} (test) > SET @crypt_str = AES_ENCRYPT('test',@key_str,@init_vector);
Query OK, 0 rows affected (0.00 sec)
mysql [localhost:5729] {msandbox} (test) > SELECT AES_DECRYPT(@crypt_str,@key_str,@init_vector);
+-----------------------------------------------+
| AES_DECRYPT(@crypt_str,@key_str,@init_vector) |
+-----------------------------------------------+
| test                                          |
+-----------------------------------------------+
1 row in set (0.00 sec)
#### 结语
加密函数为 MySQL 原生的加密手段，可以加密一些类似于身份证、银行卡等隐秘信息。业务中批量使用会造成一定的性能损耗，个人还是建议这些复杂的函数操作还是在应用层实现，降低数据库的压力。