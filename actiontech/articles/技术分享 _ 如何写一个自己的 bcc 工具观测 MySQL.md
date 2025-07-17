# 技术分享 | 如何写一个自己的 bcc 工具观测 MySQL？

**原文链接**: https://opensource.actionsky.com/20201228-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-12-27T23:39:01-08:00

---

作者：邓欢
爱可生 DMP 团队开发成员，主要负责 DMP 相关开发。
本文来源：原创投稿*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
社区之前有一篇文章[《如何使用 bcc 工具观测 MySQL 延迟》](https://opensource.actionsky.com/20200324-mysql/)，介绍了 bcc 是什么以及如何用 bcc 项目提供的工具观测 MySQL。
> 
**bcc 项目**
https://github.com/iovisor/bcc
但是如果 bcc 项目提供的 MySQL 观察工具不能满足我们的需求时该怎么办？那就自己写一个 MySQL 观察工具呗。本文将通过一个例子：观测 MySQL MGR 的数据包的处理线程号，来介绍如何编写自己的 MySQL 动态观测工具。
**环境准备**
1. 准备一台 Linux 机器，安装好 Python 和内核开发包。（注：内核开发包版本必须和内核版本一致）2. 通过 dbdeployer 安装一组组复制架构的数据库。
**bcc 观测原理**
![](.img/93bc23a8.png)											
bcc 是 eBPF 的前端，它是依赖 ePBF 实现数据收集的。整个过程可以分为三部分：- 生成 BPF 字节码
- 将 BPF 字节码加载到内核执行
- 通过 perf event 或者异步的方式从内核将数据拷贝到用户空间
bcc 程序使用 Python 编写，它会嵌入一段 c 代码，执行时将 c 代码编译成字节码加载到内核运行。而 Python 代码可以通过 perf event 读取到数据然后展示出来。了解了原理之后，下面我们就可以开始着手写自己的观测工具了。从 group replication 插件中找到 MySQL MGR 的数据包的处理函数为 apply_data_packet，所以我们的目标就是观测这个函数是哪个线程执行的。
**开始开发**
1. 我们将源代码文件命名为 mgr_apply_data_packet.py，因为使用 Python 进行开发，所以在第一行指定 Python 解释器：- 
`#!/usr/bin/python`
2. 接下来是需要导入的包，我们只使用了 bcc 包的 BPF 对象，所以只需要导入这一个对象就行。这个对象可以将我们的观测代码嵌入到观测点中执行，同时收集观测点数据。- 
```
from bcc import BPF
```
3. 接下来需要编写我们的观测代码。
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
bpf_text="""`#include <uapi/linux/ptrace.h>``#include <linux/sched.h>``
``struct data_t {``    u32 pid;``    u32 tgid;``    u64 ts;``};``
``BPF_PERF_OUTPUT(events);``
``int do_apply_data_packet(struct pt_regs *ctx) {``    struct task_struct *t = (struct task_struct *)bpf_get_current_task();``    struct data_t data = {};``    // thread id``    data.pid = t->pid;``    // thread group id(pid in user space)``    data.tgid = t->tgid;``    // bpf_ktime_get_ns returns u64 number of nanoseconds. Starts at system boot time but stops during suspend.``    data.ts = bpf_ktime_get_ns();``
``    events.perf_submit(ctx, &data, sizeof(data));``
``    return 0;``}``"""
```
观测代码是一段 c 代码，但是它是通过 BPF 对象执行的，所以这里放在了 bpf_text 对象中。这段代码主要有四部分：- 头文件 <uapi/linux/ptrace.h>和<linux/sched.h>。
- 结构体 data_t 保存我们每次观测到的结果。
- BPF_PERF_OUTPUT 定义了一个叫 events 的表，观测代码可以将观测数据写入到 events 表中，而 Python 代码可以从这个表中读取到观测数据。
- do_apply_data_packet 函数收集观测数据。我们通过 bpf_get_current_task 获取了 MySQL 进程对应的结构体 task_struct，然后从获取了其中的 pid 和 tgid。这里需要注意的是 task_struct 中的 pid 其实对应的是线程 id，tgid 对应的是线程组 id（即用户空间中的进程 id）。时间 ts 是通过 bpf_ktime_get_ns 函数获取的，这个时间并不是一个时钟时间，而是系统启动的时间。最后通过 events 表的 perf_submit 方法将观测的数据提交到表中。
4. 接下来需要做的是将观测代码与 MySQL 中需要观测的函数关联起来。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
# get mysql function name and trace it.``path = "/root/sandboxes/mysql_base/8.0.18/lib/plugin/group_replication.so"``regex = "\\w+apply_data_packet\\w+"``symbols = BPF.get_user_functions_and_addresses(path, regex)``if len(symbols) == 0:``    print("Can't find function 'apply_data_packet' in %s" % (path))``    exit(1)``(mysql_func_name, addr) = symbols[0]``b = BPF(text=bpf_text)``b.attach_uprobe(name=path, sym=mysql_func_name, fn_name="do_apply_data_packet")`因为 MySQL 的组复制是通过组复制插件实现的，所以我们需求去插件的代码中寻找需要观测的函数 apply_data_packet。寻找是通过 BPF 对象的 get_user_functions_and_addresses 函数实现的，它会从插件代码的符号表中寻找匹配正则表达式 regex 的所有符号。这里我们只需要从所有的符号中取第一个符号的函数名。接着使用前面的观测代码作为参数创建 BPF 对象，然后通过 attach_uprobe 将 MySQL 程序中的 apply_data_packet 函数与观测函数 do_apply_data_packet 关联起来。值得一提的是 attach_uprobe 函数关联的是用户空间的函数和观测函数。如果需要观测的是 Linux 内核中的函数，需要使用 attach_kprobe。****> **attach_kprobe**https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md#1-attach_kprobe
5. 最后就是输出观测结果了。- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
```
# output trace result.`print("Tracing MySQL server mgr apply_data_packet function")``print("%-14s %-6s %-6s" % ("SINCE_UP_TIME(s)", "PID", "THREAD"))``
``def print_event(cpu, data, size):``    event = b["events"].event(data)``    print("%-14s %-6s %-6s" % (event.ts/1000000000, event.tgid, event.pid))``
``b["events"].open_perf_buffer(print_event)``while 1:``    try:``        b.perf_buffer_poll()``    except KeyboardInterrupt:``        exit()
```
首先输出的两行头部信息。接着是输出单次观测数据的回调函数，而 open_perf_buffer 则是将这个回调函数注册到 events 表中。最后就是不断从 perl 缓冲中获取检测数据，然后通过回调函数输出结果。
**结果演示**
运行工具然后在另一个终端中往 MySQL 写入数据，可以观测到工具输出：- 
- 
- 
- 
- 
- 
root@ubuntu:/tmp# python mgr_apply_data_packet.py``Tracing MySQL server mgr apply_data_packet function``SINCE_UP_TIME(s) PID    THREAD``2165924        26387  27060``2165924        25810  27043``2165924        26962  27080`
**参考**
1. http://www.brendangregg.com/ebpf.html
2. https://github.com/iovisor/bcc/blob/master/docs/tutorial_bcc_python_developer.md
3. https://github.com/iovisor/bcc/blob/7e3f0c08c7c28757711c0a173b5bd7d9a31cf7ee/tools/dbslower.py
4. https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md
相关推荐：
[技术分享 | 如何使用 bcc 工具观测 MySQL 延迟](https://opensource.actionsky.com/20200324-mysql/)
[技术分享 | 大量 Opening tables 案例分析](https://opensource.actionsky.com/20201217-mysql/)
[技术分享 | MySQL 闪回工具 MyFlash](https://opensource.actionsky.com/20201214-mysql/)