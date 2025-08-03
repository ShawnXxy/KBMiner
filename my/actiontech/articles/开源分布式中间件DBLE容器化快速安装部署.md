# 开源分布式中间件DBLE容器化快速安装部署

**原文链接**: https://opensource.actionsky.com/dble%e5%ae%b9%e5%99%a8%e5%8c%96%e5%bf%ab%e9%80%9f%e5%ae%89%e8%a3%85%e9%83%a8%e7%bd%b2%ef%bc%882-19-01-0%e6%96%b0%e7%89%b9%e6%80%a7%ef%bc%89/
**分类**: 技术干货
**发布时间**: 2019-03-04T00:24:47-08:00

---

## 快速开始(docker-compose)
### 1 关于本节
- 本节内容为你介绍如何快速使用dble的docker-compose文件来启动一个dble的quick start
以及一个按照自定义的配置和sql脚本来启动dble quick start的用例
### 2 安装依赖
- 安装docker
- 安装docker-compose
- 安装mysql连接工具，用于进行连接测试观察结果
### 3 安装过程
从dble项目中下载最新的docker-compose.yml文件
https://raw.githubusercontent.com/actiontech/dble/master/docker-images/docker-compose.yml
使用docker-compose up命令直接启动dble-server，compose配置文件会从dockerhub拉取镜像并最终启动dble
下载docker-compose.yml,进入对应目录
`docker-compose up -d`
`注意：一个创建的3个容器：其中两个为MySQL容器，它们将端口3306映射到Docker宿主机的端口33061和33062；dble容器中端口8066和9066映射到Docker主机上的相同端口；
`
### 4 连接并使用
使用准备好的mysql连接工具连接主机的8066或者9066端口，在docker的默认配置中
8066 端口(服务端口能够执行SQL语句)的用户为 root/123456
9066 端口(管理端口能够执行管理语句)的用户为 man1/654321
`#connect dble server port
mysql -P8066 -u root -p123456 -h 127.0.0.1 
#connect dble manager port
mysql -P9066 -u man1 -p123456 -h 127.0.0.1
#connect mysql1
mysql -P33061 -u root -p123456 -h 127.0.0.1 
#connect mysql2
mysql -P33062 -u root -p123456 -h 127.0.0.1
`
此例子中准备了travelrecord、company、goods等表格并提前进行了表格创建，若需要连接更多的表格配置详情和使用方法
请在dble-server容器中查阅/opt/dble/conf/schema.xml文件
### 5 环境清理
使用完成或者进行环境重建的时候使用docker-compose stop/down来进行环境的清理
`docker-compose stop
`
or
`docker-compose down
`
### 6 使用自定义配置启动dble
在这里介绍下如何使用自定义的dble本地配置来启动docker-compose中的dble
首先，简单描述下默认docker-compose.yml执行的过程，dble-compose挨个启动容器，并且在最终启动dble-server的时候调用。
存在于镜像actiontech/dble:latest目录下的/opt/dble/bin/wait-for-it.sh脚本等待指定的（默认为mysql1容器的mysql服务端口）TCP端口启动，
待到指定TCP端口启动之后调用初始化脚本/opt/dble/bin/docker_init_start.sh对于dble-server这个容器进行初始化（替换配置文件，启动dble，执行sql文件）
下面是默认的docker_init_start.sh脚本
`#!/bin/sh
echo "dble init&start in docker"
sh /opt/dble/bin/dble start
sh /opt/dble/bin/wait-for-it.sh 127.0.0.1:8066
mysql -P9066 -u man1 -h 127.0.0.1 -p654321 -e "create database @@dataNode ='dn1,dn2,dn3,dn4'"
mysql -P8066 -u root -h 127.0.0.1 -p123456 -e "source /opt/dble/conf/testdb.sql" testdb
echo "dble init finish"
/bin/bash
`
可以轻易的看出脚本的内容非常简单，启动dble->等待dble服务启动->执行dble管理命令create database在后端mysql数据库中创建database->执行初始化sql脚本在dble中创建表和插入初始化数据
所以当需要使用非默认的情况进行启动dble-server容器时需要一以下几个基本步骤
+ 需要按照以上的模块化步骤编写一个自己的初始化sh文件，然后照着需要的步骤对于dble进行启动和初始化
+ 在dble-server的启动配置中添加volumes项，将linux本地的配置文件和初始化文件存放目录挂载至dble-server容器内部(注意dble本地放在/opt/dble下)
+ 修改dble-server的启动命令，将初始化脚本修改为自定义的容器内部的初始化脚本
#### e.g.
docker-compose.yml修改如下部分
` dble-server:
image: actiontech/dble:latest
container_name: dble-server
hostname: dble-server
privileged: true
stdin_open: true
tty: true
volumes:
- ./:/opt/init/
command: ["/opt/dble/bin/wait-for-it.sh", "backend-mysql1:3306","--","/opt/init/customized_script.sh"]
ports:
- "8066:8066"
- "9066:9066"
depends_on:
- "mysql1"
- "mysql2"
networks:
net:
ipv4_address: 172.18.0.5
`
对应本地目录./存在以下文件
`schema.xml rule.xml server.xml init.sql customized_script.sh
`
脚本customized_script.sh中的内容为
```
#!/bin/sh
echo "dble init&start in docker"
cp /opt/init/server.xml /opt/dble/conf/
cp /opt/init/schema.xml /opt/dble/conf/
cp /opt/init/rule.xml /opt/dble/conf/
sh /opt/dble/bin/dble start
sh /opt/dble/bin/wait-for-it.sh 127.0.0.1:8066
mysql -P9066 -u man1 -h 127.0.0.1 -p654321 -e "create database @@dataNode ='dn1,dn2,dn3,dn4'"
mysql -P8066 -u root -h 127.0.0.1 -p123456 -e "source /opt/init/init.sql" testdb
echo "dble init finish"
/bin/bash
```