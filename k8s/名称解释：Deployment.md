# 简述

Deployment 为 Pod 和 ReplicaSet 提供了一个声明式定义(declarative)方法，用来替代以前的 ReplicationController 来方便的管理应用。典型的应用场景包括：

- 定义 Deployment 来创建 Pod 和 ReplicaSet
- 滚动升级和回滚应用
- 扩容和缩容
- 暂停和继续 Deployment

比如一个简单的 nginx 应用可以定义为

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: registry:5000/nginx:latest
          ports:
            - containerPort: 80
```

扩容：

```bash
kubectl scale deployment nginx-deployment --replicas 5
```

如果集群支持`horizontal pod autoscaling`的话，还可以为`Deployment`设置自动扩展：

```bash
kubectl autoscale deployment nginx-deployment --min=3 --max=15 --cpu-percent=80
```

更新镜像也比较简单:

```bash
kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
```

回滚：

```bash
kubectl rollout undo deployment/nginx-deployment
```

#### Deployment 是什么

Deployment 为 Pod 和 Replica Set（下一代 Replication Controller）提供声明式更新。

你只需要在 Deployment 中描述你想要的目标状态是什么，Deployment controller 就会帮你将 Pod 和 Replica Set 的实际状态改变到你的目标状态。
你可以定义一个全新的 Deployment，也可以创建一个新的替换旧的 Deployment。

一个典型的用例如下：

- 使用 Deployment 来创建 ReplicaSet。ReplicaSet 在后台创建 pod。检查启动状态，看它是成功还是失败。
- 然后，通过更新 Deployment 的 PodTemplateSpec 字段来声明 Pod 的新状态。这会创建一个新的 ReplicaSet，Deployment 会按照控制的速率将 pod 从旧的 ReplicaSet 移动到新的 ReplicaSet 中。
- 如果当前状态不稳定，回滚到之前的 Deployment revision。每次回滚都会更新 Deployment 的 revision。
- 扩容 Deployment 以满足更高的负载。

#### 创建 Deployment

下面是一个 Deployment 示例，它创建了一个 Replica Set 来启动 3 个 nginx pod。

下载示例文件并执行命令：

```bash
[root@k8s-master ~]# kubectl create -f nginx-deployment.yaml --record
deployment "nginx-deployment" created
```

将 kubectl 的`—record`的 flag 设置为 true 可以在 annotation 中记录当前命令创建或者升级了该资源。
这在未来会很有用，例如，查看在每个 Deployment revision 中执行了哪些命令。

```bash
[root@k8s-master ~]# kubectl get deployments
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment      3         0         0            0           1d
```

输出结果表明我们希望的 repalica 数是 3（根据 deployment 中的`.spec.replicas`配置）

```bash
[root@k8s-master ~]# kubectl get rs
NAME                             DESIRED   CURRENT   READY     AGE
nginx-deployment-927711520       5         0         0         1d
```

你可能会注意到 Replica Set 的名字总是`<Deployment 的名字>-<pod template 的 hash 值>`。

#### 更新 Deployment

我们可以使用 edit 命令来编辑 Deployment

```bash
[root@k8s-master ~]# kubectl edit deployment/nginx-deployment
deployment "nginx-deployment" edited
```

#### Deployment 扩容

你可以使用以下命令扩容 Deployment：

```bash
[root@k8s-master ~]# kubectl scale deployment nginx-deployment --replicas 5
deployment "nginx-deployment" scaled
```

#### 查看详情

```yaml
[root@k8s-master ~]# kubectl describe deployment nginx-deployment
...
Conditions:
  Type                  Status  Reason
  ----                  ------  ------
  Available             False   MinimumReplicasUnavailable
  ReplicaFailure        True    FailedCreate
[root@k8s-master ~]# kubectl get deployment nginx-deployment -o yaml
...
status:
  conditions:
  - lastTransitionTime: 2019-04-06T17:13:32Z
    lastUpdateTime: 2019-04-06T17:13:32Z
    message: Deployment does not have minimum availability.
    reason: MinimumReplicasUnavailable
    status: "False"
    type: Available
  - lastTransitionTime: 2019-04-06T17:13:41Z
    lastUpdateTime: 2019-04-06T17:13:41Z
    message: 'unable to create pods: No API token found for service account "default",
      retry after the token is automatically created and added to the service account'
    reason: FailedCreate
    status: "True"
    type: ReplicaFailure
  observedGeneration: 5
  unavailableReplicas: 5
```
