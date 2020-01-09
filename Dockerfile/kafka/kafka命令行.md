# 参考

## 查看帮助

```sql
➜  ~ kafka-topics.sh
Create, delete, describe, or change a topic.
Option                                   Description
------                                   -----------
--alter                                  Alter the number of partitions,
                                           replica assignment, and/or
--bootstrap-server <String: server to    REQUIRED: The Kafka server to connect
  connect to>                              to. In case of providing this, a
                                           direct Zookeeper connection won't be
                                           required.
--create                                 Create a new topic.
--delete                                 Delete a topic
--delete-config <String: name>           A topic configuration override to be
                                           removed for an existing topic (see
                                           the list of configurations under the
                                           --config option). Not supported with
                                           the --bootstrap-server option.
--describe                               List details for the given topics.
--help                                   Print usage information.
--if-exists                              if set when altering or deleting or
                                           describing topics, the action will
                                           only execute if the topic exists.
                                           Not supported with the --bootstrap-
                                           server option.
--if-not-exists                          if set when creating topics, the
                                           action will only execute if the
                                           topic does not already exist. Not
                                           supported with the --bootstrap-
                                           server option.
--list                                   List all available topics.
--partitions <Integer: # of partitions>  The number of partitions for the topic
                                           being created or altered (WARNING:
                                           If partitions are increased for a
                                           topic that has a key, the partition
                                           logic or ordering of the messages
                                           will be affected
--replication-factor <Integer:           The replication factor for each
  replication factor>                      partition in the topic being created.
```

## 1. 创建topic

Let's create a topic named "test" with a single partition and only one replica

```bash
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 1 --topic fang

➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 3 --topic love
```

在三台kafka上都可以查看`topic`详情

```bash
➜  ~ kafka-topics.sh --describe --bootstrap-server 192.168.137.128:9092 --topic fang
Topic:fang      PartitionCount:1        ReplicationFactor:3     Configs:segment.bytes=1073741824
        Topic: fang     Partition: 0    Leader: 2       Replicas: 2,0,1 Isr: 2,0,1

➜  ~ kafka-topics.sh --describe --bootstrap-server 192.168.137.128:9092 --topic love
Topic:love      PartitionCount:3        ReplicationFactor:3     Configs:segment.bytes=1073741824
        Topic: love     Partition: 0    Leader: 0       Replicas: 0,2,1 Isr: 0,2,1
        Topic: love     Partition: 1    Leader: 2       Replicas: 2,1,0 Isr: 2,1,0
        Topic: love     Partition: 2    Leader: 1       Replicas: 1,0,2 Isr: 1,0,2
```

第一行给出了所有分区的摘要，下面的每行都给出了一个分区的信息。因为我们只有一个分区，所以只有一行。

- “leader”是负责给定分区所有读写操作的节点。每个节点都是随机选择的部分分区的领导者。
- “replicas”是复制分区日志的节点列表，不管这些节点是leader还是仅仅活着。
- “isr”是一组“同步”replicas，是replicas列表的子集，它活着并被指到leader。

## 2. 发送消息

```bash
➜  ~ kafka-console-producer.sh --broker-list 192.168.137.128:9092 --topic love
>hello world
>fang love you
```

## 3. 启动简单的消费者

在三台kafka上都可以接收到消息

```bash
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9093 --topic love --from-beginning
hello world
fang love you
```
