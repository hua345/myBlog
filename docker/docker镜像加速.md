# 镜像搜索地址

```bash
# 七牛云
https://hub.qiniu.com/home
# 官方地址
https://hub.docker.com/
# 阿里地址，需要登录
https://cr.console.aliyun.com/cn-hangzhou/instances/images
```

## Docker 中国官方镜像加速

您可以使用以下命令直接从该镜像加速地址进行拉取：

```bash
docker pull registry.docker-cn.com/myname/myrepo:mytag

docker pull registry.docker-cn.com/library/ubuntu:16.04
```

## 阿里镜像加速器

```bash
vi /etc/docker/daemon.json
{
  "registry-mirrors": ["https://umqazjiq.mirror.aliyuncs.com"]
}
```

```bash
systemctl restart docker
```
