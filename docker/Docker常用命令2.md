# 列出本地镜像

```bash
docker images
REPOSITORY                             TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
ubuntu                                 latest              921181ee92a9        8 weeks ago         251.1 MB
centos                                 latest              95fafe0db800        9 weeks ago         292.3 MB


```

## 拉取镜像

```bash
sudo docker pull index.tenxcloud.com/tenxcloud/ubuntu:14.04
#拉取后可以修改tag成短标签
docker pull index.tenxcloud.com/tenxcloud/ubuntu:14.04 ubuntu:14.04
```

## 启动容器

```bash
docker run --help
  -a, --attach=[]            Attach to STDIN, STDOUT or STDERR
  -d, --detach=false         Run container in background and print container ID
  -e, --env=[]               Set environment variables
  --expose=[]                Expose a port or a range of ports
  -h, --hostname=            Container host name
  -i, --interactive=false    Keep STDIN open even if not attached
  --link=[]                  Add link to another container
  --lxc-conf=[]              Add custom lxc options
  --name=                    Assign a name to the container
  -P, --publish-all=false    Publish all exposed ports to random ports
  -p, --publish=[]           Publish a container's port(s) to the host
  -t, --tty=false            Allocate a pseudo-TTY
  -v, --volume=[]            Bind mount a volume
  --volumes-from=[]          Mount volumes from the specified container(s)
  -w, --workdir=             Working directory inside the container
```

```bash
# 输出一个 “Hello World”，之后终止容器
sudo docker run ubuntu:14.04 /bin/echo 'Hello world'

# 启动一个 bash 终端，允许用户进行交互
sudo docker run -t -i ubuntu:14.04 /bin/bash
```

## 守护态运行

```bash
#在后台以守护态（Daemonized）形式运行。
sudo docker run -d ubuntu:14.04 /bin/sh -c "while true; do echo hello world; sleep 1; done"
12ce4ef2b10862054ca4b7c17cd54a66f5d8601812074f81c1cc5788c1694ee9
#容器启动后会返回一个唯一的 id，也可以通过 docker ps 命令来查看容器信息。
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS               NAMES
12ce4ef2b108        ubuntu:14.04        "/bin/sh -c 'while t   51 seconds ago      Up 50 seconds                           ecstatic_hopper
#要获取容器的输出信息，可以通过 docker logs 命令
sudo docker logs 12ce4ef2b108
```

## 终止容器

```bash
#可以使用 docker stop 来终止一个运行中的容器。
sudo docker stop 12ce4ef2b108
#终止状态的容器可以用 docker ps -a 命令看到
#处于终止状态的容器，可以通过 docker start 命令来重新启动。
```

## 进入容器

```bash
sudo docker run -t -i -d ubuntu:14.04 /bin/bash

sudo docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
0c0b3f2a8a5a        ubuntu:14.04        "/bin/bash"         5 seconds ago       Up 4 seconds                            insane_payne

#attach    Attach to a running container
sudo docker attach insane_payne

#但是使用 attach 命令有时候并不方便。当多个窗口同时 attach 到同一个容器的时候，所有窗口都会同步显示。当某个窗口因命令阻塞时,其他窗口也无法执行操作了。

#nsenter 可以访问另一个进程的名字空间。nsenter 要正常工作需要有 root 权限。
#nsenter 工具在 util-linux 包2.23版本后包含。
#查看nsenter版本, sudo nsenter -V
nsenter，来自 util-linux 2.26.2

#为了连接到容器，你还需要找到容器的第一个进程的 PID，可以通过下面的命令获取。
PID=$(sudo docker inspect --format "{{ .State.Pid }}" <container>)
#通过这个 PID，就可以连接到这个容器：
sudo nsenter --target $PID --mount --uts --ipc --net --pid
```

## 数据卷

数据卷是一个可供一个或多个容器使用的特殊目录，它绕过 UFS，可以提供很多有用的特性：

- 数据卷可以在容器之间共享和重用
- 对数据卷的修改会立马生效
- 对数据卷的更新，不会影响镜像
- 卷会一直存在，直到没有容器使用

```bash
# 挂载一个主机目录作为数据卷，加载主机上~/localVolume目录挂载到容器/src目录
sudo docker run -d  -P -v ~/localVolume:/src --name node1  centos7-nodejs node /src/index.js
# -v ~/localVolume:/src：/ro   加了 :ro 之后，就挂载为只读了。

# 通过--volumes-from 来挂载 node1 容器中的数据卷
sudo docker run -d  -P --volumes-from=node1 --name node2  centos7-nodejs node /src/index.js
# 使用 --volumes-from 参数所挂载数据卷的容器自己并不需要保持在运行状态。
```

`0.0.0.0`代表本机所有 ip 地址，`127.0.0.1`只是本机环路地址, 访问 docker 服务需要监听`0.0.0.0`地址

```js
var http = require("http");

http
  .createServer(function(req, res) {
    res.writeHead(200, { "Content-Type": "text/plain" });
    res.end("Hello World\n");
  })
  .listen(1337, function(err) {
    if (err) throw err;
    console.log("Server Listening Port 1337");
  });
```

## 备份数据卷

首先使用 --volumes-from 标记来创建一个加载 node1 容器卷的容器，并从本地主机~/backup 目录挂载到容器的 /backup 目录。

```bash
sudo docker run --rm --volumes-from node1 -v ~/backup:/backup ubuntu tar cvf /backup/backup.tar /src
```

容器启动后，使用了 tar 命令来将 node1 卷备份为本地的 /backup/backup.tar

## 容器互连

使用 --link 参数可以让容器之间安全的进行交互。
--link 参数的格式为 --link name:alias，其中 name 是要链接的容器的名称，alias 是这个连接的别名。
Docker 通过 2 种方式为容器公开连接信息：

- 环境变量
- 更新 /etc/hosts 文件

使用 env 命令来查看 web 容器的环境变量

```bash
sudo docker run --rm --link node1:mynode centos7-nodejs env

HOSTNAME=4522b6290442
MYNODE_PORT=tcp://172.17.0.2:1337
MYNODE_PORT_1337_TCP=tcp://172.17.0.2:1337
MYNODE_PORT_1337_TCP_ADDR=172.17.0.2
MYNODE_PORT_1337_TCP_PORT=1337
MYNODE_PORT_1337_TCP_PROTO=tcp
MYNODE_NAME=/grave_blackwell/mynode
MYNODE_ENV_REFRESHED_AT=2015-06-05
REFRESHED_AT=2015-06-05
HOME=/root
```

除了环境变量，Docker 还添加 host 信息到父容器的 /etc/hosts 的文件。

```bash
sudo docker run -i -t  --rm  --link node1:mynode  centos7-nodejs /bin/bash

[root@e68252f63a06 /]# cat /etc/hosts
172.17.0.8    e68252f63a06
127.0.0.1    localhost
::1    localhost ip6-localhost ip6-loopback
fe00::0    ip6-localnet
ff00::0    ip6-mcastprefix
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
172.17.0.2    mynode e5f084bb6864 node1
[root@e68252f63a06 /]# ping node1
PING mynode (172.17.0.2) 56(84) bytes of data.
64 bytes from mynode (172.17.0.2): icmp_seq=1 ttl=64 time=0.165 ms
64 bytes from mynode (172.17.0.2): icmp_seq=2 ttl=64 time=0.075 ms

```

### 参照

- [Docker —— 从入门到实践](http://dockerpool.com/static/books/docker_practice/index.html)
