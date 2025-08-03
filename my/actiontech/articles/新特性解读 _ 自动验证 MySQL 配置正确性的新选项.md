# 新特性解读 | 自动验证 MySQL 配置正确性的新选项

**原文链接**: https://opensource.actionsky.com/20190626-mysql8-autocheck/
**分类**: MySQL 新特性
**发布时间**: 2019-06-26T20:54:25-08:00

---

## 新特性解读 | 自动验证 MySQL 配置正确性的新选项
原文标题：How to validate server configuration settings.
作者：Nisha Gopalakrishnan
翻译：管长龙
标签：Configuration，How To，MySQL，Upgrades
升级 MySQL 版本之后，许多用户在启动时并未更改配置文件，但发现新的的版本不再支持某些已弃用的选项，这会导致升级的 MySQL 服务关闭。在其他情况下，修改配置文件时错误输入无效的配置项会使得服务拒绝启动。在 MySQL 5.7 中，用户依赖于使用 &#8216;help&#8217; 和 &#8216;verbose&#8217; 选项以及服务器配置的组合来测试选项，即 
./sql/mysqld --verbose --help --foo=bar
To see what values a running MySQL server is using, type
'mysqladmin variables' instead of 'mysqld --verbose --help'.
2019-03-14T05:13:46.500953Z 0 [ERROR] Aborting
在 MySQL 8.0.16 中，引入了一个名为“validate-config”的新选项，以帮助用户快速测试服务配置，而无需运行。如果没有发现问题，服务器退出时退出代码为零。对于首次出现无效配置，服务器将以错误（错误号 1 ）退出。
例如，让我们考虑在 MySQL 5.7 中弃用的服务器选项 &#8216;txreadonly&#8217; 并删除 MySQL 8.0：
./runtime_output_directory/mysqld --tx_read_only=on --validate-config
2019-03-30T10:40:02.712141Z 0 [ERROR] [MY-000067] [Server] unknown variable
'tx_read_only=on'.
2019-03-30T10:40:02.712178Z 0 [ERROR] [MY-010119] [Server] Aborting
validate-config 选项还可以与配置文件一起使用，以检查配置文件中指定的选项。例如：
./runtime_output_directory/mysqld \
--defaults-file=/home/nisha/workspace1/my.cnf --validate-config
2019-03-07T06:23:31.411188Z 0 [ERROR] [MY-000067] [Server] unknown variable
'tx_read_only=1'.
2019-03-07T06:23:31.411250Z 0 [ERROR] [MY-010119] [Server] Aborting
请注意，使用 defaults-file 选项时，它应该是命令行上的第一个选项，如上所示。
由于服务器在第一次出现无效值时退出，请更正报告的问题并重新运行以查找配置设置中的任何其他问题。
默认情况下，仅报告错误消息。如果用户也对警告和信息消息感兴趣，则需要提及 logerrorverbosity 选项值大于1。
./runtime_output_directory/mysqld \
--log-error-verbosity=2 --validate-config --read_only=s --transaction_read_only=10
2019-03-09T11:10:01.270676Z 0 [Warning] [MY-000076] [Server] option 'read_only': boolean value 's' was not recognized. Set to OFF.
2019-03-09T11:10:01.270695Z 0 [Warning] [MY-000076] [Server] option 'transaction-read-only': boolean value '10' was not recognized. Set to OFF.
如上所示，报告有关配置设置的警告，并退出服务器。因为没有错误，所以为零。在下面的示例中，配置名称无效，因此报告错误以及警告和服务器退出错误代码 1。
./runtime_output_directory/mysqld \
--log-error-verbosity=2 --validate-config --read_only=s --transaction_read_only=10 --foo=bar
2019-03-09T11:17:32.236782Z 0 [Warning] [MY-000076] [Server] option 'read_only': boolean value 's' was not recognized. Set to OFF.
2019-03-09T11:17:32.236796Z 0 [Warning] [MY-000076] [Server] option 'transaction-read-only': boolean value '10' was not recognized. Set to OFF.
2019-03-09T11:17:32.242247Z 0 [ERROR] [MY-000067] [Server] unknown variable 'foo=bar'.
2019-03-09T11:17:32.242327Z 0 [ERROR] [MY-010119] [Server] Aborting
&#8216;validate-config&#8217; 的范围仅限于在没有正常启动服务器去验证可以执行的选项。因此，&#8217;validate-config&#8217; 不包括特定于在服务器正常启动期间初始化的存储引擎和插件的选项。有关 &#8216;validate-config&#8217; 的信息也可以在 MySQL 文档中找到。我们希望这个新选项能让 MySQL 用户的工作更轻松，特别是在升级过程中。
**一如既往，感谢您使用MySQL！**
原文链接：
[https://mysqlserverteam.com/how-to-validate-server-configuration-settings/](https://mysqlserverteam.com/how-to-validate-server-configuration-settings/)
**近期社区动态**
**[第三期 社区技术内容征稿](http://mp.weixin.qq.com/s?__biz=MzU2NzgwMTg0MA==&mid=2247484778&idx=2&sn=0050d6c324e4d958950d34a29c2f8994&chksm=fc96e7f5cbe16ee3eb36d47a15e19a89ed459c8d24588a080d1bb849dc6d5f0816a72aafe35f&scene=21#wechat_redirect)**
**所有稿件，一经采用，均会为作者署名。**
**征稿主题：**MySQL、分布式中间件DBLE、数据传输组件DTLE相关的技术内容
**活动时间：**2019年6月11日 &#8211; 7月11日
**本期投稿奖励**
投稿成功：京东卡200元*1
优秀稿件：京东卡200元*1+社区定制周边（包含：定制文化衫、定制伞、鼠标垫）
**优秀稿件评选，文章获得****“好看****”****数量排名前三****的稿件为本期优秀稿件。**
![](.img/defe0cd6.png)