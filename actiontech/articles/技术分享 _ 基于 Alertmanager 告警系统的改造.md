# 技术分享 | 基于 Alertmanager 告警系统的改造

**原文链接**: https://opensource.actionsky.com/20220920-alertmanager/
**分类**: 技术干货
**发布时间**: 2022-09-26T21:42:29-08:00

---

作者：莫善
某互联网公司高级 DBA。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 一、引言
告警跟运维工作息息相关，一个好的告警系统不仅能提升运维的效率，还能提升相关人员的工作舒适度及生活质量。相反，如果告警系统比较拉胯，那运维的工作就比较难受了。比如，半夜收到无关痛痒的告警信息，又比如这个告警正在处理还一直在发，再比如同一时间产生很多告警，然后不重要的告警把重要的告警刷走了，等等。
本文想分享一下在使用Alertmanager的过程中遇到的一些困扰，以及分享一下最近在做的告警系统改造的项目，仅做经验交流。
#### 二、前期准备
我们线上采用Prometheus + Alertmanager的架构进行监控告警。所以本文主要是基于Alertmanager组件进行介绍。
alertmanager, version 0.17.0 (branch: HEAD, revision: c7551cd75c414dc81df027f691e2eb21d4fd85b2)  build user:       root@932a86a52b76  build date:       20190503-09:10:07  go version:       go1.12.4
##### 1、待处理问题
###### （1）告警干扰
因历史遗留问题，我们线上环境的环境是一个集群一个prometheus，然后共享一个告警通道Alertmanager，有时候会出现A集群的告警信息跑到B集群的告警中。比如会收到像下面这种情况：
cluster: clusterA
instance: clusterB Node
alert_name: xxx 
> 这个问题一直没找到原因，也没法稳定复现。
###### （2）告警升级
现在的告警系统在触发告警时候不会升级。比如优先发给值班人员，其次会根据接收人，告警时间，告警介质等进行升级。
> 关于告警升级后文有解释说明。
###### （3）告警恢复
对于已经恢复的告警，Alertmanager不会发送一份告警恢复的提示。
###### （4）告警抑制
Alertmanager针对重复的告警可以做到自定义时间进行抑制，但是不太智能，比如，同一个告警项，前面三次发送间隔短点，超过三次的间隔可以长点，比如第1，3，5，10，20，30分钟发送。另外也不能做到自适应时间抑制，比如工作时间抑制时间间隔可以长一点（同一个告警十分钟发一次），休息时间的抑制时间短一点（同一个告警五分钟发一次）。
###### （5）告警静默
Alertmanager支持告警静默功能，但是需要在Alertmanager平台进行配置。如果一个机器宕机后，可能触发很多告警需要静默，所以添加及事后删除静默规则的管理比较麻烦。
另外还有一个比较头疼的问题，正常通过告警页面可以点击【Silence】是可以将待静默的告警信息带到配置告警静默的页面，但是大部分时候都是不行的（空白页面），需要手动填写需要静默的告警信息，这就很头疼了。
###### （6）语音告警
Alertmanager目前不支持语音告警。
> 这个问题不做为单独的问题进行介绍，会放在告警升级部分。
##### 2、发现新问题
为了解决上述提到的【告警干扰】问题，我们采取的方法是将一个Alertmanager拆成多个（一个集群一个），这样能解决【告警干扰问题】，那么又带来了新的问题。
- 如何实现告警收敛？
- 如何管理告警静默？
###### （1）告警收敛
同一时刻产生多条告警，就会导致相关人员收到多条告警信息，这样即浪费告警资源，也对排查问题带来一定的干扰。比如单机多实例的场景，一台机器宕机，同时会产生好几十条告警，或者一个集群出现问题，所有节点都触发告警。针对这种场景如果没有告警收敛，会比较痛苦。
> Alertmanager本身支持收敛，因为我们需要解决【告警干扰】问题，所以我们改造的时候拆成了一个集群一个Alertmanager，这样我们环境就没法用自带的收敛功能了。
###### （2）告警静默
本来单个Alertmanager的告警静默就比较难管理了，如果多个告警项，可能是多个Alertmanager需要静默，静默的管理就更加麻烦了。
针对以上问题，下面会逐个介绍一下解决思路，部分解决方案不见得适合所有环境，其他环境或许有更好的解决方案，这里仅供参考。
#### 三、告警改造
##### 1、告警干扰问题
如前文所述，通过将一个Alertmanager拆成n个，这种方式看起来比较笨，但是却有效，如果有一个上帝视角将所有Alertmanager管理起来，就当作一个数据库实例去对待，其实也很方便。这类组件也不需要很多的系统资源，使用虚拟机完全够用。另外其实也有一个好处，加入说Alertmanager出现问题，比如进程正常，但是不会发告警了，这样也不至于团灭。
> 我们平台的监控、告警都已经实现自动化，并且都是通过平台进行管理，用一个Alertmanager跟多个，在部署安装上成本差不多，但是不太好管理（这个后文有说明）。
##### 2、告警升级问题
发送告警的介质主要分几种，邮件，企业微信（其他即时通讯工具），短信，电话/语音。从左到右成本依次增高，所以为了告警资源不被浪费，尽可能的节省短信/电话这种告警介质，所以我们希望我们的告警系统是能自适应的进行调整。这个升级分如下几个维度：
- 第一 告警介质的升级。邮件 &#8211;> 企业微信 &#8211;> 短信 &#8211;> 电话（同一个告警项发送超过3次就向上升级一个介质，具体可以根据需求定义）。
- 第二 告警接收人升级。一级 &#8211;> 二级 &#8211;> leader。
- 第三 按照时间升级。工作时间通过邮件/企业微信发送告警，工作时间之外通过短信/电话发送告警。
这个问题想通过Alertmanager来解决好像不可行，所以只能通过其他手段进行曲线救国了。我们采取的方式是开发一个脚本读取Alertmanager的告警信息，然后通过脚本进行发送告警信息。
> 其实也可以直接读取prometheus的告警信息，原理上差不太多。
Send a detailed message to the DBA by Mail     #只要是告警就会通过邮件告知
if now_time > 8 and now_time < 22 :
Send a simple message to the DBA by WX            
else                                           #按照告警时间升级告警介质
if alert_count > 3 and phone_count < 3 :
Send a simple simple message to the DBA by phone     #短信告警升级电话告警
elif alert_count > 3 and phone_count > 3 :
Send a simple message to the leader by phone  #接收告警人员升级
else
Send a simple message to the DBA by SMS       #告警介质升级
接受告警的人员包含值班DBA及项目负责人，如果接收告警的对象无法收到告警信息（联系方式异常，离职），就会读取通讯录获取一位同组的人员进行重新发送告警。
- 可以定义，多次告警后进行接收人员的告警升级，同理也可以定义告警时间，告警介质等告警升级。
- 只要是告警就会通过邮件告知，原因是短信/语音这种介质成本比较高，也不方便查阅，所以只会发送简单的告警提示，详细的需要查阅邮件。
##### 3、告警收敛/抑制问题
首先需要一个表来保存发送告警的记录，包含告警项（要求全局唯一，建议使用ip:port），告警状态，累计告警次数，最后告警时间，整个系统的好几个功能都需要这个表。
CREATE TABLE `tb_alert_for_task` (
`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
`alert_task` varchar(100) DEFAULT '' COMMENT '告警项目',
`alert_state` tinyint(4) NOT NULL DEFAULT '0' COMMENT '告警状态, 0表示已经恢复, 1表示正在告警',
`alert_count` int(11) NOT NULL DEFAULT '0' COMMENT '告警的次数, 单个告警项发送的告警次数是10次（每天至多发送十次）',
`u_time` datetime NOT NULL DEFAULT '2021-12-08 00:00:00' COMMENT '下一次发送告警的时间',
`alert_remarks` varchar(50) NOT NULL DEFAULT '' COMMENT '告警内容',
PRIMARY KEY (`id`),
UNIQUE KEY `uk_alert_task` (`alert_task`)
) ENGINE=InnoDB AUTO_INCREMENT=7049 DEFAULT CHARSET=utf8mb4;
通过查阅文档我们可以知道调用下面的告警信息api是可以获取当前告警信息。
api/v1/alerts?silenced=false&inhibited=false
一条告警信息长下面这样，我认为有用的就是【alertname】【cluster】【instance（主机部分）】这三个属性，可以将这三个属性作为收敛维度。
{
'labels': {
'alertname': 'TiDB_server_is_down',
'cluster': 'cluster_name_001',
'env': 'cluster_name_001',
'expr': 'probe_success{
group="tidb"
}==0',
'group': 'tidb',
'instance': '192.168.168.1:4000',
'job': 'tidb_port_probe',
'level': 'emergency',
'monitor': 'prometheus'
}
}
> 这里省略了其他信息，仅保留了labels部分
###### （1）抑制
抑制逻辑是下一次发送告警时间小于当前时间，或者告警发送次数大于10次。为什么是这个逻辑？这需要结合收敛部分的代码介绍，所以后面解释。
#这是抑制的逻辑, 将当前告警异常项都读出来, 如果当前alertmanager的告警已经在这里面就视为抑制对象, 因为这些告警还不满足再次发送的条件
select_sql = "select alert_task from tb_tidb_alert_for_task where alert_state = 1 and (u_time > now() or alert_count > 10);"
state, skip_instance = connect_mysql(opt = "select", sql = {"sql" : select_sql})
> skip_instance是个列表，在遍历告警信息的时候会用到，如果在这个列表里面就忽略这个告警，以此起到抑制的效果。
###### （2）收敛
收敛思路大概是这样，遍历每一条告警信息，遍历的时候会在【tb_tidb_alert_for_task】表记录一条记录，包含：
- instance信息，这是全局唯一。
- 告警状态，区别是正在告警，还是已经恢复告警，恢复告警的时候用到。
- 发送告警次数，这个值会作为收敛参考数据。
- 下一次发送告警时间，这是方便处理抑制。
next_time = 0
if now_time > 8 and now_time < 22 :
next_time = max_alert_count * 2 + 1
else : 
next_time = max_alert_count
insert_sql[instance_name] = """replace into tb_tidb_alert_for_task(alert_task,alert_state,alert_count,u_time,alert_remarks)
select '""" + instance_name + """',1,""" + str(max_alert_count) + """, date_add(now(), INTERVAL + """ + str(next_time) + """ MINUTE),
'tidb集群告警';"""
state, _ = connect_mysql(opt = "insert", sql = insert_sql)
上面这部分逻辑是服务于抑制功能，所以可以解释的通，上文将下一次发送告警时间要求小于当前时间。
- 工作时间，发送一次告警后，下一次告警时间是间隔 2n+1 min(n表示告警次数)。
- 非工作时间，发送一次告警后，下一次告警时间是间隔 n+1 min(n表示告警次数)
下面这部分逻辑是遍历Alertmanager的所有处于active状态的告警信息，然后做分析处理。
def f_get_alert_to_msg(url) :
try :
res = json.loads(requests.get(url, headers = header, timeout = 10).text) #读取alertmanager的告警状态
except Exception as err :
return {"code" : 1, "info" : str(err)}
for temp in res["data"] : 
cluster_name = temp["labels"]["cluster"]
alert_name = temp["labels"]["alertname"]
instance_name = cluster_name + ":all"  #特殊情况没有instance信息，这种时候是集群告警，而不是某个节点告警
if "instance" in temp["labels"] : instance_name = temp["labels"]["instance"]
if len(global_instance_list) == 0 : global_instance_list = []
if len(instance_name) > 0 : global_instance_list.append(instance_name)     #这个列表在判断是否是告警已经恢复用到
if instance_name in skip_instance : continue # 符合抑制条件就忽略这个告警
if cluster_name not in global_alert_cluster.keys() :     global_alert_cluster[cluster_name] = {}
if alert_name not in global_alert_name.keys() :     global_alert_name[alert_name] = {}
if instance[0] not in global_alert_host.keys() :     global_alert_host[instance[0]] = {}
if alert_name not in global_alert_cluster[cluster_name].keys() :     global_alert_cluster[cluster_name][alert_name] = []
if cluster_name not in global_alert_name[alert_name].keys() :     global_alert_name[alert_name][cluster_name] = []
if alert_name not in global_alert_host[instance[0]].keys() :     global_alert_host[instance[0]][alert_name] = []
if instance_name not in global_alert_cluster[cluster_name][alert_name] :     global_alert_cluster[cluster_name][alert_name].append(instance_name)
if instance_name not in global_alert_name[alert_name][cluster_name] :     global_alert_name[alert_name][cluster_name].append(instance_name)
if cluster_name + ":" + instance[1] not in     global_alert_host[instance[0]][alert_name] :     global_alert_host[instance[0]][alert_name].append(cluster_name + ":" +     instance[1])
return {"code" : 0, "info" : "ok"}
> 将【alertname】【cluster】【instance】分别保存到【global_alert_name】【global_alert_cluster】【global_alert_host】这三个字典。
下面这个逻辑是遍历alertmanager的url，根据url去扫对应的alertmanager的告警信息，可以看到代码中有一个判断Alertmanager状态的代码，可以起到监控Alertmanager的作用，会将访问异常的发送出来。
for url in url_list :
status = f_get_alert_to_msg(url) #读取alertmanager告警信息
if status == 1 :
error_list.append(url)
if len(error_list) > 0 : 
info = "Alertmanager访问异常 : " + ",".join(error_list)
status = f_alert_sms_to_user(tel,info)
最终根据【global_alert_name】【global_alert_cluster】【global_alert_host】三个字典的长度判断以哪个维度进行收敛，即哪个字典最短就以哪个维度为收敛对象。
if len(global_alert_cluster.keys()) < len(global_alert_host.keys()) and len(global_alert_cluster.keys()) < len(global_alert_name.keys()) :
alert = global_alert_cluster
info_tmp = "告警集群 : "
elif len(global_alert_name.keys()) < len(global_alert_host.keys()) :
alert = global_alert_name
info_tmp = "告警名称 : "
else :
alert = global_alert_host
info_tmp = "告警主机 : "
##### 4、告警恢复问题
#读取告警状态是1, 且比当前时间还早的条目
sql = """select alert_task from tb_tidb_alert_for_task
where alert_state = 1 and alert_remarks = 'tidb集群告警' and u_time < date_add(now(), INTERVAL - 1 MINUTE);"""
state, alert_instance = connect_mysql(opt = "select", sql = {"sql" : sql})
alert_ok = []
for instance in alert_instance :
if instance not in global_instance_list : #global_instance_list是在遍历告警信息的时候记录了所有instance信息
alert_ok.append(instance)
update_sql[instance] = """update tb_tidb_alert_for_task set alert_state = 0, alert_count = 0
where alert_state = 1 and alert_remarks = 'tidb集群短信告警' and alert_task = '""" + instance + """';"""
state, _ = connect_mysql(opt = "update", sql = update_sql)
> 如果表里处在告警状态的记录不在当前正在告警的列表中，就说明告警已经恢复，这时候就会变更告警状态，且将告警次数置为0。
##### 5、告警静默问题
###### （1）添加静默
/api/v1/silences
try :
expi_time = int(expi_time)  #小时
except Exception as err :
return {"code" : 1, "info" : str(err)}
if expi_time > 24 :
return {"code" : 1, "info" : "The alarm cannot be silent for more than 24 hours"}
local_time = f_get_time()   #当前时间2022-01-01 00:00:00
local_time = dt.datetime.strptime(local_time,'%Y-%m-%d %H:%M:%S') 
start_time = local2utc(local_time).strftime("%Y-%m-%dT%H:%M:%S.000Z") #换成UTC时间
end_time = dt.datetime.strptime(((dt.datetime.now() - timedelta(hours = -expi_time)).strftime("%Y-%m-%d %H:%M:%S")),"%Y-%m-%d %H:%M:%S")
end_time = local2utc(end_time).strftime("%Y-%m-%dT%H:%M:%S.000Z")
dic = {
"id"        : "",
"createdBy" : user,
"comment"   : comment,
"startsAt"  : start_time ,
"endsAt"    : end_time,
"matchers"  : [
{
"name"  : name,
"value" : value
}
]
}
try :
res = json.loads(requests.post(url, json = dic).text)
except Exception as err :
res = {"code" : 1, "info" : str(err)}
return res
这里需要注意，添加静默一定需要让用户提供静默超时时间，比如2h，上限是24小时，这样可以避免因时间过长，然后遗忘规则，导致告警一直被静默。
另外用户提供的是静默小时数，而添加静默是需要一个开始时间和结束时间，且需要UTC时间，所以需要通过计算特殊处理一下。
最后还需要注意，这里添加静默是单一规则，即只有一个name-value对，不支持与条件及正则。如果需要多个条件可以追加matchers列表的值。
"matchers"  : [
{
"name"  : name1,
"value" : value1
},
{
"name"  : name2,
"value" : value2
}
]
###### （2）删除静默
这部分需要用到两个api，第一个是先获取规则id，通过id进行删除。
/api/v1/silences?silenced=false&inhibited=false
/api/v1/silence/id
url = "http://xxx/api/v1/silences?silenced=false&inhibited=false"
try :
id_info = json.loads(requests.get(url).text)
except Exception as err :
return {"code" : 1, "info" : str(err)}
for item in id_info["data"] :
if item["status"]["state"] != "active" : continue  #非active状态的直接忽略
if item["matchers"][0]["name"] != name or item["matchers"][0]["value"] != value : continue #不满足条件的也直接忽略
try : #先要获取id才能进行删除规则
url = "http://xxx/api/v1/silence/" + item["id"]
res = json.loads(requests.delete(url).text)
except Exception as err : #访问失败
res = {"code" : 1, "info" : str(err)}
return res
可以看到告警静默的管理还是比较麻烦的，所以我们已经将这部分管理功能整合到平台，可以通过平台的告警管理列表页进行告警静默的管理，可以通过ip，instance，cluster，role，alert_name这几个维度进行管理，也支持告警信息展示，可以通过展示页面逐个告警添加静默，也可以将所有告警一键静默，这样就解决了告警静默难管理的问题。
#### 四、注意事项
- 如果没有平台进行管理，不建议使用这样的方式运维告警系统。
- 添加告警静默的时候强烈建议添加超时时间，且不宜过长，避免添加后遗忘。
- 添加静默的时候一定要做到心里有数，避免出现故障告警被顺带添加静默而又未进行处理的情况。
#### 五、写在最后
本文所有内容仅供参考，因各自环境不同，并非通用方案，且在使用文中代码时可能碰上未知的问题。如有线上环境操作需求，请在测试环境充分测试。