# 参考

- [https://hub.docker.com/_/redis](https://hub.docker.com/_/redis)\

## 构建脚本

```bash
docker build -t my/redis:v5.0.5 .
```

## 查看etcd版本

```bash
docker run -d -p 6379:6379 --name=redis --restart=always my/redis:v5.0.5
# 官方镜像，持久化数据
docker run --name some-redis -d -p 6379:6379 --restart=always redis:5.0.7 redis-server --appendonly yes

docker run -it --rm redis redis-cli -h some-redis
```

## 跨机器访问

```bash
docker run --name some-redis -d redis redis-server --appendonly yes
```
