# 新特性解读 | MySQL 8.0.16 组复制通讯协议的设置

**原文链接**: https://opensource.actionsky.com/20190522-mysql8-0-mgr/
**分类**: MySQL 新特性
**发布时间**: 2019-05-22T22:01:24-08:00

---

**标签：Group Communication System, Group Replication, High Availability
## 背景
在之前的文章中，我们介绍了 MySQL Group Replication 8.0.16 支持信息碎片化功能来增强大型事务处理能力。
如果您想在组复制中使用该功能，则任何组成员的版本都不能低于 8.0.16！**
简单地说就是由于低版本协议上不支持。MySQL 8.0.16 的组通讯开始支持新协议，简称**“分段协议”**，之前的版本中只有一种**“压缩协议”**。
**
如果多个成员想加入复制组，那么在协议匹配上遵循以下原则：
1、现有复制组成员和新加入成员版本相同，加入成功。
2、低版本成员想加入高版本的组会被驱逐，加入失败。
3、高版本的成员想加入低版本的组，单独加入成功，多个加入失败。
例如：
- 一个 MySQL Server 8.0.16 实例可以成功加入使用通信协议版本 5.7.24 的组。
- 一个 MySQL Server 5.7.24 实例无法成功加入使用通信协议版本 8.0.16 的组。
- 两个 MySQL Server 8.0.16 实例无法同时加入使用通信协议版本 5.7.24 的组。
- 两个 MySQL Server 8.0.16 实例可以同时加入使用通信协议版本 8.0.16 的组。
## 新增 UDF
为了能让高版本的复制组更便于加入低版本的成员，MySQL 8.0.16 新增两个 UDF。
您可以使用两个新的 UDF 命令去管理组通信协议：
1、group_replication_set_communication_protocol(new_protocol)**
设置组复制通讯协议版本
SELECT group_replication_set_communication_protocol("8.0.15");
填入一个所有成员都支持的版本号，即：**new_protocol ≤ 所有成员的  MySQL版本**。 
new_protocol 格式：major.minor.patch （主版本号.次版本号.发布版本号）例如：**8.0.15**。
**2、group_replication_get_communication_protocol()**
获取复制中最旧成员的 MySQL 版本号
SELECT group_replication_get_communication_protocol();**	+------------------------------------------------+
| group_replication_get_communication_protocol() |
+------------------------------------------------+
| 5.7.14                                         |
+------------------------------------------------+
获取的版本号可能与设置的值不一致，但不一致的版本之间组复制协议是一样的。
返回结果格式：major.minor.patch （主版本号.次版本号.发布版本号）例如：8.0.15**。
**以上两个 UDF 对全部组成员有效，主机或从机上均可执行。**
## 结尾
若想使用信息碎片功能。建议将组复制成员全部升级为 8.0.16。
若组内成员版本仅有部分为 8.0.16 ，可以用两个新的函数来让高版本的成员保持与其它成员组协议一致。
> 参考：
组复制协议：
[https://dev.mysql.com/doc/refman/8.0/en/group-replication-communication-protocol.html](https://dev.mysql.com/doc/refman/8.0/en/group-replication-communication-protocol.html)
相关博文：
[https://mysqlhighavailability.com/configuring-the-communication-protocol-in-group-replication/](https://mysqlhighavailability.com/configuring-the-communication-protocol-in-group-replication/)
欢迎参加 6.15 分布式中间件DBLE用户见面会，在**爱可生总部研发中心**，为你解密技术问题！