#### 参考:
- [官方文档部署Dashboard](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-the-dashboard-ui)
- [官方文档访问Dashboard](https://github.com/kubernetes/dashboard/wiki/Accessing-Dashboard---1.7.X-and-above)
- [https://github.com/kubernetes/dashboard](https://github.com/kubernetes/dashboard)
- [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [从零开始搭建Kubernetes集群（四、搭建K8S Dashboard）](https://www.jianshu.com/p/6f42ac331d8a)

#### 查看集群信息
```
[root@k8s-master ~]# kubectl cluster-info
Kubernetes master is running at https://192.168.137.105:6443
KubeDNS is running at https://192.168.137.105:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
#### 1.部署[Dashboard UI](https://github.com/kubernetes/dashboard)
#### 1.2可替换部署
Dashboard通过`HTTP`协议访问，认证方式通过`Authorization`方式
This setup is not fully secure. Certificates are not used and Dashboard is exposed only over HTTP. In this setup access control can be ensured only by using Authorization Header feature.
浏览器打开`https://github.com/kubernetes/dashboard/blob/master/aio/deploy/alternative/kubernetes-dashboard.yaml`
并保存到`kubernetes-dashboard.yaml`

vi kubernetes-dashboard.yaml
```
    containers:
    - name: kubernetes-dashboard
      image: k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1
      ports:
      - containerPort: 8443
        protocol: TCP
      args:
        - --auto-generate-certificates
        # Uncomment the following line to manually specify Kubernetes API server Host
        # If not specified, Dashboard will attempt to auto discover the API server and connect
        # to it. Uncomment only if the default does not work.
        # - --apiserver-host=http://my-address:port
```
    containers:
    - name: kubernetes-dashboard
      image: 192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1
      ports:
      - containerPort: 8443
        protocol: TCP
      args:
        - --auto-generate-certificates
        # Uncomment the following line to manually specify Kubernetes API server Host
        # If not specified, Dashboard will attempt to auto discover the API server and connect
        # to it. Uncomment only if the default does not work.
        - --apiserver-host=http://192.168.137.105:8080
```
[root@k8s-master ~]# kubectl apply -f ~/kubernetes-dashboard.yaml
secret/kubernetes-dashboard-certs created
serviceaccount/kubernetes-dashboard created
role.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
deployment.apps/kubernetes-dashboard created
service/kubernetes-dashboard created
```
```
[root@k8s-master ~]# kubectl get all -n kube-system
NAME                                        READY   STATUS             RESTARTS   AGE
pod/coredns-fb8b8dccf-hbzck                 1/1     Running            0          25h
pod/coredns-fb8b8dccf-w8mz9                 1/1     Running            0          25h
pod/etcd-k8s-master                         1/1     Running            0          25h
pod/kube-apiserver-k8s-master               1/1     Running            0          25h
pod/kube-controller-manager-k8s-master      1/1     Running            1          25h
pod/kube-flannel-ds-amd64-hp7h8             1/1     Running            1          24h
pod/kube-flannel-ds-amd64-mnzlg             1/1     Running            0          25h
pod/kube-flannel-ds-amd64-x56wj             1/1     Running            0          13h
pod/kube-proxy-dl9d8                        1/1     Running            0          13h
pod/kube-proxy-p4mv5                        1/1     Running            0          25h
pod/kube-proxy-x9th9                        1/1     Running            2          24h
pod/kube-scheduler-k8s-master               1/1     Running            1          25h
pod/kubernetes-dashboard-5f7b999d65-79ttk   0/1     ImagePullBackOff   0          3m21s

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                  AGE
service/kube-dns               ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP,9153/TCP   25h
service/kubernetes-dashboard   ClusterIP   10.106.188.67   <none>        443/TCP                  3m23s

NAME                                     DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                     AGE
daemonset.apps/kube-flannel-ds-amd64     3         3         3       3            3           beta.kubernetes.io/arch=amd64     25h
daemonset.apps/kube-flannel-ds-arm       0         0         0       0            0           beta.kubernetes.io/arch=arm       25h
daemonset.apps/kube-flannel-ds-arm64     0         0         0       0            0           beta.kubernetes.io/arch=arm64     25h
daemonset.apps/kube-flannel-ds-ppc64le   0         0         0       0            0           beta.kubernetes.io/arch=ppc64le   25h
daemonset.apps/kube-flannel-ds-s390x     0         0         0       0            0           beta.kubernetes.io/arch=s390x     25h
daemonset.apps/kube-proxy                3         3         3       3            3           <none>                            25h

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/coredns                2/2     2            2           25h
deployment.apps/kubernetes-dashboard   0/1     1            0           3m23s

NAME                                              DESIRED   CURRENT   READY   AGE
replicaset.apps/coredns-fb8b8dccf                 2         2         2       25h
replicaset.apps/kubernetes-dashboard-5f7b999d65   1         1         0       3m23s
```
#### 2.运行`kubectl proxy`
```
[root@k8s-master ~]# kubectl proxy --address='0.0.0.0'  --accept-hosts='^*$'
Starting to serve on [::]:8001
```
访问`kubernetes-dashboard`
```
http://192.168.137.105:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
```
#### a. 出现的问题
#### a.1 no endpoints available for service
```
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {
    
  },
  "status": "Failure",
  "message": "no endpoints available for service \"https:kubernetes-dashboard:\"",
  "reason": "ServiceUnavailable",
  "code": 503
}
```
#### a.1.1 ImagePullBackOff
Back-off pulling image "k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1"
```
[root@k8s-master ~]# kubectl get pods -n kube-system
NAME                                    READY   STATUS             RESTARTS   AGE
coredns-fb8b8dccf-hbzck                 1/1     Running            0          25h
coredns-fb8b8dccf-w8mz9                 1/1     Running            0          25h
etcd-k8s-master                         1/1     Running            0          25h
kube-apiserver-k8s-master               1/1     Running            0          25h
kube-controller-manager-k8s-master      1/1     Running            1          25h
kube-flannel-ds-amd64-hp7h8             1/1     Running            1          25h
kube-flannel-ds-amd64-mnzlg             1/1     Running            0          25h
kube-flannel-ds-amd64-x56wj             1/1     Running            0          13h
kube-proxy-dl9d8                        1/1     Running            0          13h
kube-proxy-p4mv5                        1/1     Running            0          25h
kube-proxy-x9th9                        1/1     Running            2          25h
kube-scheduler-k8s-master               1/1     Running            1          25h
kubernetes-dashboard-5f7b999d65-79ttk   0/1     ImagePullBackOff   0          23m

[root@k8s-master ~]# kubectl describe po/kubernetes-dashboard-5f7b999d65-79ttk -n kube-system
Name:               kubernetes-dashboard-5f7b999d65-79ttk
Namespace:          kube-system
Priority:           0
PriorityClassName:  <none>
Node:               k8s-node01/192.168.137.89
Start Time:         Tue, 09 Apr 2019 21:02:42 -0400
Labels:             k8s-app=kubernetes-dashboard
                    pod-template-hash=5f7b999d65
Annotations:        <none>
Status:             Pending
IP:                 10.100.4.5
Controlled By:      ReplicaSet/kubernetes-dashboard-5f7b999d65
Events:
  Type     Reason     Age                             From                 Message
  ----     ------     ----                            ----                 -------
  Normal   Scheduled  25m                             default-scheduler    Successfully assigned kube-system/kubernetes-dashboard-5f7b999d65-79ttk to k8s-node01
  Normal   Pulling    <invalid> (x4 over <invalid>)   kubelet, k8s-node01  Pulling image "k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1"
  Warning  Failed     <invalid> (x4 over <invalid>)   kubelet, k8s-node01  Failed to pull image "k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1": rpc error: code = Unknown desc = Error response from daemon: Get https://k8s.gcr.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
  Warning  Failed     <invalid> (x4 over <invalid>)   kubelet, k8s-node01  Error: ErrImagePull
  Normal   BackOff    <invalid> (x14 over <invalid>)  kubelet, k8s-node01  Back-off pulling image "k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1"
  Warning  Failed     <invalid> (x52 over <invalid>)  kubelet, k8s-node01  Error: ImagePullBackOff
```
```
[root@k8s-master ~]# kubectl delete -f ~/kubernetes-dashboard.yaml
secret "kubernetes-dashboard-certs" deleted
serviceaccount "kubernetes-dashboard" deleted
role.rbac.authorization.k8s.io "kubernetes-dashboard-minimal" deleted
rolebinding.rbac.authorization.k8s.io "kubernetes-dashboard-minimal" deleted
deployment.apps "kubernetes-dashboard" deleted
service "kubernetes-dashboard" deleted
```
下载docker镜像
```
docker pull registry.cn-hangzhou.aliyuncs.com/kuberneters/kubernetes-dashboard-amd64:v1.10.1
docker tag registry.cn-hangzhou.aliyuncs.com/kuberneters/kubernetes-dashboard-amd64:v1.10.1 k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1
docker tag registry.cn-hangzhou.aliyuncs.com/kuberneters/kubernetes-dashboard-amd64:v1.10.1 192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1
vi kubernetes-dashboard.yaml
image: k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1 -> image: 192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1
```
```
[root@k8s-master ~]# kubectl apply -f ~/kubernetes-dashboard.yaml
secret/kubernetes-dashboard-certs created
serviceaccount/kubernetes-dashboard created
role.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
deployment.apps/kubernetes-dashboard created
service/kubernetes-dashboard created

[root@k8s-master ~]# kubectl get pods -n kube-system
NAME                                    READY   STATUS    RESTARTS   AGE
coredns-fb8b8dccf-hbzck                 1/1     Running   3          26h
coredns-fb8b8dccf-w8mz9                 1/1     Running   2          26h
etcd-k8s-master                         1/1     Running   2          26h
kube-apiserver-k8s-master               1/1     Running   1          26h
kube-controller-manager-k8s-master      1/1     Running   2          26h
kube-flannel-ds-amd64-hp7h8             1/1     Running   1          25h
kube-flannel-ds-amd64-mnzlg             1/1     Running   2          25h
kube-flannel-ds-amd64-x56wj             1/1     Running   0          14h
kube-proxy-dl9d8                        1/1     Running   0          14h
kube-proxy-p4mv5                        1/1     Running   1          26h
kube-proxy-x9th9                        1/1     Running   2          25h
kube-scheduler-k8s-master               1/1     Running   2          26h
kubernetes-dashboard-6544b4bdfc-kvjnm   1/1     Running   0          104s
```
#### a.1.2.1 CrashLoopBackOff
Error: 'dial tcp 10.100.4.7:8443: i/o timeout'
Trying to reach: 'https://10.100.4.7:8443/'
```
[root@k8s-master ~]# kubectl get pods -n kube-system
NAME                                    READY   STATUS             RESTARTS   AGE
kubernetes-dashboard-6544b4bdfc-kvjnm   0/1     CrashLoopBackOff   33         20h

[root@k8s-master ~]# kubectl describe po/kubernetes-dashboard-6544b4bdfc-kvjnm -n kube-system
Name:               kubernetes-dashboard-6544b4bdfc-bftd5
Namespace:          kube-system
Priority:           0
PriorityClassName:  <none>
Node:               k8s-node02/192.168.137.97
Start Time:         Wed, 10 Apr 2019 12:33:28 -0400
Labels:             k8s-app=kubernetes-dashboard
                    pod-template-hash=6544b4bdfc
Annotations:        <none>
Status:             Running
IP:                 10.100.1.6
Controlled By:      ReplicaSet/kubernetes-dashboard-6544b4bdfc

Events:
  Type     Reason     Age                     From                 Message
  ----     ------     ----                    ----                 -------
  Normal   Pulling    9m39s                   kubelet, k8s-node02  Pulling image "192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1"
  Normal   Scheduled  9m35s                   default-scheduler    Successfully assigned kube-system/kubernetes-dashboard-6544b4bdfc-bftd5 to k8s-node02
  Normal   Pulled     9m33s                   kubelet, k8s-node02  Successfully pulled image "192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1"
  Normal   Pulled     6m2s (x4 over 8m58s)    kubelet, k8s-node02  Container image "192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1" already present on machine
  Normal   Created    6m (x5 over 9m32s)      kubelet, k8s-node02  Created container kubernetes-dashboard
  Normal   Started    5m59s (x5 over 9m31s)   kubelet, k8s-node02  Started container kubernetes-dashboard
  Warning  Unhealthy  5m28s                   kubelet, k8s-node02  Liveness probe failed: Get https://10.100.1.6:8443/: dial tcp 10.100.1.6:8443: connect: connection refused
  Warning  BackOff    4m28s (x14 over 8m23s)  kubelet, k8s-node02  Back-off restarting failed container

[root@k8s-master ~]# kubectl logs -f kubernetes-dashboard-59878787b5-fv4tv -n kube-system
2019/04/24 16:05:28 Starting overwatch
2019/04/24 16:05:28 Using apiserver-host location: http://192.168.137.105:8080
2019/04/24 16:05:28 Skipping in-cluster config
2019/04/24 16:05:28 Using random key for csrf signing
2019/04/24 16:05:58 Error while initializing connection to Kubernetes apiserver. This most likely means that the cluster is misconfigured (e.g., it has invalid apiserver certificates or service account's configuration) or the --apiserver-host param points to a server that does not exist. Reason: Get http://192.168.137.105:8080/version: dial tcp 192.168.137.105:8080: i/o timeout
```
```
[root@k8s-master ~]# kubectl proxy --address='0.0.0.0' --port 8080  --accept-hosts='^*$'
Starting to serve on [::]:8080
```
#### a.1.2.2 查看`kubectl proxy`的端口
```
[root@k8s-master ~]# kubectl proxy --address='0.0.0.0' --port 8001  --accept-hosts='^*$'
Starting to serve on [::]:8001
```
#### a.1.2.3修改`kubernetes-dashboard.yaml`文件
```
    containers:
    - name: kubernetes-dashboard
      image: 192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1
      ports:
      - containerPort: 8443
        protocol: TCP
      args:
        - --auto-generate-certificates
        # Uncomment the following line to manually specify Kubernetes API server Host
        # If not specified, Dashboard will attempt to auto discover the API server and connect
        # to it. Uncomment only if the default does not work.
        - --apiserver-host=http://192.168.137.105:8001
```
#### a.1.2.3重新部署`kubernetes-dashboard`
```
[root@k8s-master ~]# kubectl delete -f ~/kubernetes-dashboard.yaml
[root@k8s-master ~]# kubectl apply -f ~/kubernetes-dashboard.yaml
[root@k8s-master ~]# kubectl describe po/kubernetes-dashboard-6544b4bdfc-bftd5 -n kube-system
Events:
  Type     Reason     Age                 From                 Message
  ----     ------     ----                ----                 -------
  Normal   Pulling    112s                kubelet, k8s-node02  Pulling image "192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1"
  Normal   Scheduled  108s                default-scheduler    Successfully assigned kube-system/kubernetes-dashboard-6544b4bdfc-bftd5 to k8s-node02
  Normal   Pulled     106s                kubelet, k8s-node02  Successfully pulled image "192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1"
  Warning  BackOff    31s (x2 over 36s)   kubelet, k8s-node02  Back-off restarting failed container
  Normal   Pulled     20s (x2 over 71s)   kubelet, k8s-node02  Container image "192.168.137.89:5000/kubernetes-dashboard-amd64:v1.10.1" already present on machine
  Normal   Created    19s (x3 over 105s)  kubelet, k8s-node02  Created container kubernetes-dashboard
  Normal   Started    17s (x3 over 104s)  kubelet, k8s-node02  Started container kubernetes-dashboard

[root@k8s-master ~]# kubectl describe service/kubernetes-dashboard -n kube-system
Name:              kubernetes-dashboard
Namespace:         kube-system
Labels:            k8s-app=kubernetes-dashboard
Annotations:       kubectl.kubernetes.io/last-applied-configuration:
                     {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"k8s-app":"kubernetes-dashboard"},"name":"kubernetes-dashboard"...
Selector:          k8s-app=kubernetes-dashboard
Type:              ClusterIP
IP:                10.102.217.143
Port:              <unset>  443/TCP
TargetPort:        8443/TCP
Endpoints:         10.100.1.6:8443
Session Affinity:  None
Events:            <none>
```
#### b. [kubernetes-dashboard.yaml](https://github.com/kubernetes/dashboard/blob/master/aio/deploy/alternative/kubernetes-
