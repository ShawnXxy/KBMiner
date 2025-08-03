# 故障分析 | MySQL 备份文件静默损坏一例分析

**原文链接**: https://opensource.actionsky.com/20230313-mysql/
**分类**: MySQL 新特性
**发布时间**: 2023-03-12T23:04:58-08:00

---

作者：付祥
现居珠海，主要负责 Oracle、MySQL、mongoDB 和 Redis 维护工作。
本文来源：原创投稿
*爱可生开源社区出品，原创内容未经授权不得随意使用，转载请联系小编并注明来源。
#### 背景
线上一套 MySQL 计划升级到 8.0 ，通过备份还原搭建一个测试环境，用于升级测试。数据库采用 xtrabackup 每天进行全备，压缩备份文件约 300G ，解压到一半就报错了：
gzip: stdin: invalid compressed data--format violated
tar: Unexpected EOF in archive
tar: Unexpected EOF in archive
tar: Error is not recoverable: exiting now
刚开始以为只是这个备份文件不完整，又找了前一天备份文件，解压过程中也报了同样的错误，备份文件比较大，无疑增加了排障时间。
#### 故障分析
备份脚本通过 crontab 每天凌晨执行，线上都是同一套备份脚本，不同项目时常做备份数据还原，还是头一次遇到备份文件解压失败现象，查看了脚本，每个关键阶段都做了状态码判断是否成功，若失败就告警，同时对 xtrabackup 备份日志最后一行是否包含 completed OK 关键词也做了判断，关键备份脚本如下：
xtrabackup xxx --stream=tar  --no-timestamp $bkdir 2> xxx.log | gzip - > xxx.tar.gz
近期也没收到失败告警，说明备份脚本是执行成功了的，感觉太奇怪了，查看定时任务日志，发现同一任务同一时间点竟然启了2次：
[root@localhost backup]# grep backup /var/log/cron
Mar  6 00:00:01 localhost CROND[6212]: (root) CMD (sh xxx/mysql_ftp_backup.sh || echo 1 > xxx/err.log)
Mar  6 00:00:01 localhost CROND[6229]: (root) CMD (sh xxx/mysql_ftp_backup.sh || echo 1 > xxx/err.log)
Mar  7 00:00:01 localhost CROND[5387]: (root) CMD (sh xxx/mysql_ftp_backup.sh || echo 1 > xxx/err.log)
Mar  7 00:00:01 localhost CROND[5420]: (root) CMD (sh xxx/mysql_ftp_backup.sh || echo 1 > xxx/err.log)
crond 服务每次同时拉起2个进程执行备份，并发地往同一个压缩文件 xxx.tar.gz 写数据，备份数据相互覆盖，导致备份文件损坏，每天看似备份成功的任务，其实备份都是无效的，这也说明了定期备份恢复演练的重要性。为何定时任务同一时间点会启动2次？查看 crond 进程：
[root@localhost backup]# ps -ef|grep crond |grep -v grep
root 2883 1 0 2018  ? 01:42:46 crond 
root 17293 1 0 2022 ? 00:43:22 crond
原来是因为系统启动了2个 crond 进程，kill crond 进程后重启，再次查看只有一个 crond 进程：
[root@localhost backup]# service crond stop
Stopping crond:                                            [  OK  ]
[root@localhost backup]# ps -ef|grep crond
root      2883     1  0  2018 ?        01:42:46 crond
root     31486 31856  0 10:59 pts/2    00:00:00 grep crond
[root@localhost backup]# kill 2883
[root@localhost backup]# ps -ef|grep crond
root     31572 31856  0 10:59 pts/2    00:00:00 grep crond
[root@localhost backup]# service crond start
Starting crond:                                            [  OK  ]
[root@localhost backup]# ps -ef|grep crond
root     31632     1  0 10:59 ?        00:00:00 crond
root     31639 31856  0 11:00 pts/2    00:00:00 grep crond
#### 总结
为了确保备份有效，需要做如下改进：
1、flock给脚本执行加互斥锁，确保一个时间点只有1个进程运行。
2、定期做备份恢复演练。
3、增加crond进程监控，不等于1告警。