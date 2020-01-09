# 参考文档

- [名词解释：Secret](https://www.kubernetes.org.cn/secret)

## Secret

Secret 解决了密码、token、密钥等敏感数据的配置问题，而不需要把这些敏感数据暴露到镜像或者 Pod Spec 中。Secret 可以以 Volume 或者环境变量的方式使用。

Secret 有三种类型：

- Service Account：用来访问 Kubernetes API，由 Kubernetes 自动创建，并且会自动挂载到 Pod 的/run/secrets/kubernetes.io/serviceaccount 目录中；
- Opaque：base64 编码格式的 Secret，用来存储密码、密钥等；
- kubernetes.io/dockerconfigjson：用来存储私有 docker registry 的认证信息。

## Opaque Secret

Opaque 类型的数据是一个 map 类型，要求 value 是 base64 编码格式：

```bash
[root@k8s-master ~]# echo -n "admin" | base64
YWRtaW4=
[root@k8s-master ~]# echo -n "123456" | base64
MTIzNDU2
```

secrets01.yml

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret01
type: Opaque
data:
  password: MTIzNDU2
  username: YWRtaW4=
```

接着，就可以创建 secret 了：`kubectl create -f secrets01.yml`

创建好 secret 之后，有两种方式来使用它：

- 以 Volume 方式
- 以环境变量方式

## Service Account

Service Account 用来访问 Kubernetes API，由 Kubernetes 自动创建，并且会自动挂载到 Pod 的`/run/secrets/kubernetes.io/serviceaccount`目录中。

```bash
[root@k8s-master ~]# kubectl run nginx --image registry:5000/nginx
deployment "nginx" created
[root@k8s-master ~]# kubectl get pods
NAME                     READY     STATUS    RESTARTS   AGE
nginx-3137573019-md1u2   1/1       Running   0          13s
[root@k8s-master ~]# kubectl exec nginx-3137573019-md1u2 ls /run/secrets/kubernetes.io/serviceaccount
ca.crt
namespace
token
```
