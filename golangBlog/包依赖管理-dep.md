# 包管理工具 dep

`Vendor`只是 go 官方提供的一个机制，但是包管理的问题依然没有解决，并且也没有对依赖进行版本管理。如果要实现上述的功能，还需要借助包管理工具。

- https://github.com/golang/go/wiki/PackageManagementTools
- https://github.com/golang/dep

## dep 源码安装

```bash
go get -d -u github.com/golang/dep
cd $(go env GOPATH)/src/github.com/golang/dep
DEP_LATEST=$(git describe --abbrev=0 --tags)
git checkout $DEP_LATEST
go install -ldflags="-X main.version=$DEP_LATEST" ./cmd/dep
git checkout master
```

## 查看帮助

```bash
$ dep -h
Dep is a tool for managing dependencies for Go projects

Usage: "dep [command]"

Commands:

  init     Set up a new Go project, or migrate an existing one
  status   Report the status of the project's dependencies
  ensure   Ensure a dependency is safely vendored in the project
  version  Show the dep version information
  check    Check if imports, Gopkg.toml, and Gopkg.lock are in sync

Examples:
  dep init                               set up a new project
  dep ensure                             install the project's dependencies
  dep ensure -update                     update the locked versions of all dependencies
  dep ensure -add github.com/pkg/errors  add a dependency to the project

Use "dep help [command]" for more information about a command.
```

## 参考

- [dep installation](https://golang.github.io/dep/docs/installation.html)
