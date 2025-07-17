# 技术分享 | 使用 sync_diff_inspector 对两个 MySQL 进行数据校验

**原文链接**: https://opensource.actionsky.com/20230228-sync-diff-inspector/
**分类**: 技术干货
**发布时间**: 2023-03-01T17:30:33-08:00

---

作者：沈光宇
爱可生南区 DBA 团队成员，主要负责 MySQL 故障处理和性能优化。对技术执着，为客户负责。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一、sync-diff-inspector简介
sync-diff-inspector 是由 PingCap 开源的数据校验工具，用于校验MySQL/TiDB中两份数据是否一致。
主要功能如下：
- 对比表结构和数据
- 如果数据不一致，则生成用于修复数据的 SQL 语句
- 支持不同库名或表名的数据校验
- 支持分库分表场景下的数据校验
- 支持 TiDB 主从集群的数据校验
- 支持从 TiDB DM 拉取配置的数据校验
sync-diff-inspector 的使用限制
- 对于 MySQL 和 TiDB 之间的数据同步不支持在线校验，需要保证上下游校验的表中没有数据写入，或者保证某个范围内的数据不再变更，通过配置 range 来校验这个范围内的数据。
- FLOAT、DOUBLE 等浮点数类型在 TiDB 和 MySQL 中的实现方式不同，在计算 checksum 时会分别取 6 位和 15 位有效数字。如果不使用该特性，需要设置 ignore-columns 忽略这些列的检查。
- 支持对不包含主键或者唯一索引的表进行校验，但是如果数据不一致，生成的用于修复的 SQL 可能无法正确修复数据。
本文将介绍使用 sync-diff-inspector 工具对两个 MySQL 实例中的数据进行校验，两个 MySQL 实例之间使用 DTS 工具来同步数据。
#### 二、sync-diff-inspector工具下载安装
#sync-diff-inspector已集成在TiDB工具包中，直接下载TiDB工具包即可
shell> wget https://download.pingcap.org/tidb-community-toolkit-v6.4.0-linux-amd64.tar.gz
shell> tar zxvf tidb-community-toolkit-v6.4.0-linux-amd64.tar.gz
shell> ls -lh tidb-community-toolkit-v6.4.0-linux-amd64 | grep sync_diff_inspector
-rwxr-xr-x 1 tidb tidb  98M Nov 17 11:41 sync_diff_inspector
shell> ./sync_diff_inspector  -V
App Name: sync_diff_inspector v2.0
Release Version: v6.4.0
Git Commit Hash: f7e65073b35538def61ae094cd4a8e57e705344b
Git Branch: heads/refs/tags/v6.4.0
UTC Build Time: 2022-11-04 07:21:08
Go Version: go1.19.2
#### 三、sync-diff-inspector工具使用示例
1.配置文件通用部分
shell> cat config.toml
check-thread-count = 4             # 检查数据的线程数量
export-fix-sql = true              # 如果开启，若表数据存在不一致，则输出用于修复的SQL语句
check-struct-only = false          # 只对比表结构而不对比数据
[data-sources]                    
[data-sources.mysql1]              # 上游MySQL数据库配置（源端）
host = "10.186.65.57"          
port = 3306
user = "sgy"
password = "admin"
route-rules = ["rule1"]        # 映射匹配规则,通过配置相应的规则可以对单个、多个schema或table进行校验
# 如有多个rule时，可配置成 ["rule1", "rule2"]
[data-sources.mysql2]              # 下游MySQL数据库配置（目标端）
host = "10.186.65.89"
port = 3309
user = "sgy"
password = "admin"
2.基于schema的数据校验
- 对单个schema进行数据校验
#映射匹配规则部分,需要将此部分放到置配置文件通用部分的后面
[routes]                               # 映射关系,如上下游schema不同名可在此配置
[routes.rule1]
schema-pattern = "sbtest"          # 匹配上游数据库的的库名
target-schema = "sbtest"           # 匹配下游数据库的库名
[task]
output-dir = "./output"
source-instances = ["mysql1"]   # 上游数据库，内容是 data-sources 声明的唯一标识 id，分库分表场景下支持多个上游数据库，如：["mysql10", "mysql20"]
target-instance = "mysql2"      # 下游数据库，内容是 data-sources 声明的唯一标识 id
target-check-tables = ["sbtest.*"]    # 需要比对的下游数据库的表
# 进行数据校验
shell> ./sync_diff_inspector  --config=./config.toml
A total of 8 tables need to be compared
Progress [>------------------------------------------------------------] 0% 0/0
Comparing the table structure of ``sbtest`.`sbtest4`` ... equivalent     #表结构一致
Comparing the table structure of ``sbtest`.`sbtest5`` ... equivalent
.......................................................
Comparing the table data of ``sbtest`.`sbtest2`` ... equivalent          #表中数据一致
Comparing the table data of ``sbtest`.`sbtest8`` ... equivalent
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
A total of 8 table have been compared and all are equal.
You can view the comparision details through './output/sync_diff.log'
- 对多个schema进行数据校验
#由于对多个schema进行数据校验，routes包含了rule1、rule2,配置文件通用部分需要做以下修改
[data-sources.mysql1] 
route-rules = ["rule1","rule2"]
#映射匹配规则部分,需要将此部分放到置配置文件通用部分的后面
[routes]
[routes.rule1]
schema-pattern = "sbtest*"       #使用正则匹配sbtest开头的schema，如sbtest,sbtest1,sbtest2,sbtest3
target-schema = "sbtest*"
[routes.rule2]
schema-pattern = "sgy"           #匹配schema:sgy
target-schema = "sgy"
[task]
output-dir = "./output"
source-instances = ["mysql1"]     # 上游数据库，内容是 data-sources 声明的唯一标识 id，分库分表场景下支持多个上游数据库，如：["mysql10", "mysql20"]
target-instance = "mysql2"        # 下游数据库，内容是 data-sources 声明的唯一标识 id
target-check-tables = [ "sbtest*.*","sgy.*"]   #对源、目标实例中的sgy及以sbtest开头的schema所有表进行校验
#进行数据校验
shell> ./sync_diff_inspector --config=./config.toml
A total of 24 tables need to be compared
Progress [>------------------------------------------------------------] 0% 0/0
Comparing the table structure of ``sgy`.`sbtest2`` ... equivalent
Comparing the table data of ``sgy`.`sbtest2`` ... equivalent
.......................................................
Comparing the table data of ``sbtest`.`sbtest1`` ... equivalent
Comparing the table data of ``sbtest3`.`sbtest1`` ... equivalent
Comparing the table data of ``sbtest2`.`sbtest1`` ... equivalent
Comparing the table data of ``sbtest1`.`sbtest2`` ... equivalent
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
A total of 24 table have been compared and all are equal.
You can view the comparision details through './output/sync_diff.log'
3.基于table的数据校验
- 对单个table进行数据校验
#映射匹配规则部分,需要将此部分放到配置文件通用部分的后面
[routes]
[routes.rule1]
schema-pattern = "sbtest"
target-schema = "sbtest"
[task]
output-dir = "./output"
source-instances = ["mysql1"]      # 上游数据库，内容是 data-sources 声明的唯一标识 id，分库分表场景下支持多个上游数据库，如：["mysql10", "mysql20"] 
target-instance = "mysql2"         # 下游数据库，内容是 data-sources 声明的唯一标识 id
target-check-tables = ["sbtest.sbtest1"]      #只校验表：sbtest.sbtest1
#进行数据校验 
shell> ./sync_diff_inspector --config=./config.toml
A total of 1 tables need to be compared
Progress [>------------------------------------------------------------] 0% 0/0
Comparing the table structure of ``sbtest`.`sbtest1`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest1`` ... equivalent
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
A total of 1 table have been compared and all are equal.
You can view the comparision details through './output/sync_diff.log'
- 对多个table进行数据校验
#对schema进行数据校验也是对多个table进行数据校验的一种，这里以指定多个具体表名为例
#由于对多个table进行数据校验，routes包含了rule1、rule2,配置文件通用部分需要做以下修改
[data-sources.mysql1] 
route-rules = ["rule1","rule2"]
#映射匹配规则部分,需要将此部分放置到配置文件通用部分的后面
[routes]
[routes.rule1]
schema-pattern = "sbtest*"
target-schema = "sbtest*"
[routes.rule2]
schema-pattern = "sgy"
target-schema = "sgy"
[task]
output-dir = "./output"
source-instances = ["mysql1"]       # 上游数据库，内容是 data-sources 声明的唯一标识 id，分库分表场景下支持多个上游数据库，如：["mysql10", "mysql20"]
target-instance = "mysql2"          # 下游数据库，内容是 data-sources 声明的唯一标识 id
#只校验sbtest.sbtest8,sgy.sbtest4,sbtest1.sbtest1,sbtest2.sbtest2这四个表
target-check-tables = [ "sbtest.sbtest8","sgy.sbtest4","sbtest1.sbtest1","sbtest2.sbtest2"]
#进行数据校验 
shell> ./sync_diff_inspector --config=./config.toml
A total of 4 tables need to be compared
Progress [>------------------------------------------------------------] 0% 0/0
Comparing the table structure of ``sbtest2`.`sbtest2`` ... equivalent
Comparing the table data of ``sbtest2`.`sbtest2`` ... equivalent
Comparing the table structure of ``sgy`.`sbtest4`` ... equivalent
Comparing the table structure of ``sbtest1`.`sbtest1`` ... equivalent
Comparing the table data of ``sgy`.`sbtest4`` ... equivalent
Comparing the table data of ``sbtest1`.`sbtest1`` ... equivalent
Comparing the table structure of ``sbtest`.`sbtest8`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest8`` ... equivalent
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
A total of 4 table have been compared and all are equal.
You can view the comparision details through './output/sync_diff.log'
- 对单表进行范围校验
#映射匹配规则部分,需要将此部分放置到配置文件通用部分的后面
[routes]
[routes.rule1]
schema-pattern = "sbtest"
target-schema = "sbtest"
[task]
output-dir = "./output"
source-instances = ["mysql1"]      # 上游数据库，内容是 data-sources 声明的唯一标识 id，分库分表场景下支持多个上游数据库，如：["mysql10", "mysql20"]
target-instance = "mysql2"         # 下游数据库，内容是 data-sources 声明的唯一标识 id
target-check-tables = ["sbtest.sbtest1"]      # 指定校验目标实例上的sbtest.sbtest1表
target-configs = ["config1"]                  # 对部分表的额外配置
[table-configs.config1] 
target-tables = ["sbtest.sbtest1"]                # 指定校验目标实例上的sbtest.sbtest1表
range = "id > 10 AND id < 100"                    # 指定校验目标表的具体范围，相当于SQL中的where条件
#数据校验见数据修复功能部分
4.数据修复功能
#为了演示数据修复，在目标端表中删除一些数据
shell> mysql -usgy -padmin -h 10.186.65.89 -P 3309 -e "delete from sbtest.sbtest1 where id in (11,22,33,44,55,66,77,88,99);"
# 使用对单表进行范围校验配置，对sbtest.sbtest1表进行范围校验
shell> ./sync_diff_inspector  --config=./config.toml
A total of 1 tables need to be compared
Comparing the table structure of ``sbtest`.`sbtest1`` ... equivalent     #sbtest.sbtest1表结构一致
Comparing the table data of ``sbtest`.`sbtest1`` ... failure             #sbtest.sbtest1表数据有差异
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
The data of `sbtest`.`sbtest1` is not equal
The rest of tables are all equal.
The patch file has been generated in 
'output/fix-on-mysql2/'                 # 生成修复SQL输出到此目录
You can view the comparision details through './output/sync_diff.log'
# 查看输出修复SQL
shell> cat output/fix-on-mysql2/sbtest\:sbtest1\:0\:0-0\:0.sql 
-- table: sbtest.sbtest1
-- range in sequence: Full
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (11,50148,'69183965773-14680923687-92934799461-07606242492-78811530738-23241332728-92911647895-70477201282-85254929997-06214236905','33737501839-63208420999-35708593012-95906952636-68691055996');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (22,41538,'14140185946-16271766410-68340573738-46226480462-08989140676-29936780681-56784925909-45742390296-67137862436-18242076592','25112986220-19824650341-42825248958-70186905082-33867163574');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (33,50105,'48402160130-78797253227-05588677001-93556313541-39295466587-91364622063-58862572731-27837539373-64526858273-89372384747','72073637794-12055602042-16862397531-87496431032-85451396141');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (44,49917,'98096713237-15265478716-72025332919-62964308854-01270604715-12000922788-50929365082-43513513022-28543412388-57790852446','33907865533-62267179125-36062850111-84091551774-69847376840');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (55,50259,'68826640374-18002055907-53999869701-72145793168-90893177888-85273641163-24331745145-62755454379-79511152711-99618812770','02724012569-91405199011-30257626349-21678066897-42535351703');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (66,41995,'58396552954-26907336026-99506693837-77815822050-42927030403-40927779227-58101279219-11438233008-00344004393-35806649113','02348992414-65327666387-20632806790-74456238429-90933031209');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (77,49757,'73705207329-00308504929-05904865650-29498186065-09990420614-84131302024-40320022420-77358683577-34731688411-70665402097','92567035674-84728177369-79087155038-84461952379-45481760225');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (88,50497,'77112982215-98755241853-36424062009-45217742824-83650985380-60232607362-47569976121-30091332050-97996374956-97911403909','88977046077-43519705750-51246090615-77629911610-94055348738');
REPLACE INTO `sbtest`.`sbtest1`(`id`,`k`,`c`,`pad`) VALUES (99,49977,'63255973711-62890656114-72914458941-22277906368-32619356110-31219579310-16762665782-69578495131-76043317830-28240408380','08589883275-03392784968-00244590156-39735355951-95769933801');
#将生成的修复SQL导入目标库
shell> mysql -usgy -padmin -h 10.186.65.89 -P 3309 < output/fix-on-mysql2/sbtest\:sbtest1\:0\:0-0\:0.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
#再次检验,发现数据已经一致
shell> ./sync_diff_inspector  --config=./config.toml
A total of 1 tables need to be compared
Comparing the table structure of ``sbtest`.`sbtest1`` ... equivalent
Comparing the table data of ``sbtest`.`sbtest1`` ... equivalent
_____________________________________________________________________________
Progress [============================================================>] 100% 0/0
A total of 1 table have been compared and all are equal.
You can view the comparision details through './output/sync_diff.log'
#### 四、相关问题
- 修改配置文件后需要手动删除outputDir目录
shell> vim config.toml
shell> ./sync_diff_inspector --config=./config.toml     #将output-dir删除即可解决
Fail to initialize config.
failed to init Task: config changes breaking the checkpoint, please use another outputDir and start over again!
- 表建议使用utf8mb4字符集，不支持MySQL8.0的utf8mb3字符集
mysql> select @@version;
+-----------+
| @@version |
+-----------+
| 8.0.30    |
+-----------+
1 row in set (0.00 sec)
mysql> alter table sgy.sbtest4 CHARSET=utf8;
Query OK, 0 rows affected, 1 warning (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 1
mysql> show create table sgy.sbtest4 \G
*************************** 1. row ***************************
Table: sbtest4
Create Table: CREATE TABLE `sbtest4` (
`id` int NOT NULL AUTO_INCREMENT,
`k` int NOT NULL DEFAULT '0',
`c` char(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
`pad` char(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
PRIMARY KEY (`id`),
KEY `k_4` (`k`)
) ENGINE=InnoDB AUTO_INCREMENT=100001 DEFAULT CHARSET=utf8mb3     
1 row in set (0.00 sec)   
#执行数据校验时报错
shell> ./sync_diff_inspector --config=./config.toml
There is something error when initialize diff, please check log info in output/sync_diff.log
#查看日志文件
shell> cat output/sync_diff.log  |grep utf8mb3
[2023/02/19 11:13:04.980 +08:00] [FATAL] [main.go:120] ["failed to initialize diff process"] [error="get table sgy.sbtest4's information error [parser:1115]Unknown character set: 'utf8mb3'\ngithub.com/pingcap/errors.
更详细的使用说明，请参考 sync-diff-inspector 官方文档：https://docs.pingcap.com/zh/tidb/stable/sync-diff-inspector-overview