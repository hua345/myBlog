# git镜像加速

## 参考

[https://github.com/hoodiearon/w3-goto-world/tree/master/下载加速Clone、AWS、Git镜像](https://github.com/hoodiearon/w3-goto-world/tree/master/下载加速Clone、AWS、Git镜像)

## 1.git下载

使用淘宝源加快国内git下载

[https://npm.taobao.org/mirrors/git-for-windows/](https://npm.taobao.org/mirrors/git-for-windows/)

## 2.Github 下载过慢处理（releases）

### 2.1查询以下链接的DNS解析地址

- [https://www.ipaddress.com/](https://www.ipaddress.com/)
- [http://tool.chinaz.com/dns](http://tool.chinaz.com/dns)

```bash
github.com
assets-cdn.github.com
github.global.ssl.fastly.net
raw.githubusercontent.com
```

### 2.2 记录下查询到的IP地址，并添加进入`C:\Windows\System32\drivers\etc\Hosts`文件

### 2.3 添加 `aws host`

```bash
52.216.177.37 s3.amazonaws.com
52.216.76.252 github-cloud.s3.amazonaws.com
```

### 2.4 运行cmd输入`ipconfig /flushdns`指令刷新系统DNS

## host

将以下host复制进`C:\Windows\System32\drivers\etc\hosts`，再使用命令行输入`ipconfig /flushdns`刷新dns缓存。

详情 关于Github克隆及下载过慢的解决方案

```conf
## GitHub Start
140.82.114.3 github.com
140.82.114.4 github.com
140.82.113.3 github.com
140.82.113.4 github.com
192.30.253.118 gist.github.com
151.101.109.194 github.global.ssl.fastly.net
31.13.64.49 github.global.ssl.fastly.net
123.129.254.13 github.global.ssl.fastly.net
123.129.254.14 github.global.ssl.fastly.net
123.129.254.15 github.global.ssl.fastly.net
185.199.110.153 assets-cdn.github.com
185.199.111.153 assets-cdn.github.com
185.199.109.153 assets-cdn.github.com
185.199.108.153 assets-cdn.github.com

151.101.76.133 raw.githubusercontent.com
13.250.162.133 githubusercontent.com
199.232.68.133 githubusercontent.com
## GitHub End
## amazonaws Start
52.216.168.133 s3.amazonaws.com
52.216.24.214 s3.amazonaws.com
52.216.76.252 github-cloud.s3.amazonaws.com
## amazonaws End
```

## 加速网站

- [https://toolwa.com/github/](https://toolwa.com/github/)
- [https://shrill-pond-3e81.hunsh.workers.dev/](https://shrill-pond-3e81.hunsh.workers.dev/)

## Git Clone 克隆过慢改进

### 浅克隆

`git clone` 默认会下载项目的完整历史版本，若只关心最新的代码，而不关心之前的历史，可以使用浅复制功能：

`git clone --depth=1  xxx`

`--depth=1` 表示只下载最近一次的版本，使用浅复制可以大大减少下载的数据量，这样即使在红色网络环境下，也可以快速的获得代码
