#### 由于网络原因

```bash
#google.golang.org/grpc
git clone https://github.com/grpc/grpc-go.git $GOPATH/src/google.golang.org/grpc
#google.golang.org/genproto
git clone https://github.com/google/go-genproto.git $GOPATH/src/google.golang.org/genproto
```

无法下载`https://golang.org/x/net`依赖包
`golang`在github上有对应的镜像库

```bash
go get github.com/golang/net
go get github.com/golang/tools
go get github.com/golang/crypto
go get github.com/golang/sys
go get github.com/golang/sync
go get github.com/golang/text
go get github.com/golang/time
go get github.com/golang/lint
go get github.com/golang/exp
go get github.com/golang/perf

mv $GOPATH/src/github.com/golang/net $GOPATH/src/golang.org/x/net
mv $GOPATH/src/github.com/golang/tools $GOPATH/src/golang.org/x/tools
mv $GOPATH/src/github.com/golang/crypto $GOPATH/src/golang.org/x/crypto
mv $GOPATH/src/github.com/golang/sys $GOPATH/src/golang.org/x/sys
mv $GOPATH/src/github.com/golang/sync $GOPATH/src/golang.org/x/sync
mv $GOPATH/src/github.com/golang/text $GOPATH/src/golang.org/x/text
mv $GOPATH/src/github.com/golang/time $GOPATH/src/golang.org/x/time
mv $GOPATH/src/github.com/golang/lint $GOPATH/src/golang.org/x/lint
mv $GOPATH/src/github.com/golang/exp $GOPATH/src/golang.org/x/exp
mv $GOPATH/src/github.com/golang/perf $GOPATH/src/golang.org/x/perf
```
