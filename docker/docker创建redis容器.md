# 下载 redis 数据库 image

```bash
docker pull dockerfile/redis #根据官方DockerFile下载并创建镜像
```

创建 redis 容器实例,我们使用了 Docker 的端口映射机制，从而我们就可以使用 Host 服务器的 IP 访问这些实例

```bash
docker run -d --name node1 -p 7001:6379 dockerfile/redis
docker run -d --name node2 -p 7002:6379 dockerfile/redis
docker run -d --name node3 -p 7003:6379 dockerfile/redis
```

docker ps 查看容器信息，0.0.0.0:7001->6379/tcp
Docker 虚拟机中的 6379 端口映射到了容器的 7001 端口

## 在容器之间建立连接

现在我们可以创建我们的应用程序容器，我们使用-link 参数来创建一个连接 redis 容器，我们使用别名 db,这将会在 redis 容器和 redis 实例容器中创建一个安全的通信隧道

```bash
sudo docker run --link node1:db -i -t ubuntu:lastest /bin/bash
```

进入我们刚才创建的容器，我们需要安装 redis 的 redis-cli 的二进制包来测试连接

```bash
sudo apt-get update
sudo git clone https://github.com/antirez/redis.git
sudo cd redis
sudo make && install
```

现在我们可以测试连接，首先我么要先查看下 web 应用程序容器的环境变量，我们可以用我们的 ip 和端口来连接 redis 容器

```bash
env | grep DB_
```

```conf
DB_NAME=/cranky_lumiere/db
DB_PORT_6379_TCP_PORT=6379
DB_PORT=tcp://172.17.0.9:6379
DB_PORT_6379_TCP=tcp://172.17.0.9:6379
DB_PORT_6379_TCP_ADDR=172.17.0.9
DB_PORT_6379_TCP_PROTO=tcp
```

我们可以看到我们有一个 DB 为前缀的环境变量列表，DB 来自指定别名连接我们的现在的容器，让我们使用 DB_PORT_6379_TCP_ADDR 变量连接到 Redis 容器。

```bash
redis-cli -h $DB_PORT_6379_TCP_ADDR
172.17.0.9:6379> ping
PONG
172.17.0.9:6379> set hello world
OK
172.17.0.9:6379> get hello
"world"
172.17.0.9:6379> exit
```

### 在 Host 服务器上与 docker 容器连接

> 我们需要重新看看这个虚拟网络的结构，要看整个网络的结构，我们应该先了解 Docker 的层次结构。在 Linux 中，Docker 的逻辑结构是这样的：
> **硬件 < Linux 系统（Docker Kernel） < Docker 容器**
> 在 Windows 中要运行 Docker，实际上是在虚拟机下运行的，所以在 Windows 中 Docker 的逻辑结构应该是：
> **硬件 < Windows 系统 < Docker 虚拟机（Docker Kernel） < Docker 容器。**
> 在 windows 下，我们只需进入 VirtualBox 中，将 Docker 虚拟机的网络做个桥接，或者端口映射就行了。
> 进入 VirtualBox 主界面，选中 Docker 虚拟机(boot2docker-vm)，单击设置按钮，在设置中选择网络，这里我们发现 Docker 虚拟机默认选择了“网络地址转换(NAT)”。

![Docker虚拟机的网络连接方式默认是NAT](http://img.blog.csdn.net/20150512202418305)
为虚拟机端口添加映射，将 windows 端口[9001~9003]映射到虚拟机端口[7001~7003]。其中 ssh 是 Docker 客户端和 Docker 虚拟机进行通信的端口。
![端口映射](http://img.blog.csdn.net/20150512202520687)
通过 windows 的 redis-cli 与服务器连接
![redis-cli连接](http://img.blog.csdn.net/20150512203059597)
参考:
[从 Docker 在 Linux 和 Windows 下的区别简单理解 Docker 的层次结构](http://www.cnblogs.com/bjfuouyang/p/3798421.html?utm_source=tuicool)
[利用 Docker 构建开发环境](http://tech.uc.cn/?p=2726)
[用 Docker 构建分布式 Redis 集群](http://dockone.io/article/180)
[Dockerizing a Redis Service](https://docs.docker.com/examples/running_redis_service/)
[Docker 中运行 Redis 服务](http://get.jobdeer.com/11.get)
