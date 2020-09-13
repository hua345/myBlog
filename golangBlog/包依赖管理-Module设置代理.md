# Go Module代理

- [https://mirrors.aliyun.com/goproxy/](https://mirrors.aliyun.com/goproxy/)
- [https://github.com/golang/go/wiki/Modules#are-there-always-on-module-repositories-and-enterprise-proxies](https://github.com/golang/go/wiki/Modules#are-there-always-on-module-repositories-and-enterprise-proxies)

> Golang 从1.13开始默认使用Go Mod，请切换至Go Mod并配置goproxy

## 设置GOPROXY代理

```bash
go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GOPROXY=https://goproxy.io,direct
go env -w GOPROXY=https://gocenter.io,direct
```

## 设置GOSUMDB校验

> `Get https://sum.golang.org/lookup/github.com/xxx:` dial 超时

因为Go 1.13设置了默认的`GOSUMDB=sum.golang.org`，这个网站是被墙了的，用于验证包的有效性

```bash
# 关闭自动验证
go env -w GOSUMDB=off
# 可以设置专门为国内提供的sum 验证服务。
go env -w GOSUMDB="sum.golang.google.cn"
```
