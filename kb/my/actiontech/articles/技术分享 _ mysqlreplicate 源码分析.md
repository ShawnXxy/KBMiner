# 技术分享 | mysqlreplicate 源码分析

**原文链接**: https://opensource.actionsky.com/20220823-mysql/
**分类**: MySQL 新特性
**发布时间**: 2022-08-22T21:55:44-08:00

---

作者：王向
爱可生 DBA 团队成员，负责公司 DMP 产品的运维和客户 MySQL 问题的处理。擅长数据库故障处理。对数据库技术和 python 有着浓厚的兴趣。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 目录
- mysqlreplicate介绍
- 使用方法
- mysqlreplicate源码分析
第一步：检查重要参数的唯一性
检查server_id唯一性
- 检查uuid_id唯一性
- 第二步：检查InnoDB兼容性
- 第三步：检查存储引擎一致性
- 第四步：检查master binary logging
- 第五步：创建复制
- 步骤梳理
#### mysqlreplicate 介绍
> his utility permits an administrator to setup and start replication from one server (the master) to another (the slave). The user provides login information for the slave and connection information for connecting to the master. It is also possible to specify a database to be used to test replication.
The utility reports conditions where the storage engines on the master and the slave differ for older versions of the server. It also reports a warning if the InnoDB storage engine type (plugin verus built-in) differs on the master and slave. For InnoDB to be the same, both servers must be running the same &#8220;type&#8221; of InnoDB (built-in or the InnoDB Plugin), and InnoDB on both servers must have the same major and minor version numbers and enabled state.
By default, the utility issues warnings for mismatches between the sets of storage engines, the default storage engine, and the InnoDB storage engine. To produce errors instead, use the &#8211;pedantic option, whichrequires storage engines to be the same on the master and slave.
The -vv option displays any discrepancies between the storage engines and InnoDB values, with or without the&#8211;pedantic option.
Replication can be started using one of the following strategies.
就是可以使用一条命令快速创建从库环境
#### 使用方法
最常用的方式：
mysqlreplicate \
--master=root:123@10.186.65.20:3306 \
# user[:passwd]@host[:port][:socket]
--slave=root:123@10.186.65.119:3306 \
--rpl-user=rpl:rpl \
# user[:password]
-vv \
# 详细输出
--pedantic
# Fail if both servers do not have the same set of storage engines, the same default storage engine, and the same InnoDB storage engine.
指定 pos 点：
The following command starts replication from the beginning of a specific master binary log file:
shell> mysqlreplicate --master=root@localhost:3306 \
--slave=root@localhost:3307 --rpl-user=rpl:rpl \
--master-log-file=my_log.000003
# master on localhost: ... connected.
# slave on localhost: ... connected.
# Checking for binary logging on master...
# Setting up replication...
# ...done.
The following command starts replication from specific master binary log coordinates (specific log file and
position):
shell> mysqlreplicate --master=root@localhost:3306 \
--slave=root@localhost:3307 --rpl-user=rpl:rpl \
--master-log-file=my_log.000001 --master-log-pos=96
# master on localhost: ... connected.
# slave on localhost: ... connected.
# Checking for binary logging on master...
# Setting up replication...
# ...done.
[root@wx-super ~]# mysqlreplicate --master=root:123@10.186.65.20:3306 --slave=root:123@10.186.65.119:3306 --rpl-user=rpl:rpl -vv --pedantic
WARNING: Using a password on the command line interface can be insecure.
# master on 10.186.65.20: ... connected.
# slave on 10.186.65.119: ... connected.
# master id = 159197357
#  slave id = 567719145
# master uuid = fec2b773-1850-11ec-9db1-02000aba4114
#  slave uuid = f2743970-1850-11ec-ab78-02000aba4177
# Checking InnoDB statistics for type and version conflicts.
# Checking storage engines...
# Checking for binary logging on master...
# Setting up replication...
# Connecting slave to master...
# CHANGE MASTER TO MASTER_HOST = '10.186.65.20', MASTER_USER = 'rpl', MASTER_PASSWORD = 'rpl', MASTER_PORT = 3306, MASTER_AUTO_POSITION=1
# Starting slave from master's last position...
# IO status: Waiting for master to send event
# IO thread running: Yes
# IO error: None
# SQL thread running: Yes
# SQL error: None
# ...done.
#### mysqlreplicate 源码分析
##### 第一步：检查重要参数的唯一性
**检查 server_id 唯一性**
# Create an instance of the replication object
rpl = Replication(master, slave, rpl_options)
errors = rpl.check_server_ids() # 检查主服务器和从服务器的id 
for error in errors:
# 1.master_server_id不能等于0
# 2.slave_server_id不能等于0
# 3.master_server_id不能等于slave_server_id
print error
# Check for server_id uniqueness
if verbosity > 0:
print "# master id = %s" % master.get_server_id()
print "#  slave id = %s" % slave.get_server_id()
# check_server_ids方法解析
def check_server_ids(self):
master_server_id = self.master.get_server_id() # 内部封装其实是执行SHOW VARIABLES LIKE 'server_id'的结果
slave_server_id = self.slave.get_server_id()
if master_server_id == 0:
raise UtilRplError("Master server_id is set to 0.")
if slave_server_id == 0:
raise UtilRplError("Slave server_id is set to 0.")
# Check for server_id uniqueness
if master_server_id == slave_server_id:
raise UtilRplError("The slave's server_id is the same as the "
"master.")
return []
###### 检查 uuid_id 唯一性
errors = rpl.check_server_uuids()
for error in errors:
# 1.mysql版本不小于5.6.5
# 2.GTID_MODE必须开启
# 3.master_uuid 必须开启
# 4.slave_uuid 必须开启
# 5.master_uuid和slave_uuid不能等于
print error
# Check for server_uuid uniqueness
if verbosity > 0:
print "# master uuid = %s" % master.get_server_uuid()
print "#  sla
# check_server_uuids方法解析
def check_server_uuids(self):
master_uuid = self.master.get_uuid()
slave_uuid = self.slave.get_uuid()
# 内部封装get_uuid()
if self.supports_gtid() != "NO":
# 检查是否开启了gtid其内部封装其实是执行SELECT @@GLOBAL.GTID_MODE的结果
# ON为开启，OFF为支持但未开启，NO为不支持GITD
# 什么情况下为得出NO值？，mysql版本小于5.6.5
#version_ok = self.check_version_compat(5, 6, 5)
# 内部封装为执行 SHOW VARIABLES LIKE 'VERSION'
#if not version_ok:
#    return "NO"
res = self.show_server_variable("server_uuid") # 内部封装为执行SHOW VARIABLES LIKE 'server_uuid'
# Check for both not supporting UUIDs.
if master_uuid is None and slave_uuid is None:
return []
# Check for unbalanced servers - one with UUID, one without
if master_uuid is None or slave_uuid is None:
raise UtilRplError("%s does not support UUIDs." %
"Master" if master_uuid is None else "Slave")
# Check for uuid uniqueness
if master_uuid == slave_uuid:
raise UtilRplError("The slave's UUID is the same as the "
"master.")
##### 第二步：检查 InnoDB 兼容性
# Check InnoDB compatibility
if verbosity > 0:
print "# Checking InnoDB statistics for type and version conflicts."
errors = rpl.check_innodb_compatibility(options) #检查InnoDB兼容性
for error in errors:
print error
# check_innodb_compatibility方法
def check_innodb_compatibility(self, options):
pedantic = options.get("pedantic", False)
verbose = options.get("verbosity", 0) > 0
errors = []
master_innodb_stats = self.master.get_innodb_stats()
slave_innodb_stats = self.slave.get_innodb_stats()
# get_innodb_stats()所做的操作
# 1.是否内置了innodb引擎，能查出数据则为内置了innodb引擎，innodb类型改为builtin
# SELECT (support='YES' OR support='DEFAULT' OR support='ENABLED') AS `exists` FROM INFORMATION_SCHEMA.ENGINES WHERE engine = 'innodb'
# 2.是否使用了innodb插件，能查出数据则为支持innodb引擎插件，innodb类型改为plugin
# SELECT (plugin_library LIKE 'ha_innodb_plugin%') AS `exists` FROM INFORMATION_SCHEMA.PLUGINS WHERE LOWER(plugin_name) = 'innodb' AND LOWER(plugin_status) = 'active'
# 3.innodb的版本信息
# SELECT plugin_version, plugin_type_version FROM INFORMATION_SCHEMA.PLUGINS WHERE LOWER(plugin_name) = 'innodb';
# innodb本部号分为两个，plugin_version和plugin_type_version
# +----------------+---------------------+
# | plugin_version | plugin_type_version |
# +----------------+---------------------+
# | 5.7            | 50725.0             |
# +----------------+---------------------+
# 4.检查have_innodb是否开启
# SHOW VARIABLES LIKE 'have_innodb' 目前不知道这一步是用了做什么的，mysql官方文档没有查到have_innodb参数的具体用意。是否与Mariadb有关？
# 从代码判断have_innodb的返回值为Yes和No
# 最终返回一个：(innoDB类型,plugin_version, plugin_type_version, have_innodb)
if master_innodb_stats != slave_innodb_stats:
# master和slave的innoDB类型,plugin_version, plugin_type_version, have_innodb参数必须一样
if not pedantic:
errors.append("WARNING: Innodb settings differ between master "
"and slave.")
if verbose or pedantic:
cols = ['type', 'plugin_version', 'plugin_type_version',
'have_innodb']
rows = []
rows.append(master_innodb_stats)
errors.append("# Master's InnoDB Stats:")
errors.extend(_get_list(rows, cols))
rows = []
rows.append(slave_innodb_stats)
errors.append("# Slave's InnoDB Stats:")
errors.extend(_get_list(rows, cols))
if pedantic:
for line in errors:
print line
raise UtilRplError("Innodb settings differ between master "
"and slave.")
return errors
#### 第三步：检查存储引擎一致性
# Checking storage engines
if verbosity > 0:
print "# Checking storage engines..."
errors = rpl.check_storage_engines(options) #检查存储引擎
for error in errors:
print error
# check_storage_engines方法
def check_storage_engines(self, options):
pedantic = options.get("pedantic", False)
verbose = options.get("verbosity", 0) > 0
errors = []
slave_engines = self.slave.get_storage_engines()
results = self.master.check_storage_engines(slave_engines)
# get_storage_engines()所做的操作
# 执行 SELECT UPPER(engine), UPPER(support) FROM INFORMATION_SCHEMA.ENGINES ORDER BY engine获取当前数据库所安装或所支持的引擎
# 1.get_storage_engines检查所得到的引擎主从要一致
if results[0] is not None or results[1] is not None:
if not pedantic:
errors.append("WARNING: The master and slave have differing "
"storage engine configurations!")
if verbose or pedantic:
cols = ['engine', 'support']
if results[0] is not None:
errors.append("# Storage engine configuration on Master:")
errors.extend(_get_list(results[0], cols))
if results[1] is not None:
errors.append("# Storage engine configuration on Slave:")
errors.extend(_get_list(results[1], cols))
if pedantic:
for line in errors:
print line
raise UtilRplError("The master and slave have differing "
"storage engine configurations!")
return errors
#### 第四步：检查 master binary logging
# Check master for binary logging
print "# Checking for binary logging on master..."
errors = rpl.check_master_binlog()
# check_master_binlog内执行SHOW VARIABLES LIKE 'log_bin'获取是否开启了binlog，如果为"OFF"或者"0"则报错
if errors != []:
raise UtilError(errors[0])
#### 第五步：创建复制
# Setup replication
print "# Setting up replication..."
if not rpl.setup(rpl_user, 10): #建立主从复制，等待slave同步的尝试次数
raise UtilError("Cannot setup replication.")
# setup方法解析
def setup(self, rpl_user, num_tries):
if self.master is None or self.slave is None:
print "ERROR: Must connect to master and slave before " \
"calling replicate()"
return False
result = True
# Parse user and password (support login-paths)
try:
r_user, r_pass = parse_user_password(rpl_user)
except FormatError:
raise UtilError(USER_PASSWORD_FORMAT.format("--rpl-user"))
# Check to see if rpl_user is present, else create her
if not self.create_rpl_user(r_user, r_pass)[0]:
# create_rpl_user()创建复制用户
# 1.检查是否启用了跳过权限表，就是启动了--skip-grant-tables参数
# 执行SHOW GRANTS FOR 'snuffles'@'host'，报错如ERROR 1141 (42000)则为未开启，ERROR 1290 (HY000)为开启了--skip-grant-tables参数
# 2.检查用户是否存在
# 通过user.exists()方法执行：SELECT * FROM mysql.user WHERE user = 'rpl' and host = '10.186.65.119' 进行检查
# 3.不存在则创建用户
# CREATE USER 'rpl'@'10.186.65.119' IDENTIFIED WITH 'mysql_native_password' AS '*624459C87E534A126498ADE1B12E0C66EDA035A3' # 创建用户和密码
# GRANT REPLICATION SLAVE ON *.* TO 'rpl'@'10.186.65.119' # 赋予复制权限
# 4.检查用户权限
# SELECT CURRENT_USER()
# SHOW GRANTS FOR 'rpl'@'10.186.65.119';
return False
# Read master log file information
res = self.master.get_status() # 就是SHOW MASTER STATUS，如果执行错误则报错
if not res:
print "ERROR: Cannot retrieve master status."
return False
# If master log file, pos not specified, read master log file info
read_master_info = False
if self.master_log_file is None:
res = self.master.get_status() # 没有指定位置点则使用SHOW MASTER STATUS获取的
if not res:
print "ERROR: Cannot retrieve master status."
return False
#mysql> SHOW MASTER STATUS;
#+------------------+-----------+--------------+------------------+------------------------------------------------------------------------------------------------+
#| File             | Position  | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                                                                              |
#+------------------+-----------+--------------+------------------+------------------------------------------------------------------------------------------------+
#| mysql-bin.000023 | 211116031 |              |                  | f7d09cd0-1850-11ec-8d9a-02000aba414d:1-1849979 |
#+------------------+-----------+--------------+------------------+------------------------------------------------------------------------------------------------+
read_master_info = True
self.master_log_file = res[0][0] # 对应SHOW MASTER STATUS里的File字段
self.master_log_pos = res[0][1] # 对应SHOW MASTER STATUS里的Position字段
else:
#指定了位置点所做的操作
# Check to make sure file is accessible and valid
found = False
res = self.master.get_binary_logs(self.query_options)
for row in res:
if row[0] == self.master_log_file:
found = True
break
if not found:
raise UtilError("Master binary log file not listed as a "
"valid binary log file on the master.")
if self.master_log_file is None:
raise UtilError("No master log file specified.")
# Stop slave first
res = self.slave.get_thread_status()
# 执行 SHOW SLAVE STATUS，获取(slave_io_state, slave_io_running, slave_sql_running)
if res is not None:
if res[1] == "Yes" or res[2] == "Yes":
# io线程和sql线程都为running时，停止复制
res = self.slave.stop(self.query_options)
# self.slave.stop就是执行 STOP SLAVE
# Connect slave to master
if self.verbosity > 0:
print "# Connecting slave to master..."
master_values = {
'Master_Host': self.master.host,
'Master_Port': self.master.port,
'Master_User': r_user,
'Master_Password': r_pass,
'Master_Log_File': self.master_log_file,
'Read_Master_Log_Pos': self.master_log_pos,
}
# Use the options SSL certificates if defined,
# else use the master SSL certificates if defined.
if self.ssl:
master_values['Master_SSL_Allowed'] = 1
if self.ssl_ca:
master_values['Master_SSL_CA_File'] = self.ssl_ca
if self.ssl_cert:
master_values['Master_SSL_Cert'] = self.ssl_cert
if self.ssl_key:
master_values['Master_SSL_Key'] = self.ssl_key
elif self.master.has_ssl:
master_values['Master_SSL_Allowed'] = 1
master_values['Master_SSL_CA_File'] = self.master.ssl_ca
master_values['Master_SSL_Cert'] = self.master.ssl_cert
master_values['Master_SSL_Key'] = self.master.ssl_key
change_master = self.slave.make_change_master(self.from_beginning,
master_values)
#创建复制
# CHANGE MASTER TO MASTER_HOST = '10.186.65.20' MASTER_USER = 'rpl' MASTER_PASSWORD = <secret> MASTER_PORT = 3306 MASTER_AUTO_POSITION=1
res = self.slave.exec_query(change_master, self.query_options)
if self.verbosity > 0:
print "# %s" % change_master
# Start slave
if self.verbosity > 0:
if not self.from_beginning:
if read_master_info:
print "# Starting slave from master's last position..."
else:
msg = "# Starting slave from master log file '%s'" % \
self.master_log_file
if self.master_log_pos >= 0:
msg += " using position %s" % self.master_log_pos
msg += "..."
print msg
else:
print "# Starting slave from the beginning..."
res = self.slave.start(self.query_options)
# 启动slave 就是执行 START SLAVE
# COMMIT提交事务
# Add commit because C/Py are auto_commit=0 by default
self.slave.exec_query("COMMIT")
# 检查slave的状态
# Check slave status
i = 0
while i < num_tries:
time.sleep(1)
res = self.slave.get_slaves_errors() # SHOW SLAVE STATUS
status = res[0]
sql_running = res[4]
if self.verbosity > 0:
io_errorno = res[1]
io_error = res[2]
io_running = res[3]
sql_errorno = res[5]
sql_error = res[6]
print "# IO status: %s" % status
print "# IO thread running: %s" % io_running
# if io_errorno = 0 and error = '' -> no error
if not io_errorno and not io_error:
print "# IO error: None"
else:
print "# IO error: %s:%s" % (io_errorno, io_error)
# if io_errorno = 0 and error = '' -> no error
print "# SQL thread running: %s" % sql_running
if not sql_errorno and not sql_error:
print "# SQL error: None"
else:
print "# SQL error: %s:%s" % (io_errorno, io_error)
if status == "Waiting for master to send event" and sql_running:
break
elif not sql_running:
if self.verbosity > 0:
print "# Retry to start the slave SQL thread..."
# SQL thread is not running, retry to start it
res = self.slave.start_sql_thread(self.query_options)
if self.verbosity > 0:
print "# Waiting for slave to synchronize with master"
i += 1
if i == num_tries:
print "ERROR: failed to sync slave with master."
result = False
if result is True:
self.replicating = True
return result
# 测试复制
# Test the replication setup.
if test_db:
rpl.test(test_db, 10)
# 就是主库执行 CREATE DATABASE TEST1
# 从库执行 SHOW DATABASES检查TEST1是否存在，检查失败重试10次。能检查出来就通过
print "# ...done."
#### 步骤梳理
第一步：检查重要参数的唯一性
- 检查server_id唯一性 符合mysql主从复制集群创建的server_id唯一性的条件： 1.master和slave必须开启server_id ；2.master和slave的server_id值必不能相对
- 检查server_id的方式： SHOW VARIABLES LIKE &#8216;server_id&#8217;等于0则为未开启 
- 检查uuid_id唯一性 符合mysql主从复制集群创建的server_uuid唯一性的条件 mysql版本不小于5.6.5
- master和slave的GTID_MODE参数必须开启
- master和slave的master_uuid参数必须开启
- master和slave的master_uuid参数不可以相等 
- 检查uuid_id的方式：SHOW VARIABLES LIKE &#8216;server_uuid&#8217;
- 检查gtid是否开启的方式： SELECT @@GLOBAL.GTID_MODE ON为开启，OFF为支持但未开启
- 检查mysql版本的方式： SHOW VARIABLES LIKE &#8216;VERSION&#8217; 
第二步：检查InnoDB兼容性
- 符合InnoDB兼容性的条件: 内置了innodb引擎或者使用了innodb引擎的插件，即为数据库必须有innodb引擎存在 
- 主从库的innoDB类型,plugin_version, plugin_type_version, have_innodb参数必须完全一致 
- 检查innodb引擎的方式： SELECT (support=&#8217;YES&#8217; OR support=&#8217;DEFAULT&#8217; OR support=&#8217;ENABLED&#8217;) AS `exists` FROM INFORMATION_SCHEMA.ENGINES WHERE engine = &#8216;innodb&#8217; 
- 获取innodb版本号的方式： SELECT plugin_version, plugin_type_version FROM INFORMATION_SCHEMA.PLUGINS WHERE LOWER(plugin_name) = &#8216;innodb&#8217;; 
第三步：检查存储引擎一致性
- 符合存储引擎一致性的条件：
检查所得到的引擎主从要一致
- 检查存储引擎的方法：
SELECT UPPER(engine), UPPER(support) FROM INFORMATION_SCHEMA.ENGINES ORDER BY engine
第四步：检查master binary logging
- 符合存master binary logging的条件
log_bin必须开启
- 检查log_bin的方式：
SHOW VARIABLES LIKE &#8216;log_bin&#8217;
第五步：创建复制
- 创建复制用户
检查是否启用了跳过权限表(启动了&#8211;skip-grant-tables参数)
SHOW GRANTS FOR &#8216;snuffles&#8217;@&#8217;host&#8217;
#执行SHOW GRANTS FOR &#8216;snuffles&#8217;@&#8217;host&#8217;，报错如ERROR 1141 (42000)则为未开启，ERROR 1290 (HY000)为开启了&#8211;skip-grant-tables参数
- 检查用户是否存在
SELECT * FROM mysql.user WHERE user = &#8216;rpl&#8217; and host = &#8216;10.186.65.119&#8217;
- 不存在则创建用户
CREATE USER &#8216;rpl&#8217;@&#8217;10.186.65.119&#8217; IDENTIFIED WITH &#8216;mysql_native_password&#8217; AS &#8216;*624459C87E534A126498ADE1B12E0C66EDA035A3&#8217;
- 赋予复制权限
GRANT REPLICATION SLAVE ON *.* TO &#8216;rpl&#8217;@&#8217;10.186.65.119&#8217;
- 检查用户权限
SHOW GRANTS FOR &#8216;rpl&#8217;@&#8217;10.186.65.119&#8217;;
- 检查slave机器上是否有复制信息
SHOW SLAVE STATUS
- io线程和sql线程都为running时，停止复制
- STOP SLAVE
- 创建复制
CHANGE MASTER TO MASTER_HOST = &#8216;10.186.65.20&#8217; MASTER_USER = &#8216;rpl&#8217; MASTER_PASSWORD =  MASTER_PORT = 3306 MASTER_AUTO_POSITION=1
- 启动复制
start slave
- 检查复制状态
SHOW SLAVE STATUS
- 测试复制
主库执行CREATE DATABASE TEST1
- 从库执行SHOW DATABASES检查TEST1是否存在，检查失败重试10次。能检查出来就通过