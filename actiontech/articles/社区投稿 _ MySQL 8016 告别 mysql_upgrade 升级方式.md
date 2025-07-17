# 社区投稿 | MySQL 8.0.16 告别 mysql_upgrade 升级方式

**原文链接**: https://opensource.actionsky.com/20190507-mysql8-0-upgrade/
**分类**: MySQL 新特性
**发布时间**: 2019-05-07T18:06:06-08:00

---

最熟悉的命令要消失了！
MySQL 8.0.16 开始，MySQL 不推荐使用mysql_upgrade。取而代之的是server upgrade的升级方式。
### 一、为什么变更升级方式？
**官方为什么这么做？**
1.升级速度更快
2.升级更简单
3.安全性更好
4.减少升级步骤，方便自动化
5.不需要重启 MySQL
6.即插即用
### 二、新旧方式升级流程对比
**在 MySQL 8.0.16 之前：**
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/之前-300x153.png)
1.关闭 MySQL，替换新的二进制 MySQL
2.启动 MySQL，让服务器升级 DD（数据字典）表
3.运行 mysql_upgrade，更新系统表和用户表
4.加载新的帮助表
5.重启 MySQL
**从MySQL8.0.16开始：**
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/开始-300x171.png)
1.关闭 MySQL，替换新的二进制 MySQL
2.启动 MySQL，升级 DD（数据字典）表和系统表、用户表和帮助表
升级的时间和操作都会大幅度缩短，操作步骤也减少了很多，更方便了用户。
### 三、关于 MySQL 8.0.16 的新的升级方式
**那么看看该如何使用新的升级姿势吧。**
在 mysqld 额外添加了一个新的选项 &#8211;upgrade。可选值为 NONE，AUTO，MINIMAL，FORCE。
姿势是这样的：/usr/local/mysql/bin/mysqld&#8211;upgrade=NONE
&#8211; 新的选项代表什么？
**NONE：**不尝试进行升级。
**AUTO：**默认选项，MySQL 进行数据字典升级和服务升级
**MINIMAL：**仅升级数据字典
**FORCE：**强制升级，类似旧的 mysql  &#8211;upgrade –force
**MySQL 8.0.16 新的升级方式，总体来说分为2个步骤。**
1.升级数据字典（DD）
2.服务器升级：升级 MySQL 系统表、升级用户表、升级 sys 表、升级帮助更新表
**可能出现的问题：**
1.升级数据字典：原子性操作。如果操作失败。则根据目录可以回滚回来
2.升级系统表、用户表：可以从备份还原中恢复
> 
**个人建议，针对升级：**
1.使用新的版本，尤其是 MySQL 8.0 系列。每个版本都有新特性，还有bug的修复，定期小版本升级会使你的 MySQL 更加稳定。
2.阅读新版本的Release。
3.最后，升级之前要做好备份，以便升级失败回滚使用。
**开源分布式中间件DBLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dble
技术交流群：669663113
**开源数据传输中间件DTLE**
社区官网：https://opensource.actionsky.com/
GitHub主页：https://github.com/actiontech/dtle
技术交流群：852990221
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/默认标题_宣传单_2019.05.06-1-223x300.jpg)