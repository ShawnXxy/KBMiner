# 技术分享 | 快速掌握 MySQL 8.0 认证插件的使用

**原文链接**: https://opensource.actionsky.com/20200217-mysql/
**分类**: MySQL 新特性
**发布时间**: 2020-02-17T01:38:47-08:00

---

**引言**
MySQL 8.0.15 版本主从复制时，io 线程一直处于 connecting 状态， 由于复制用户使用的认证插件是 caching_sha2_password，而想要通过 caching_sha2_password 认证的用户访问数据库，只有两个途径：
1. 使用加密连接2. 使用支持 RSA 密钥对，进行密码交换的非加密连接
之前 change master to 时，未进行配置 master_ssl=1（等效于客户端 &#8211;ssl-mode=REQUIRED 的配置），导致从库通过复制用户连接主库时使用的非加密连接，同时又没有进行 RSA 密钥配置，导致 io 线程运行异常。为此整理一些关于 MySQL 8.0 认证插件 caching_sha2_password 的一些限制以及 RSA 的相关内容。
**一、认证插件 caching_sha2_password**
**1.1 作用：**
用于实现 SHA-256 认证
**1.2 工作机制：**1）caching_sha2_password 会将用户名和用户密码哈希对作为缓存条目进行缓存，当用户进行访问时，会跟缓存条目进行匹配，如果匹配则认证成功。2）如果插件没有匹配到相应的缓存条目，首先会根据 mysql.user 系统表进行校验，如果校验通过会生成相应的缓存条目，下次相同用户进行访问时可以直接命中缓存条目，提升二次认证效率。如果校验失败，则认证失败、访问拒绝。
**1.3 优势（相对于 sha256_password）：**1）caching_sha2_password 认证插件在 MySQL 服务端进行缓存认证条目，对于之前认证过的用户，可以提升二次认证的速度。2）不管与 MySQL 链接的 SSL 库如何，都可以使用基于 RSA 的密码交换3）提供了对使用 Unix 套接字文件和共享内存协议的客户端连接的支持
**1.4 缓存管理：**
1）当删除用户、修改用户名、修改用户密码、修改认证方式会清理相对应的缓存条目
2）Flush Privileges 会清除所有的缓存条目
3）数据库关闭时会清除所有缓存条目
**1.5 限制：**
通过 caching_sha2_password 认证的用户访问数据库，只能通过加密的安全连接或者使用支持 RSA 密钥对进行密码交换的非加密连接进行访问。
**二、caching_sha2_password 插件使用 RSA 秘钥对**
**2.1秘钥对生成方式：**1）自动生成
参数 caching_sha2_password_auto_generate_rsa_keys 默认是开启，数据库在启动时自动生成相对应的公钥和私钥。2）手动生成
通过 mysql_ssl_rsa_setup 指定目录生成 SSL 相关的私钥和证书以及 RSA 相关的公钥和私钥。
**2.2 查看 RSA 公钥值的方式：**
通过状态变量 Caching_sha2_password_rsa_public_key 可以查看 caching_sha2_password 身份验证插件使用的 RSA 公钥值。
**2.3 使用 RSA 键值对的注意事项：**
1）拥有 MySQL 服务器上 RSA 公钥的客户端，可以在连接过程中与服务器进行基于 RSA 密钥对的密码交换2）对于通过使用 caching_sha2_password 和基于 RSA 密钥对的密码交换进行身份验证的帐户，默认情况下，MySQL 服务端不会将 RSA 公钥发送给客户端，获取 RSA 公钥的方式有以下两种：A. 客户端从服务端拷贝相应的 RSA 公钥，B. 客户端发起访问时，请求获取 RSA 公钥。在 RSA 公钥文件可靠性能够保证的前提下，拷贝 RSA 公钥跟请求获取 RSA 公钥相比，由于减少了 c/s 之间的通信，相对而言更安全。如果在网络安全前提下，后者相对来说会更方便。
**2.4 命令行客户端通过 RSA 秘钥对进行访问：**1）通过拷贝方式获取RSA公钥，在通过命令行客户端进行访问时，需要在命令行指定 &#8211;server-public-key-path 选项来进行访问
2）通过请求获取RSA公钥的方式，在通过命令行客户端进行访问时，需要在命令行中指定 &#8211;get-server-public-key 选项来进行访问。选项 &#8211;server-public-key-path 优于 &#8211;get-server-public-key