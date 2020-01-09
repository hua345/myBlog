# Docker简介

> Docker 是一个开源的应用容器引擎，可以轻松的为任何应用创建一个轻量级的、可移植的、自给自足的容器。
>
> 利用 Linux 的 LXC、AUFS、Go 语言、cgroup 实现了资源的独立，可以很轻松的实现文件、资源、网络等隔离，其最终的目标是实现类似 PaaS 平台的应用隔离。
>
> docker 需要 64 位系统并且内核版本至少为`3.10.x`，如果内核低于`3.10.x`需要先升级内核，并且内核包含了`aufs`模块。

## 查看当前内核版本

```bash
uname -r
3.19.0-15-generic
```

## 查看内核是否安装 aufs 模块

```bash
grep aufs /proc/filesystems
nodev   aufs
```

## 1. 配置 docker 镜像

```bash
# step 1: 安装必要的一些系统工具
yum install -y yum-utils device-mapper-persistent-data lvm2
# Step 2: 添加软件源信息
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
# Step 3: 更新并安装 Docker-CE
yum makecache fast
```

## 2. 安装 docker

```bash
#先看一下有哪些可用版本：
yum list docker-ce --showduplicates | sort -r
#查看当前docker版本
yum info docker
#卸载老版本docker
yum remove docker docker-client \
                  docker-common \
                  docker-latest \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine
#安装docker-ce
yum install docker-ce
#启动docker：
systemctl enable docker --now
#查看服务状态：
systemctl status docker
#查看docker版本
[root@k8s-master ~]# docker version
Client: Docker Engine - Community
 Version:           19.03.5
 API version:       1.40
 Go version:        go1.12.12
 Git commit:        633a0ea
 Built:             Wed Nov 13 07:25:41 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.5
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.12
  Git commit:       633a0ea
  Built:            Wed Nov 13 07:24:18 2019
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.10
  GitCommit:        b34a5c8af56e510852c35414db4c1f4fa6172339
 runc:
  Version:          1.0.0-rc8+dev
  GitCommit:        3e425f80a8c931f88e6d94a8c831b9d5aa481657
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
```

## Cannot connect to the Docker daemon

```bash
docker info
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
#docker服务没有启动
#启动docker服务
systemctl start docker
```
