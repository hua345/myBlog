# apiVersion

Kubernetes 的官方文档中并没有对 apiVersion 的详细解释，而且因为 K8S 本身版本也在快速迭代，有些资源在低版本还在 beta 阶段，到了高版本就变成了 stable。

如`Deployment`:

- 1.6版本之前 apiVsersion：extensions/v1beta1
- 1.6版本到1.9版本之间：apps/v1beta1
- 1.9版本之后:apps/v1

## 查看当前可用的 API 版本

```bash
[root@k8s-master ~]# kubectl --version
Kubernetes v1.5.2
[root@k8s-master ~]# kubectl api-versions
apps/v1beta1
authentication.k8s.io/v1beta1
authorization.k8s.io/v1beta1
autoscaling/v1
batch/v1
certificates.k8s.io/v1alpha1
extensions/v1beta1
policy/v1beta1
rbac.authorization.k8s.io/v1alpha1
storage.k8s.io/v1beta1
v1
```
