# 技术译文 | 使用 Docker 安装 MySQL

**原文链接**: https://opensource.actionsky.com/20191121-mysql/
**分类**: MySQL 新特性
**发布时间**: 2019-11-21T00:34:26-08:00

---

**作者：****Peter Zaitsev**
原文：https://www.percona.com/blog/2019/11/19/installing-mysql-with-docker/
在工作中，我经常需要安装特定版本的 MySQL，MariaDB 或 Percona 来运行一些实验，例如：检查版本差异或是提供测试说明。此博客系列将阐述如何使用 Docker 安装 MySQL，MariaDB 或 Percona。这篇文章是第一篇，重点是 MySQL。Docker 的优点在于它可以非常轻松地安装最新的 MySQL 版本以及任何其他版本，但往往与典型的生产安装不匹配。当您需要简单的单个实例时，Docker 的确很方便。如果您正在研究一些与复制相关的行为，那么则不一定适合。**这些说明皆在快速、轻松地运行测试实例的情况下。****不适用于生产部署。****以下内容假定已安装 Docker。**
首先，您应该知道只有两个“官方” MySQL Docker 存储库。其中之一由 Docker 团队维护，可通过一个简单的 docker 命令 mysql:latest 运行起来。另一个由 Oracle 的 MySQL 团队维护，语法：- `docker run mysql/mysql-server:latest`
**说明：语法中的 latest 是 tag 值，表示默认安装库中的最新版本。**在以下示例中，我们将使用 MySQL 团队的 Docker 映像，尽管 Docker 团队的工作方式与此类似。
**使用 Docker 安装最新版本的 MySQL**- `docker run --name mysql-latest  \`
- `-p 3306:3306 -p 33060:33060  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:latest`
这将启动最新版本的 MySQL 实例，可以使用指定的 root 密码从任何地方远程访问该实例。这很容易测试，但不是好的安全习惯（这就是为什么它不是默认值）的原因。
**连接到 MySQL Server Docker 容器**使用 Docker 安装意味着您无法直接在主机上获得任何工具，实用程序或库，因此您可以单独安装它们，从远程主机访问创建的实例，或使用 Docker 映像附带的命令行。**通过 Docker 启动 MySQL 命令行客户端：**- `docker exec -it mysql-latest mysql -uroot -pstrongpassword`
**使用 Docker 启动 MySQL Shell：**
- `docker exec -it mysql-latest mysqlsh -uroot -pstrongpassword`
**在 Docker 容器中管理 MySQL 服务器**当您要停止 MySQL Server Docker 容器运行时：- `docker stop mysql-latest`
如果要重新启动已停止的 MySQL Docker 容器，则不应尝试使用 docker run 重新启动它。相反，您应该使用：
- `docker start mysql-latest`
如果出现错误，例如，如果容器未启动，则可以使用以下命令访问其日志：
- `docker logs mysql-latest`
如果要从头开始重新创建一个新的 Docker 容器，可以运行：
- `docker stop mysql-latest`
- `docker rm mysql-latest`
之后再次执行 `docker run` 命令。
**将命令行选项传给 Docker 容器中的 MySQL Server**如果要将某些命令行选项传给 MySQL Server，可以采用以下方式：- `docker run --name mysql-latest  \`
- `-p 3306:3306 -p 33060:33060  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:latest \`
- `--innodb_buffer_pool_size=256M \`
- `--innodb_flush_method=O_DIRECT \`
**在 Docker 中运行指定版本的 MySQL 服务器**如果想在 Docker 容器中运行某版本的 MySQL，这很简单。您可以使用 Docker Image Tag 选择想要的版本，并将 Name 更改为其他名称，以避免名称冲突：- `docker run --name mysql-8.0.17  \`
- `-p 3306:3306 -p 33060:33060  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:8.0.17`
这将在 Docker 容器中启动 MySQL 8.0.17。- `docker run --name mysql-5.7  \`
- `-p 3306:3306 -p 33060:33060  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:5.7`
这将在 Docker 中启动最新的 MySQL 5.7。
**在 Docker 中同时运行多版本的 MySQL 服务器**同时在 Docker 中运行多版本的 MySQL ，潜在问题是 TCP 端口冲突。如果您不从外部访问 Docker 容器，而只运行同一容器中包含的程序，则可以删除端口映射（-p option）选项，然后可以运行多个容器：- `docker run --name mysql-latest  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:latest`
- 
- `docker run --name mysql-8.0.17  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:8.0.17`
在更常见的情况下，当您需要从外部访问 Docker 容器时，您将需要将其映射为使用不同的外部端口名称。例如，要在端口 3306/33060 和 MySQL 8.0.17 在 3307/33070 处启动最新的 MySQL 8，我们可以使用：- `docker run --name mysql-latest  \`
- `-p 3306:3306 -p 33060:33060  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:latest`
- 
- `docker run --name mysql-8.0.17  \`
- `-p 3307:3306 -p 33070:33060  \`
- `-e MYSQL_ROOT_HOST='%' -e MYSQL_ROOT_PASSWORD='strongpassword'   \`
- `-d mysql/mysql-server:8.0.17`
如果要在 Docker 上使用 MySQL 进行更复杂的事请，那还有很多事情要考虑。
> 有关更多信息，请查阅：
https://hub.docker.com/r/mysql/mysql-server/
https://dev.mysql.com/doc/refman/8.0/en/linux-installation-docker.html
**社区近期动态**
**No.1**
**Mycat 问题免费诊断**
诊断范围支持：
Mycat 的故障诊断、源码分析、性能优化
服务支持渠道：
技术交流群，进群后可提问
QQ群（669663113）
社区通道，邮件&电话
osc@actionsky.com
现场拜访，线下实地，1天免费拜访
关注“爱可生开源社区”公众号，回复关键字“Mycat”，获取活动详情。
**No.2**
**社区技术内容征稿**
征稿内容：
格式：.md/.doc/.txt
主题：MySQL、分布式中间件DBLE、数据传输组件DTLE相关技术内容
要求：原创且未发布过
奖励：作者署名；200元京东E卡+社区周边
投稿方式：
邮箱：osc@actionsky.com
格式：[投稿]姓名+文章标题
以附件形式发送，正文需注明姓名、手机号、微信号，以便小编及时联系