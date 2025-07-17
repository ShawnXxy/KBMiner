# 02 期 | BEGIN 语句会马上启动事务吗？

**原文链接**: https://opensource.actionsky.com/%e7%ac%ac-02-%e6%9c%9f-%e4%ba%8b%e5%8a%a1-begin-%e8%af%ad%e5%8f%a5%e4%bc%9a%e9%a9%ac%e4%b8%8a%e5%90%af%e5%8a%a8%e4%ba%8b%e5%8a%a1%e5%90%97%ef%bc%9f/
**分类**: 技术干货
**发布时间**: 2024-01-09T21:50:09-08:00

---

聊聊最常用也是最简单的 BEGIN 语句，开始一个事务的过程中都干了什么。
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
# BEGIN 语句会马上启动事务吗？
> 本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
 
**正文**
## 1. BEGIN 语句的七十二变
我们查看官方文档中开始一个事务的语法，会发现还挺复杂：
`START TRANSACTION
[transaction_characteristic [, transaction_characteristic] ...]
transaction_characteristic: {
WITH CONSISTENT SNAPSHOT
| READ WRITE
| READ ONLY
}
BEGIN [WORK]
`
上面眼花缭乱的语法，按照各种组合展开之后，可以得到这些 SQL 语句：
`/*  1 */ BEGIN
/*  2 */ BEGIN WORK
/*  3 */ START TRANSACTION
/*  4 */ START TRANSACTION READ WRITE
/*  5 */ START TRANSACTION READ ONLY
/*  6 */ START TRANSACTION WITH CONSISTENT SNAPSHOT
/*  7 */ START TRANSACTION WITH CONSISTENT SNAPSHOT, READ WRITE
/*  8 */ START TRANSACTION WITH CONSISTENT SNAPSHOT, READ ONLY
/*  9 */ START TRANSACTION WITH CONSISTENT SNAPSHOT, READ WRITE, READ ONLY
/* 10 */ START TRANSACTION READ WRITE, READ ONLY
`
其中，语句 1 ~ 8 都能正常执行，语句 9、10 会报语法错误：
`(1064, 
"You have an error in your SQL syntax;
check the manual that corresponds
to your MySQL server version 
for the right syntax to use 
near '' at line 1")
`
语句 9、10 报语法错误，并不是因为 MySQL 不能识别这两种语法，而是识别语法之后进行判断给出的错误提示：
`start:
START_SYM TRANSACTION_SYM opt_start_transaction_option_list
{
LEX *lex= Lex;
lex->sql_command= SQLCOM_BEGIN;
/* READ ONLY and READ WRITE are mutually exclusive. */
if (($3 & MYSQL_START_TRANS_OPT_READ_WRITE) &&
($3 & MYSQL_START_TRANS_OPT_READ_ONLY))
{
YYTHD->syntax_error();
MYSQL_YYABORT;
}
lex->start_transaction_opt= $3;
}
;
`
上面是解析 START TRANSACTION 的部分逻辑，通过以上逻辑可以看到，当 START TRANSACTION 同时包含以下两项时：
- MYSQL_START_TRANS_OPT_READ_WRITE
- MYSQL_START_TRANS_OPT_READ_ONLY
MySQL 会通过 YYTHD->syntax_error() 主动抛出一个语法错误，告诉我们不支持这样的语法。
在可以正常执行的语句 1 ~ 8 中：
- 语句 1 ~ 4：用于开始一个新的读写事务。
语句 5：用于开始一个新的只读事务。
这两类语句都不需立即创建一致性读视图，事务的启动将延迟至实际需要时。
- 语句 6 ~ 7：用于开始一个新的读写事务。
语句 8：用于开始一个新的只读事务。
这两类语句都会先启动事务，随后立即创建一致性读视图。
如果要投票选出我们最常用于开始一个事务的语句，大概非 BEGIN 莫属了。
接下来，我们就用 BEGIN 作为语句 1 ~ 5 的代表，来聊聊开始一个新事务的过程中，MySQL 做的那些事。
## 2. BEGIN 语句都干什么了？
如果用一个词语描述 BEGIN 语句要做的事，那就是辞旧迎新，展开来说，BEGIN 语句**主要**做两件事：
- 辞旧：提交老事务。
- 迎新：准备新事务。
### 2.1 提交老事务
我们先来看一个场景：
在 MySQL 客户端命令行（`mysql`）中，我们通过 BEGIN 语句开始了一个事务（`事务 1`），并且已经执行了一条 INSERT 语句。
事务 1 还没有提交（即处于活跃状态），我们在同一个连接中又执行了 BEGIN 语句，事务 1 会发生什么？
答案是：事务 1 会被提交。
原因是： MySQL 不支持嵌套事务。事务 1 没有提交的情况下，又要开始一个新事务，事务 1 将无处安放，只能被动提交了。
回到本小节主题，我们来看看 BEGIN 语句提交老事务的流程。
首先，BEGIN 语句会判断当前连接中**是否有可能**存在未提交事务，判断逻辑为：当前连接的线程是否被打上了 `OPTION_NOT_AUTOCOMMIT` 或 `OPTION_BEGIN` 标志位（如下代码所示）。
`if (thd->in_multi_stmt_transaction_mode() || ...) {
...
}
inline bool in_multi_stmt_transaction_mode() const {
return variables.option_bits & 
(OPTION_NOT_AUTOCOMMIT | OPTION_BEGIN);
}
`
只要 `variables.option_bits` 包含其中一个标志位，就说明当前连接中**可能**存在未提交事务。
BEGIN 语句想要开始一个新事务，就必须先执行一次提交操作，把可能未提交的事务给提交了（如下代码所示）。
`if (thd->in_multi_stmt_transaction_mode() || ...) {
...
res = ha_commit_trans(thd, true);
}
`
如果 `variables.option_bits` 没有包含两个标志位中的任何一个，说明当前连接中没有未提交事务，可以直接开始一个新事务。
### 2.2 准备新事务
辞旧完事，就该迎新了。
由于 MySQL 一向秉持不铺张浪费的原则，对于资源，能少分配就少分配、能晚分配就晚分配。
启动事务也需要分配资源，遵循不铺张浪费的原则，BEGIN 语句执行过程中，并不会马上启动一个新事务，只会为新事务做一点点准备工作。
这个一点点真的是一点点，你看：
`thd->variables.option_bits |= OPTION_BEGIN;
`
上面的准备工作就是给当前连接的线程打上 `OPTION_BEGIN` 标志。
有了 `OPTION_BEGIN` 标志，MySQL 就不会每次执行完一条 SQL 语句就提交事务，而是需要用户发起 commit 语句才提交事务，这样的事务就可以执行多条 SQL 了。
## 3. 总结
一句话总结：BEGIN 语句执行过程中，要做的事情就是辞旧（提交老事务）迎新（准备新事务），并不会马上启动一个新事务。
> **本期问题**：对于 START TRANSACTION 同时指定 READ WRITE、READ ONLY，除了报错，你还有别的思路解决这个问题吗？欢迎大家留言交流。
**下期预告**：我是一个事务，请给我一个对象。