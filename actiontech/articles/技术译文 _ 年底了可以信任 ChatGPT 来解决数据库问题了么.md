# 技术译文 | 年底了，可以信任 ChatGPT 来解决数据库问题了么？

**原文链接**: https://opensource.actionsky.com/%e6%8a%80%e6%9c%af%e8%af%91%e6%96%87-%e5%b9%b4%e5%ba%95%e4%ba%86%ef%bc%8c%e5%8f%af%e4%bb%a5%e4%bf%a1%e4%bb%bb-chatgpt-%e6%9d%a5%e8%a7%a3%e5%86%b3%e6%95%b0%e6%8d%ae%e5%ba%93%e9%97%ae%e9%a2%98/
**分类**: 技术干货
**发布时间**: 2023-12-25T19:16:36-08:00

---

2023 年会被称为生成式人工智能（GAI）之年吗？我不知道，但可以肯定的是，ChatGPT 从 2022 底开始引发了很多行业围绕该技术的巨大变革。确实是有趣的时刻，我们目睹了一些改变我们世界的事情。
> 
作者：Przemysław Malkowski
本文来源：[https://www.percona.com/，封面由](https://www.percona.com/，封面由) DELL-3 生成，爱可生开源社区翻译。
本文约 3400 字，预计阅读需要 8 分钟。
我在二月份玩了一下 ChatGPT，看看它如何响应与数据库相关的问题，发现它令人印象深刻，同时也很烦人。我不喜欢它的是，如果没有足够的数据，它就会编造“事实”。我多次成功地发现它在撒谎，在我证明它是错误之后，机器人道歉了，后来在不同的话题上再次做了类似的虚构的事情。我决定在临近十二月时再检查一下。
在我写这篇文章的时候，有很多地方可以与人工智能聊天，但据我所知，目前只有 **Google 的 Bard、微软的 Bing Chat 和 OpenAI 的 ChatGPT** 比较容易访问，以下我只对 **MongoDB 和 MySQL** 这两种技术进行测试和评论。
# Google Bard
这是我对 Bard 的第一次测试，我对 Bard 抱有很高的期望，因为它可以访问线上的数据信息，而不是那个在有限的数据上运行的 ChatGPT。然而，它从一开始就以其可笑的答案让我震惊！我从一个有点棘手的问题开始，但答案绝对是搞笑的！
*我：为什么 MongoDB 7.0 版本现在降级更加容易？*
*Bard：*
由于 MongoDB 7.0 中引入了多项关键改进，从 MongoDB 版本 7.0 降级到任何以前的版本现在比以前的版本要容易得多。以下是 MongoDB 7.0 中降级变得更加简单的主要原因：
- 简化的降级工作流程：MongoDB 7.0 引入了简化的降级工作流程，无需在降级之前手动备份数据并重新启动复制。这种简化的流程降低了错误风险并简化了降级程序。
- 增强的降级兼容性：MongoDB 7.0 通过引入使降级数据库更容易与旧版 MongoDB 版本互操作的更改，显着增强了降级兼容性。这意味着降级的数据库更有可能在旧版本中正常运行，从而减少了降级后大量数据清理或架构调整的需要。
- 改进的数据完整性检查：MongoDB 7.0 在降级过程中实施了改进的数据完整性检查。这些检查有助于识别和防止降级期间可能出现的潜在数据损坏问题，确保降级数据的完整性。
- 增强的回滚机制： MongoDB 7.0 完善了回滚机制，使其在处理降级过程时更加高效可靠。这种增强的回滚功能可确保降级期间遇到的任何问题都能得到及时解决，而不会影响数据完整性。
- 简化的降级命令： MongoDB 7.0 引入了简化的降级命令，它提供了单个命令来启动降级过程。此命令消除了对多个命令和手动步骤的需要，使降级过程更加用户友好。
综上所述，MongoDB 7.0 中的降级过程得到了显着简化和增强，使得从 MongoDB 7.0 降级到以前的版本变得更加容易和可靠。简化的工作流程、改进的兼容性、增强的检查、高效的回滚机制和简化的命令有助于提供更直接且降低风险的降级体验。
显然，我不喜欢这个答案。看来 Bard 被我提供的错误提问所误导，并试图用我期望收到的答案来取悦我。**该答复与事实完全不符！从 MongoDB 7.0 版本开始，不再支持二进制降级，并且降级的复杂度大大提高。**让我们继续挖掘这个问题。
*我：好的，那么如果我想将 MongoDB 独立服务器从版本 7.0 降级到 6.0，我应该使用哪些命令？*
*Brad：*
将 MongoDB 独立服务器从 7.0 降级到 6.0。
先决条件：
- 备份 MongoDB 数据库：在继续降级之前，强烈建议创建 MongoDB 数据库的备份，以确保降级期间出现任何问题时数据的完整性。
- 访问控制：如果您的部署启用了访问控制，请确保执行降级的用户具有降级数据库所需的权限。具有该角色的用户 root 具有所需的权限。
降级程序：
- 下载 MongoDB 6.0 二进制文件：从 MongoDB 下载中心下载 MongoDB 6.0 的最新补丁版本，或使用系统的包管理器安装 6.0 二进制文件。
- 停止 MongoDB 7.0 服务器：mongod使用带有 标志的命令停止 MongoDB 7.0 服务器-shutdown。例如，在 Linux 或 macOS 上，使用：`mongod -shutdown`。
- 将 MongoDB 7.0 二进制文件替换为 6.0 二进制文件：将系统 bin 目录中现有的 MongoDB 7.0 二进制文件替换为下载的 6.0 二进制文件。
- 降级功能兼容性版本 (fCV)：使用 Shell *mongosh* 连接到 MongoDB 6.0 服务器，并使用以下命令将 featureCompatibilityVersion 降级到“5.0”：
`mongosh -u root <database_name> 
db.adminCommand( { setFeatureCompatibilityVersion: "5.0" } )
`
- 启动 MongoDB 6.0 服务器： 使用命令启动 MongoDB 6.0 服务器 mongod 。例如，在 Linux 或 macOS 上，使用：`mongod -f <path_to_mongodb_6.0_config_file>`。
- 验证降级： 验证 MongoDB 服务器正在运行并且可以使用 Shell `mongosh` 访问降级的数据库。
重要考虑因素：
- 降级是不可逆的。一旦降级，您将无法轻松恢复到以前的 MongoDB 版本。
- 降级可能需要数据清理或架构调整以解决兼容性问题。
- 与之前的 MongoDB 版本相比，降级可能会带来性能或兼容性限制。
- 始终建议在将降级数据库用于生产用途之前对其进行彻底测试。
好的，是时候对回复提出质疑了。
*我：手册中说“从 MongoDB 7.0 开始，MongoDB 社区版不再支持二进制降级。”，是否与您的建议相矛盾？*
*Bard：*
是的，你是对的。从 MongoDB 7.0 开始，MongoDB Community Edition 不再支持二进制降级。这意味着您不能简单地将 MongoDB 7.0 二进制文件替换为 MongoDB 6.0 二进制文件并期望数据库正常运行。
如果您需要将 MongoDB 独立服务器从版本 7.0 降级到 6.0，您需要联系 MongoDB 支持寻求帮助。他们将为您提供必要的步骤，以安全且受支持的方式降级您的数据库。
对于我之前的指示中的错误，我深表歉意。我仍在发展中，我一直在学习新事物。今后我会更加小心地提供准确和最新的信息。
好的，那么我们来看看 MySQL 类似的问题。
*我：如果升级不成功，如何将 MySQL 版本 8.0.35 降级回 5.7.44？*
*Brad：*
将 MySQL 从版本 8.0.35 降级到 5.7.44 涉及两个步骤：
**步骤 1：卸载 MySQL 8.0.35**
- 停止 MySQL 服务： 继续之前，请确保 MySQL 服务已停止，以避免卸载过程中出现任何冲突。对于 Windows 使用以下命令，对于 Linux 发行版使用等效命令：`net stop mysql`。
- 删除 MySQL 二进制文件： 使用适合您操作系统的方法从系统中卸载 MySQL 8.0.35 二进制文件。对于 Windows，请使用该 `msiexec` 命令，而对于 Linux，请使用包管理器的卸载选项。
`msiexec /uninstall MySQL Community Server 8.0.35
`
- 删除 MySQL 数据和配置： 导航到 MySQL 安装目录并删除数据目录（通常 `/data`）和配置文件（`my.ini`）。
```
rm -rf /opt/mysql/data/ 
rm /etc/my.cnf
```
**步骤 2：安装 MySQL 5.7.44**
- 下载 MySQL 5.7.44：从官方 MySQL 下载页面下载适合您的操作系统的 MySQL 5.7.44 安装程序。
- 安装 MySQL 5.7.44：运行 MySQL 5.7.44 安装程序并按照屏幕上的说明完成安装过程。确保使用适合您环境的设置来配置 MySQL 服务器。
- 创建数据库备份：安装完成后，创建 MySQL 数据库的备份，以确保降级过程中出现任何问题时数据的完整性。
- 降级MySQL服务器：使用命令行客户端连接MySQL 5.7.44服务器，使用以下命令降级服务器版本：
`ALTER SYSTEM SET version=5.7.44;
`
- 重新启动 MySQL 服务器： 重新启动 MySQL 服务器以应用降级更改并确保服务器以降级版本运行。
```
service mysql start
```
- 恢复数据库备份：恢复您在步骤 3 中创建的数据库备份，使数据恢复到升级前的状态。
- 验证降级：验证 MySQL 服务器是否正在运行版本 5.7.44，以及您的数据库是否可访问且功能正常。
好吧，我简直不敢相信自己的眼睛，Bard 现在的状态真的这么差吗？你是否注意到第三个建议步骤是在 **尚未进行备份的情况下删除数据？**不仅这个回复总体上是错误和危险的，而且在小细节上也有很多错误 —— 混合了 Windows 和 Linux 命令、错误的顺序、尴尬的 ALTER 查询、执行和恢复空备份等。
我玩的 Bard 版本是 Bard-17.3.38。
# Bing Chat
我们可以快速测试的另一个替代方案是 Bing Chat，它可以与 Bard 相媲美，可以在线访问互联网。它使用了 GPT-4 引擎，就像最新的 ChatGPT Plus（付费）选项一样。我用类似的问题向它发起挑战。
*我：你好 Bing，如果我的升级不成功，你能帮我将 MySQL 版本 8.0.35 降级回 5.7.44 吗？*
*Bing：*
得知您升级失败，我们深表遗憾。根据 MySQL 官方文档，**不支持** 从 MySQL 8.0 降级到 MySQL 5.7 或从 MySQL 8.0 版本降级到之前的 MySQL 8.0 版本。唯一受支持的替代方案是恢复升级之前进行的备份。因此，在开始升级过程之前必须备份数据。
如果您有数据备份，可以将其恢复到 MySQL 5.7 实例。如果您没有备份，您可以尝试从 MySQL 8.0 导出数据并将其导入 MySQL 5.7 实例。然而，这个过程可能并不简单，并且可能需要一些手动干预。
我希望这有帮助。如果您还有其他问题，请告诉我..
资料来源：与 Bing 对话，2023 年 12 月 8 日
- 《MySQL 8.0 参考手册：2.11 MySQL 降级》[https://dev.mysql.com/doc/refman/8.0/en/downgrading.html。](https://dev.mysql.com/doc/refman/8.0/en/downgrading.html。)
- 《如何将 MySQL 从 8.0.33 降级到 8.0.28》[https://dba.stackexchange.com/questions/326263/how-to-downgrade-mysql-from-8-0-33-to-8-0-28。](https://dba.stackexchange.com/questions/326263/how-to-downgrade-mysql-from-8-0-33-to-8-0-28。)
- 《MySQL 8.0 发行说明》[https://dev.mysql.com/doc/relnotes/mysql/8.0/en/。](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/。)
- 《MySQL 主要版本从 5.7 升级到 8.0.30》[https://dbsguru.com/mysql-major-version-upgrade-from-5-7-to-8-0-30/。](https://dbsguru.com/mysql-major-version-upgrade-from-5-7-to-8-0-30/。)
- 《MySQL 5.7.44 的变更》[https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-44.html。](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-44.html。)
……
哇，真是一个惊喜！该建议非常准确，并且包含参考链接。估计 MongoDB 棘手的问题也处理得很好。
*我：为什么 MongoDB 7.0 版本现在降级更加容易？*
*BIng：*
对不起，但我必须纠正你。根据 MongoDB 官方文档，**不支持从 MongoDB 7.0 降级到早期版本**。但是，文档确实提到 MongoDB 7.0 包含 MongoDB Rapid Releases 6.1、6.2 和 6.3 中引入的更改，这些更改可能会影响与旧版本 MongoDB 的兼容性。要了解有关主要版本和快速版本之间差异的更多信息，请参阅 MongoDB 版本控制。
如果您正在寻找有关如何从 MongoDB 7.0 降级到 MongoDB 6.0 的信息，可以参考 MongoDB 官方文档。该文档指出，要从 MongoDB 7.0 降级到早期版本，您必须删除使用以下任何功能的数据：带有范围索引的、带有 cryptoFields 的集合、需要 fCV 7.0 或更高版本的复合通配符索引，以及需要 fCV 7.0 或更高版本的 7.0 之前的 mongod。如果您使用一个或多个复合通配符索引，则不会启动。
我希望这有帮助。如果您还有其他问题，请告诉我。
资料来源：与 Bing 对话，2023 年 12 月 8 日
- 《MongoDB 7.0 中的兼容性变更 — MongoDB 手册》[https://www.mongodb.com/docs/v7.0/release-notes/7.0-compatibility/。](https://www.mongodb.com/docs/v7.0/release-notes/7.0-compatibility/。)
- 《MongoDB 7.0 中的兼容性变更 — MongoDB 手册》[https://www.mongodb.com/docs/upcoming/release-notes/7.0-compatibility/。](https://www.mongodb.com/docs/upcoming/release-notes/7.0-compatibility/。)
- 《将单机升级到 6.0——MongoDB 手册》[https://www.mongodb.com/docs/manual/release-notes/6.0-upgrade-standalone/。](https://www.mongodb.com/docs/manual/release-notes/6.0-upgrade-standalone/。)
……
同样，回复与 Bard 的完全不同，而且质量更好。
我还检查了离线的 ChatGPT 3.5，据我观察，当它没有数据时，就不再制造错误答案了。至少在我的几次测试中是这样。
# ChatGPT
> 
截至 2022 年 1 月的最后一次知识更新，我没有有关 Percona XtraBackup 版本 8.0.33 中的更改或改进的具体信息，因为它是更新的版本。 
请注意，当询问完全相同的问题时，您预计会收到不同的答案。
# 总结
生成式 AI、大语言模型在最近一年左右经历了非常快速的发展。看来在实际业务中实施这项新技术的压力很大，而且这种情况已经发生了。然而，其中存在很多潜在的问题和风险。我认为谨慎对待这个新机会并努力验证一切非常重要。