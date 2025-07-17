# 10 期 | binlog 怎么写入日志文件？

**原文链接**: https://opensource.actionsky.com/10-%e6%9c%9f-binlog-%e6%80%8e%e4%b9%88%e5%86%99%e5%85%a5%e6%97%a5%e5%bf%97%e6%96%87%e4%bb%b6%ef%bc%9f/
**分类**: 技术干货
**发布时间**: 2024-03-20T22:28:38-08:00

---

这篇文章，我们来聊聊：事务执行过程中，临时存放到 trx_cache 的那些 binlog，是怎么乾坤大挪移到 binlog 日志文件的。
> 作者：操盛春，爱可生技术专家，公众号『一树一溪』作者，专注于研究 MySQL 和 OceanBase 源码。
爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
本文基于 MySQL 8.0.32 源码，存储引擎为 InnoDB。
## 1. 关于 binlog 日志文件
binlog 日志文件包含两部分：
- **内存 buffer**，这是 MySQL 自己为 binlog 日志文件提供的内存缓冲区，称为 `IO_CACHE`，和操作系统为文件提供的缓冲区（`page cache`）不是同一个东西。
- **磁盘文件**，这是磁盘上真正的 binlog 日志文件。
不考虑操作系统的 page cache，写入 binlog 日志到 binlog 日志文件的过程是这样的：
- 写入 binlog 日志到内存 buffer。
- 写满内存 buffer 之后，再把内存 buffer 中的全部内容一次性写入 binlog 日志文件。
- 清空内存 buffer，以供后续写入 binlog 日志复用。
和 trx_cache 的内存 buffer 一样，binlog 日志文件的内存 buffer 也有大小限制。
MySQL 打开新的 binlog 日志文件时，会初始化对应的内存 buffer，代码如下：
`// sql/binlog.cc
class MYSQL_BIN_LOG::Binlog_ofile : public Basic_ostream {
...
bool open(...) {
...
if (file_ostream->open(...)) return true;
...
}
...
}
// sql/basic_ostream.cc
bool IO_CACHE_ostream::open(...) {
...
// 打开 binlog 日志文件
if ((file = mysql_file_open(...)) < 0)
return true;
// 初始化内存 buffer
if (init_io_cache(..., IO_SIZE, ...)) {
...
}
return false;
}
`
上面代码中，传递给 init_io_cache() 函数 `cachesize` 参数的 `IO_SIZE` 用于指定内存 buffer 的大小。
IO_SIZE 是个常量，定义如下：
`// include/my_io.h
// IO_SIZE = 4096 字节
constexpr const size_t IO_SIZE{4096}
`
init_io_cache() 调用 init_io_cache_ext() 初始化内存 buffer 时，指定了内存 buffer 大小的下限为 `2 * IO_SIZE`。
所以，binlog 日志文件的内存 buffer 大小并不是 4096 字节，而是 8192 字节（**8K**）。
## 2. 从 trx_cache 读出来
通过前面介绍事务执行过程中 binlog 日志写到哪里的文章，我们知道了 trx_cache 包含两部分：
- **内存 buffer**。
- **临时文件**。
事务执行过程中产生的 binlog 日志都会先写入 trx_cache，写入过程是这样的：
- 先写入内存 buffer。
- 写满内存 buffer 之后，再把内存 buffer 中的全部内容一次性写入临时文件。
- 清空内存 buffer，以供后续复用。
事务提交过程中，二阶段提交的 flush 子阶段要把 trx_cache 中的 binlog 日志写入 binlog 日志文件。
写入 binlog 日志文件之前，要先把 binlog 日志从 trx_cache 中读出来，这分为两种情况。
**情况 1**：只从内存 buffer 读取。
如果事务执行过程中产生的 binlog 日志少，没有写满过 trx_cache 的内存 buffer，就只需要从内存 buffer 中读取。
**情况 2**：从临时文件读取。
如果事务执行过程中产生的 binlog 日志比较多，写满过 trx_cache 的内存 buffer 一次或多次，临时文件中也会有 binlog 日志。那就需要从临时文件中读取 binlog 日志了。
事务执行过程中，把 binlog 日志写入 trx_cache，内存 buffer 类型是 `WRITE_CACHE`。
二阶段提交的 flush 子阶段，事务不会再产生 binlog 日志，也就不会再往 trx_cache 写 binlog 日志，内存 buffer 作为 WRITE_CACHE 的身份就结束了。
从此之后，它会被用作从 trx_cache 临时文件读取 binlog 日志的内存 buffer。它有了新的身份，就是 `READ_CACHE`。
### 2.1 只从内存 buffer 读取
这种情况就很简单了，因为 trx_cache 的 binlog 日志只存在于内存 buffer 中。
从内存 buffer 中读取全部 binlog 日志写入 binlog 日志文件就可以了。
### 2.2 从临时文件读取
事务执行过程中产生的 binlog 日志，写入 trx_cache 时，要先把内存 buffer 写满。
最后一次写满内存 buffer，把里面全部内容写入 trx_cache 临时文件之后，还有可能出现两种场景：
**场景 1**：在此之后，事务就没再产生 binlog 日志。事务提交时，binlog 日志只存在于 trx_cache 的临时文件中，内存 buffer 是空的。
**场景 2**：在此之后，事务还产生了一些 binlog 日志，但是没写满内存 buffer。事务提交时，trx_cache 中的大部分 binlog 日志存在于临时文件中，小部分 binlog 日志存在于内存 buffer 中。
内存 buffer 的类型从 WRITE_CACHE 转换为 READ_CACHE 之前，为了避免丢失其中的 binlog 日志，MySQL 会把内存 buffer 中的全部内容都写入临时文件。
场景 2 变成了场景 1，逻辑就更简单了，只需要考虑场景 1。
trx_cache 内存 buffer 的大小，我们称为 `buffer_length`，默认是 32K。
假设从临时文件读取 binlog 日志的操作需要进行 N 次（N >= 1），前面 N &#8211; 1 次都会读取 `buffer_length` 字节，每次都会填满内存 buffer。最后一次读取剩余的小于等于 32K 的全部 binlog 日志。
每次从临时文件读取 binlog 日志到内存 buffer 之后，都会把内存 buffer 中的 binlog 日志全部写入 binlog 日志文件。
循环往复，直到把临时文件中的所有 binlog 日志都写入 binlog 日志文件，这个过程就结束了。
## 3. 写入 binlog 日志文件
前面我们介绍了把 binlog 日志写入 binlog 日志文件的整体流程。
因为写入过程涉及 binlog 内存 buffer 和日志文件的协同配合，我们再来看看两者是怎么配合的。
以把 trx_cache 内存 buffer 中 32K 的 binlog 日志写入 binlog 日志文件为例，流程是这样的：
- 计算 binlog 日志文件的内存 buffer 剩余多少空闲空间（**假设为 2K**）。
- 判断 binlog 日志文件的内存 buffer 的剩余空闲空间，是否能够容纳从 trx_cache 内存 buffer 读取出来的 32K binlog 日志，显然容纳不下。
- 那么，先把读取出来的 32K binlog 日志中的前面 2K 写入 binlog 日志文件的内存 buffer，剩余未写入 binlog 日志文件的还有 30K。
- 判断剩余未写入 binlog 日志文件的 binlog 日志，是否大于等于 **4096 字节**（`IO_SIZE`）。
- 如果剩余 binlog 日志**小于** 4096 字节，把它们都写入 binlog 日志文件的内存 buffer。
- 如果剩余 binlog 日志**大于等于** 4096 字节，把剩余 binlog 日志前面的 **N * 4096** 字节直接写入 binlog 日志文件。
最后有可能还会剩下不足 4096 字节的 binlog 日志，写入 binlog 日志文件的内存 buffer。
## 4. 总结
binlog 日志文件包含两部分：内存 buffer、磁盘文件。内存 buffer 的大小固定为 8K。
二阶段提交的 flush 子阶段，会从 trx_cache 中读取 binlog 日志，写入 binlog 日志文件。
> **本期问题**：如果事务执行过程中产生的 binlog 日志直接写入 binlog 日志文件，会有什么问题吗？欢迎留言交流。
**下期预告**：MySQL 核心模块揭秘 | 11 期 | InnoDB 提交事务，提交了什么？