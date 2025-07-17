# 技术分享 | MySQL复制重试参数配置

**原文链接**: https://opensource.actionsky.com/20210601-mysql/
**分类**: MySQL 新特性
**发布时间**: 2021-06-01T23:00:23-08:00

---

作者：code0
爱可生 DMP 团队一位不知名的 coder，充满神秘的气息&#8230;
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
## 一、起因
非 root 用户运行 MySQL，当 MySQL 配置比较高时，MySQL 运行中生效的参数值与配置的值不一样，所以具体分析一下 MySQL 是怎么调整这些参数值的。
所以这篇文章的目的是为了说明在系统资源不够的情况下，MySQL 是怎么调整者三个参数的。
## 二、说明
此文涉及到 3 个参数:
- 
open_files_limit
- 
max_connections
- 
table_open_cache
这 3 个参数与系统相关的资源是最多能同时打开的文件（ `ulimit -n` 查看）实际即文件描述符（`fd`）。
系统参数与文件描述符的关系 &#8211; max_connection &#038; fd : 每一个MySQL connection都需要一个文件描述符 &#8211; table_open_cache &#038; fd 打开一张表至少需要一个文件描述符，如打开MyISAM需要两个fd
## 三、MySQL 调整参数的方式
- 
根据配置（配置的 3 个参数值或默认值）计算 request_open_files（需要的文件描述符）
- 
获取有效的系统的限制值 effective_open_files
- 
根据 effective_open_files 调整 request_open_files
- 
根据调整后的 request_open_files，计算实际生效的参数值（ `show variables` 查看到的 3 个参数值）
## 1、计算 request_open_files
request_open_files 有三个计算公式：
`# 最大连接数+同时打开的表的最大数量+其他（各种日志等等）
limit_1= max_connections + table_cache_size * 2 + 10;
# 假设平均每个连接打开的表的数量（2-4）
# 源码中是这么写的：
# We are trying to allocate no less than  
# max_connections*5 file handles 
limit_2= max_connections * 5;
# MySQL 默认的最低值是 5000
limit_3= open_files_limit ? open_files_limit : 5000;
# 所以 open_files_limit 期待的最低 
request_open_files= max(limit_1, limit_2,limit_3);
`
## 2、计算 effective_open_files
MySQL 的思路：在有限值的的范围内 MySQL 尽量将 effective_open_files 的值设大
## 3、修正 request_open_files
requested_open_files= min(effective_open_files, request_open_files);
## 重新计算参数值
## 1、修正 open_files_limit
open_files_limit = effective_open_files
## 2、修正 max_connections
max_connections 根据 request_open_files 来做修正。
`limit = requested_open_files - 10 - TABLE_OPEN_CACHE_MIN * 2;
`
- 
如果配置的 max_connections 值大于 limit，则将 max_connections 的值修正为 limit
- 
其他情况下 max_connections 保留配置值
## 3、修正 table_cache_size
table_cache_size 会根据 request_open_files 来做修正。
`# MySQL table_cache_size 最小值，400
limit1 = TABLE_OPEN_CACHE_MIN 
# 根据 requested_open_files 计算
limit2 = (requested_open_files - 10 - max_connections) / 2
limit = max(limit1,limt2);
`
- 
如果配置的 table_cache_size 值大于limit，则将 table_cache_size 的值修正为 limit
- 
其他情况下 table_cache_size 保留配置值
## 四、举例
以下用例全部在非 root 用户下运行
`- 系统资源不够且无法调整
# 参数设置
mysql max_connections = 1000 //ulimit -n 1024
# 生效的值
open_files_limit = 1024 max_connections = 1024 - 10 - 800 = 214 table_open_cache = ( 1024 - 10 - 214) / 2 = 400
---
- 系统资源不够可以调整
# 参数设置
mysql max_connections = 1000 //ulimit -S -n 1000 //ulimit -H -n 65535
# 生效的值
open_files_limit = 65535 max_connections = 1000 table_open_cache = ( 1024 - 10 - 214) / 2 = 400
---
- mysql 修改 open_files_limit
# 参数设置
//mysql max_connections = 1000 max_connections = 1000 //ulimit -n 65535
# 生效的值
open_files_limit = 65535 max_connections = 1000 table_open_cache = 2000 ```
`
## 五、其它
淘宝数据库内核月报中说道的相关内容：《MySQL·答疑解惑·open file limits》这篇主要讲的是，MySQL 在执行哪些操作时会执行打开文件的操作。
《MySQL·答疑解惑·open file limits》：http://mysql.taobao.org//monthly/2015/08/07/