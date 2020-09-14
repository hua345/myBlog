# 分布式一致性算法

## 参考

- [https://raft.github.io/raftscope/index.html](https://raft.github.io/raftscope/index.html)
- [分布式一致性协议介绍（Paxos、Raft）](https://www.cnblogs.com/zhang-qc/p/8688258.html)
- [分布式一致性算法-Paxos、Raft、ZAB、Gossip](https://zhuanlan.zhihu.com/p/130332285)
- [分布式一致性算法](https://www.jianshu.com/p/40dbe406d2f4)

## `CAP`理论

一个分布式系统不可能同时满足一致性`C:Consistency`，可用性`A: Availability`和分区容错性`P：Partition tolerance`这三个基本需求，`最多只能同时满足其中的 2 个`。

| 选项                      | 描述                                                                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `C(Consistence)`          | 一致性，指数据在多个副本之间能够保持一致的特性（严格的一致性）。                                                             |
| `A(Availability)`         | 可用性，指系统提供的服务必须一直处于可用的状态，每次请求都能获取到非错的响应——但是不保证获取的数据为最新数据。               |
| `P(Network partitioning)` | 分区容错性，分布式系统在遇到任何网络分区故障的时候，仍然能够对外提供满足一致性和可用性的服务，除非整个网络环境都发生了故障。 |

## `Base`理论

`BASE` 是 `Basically Available`(基本可用)，`Soft state`（软状态）,和`Eventually consistent`（最终一致性）三个短语的缩写。

## 一致性的分类

### 强一致性

说明：保证系统改变提交以后立即改变集群的状态。
模型：

- Paxos
- Raft（muti-paxos）
- ZAB（muti-paxos）

### 弱一致性

说明：也叫最终一致性，系统不保证改变提交以后立即改变集群的状态，但是随着时间的推移最终状态是一致的。
模型：

- DNS 系统
- Gossip 协议

### 一致性算法实现举例

Google 的 Chubby 分布式锁服务，采用了 Paxos 算法
`etcd`和`consul`分布式键值数据库，采用了`Raft`算法
`ZooKeeper`分布式应用协调服务，Chubby 的开源实现，采用 ZAB 算法

## 两阶段提交

`Two-phase Commit`（2PC）：保证一个事务跨越多个节点时保持 ACID 特性；

两类节点：协调者(`Coordinator`)和参与者(`Participants`)，协调者只有一个，参与者可以有多个。

过程：

准备阶段：`协调者询问参与者事务是否执行成功`.

提交阶段：如果事务在每个参与者上都执行成功，协调者发送通知让参与者提交事务；否则，协调者发送通知让参与者回滚事务。

## Raft 算法

说明：Paxos 算法不容易实现，Raft 算法是对 Paxos 算法的简化和改进
概念介绍

- `Leader`总统节点，负责发出提案
- `Follower`追随者节点，负责同意`Leader`发出的提案
- `Candidate`候选人，负责争夺`Leader`

`Raft`算法将一致性问题分解为两个的子问题，`Leader选举`和`状态复制`

`raft` 最关键的一个概念是任期，每一个 `leader` 都有自己的任期，必须在任期内发送心跳信息给 `follower` 来延长自己的任期。

`Leader` 会周期性的发送心跳包给 `Follower`。每个 `Follower` 都设置了一个随机的竞选超时时间，一般为 150ms~300ms，如果在这个时间内没有收到 `Leader` 的心跳包，就会变成 `Candidate`，进入竞选阶段。

下图表示一个分布式系统的最初阶段，此时只有 `Follower`，没有 `Leader`。`Follower A` 等待一个随机的竞选超时时间之后，没收到 `Leader` 发来的心跳包，因此进入竞选阶段。
