# git镜像加速

## 参考

[https://github.com/hoodiearon/w3-goto-world/tree/master/下载加速Clone、AWS、Git镜像](https://github.com/hoodiearon/w3-goto-world/tree/master/下载加速Clone、AWS、Git镜像)

## git下载

使用淘宝源加快国内git下载

[https://npm.taobao.org/mirrors/git-for-windows/](https://npm.taobao.org/mirrors/git-for-windows/)

## Github 下载过慢处理（releases）

查询以下链接的DNS解析地址

- [https://www.ipaddress.com/](https://www.ipaddress.com/)
- [http://tool.chinaz.com/dns](http://tool.chinaz.com/dns)

```bash
github.com
assets-cdn.github.com
```

记录下查询到的IP地址，并添加进入`C:\Windows\System32\drivers\etc\Hosts`文件

运行cmd输入`ipconfig /flushdns`指令刷新系统DNS

## host

将以下host复制进`C:\Windows\System32\drivers\etc\hosts`，再使用命令行输入`ipconfig /flushdns`刷新dns缓存。

详情 关于Github克隆及下载过慢的解决方案

```conf
## GitHub Start
140.82.114.4 github.com
140.82.113.4 github.com
13.229.188.59 github.com
192.30.253.112 github.com
192.30.253.118 gist.github.com
31.13.85.16 github.global.ssl.fastly.net
69.63.178.13 github.global.ssl.fastly.net
123.129.254.13 github.global.ssl.fastly.net
123.129.254.14 github.global.ssl.fastly.net
123.129.254.15 github.global.ssl.fastly.net
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.108.153 assets-cdn.github.com

199.232.4.133 raw.githubusercontent.com
199.232.4.133 githubusercontent.com
## GitHub End
```
