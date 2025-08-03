# 技术分享 | MySQL Test 初探

**原文链接**: https://opensource.actionsky.com/20200331-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-03-31T00:40:02-08:00

---

作者：雷霞
爱可生测试团队负责人，专注于 MySQL 相关的测试工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
**什么是 MySQL Test？**
MySQL Test 是 MySQL 发行版本中集成 all-in-one 测试框架，用于做 mysql 服务的单元，回归和一致性测试，并提供了运行单元测试和创建新单元测试的工具。框架包括一组测试用例和用于运行它们的程序：perl 脚本（mysql-test-run.pl）和 c++ 二进制（mysqltest）。- perl 脚本：负责控制流程，包括启停、识别执行哪些用例、创建文件夹、收集结果等操作。
- mysqltest：负责执行测试用例，包括读文件，解析特定语法，执行用例。
**安装环境**
OS：Ubuntu 18.04.1 LTS
**1. 下载 MySQL 源码包**
本文采用的 MySQL 版本是 5.7.26，可根据需要自行选择版本。- `wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.26.tar.gz`
**2. 安装编译 MySQL 源码所需依赖包**
- `apt install make cmake gcc g++ perl \`
- `    bison libaio-dev libncurses5 \`
- `    libncurses5-dev libnuma-dev`
如上步操作失败或速度过慢，可修改 `/etc/apt/sources.list` 换成国内的源。- `deb https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse`
- `deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic main restricted universe multiverse`
- `deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse`
- `deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse`
- `deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse`
- `deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse`
- `deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse`
- `deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-security main restricted universe multiverse`
- `deb https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse`
- `deb-src https://mirrors.ustc.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse`
**3. 安装 boost 1.59**
需要安装 boost 1.59 版本，系统默认的 1.65 版本不可用。- `wget https://sourceforge.net/projects/boost/files/boost/1.59.0/boost_1_59_0.tar.gz`
- `./bootstrap.sh`
- `./b2 install`
**4. 配置编译安装**
- `cmake . -DBUILD_CONFIG=mysql_release -DCPACK_MONOLITHIC_INSTALL=ON -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DMYSQLX_TCP_PORT=33060 -DMYSQL_UNIX_ADDR=/usr/local/mysql/mysql.sock -DMYSQL_TCP_PORT=3306 -DMYSQLX_UNIX_ADDR=/usr/local/mysql/mysqlx.sock -DMYSQL_DATADIR=/usr/local/mysql/data -DSYSCONFDIR=/usr/local/mysql/etc -DENABLE_DOWNLOADS=ON -DWITH_BOOST=system`
- 
- `make -j4`
- `make install`
编译完成后，在 MySQL 安装目录生成如下目录结构。- `drwxr-xr-x  2 root root   4096 Feb 12 04:24 collections/`
- `drwxr-xr-x  4 root root   4096 Feb 12 04:24 extra/`
- `drwxr-xr-x  2 root root  40960 Feb 12 04:24 include/`
- `drwxr-xr-x  4 root root   4096 Feb 12 04:24 lib/`
- `-rw-r--r--  1 root root    836 Apr 13  2019 lsan.supp`
- `lrwxrwxrwx  1 root root     19 Feb 12 04:24 mtr -> ./mysql-test-run.pl*`
- `-rwxr-xr-x  1 root root  36862 Apr 13  2019 mysql-stress-test.pl*`
- `lrwxrwxrwx  1 root root     19 Feb 12 04:24 mysql-test-run -> ./mysql-test-run.pl*`
- `-rwxr-xr-x  1 root root 220158 Apr 13  2019 mysql-test-run.pl*`
- `drwxr-xr-x  2 root root  65536 Feb 16 10:22 r/`
- `drwxr-xr-x  7 root root  12288 Feb 12 04:24 std_data/`
- `drwxr-xr-x 46 root root   4096 Feb 12 04:24 suite/`
- `drwxr-xr-x  2 root root  77824 Feb 16 10:22 t/`
- `-rw-r--r--  1 root root  29730 Apr 13  2019 valgrind.supp`
- `drwxr-xr-x  9 root root   4096 Mar  5 08:40 var/`
**测试示例**
我们通过一个最简单的例子来说明这个框架是怎么使用的。
**1. 创建测试用例**
在 `mysql-test/t` 目录下创建一个文件名为 action_1st.test 的文件，- `root@ubuntu:/usr/local/mysql/mysql-test# vim t/action_1st.test`
- `--disable_warnings`
- `DROP TABLE IF EXISTS t1;`
- `SET @@sql_mode='NO_ENGINE_SUBSTITUTION';`
- `--enable_warnings`
- 
- `SET SQL_WARNINGS=1;`
- 
- `CREATE TABLE t1 (a INT);`
- `INSERT INTO t1 VALUES (1);`
- `INSERT INTO t1 VALUES (2);`
- 
- `DROP TABLE t1;`
在 `/mysql-test/r` 目录下创建一个 action_1st.resul 的文件，- `root@ubuntu:/usr/local/mysql/mysql-test# vim r/action_1st.result`
- `DROP TABLE IF EXISTS t1;`
- `SET @@sql_mode='NO_ENGINE_SUBSTITUTION';`
- `SET SQL_WARNINGS=1;`
- `CREATE TABLE t1 (a INT);`
- `INSERT INTO t1 VALUES (1);`
- `INSERT INTO t1 VALUES (2);`
- `DROP TABLE t1;`
**2. 执行并查看运行效果**
执行测试用例，- `root@ubuntu:/usr/local/mysql/mysql-test# ./mtr action_1st.test`
- `Logging: ./mtr  action_1st.test`
- `MySQL Version 5.7.26`
- `Checking supported features...`
- ` - SSL connections supported`
- `Collecting tests...`
- `Checking leftover processes...`
- `Removing old var directory...`
- `Creating var directory '/usr/local/mysql/mysql-test/var'...`
- `Installing system database...`
- `Using parallel: 1`
- 
- `==============================================================================`
- 
- `TEST                                      RESULT   TIME (ms) or COMMENT`
- `--------------------------------------------------------------------------`
- 
- `worker[1] Using MTR_BUILD_THREAD 300, with reserved ports 13000..13009`
- `worker[1] mysql-test-run: WARNING: running this script as _root_ will cause some tests to be skipped`
- `[100%] main.action_1st                          [ pass ]     12`
- `--------------------------------------------------------------------------`
- `The servers were restarted 0 times`
- `Spent 0.012 of 4 seconds executing testcases`
- 
- `Completed: All 1 tests were successful.`
测试用例运行时，mysqltest 会将 mysql-test/t/action_1st.test 的执行结果与 mysql-test/r/action_1st.result 作差异对比 diff。如果预期结果与实际结果不同，测试用例失败，如上图所示，测试用例的执行结果与预期结果一致。