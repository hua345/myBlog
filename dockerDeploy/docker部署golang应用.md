#### 1. 拉取goalng环境镜像
```
docker pull golang

[root@dockerMaster ~]# docker run golang:latest go version
go version go1.12.5 linux/amd64
```
#### 2. 创建golang工程
在`$GOPATH/src`目录,创建`hellodocker`目录
编辑`main.go`文件
```
package main

import (
    "fmt"
    "net/http"
)

func indexHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "hello docker from golang\n")
    fmt.Println("handle /")
}

func main() {
    http.HandleFunc("/", indexHandler)
    http.ListenAndServe(":8080", nil)
}
```
#### 3. 编辑`Dockerfile`
在工程目录`hellodocker`下，新建`Dockerfile`文件
```
FROM golang:latest

MAINTAINER chenjianhua 2290910211@qq.com

WORKDIR $GOPATH/src/hellodocker
ADD . $GOPATH/src/hellodocker
RUN go build .

EXPOSE 8080

ENTRYPOINT ["./hellodocker"]
```
#### 4. 构建docker镜像
```
[root@dockerMaster hellodocker]# docker build -t hellodocker .
Sending build context to Docker daemon  6.562MB
Step 1/7 : FROM golang:latest
 ---> 7ced090ee82e
Step 2/7 : MAINTAINER chenjianhua 2290910211@qq.com
 ---> Using cache
 ---> b0cb7729ca65
Step 3/7 : WORKDIR $GOPATH/src/hellodocker
 ---> Running in b2d9e6d108bf
Removing intermediate container b2d9e6d108bf
 ---> 35a26357dee2
Step 4/7 : ADD . $GOPATH/src/hellodocker
 ---> 7af96a2797e5
Step 5/7 : RUN go build .
 ---> Running in f185437eebe5
Removing intermediate container f185437eebe5
 ---> 11c240eea12f
Step 6/7 : EXPOSE 8080
 ---> Running in 0ed34639954f
Removing intermediate container 0ed34639954f
 ---> d619db252376
Step 7/7 : ENTRYPOINT ["./hellodocker"]
 ---> Running in 6bd0468e19d6
Removing intermediate container 6bd0468e19d6
 ---> f07fc247dc4b
Successfully built f07fc247dc4b
Successfully tagged hellodocker:latest
```
#### 运行docker镜像
```
docker run -it -p 8080:8080 hellodocker
# 后台运行
docker run -d -p 8080:8080 hellodocker
```
