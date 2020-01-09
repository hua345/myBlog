# Compose简介

> Compose 项目是 Docker 官方的开源项目，负责实现对 Docker 容器集群的快速编排。
>
> Compose 定位是 「定义和运行多个 Docker 容器的应用（Defining and running multicontainer Docker applications）」
>
> Compose 项目由 Python 编写，实现上调用了 Docker 服务提供的 API 来对容器进行管理。
> 因此，只要所操作的平台支持 Docker API，就可以在其上利用 Compose 来进行编排管理。

## Compose 安装

> `Compose` 可以通过`Python`的包管理工具`pip`进行安装，也可以直接下载编译好的二进制文件使用，甚至能够直接在`Docker`容器中运行

## 二进制包安装

在 Linux 上的也安装十分简单，从[Compose GitHub Release](https://github.com/docker/compose) 处直接下载编译好的二进制文件即可。

```bash
docker-compose-Linux-x86_64
chmod +x docker-compose-Linux-x86_64
mv docker-compose-Linux-x86_64 /usr/bin/docker-compose
```

## pip 安装

```bash
➜  ~ pip install docker-compose

➜  ~ docker-compose version
docker-compose version 1.24.0, build 0aa59064
docker-py version: 3.7.2
CPython version: 3.6.8
OpenSSL version: OpenSSL 1.1.0j  20 Nov 2018
```
