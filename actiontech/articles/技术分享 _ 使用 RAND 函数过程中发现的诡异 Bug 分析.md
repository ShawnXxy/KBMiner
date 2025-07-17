# 技术分享 | 使用 RAND() 函数过程中发现的诡异 Bug 分析

**原文链接**: https://opensource.actionsky.com/20200310-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-03-10T01:00:21-08:00

---

作者：Agate Li
爱可生研发团队成员，负责数据库管理平台相关项目，.Net 技术爱好者，长期潜水于技术圈。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**背景**
> MySQL 中的 RAND() 函数是一个随机数发生器，可以返回一个 `>=0` 并 `<1.0` 的随机浮点数。
最近在实际使用过程里遇见了一个主流版本中非常诡异的 Bug，故整理出来，以免大家踩坑。
**演示**
文中使用的 MySQL 版本是 5.7.25，话不多说，直接上演示：
**1. 创建测试表**
- `CREATE TABLE test (`id` INT(3) NOT NULL PRIMARY KEY AUTO_INCREMENT) ENGINE=`InnoDB`;`
**2. 往表里插入 10 条记录**- `INSERT INTO test VALUES(),(),(),(),(),(),(),(),(),();`
**3. 关键来了，执行几次下面这条 SQL**
- `SELECT sub.rnd FROM (SELECT FLOOR(RAND()*10) rnd FROM test) sub WHERE sub.rnd<3;`
明明指定了筛选内层 `sub.rnd` 小于 3 的条件，输出出来的结果却完全不对。
**4. 接下来排查问题的触发条件**
由于直接使用 RAND() 函数输出出来的结果是随机的，首先要做的就是指定一枚固定的种子，一是以免干扰后续排查，二是可以让大家自行精确复现。首先将种子设定为 100，并多次查询内层的随机数
可以看到，符合预期。继续：
仍然符合预期，看起来不像是 RAND() 函数本身的问题。
**5. 为第三步中的 SQL 指定种子：**
- `SELECT sub.rnd FROM (SELECT FLOOR(RAND(100)*10) rnd FROM test) sub WHERE sub.rnd<3;`
熟悉的味道出现了，刺激的感觉回来了…… EXPLAIN 一波
**6. 去掉第三步中的 test 表再试**
- `SELECT sub.rnd FROM (SELECT FLOOR(RAND(100)*10) rnd) sub WHERE sub.rnd<3;`
哈？并没有问题？再 EXPLAIN 一波
到这里就有了个怀疑，是不是跟派生表物化相关？
**7. 再改改第三步中的 SQL**
- `SELECT sub.rnd FROM (SELECT FLOOR(RAND(100)*10) rnd FROM test LIMIT 10000) sub WHERE sub.rnd<3;`
再再 EXPLAIN 一波
嗯，不出所料呢。这回结果对了。
**8. 再验证一次，把第三步中的 SQL 拉平**
- `SELECT FLOOR(RAND(100)*10) rnd FROM test HAVING rnd<3;`
再再再 EXPLAIN 一波
没错，还是熟悉的味道，还是刺激的感觉。
**9. 这时候可以推测，大概率是在派生表未物化的情况下 RAND() 在外层重算了……**
拿着推测，去 google 一波，立刻找到了一个相关 Bug：> https://bugs.mysql.com/bug.php?id=86624
嗯，2017 年年中就有人报过的 Bug，再看看 Bug 状态，噢，“嘻嘻，我们验证了但不打算修”……
**好在官方还是给出了解决方法：**
- 对于5.7，跟我们的做法一样，加上 LIMIT <一个很大的数>；
- 对于8.0，加上 no_merge。
文末例行完结撒花。