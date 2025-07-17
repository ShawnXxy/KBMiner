# 技术译文 | 使用 Perf 和火焰图分析软件

**原文链接**: https://opensource.actionsky.com/20191210-percona/
**分类**: 技术干货
**发布时间**: 2019-12-10T00:35:50-08:00

---

> **作者：****Agustín**
翻译：孟维克
原文：https://www.percona.com/blog/2019/11/20/profiling-software-using-perf-and-flame-graphs/
在这篇博文中，我们将探讨如何一起使用 perf 和火焰图。它们用于生成我们选择的软件正在调用的函数的图形。在此我们使用 Percona 分支版本，但是它可以扩展到任何可以进行解析堆栈跟踪的软件。在继续之前，请注意，与任何分析工具一样，除非您知道自己在做什么，否则**不要**在生产环境运行。
**安装需要的软件包**为了简单，为使用 CentOS7 版本，但是对于基于 Debian 的发行版来说，它们应该是相同的（步骤中的唯一区别是用 `apt-get install linux-tools-$(uname -r)` 代替 yum 命令）。
安装 perf- `SHELL> sudo yum install -y perf`
获得火焰图软件包- `SHELL> mkdir -p ~/src`
- `SHELL> cd ~/src`
- `SHELL> git clone https://github.com/brendangregg/FlameGraph`
全部安装完毕！让我们继续
**抓取采集样本**火焰图是一种可视化数据的方式，所以我们需要一些可以作为基础的样本。可以用三种方式做到这一点（请注意，这里我们使用 `-p` 选项仅抓取我们感兴趣的进程的数据，但是如果需要，我们可以抓取所有正在运行的进程的数据）
1. 仅抓取设定时间（这里是10秒）- `SHELL> sudo perf record -a -F 99 -g -p $(pgrep -x mysqld) --sleep 10`
2. 抓取直到我们发出中断讯号（CTRL+C）- `SHELL> sudo perf record -a -F 99 -g -p $(pgrep -x mysqld)`
3. 抓取整个进程的生命周期- `# 注意，如果我们中断了这个variant，我们同样杀死了上面的子进程`
- `SHELL> sudo perf record -a -F 99 -g --/sbin/mysqld \`
- `--defaults-file=/etc/percona-server.conf.d/mysqld.cnf --user=mysql`
或者- `SHELL> sudo perf record -a -F 99 -g -p $(pgrep -x mysqld) --mysql -e "SELECT * FROM db.table"`
在第三个场景的第一种情况下，我们被迫抓取了所有进程的数据，因为实现不可能直到进程 ID 号（PID）（通过执行该命令，我们实际上正在启动 MySQL 服务）。当您希望从进程启动时就开始获取数据，这种类型的命令非常有用，否则是不可能的。在第二个场景下，我们在正在运行的 MySQL 服务上执行一个查询，因此我们可以使用 *-p* 选项抓取这个进程的数据。例如，如果您希望抓取作业正在运行的时的数据，这就非常方便。
**准备样本**初始化抓取完成后，我们需要将收集到的数据“可读”。这是必要的，因为通过 *perf record* 生成的是二进制格式。因此，我们将执行：- `SHELL> sudo perf script > perf.script`
默认情况下它读取 *perf.data*，*perf record* 也默认输出到这个文件。它可以分别使用 *-i* 选项和 *-o* 选项来覆盖写入。现在我们能读取生成的文本文件，因为已经是易读的形式。然而，当您做到这时，你很快就会意识到我们为什么要将这些数据聚合为更易懂的形式。
**生成火焰图**我们可以将第一个命令的输出作为第二个命令的输出，在一行命令中完成以下工作。因为我们没有将火焰图的 git 文件夹加入到 PATH 变量中，因此要使用完整路径。- `SHELL> ~/src/FlameGraph/stackcollapse-perf.pl perf.script | ~/src/FlameGraph/flamegraph.pl > flamegraph.svg`
现在我们在任何浏览器打开 .svg 文件并开始分析富含信息的图形。
**看起来如何**作为示例，我将使用第 2 种抓取数据的方法的完整命令、输出和生成火焰图的屏幕截图帖在如下。我们执行 `INSERT INTO...SELECT` 语句，我们可以分析执行过程。
**看起来如何**作为示例，我将使用第 2 种抓取数据的方法的完整命令、输出和生成火焰图的屏幕截图帖在如下。我们执行 `INSERT INTO...SELECT` 语句，我们可以分析执行过程。- `SHELL> time sudo perf record -a -F 99 -g \`
- `-p $(pgrep -x mysqld) \`
- `--mysql test -e "INSERT INTO joinit SELECT NULL, uuid(), time(now()),  (FLOOR( 1 + RAND( ) *60 )) FROM joinit;"`
- `Warning:`
- `PID/TID switch overriding SYSTEM`
- `[ perf record: Woken up 7 times to write data ]`
- `[ perf record: Captured and wrote 1.909 MB perf.data (8214 samples) ]`
- 
- `real 1m24.366s`
- `user 0m0.133s`
- `sys 0m0.378s`
- `SHELL> sudo perf script | \`
- `~/src/FlameGraph/stackcollapse-perf.pl perf.script | \`
- `~/src/FlameGraph/flamegraph.pl > mysql_select_into_flamegraph.svg`
敏锐的读者会注意到，我们在这里更进一步，通过一个管道（|）合并了步骤 2 和步骤 3，避免向 *perf.script* 文件写入和读取数据。此外，还有时间输出，我们可以对工具生成的数据量进行估计（1 分 25 秒生成约 2Mb 数据）；当然这取决于许多因素，所以要谨慎对待，并在自己的环境中进行测试。
生成的火焰图如下：
![](https://opensource.actionsky.com/wp-content/uploads/2019/12/火焰图1-1024x479.jpg)											
优化的一个明显的候选对象是 *write_record*：如果我们使这个函数变的更快，那么就有很大潜力来减少整体执行时间（左下角的蓝色方框表示，我们可以看到 60% 的样本是在这个代码路径中获取的）。在下面的最后一个章节中，我们将提供一篇博客，该文章详细解释了如何解释火焰图，但是现在，您只需要知道移动鼠标在各个函数名上，它将动态地更改左下角显示的信息。您也可以通过以下指南更好理解它：
![](https://opensource.actionsky.com/wp-content/uploads/2019/12/火焰图2-1024x530.jpg)											
**总结**
对于支持工程师，在许多情况下，我们使用此工具来深入了解 MySQL 正在执行的内容及执行的时间。这样，我们就可以更好地了解特定负载背后的操作，并采取相应的措施。这个软件用于优化或故障排查，它是我们工具箱中非常强大的工具！众所周知，人类处理图像比处理文本更擅长，而在我看来，该工具十分出色。
**相关链接**> Interpreting Flame Graphs (scroll down to the “Flame Graph Interpretation” section)
https://queue.acm.org/detail.cfm?id=2927301
Flame Graphs 201, Percona分享会
https://www.percona.com/resources/webinars/flame-graphs-201
Brendan Gregg ，火焰图作者
http://www.brendangregg.com/flamegraphs.html
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