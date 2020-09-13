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
