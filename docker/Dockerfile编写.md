# 基本结构

Dockerfile 由一行行命令语句组成，并且支持以 # 开头的注释行。

一般的，Dockerfile 分为四部分：基础镜像信息、维护者信息、镜像操作指令和容器启动时执行指令。

```bash
# pull Base image to use, this must be set as the first line
FROM ubuntu

MAINTAINER chenjianhua 2290910211@qq.com

# Commands to update the image
RUN apt-get update && apt-get install -y nginx
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

# Commands when creating a new container
CMD /usr/sbin/nginx
```

其中，一开始必须指明所基于的镜像名称，接下来推荐说明维护者信息。

后面则是镜像操作指令，例如 RUN 指令，RUN 指令将对镜像执行跟随的命令。每运行一条 RUN 指令，镜像添加新的一层，并提交。

最后是 CMD 指令，来指定运行容器时的操作命令。

## FROM

格式为 `FROM <image>`或`FROM <image>:<tag>`。

第一条指令必须为 FROM 指令。并且，如果在同一个 Dockerfile 中创建多个镜像时，可以使用多个 FROM 指令（每个镜像一次）

## MAINTAINER

格式为 `MAINTAINER <name>`，指定维护者信息。

## RUN

格式为 `RUN <command>` 或 `RUN ["executable", "param1", "param2"]`。
每条 RUN 指令将在当前镜像基础上执行指定命令，并提交为新的镜像。当命令较长时可以使用 \ 来换行。

## CMD

支持三种格式

- `CMD ["executable","param1","param2"]`使用 exec 执行，推荐方式；
- `CMD command param1 param2` 在 `/bin/sh` 中执行，提供给需要交互的应用；
- `CMD ["param1","param2"]` 提供给`ENTRYPOINT`的默认参数；

指定启动容器时执行的命令，每个 Dockerfile 只能有一条 CMD 命令。如果指定了多条命令，只有最后一条会被执行。

如果用户启动容器时候指定了运行的命令，则会覆盖掉 CMD 指定的命令。

## EXPOSE

格式为 `EXPOSE <port> [<port>...]`。
告诉 Docker 服务端容器暴露的端口号，供互联系统使用。在启动容器时需要通过 -P，Docker 主机会自动分配一个端口转发到指定的端口。

## ENV

格式为 ENV `<key> <value>`。 指定一个环境变量，会被后续 RUN 指令使用，并在容器运行时保持。

## ADD

格式为 `ADD <src> <dest>`。

该命令将复制指定的 `<src>`到容器中的`<dest>`。 其中`<src>` 可以是 Dockerfile 所在目录的一个相对路径；也可以是一个`URL`；还可以是一个 tar 文件（自动解压为目录）。

## COPY

格式为 `COPY <src> <dest>`。
复制本地主机的`<src>`（为 Dockerfile 所在目录的相对路径）到容器中的 `<dest>`。
当使用本地目录为源目录时，推荐使用 COPY。

## ENTRYPOINT

程序入口点

- `ENTRYPOINT ["executable", "param1", "param2"]`
- `ENTRYPOINT command param1 param2（shell中执行）`。

配置容器启动后执行的命令，并且不可被 docker run 提供的参数覆盖。
每个 Dockerfile 中只能有一个 ENTRYPOINT，当指定多个时，只有最后一个起效。

## VOLUME

格式为 `VOLUME ["/data"]`。
创建一个可以从本地主机或其他容器挂载的挂载点，一般用来存放数据库和需要保持的数据等。

## WORKDIR

格式为 `WORKDIR /path/to/workdir`。
为后续的`RUN、CMD、ENTRYPOINT`指令配置工作目录。
可以使用多个 `WORKDIR`指令，后续命令如果参数是相对路径，则会基于之前命令指定的路径。例如

```Dockerfile
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

则最终路径为 /a/b/c。

## ONBUILD

格式为 `ONBUILD [INSTRUCTION]`。
配置当所创建的镜像作为其它新创建镜像的基础镜像时，所执行的操作指令。
例如，`Dockerfile`使用如下的内容创建了镜像 `image-A`。

```Dockerfile
[...]
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
[...]
```

如果基于 image-A 创建新的镜像时，新的 Dockerfile 中使用 FROM image-A 指定基础镜像时，会自动执行 ONBUILD 指令内容，等价于在后面添加了两条指令。

```Dockerfile
FROM image-A

#Automatically run the following
ADD . /app/src
RUN /usr/local/bin/python-build --dir /app/src
```

### 简单示例

```Dockerfile
# Base image to use, this must be set as the first line
FROM ubuntu

# Maintainer: docker_user <docker_user at email.com> (@docker_user)
MAINTAINER docker_user docker_user@email.com

# Commands to update the image

RUN cd /etc/apt && \
wget http://mirrors.163.com/.help/sources.list.trusty  && \
rm /etc/apt/sources.list && \
mv /etc/apt/sources.list.trusty /etc/apt/sources.list && \
apt-get update && \
apt-get install redis-server -y && \
sed -i 's/^\(bind .*\)$/# \1/' /etc/redis/redis.conf && \
sed -i 's/^\(daemonize .*\)$/# \1/' /etc/redis/redis.conf && \
sed -i 's/^\(dir .*\)$/# \1\ndir \/data/' /etc/redis/redis.conf && \
apt-get clean

ENV REDIS_DIR /data

# Define mountable directories.
VOLUME ["/data"]

# Expose ports.
EXPOSE 6379

# Commands when creating a new container
# Define default command.
CMD ["redis-server", "/etc/redis/redis.conf"]
```

### 创建镜像

编写完成 Dockerfile 之后，可以通过 docker build 命令来创建镜像。
基本的格式为 docker build [选项] 路径，该命令将读取指定路径下（包括子目录）的 Dockerfile，并将该路径下所有内容发送给 Docker 服务端，由服务端来创建镜像。因此一般建议放置 Dockerfile 的目录为空目录。也可以通过`.dockerignore`文件（每一行添加一条匹配模式）来让 Docker 忽略路径下的目录和文件。

```bash
sudo docker build .
```

### 参照

- [Docker —— 从入门到实践](http://dockerpool.com/static/books/docker_practice/dockerfile/instructions.html)
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Dockerfile redis](https://github.com/dockerfile/redis/blob/master/Dockerfile#L21)
