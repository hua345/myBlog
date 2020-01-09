#### 参考
 - [kubernetes1.13.1+etcd3.3.10+flanneld0.10集群部署](https://www.kubernetes.org.cn/5025.html)
#### 1.主要组件说明
- `Kubernetes` 集群中主要存在两种类型的节点，分别是 `master` 节点，以及 `minion` 节点。
- `Minion` 节点是实际运行 `Docker` 容器的节点，负责和节点上运行的 `Docker` 进行交互，并且提供了代理功能。
- `Master` 节点负责对外提供一系列管理集群的 API 接口，并且通过和 `Minion` 节点交互来实现对集群的操作管理。
- `apiserver`：用户和 `kubernetes` 集群交互的入口，封装了核心对象的增删改查操作，提供了 RESTFul 风格的 API 接口，通过 etcd 来实现持久化并维护对象的一致性。
- `scheduler`：负责集群资源的调度和管理，例如当有 pod 异常退出需要重新分配机器时，scheduler 通过一定的调度算法从而找到最合适的节点。
- `controller-manager`：主要是用于保证 replicationController 定义的复制数量和实际运行的 pod 数量一致，另外还保证了从 service 到 pod 的映射关系总是最新的。
- `kubelet`：运行在 minion 节点，负责和节点上的 Docker 交互，例如启停容器，监控运行状态等。
- `proxy`：运行在 minion 节点，负责为 pod 提供代理功能，会定期从 etcd 获取 service 信息，并根据 service 信息通过修改 iptables 来实现流量转发（最初的版本是直接通过程序提供转发功能，效率较低。），将流量转发到要访问的 pod 所在的节点上去。
- `etcd`：key-value键值存储数据库，用来存储kubernetes的信息的。
- `flannel`：`Flannel` 是 CoreOS 团队针对 Kubernetes 设计的一个覆盖网络（Overlay Network）工具，需要另外下载部署。我们知道当我们启动 Docker 后会有一个用于和容器进行交互的 IP 地址，如果不去管理的话可能这个 IP 地址在各个机器上是一样的，并且仅限于在本机上进行通信，无法访问到其他机器上的 Docker 容器。Flannel 的目的就是为集群中的所有节点重新规划 IP 地址的使用规则，从而使得不同节点上的容器能够获得同属一个内网且不重复的 IP 地址，并让属于不同节点上的容器能够直接通过内网 IP 通信。
#### 2.1环境信息
| Ip | etcdName|k8s节点及功能|Host|
|------------|---------------|---------|-----------|
|192.168.137.89|etcd01|etcd、registry、kube-apiserver、kube-controller-manager、kube-scheduler|k8s-master|
|192.168.137.105|etcd02|etcd、kubelet、docker、kube_proxy|k8s-node01|
|192.168.137.97|etcd03|etcd、kubelet、docker、kube_proxy|k8s-node02|

#### 2.2设置主机名
master上执行
```
hostnamectl --static set-hostname k8s-master
```

node01上执行：
```
hostnamectl --static set-hostname k8s-node01
```
node02上执行：
```
hostnamectl --static set-hostname k8s-node02
```
在三台机器上设置hosts，均执行如下命令：
```
echo '192.168.137.89   k8s-master
192.168.137.89   registry
192.168.137.105   k8s-node01
192.168.137.97    k8s-node02' >> /etc/hosts
```
#### 2.3关闭三台机器上的防火墙
```
systemctl disable firewalld.service
systemctl stop firewalld.service
```
#### 3.1 [部署etcd](https://github.com/hua345/dockerBlog/blob/master/etcd%E9%9B%86%E7%BE%A4%E6%90%AD%E5%BB%BA.md)
k8s运行依赖etcd，需要先部署etcd
可以参考[etcd集群搭建.md](./etcd集群搭建.md)
```bash
[root@k8s-master ~]# etcdctl member list
98665f721f5a04bc: name=etcd02 peerURLs=http://192.168.137.105:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.105:2379 isLeader=false
b25b7cce630db8e4: name=etcd01 peerURLs=http://192.168.137.89:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.89:2379 isLeader=false
dd4948cb7ad732bb: name=etcd03 peerURLs=http://192.168.137.97:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.97:2379 isLeader=true
```
#### 3.2 [部署docker私有仓库](https://github.com/hua345/dockerBlog/blob/master/CentOS%E6%90%AD%E5%BB%BADocker%E7%A7%81%E6%9C%89%E4%BB%93%E5%BA%93.md)
可以参考[CentOS搭建Docker私有仓库.md](./CentOS搭建Docker私有仓库.md)
```bash
[root@k8s-master ~]# docker images
REPOSITORY           TAG                 IMAGE ID            CREATED             SIZE
docker.io/registry   latest              f32a97de94e1        4 weeks ago         25.8 MB
[root@k8s-master ~]# docker run -d -p 5000:5000 registry
928b48650dc47c617c08ba3c1dda8a2e7a9307fe13e9b5492bf05e5611f2ca51
[root@k8s-master ~]# docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
928b48650dc4        registry            "/entrypoint.sh /e..."   4 seconds ago       Up 2 seconds        0.0.0.0:5000->5000/tcp   modest_mcnulty
[root@k8s-node02 ~]# docker push registry:5000/ubuntu

```
#### 4.部署Master
#### 4.1安装docker和kubernate
```bash
[root@k8s-master ~]# yum install docker kubernetes -y
Installed:
  kubernetes.x86_64 0:1.5.2-0.7.git269f928.el7

Dependency Installed:
  conntrack-tools.x86_64 0:1.4.4-4.el7
  kubernetes-client.x86_64 0:1.5.2-0.7.git269f928.el7
  kubernetes-master.x86_64 0:1.5.2-0.7.git269f928.el7
  kubernetes-node.x86_64 0:1.5.2-0.7.git269f928.el7
  libnetfilter_cthelper.x86_64 0:1.0.0-9.el7
  libnetfilter_cttimeout.x86_64 0:1.0.0-6.el7
  libnetfilter_queue.x86_64 0:1.0.2-2.el7_2
  socat.x86_64 0:1.7.3.2-2.el7
```
#### 4.2配置并启动kubernetes
在kubernetes master上需要运行以下组件：
- Kubernets API Server
- Kubernets Controller Manager
- Kubernets Scheduler

#### 4.2.1编辑`/etc/kubernetes/apiserver`
```
###
# kubernetes system config
#
# The following values are used to configure the kube-apiserver
#

# The address on the local server to listen to.
KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"

# The port on the local server to listen on.
KUBE_API_PORT="--port=8080"

# Port minions listen on
# KUBELET_PORT="--kubelet-port=10250"

# Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd-servers=http://192.168.137.89:2379,http://192.168.137.105:2379,http://192.168.137.97:2379"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# default admission control policies
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"

# Add your own!
KUBE_API_ARGS=""
```
- `KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"`
- `KUBE_ETCD_SERVERS="--etcd-servers=http://192.168.137.89:2379,http://192.168.137.105:2379,http://192.168.137.97:2379`
- `KUBE_API_PORT="--port=8080"`

#### 4.2.2编辑`/etc/kubernetes/config`
```
###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the controller-manager, scheduler, and proxy find the apiserver
KUBE_MASTER="--master=http://k8s-master:8080"
```
- `KUBE_MASTER="--master=http://k8s-master:8080"`
#### 4.3启动Master上的三个服务
```bash
systemctl start kube-apiserver
systemctl start kube-controller-manager
systemctl start kube-scheduler
systemctl enable kube-apiserver
systemctl enable kube-controller-manager
systemctl enable kube-scheduler
```
#### 5.部署Node
#### 5.1安装docker和kubernate
```bash
[root@k8s-node01 ~]# yum install docker kubernetes -y
Installed:
  kubernetes.x86_64 0:1.5.2-0.7.git269f928.el7

Dependency Installed:
  conntrack-tools.x86_64 0:1.4.4-4.el7
  kubernetes-client.x86_64 0:1.5.2-0.7.git269f928.el7
  kubernetes-master.x86_64 0:1.5.2-0.7.git269f928.el7
  kubernetes-node.x86_64 0:1.5.2-0.7.git269f928.el7
  libnetfilter_cthelper.x86_64 0:1.0.0-9.el7
  libnetfilter_cttimeout.x86_64 0:1.0.0-6.el7
  libnetfilter_queue.x86_64 0:1.0.2-2.el7_2
  socat.x86_64 0:1.7.3.2-2.el7
```
#### 5.2配置并启动kubernetes
在kubernetes node上需要运行以下组件：
- Kubelet
- Kubernets Proxy
#### 5.3.1编辑`/etc/kubernetes/config`
```bash
###
# kubernetes system config
#
# The following values are used to configure various aspects of all
# kubernetes services, including
#
#   kube-apiserver.service
#   kube-controller-manager.service
#   kube-scheduler.service
#   kubelet.service
#   kube-proxy.service
# logging to stderr means we get it in the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow-privileged=false"

# How the controller-manager, scheduler, and proxy find the apiserver
KUBE_MASTER="--master=http://k8s-master:8080"
```
- `KUBE_MASTER="--master=http://k8s-master:8080"`
#### 5.3.2编辑`/etc/kubernetes/kubelet`
```
###
# kubernetes kubelet (minion) config

# The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
KUBELET_ADDRESS="--address=0.0.0.0"

# The port for the info server to serve on
# KUBELET_PORT="--port=10250"

# You may leave this blank to use the actual hostname
KUBELET_HOSTNAME="--hostname-override=k8s-node01"

# location of the api-server
KUBELET_API_SERVER="--api-servers=http://k8s-master:8080"

# pod infrastructure container
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest"

# Add your own!
KUBELET_ARGS=""
```
- `KUBELET_ADDRESS="--address=0.0.0.0"`
- `KUBELET_HOSTNAME="--hostname-override=k8s-node01"`
- `KUBELET_API_SERVER="--api-servers=http://k8s-master:8080"`
#### 5.4分别启动kubernetes node服务
```bash
systemctl start kubelet
systemctl start kube-proxy
systemctl enable kubelet
systemctl enable kube-proxy
```
#### 6.查看状态
在master上查看集群中节点及节点状态
```
[root@k8s-master ~]# kubectl get nodes
NAME         STATUS    AGE
k8s-node01   Ready     1m
k8s-node02   Ready     1m
[root@k8s-master ~]# kubectl -s http://k8s-master:8080 get node
NAME         STATUS    AGE
k8s-node01   Ready     1m
k8s-node02   Ready     1m
```
#### 7.创建覆盖网络——Flannel
#### 7.1安装Flannel
在master、node上均执行如下命令，进行安装
```
yum install flannel -y
```
#### 7.2配置Flannel
master、node上均编辑`/etc/sysconfig/flanneld`
如果都部署了etcd集群就不需要修改
```
# Flanneld configuration options

# etcd url location.  Point this to the server where etcd runs
FLANNEL_ETCD_ENDPOINTS="http://192.168.137.89:2379,http://192.168.137.105:2379,http://192.168.137.97:2379"

# etcd config key.  This is the configuration key that flannel queries
# For address range assignment
FLANNEL_ETCD_PREFIX="/atomic.io/network"

# Any additional options that you want to pass
#FLANNEL_OPTIONS=""
```
- `FLANNEL_ETCD_ENDPOINTS="http://192.168.137.89:2379,http://192.168.137.105:2379,http://192.168.137.97:2379"`
#### 7.3配置etcd中关于flannel的key
Flannel使用Etcd进行配置，来保证多个Flannel实例之间的配置一致性，所以需要在etcd上进行如下配置：（‘/atomic.io/network/config’这个key与上文/etc/sysconfig/flannel中的配置项FLANNEL_ETCD_PREFIX是相对应的，错误的话启动就会出错）
```
[root@k8s-master ~]# etcdctl mk /atomic.io/network/config '{ "Network": "10.0.0.0/16" }'
{ "Network": "10.0.0.0/16" }
# 若要重新建，先删除
[root@k8s-master ~]# etcdctl rm /coreos.com/network/ --recursive
```
#### 7.4启动Flannel
#### 7.4.1在master执行：
```
systemctl enable flanneld
systemctl start flanneld
systemctl restart docker
systemctl restart kube-apiserver
systemctl restart kube-controller-manager
systemctl restart kube-scheduler
```
#### 7.4.2在node上执行：
```
systemctl enable flanneld
systemctl start flanneld
systemctl restart docker
systemctl restart kubelet
systemctl restart kube-proxy
```
#### 7.5验证Flannel服务
```
cat /run/flannel/subnet.env
FLANNEL_NETWORK=10.0.0.0/16
FLANNEL_SUBNET=10.0.10.1/24
FLANNEL_MTU=1472
FLANNEL_IPMASQ=false
```
```
[root@k8s-master ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:01:6b:08 brd ff:ff:ff:ff:ff:ff
    inet 192.168.137.89/24 brd 192.168.137.255 scope global noprefixroute dynamic eth0
       valid_lft 579383sec preferred_lft 579383sec
    inet6 fe80::d2f3:edc2:6f88:9e2e/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    link/ether 02:42:6e:89:dc:82 brd ff:ff:ff:ff:ff:ff
    inet 10.0.10.1/24 scope global docker0
       valid_lft forever preferred_lft forever
    inet6 fe80::42:6eff:fe89:dc82/64 scope link
       valid_lft forever preferred_lft forever
8: flannel0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1472 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none
    inet 10.0.10.0/16 scope global flannel0
       valid_lft forever preferred_lft forever
    inet6 fe80::8c2c:cbdb:d4d3:17f9/64 scope link flags 800
       valid_lft forever preferred_lft forever
```
#### 8.查看k8s状态
```
[root@k8s-master ~]# kubectl get cs,nodes
NAME                    STATUS    MESSAGE             ERROR
cs/scheduler            Healthy   ok
cs/controller-manager   Healthy   ok
cs/etcd-2               Healthy   {"health":"true"}
cs/etcd-1               Healthy   {"health":"true"}
cs/etcd-0               Healthy   {"health":"true"}

NAME            STATUS    AGE
no/k8s-node01   Ready     40m
no/k8s-node02   Ready     40m

```
