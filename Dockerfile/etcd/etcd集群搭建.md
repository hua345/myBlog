#### 1.下载Etcd

[https://github.com/etcd-io/etcd/releases](https://github.com/etcd-io/etcd/releases)

#### 2.虚拟机信息

| Ip | etcdName|
|------------|---------------|
|192.168.137.89|etcd01|
|192.168.137.105|etcd02|
|192.168.137.97|etcd03|

#### 3.[Yaml配置文件启动](https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/configuration.md)

```yaml
#etcd01：
#etcd集群中的节点名
name: etcd01
#数据存放目录
data-dir: /var/lib/etcd
#监听的用于客户端通信的url,同样可以监听多个。
listen-client-urls: http://192.168.137.89:2379,http://127.0.0.1:2379
#建议使用的客户端通信url,该值用于etcd代理或etcd成员与etcd节点通信。
advertise-client-urls: http://192.168.137.89:2379,http://127.0.0.1:2379
#监听的用于节点之间通信的url，可监听多个，集群内部将通过这些url进行数据交互(如选举，数据同步等)
listen-peer-urls: http://192.168.137.89:2380
#建议用于节点之间通信的url，节点间将以该值进行通信。
initial-advertise-peer-urls: http://192.168.137.89:2380
#也就是集群中所有的initial-advertise-peer-urls 的合集
initial-cluster: etcd01=http://192.168.137.89:2380,etcd02=http://192.168.137.105:2380,etcd03=http://192.168.137.97:2380
#节点的token值，设置该值后集群将生成唯一id,并为每个节点也生成唯一id,当使用相同配置文件再启动一个集群时，只要该token值不一样，etcd集群就不会相互影响。
initial-cluster-token: k8s-etcd-cluster
#新建集群的标志，初始化状态使用 new，建立之后改此值为 existing
initial-cluster-state: new
#etcd02：
name: etcd02
data-dir: /var/lib/etcd
listen-client-urls: http://192.168.137.105:2379,http://127.0.0.1:2379
advertise-client-urls: http://192.168.137.105:2379,http://127.0.0.1:2379
listen-peer-urls: http://192.168.137.105:2380
initial-advertise-peer-urls: http://192.168.137.105:2380
initial-cluster: etcd01=http://192.168.137.89:2380,etcd02=http://192.168.137.105:2380,etcd03=http://192.168.137.97:2380
initial-cluster-token: k8s-etcd-cluster
initial-cluster-state: new
#etcd03：
name: etcd03
data-dir: /var/lib/etcd
listen-client-urls: http://192.168.137.97:2379,http://127.0.0.1:2379
advertise-client-urls: http://192.168.137.97:2379,http://127.0.0.1:2379
listen-peer-urls: http://192.168.137.97:2380
initial-advertise-peer-urls: http://192.168.137.97:2380
initial-cluster: etcd01=http://192.168.137.89:2380,etcd02=http://192.168.137.105:2380,etcd03=http://192.168.137.97:2380
initial-cluster-token: k8s-etcd-cluster
initial-cluster-state: new
```

#### 4.启动etcd

```bash
etcd --config-file ~/etcd.yaml
```

#### 5.访问etcd集群

```bash
[root@localhost ~]# ETCDCTL_API=3 etcdctl member list
98665f721f5a04bc, started, etcd02, http://192.168.137.105:2380, http://127.0.0.1:2379,http://192.168.137.105:2379
b25b7cce630db8e4, started, etcd01, http://192.168.137.89:2380, http://127.0.0.1:2379,http://192.168.137.89:2379
dd4948cb7ad732bb, started, etcd03, http://192.168.137.97:2380, http://127.0.0.1:2379,http://192.168.137.97:2379
[root@localhost ~]# etcdctl member list
98665f721f5a04bc: name=etcd02 peerURLs=http://192.168.137.105:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.105:2379 isLeader=false
b25b7cce630db8e4: name=etcd01 peerURLs=http://192.168.137.89:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.89:2379 isLeader=false
dd4948cb7ad732bb: name=etcd03 peerURLs=http://192.168.137.97:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.97:2379 isLeader=true
[root@localhost ~]# etcdctl cluster-health
member 98665f721f5a04bc is healthy: got healthy result from http://127.0.0.1:2379
member b25b7cce630db8e4 is healthy: got healthy result from http://127.0.0.1:2379
member dd4948cb7ad732bb is healthy: got healthy result from http://127.0.0.1:2379
cluster is healthy
[root@localhost ~]# etcdctl --endpoints=http://192.168.137.89:2379  set name fang
fang
[root@localhost ~]# etcdctl --endpoints=http://192.168.137.89:2379  get name
fang
```

#### 6.[运行时动态扩容](https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/runtime-configuration.md)

目前`etcd`可以支持在线动态扩容，无须重启`etcd`集群

#### 6.1虚拟机信息

| Ip | etcdName|
|------------|---------------|
|192.168.137.89|etcd01|
|192.168.137.105|etcd02|
|192.168.137.97|etcd03|
|192.168.137.218|etcd04|

#### 6.2添加新的节点

```bash
[root@localhost ~]# etcdctl --endpoints=http://192.168.137.89:2379,http://192.168.137.105:2379,http://192.168.137.97:2379 member add etcd04 http://192.168.137.218:2380
Added member named etcd04 with ID 94cac437e66f2ad to cluster

ETCD_NAME="etcd04"
ETCD_INITIAL_CLUSTER="etcd04=http://192.168.137.218:2380,etcd02=http://192.168.137.105:2380,etcd01=http://192.168.137.89:2380,etcd03=http://192.168.137.97:2380"
ETCD_INITIAL_CLUSTER_STATE="existing"
```

#### 6.3启动新的节点

```bash
[root@localhost ~]# vi ~/etcd.yaml
name: etcd04
data-dir: /var/lib/etcd
listen-client-urls: http://192.168.137.218:2379,http://127.0.0.1:2379
advertise-client-urls: http://192.168.137.218:2379,http://127.0.0.1:2379
listen-peer-urls: http://192.168.137.218:2380
initial-advertise-peer-urls: http://192.168.137.218:2380
initial-cluster: etcd04=http://192.168.137.218:2380,etcd02=http://192.168.137.105:2380,etcd01=http://192.168.137.89:2380,etcd03=http://192.168.137.97:2380
initial-cluster-token: k8s-etcd-cluster
initial-cluster-state: existing
#启动etcd
[root@localhost ~]# etcd --config-file ~/etcd.yaml
#查看集群信息
[root@localhost ~]# etcdctl cluster-health
member 94cac437e66f2ad is healthy: got healthy result from http://127.0.0.1:2379
member 98665f721f5a04bc is healthy: got healthy result from http://127.0.0.1:2379
member b25b7cce630db8e4 is healthy: got healthy result from http://127.0.0.1:2379
member dd4948cb7ad732bb is healthy: got healthy result from http://127.0.0.1:2379
cluster is healthy
[root@localhost ~]# etcdctl member list
94cac437e66f2ad: name=etcd04 peerURLs=http://192.168.137.218:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.218:2379 isLeader=false
98665f721f5a04bc: name=etcd02 peerURLs=http://192.168.137.105:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.105:2379 isLeader=false
b25b7cce630db8e4: name=etcd01 peerURLs=http://192.168.137.89:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.89:2379 isLeader=false
dd4948cb7ad732bb: name=etcd03 peerURLs=http://192.168.137.97:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.97:2379 isLeader=true
```

#### 6.4节点去除命令

```bash
[root@localhost ~]# etcdctl --endpoints=http://192.168.137.89:2379,http://192.168.137.105:2379,http://192.168.137.97:2379 member remove 94cac437e66f2ad
Removed member 94cac437e66f2ad from cluster
```

#### 6.5 修改配置文件

将配置文件的`initial-cluster`的值更新为4台信息即可，已便以后etcd集群启动时可以通过配置正常加载
#### 7. [通过服务发现扩容](https://github.com/etcd-io/etcd/blob/master/Documentation/op-guide/clustering.md#discovery)

#### 7.1 etcd发现服务

```bash
[root@localhost ~]# curl -X PUT http://192.168.137.218:2379/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size -d value=3
{"action":"set","node":{"key":"/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83/_config/size","value":"3","modifiedIndex":4,"createdIndex":4}}

#公共etcd发现服务
[root@localhost ~]# curl https://discovery.etcd.io/new?size=3
https://discovery.etcd.io/8b2eb37ec28448699a46c126b065ba51
```

#### 7.2 etcd配置

```yaml
#etcd01
name: etcd01
data-dir: /var/lib/etcd
listen-client-urls: http://192.168.137.89:2379,http://127.0.0.1:2379
advertise-client-urls: http://192.168.137.89:2379,http://127.0.0.1:2379
listen-peer-urls: http://192.168.137.89:2380
initial-advertise-peer-urls: http://192.168.137.89:2380
#discovery: http://192.168.137.218:2379/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
discovery: https://discovery.etcd.io/8b2eb37ec28448699a46c126b065ba51
#etcd02：
name: etcd02
data-dir: /var/lib/etcd
listen-client-urls: http://192.168.137.105:2379,http://127.0.0.1:2379
advertise-client-urls: http://192.168.137.105:2379,http://127.0.0.1:2379
listen-peer-urls: http://192.168.137.105:2380
initial-advertise-peer-urls: http://192.168.137.105:2380
#discovery: http://192.168.137.218:2379/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
discovery: https://discovery.etcd.io/8b2eb37ec28448699a46c126b065ba51
#etcd03：
name: etcd03
data-dir: /var/lib/etcd
listen-client-urls: http://192.168.137.97:2379,http://127.0.0.1:2379
advertise-client-urls: http://192.168.137.97:2379,http://127.0.0.1:2379
listen-peer-urls: http://192.168.137.97:2380
initial-advertise-peer-urls: http://192.168.137.97:2380
#discovery: http://192.168.137.218:2379/v2/keys/discovery/6c007a14875d53d9bf0ef5a6fc0257c817f0fb83
discovery: https://discovery.etcd.io/8b2eb37ec28448699a46c126b065ba51
```

#### 7.3 启动集群

```bash
[root@localhost ~]# etcd --config-file ~/etcdDiscovery.yaml
[root@localhost ~]# etcdctl member list
98665f721f5a04bc: name=etcd02 peerURLs=http://192.168.137.105:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.105:2379 isLeader=false
b25b7cce630db8e4: name=etcd01 peerURLs=http://192.168.137.89:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.89:2379 isLeader=true
dd4948cb7ad732bb: name=etcd03 peerURLs=http://192.168.137.97:2380 clientURLs=http://127.0.0.1:2379,http://192.168.137.97:2379 isLeader=false
```

#### 8.遇到的问题

#### 8.1 dial tcp **** i/o timeout

```bash
2019-04-03 08:26:12.590325 W | rafthttp: health check for peer 98665f721f5a04bc could not connect: dial tcp 192.168.137.105:2380: i/o timeout (prober "ROUND_TRIPPER_SNAPSHOT")
2019-04-03 08:26:12.590352 W | rafthttp: health check for peer 98665f721f5a04bc could not connect: dial tcp 192.168.137.105:2380: connect: no route to host (prober "ROUND_TRIPPER_RAFT_MESSAGE")
```

```bash
$ telnet  192.168.137.105
Trying 192.168.137.105...
telnet: connect to address 192.168.137.105: No route to host
# 在192.168.137.105电脑上，#清空防火墙fllter表所有链
$ iptables -F
$ telnet  192.168.137.105
Trying 192.168.137.105...
telnet: connect to address 192.168.137.105: Connection refused
```

#### 8.2 集群id不匹配

```bash
rafthttp: request cluster ID mismatch (got d9dad96810d1fea6 want cdf818194e3a8c32)
```

主要是因为数据目录没有删除，然后导致集群的id不匹配，删除数据目录，然后重新加入即可

#### 8.3 时钟不同步

```bash
rafthttp: the clock difference against peer dd4948cb7ad732bb is too high [7h16m58.537626179s > 1s] (prober "ROUND_TRIPPER_SNAPSHOT")
rafthttp: the clock difference against peer 98665f721f5a04bc is too high [18h30m30.990978651s > 1s] (prober"ROUND_TRIPPER_RAFT_MESSAGE")
```

使用ntpdate进行时间同步

```bash
yum install ntpdate
ntpdate cn.pool.ntp.org
```
