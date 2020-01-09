#### 参考
- [设置Golang的GOPATH](https://github.com/hua345/golangBlog/blob/master/设置Golang的GOPATH.md)

#### 构建脚本
```bash
docker build -t my/golang:v1.12.5 .
```
#### 查看etcd版本
```
docker run --rm my/golang:v1.12.5 go version
```