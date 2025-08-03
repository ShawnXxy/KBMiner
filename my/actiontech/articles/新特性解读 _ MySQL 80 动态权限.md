# 新特性解读 | MySQL 8.0 动态权限

**原文链接**: https://opensource.actionsky.com/20190709-mysql8-rule/
**分类**: MySQL 新特性
**发布时间**: 2019-07-08T19:45:31-08:00

---

# 背景
在了解动态权限之前，我们先回顾下 MySQL 的权限列表。
权限列表大体分为服务级别和表级别，列级别以及大而广的角色（也是MySQL 8.0 新增）存储程序等权限。我们看到有一个特殊的 SUPER 权限，可以做好多个操作。比如 SET 变量，在从机重新指定相关主机信息以及清理二进制日志等。那这里可以看到，SUPER 有点太过强大，导致了仅仅想实现子权限变得十分困难，比如用户只能 SET 变量，其他的都不想要。那么 MySQL 8.0 之前没法实现，权限的细分不够明确，容易让非法用户钻空子。
那么 MySQL 8.0 把权限细分为静态权限和动态权限，**下面我画了两张详细的区分图，图 1 为静态权限，图 2 为动态权限。**
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/动态权限1-1024x532.png)											
###### 图 1- MySQL 静态权限的权限管理图
![](https://opensource.actionsky.com/wp-content/uploads/2019/07/动态权限2-1024x901.png)											
###### 图 2-动态权限图
那我们看到其实动态权限就是对 SUPER 权限的细分。 SUPER 权限在未来将会被废弃掉。
我们来看个简单的例子，
比如， 用户 &#8216;ytt2@localhost&#8217;, 有 SUPER 权限。
mysql> show grants for ytt2@'localhost';
+---------------------------------------------------------------------------------+
| Grants for ytt2@localhost                                                       |
+---------------------------------------------------------------------------------+
| GRANT INSERT, UPDATE, DELETE, CREATE, ALTER, SUPER ON *.* TO ytt2@localhost |
+---------------------------------------------------------------------------------+
1 row in set (0.00 sec)
但是现在我只想这个用户有 SUPER 的子集，设置变量的权限。那么单独给这个用户赋予两个能设置系统变量的动态权限，完了把 SUPER 给拿掉。
mysql> grant session_variables_admin,system_variables_admin on *.* to ytt2@'localhost';
Query OK, 0 rows affected (0.03 sec)
mysql> revoke super on *.* from ytt2@'localhost';
Query OK, 0 rows affected, 1 warning (0.02 sec)
我们看到这个 WARNINGS 提示 SUPER 已经废弃了。
mysql> show warnings;
+---------+------+----------------------------------------------+
| Level | Code | Message |
+---------+------+----------------------------------------------+
| Warning | 1287 | The SUPER privilege identifier is deprecated |
+---------+------+----------------------------------------------+
1 row in set (0.00 sec)`
mysql> show grants for ytt2@'localhost';
+-----------------------------------------------------------------------------------+
| Grants for ytt2@localhost |
+-----------------------------------------------------------------------------------+
| GRANT INSERT, UPDATE, DELETE, CREATE, ALTER ON *.* TO ytt2@localhost |
| GRANT SESSION_VARIABLES_ADMIN,SYSTEM_VARIABLES_ADMIN ON *.* TO ytt2@localhost |
+-----------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
当然图 2 上还有其它的动态权限，这里就不做特别说明了。
**近期社区动态**
![](https://opensource.actionsky.com/wp-content/uploads/2019/08/海报.jpg)