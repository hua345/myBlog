# 参考

- [https://etcd.io/](https://etcd.io/)
- [https://etcd.io/docs/v3.3.12/](https://etcd.io/docs/v3.3.12/)
- [https://github.com/etcd-io/etcd](https://github.com/etcd-io/etcd)

- [etcd Dockerfile](https://github.com/etcd-io/etcd/blob/master/Dockerfile-release)

## 构建脚本

```bash
docker build -t my/etcd:v3.3.13 .
```

### 查看etcd版本

```bash
docker run --rm my/etcd:v3.3.13 /usr/local/bin/etcd --version
docker run --rm my/etcd:v3.3.13 /bin/sh -c "ETCDCTL_API=3 /usr/local/bin/etcdctl version"
```

#### 单节点启动

```bash
docker run \
-p 2379:2379 \
-p 2380:2380 \
--mount type=bind,source=/root/etcd-data/etcd01,destination=/etcd-data \
my/etcd:v3.3.13 \
/usr/local/bin/etcd \
--name etcd01 \
--data-dir /etcd-data \
--listen-client-urls http://0.0.0.0:2379 \
--advertise-client-urls http://0.0.0.0:2379 \
--listen-peer-urls http://0.0.0.0:2380 \
--initial-advertise-peer-urls http://0.0.0.0:2380 \
--initial-cluster etcd01=http://0.0.0.0:2380 \
--initial-cluster-token k8s-etcd-cluster \
--initial-cluster-state new
```
