# 参考

- [redis创建集群时显示错误： [ERR] Node xxx is not empty.](https://blog.csdn.net/XIANZHIXIANZHIXIAN/article/details/82777767)
- [redis实战第七篇 使用redis工具（redis-cli）搭建redis cluster](https://blog.csdn.net/u012062455/article/details/87280467)

## 修改配置文件

```bash
cp ./redis-5.0.5/redis.conf ./redis01.conf
cp redis01.conf redis02.conf
cp redis01.conf redis03.conf
cp redis01.conf redis04.conf
cp redis01.conf redis05.conf
cp redis01.conf redis06.conf
redis-server redis01.conf
```

分别修改这三个配置文件，修改如下内容

```conf
# 绑定地址
bind 0.0.0.0
# By default protected mode is enabled. You should disable it only if
# you are sure you want clients from other hosts to connect to Redis
# even if no authentication is configured, nor a specific set of interfaces
# are explicitly listed using the "bind" directive.
protected-mode no
# 端口号6379,6380,6381
port 6379
# 后台启动
daemonize yes
# pidfile redis_6379.pid,redis_6380.pid,redis_6381.pid
pidfile  /var/run/redis_6379.pid
# 数据文件存储位置data01，data02，data03
dir /root/redis/data01
################################ REDIS CLUSTER  ###############################

# Normal Redis instances can't be part of a Redis Cluster; only nodes that are
# started as cluster nodes can. In order to start a Redis instance as a
# cluster node enable the cluster support uncommenting the following:
#
cluster-enabled  yes
# Every cluster node has a cluster configuration file. This file is not
# intended to be edited by hand. It is created and updated by Redis nodes.
# Every Redis Cluster node requires a different cluster configuration file.
# Make sure that instances running in the same system do not have
# overlapping cluster configuration file names.
# 配置文件首次启动自动生成 nodes-6379.conf,nodes-6380.conf,nodes-6381.conf
cluster-config-file nodes-6379.conf

# Cluster node timeout is the amount of milliseconds a node must be unreachable
# for it to be considered in failure state.
# Most other internal time limits are multiple of the node timeout.
#
cluster-node-timeout  1500
```

## 启动redis

```bash
redis-server ~/redis/redis01.conf
redis-server ~/redis/redis02.conf
redis-server ~/redis/redis03.conf
redis-server ~/redis/redis04.conf
redis-server ~/redis/redis05.conf
redis-server ~/redis/redis06.conf
```

## 查看启动情况

```bash
➜  redis netstat -nltup
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      5466/mysqld
tcp        0      0 0.0.0.0:6379            0.0.0.0:*               LISTEN      93511/redis-server
tcp        0      0 0.0.0.0:6380            0.0.0.0:*               LISTEN      93520/redis-server
tcp        0      0 0.0.0.0:6381            0.0.0.0:*               LISTEN      93529/redis-server
tcp        0      0 0.0.0.0:6382            0.0.0.0:*               LISTEN      93686/redis-server
tcp        0      0 0.0.0.0:6383            0.0.0.0:*               LISTEN      93695/redis-server
tcp        0      0 0.0.0.0:6384            0.0.0.0:*               LISTEN      93704/redis-server
tcp        0      0 0.0.0.0:16379           0.0.0.0:*               LISTEN      93511/redis-server
tcp        0      0 0.0.0.0:16380           0.0.0.0:*               LISTEN      93520/redis-server
tcp        0      0 0.0.0.0:16381           0.0.0.0:*               LISTEN      93529/redis-server
tcp        0      0 0.0.0.0:16382           0.0.0.0:*               LISTEN      93686/redis-server
tcp        0      0 0.0.0.0:16383           0.0.0.0:*               LISTEN      93695/redis-server
tcp        0      0 0.0.0.0:16384           0.0.0.0:*               LISTEN      93704/redis-server
```

## 查看帮助

```bash
➜  redis redis-cli --cluster help
Cluster Manager Commands:
  create         host1:port1 ... hostN:portN
                 --cluster-replicas <arg>
  check          host:port
                 --cluster-search-multiple-owners
  info           host:port
  fix            host:port
                 --cluster-search-multiple-owners
  reshard        host:port
                 --cluster-from <arg>
                 --cluster-to <arg>
                 --cluster-slots <arg>
                 --cluster-yes
                 --cluster-timeout <arg>
                 --cluster-pipeline <arg>
                 --cluster-replace
  rebalance      host:port
                 --cluster-weight <node1=w1...nodeN=wN>
                 --cluster-use-empty-masters
                 --cluster-timeout <arg>
                 --cluster-simulate
                 --cluster-pipeline <arg>
                 --cluster-threshold <arg>
                 --cluster-replace
  add-node       new_host:new_port existing_host:existing_port
                 --cluster-slave
                 --cluster-master-id <arg>
  del-node       host:port node_id
  call           host:port command arg arg .. arg
  set-timeout    host:port milliseconds
  import         host:port
                 --cluster-from <arg>
                 --cluster-copy
                 --cluster-replace
```

## 使用redis-cli创建集群

redis-cli会按照给定的顺序设置主节点和从节点

```bash
redis-cli --cluster create 192.168.137.128:6379 192.168.137.128:6380  192.168.137.128:6381 192.168.137.128:6382 192.168.137.128:6383  192.168.137.128:6384 --cluster-replicas 1
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 192.168.137.128:6383 to 192.168.137.128:6379
Adding replica 192.168.137.128:6384 to 192.168.137.128:6380
Adding replica 192.168.137.128:6382 to 192.168.137.128:6381
>>> Trying to optimize slaves allocation for anti-affinity
[WARNING] Some slaves are in the same host as their master
M: 1d68c7a36bc00be3f0df7b7096a4a367e23a3610 192.168.137.128:6379
   slots:[0-5460] (5461 slots) master
M: c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7 192.168.137.128:6380
   slots:[5461-10922] (5462 slots) master
M: c793350910a9c04c8748ba2c4cf6a4543edf182f 192.168.137.128:6381
   slots:[10923-16383] (5461 slots) master
S: 52ec5a1fe99e6b885bb0039fad90eed83c99e13a 192.168.137.128:6382
   replicates c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7
S: 2cb873af1acd97f2b5bee1394ed67744335cea20 192.168.137.128:6383
   replicates c793350910a9c04c8748ba2c4cf6a4543edf182f
S: 892fa7b02be417a6d9931820865c45cc69a4f1e8 192.168.137.128:6384
   replicates 1d68c7a36bc00be3f0df7b7096a4a367e23a3610
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
.....
>>> Performing Cluster Check (using node 192.168.137.128:6379)
M: 1d68c7a36bc00be3f0df7b7096a4a367e23a3610 192.168.137.128:6379
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
S: 892fa7b02be417a6d9931820865c45cc69a4f1e8 192.168.137.128:6384
   slots: (0 slots) slave
   replicates 1d68c7a36bc00be3f0df7b7096a4a367e23a3610
S: 2cb873af1acd97f2b5bee1394ed67744335cea20 192.168.137.128:6383
   slots: (0 slots) slave
   replicates c793350910a9c04c8748ba2c4cf6a4543edf182f
S: 52ec5a1fe99e6b885bb0039fad90eed83c99e13a 192.168.137.128:6382
   slots: (0 slots) slave
   replicates c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7
M: c793350910a9c04c8748ba2c4cf6a4543edf182f 192.168.137.128:6381
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
M: c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7 192.168.137.128:6380
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

## 集群完整性检查

```bash
➜  ~ redis-cli --cluster check 127.0.0.1:6380
127.0.0.1:6380 (c445aaf6...) -> 0 keys | 5462 slots | 1 slaves.
192.168.137.128:6379 (1d68c7a3...) -> 0 keys | 5461 slots | 1 slaves.
192.168.137.128:6381 (c7933509...) -> 0 keys | 5461 slots | 1 slaves.
[OK] 0 keys in 3 masters.
0.00 keys per slot on average.
>>> Performing Cluster Check (using node 127.0.0.1:6380)
M: c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7 127.0.0.1:6380
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: 52ec5a1fe99e6b885bb0039fad90eed83c99e13a 192.168.137.128:6382
   slots: (0 slots) slave
   replicates c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7
M: 1d68c7a36bc00be3f0df7b7096a4a367e23a3610 192.168.137.128:6379
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: c793350910a9c04c8748ba2c4cf6a4543edf182f 192.168.137.128:6381
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: 892fa7b02be417a6d9931820865c45cc69a4f1e8 192.168.137.128:6384
   slots: (0 slots) slave
   replicates 1d68c7a36bc00be3f0df7b7096a4a367e23a3610
S: 2cb873af1acd97f2b5bee1394ed67744335cea20 192.168.137.128:6383
   slots: (0 slots) slave
   replicates c793350910a9c04c8748ba2c4cf6a4543edf182f
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

## 集群测试

```bash
➜  ~ redis-cli -p 6380
127.0.0.1:6380> set name fang
OK
127.0.0.1:6380> get name
"fang"

# 正常重定向
➜  ~ redis-cli -p 6381
127.0.0.1:6381> get name
(error) MOVED 5798 192.168.137.128:6380
```

## 出现的问题

### 需要至少六个节点

```bash
*** ERROR: Invalid configuration for cluster creation.
*** Redis Cluster requires at least 3 master nodes.
*** This is not possible with 3 nodes and 1 replicas per node.
*** At least 6 nodes are required.
```

### 创建集群错误

```bash
[ERR] Node 192.168.137.128:6379 is not empty. Either the node already knows other nodes (check with CLUSTER NODES) or contains some key in database 0.
```

#### 使用redis-cli -c -h -p登录每个redis节点，使用以下命令

```bash
flushdb
cluster reset
```

#### 删除每个redis节点的备份文件，数据库文件和集群配置文件

删除每个节点appendonly.aof、dump.rdb、node_xxx.conf

```bash
➜  redis ls data01
dump.rdb  nodes-6379.conf
```

#### 重启所有的redis服务，再试试redis集群连接命令
