# 新特性解读 | MySQL 8.0.16 组复制新功能：消息碎片化

**原文链接**: https://opensource.actionsky.com/20190521-mysql8-0-mgr/
**分类**: MySQL 新特性
**发布时间**: 2019-05-21T01:29:34-08:00

---

> 标签：Group Communication System, Group Replication, High Availability, XCom
MySQL 8.0.16 已经发布，它像往常一样增强了组复制 Group Replication 功能。
这篇文章介绍了 MySQL 8.0.16 为 Group Replication 带来的新功能：
Message fragmentation（信息碎片化）。
## 背景
Group Replication 目前使用 XCom（一种组通信引擎），特点：原子性，组员状态检测等。每个成员的组复制插件先将信息转发到本地 XCom，再由 XCom 最终以相同的顺序将信息传递给每个组成员的 Group Replication 插件。
XCom 由单线程实现。当一些成员广播信息过大时，XCom 线程必须花费更多的时间来处理那个大信息。如果成员的 XCom 线程忙于处理大信息的时间过长，它可能会去查看其他成员的 XCom 实例。例如，忙碌的成员失效。如果是这样，该组可以从该组中驱逐忙碌的成员。
MySQL 8.0.13 新增  group_replication_member_expel_timeout  系统变量，您可以通过它来调整将成员从组中驱逐的时间。例如，怀疑成员失败，但成员实际上忙于处理大信息，给成员足够的时间来完成处理。在这种情况下，是否为成员增加驱逐超时的设置是一种权衡。有可能等了很久，该成员实际真的失效了。
## Message fragmentation（信息碎片化）
MySQL 8.0.16 的 Group Replication 插件新增用来处理大信息的功能：信息碎片化。
简而言之，您可以为成员的广播信息指定最大值。超过最大值的信息将分段为较小的块传播。
``您可以使用  group_replication_communication_max_message_size  系统变量指定允许的信息最大值（默认值为10 MiB）。
## 示例
让我们用一个例子来解释新功能。图1显示了当绿色成员向组广播信息时，新功能是如何处理的。
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图1.png)											
**图1 对传出信息进行分段**
1. 如果信息大小超过用户允许的最大值（group_replication_communication_max_message_size），则该成员会将信息分段为不超过最大值的块。
2. 该成员将每个块广播到该组，即将每个块单独转发到XCom。
XCom 最终将这些块提供给组成员。下面三张图展示出了中间绿色成员发送大信息时工作的新特征。
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图2a-1024x429.png)											
**图2a 重新组合传入的信息：第一个片段**
3. 成员得出结论，传入的信息实际上是一个更大信息的片段。
4. 成员缓冲传入的片段，因为他们认为片段是仍然不完整的信息的一部分。（片段包含必要的元数据以达到这个结论。）
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图2b.png)											
**图2b 重新组合传入的信息：第二个片段**
5. 见上面的第3步。
6. 见上面的第4步。
![](https://opensource.actionsky.com/wp-content/uploads/2019/05/图2c-1024x429.png)											
**图2c 重新组合传入的信息：最后一个片段**
7. 成员得出结论，传入的信息实际上是一个更大信息的片段。
8. 成员得出结论，传入的片段是最后一个缺失的块，重新组合原始信息，然后对其进行处理，传输完毕。
## 结论
MySQL 8.0.16 已经发布后，组复制现在可以确保组内交换的信息大小不超过用户定义的阈值。这可以防止组内误判而驱逐成员。
> 参考：https://mysqlhighavailability.com/enhanced-support-for-large-transactions-in-group-replication/
欢迎参加 6.15 分布式中间件DBLE用户见面会，在**爱可生总部研发中心**，为你解密技术问题！