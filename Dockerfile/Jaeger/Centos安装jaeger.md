# 参考

## 下载jaeger

```bash
# https://github.com/jaegertracing/jaeger/releases
wget https://github.com/jaegertracing/jaeger/releases/download/v1.14.0/jaeger-1.14.0-linux-amd64.tar.gz
```

```bash
go get github.com/jaegertracing/jaeger
cd $GOPATH/src/github.com/jaegertracing/jaeger
make install
go run ./examples/hotrod/main.go all
```
