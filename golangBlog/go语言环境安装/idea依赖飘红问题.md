## 打开mod的golang项目后依赖飘红

```bash
#查看环境变量
$ go env
set GO111MODULE=
set GOARCH=amd64
set GOEXE=.exe
set GOMODCACHE=D:\gocode\pkg\mod
set GOOS=windows
set GOPATH=D:\gocode
set GOPRIVATE=
set GOPROXY=https://goproxy.io,direct
set GOROOT=D:\Program Files\go
```

## 开启mod模式

```
go env -w GO111MODULE=on
```

```
$ go env
set GO111MODULE=on
set GOARCH=amd64
```

