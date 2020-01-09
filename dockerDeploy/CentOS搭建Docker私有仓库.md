[hub.docker.com](https://hub.docker.com/_/registry)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190401185811433.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5qaDIxMw==,size_16,color_FFFFFF,t_70)
### 1.下载`registry`镜像
```bash
# docker pull <host>/<project>/<repo>:<tag>
$ docker pull registry.docker-cn.com/library/registry
$ docker images
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
registry.docker-cn.com/library/registry   latest              f32a97de94e1        3 weeks ago         25.8 MB
```
#### 2.启动本地私有仓库
```bash
# docker tag <img_name>:<tag> <host>/<project>/<repo>:<tag>
$ docker tag registry.docker-cn.com/library/registry registry
$ docker run -d -p 5000:5000 registry
e3782ea6fc6de52ddd31b5f1e056dd3d35518fea7294de3ce36f2784a5680a63
```
#### 3.简单推送容器到私有仓库
```bash
$ docker pull ubuntu
# docker tag <img_name>:<tag> <host>/<project>/<repo>:<tag>
$ docker tag ubuntu localhost:5000/ubuntu
# docker push <host>/<project>/<repo>:<tag>
$ docker push localhost:5000/ubuntu
```
默认情况下，会将仓库存放于容器内的`/var/lib/registry`目录下，这样如果容器被删除，则存放于容器中的镜像也会丢失，所以我们一般情况下会指定本地一个目录挂载到容器内的`/var/lib/registry`下，
```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
ac61b29b7993        registry            "/entrypoint.sh /e..."   4 seconds ago       Up 2 seconds        0.0.0.0:5000->5000/tcp   jovial_lovelace

# 进入registry容器查看docker保存位置
$ docker exec -it ac61b29b7993 sh
/ # find / -name registry
/bin/registry
/etc/docker/registry
/tmp/registry
/var/lib/registry
/var/lib/registry/docker/registry
```
#### 4.开放注册https协议
```
vi  /etc/docker/daemon.json
#添加配置文件
{"insecure-registries":["registry:5000"] }
#重启服务
systemctl restart docker
```
#### 5.挂载本地路径到镜像服务器
`--restart=always` 表示自动启动容器 
`-v <宿主机目录>:<容器目录> `将宿主机的目录映射到容器上 
`--privileged=true` 给容器加权限，这样上传就不会因为目录权限出错 
`/var/lib/registry` 这个目录是docker私有仓库，镜像的存储目录 
```bash
$ docker stop ac61b29b7993
$ docker run -d -p 5000:5000 --name=registry --restart=always --privileged=true -v ~/data/registry:/var/lib/registry registry
f6ab8faaac24c332358abccc9230cc140e83dc63ae6c9739c6020e79c7ec0b3a
# docker tag <img_name>:<tag> <host>/<project>/<repo>:<tag>
$ docker tag ubuntu 192.168.137.196:5000/ubuntu
# docker push <host>/<project>/<repo>:<tag>
$ docker push 192.168.137.196:5000/ubuntu
The push refers to a repository [192.168.137.196:5000/ubuntu]
4b7d93055d87: Pushed
663e8522d78b: Pushed
283fb404ea94: Pushed
bebe7ce6215a: Pushed
latest: digest: sha256:be159ff0e12a38fd2208022484bee14412680727ec992680b66cdead1ba76d19 size: 1150
```
#### 6.1Https协议问题
```
[root@k8s-master ~]#  docker push registry:5000/redis
The push refers to a repository [registry:5000/redis]
Get https://registry:5000/v1/_ping: http: server gave HTTP response to HTTPS client
```
这个问题可能是由于客户端采用https，docker registry未采用https服务所致。
```
vi  /etc/docker/daemon.json
#添加配置文件
{"insecure-registries":["registry:5000"] }
#重启服务
systemctl restart docker
```
#### 6.2上传时一直Retrying
上传镜像的时候，上传不上去，导致这个问题的原因是，权限不够，需要给这个容器扩展的特权
```
--privileged=true
```
