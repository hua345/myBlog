# redis集群介绍

> 分布式数据库需要解决数据分区问题，redis cluster采用虚拟槽分区来对数据进行划分。
> redis cluster的虚拟槽固定为16384个，编号为0~16383。
> 槽（slot）是集群管理和迁移的基本单位，每个节点会负责一定数量的槽。一个key只对应一个槽。

![redis01](img/redis01.png)

有了槽之后，节点可以动态的变化管理槽的数量，这样集群的伸缩更加灵活。
但是同时由于槽的存在，redis的一些操作也受到了限制。

- key批量操作支持有限，例如mget，mset，目前只支持具有相同slot值的key执行批量操作，对于隐射不同slot值的key由于执行mget，mset等操作存在于多个不同的节点而不被支持
- key事务操作支持有限。同样也只支持多key在同一节点上的操作，当多个key位于不同节点时无法使用事务功能。、
- key作为数据分区的最小粒度，不能将一个大key，比如list，hash映射到不同节点上。
- 不支持多数据库空间，单机下redis支持16个库，集群下只支持一个库，即db0
- 复制结构只支持一层，从节点只能复制主节点，不支持嵌套树状复制结构

## 查看帮助

```bash
192.168.137.128:6380> cluster help
 1) CLUSTER <subcommand> arg arg ... arg. Subcommands are:
 2) ADDSLOTS <slot> [slot ...] -- Assign slots to current node.
 3) BUMPEPOCH -- Advance the cluster config epoch.
 4) COUNT-failure-reports <node-id> -- Return number of failure reports for <node-id>.
 5) COUNTKEYSINSLOT <slot> - Return the number of keys in <slot>.
 6) DELSLOTS <slot> [slot ...] -- Delete slots information from current node.
 7) FAILOVER [force|takeover] -- Promote current replica node to being a master.
 8) FORGET <node-id> -- Remove a node from the cluster.
 9) GETKEYSINSLOT <slot> <count> -- Return key names stored by current node in a slot.
10) FLUSHSLOTS -- Delete current node own slots information.
11) INFO - Return onformation about the cluster.
12) KEYSLOT <key> -- Return the hash slot for <key>.
13) MEET <ip> <port> [bus-port] -- Connect nodes into a working cluster.
14) MYID -- Return the node id.
15) NODES -- Return cluster configuration seen by node. Output format:
16)     <id> <ip:port> <flags> <master> <pings> <pongs> <epoch> <link> <slot> ... <slot>
17) REPLICATE <node-id> -- Configure current node as replica to <node-id>.
18) RESET [hard|soft] -- Reset current node (default: soft).
19) SET-config-epoch <epoch> - Set config epoch of current node.
20) SETSLOT <slot> (importing|migrating|stable|node <node-id>) -- Set slot state.
21) REPLICAS <node-id> -- Return <node-id> replicas.
22) SLOTS -- Return information about slots range mappings. Each range is made of:
23)     start, end, master and replicas IP addresses, ports and ids
```

## 查看集群节点信息

```bash
127.0.0.1:6379> cluster nodes
892fa7b02be417a6d9931820865c45cc69a4f1e8 192.168.137.128:6384@16384 slave 1d68c7a36bc00be3f0df7b7096a4a367e23a3610 0 1565855145501 6 connected
2cb873af1acd97f2b5bee1394ed67744335cea20 192.168.137.128:6383@16383 slave c793350910a9c04c8748ba2c4cf6a4543edf182f 0 1565855145000 5 connected
52ec5a1fe99e6b885bb0039fad90eed83c99e13a 192.168.137.128:6382@16382 slave c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7 0 1565855146524 4 connected
c793350910a9c04c8748ba2c4cf6a4543edf182f 192.168.137.128:6381@16381 master - 0 1565855145000 3 connected 10923-16383
1d68c7a36bc00be3f0df7b7096a4a367e23a3610 192.168.137.128:6379@16379 myself,master - 0 1565855146000 1 connected 0-5460
c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7 192.168.137.128:6380@16380 master - 0 1565855145000 2 connected 5461-10922
```

## 查看集群信息

```bash
127.0.0.1:6379> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_ping_sent:5935
cluster_stats_messages_pong_sent:6265
cluster_stats_messages_sent:12200
cluster_stats_messages_ping_received:6260
cluster_stats_messages_pong_received:5935
cluster_stats_messages_meet_received:5
cluster_stats_messages_received:12200
```

## 查看插槽分配

```bash
192.168.137.128:6380> cluster slots
1) 1) (integer) 5461
   2) (integer) 10922
   3) 1) "192.168.137.128"
      2) (integer) 6380
      3) "c445aaf6edc938bac25fa710bf30c9bdd0f7ccc7"
   4) 1) "192.168.137.128"
      2) (integer) 6382
      3) "52ec5a1fe99e6b885bb0039fad90eed83c99e13a"
2) 1) (integer) 0
   2) (integer) 5460
   3) 1) "192.168.137.128"
      2) (integer) 6384
      3) "892fa7b02be417a6d9931820865c45cc69a4f1e8"
   4) 1) "192.168.137.128"
      2) (integer) 6379
      3) "1d68c7a36bc00be3f0df7b7096a4a367e23a3610"
3) 1) (integer) 10923
   2) (integer) 16383
   3) 1) "192.168.137.128"
      2) (integer) 6381
      3) "c793350910a9c04c8748ba2c4cf6a4543edf182f"
   4) 1) "192.168.137.128"
      2) (integer) 6383
      3) "2cb873af1acd97f2b5bee1394ed67744335cea20"
```
