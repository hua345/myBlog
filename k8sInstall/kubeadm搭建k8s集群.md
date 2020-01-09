#### 1.kubeadm简介
kubeadm是Kubernetes官方提供的用于快速安装Kubernetes集群的工具.
kubeadm这个工具可以通过简单的kubeadm init和kubeadm join命令来创建一个kubernetes集群，
kubeadm提供的其他命令都比较通俗易懂：
- kubeadm init 启动一个master节点；
- kubeadm join 启动一个node节点，加入master；
- kubeadm upgrade 更新集群版本；
- kubeadm config 从1.8.0版本开始已经用处不大，可以用来view一下配置；
- kubeadm token 管理kubeadm join的token；
- kubeadm reset 把kubeadm init或kubeadm join做的更改恢复原状；
- kubeadm version打印版本信息；
- kubeadm alpha预览一些alpha特性的命令。

#### 2.环境准备
|ip|Host|
|--------------|--------------------|
|192.168.137.105|	k8s-master|
|192.168.137.89|	k8s-node01|
|192.168.137.97	|k8s-node02 |

#### 2.1设置主机名
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
cat <<EOF > /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.137.105   k8s-master
192.168.137.105   registry
192.168.137.89    k8s-node01
192.168.137.97    k8s-node02
EOF
```
#### 2.3配置yum源
```bash
cd /etc/yum.repos.d
# docker repo
curl -o docker-ce.repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

# k8s repo
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

#查看repo
yum repolist
repo id                      repo name                                    status
base/7/x86_64                CentOS-7 - Base - mirrors.aliyun.com         10,019
docker-ce-stable/x86_64      Docker CE Stable - x86_64                        39
extras/7/x86_64              CentOS-7 - Extras - mirrors.aliyun.com          385
kubernetes                   Kubernetes                                      336
updates/7/x86_64             CentOS-7 - Updates - mirrors.aliyun.com       1,493
repolist: 12,272
```
#### 2.4 配置selinux和firewalld
```
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config
# Stop and disable firewalld
systemctl disable firewalld --now
```
#### 2.5关闭交换空间
```
#查看是否有swap内存
#[ERROR Swap]: running with swap on is not supported. Please disable swap
[root@k8s-master ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:           2.1G        1.1G        145M         25M        909M        919M
Swap:          2.0G        264K        2.0G
#永久关闭交换空间
[root@k8s-master ~]# swapoff -a
#注释/etc/fstab中swap条目
#
# /etc/fstab
# Created by anaconda on Tue Apr  2 15:20:16 2019
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/centos-root /                       xfs     defaults        0 0
UUID=5fcc7098-93a5-4535-b34b-294085052969 /boot                   xfs     defaults        0 0
#/dev/mapper/centos-swap swap                    swap    defaults        0 0

#重启服务器
[root@k8s-master ~]# reboot
```
#### 2.6 设置bridge-nf-call-iptables
```
[ERROR FileContent--proc-sys-net-bridge-bridge-nf-call-iptables]: /proc/sys/net/bridge/bridge-nf-call-iptables contents are not set to 1
echo "1" >/proc/sys/net/bridge/bridge-nf-call-iptables
```
#### 2.7 设置ip_forward
```
[ERROR FileContent--proc-sys-net-ipv4-ip_forward]: /proc/sys/net/ipv4/ip_forward contents are not set to 1
echo "1" > /proc/sys/net/ipv4/ip_forward
```
#### 2.8 设置cgroupfs
```
[WARNING IsDockerSystemdCheck]: detected "cgroupfs" as the Docker cgroup driver. The recommended driver is "systemd". Please follow the guide at https://kubernetes.io/docs/setup/cri/
```
现在有两种方式, 一种是修改docker, 另一种是修改kubelet
#### 2.8.1 修改docker
```
#查看docker方式
[root@k8s-master ~]# docker info | grep 'Cgroup'
Cgroup Driver: systemd

# 修改或创建/etc/docker/daemon.json，加入下面的内容：
{
  "exec-opts": ["native.cgroupdriver=systemd"]
}

#重启docker
systemctl restart docker
```
#### 3.安装docker
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
Client:
 Version:           18.09.4
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        d14af54266
 Built:             Wed Mar 27 18:34:51 2019
 OS/Arch:           linux/amd64
 Experimental:      false
```
#### 4.安装kubeadm、kubelet和kubectl
```
#查看要安装的版本
[root@k8s-master ~]# yum info kubeadm
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirrors.aliyun.com
 * extras: mirrors.aliyun.com
 * updates: mirrors.aliyun.com
Available Packages
Name        : kubeadm
Arch        : x86_64
Version     : 1.14.0
Release     : 0
Size        : 8.7 M
Repo        : kubernetes
Summary     : Command-line utility for administering a Kubernetes cluster.
URL         : https://kubernetes.io
License     : ASL 2.0
Description : Command-line utility for administering a Kubernetes cluster.

# 检查老版本kubernetes是否安装
yum info kubernetes
#移除老版本kubernetes
yum remove kubernetes kubernetes-client kubernetes-node kubernetes-master
#移除老版本flanneld
yum remove flanneld
# 安装kubeadm
yum install kubelet kubeadm kubectl
#启动kubelet
systemctl enable --now kubelet

[root@k8s-master ~]# kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.0", GitCommit:"641856db18352033a0d96dbc99153fa3b27298e5", GitTreeState:"clean", BuildDate:"2019-03-25T15:51:21Z", GoVersion:"go1.12.1", Compiler:"gc", Platform:"linux/amd64"}
```

#### 5.容器镜像
```
#kubeadm列出需要的镜像
[root@k8s-master ~]# kubeadm config images list
k8s.gcr.io/kube-apiserver:v1.14.0
k8s.gcr.io/kube-controller-manager:v1.14.0
k8s.gcr.io/kube-scheduler:v1.14.0
k8s.gcr.io/kube-proxy:v1.14.0
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.3.10
k8s.gcr.io/coredns:1.3.1

docker pull docker.io/mirrorgooglecontainers/kube-apiserver-amd64:v1.14.0
docker pull docker.io/mirrorgooglecontainers/kube-controller-manager-amd64:v1.14.0
docker pull docker.io/mirrorgooglecontainers/kube-scheduler-amd64:v1.14.0
docker pull docker.io/mirrorgooglecontainers/kube-proxy-amd64:v1.14.0
docker pull mirrorgooglecontainers/pause-amd64:3.1
docker pull mirrorgooglecontainers/etcd-amd64:3.3.10
docker pull coredns/coredns:1.3.1

docker tag docker.io/mirrorgooglecontainers/kube-apiserver-amd64:v1.14.0 k8s.gcr.io/kube-apiserver:v1.14.0
docker tag docker.io/mirrorgooglecontainers/kube-controller-manager-amd64:v1.14.0 k8s.gcr.io/kube-controller-manager:v1.14.0
docker tag docker.io/mirrorgooglecontainers/kube-scheduler-amd64:v1.14.0 k8s.gcr.io/kube-scheduler:v1.14.0
docker tag docker.io/mirrorgooglecontainers/kube-proxy-amd64:v1.14.0 k8s.gcr.io/kube-proxy:v1.14.0
docker tag docker.io/mirrorgooglecontainers/pause-amd64:3.1 k8s.gcr.io/pause:3.1
docker tag docker.io/mirrorgooglecontainers/etcd-amd64:3.3.10 k8s.gcr.io/etcd:3.3.10
docker tag docker.io/coredns/coredns:1.3.1 k8s.gcr.io/coredns:1.3.1
```
#### 6.1安装k8s master
```
[root@k8s-master ~]# kubeadm init --kubernetes-version=v1.14.0 --pod-network-cidr=10.100.0.0/16
[init] Using Kubernetes version: v1.14.0
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Activating the kubelet service
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [k8s-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.137.105]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.137.105 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [k8s-master localhost] and IPs [192.168.137.105 127.0.0.1 ::1]
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 39.004761 seconds
[upload-config] storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.14" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --experimental-upload-certs
[mark-control-plane] Marking the node k8s-master as control-plane by adding the label "node-role.kubernetes.io/master=''"
[mark-control-plane] Marking the node k8s-master as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[kubelet-check] Initial timeout of 40s passed.
[bootstrap-token] Using token: mv1gaz.4m7imij92pbnudxq
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.137.105:6443 --token mv1gaz.4m7imij92pbnudxq \
    --discovery-token-ca-cert-hash sha256:a25cabc3255f644b5563052f31e2d45ec87e21cf4fa323d0021745fb93451018
```
#### 6.2配置环境变量
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

#### 6.3查看集群状态：
```
[root@k8s-master ~]# kubectl get node
NAME         STATUS     ROLES    AGE     VERSION
k8s-master   NotReady   master   2m50s   v1.14.1

[root@k8s-master ~]# kubectl get cs
NAME                 STATUS    MESSAGE             ERROR
controller-manager   Healthy   ok
scheduler            Healthy   ok
etcd-0               Healthy   {"health":"true"}

[root@k8s-master ~]# kubectl get pod -n kube-system
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-fb8b8dccf-dfwvt              0/1     Pending   0          87s
coredns-fb8b8dccf-slbgd              0/1     Pending   0          87s
etcd-k8s-master                      1/1     Running   0          24s
kube-apiserver-k8s-master            1/1     Running   0          40s
kube-controller-manager-k8s-master   1/1     Running   0          42s
kube-proxy-2zrr8                     1/1     Running   0          86s
kube-scheduler-k8s-master            1/1     Running   0          48s
```
#### 6.4安装网络插件flannel
由于网络功能是作为插件存在的，k8s本身并不提供网络功能，所有我们需要自行安装，这里我们选择flannel
```
[root@k8s-master ~]# docker pull quay.io/coreos/flannel:v0.11.0-amd64
[root@k8s-master ~]# wget  https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
[root@k8s-master ~]# kubectl apply -f kube-flannel.yml  

clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.extensions/kube-flannel-ds-amd64 created
daemonset.extensions/kube-flannel-ds-arm64 created
daemonset.extensions/kube-flannel-ds-arm created
daemonset.extensions/kube-flannel-ds-ppc64le created
daemonset.extensions/kube-flannel-ds-s390x created
```
#### 6.5查看集群状态
```
[root@k8s-master ~]# kubectl get node
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   20m   v1.14.1

[root@k8s-master ~]# kubectl get pod -n kube-system
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-fb8b8dccf-dfwvt              1/1     Running   0          15m
coredns-fb8b8dccf-slbgd              1/1     Running   0          15m
etcd-k8s-master                      1/1     Running   0          14m
kube-apiserver-k8s-master            1/1     Running   0          14m
kube-controller-manager-k8s-master   1/1     Running   0          14m
kube-flannel-ds-amd64-qj6dr          1/1     Running   0          12m
kube-proxy-2zrr8                     1/1     Running   0          15m
kube-scheduler-k8s-master            1/1     Running   0          15m

```
#### 6.6 kubeadm token
```
[root@k8s-master ~]# kubeadm token list
TOKEN                     TTL       EXPIRES                     USAGES                   DESCRIPTION                                                EXTRA GROUPS
0jw2r9.ip61hlppb6vjab5a   23h       2019-04-15T09:49:48+08:00   authentication,signing   The default bootstrap token generated by 'kubeadm init'.   system:bootstrappers:kubeadm:default-node-token

#生成新的token
[root@k8s-master ~]# kubeadm token create
iiyb51.qqtfqmfnpq3hca3m
#查看token列表
[root@k8s-master ~]# kubeadm token list
TOKEN                     TTL       EXPIRES                     USAGES                   DESCRIPTION                                                EXTRA GROUPS
0jw2r9.ip61hlppb6vjab5a   23h       2019-04-15T09:49:48+08:00   authentication,signing   The default bootstrap token generated by 'kubeadm init'.   system:bootstrappers:kubeadm:default-node-token
iiyb51.qqtfqmfnpq3hca3m   23h       2019-04-15T10:29:42+08:00   authentication,signing   <none>                                                     system:bootstrappers:kubeadm:default-node-token

#查看证书sha值
[root@k8s-master ~]# openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

b01b6bcab668f19294b08973783fc5adb54195dc4d6b24cd64f94537337c093b

#节点加入到集群
kubeadm join 192.168.137.105:6443 --token 0jw2r9.ip61hlppb6vjab5a \
    --discovery-token-ca-cert-hash sha256:b01b6bcab668f19294b08973783fc5adb54195dc4d6b24cd64f94537337c093b
```
#### 7.1加入节点到集群中
```
[root@k8s-node02 ~]# kubeadm join 192.168.137.105:6443 --token mv1gaz.4m7imij92pbnudxq     --discovery-token-ca-cert-hash sha256:a25cabc3255f644b5563052f31e2d45ec87e21cf4fa323d0021745fb93451018
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -oyaml'
[kubelet-start] Downloading configuration for the kubelet from the "kubelet-config-1.14" ConfigMap in the kube-system namespace
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Activating the kubelet service
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...

This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.

```
#### 7.2查看集群信息
```
[root@k8s-master ~]# kubectl get nodes
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   12h   v1.14.0
k8s-node01   Ready    <none>   28m   v1.14.0
k8s-node02   Ready    <none>   11h   v1.14.0

[root@k8s-master ~]# kubectl get pod -n kube-system
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-fb8b8dccf-hbzck              1/1     Running   0          12h
coredns-fb8b8dccf-w8mz9              1/1     Running   0          12h
etcd-k8s-master                      1/1     Running   0          12h
kube-apiserver-k8s-master            1/1     Running   0          12h
kube-controller-manager-k8s-master   1/1     Running   0          12h
kube-flannel-ds-amd64-hp7h8          1/1     Running   1          11h
kube-flannel-ds-amd64-mnzlg          1/1     Running   0          12h
kube-flannel-ds-amd64-x56wj          1/1     Running   0          27m
kube-proxy-dl9d8                     1/1     Running   0          27m
kube-proxy-p4mv5                     1/1     Running   0          12h
kube-proxy-x9th9                     1/1     Running   2          11h
kube-scheduler-k8s-master            1/1     Running   0          12h
```
#### 8.1卸载node
```
# master
kubectl drain k8s-node01 --delete-local-data --force --ignore-daemonsets
kubectl delete node k8s-node01
```
然后，在要删除的节点上，重置所有kubeadm安装状态：
```
# node
yum install net-tools -y
kubeadm reset


systemctl stop kubelet
systemctl stop docker
rm -rf /var/lib/cni/
rm -rf /var/lib/kubelet/*
rm -rf /etc/cni/
ifconfig cni0 down
ifconfig flannel.1 down
ifconfig docker0 down
ip link delete cni0
ip link delete flannel.1
systemctl start docker
```
#### 8.2卸载master
```
kubeadm reset
rm -rf $HOME/.kube
rm -rf /etc/kubernetes/
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

#### 9.出现的问题
#### 9.1 Init:ImagePullBackOff
```
[root@k8s-master ~]# kubectl get pod -n kube-system
NAME                                 READY   STATUS                  RESTARTS   AGE
coredns-fb8b8dccf-hbzck              1/1     Running                 0          11h
coredns-fb8b8dccf-w8mz9              1/1     Running                 0          11h
etcd-k8s-master                      1/1     Running                 0          11h
kube-apiserver-k8s-master            1/1     Running                 0          11h
kube-controller-manager-k8s-master   1/1     Running                 0          11h
kube-flannel-ds-amd64-bsgbw          0/1     Init:ImagePullBackOff   0          7h4m
kube-flannel-ds-amd64-hp7h8          1/1     Running                 1          11h
kube-flannel-ds-amd64-mnzlg          1/1     Running                 0          11h
kube-proxy-cn2ff                     1/1     Running                 1          7h4m
kube-proxy-p4mv5                     1/1     Running                 0          11h
kube-proxy-x9th9                     1/1     Running                 2          11h
kube-scheduler-k8s-master            1/1     Running                 0          11h
```
检查`https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml`中`flannel`版本
下载对应的`flannel`版本
#### 9.2重新安装master时,Unable to connect to the server: x509
```
[root@k8s-master ~]# kubectl get node
Unable to connect to the server: x509: certificate signed by unknown authority (possibly because of "crypto/rsa: verification error" while trying to verify candidate authority certificate "kubernetes")
```
删除之前配置
```
rm -rf $HOME/.kube
```
kubeadm初始化后再执行
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

#### 9.3 coredns 1 node(s) had taints that the pod didn't tolerate.
```
[root@k8s-master ~]# kubectl get all -n kube-system
NAME                                     READY   STATUS    RESTARTS   AGE
pod/coredns-fb8b8dccf-49j92              0/1     Pending   0          8m18s
pod/coredns-fb8b8dccf-p57cx              0/1     Pending   0          8m19s
pod/etcd-k8s-master                      1/1     Running   0          7m24s
pod/kube-apiserver-k8s-master            1/1     Running   0          7m32s

[root@k8s-master ~]# kubectl describe  pod/coredns-fb8b8dccf-49j92 -n kube-system
Events:
  Type     Reason            Age                   From               Message
  ----     ------            ----                  ----               -------
  Warning  FailedScheduling  2m7s (x52 over 7m8s)  default-scheduler  0/1 nodes are available: 1 node(s) had taints that the pod didn't tolerate.
```
解决方法
```
wget  https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f kube-flannel.yml
[root@master ~]# kubectl get pod -n kube-system
NAME                                 READY   STATUS              RESTARTS   AGE
coredns-fb8b8dccf-298ps              0/1     ContainerCreating   0          2m33s
coredns-fb8b8dccf-f5b4t              0/1     Running             0          2m33s
etcd-k8s-node01                      1/1     Running             0          110s
kube-apiserver-k8s-node01            1/1     Running             0          90s
kube-controller-manager-k8s-node01   1/1     Running             0          98s
kube-flannel-ds-amd64-674xl          1/1     Running             0          7s
kube-proxy-nkv7n                     1/1     Running             0          2m33s
kube-scheduler-k8s-node01            1/1     Running             0          104s

[root@master ~]# kubectl get pod -n kube-system
NAME                                 READY   STATUS    RESTARTS   AGE
coredns-fb8b8dccf-298ps              1/1     Running   0          2m38s
coredns-fb8b8dccf-f5b4t              0/1     Running   0          2m38s
etcd-k8s-node01                      1/1     Running   0          115s
kube-apiserver-k8s-node01            1/1     Running   0          95s
kube-controller-manager-k8s-node01   1/1     Running   0          103s
kube-flannel-ds-amd64-674xl          1/1     Running   0          12s
kube-proxy-nkv7n                     1/1     Running   0          2m38s
kube-scheduler-k8s-node01            1/1     Running   0          109s

```
#### 9.4 `kubeadm join`的时候一直卡在`[preflight] Running pre-flight checks`
重启虚拟机

#### 9.5 重启虚拟机后Evicted和CrashLoopBackOff
```
[root@k8s-master ~]# kubectl get all -n kube-system
NAME                                     READY   STATUS             RESTARTS   AGE
pod/coredns-fb8b8dccf-4vsfn              0/1     CrashLoopBackOff   57         7h43m
pod/coredns-fb8b8dccf-dfwvt              0/1     Evicted            0          30h
pod/coredns-fb8b8dccf-p6n2n              0/1     CrashLoopBackOff   56         7h43m
pod/coredns-fb8b8dccf-slbgd              0/1     Evicted            0          30h
pod/etcd-k8s-master                      1/1     Running            6          30h
pod/kube-apiserver-k8s-master            1/1     Running            6          30h
pod/kube-controller-manager-k8s-master   0/1     CrashLoopBackOff   40         30h
pod/kube-flannel-ds-amd64-8bmz2          1/1     Running            4          29h
pod/kube-flannel-ds-amd64-92dxf          1/1     Running            4          29h
pod/kube-flannel-ds-amd64-r26md          0/1     Evicted            0          5m36s
pod/kube-proxy-49ttv                     1/1     Running            4          29h
pod/kube-proxy-8sd28                     0/1     Evicted            0          5m36s
pod/kube-proxy-m9qnk                     1/1     Running            5          29h
pod/kube-scheduler-k8s-master            0/1     CrashLoopBackOff   39         30h
```
```
kubectl logs -f pod/kube-controller-manager-k8s-master -n kube-system
```
