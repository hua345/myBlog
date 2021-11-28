`etcd是一个高可用的键值存储系统，主要用于共享配置和服务发现`。`etcd`是由CoreOS开发并维护的，灵感来自于` ZooKeeper` 和 `Doozer`，它使用Go语言编写，并通过Raft一致性算法处理日志复制以保证强一致性。`Raft`是一个来自`Stanford`的新的一致性算法，适用于分布式系统的日志复制，`Raft`通过选举的方式来实现一致性，在`Raft`中，任何一个节点都可能成为`Leader`。

>分布式系统中的数据分为控制数据和应用数据。
使用etcd的场景默认处理的数据都是控制数据，对于应用数据，只推荐数据量很小，但是更新访问频繁的情况。

#### 1.etcd的特性如下

- 简单: curl可访问的用户的API（HTTP+JSON）
- 安全: 可选的SSL客户端证书认证
- 快速: 单实例每秒 1000 次写操作
- 可靠: 使用Raft保证一致性

### 2.[源码编译](https://github.com/coreos/etcd)

```bash
# go is required
$ go version
go version go1.6.2 linux/amd64
# GOPATH should be set correctly
$ echo $GOPATH
/home/chenjianhua/gocode:/home/chenjianhua/myGolang
$ cd /home/chenjianhua/myGolang/src
$ git clone https://github.com/etcd-io/etcd.git 
$ cd etcd
$ ./build
```

### 3.运行服务和简单`Key Value`操作

```bash
$ ./bin/etcd

#etcdctl
#etcdctl最新版本是v3.设置环境变量ETCDCTL_API=3
$export ETCDCTL_API=3
$etcdctl version
etcdctl version: 3.2.18
API vetsion: 3.2

# Set a key
$ ./bin/etcdctl put msg "hello"
$ OK
# Get a key
$ ./bin/etcdctl get msg
$ msg
$ hello
# Delete a key
$ ./bin/etcdctl del msg
# 1
```

### 4.`watch`监听

`watch`后`etcdctl`阻塞，当另一个终端监听的值改变时，`watch`触发

```bash
$ etcdctl watch event1
# PUT
# event1
# hello
# DELETE
# event1
```

### 5.`lease`租约

etcd也能为`key`设置超时时间，但与`redis`不同，需要先创建`lease`，然后使用put命令加上参数`--lease=<lease ID>来设置

```bash
# 创建lease
$ etcdctl lease grant 1000
$ lease 694d6280d047720f granted with TTL(1000s)

# 设置key value 存活时间
$ etcdctl put name "fang" --lease=694d6280d047720f
$ OK

# 查询lease剩余时间
$ etcdctl lease timetolive 694d6280d047720f
$ lease 694d6275d93d3e0c granted with TTL(100s), remaining(968s)

# 查询lease剩余时间和关联的keys
$ etcdctl lease timetolive  694d6280d047720f --keys
$ lease 694d6280d047720f granted with TTL(1000s), remaining(755s), attached keys([name])

# 刷新lease存活时间
$ etcdctl lease keep-alive 694d6280d047720f
$ lease 694d6280d047720f keepalived with TTL(1000)

# 删除lease，并删除所有关联的key
$ etcdctl lease revoke 694d6280d047720f
$ lease 694d6280d047720f revoked

```

#### 参考:[etcd：从应用场景到实现原理的全方位解读](http://www.infoq.com/cn/articles/etcd-interpretation-application-scenario-implement-principle)
