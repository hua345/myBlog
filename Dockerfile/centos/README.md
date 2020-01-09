# 构建Docker镜像

```bash
# 查看最新的centos版本
docker run centos cat /etc/redhat-release
CentOS Linux release 8.0.1905 (Core)

# 构建镜像
docker build -t my/centos:latest .

# 删除镜像
docker run --rm  my/centos
```

## docker 网络设置

```bash
vi /etc/docker/daemon.json
{
  "dns" : [
    "223.5.5.5",
    "223.6.6.6",
    "8.8.8.8",
    "8.8.4.4"
  ]
}
```
