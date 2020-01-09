# 参考

- [https://travis-ci.org/](https://travis-ci.org/)
- [https://github.com/marketplace/travis-ci](https://github.com/marketplace/travis-ci)
- [持续集成服务 Travis CI 教程](http://www.ruanyifeng.com/blog/2017/12/travis_ci_tutorial.html)
- [https://docs.travis-ci.com/user/languages/go/](https://docs.travis-ci.com/user/languages/go/)

## 运行流程

`Travis` 的运行流程很简单，任何项目都会经过两个阶段。

- `install` 阶段：安装依赖
- `script` 阶段：运行脚本

## 钩子方法

Travis 为上面这些阶段提供了 7 个钩子。

- `before_install`：install 阶段之前执行
- `before_script`：script 阶段之前执行
- `after_failure`：script 阶段失败时执行
- `after_success`：script 阶段成功时执行
- `before_deploy`：deploy 步骤之前执行
- `after_deploy`：deploy 步骤之后执行
- `after_script`：script 阶段之后执行

## go依赖管理

项目中有`Makefile`文件,步骤`install steps`不会执行

项目中如果没有`Makefile`文件

```bash
go get -v ./...
```

## go 默认构建脚本

项目中有`Makefile`文件,`Travis CI`会运行测试用例

```bash
make
```

项目中如果没有`Makefile`文件

```bash
go test -v ./...
```

## [数据库服务](https://docs.travis-ci.com/user/database-setup/#redis)

### MySQL

Start MySQL in your `.travis.yml`:

```yaml
services:
  - mysql
```

>MySQL binds to `127.0.0.1` and a socket defined in `~travis/.my.cnf` and requires authentication.
You can connect using the username `travis or root` and a `blank password`.

### PostgreSQL

Start PostgreSQL in your .travis.yml:

```yaml
services:
  - postgresql
```

The default user for accessing the local PostgreSQL server is `postgres` with a `blank password`.

Create a database for your application by adding a line to your `.travis.yml`:

```yaml
before_script:
  - psql -c 'create database travis_ci_test;' -U postgres
```

### Redis

Start Redis in your `.travis.yml`:

```yaml
services:
  - redis-server
```

Redis uses the default configuration and is available on localhost.

```yaml
language: go

go:
  - 1.13.x

services:
  - redis-server

script:
  - go test ./pkg/algorithm/...
  - go test ./pkg/encrypt/...
  - go test ./pkg/golang/...
  - go test ./pkg/jwt/...
  - go test ./pkg/patterns/...
  - go test ./pkg/redigo/...
  - go test ./pkg/redis/...
  - go test ./pkg/util/...

before_install:
  - go get -v -t -d ./...
```

```bash
# git clone --depth=50 --branch=master https://github.com/hua345/golangpkg.git hua345/golangpkg
# cd hua345/golangpkg
# travis_setup_go
go version go1.13.4 linux/amd64
# export GOPATH="/home/travis/gopath"
# export GO111MODULE="auto"
# go version
go version go1.13.4 linux/amd64
go.env
# go env
# travis_install_go_dependencies 1.13.x -v
# go get -v -t ./...
```
