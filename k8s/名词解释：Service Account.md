# Service Account

Service account 是为了方便 Pod 里面的进程调用 Kubernetes API 或其他外部服务而设计的。它与 User account 不同

- User account 是为人设计的，而 service account 则是为 Pod 中的进程调用 Kubernetes API 而设计；
- User account 是跨 namespace 的，而 service account 则是仅局限它所在的 namespace；
- 每个 namespace 都会自动创建一个 default service account
- Token controller 检测 service account 的创建，并为它们创建 secret
- 开启 ServiceAccount Admission Controller 后
  - 每个 Pod 在创建后都会自动设置 spec.serviceAccount 为 default（除非指定了其他 ServiceAccout）
  - 验证 Pod 引用的 service account 已经存在，否则拒绝创建
  - 如果 Pod 没有指定 ImagePullSecrets，则把 service account 的 ImagePullSecrets 加到 Pod 中
  - 每个 container 启动后都会挂载该 service account 的 token 和 ca.crt 到/var/run/secrets/kubernetes.io/serviceaccount/

## 创建 Service Account

```yaml
[root@k8s-master ~]# kubectl create serviceaccount jenkins
serviceaccount "jenkins" created
[root@k8s-master ~]# kubectl get serviceaccounts jenkins -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2019-04-08T08:04:50Z
  name: jenkins
  namespace: default
  resourceVersion: "82928"
  selfLink: /api/v1/namespaces/default/serviceaccounts/jenkins
  uid: fbd43f82-59d4-11e9-bbc4-00155d016b08
```

自动创建的 secret：

```yaml
[root@k8s-master ~]# kubectl get secret mysecret01 -o yaml
apiVersion: v1
data:
  password: MTIzNDU2
  username: YWRtaW4=
kind: Secret
metadata:
  creationTimestamp: 2019-04-08T06:57:06Z
  name: mysecret01
  namespace: default
  resourceVersion: "78276"
  selfLink: /api/v1/namespaces/default/secrets/mysecret01
  uid: 85844b5c-59cb-11e9-bbc4-00155d016b08
type: Opaque
```

## 授权

`Service Account`为服务提供了一种方便的认证机制，但它不关心授权的问题。可以配合 RBAC 来为 Service Account 鉴权：

- 配置–authorization-mode=RBAC 和–runtime-config=rbac.authorization.k8s.io/v1alpha1
- 配置–authorization-rbac-super-user=admin
- 定义 Role、ClusterRole、RoleBinding 或 ClusterRoleBinding

比如
编辑`pod-reader.yaml`

```yaml
# This role allows to read pods in the namespace "default"
kind: Role
apiVersion: rbac.authorization.k8s.io/v1alpha1
metadata:
  namespace: default
  name: pod-reader
rules:
  - apiGroups: [""] # The API group "" indicates the core API Group.
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
    nonResourceURLs: []
```

```bash
[root@k8s-master ~]# kubectl create -f pod-reader.yaml
role "pod-reader" created
```

编辑`read-pods.yaml`

```yaml
# This role binding allows "default" to read pods in the namespace "default"
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1alpha1
metadata:
  name: read-pods
  namespace: default
subjects:
  - kind: ServiceAccount # May be "User", "Group" or "ServiceAccount"
    name: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

```
[root@k8s-master ~]# kubectl create -f read-pods.yaml
rolebinding "read-pods" created
```
