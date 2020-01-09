# 查看 docker 信息（version、info）

```shell
#查看docker版本
$docker version
# 显示docker系统的信息
$docker info
```

## 对 image 的操作

```bash
# 检索image
$ docker search image_name
```

```bash
# 下载image
$ docker pull image_name
```

```bash
# 查看本地已经有哪些镜像
$ docker images
//docker images -notrunc=true获得完整的镜像ID
```

```bash
# 删除给定若干个image
$ docker rmi image_name
```

```bash
# 显示一个image的历史;
$ docker history image_name
```

## 创建新的容器:run

docker 容器可以理解为在沙盒中运行的进程。这个沙盒包含了该进程运行所必须的资源，包括文件系统、系统类库、shell 环境等等。但这个沙盒默认是不会运行任何程序的。你需要在沙盒中运行一个进程来启动某一个容器。这个进程是该容器的唯一进程，所以当该进程结束的时候，容器也会完全的停止。

```bash
//在容器中运行"echo"命令，输出"hello word"
$ docker run ubuntu echo "hello world"
hello world
```

```bash
#交互式进入容器中
#-i参数, Keep STDIN open even if not attached(将docker控制台与容器关联)
#-t参数, Allocate a pseudo-TTY(分配一个伪终端)
$ docker run -i -t ubuntu bash
root@2bb9ca452f99:/# echo "hello world"
hello world
root@2bb9ca452f99:/# apt-get install -y curl
root@2bb9ca452f99:/# exit
exit
```

```bash
# 开启一个非常有用的长时间工作进程
# -d参数，容器后台运行并打印容器ID
CONTAINER_ID=$(docker run -d ubuntu sh -c "while true; do echo Hello World;sleep 1; done")
```

Note： 在执行 apt-get 命令的时候，要带上-y 参数。如果不指定-y 参数的话，apt-get 命令会进入交互模式，需要用户输入命令来进行确认，但在 docker 环境中是无法响应这种交互的。apt-get 命令执行完毕之后，容器就会停止，但对容器的改动不会丢失。

### 容器操作

```bash
$ docker ps //列出当前所有正在运行的container
# 参数-a， 列出所有的container
# 参数-l， 列出最近一次启动的container
# 参数 -q ，只列出容器 ID
```

```bash
#保存对容器的修改:commit
#当你对某一个容器做了修改之后（通过在容器中运行某一个命令），可以把对容器的修改保存下来，这样下次可以从保存后的最新状态运行该容器。

docker run learn/tutorial apt-get install -y curl
docker ps # 找到容器ID
485191de5d28        learn/tutorial:latest

docker commit  -m "install curl"  4851  linux/curl:v2
3d5c63acd1bdc95be9b2706a7a6ad91e90dac0a8df9699c7979379a631603635

docker run linux/curl curl www.baidu.com
```

```bash
# 删除已经停止的容器
docker container prune
# 删除指定容器
docker rm $CONTAINER_ID
```

```bash
# 停止、启动、杀死一个容器
docker stop $CONTAINER_ID
docker start $CONTAINER_ID
docker kill $CONTAINER_ID
```

```bash
# 查看一个容器日志
docker logs $CONTAINER_ID
```

```bash
# 列出一个容器里面被改变的文件或者目录，list列表会显示出三种事件，A 增加的，D 删除的，C 被改变的
docker diff $CONTAINER_ID
```

```bash
# 显示一个运行的容器里面的进程信息
docker top $CONTAINER_ID
```

```bash
# 从容器里面拷贝文件/目录到本地一个路径
docker cp Name:/container_path to_path
docker cp ID:/container_path to_path
```

```bash
# 重启一个正在运行的容器
docker restart $CONTAINER_ID
```

```bash
docker run -i -d learn/ping ping www.baidu.com
e31f8fcc91135fbe9d69d4b7e5d4cb1408dc4985110f9868cf7d73ade3c8b52d
# 附加到一个运行的容器上面
docker attach e31f
```

Note： attach 命令允许你查看或者影响一个运行的容器。Ctrl + C 退出。

### 收集有关容器和镜像的底层信息:inspect

容器实例的 IP 地址、端口绑定列表、特定的端口映射的搜索、收集配置的详细信息

```bash
docker ps
ee45f0638993        ubuntu:latest
docker inspect ee45  //精简ID
```

### 保存和加载镜像: save,load

当需要把一台机器上的镜像迁移到另一台机器的时候，需要保存镜像与加载镜像。

```bash
# 保存镜像到一个tar包;
docker save dockerfile/nginx > mynginx.tar
```

```bash
# 将mynginx.tar复制到机器b上
docker load < mynginx.tar
```

### 导入导出容器:import,export

```bash
docker export $container_id > mycontainer.tar
```

```bash
# 使用HTTP的URL从远程位置导入
docker import http://example.com/example.tar
# 本地文件导入需要使用 - 参数
docker import - mycontainer.tar
```

用户既可以使用 docker load 来导入镜像存储文件到本地镜像库，也可以使用 docker import 来导入一个容器快照到本地镜像库。这两者的区别在于容器快照文件将丢弃所有的历史记录和元数据信息（即仅保存容器当时的快照状态），而镜像存储文件将保存完整记录，体积也要大。

### 从一个 Dockerfile 创建一个镜像：build

```bash
docker build -t image_name Dockerfile_path
```

参考：

- [Docker 学习笔记(2)--Docker 常用命令](http://blog.csdn.net/we_shell/article/details/38368137?utm_source=tuicool)
- [ubuntu 下安装 Docker](http://www.cnblogs.com/linjiqin/p/3625609.html)
- [导出和导入容器](http://dockerpool.com/static/books/docker_practice/container/import_export.html)
