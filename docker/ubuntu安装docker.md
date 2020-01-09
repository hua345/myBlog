# Docker简介

Docker 是一个开源的应用容器引擎，可以轻松的为任何应用创建一个轻量级的、可移植的、自给自足的容器。利用 Linux 的 LXC、AUFS、Go 语言、cgroup 实现了资源的独立，可以很轻松的实现文件、资源、网络等隔离，其最终的目标是实现类似 PaaS 平台的应用隔离。

docker 需要 64 位系统并且内核版本至少为 3.10.x，如果内核低于 3.10.x 需要先升级内核，并且内核包含了 aufs 模块。
查看当前内核版本

```bash
uname -r
3.19.0-15-generic
```

查看内核是否安装 aufs 模块

```bash
grep aufs /proc/filesystems
nodev   aufs
```

## 官方脚本安装

```bash
sudo curl -sSL https://get.docker.com/ | sh
docker version
```

## 编译安装

通过文档和代码了解到 docker 官方推荐的是在 docker 本身的容器里面搭建环境和编译，官方给出的是一个基于 ubuntu 的 dockerfile。所以要先安装 docker。

```bash
#由于docker是由golang语言写的，源码管理是用Git,所以需要先安装git，golang，make
sudo git clone https://github.com/docker/docker.git
cd docker
#查看已经存在的tag
git tag
git checkout -b v1.8.0
```

如果访问外国网速比较慢的话,编辑`Dockerfile`文件。

```bash
#更换apt-get源为http://mirrors.163.com
RUN apt-get install -y curl && rm /etc/apt/sources.list && curl http://mirrors.163.com/.help/sources.list.trusty -o /etc/apt/sources.list
#安装ubuntu-zfs和libzfs-dev时需要保留
RUN     apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys E871F18B51E0147C77796AC81196BA81F6B0FC61
RUN     echo deb http://ppa.launchpad.net/zfs-native/stable/ubuntu trusty main > /etc/apt/sources.list.d/zfs.list
#更换lxc源为github
ENV LXC_VERSION 1.1.2
RUN  git clone https://github.com/lxc/lxc.git /usr/src/lxc/
RUN cd /usr/src/lxc \
&& git checkout -b lxc-${LXC_VERSION} \
    && ./configure \
    && make \
    && make install \
    && ldconfig
#更换golang源为golang中国http://www.golangtc.com/
ENV GO_VERSION 1.4.2
RUN curl  http://www.golangtc.com/static/go/go${GO_VERSION}.src.tar.gz | tar -v -C /usr/local -xz \
    && mkdir -p /go/bin
ENV PATH /go/bin:/usr/local/go/bin:$PATH
ENV GOPATH /go:/go/src/github.com/docker/docker/vendor
RUN cd /usr/local/go/src && ./make.bash --no-clean 2>&1
#更换ruby的gem源为https://ruby.taobao.org
# TODO replace FPM with some very minimal debhelper stuff
RUN gem sources --remove https://rubygems.org/ \
  && gem sources -a https://ruby.taobao.org/ \
&& gem install --no-rdoc --no-ri fpm --version 1.3.2

# Download man page generator
#删除-b切换分支,安装过程出现错误
git clone  https://github.com/cpuguy83/go-md2man.git
git clone  https://github.com/russross/blackfriday.git
```

```bash
make build && make binary
#编译生成的文件在
./bundles/1.9.0-dev/binary/docker-1.9.0-dev

cp ./bundles/1.9.0-dev/binary/docker-1.9.0-dev /usr/bin/docker

#安装apparmor和cgroup-lite
sudo apt-get install -y apparmor
sudo apt-get install -y cgroup-lite
```

[https://docs.docker.com/](https://docs.docker.com/)
[https://github.com/docker/docker](https://github.com/docker/docker)
[手动编译安装 docker 环境](http://www.cnblogs.com/yanghuahui/p/4326210.html)
[如何在"特殊"的网络环境下编译 Docker](http://www.throwexcept.com/article/1416337217093.html)
