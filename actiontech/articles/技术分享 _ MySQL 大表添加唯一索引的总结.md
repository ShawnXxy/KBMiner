# 技术分享 | MySQL 大表添加唯一索引的总结

**原文链接**: https://opensource.actionsky.com/20230302-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-03-05T22:05:58-08:00

---

作者：莫善
某互联网公司高级 DBA。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 1 前言
在数据库的运维工作中经常会遇到业务的改表需求，这可能是DBA比较头疼的需求，其中添加唯一索引可能又是最头疼的需求之一了。
MySQL 5.6 开始支持 Online DDL，添加[唯一]索引虽然不需要重建表，也不阻塞DML，但是大表场景下还是不会直接使用Alter Table进行添加，而是使用第三方工具进行操作，比较常见的就属pt-osc和gh-ost了。本文就来总结梳理一下添加唯一索引的相关内容。
> 本文对ONLINE DDL讨论的也是基于MySQL 5.6及以后的版本。
#### 2 添加唯一索引的方案简介
> 这部分内容仅介绍ONLINE DDL、pt-osc和gh-ost三种方案，且仅做简单介绍，更加详细的内容请参考官方文档。
##### 2.1 ONLINE DDL
首先我们看一下官方对添加索引的介绍：
| Operation | In Place | Rebuilds Table | Permits Concurrent DML | Only Modifies Metadata |
| --- | --- | --- | --- | --- |
| Creating or adding a secondary index | Yes | No | Yes | No |
> 唯一索引属于特殊的二级索引，将引用官方介绍添加二级索引的内容做例子。
可以看到ONLINE DDL采用In Place算法创建索引，添加索引是不阻塞DML，大致流程如下：
- 同步全量数据。遍历主键索引，将对应的字段（多字段）值，写到新索引。
- 同步增量数据。遍历期间将修改记录保存到Row Log，等待主键索引遍历完毕后回放Row Log。
> 也不是完全不阻塞DML，在Prepare和Commit阶段需要获取表的MDL锁，但Execute阶段开始前就已经释放了MDL锁，所以不会阻塞DML。在没有大查询的情况下，持锁时间很短，基本可以忽略不计，所以强烈建议改表操作时避免出现大查询。
由此可见，表记录大小影响着加索引的耗时。如果是大表，将严重影响从库的同步延迟。好处就是能发现重复数据，不会丢数据。
##### 2.2 pt-osc
# ./pt-online-schema-change --version
pt-online-schema-change 3.0.13
# 
- 创建一张与原表结构一致的新表，然后添加唯一索引。
- 同步全量数据。遍历原表，通过【INSERT IGNORE INTO】将数据拷贝到新表。
- 同步增量数据。通过触发器同步增量数据。
| 触发器 | 映射的SQL语句 |
| --- | --- |
| INSERT 触发器 | REPLACE INTO |
| UPDATE 触发器 | DELETE IGNORE + REPLACE INTO |
| DELETE 触发器 | DELETE IGNORE |
由此可见，这个方式不会校验数据的重复值，遇到重复的数据后，如果是同步全量数据就直接忽略，如果是同步增量数据就覆盖。
这个工具暂时也没有相关辅助功能保证不丢数据或者在丢数据的场景下终止添加唯一索引操作。
> pt-osc有个参数【&#8211;check-unique-key-change】可以禁止使用该工具添加唯一索引，如果不使用这个参数就表示允许使用pt-osc进行添加索引，当遇到有重复值的场景，好好谋划一下怎么跑路吧。
##### 2.3 gh-ost
# ./bin/gh-ost --version
1.1.5
# 
- 创建一张与原表结构一致的新表，然后添加唯一索引。
- 同步全量数据。遍历原表，通过【INSERT IGNORE INTO】将数据拷贝到新表。
- 同步增量数据。通过应用原表DML产生的binlog同步增量数据。
| binlog语句 | 映射的SQL语句 |
| --- | --- |
| INSERT | REPLACE INTO |
| UPDATE | UPDATE |
| DELETE | DELETE |
由此可见，这个方式也不会校验数据的重复值，遇到重复的数据后，如果是同步全量数据就直接忽略，如果是同步增量数据就覆盖。
值得一提的是，这个工具可以通过hook功能进行辅助，以此保证在丢数据的场景下可以直接终止添加唯一索引操作。
> hook功能后文会着重介绍。
##### 2.4 小总结
由上述介绍可知，各方案都有优缺点
| 方案 | 是否丢数据 | 建议 |
| --- | --- | --- |
| ONLINE DDL | 不丢数据 | 适合小表，及对从库延迟没要求的场景 |
| pt-osc | 可能丢数据，无辅助功能可以避免丢数据的场景 | 不适合添加唯一索引 |
| gh-ost | 可能丢数据，有辅助功能可以避免部分丢数据的场景 | 适合添加唯一索引 |
#### 3 添加唯一索引的风险
根据上面的介绍可以得知gh-ost是比较适合大表加唯一索引，所以这部分就着重介绍一下gh-ost添加唯一索引的相关内容，主要是希望能帮助大家避坑。
> 如果业务能接受从库长时间延迟，也推荐ONLINE DDL的方案。
##### 3.1 风险介绍
我们都知道使用第三方改表工具添加唯一索引存在丢数据的风险，总结起来大致可以分如下三种：
> 文中出现的示例表的id字段默认是主键。
- 第一，新加字段，并对该字段添加唯一索引。
| id | name | age |
| --- | --- | --- |
| 1 | 张三 | 22 |
| 2 | 李四 | 19 |
| 3 | 张三 | 20 |
alter table t add addr varchar(20) not null default '北京',add unique key uk_addr(addr); #注意这里是不允许为空
如果这时候使用gh-ost执行上述需求，最后只会剩下一条记录，变成下面这样。
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
- 第二，原表存在重复值，如下数据表。
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
| 2 | 李四 | 19 | 广州 |
| 3 | 张三 | 20 | 深圳 |
alter table t add unique key uk_name(name);
如果这时候使用gh-ost执行上述需求，id=3这行记录就会被丢弃，变成下面这样。
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
| 2 | 李四 | 19 | 广州 |
- 第三，改表过程中新写（包含更新）的数据出现重复值。
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
alter table t add unique key uk_name(name);
如果这时候使用gh-ost执行上述需求，在拷贝原表数据期间，业务端新增一条如下面INSERT语句的记录。
insert into t(name,age,addr) values('张三',22,'北京');
这时候，id=1这行记录就会被新增的记录覆盖，变成下面这样
| id | name | age | addr |
| --- | --- | --- | --- |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
| 4 | 张三 | 22 | 北京 |
##### 3.2 风险规避
- 新加字段，并对该字段添加唯一索引的风险规避
针对这类场景，规避方式可以禁止【添加唯一索引与其他改表动作】同时使用。最终，将风险转移到了上述的第二种场景（原表存在重复值）。
> 如果是工单系统，在前端审核业务提交的SQL是否只有添加唯一索引操作，不满足条件的SQL工单不允许提交。
- 原表存在重复值的风险规避
针对这类场景，规避方式可以采用hook功能辅助添加唯一索引，在改表前先校验待添加唯一索引的字段的数据唯一性。
- 改表过程中新写（包含更新）的数据出现重复值的风险规避
针对这类场景，规避方式可以采用hook功能添加唯一索引，在全量拷完切表前校验待添加唯一索引的字段的数据唯一性。
#### 4 添加唯一索引的测试
##### 4.1 hook功能
gh-ost支持hook功能。简单来理解，hook是gh-ost工具跟外部脚本的交互接口。使用起来也很方便，根据要求命名脚本名且添加执行权限即可。
> 具体使用请看官方文档 https://github.com/github/gh-ost/blob/f334dbde5ebbe85589363d369ee530e3aa1c36bc/doc/hooks.md
##### 4.2 hook使用样例
这个样例是网上找的，可能很多小伙伴都在用。
（1）创建hook目录
mkdir /tmp/hook
cd /tmp/hook
（2）改表前执行的hook脚本
vim gh-ost-on-rowcount-complete-hook
#!/bin/bash
echo "$(date '+%F %T') rowcount-complete schema:$GH_OST_DATABASE_NAME.$GH_OST_TABLE_NAME before_row:$GH_OST_ESTIMATED_ROWS"
echo "$GH_OST_ESTIMATED_ROWS" > /tmp/$GH_OST_DATABASE_NAME.$GH_OST_TABLE_NAME.txt
（3）全量拷贝完成后执行的hook脚本
vim gh-ost-on-row-copy-complete-hook
#!/bin/bash
echo "时间: $(date '+%F %T') 库表: $GH_OST_DATABASE_NAME.$GH_OST_TABLE_NAME 预计总行数: $GH_OST_ESTIMATED_ROWS 拷贝总行数: $GH_OST_COPIED_ROWS"
if [[ `cat /tmp/$GH_OST_DATABASE_NAME.$GH_OST_TABLE_NAME.txt` -gt $GH_OST_COPIED_ROWS ]];then
echo '拷贝总行数不匹配，修改失败，退出.'
sleep 5
exit -1
fi
（4）添加对应权限
chmod +x /tmp/hook/*
（5）使用
在gh-ost命令添加如下参数即可。
--hooks-path=/tmp/hook
这个hook的工作流程大概如下：
- 改表前先执行【gh-ost-on-rowcount-complete-hook】脚本获取当前表的记录数【GH_OST_ESTIMATED_ROWS】，并保存到【GH_OST_DATABASE_NAME.GH_OST_TABLE_NAME.txt】文件
- 原表全量数据拷贝完成后执行【gh-ost-on-row-copy-complete-hook】脚本，获取实际拷贝的记录数【GH_OST_COPIED_ROWS】，然后和【GH_OST_DATABASE_NAME.GH_OST_TABLE_NAME.txt】文件存的值做比较，如果实际拷贝的记录数小，就视为丢数据了，然后就终止改表操作。反之就视为没有丢数据，可以完成改表。
其实这个hook是存在风险的：
- 第一，如果改表过程中原表有删除操作，那么实际拷贝的行数势必会比【GH_OST_DATABASE_NAME.GH_OST_TABLE_NAME.txt】文件保存的值小，所以会导致改表失败。这种场景对我们来说体验十分不友好，只要改表过程中目标表存在【DELETE】操作，就会导致添加唯一索引操作失败。
> 关于这个问题，之前跟这个hook用例的原作者沟通过，他是知晓这个问题的，并表示他们的业务逻辑是没有删除【DELETE】操作，所以不会有影响。
- 第二，如果改表过程中，新加一条与原表的记录重复的数据，那么这个操作不会影响【GH_OST_COPIED_ROWS】的值，最终会改表成功，但是实际会丢失数据。
有小伙伴可能会疑问，上述【gh-ost-on-row-copy-complete-hook】脚本中，为什么不用【GH_OST_ESTIMATED_ROWS】的值与【GH_OST_COPIED_ROWS】比较？
首先我们看一下【GH_OST_ESTIMATED_ROWS】的值是怎么来的。
GH_OST_ESTIMATED_ROWS := atomic.LoadInt64(&this.migrationContext.RowsEstimate) + atomic.LoadInt64(&this.migrationContext.RowsDeltaEstimate)
可以看到【GH_OST_ESTIMATED_ROWS】是预估值，只要原表在改表过程中有DML操作，该值就会变化，所以不能用来和【GH_OST_COPIED_ROWS】作比较。
> hook实现逻辑请参考 https://github.com/github/gh-ost/blob/master/go/logic/hooks.go
##### 4.3 加强版 hook 样例
上面的hook样例虽然存在一定的不足，但是也给我提供了一个思路，知道有这么个辅助功能可以规避添加唯一索引引发丢数据的风险。
受这个启发，并查阅了官方文档后，我整理了个加强版的hook脚本，只需要一个脚本就能避免上述存在的几种问题。
按说应该是两个脚本，且代码一致即可。
- 改表前先校验一次原表是否存在待添加唯一索引的字段的数据是否是唯一的，如果不满足唯一性就直接退出添加唯一索引。
- 切表前再校验一次，但是我们环境是在代码里面做了校验，在业务提交工单后直接先判断唯一性，然后再处理后续的逻辑，所以第一个校验就省略了（改表工单代码代替hook校验）。
vim gh-ost-on-before-cut-over
> 这表示在切表前需要执行的hook脚本，即：切表前检查一下唯一索引字段的数据是否有重复值，这样避免改表过程中新增的数据跟原来的有重复。
#!/bin/bash
work_dir="/opt/soft/zzonlineddl"                                  #工作目录
. ${work_dir}/function/log/f_logging.sh                           #日志模块
if [ -f "${work_dir}/conf/zzonlineddl.conf" ]
then
. ${work_dir}/conf/zzonlineddl.conf                           #改表项目的配置文件
fi
log_addr='${BASH_SOURCE}:${FUNCNAME}:${LINENO}' #eval echo ${log_addr}
#针对该改表任务生成的配置文件
#里面保存的是这个改表任务的目标库的从库连接信息【mysql_comm】变量的值
#还有数据唯一性的校验SQL【mysql_sql】变量的值
hook_conf="${work_dir}/hook/conf/--mysql_port--_${GH_OST_DATABASE_NAME}.${GH_OST_TABLE_NAME}"  
. ${hook_conf}
function f_main()
{
count_info="$(${mysql_comm} -NBe "${mysql_sql}")"
count_total="$(awk -F: '{print $NF}' <<< "${count_info}")"
f_logging "$(eval echo ${log_addr}):INFO" "库表: ${GH_OST_DATABASE_NAME}.${GH_OST_TABLE_NAME} 原表预计总行数: ${GH_OST_ESTIMATED_ROWS}, 实际拷贝总行数: ${GH_OST_COPIED_ROWS}"
if [ -z "${count_total}" ]
then
f_logging "$(eval echo ${log_addr}):ERROR" "唯一索引字段数据唯一性检查异常, 终止改表操作"
exit -1
fi
mark=""
for count in $(echo "${count_info}"|tr ":" " ")
do
if [ -n "${count}" ] && [ "${count}x" == "${count_total}x" ]
then
[ "${mark}x" == "x" ] && mark="true"
else 
mark="false"
fi
done
if [ "${mark}x" == "truex" ]
then
f_logging "$(eval echo ${log_addr}):INFO" "唯一索引字段数据唯一性正常, 允许切表"
else 
f_logging "$(eval echo ${log_addr}):ERROR" "唯一索引字段数据唯一性检测到可能丢失数据, 终止改表操作"
exit -1
fi
exit 0
}
f_main
> 该脚本非通用版，仅供参考。
hook_conf变量的值是这样的，由改表平台根据业务的SQL语句自动生成。
mysql_comm='mysql -h xxxx -P xxxx -u xxxx -pxxxx db_name'   #这里是从库的地址
mysql_sql="select concat(count(distinct rshost,a_time),':',count(*)) from db.table"
> 其中检查唯一性的SQL可以使用如下的命令生成，仅供参考。
alter="alter table t add unique key uk_name(name,name2),add unique key uk_age(age);"
echo "${alter}"|awk 'BEGIN{ FS="(" ; RS=")";print "select concat(" } 
NF>1 { print "count(distinct "$NF"),'\'':'\''," }
END{print "count(*)) from t;"}'|tr -d '\n'
执行上面的命令会根据业务提交的添加唯一索引的SQL得到一条检查字段数据唯一性的SQL。
select concat(count(distinct name,name2),':',count(distinct age),':',count(*)) from t;
需要注意的是，这个加强版的hook也不能100%保证一定不会丢数据，有两种极端情况还是会丢数据。
- 第一，如果是大表，在执行【gh-ost-on-before-cut-over】脚本过程中（大表执行这个脚本时间较长），新增的记录跟原来数据有重复，这个就没法规避了。
- 第二，在改表过程中，如果业务新增一条与原数据重复的记录，然后又删除，这种场景也会导致丢数据。
针对第二个场景可能有点抽象，所以举一个具体的例子，原表数据如下：
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
> 现在对name字段添加唯一索引。
假如现在正在使用gh-ost进行添加唯一索引，这时候业务做了下面几个操作：
（1）新增一条记录
insert into t(name,age,addr) values('张三',22,'北京');
这时候原表的数据就会变成像下面这样。
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
| 4 | 张三 | 22 | 北京 |
这时候新表的数据就会变成像下面这样。
| id | name | age | addr |
| --- | --- | --- | --- |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
| 4 | 张三 | 22 | 北京 |
> id=1和id=4是两条重复的记录，所以id=1会被覆盖掉。
（2）删除新增的记录
业务新增记录后意识到这条数据是重复的，所以又删除新增这条记录。
delete from t where id = 4;
这时候原表的数据就会变成像下面这样。
| id | name | age | addr |
| --- | --- | --- | --- |
| 1 | 张三 | 22 | 北京 |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
这时候新表的数据就会变成像下面这样。
| id | name | age | addr |
| --- | --- | --- | --- |
| 2 | 李四 | 19 | 广州 |
| 3 | 王五 | 20 | 深圳 |
> 可以发现，这时候如果发生切表，原表id=1的记录将会丢失，而且这种场景hook的脚本没法发现，它检查原表的name字段的数据唯一性是正常的。
针对上述两种极端场景，发生的概率应该是极低的，目前我也没想到什么方案解决这两个场景。
gh-ost官方文档上说&#8211;test-on-replica参数可以确保不会丢失数据，这个参数的做法是在切表前停掉从库的复制，然后在从库上校验数据。
gh-ost comes with built-in support for testing via --test-on-replica: 
it allows you to run a migration on a replica, such that at the end of the migration gh-ost would stop the replica, swap tables, reverse the swap, and leave you with both tables in place and in sync, replication stopped.
This allows you to examine and compare the two tables at your leisure.
> https://github.blog/2016-08-01-gh-ost-github-s-online-migration-tool-for-mysql/#testable Testable部分（Testable不是书写错误）
很明显，这个方式还是没法解决在实际切表那一刻保证数据不会丢，就是说切表和校验之间一定是存在时间差，这个时间差内出现新写入重复数据是没法发现的，而且大表的这个时间差只会更大。
另外停掉从库的复制很可能也存在风险，很多业务场景是依赖从库进行读请求的，所以要慎用这个功能。
#### 5 总结
- 如果业务能接受，可以不使用唯一索引。将添加唯一索引的需求改成添加普通二级索引，这样就可以避免加索引导致数据丢失。
存储引擎读写磁盘，是以页为最小单位进行。唯一索引较于普通二级索引，在性能上并没有多大优势。相反，可能还不如普通二级索引。
- 在读请求上，唯一索引和普通二级索引的性能差异几乎可以忽略不计了。
- 在写请求上，普通二级索引可以使用到【Change Buffer】，而唯一索引没法用到【Change Buffer】，所以唯一索引会差于普通二级索引。
- 一定要加唯一索引的话，可以跟业务沟通确认是否能接受从库长时间延迟。如果能接受长时间延迟，可以优先使用ONLINE DDL进行添加唯一索引（小表直接用ONLINE DDL即可）。
- 如果使用第三方工具添加唯一索引，要优先使用gh-ost（配上hook），添加之前一定要先检查待加唯一索引字段的唯一性，避免因为原表存在重复值而导致丢数据。
强烈建议不要马上删除【old】表，万一碰到极端场景导致丢数据了，还可以通过【old】表补救一下。
- pt-osc 建议添加【&#8211;no-drop-old-table】参数
- gh-ost 不建议添加【&#8211;ok-to-drop-table】参数
#### 6 写在最后
本文对MySQL大表添加唯一索引做了一下总结，分享了一些案例和经验。
总体来说添加唯一索引是存在一定的风险的，各公司的业务场景也不一样，需求也不同，还可能碰上其他未知的问题，本文所有内容仅供参考。