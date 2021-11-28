# 参考

- [https://etcd.io/docs/v3.3.12/demo/](https://etcd.io/docs/v3.3.12/demo/)

## 查询集群列表

```bash
➜  ~ etcdctl member list
45bfac6c716f67b9, started, etcd01, http://192.168.137.128:2380, http://127.0.0.1:2379,http://192.168.137.128:2379
603a0c88855d47c1, started, etcd03, http://192.168.137.128:32380, http://127.0.0.1:32379,http://192.168.137.128:32379
b6e653038eeb4204, started, etcd02, http://192.168.137.128:22380, http://127.0.0.1:22379,http://192.168.137.128:22379
```

## 键值对命令

```bash
# `put`设置key
etcdctl put foo 'Hello World'

# `get`取得key
etcdctl get foo
etcdctl --write-out="json" get foo
{"header":{"cluster_id":8144621041877720777,"member_id":5025925290928334777,"revision":29,"raft_term":2}}

# `del`删除key
➜  ~ etcdctl del foo
1
```

## 通过Key前缀获取Key

```bash
etcdctl put web1 value1
etcdctl put web2 value2
etcdctl put web3 value3

➜  ~ etcdctl  get web --prefix
web1
value1
web2
value2
web3
value3
➜  ~ etcdctl --write-out="json" get web --prefix
{"header":{"cluster_id":8144621041877720777,"member_id":5025925290928334777,"revision":29,"raft_term":2},"kvs":[{"key":"d2ViMQ==","create_revision":2,"mod_revision":5,"version":2,"value":"dmFsdWUx"},{"key":"d2ViMg==","create_revision":3,"mod_revision":6,"version":2,"value":"dmFsdWUy"},{"key":"d2ViMw==","create_revision":4,"mod_revision":7,"version":2,"value":"dmFsdWUz"}],"count":3}
```

## txn事务

`txn` to wrap multiple requests into one transaction:

```go
var Compare_CompareTarget_name = map[int32]string{
    0: "VERSION",
    1: "CREATE",
    2: "MOD",
    3: "VALUE",
    4: "LEASE",
}
```

```bash
➜  ~ etcdctl put user1 bad
OK
➜  ~ etcdctl txn -i
compares:
value("user1") = "bad"

success requests (get, put, del):
del user1

failure requests (get, put, del):
put user1 good

SUCCESS

1
➜  ~ etcdctl get user1 -w="json"
{"header":{"cluster_id":8144621041877720777,"member_id":5025925290928334777,"revision":4083,"raft_term":10},"kvs":[{"key":"dXNlcjE=","create_revision":4081,"mod_revision":4081,"version":1,"value":"Z29vZA=="}],"count":1}
➜  ~ etcdctl txn -i
compares:
create("user1") = "4081"

success requests (get, put, del):

failure requests (get, put, del):

SUCCESS
```

## watch监听Key的变化

`watch` to get notified of future changes:

```bash
➜  ~ etcdctl watch stock1
➜  ~ etcdctl put stock1 1000
➜  ~ etcdctl watch stock1
PUT
stock1
1000


➜  ~ etcdctl watch stock --prefix
➜  ~ etcdctl put stock1 100
OK
➜  ~ etcdctl watch stock1
PUT
stock1
1000
PUT
stock1
100
➜  ~ etcdctl watch stock --prefix
PUT
stock1
100

➜  ~ etcdctl put stock2 200
OK
➜  ~ etcdctl watch stock --prefix
PUT
stock1
100
PUT
stock2
200
```

## lease租约

`lease` to write with TTL:

```bash
➜  ~ etcdctl lease grant 100
lease 67b96bd7a874305b granted with TTL(100s)

➜  ~ etcdctl put name fang --lease=67b96bd7a874305b
OK
➜  ~ etcdctl get name
name
fang

➜  ~ etcdctl lease keep-alive 67b96bd7a874305b
lease 67b96bd7a874305b keepalived with TTL(100)

➜  ~ etcdctl lease revoke 67b96bd7a874305b
lease 67b96bd7a874305b revoked

# or after 300 seconds
➜  ~ etcdctl get name

```

## lock分布式锁

`lock` for distributed lock:

```bash
➜  ~ etcdctl lock mutex1
mutex1/67b96bd7a8743061

# another client with the same name blocks
➜  ~ etcdctl lock mutex1
```

## 选举

elect for leader election:

```bash
➜  ~ etcdctl elect one etcd01
one/67b96bd7a874307e
etcd01

# another client with the same name blocks
➜  ~ etcdctl elect one etcd02
```
