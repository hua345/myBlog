# 使用配置文件创建一个容器

Kubernetes 是在 Pod 中来运行容器的。一个包含了一个简单的 HellWorld 容器的 Pod 可以被如下的 YAML 文件指定：

```yaml
apiVersion: v1
kind: Pod
metadata:
name: hello-world
spec: # specification of the pod’s contents
restartPolicy: Never
containers:
- name: hello
image: registry:5000/ubuntu
command: ["/bin/echo","hello”,”world"]
```

`metadata.name`的值 hello-world ，将会成为创建成功后 Pod 的名称，这个名称必须在集群中唯一，而 container[0].name 只是容器在 Pod 中的昵称。
`image` 就是 Docker image 的名称且 Kubernetes 默认会从 Docker Hub 中拉取镜像。
`restartPolicy`:`Never`指明了我们只是想运行容器一次然后就终止 Pod。
`Command` 覆盖了 docker 容器的`Entrypoint`。命令的参数（相当于 Docker 的 Cmd ）可以指定`args`参数，如下所示：

```yaml
command: ["/bin/echo"]
args: ["hello","world"]
```

创建这个 pod 就可以使用`create`命令了

```bash
$ kubectl create -f ./hello-world.yaml
pods/hello-world
```

当成功创建时， kubectl 打印出资源类型和资源名称。

## 出现的问题

```bash
[root@k8s-master ~]# kubectl create -f hello-pod.yaml
error: error validating "hello-pod.yaml": error validating data: [found invalid field command for v1.Pod, found invalid field name for v1.Pod, found invalid field restartPolicy for v1.Pod, found invalid field containers for v1.Pod, found invalid field image for v1.Pod]; if you choose to ignore these errors, turn validation off with --validate=false
```
