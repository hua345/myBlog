# 参考

- [Interactive Tutorial - Deploying an App](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-interactive/)

## 1.查看 master 服务状态

```bash
[root@k8s-master ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.0", GitCommit:"641856db18352033a0d96dbc99153fa3b27298e5", GitTreeState:"clean", BuildDate:"2019-03-25T15:53:57Z", GoVersion:"go1.12.1", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.0", GitCommit:"641856db18352033a0d96dbc99153fa3b27298e5", GitTreeState:"clean", BuildDate:"2019-03-25T15:45:25Z", GoVersion:"go1.12.1", Compiler:"gc", Platform:"linux/amd64"}

[root@k8s-master ~]# kubectl get nodes
NAME         STATUS   ROLES    AGE    VERSION
k8s-master   Ready    master   13h    v1.14.0
k8s-node01   Ready    <none>   131m   v1.14.0
k8s-node02   Ready    <none>   13h    v1.14.0
```

## 2 在 master 节点上创建一个 deployment

### 2.1 通过 yaml 文件创建 deployment

`vi nginx-yaml-deployment.yaml`

```yaml
---
apiVersion: apps/v1
#指定创建资源的角色/类型
kind: Deployment
metadata:
  labels:
    #设定资源的标签
    app: nginx-yaml
  #资源的名字，在同一个namespace中必须唯一
  name: nginx-yaml
  namespace: default
#specification of the resource content 指定该资源的内容
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-yaml
  template:
    metadata:
      labels:
        app: nginx-yaml
    spec:
      containers:
        #容器使用的镜像地址
        - image: nginx:latest
          # 三个选择Always、Never、IfNotPresent，每次启动时检查和更新（从registery）images的策略，
          # Always，每次都检查
          # Never，每次都不检查（不管本地是否有）
          # IfNotPresent，如果本地有就不检查，如果没有就拉取
          imagePullPolicy: IfNotPresent
          #容器的名字
          name: nginx
          ports:
            - containerPort: 80
```

```bash
kubectl create -f nginx-yaml-deployment.yaml
```

#### 2.2 通过命令行方式创建 deployment

```bash
[root@k8s-master ~]# kubectl create deployment nginx-demo  --image=nginx:latest
deployment.apps/nginx-demo created

[root@k8s-master ~]# kubectl get deployments
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-demo   3/3     3            3           51m
nginx-yaml   3/3     3            3           31s

[root@k8s-master ~]# kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
nginx-demo-6f6475bfb5-4rmc4   1/1     Running   0          51m
nginx-demo-6f6475bfb5-8k29b   1/1     Running   0          51m
nginx-demo-6f6475bfb5-dn4xt   1/1     Running   0          51m
nginx-yaml-7d8cfbccf6-h5pnq   1/1     Running   0          50s
nginx-yaml-7d8cfbccf6-l9ngp   1/1     Running   0          50s
nginx-yaml-7d8cfbccf6-wgnvp   1/1     Running   0          50s

[root@k8s-master ~]# kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE         NOMINATED NODE   READINESS GATES
nginx-demo-6f6475bfb5-4rmc4   1/1     Running   0          52m   10.100.1.2   k8s-node01   <none>           <none>
nginx-demo-6f6475bfb5-8k29b   1/1     Running   0          52m   10.100.2.2   k8s-node02   <none>           <none>
nginx-demo-6f6475bfb5-dn4xt   1/1     Running   0          52m   10.100.1.3   k8s-node01   <none>           <none>
nginx-yaml-7d8cfbccf6-h5pnq   1/1     Running   0          93s   10.100.2.3   k8s-node02   <none>           <none>
nginx-yaml-7d8cfbccf6-l9ngp   1/1     Running   0          93s   10.100.1.4   k8s-node01   <none>           <none>
nginx-yaml-7d8cfbccf6-wgnvp   1/1     Running   0          93s   10.100.2.4   k8s-node02   <none>           <none>
```

### 2.2 扩容 deployment

```bash
kubectl scale --replicas=3 deployment nginx-demo

[root@k8s-master ~]# kubectl get pods
NAME                          READY   STATUS              RESTARTS   AGE
nginx-demo-6f6475bfb5-4rmc4   1/1     Running             0          17s
nginx-demo-6f6475bfb5-8k29b   0/1     ContainerCreating   0          9s
nginx-demo-6f6475bfb5-dn4xt   0/1     ContainerCreating   0          9s

[root@k8s-master ~]# kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
nginx-demo-6f6475bfb5-4rmc4   1/1     Running   0          22s
nginx-demo-6f6475bfb5-8k29b   1/1     Running   0          14s
nginx-demo-6f6475bfb5-dn4xt   1/1     Running   0          14s

[root@k8s-master ~]# kubectl get deployments
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-demo   3/3     3            3           100s

```

### 3.1 查看`pod`详细信息

```bash
[root@k8s-master ~]# kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE         NOMINATED NODE   READINESS GATES
nginx-demo-6f6475bfb5-4rmc4   1/1     Running   0          44s   10.100.1.2   k8s-node01   <none>           <none>
nginx-demo-6f6475bfb5-8k29b   1/1     Running   0          36s   10.100.2.2   k8s-node02   <none>           <none>
nginx-demo-6f6475bfb5-dn4xt   1/1     Running   0          36s   10.100.1.3   k8s-node01   <none>           <none>

[root@k8s-master ~]# kubectl describe po nginx-demo-6f6475bfb5-ppj5v
Name:               nginx-demo-6f6475bfb5-4rmc4
Namespace:          default
Priority:           0
PriorityClassName:  <none>
Node:               k8s-node01/192.168.137.89
Start Time:         Sun, 14 Apr 2019 10:55:47 +0800
Labels:             app=nginx-demo
                    pod-template-hash=6f6475bfb5
Annotations:        <none>
Status:             Running
IP:                 10.100.1.2
Controlled By:      ReplicaSet/nginx-demo-6f6475bfb5
Events:
  Type    Reason     Age    From                 Message
  ----    ------     ----   ----                 -------
  Normal  Scheduled  2m28s  default-scheduler    Successfully assigned default/nginx-demo-6f6475bfb5-4rmc4 to k8s-node01
  Normal  Pulling    2m26s  kubelet, k8s-node01  Pulling image "nginx:latest"
  Normal  Pulled     2m18s  kubelet, k8s-node01  Successfully pulled image "nginx:latest"
  Normal  Created    2m18s  kubelet, k8s-node01  Created container nginx
  Normal  Started    2m18s  kubelet, k8s-node01  Started container nginx
```

> Pod 分配到了`k8s-node01/192.168.137.89`，容器的 ip：`10.100.1.2`

```bash
# 在k8s-node01/192.168.137.89测试nginx是否正常启动
curl 10.100.1.2:80
```

#### 4.创建 service 向外暴露服务

`Service`有四种 type:
`ClusterIP`(默认）、`NodePort`、`LoadBalancer`、`ExternalName`. 其中`NodePort`和`LoadBalancer`两类型的`Services`可以对外提供服务。

#### 4.1 使用 yaml 文件创建 Service

`vi nginx-yaml-service.yaml`

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-yaml
  labels:
    name: nginx-yaml
  namespace: default
spec:
  type: NodePort      #这里代表是NodePort类型的
  ports:
    - port: 80          #service 暴露在 cluster ip上的端口,供内部访问。
      targetPort: 80  #端口一定要和container暴露出来的端口对应，nginx暴露的端口是80
      protocol: TCP
      nodePort: 31975  # 暴露在集群物理节点上node的端口 ，此端口供外部调用。
  selector:
    app: nginx-yaml   #创建deploy时的标签
```

```bash
[root@k8s-master ~]# kubectl create -f nginx-yaml-service.yaml
service/nginx-yaml created
```

#### 4.2 使用命令创建 Service

```bash
[root@k8s-master ~]# kubectl expose deployment/nginx-demo --type=NodePort --port 80 --target-port 80
service/nginx-demo exposed
```

> - `--port`：暴露出去的端口
> - `--type=NodePort`：使用结点+端口方式访问服务
> - `--target-port`：容器的端口
> - `--name`：创建 service 指定的名称

#### 5.查看`service`详细信息

```bash
[root@k8s-master ~]# kubectl get all
NAME                              READY   STATUS    RESTARTS   AGE
pod/nginx-demo-6f6475bfb5-4rmc4   1/1     Running   0          71m
pod/nginx-demo-6f6475bfb5-8k29b   1/1     Running   0          71m
pod/nginx-demo-6f6475bfb5-dn4xt   1/1     Running   0          71m
pod/nginx-yaml-7d8cfbccf6-h5pnq   1/1     Running   0          21m
pod/nginx-yaml-7d8cfbccf6-l9ngp   1/1     Running   0          21m
pod/nginx-yaml-7d8cfbccf6-wgnvp   1/1     Running   0          21m

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
service/kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        137m
service/nginx-demo   NodePort    10.106.33.155   <none>        80:31973/TCP   62m
service/nginx-yaml   NodePort    10.97.26.121    <none>        80:31975/TCP   33s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx-demo   3/3     3            3           71m
deployment.apps/nginx-yaml   3/3     3            3           21m

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-demo-6f6475bfb5   3         3         3       71m
replicaset.apps/nginx-yaml-7d8cfbccf6   3         3         3       21m

[root@k8s-master ~]# kubectl describe service/nginx-demo
Name:                     nginx-demo
Namespace:                default
Labels:                   app=nginx-demo
Annotations:              <none>
Selector:                 app=nginx-demo
Type:                     NodePort
IP:                       10.106.33.155
Port:                     <unset>  80/TCP
TargetPort:               80/TCP
NodePort:                 <unset>  31973/TCP
Endpoints:                10.100.1.2:80,10.100.1.3:80,10.100.2.2:80
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>

```

#### 6.访问应用

> `10.106.33.155`是 Service 的虚拟 IP 地址
>
> 从`pod`信息中看到部署在`k8s-node01`上，暴露的端口是`31973`

```bash
curl 192.168.137.89:31973
```

#### 7.和运行着的 Pod 交互

```bash
kubectl logs <pod-name>

# 运行tail -f 得到日志输出
kubectl logs -f <pod-name>
```

#### 8.删除

```bash
kubectl delete deployments/nginx-demo services/nginx-demo
```

#### 9. 查看 iptables

```bash
# iptables -nvL
[root@k8s-node02 ~]# iptables-save | grep default/nginx-demo
-A KUBE-NODEPORTS -p tcp -m comment --comment "default/nginx-demo:" -m tcp --dport 31911 -j KUBE-MARK-MASQ
-A KUBE-NODEPORTS -p tcp -m comment --comment "default/nginx-demo:" -m tcp --dport 31911 -j KUBE-SVC-53PNG6KROACM5MQP
-A KUBE-SERVICES ! -s 10.100.0.0/16 -d 10.108.54.204/32 -p tcp -m comment --comment "default/nginx-demo: cluster IP" -m tcp --dport 80 -j KUBE-MARK-MASQ
-A KUBE-SERVICES -d 10.108.54.204/32 -p tcp -m comment --comment "default/nginx-demo: cluster IP" -m tcp --dport 80 -j KUBE-SVC-53PNG6KROACM5MQP
```

> 访问 192.168.137.97/32 31911 端口的请求会被重定向到 10.108.54.204/32 的 80 端口。这些规则是由`kube-proxy`生成

#### kubectl proxy

为访问 kubernetes apiserver 的 REST api 充当反向代理角色

```bash
kubectl proxy --address=0.0.0.0
```

设置 API server 接收所有主机的请求：

```bash
kubectl proxy --address=0.0.0.0  --accept-hosts='^*$'
Starting to serve on [::]:8001
```

#### 出现的问题

#### network: failed to set bridge addr: "cni0" already has an IP address different from 10.100.3.1/24

```bash
 Warning  FailedCreatePodSandBox  2m8s                   kubelet, k8s-node01  Failed create pod sandbox:
rpc error: code = Unknown desc = failed to set up sandbox container "03c30f02d76551b8c1444b79488844361d01430234fecf2cbe30cb83bcd3b8c5" network for pod "nginx-yaml-7d8cfbccf6-6s4vv": NetworkPlugin cni failed to set up pod "nginx-yaml-7d8cfbccf6-6s4vv_default"
network: failed to set bridge addr: "cni0" already has an IP address different from 10.100.3.1/24
```

卸载 node

```bash
# master
kubectl drain k8s-node01 --delete-local-data --force --ignore-daemonsets
kubectl delete node k8s-node01
```

重置 Node 节点的 kubernetes 服务，重置网络。

```bash
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
