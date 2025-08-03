# MySQL · 源码阅读 · RAND 表达式

**Date:** 2022/06
**Source:** http://mysql.taobao.org/monthly/2022/06/03/
**Images:** 1 images downloaded

---

数据库内核月报

 [
 # 数据库内核月报 － 2022 / 06
 ](/monthly/2022/06)

 * 当期文章

 MySQL · 引擎特性 · PolarDB-CloudJump：优化基于云存储服务的云数据库(发表于VLDB 2022)
* MySQL · 引擎特性 · 通过performance_schema 定量分析系统瓶颈
* MySQL · 源码阅读 · RAND 表达式
* MySQL中的HyperGraph优化器
* MYSQL·分区表特性·一致性哈希算法应用
* PolarDB ·性能大赛·云原生共享内存数据库性能优化

 ## MySQL · 源码阅读 · RAND 表达式 
 Author: 臻成 

 ## 三种形式
RAND 表达式有以下三种形式：

1. RAND(非常量表达式)，此时 RAND 的值仅和表达式的计算值相关，与其所在的位置无关
2. RAND(常量)，每次查询都相同
3. RAND()，每次查询都不相同，这种与通常概念上的随机比较接近

我们通过一些例子来实际看看 RAND 的结果：

### 第一种形式 RAND(非常量表达式)

`create table t1(c1 int, c2 varchar(10)) engine innodb;
insert into t1 values(1, '1');
insert into t1 values(1, '1');
select c1, c2, rand(c1), rand(c2), rand(c1) = rand(c2) from t1;
+------+------+---------------------+---------------------+---------------------+
| c1 | c2 | rand(c1) | rand(c2) | rand(c1) = rand(c2) |
+------+------+---------------------+---------------------+---------------------+
| 1 | 1 | 0.40540353712197724 | 0.40540353712197724 | 1 |
| 1 | 1 | 0.40540353712197724 | 0.40540353712197724 | 1 |
+------+------+---------------------+---------------------+---------------------+
2 rows in set (0.01 sec)
`

可以看到，不同行，不同列，甚至是不同类型的字段，只要其内容一样，RAND 计算的结果就是一样的。

### 第二种形式 RAND(常量)

`select rand(1), rand(1), rand(2), rand('2') from t1;
+---------------------+---------------------+---------------------+---------------------+
| rand(1) | rand(1) | rand(2) | rand('2') |
+---------------------+---------------------+---------------------+---------------------+
| 0.40540353712197724 | 0.40540353712197724 | 0.6555866465490187 | 0.6555866465490187 |
| 0.8716141803857071 | 0.8716141803857071 | 0.12234661925802624 | 0.12234661925802624 |
+---------------------+---------------------+---------------------+---------------------+
select rand(1), rand(1), rand(2), rand('2') from t1;
+---------------------+---------------------+---------------------+---------------------+
| rand(1) | rand(1) | rand(2) | rand('2') |
+---------------------+---------------------+---------------------+---------------------+
| 0.40540353712197724 | 0.40540353712197724 | 0.6555866465490187 | 0.6555866465490187 |
| 0.8716141803857071 | 0.8716141803857071 | 0.12234661925802624 | 0.12234661925802624 |
+---------------------+---------------------+---------------------+---------------------+
`

RAND(常量) 在不同行会有不同的结果，可以生成一个随机数序列，但是只要常量相同，那么生成的序列就是一样的，即使一个查询中出现多次，或者多次查询，结果也保持不变。可以利用这个生成稳定的随机数序列。

### 第三种形式 RAND()

`select rand(), rand() from t1;
+---------------------+---------------------+
| rand() | rand() |
+---------------------+---------------------+
| 0.03644291408028725 | 0.07858704782890813 |
| 0.28360652763732386 | 0.18227152543353992 |
+---------------------+---------------------+
2 rows in set (0.00 sec)

select rand(), rand() from t1;
+----------------------+--------------------+
| rand() | rand() |
+----------------------+--------------------+
| 0.060538074989372935 | 0.75587582937989 |
| 0.597764952664976 | 0.7211973059188549 |
+----------------------+--------------------+
2 rows in set (0.00 sec)
`

不带任何参数的 RAND() 表达式，每次取值看起来都是随机的。每一行，每一个 RAND 表达式都会生成不同的值。可以生成随机数序列。

## MySQL 实现

`void randominit(struct rand_struct *rand_st, ulong seed1,
 ulong seed2) { /* For mysql 3.21.# */
 rand_st->max_value = 0x3FFFFFFFL;
 rand_st->max_value_dbl = (double)rand_st->max_value;
 rand_st->seed1 = seed1 % rand_st->max_value;
 rand_st->seed2 = seed2 % rand_st->max_value;
}

double my_rnd(struct rand_struct *rand_st) {
 rand_st->seed1 = (rand_st->seed1 * 3 + rand_st->seed2) % rand_st->max_value;
 rand_st->seed2 = (rand_st->seed1 + rand_st->seed2 + 33) % rand_st->max_value;
 return (((double)rand_st->seed1) / rand_st->max_value_dbl);
}

void Item_func_rand::seed_random(Item *arg) {
 /*
 TODO: do not do reinit 'rand' for every execute of PS/SP if
 args[0] is a constant.
 */
 uint32 tmp = (uint32)arg->val_int();
 randominit(rand, (uint32)(tmp * 0x10001L + 55555555L),
 (uint32)(tmp * 0x10000001L));
}

double Item_func_rand::val_real() {
 DBUG_ASSERT(fixed == 1);
 if (arg_count) {
 if (!args[0]->const_for_execution())
 seed_random(args[0]);
 else if (first_eval) {
 /*
 Constantness of args[0] may be set during JOIN::optimize(), if arg[0]
 is a field item of "constant" table. Thus, we have to evaluate
 seed_random() for constant arg there but not at the fix_fields method.
 */
 first_eval = false;
 seed_random(args[0]);
 }
 }
 return my_rnd(rand);
}

`

所有相关的代码都在上面了，代码很少，我们还是根据三种形式的不同来分析一下代码

### 第一种形式 RAND(非常量表达式)

`double Item_func_rand::val_real() {
 DBUG_ASSERT(fixed == 1);
 if (arg_count) {
 if (!args[0]->const_for_execution())
 seed_random(args[0]);
 }
 return my_rnd(rand);
}
`

经过分支简化，RAND(非常量表达式) 的代码实际上是这样的，我们可以看到，运算过程中唯一的变量就是 args[0]->val_int()，这个 int 取出来后与各种常数进行运算得到最后的结果。因此只要这个非常量表达式转换成 int 之后的值相同，那么 RAND 表达式的结果也相同。

### 第二种形式 RAND(常量)

`double Item_func_rand::val_real() {
 DBUG_ASSERT(fixed == 1);
 if (arg_count) {
 if (first_eval) {
 first_eval = false;
 seed_random(args[0]);
 }
 }
 return my_rnd(rand);
}
`

经过分支简化，可以看到第一次调用时，会使用常量 args[0] 初始化 rand_struct 中的 seed1 和 seed2，之后，每次调用仅会调用 my_rnd，更新 seed1 和 seed2，并利用 seed1 和 seed2 计算出一个值。因此只要第一个初始的 args[0] 相同，其后生成的随机数序列也相同。

### 第三种形式 RAND()

`double Item_func_rand::val_real() {
 DBUG_ASSERT(fixed == 1);
 return my_rnd(rand);
}
`

没有参数了，每次更新 rand_struct 的 seed1 和 seed2。
而此时的 rand 来自 thd->rand

`bool Item_func_rand::fix_fields(THD *thd, Item **ref) {
 // ...
 if (arg_count) { // Only use argument once in query
 // ...
 } else {
 /*
 Save the seed only the first time RAND() is used in the query
 Once events are forwarded rather than recreated,
 the following can be skipped if inside the slave thread
 */
 if (!thd->rand_used) {
 thd->rand_used = 1;
 thd->rand_saved_seed1 = thd->rand.seed1;
 thd->rand_saved_seed2 = thd->rand.seed2;
 }
 rand = &thd->rand;
 }
 return false;
}
`

thd->rand 在每次查询开始时更新：

`// 实例启动时
randominit(&sql_rand, (ulong)server_start_time, (ulong)server_start_time / 2);

ulong sql_rnd_with_mutex() {
 mysql_mutex_lock(&LOCK_sql_rand);
 ulong tmp =
 (ulong)(my_rnd(&sql_rand) * 0xffffffff); /* make all bits random */
 mysql_mutex_unlock(&LOCK_sql_rand);
 return tmp;
}

void THD::init(void) {
 // ...
 ulong tmp;
 tmp = sql_rnd_with_mutex();
 randominit(&rand, tmp + (ulong)&rand,
 tmp + (ulong)::atomic_global_query_id);
 // ...
}

`

实例在启动时，会根据系统的启动时间初始化一个全局的 rand seed，称为 sql_rand，之后每个查询开始时，调用 my_rnd 更新 sql_rand 并生成一个新的随机数，之后，再使用这个随机数，rand 结构体的地址，global query id 生成当前查询的 rand seed。因此，RAND() 表现出的结果更为随机，但之后的序列生成仍然使用常量进行计算，本质上仍为按规则生成的序列。

## 对并行的影响
PolarDB 在查询加速上做了很多工作，包含 Parallel Query 以及列存加速索引，这些新的实现都利用多核并行获得加速，但在处理 RAND 表达式上，为了实现与 MySQL 行为兼容，需要在某些情况下取消并行执行。我们来分析一下三种形式对并行的影响。

1. RAND(非常量表达式)，此时 RAND 的值仅和表达式的计算值相关，与其所在的位置无关，不存在兼容性问题，可并行执行
2. RAND()，使用随机 seed 生成序列，每次查询都不相同，这种与通常概念上的随机比较接近，应该也是比较常用的形式，因为是随机的，每次执行结果不同，无法复现，因此也不存在兼容性问题，可并行执行
3. RAND(常量)，使用常量作为 seed 生成序列，每次查询都相同，无法并行执行，存在兼容性问题，这种情况为了兼容，往往需要将并行关闭，顺序地获得 RAND 表达式的结果。

## 出现在其他位置
刚才我们的大部分分析都是 RAND 表达式出现在 select list 中的情况，RAND 作为通用的表达式，可以出现在任何使用表达式的地方，例如 order by，group by，roll up 等。我们从之前对实现的分析中可以知道，RAND 返回的结果与求值的顺序有关，因此出现在这些位置时，由于求值顺序与可能与想象中有差异，需要仔细测试确认是否满足需求。

 阅读： - 

[![知识共享许可协议](.img/8232d49bd3e9_88x31.png)](http://creativecommons.org/licenses/by-nc-sa/3.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 3.0 未本地化版本许可协议](http://creativecommons.org/licenses/by-nc-sa/3.0/)进行许可。

 [

 ](#0)