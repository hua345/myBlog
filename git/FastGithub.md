## 参考

[庆祝dotnet6，fastgithub送给你](https://www.cnblogs.com/kewei/p/15533079.html)

[https://github.com/dotnetcore/FastGithub](https://github.com/dotnetcore/FastGithub)

### 软件功能

- 提供域名的纯净IP解析；
- 提供IP测速并选择最快的IP；
- 提供域名的tls连接自定义配置；
- google的CDN资源替换，解决大量国外网站无法加载js和css的问题；

这是一个本机工具，无任何中转的远程服务器，但也能让你的网络产生很大的改善：

### 安全性说明

FastGithub为每台不同的主机生成自颁发CA证书，保存在cacert文件夹下。客户端设备需要安装和无条件信任自颁发的CA证书，请不要将证书私钥泄露给他人，以免造成损失。

### 合法性说明

《国际联网暂行规定》第六条规定：“计算机信息网络直接进行国际联网，必须使用邮电部国家公用电信网提供的国际出入口信道。任何单位和个人不得自行建立或者使用其他信道进行国际联网。” FastGithub本地代理使用的都是“公用电信网提供的国际出入口信道”，从国外Github服务器到国内用户电脑上FastGithub程序的流量，使用的是正常流量通道，其间未对流量进行任何额外加密（仅有网页原有的TLS加密，区别于VPN的流量加密），而FastGithub获取到网页数据之后发生的整个代理过程完全在国内，不再适用国际互联网相关之规定。

### FastGithub日志

```
已监听https://localhost:443，https反向代理服务启动完成
已监听http://localhost:80，http反向代理服务启动完成
已监听ssh://localhost:22，github的ssh反向代理服务启动完成
已监听git://localhost:9418，github的git反向代理服务启动完成
FastGithub启动完成，当前版本为v2.1.1，访问 https://github.com/dotnetcore/fastgithub 关注新版本

alive.github.com->127.0.0.1
github.com->127.0.0.1
github.githubassets.com->127.0.0.1

github.com:443->[52.192.72.89, 140.82.114.3, 140.82.112.4]
api.github.com:443->[192.32021-11-28 21:08:43.873
github.com:443->[52.192.72.89, 140.82.114.3, 140.82.112.4]0.255.116, 192.30.255.117, 140.82.121.5]
```

