# 新特性解读 | MySQL 8.0 正则替换

**原文链接**: https://opensource.actionsky.com/20190724-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-07-24T01:44:38-08:00

---

MySQL 一直以来都支持正则匹配，不过对于正则替换则一直到MySQL 8.0 才支持。对于这类场景，以前要么在MySQL端处理，要么把数据拿出来在应用端处理。
比如我想把表y1的列str1的出现第3个action的子 串替换成dble，怎么实现？
**1. 自己写SQL层的存储函数。****代码如下写死了3个，没有优化，仅仅作为演示，MySQL 里非常不建议写这样的函数。**
- `   mysql`
- `   DELIMITER $$`
- `   USE `ytt`$$`
- `   DROP FUNCTION IF EXISTS `func_instr_simple_ytt`$$`
- `   CREATE DEFINER=`root`@`localhost` FUNCTION `func_instr_simple_ytt`(`
- `       f_str VARCHAR(1000), -- Parameter 1`
- `       f_substr VARCHAR(100),  -- Parameter 2`
- `       f_replace_str varchar(100),`
- `       f_times int -- times counter.only support  3.`
- `       ) RETURNS varchar(1000)`
- `   BEGIN`
- `     declare v_result varchar(1000) default 'ytt'; -- result.`
- `     declare v_substr_len int default 0; -- search string length.`
- 
- `     set f_times = 3; -- only support  3.`
- `     set v_substr_len = length(f_substr);`
- `     select instr(f_str,f_substr) into @p1; -- First real position .`
- `     select instr(substr(f_str,@p1+v_substr_len),f_substr) into @p2; Secondary virtual position.`
- `     select instr(substr(f_str,@p2+ @p1 +2*v_substr_len - 1),f_substr) into @p3; -- Third virtual position.`
- `     if @p1 > 0  && @p2 > 0 && @p3 > 0 then -- Fine.`
- `         select`
- `        concat(substr(f_str,1,@p1 + @p2 + @p3 + (f_times - 1) * v_substr_len  - f_times)`
- `        ,f_replace_str,`
- `        substr(f_str,@p1 + @p2 + @p3 + f_times * v_substr_len-2)) into v_result;`
- `     else`
- `       set v_result = f_str; -- Never changed.`
- `     end if;`
- `     -- Purge all session variables.`
- `     set @p1 = null;`
- `     set @p2 = null;`
- `     set @p3 = null;`
- `     return v_result;`
- 
- `   end;`
- `   $$`
- `   DELIMITER ;`
- 
- `   -- 调用函数来更新：`
- `   mysql> update y1 set str1 = func_instr_simple_ytt(str1,'action','dble',3);`
- `   Query OK, 20 rows affected (0.12 sec)`
- `   Rows matched: 20  Changed: 20  Warnings: 0`
**2. 导出来用sed之类的工具替换掉在导入，步骤如下：（推荐使用）**
1）导出表y1的记录。
- `mysql`
- `mysql> select * from y1 into outfile '/var/lib/mysql-files/y1.csv';`
- `Query OK, 20 rows affected (0.00 sec)`
2）用sed替换导出来的数据。
- `shell`
- `root@ytt-Aspire-V5-471G:/var/lib/mysql-files#  sed -i 's/action/dble/3' y1.csv`
3）再次导入处理好的数据，完成。
- `mysql`
- `mysql> truncate y1;`
- `Query OK, 0 rows affected (0.99 sec)`
- 
- `mysql> load data infile '/var/lib/mysql-files/y1.csv' into table y1;`
- `Query OK, 20 rows affected (0.14 sec)`
- `Records: 20  Deleted: 0  Skipped: 0  Warnings: 0`
以上两种还是推荐导出来处理好了再重新导入，性能来的高些，而且还不用自己费劲写函数代码。
那MySQL 8.0 对于以上的场景实现就非常简单了，一个函数就搞定了。
- `mysql`
- `mysql> update y1 set str1 = regexp_replace(str1,'action','dble',1,3) ;`
- `Query OK, 20 rows affected (0.13 sec)`
- `Rows matched: 20  Changed: 20  Warnings: 0`
还有一个regexp_instr 也非常有用，特别是这种特指出现第几次的场景。比如定义 SESSION 变量@a。
- `mysql`
- `mysql> set @a = 'aa bb cc ee fi lucy  1 1 1 b s 2 3 4 5 2 3 5 561 19 10 10 20 30 10 40';`
- `Query OK, 0 rows affected (0.04 sec)`
拿到至少两次的数字出现的第二次子串的位置。
- `mysql`
- `mysql> select regexp_instr(@a,'[:digit:]{2,}',1,2);`
- `+--------------------------------------+`
- `| regexp_instr(@a,'[:digit:]{2,}',1,2) |`
- `+--------------------------------------+`
- `|                                   50 |`
- `+--------------------------------------+`
- `1 row in set (0.00 sec)`
那我们在看看对多字节字符支持如何。
- `mysql`
- `mysql> set @a = '中国 美国 俄罗斯 日本 中国 北京 上海 深圳 广州 北京 上海 武汉 东莞 北京 青岛 北京';`
- `Query OK, 0 rows affected (0.00 sec)`
- 
- `mysql> select regexp_instr(@a,'北京',1,1);`
- `+-------------------------------+`
- `| regexp_instr(@a,'北京',1,1)   |`
- `+-------------------------------+`
- `|                            17 |`
- `+-------------------------------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> select regexp_instr(@a,'北京',1,2);`
- `+-------------------------------+`
- `| regexp_instr(@a,'北京',1,2)   |`
- `+-------------------------------+`
- `|                            29 |`
- `+-------------------------------+`
- `1 row in set (0.00 sec)`
- 
- `mysql> select regexp_instr(@a,'北京',1,3);`
- `+-------------------------------+`
- `| regexp_instr(@a,'北京',1,3)   |`
- `+-------------------------------+`
- `|                            41 |`
- `+-------------------------------+`
- `1 row in set (0.00 sec)`
那总结下，
这里我提到了 MySQL 8.0 的两个最有用的正则匹配函数 regexp_replace 和 regexp_instr。针对以前类似的场景算是有一个完美的解决方案。
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)