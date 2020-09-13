# 参考

- [Golang环境安装和依赖管理](https://www.jianshu.com/p/80b52e054c35)

## Vendor

> `Golang1.5`加入了一个试验性的`vendor`文件夹机制`(vendor：供应商/小贩)`。
从`Golang1.6`正式开启这个功能。`vendor`机制就是在项目中加入了vendor文件夹，用于存放依赖，这样就可以将不同项目的依赖隔离开。
当使用`go run`或者`go build`命令时，会首先从当前路径下的`vendor`文件夹中查找依赖，如果`vendor`不存在，才会从`GOPATH`中查找依赖。
然而我们安装依赖通常使用`go get`或者`go install`命令，这两个命令依旧会把依赖安装到`GOPATH`路径下。

### go mod/Go1.11以后

> `Golang 1.11` 开始， 实验性出现了可以不用定义`GOPATH`的功能，且官方有`go mod`支持。`Golang 1.12`更是将此特征正式化。

现在用 Golang1.12 进行

```bash
$ go mod init
go: modules disabled inside GOPATH/src by GO111MODULE=auto; see 'go help modules'
```

其中`GO111MODULE=auto`是一个开关，开启或关闭模块支持，它有三个可选值：`off/on/auto`，默认值是`auto`。

- `GO111MODULE=off`,不使用`go Module`支持，通过`vendor`文件夹和`GOPATH`寻找依赖包。现在可以称为`GOPATH mode`。
- `GO111MODULE=on`,要求使用`go Module`支持,忽略`GOPATH`和`vendor`文件夹，只根据`go.mod`文件下载依赖。
- `GO111MODULE=auto`，该项目在`GOPATH src`外面且根目录有`go.mod`文件时，开启模块支持。
在使用模块的时候，`GOPATH`是无意义的，不过它还是会把下载的依赖储存在`GOPATH/src`中，也会把`go install`的结果放在 GOPATH/bin（如果 GOBIN 不存在的话）
我们将项目移出`GOPATH`，然后:

```bash
$ go mod init
go: creating new go.mod: module github.com/hua345/generateCode
```

将会生成`go.mod`文件

```bash
module github.com/hua345/generateCode

go 1.12
```
