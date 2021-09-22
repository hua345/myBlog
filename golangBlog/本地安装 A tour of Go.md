## 参考

- [Go 技巧分享：本地安装 A tour of Go](https://learnku.com/go/wikis/38166)

官方的 [tour.golang.org](https://tour.golang.org/) 是一个很棒的入门资料。

Go 团队将其源码 [托管到 GitHub 上](https://github.com/golang/tour)。针对访问不稳定的情况，国内用户推荐在本地搭建『Go Tour』网站。

## 

```bash
# 下载安装包
$ go get golang.org/x/tour
# 检查mod文件
$ ls -al $GOPATH/pkg/mod/golang.org/x
drwxr-xr-x 1 chenjh91 1049089 0 Sep  9 10:14 'tour@v0.1.0'/
# 首先创建目标文件夹
mkdir -p $GOPATH/src/golang.org/x
# 接下来只需将 pkg 下的 Tour 的内容复制到 src 下即可：

$ cp -rf $GOPATH/pkg/mod/golang.org/x/tour@v0.1.0 $GOPATH/src/golang.org/x/tour

```

#### 编译中文版

```
# go get -u github.com/Go-zh/tour
```

#### 运行服务
```
Fang@FangFang MINGW64 /e/goCode/bin
$ tour.exe
2019/05/14 17:18:45 Serving content from E:\goCode\src\github.com\Go-zh\tour
2019/05/14 17:18:45 A browser window should open. If not, please visit http://127.0.0.1:3999
2019/05/14 17:18:46 accepting connection from: 127.0.0.1:61926
2019/05/14 17:19:02 running snippet from: 127.0.0.1:61926
```

#### 编译英文版
```
go get github.com/golang/tour 
mv $GOPATH/src/github.com/golang/tour $GOPATH/src/golang.org/x/tour
cd $GOPATH/src/golang.org/x/tour
go build && go install
```
