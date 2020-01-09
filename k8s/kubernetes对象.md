# 1.描述 Kubernetes 对象

在 Kubernetes 中创建对象时，必须提供描述其所需 Status 的对象 Spec，以及关于对象（如 name）的一些基本信息。
当使用 Kubernetes API 创建对象（直接或通过 kubectl）时，该 API 请求必须将该信息作为 JSON 包含在请求 body 中。
通常，可以将信息提供给 kubectl .yaml 文件，在进行 API 请求时，kubectl 将信息转换为 JSON。

以下示例是一个.yaml 文件，显示 Kubernetes Deployment 所需的字段和对象 Spec：

```yaml
vi nginx-deployment.yaml

apiVersion: apps/v1beta1
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

使用上述.yaml 文件创建 Deployment，是通过在 kubectl 中使用`kubectl create`命令来实现。
将该.yaml 文件作为参数传递。如下例子：

```bash
[root@k8s-master ~]# kubectl create -f ./nginx-deployment.yaml
deployment "nginx-deployment" created
```

## 1.2 对于要创建的 Kubernetes 对象的 yaml 文件，需要为以下字段设置值：

- apiVersion - 创建对象的 Kubernetes API 版本
- kind - 要创建什么样的对象？
- metadata- 具有唯一标示对象的数据，包括 name（字符串）、UID 和 Namespace

### 1.3 出现的问题

```bash
error: error validating "./nginx-deployment.yaml": error validating data: couldn't find type: v1beta1.Deployment;
```

### 1.4 查看 kubernete 版本

```bash
[root@k8s-master ~]# kubectl version
Client Version: version.Info{Major:"1", Minor:"5", GitVersion:"v1.5.2", GitCommit:"269f928217957e7126dc87e6adfa82242bfe5b1e", GitTreeState:"clean", BuildDate:"2017-07-03T15:31:10Z", GoVersion:"go1.7.4", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"5", GitVersion:"v1.5.2", GitCommit:"269f928217957e7126dc87e6adfa82242bfe5b1e", GitTreeState:"clean", BuildDate:"2017-07-03T15:31:10Z", GoVersion:"go1.7.4", Compiler:"gc", Platform:"linux/amd64"}
```

应用程序 API 组将是 v1 部署类型所在的位置。
`apps/v1beta1`版本已在`1.6.0`中添加，因此如果您有`1.5.x`客户端或服务器，则仍应使用`extensions/v1beta1`版本。

## 2.何时使用多个 Namespaces

当团队或项目中具有许多用户时，可以考虑使用 Namespace 来区分，a 如果是少量用户集群，
可以不需要考虑使用 Namespace，如果需要它们提供特殊性质时，可以开始使用 Namespace。

Namespace 为名称提供了一个范围。资源的 Names 在 Namespace 中具有唯一性。

### 2.1 查看 Namespaces

```bash
[root@k8s-master ~]# kubectl get namespaces
NAME          STATUS    AGE
default       Active    1d
kube-system   Active    1d
```

Kubernetes 从两个初始的 Namespace 开始：

- default
- kube-system 由 Kubernetes 系统创建的对象的 Namespace

### 2.2 创建 Namespace

```bash
#1.命令行直接创建
[root@k8s-master ~]# kubectl create namespace my-namespace
namespace "my-namespace" created
#2.通过文件创建
$ cat my-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace2

[root@k8s-master ~]# kubectl create -f ./my-namespace.yaml
namespace "my-namespace2" created
```

### 2.3 删除 Namespace

```bash
[root@k8s-master ~]# kubectl delete namespaces my-namespace2
namespace "my-namespace2" deleted
```

删除一个 namespace 会自动删除所有属于该 namespace 的资源。
default 和 kube-system 命名空间不可删除。
