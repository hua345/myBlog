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

## 1. 创建 topic

Let's create a topic named "test" with a single partition and only one replica

```bash
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 1 --topic fang

➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 3 --topic love
```

### 修改主题的分区数量

修改后的分区需要比当前分区数量大,如果当前分区数是`3`,改为分区数为`2`,则会报如下错误
`Topic currently has 3 partitions, which is higher than the requested 2.`

```bash
kafka-topics.sh --bootstrap-server 192.168.137.128:9092 --alter --topic love --partitions 4
```

在三台 kafka 上都可以查看`topic`详情

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
- “replicas”是复制分区日志的节点列表，不管这些节点是 leader 还是仅仅活着。
- “isr”是一组“同步”replicas，是 replicas 列表的子集，它活着并被指到 leader。

## 2. 发送消息

```bash
➜  ~ kafka-console-producer.sh --broker-list 192.168.137.128:9092 --topic love
>hello world
>fang love you
```

## 3. 启动简单的消费者

在三台 kafka 上都可以接收到消息

```bash
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fang --group fangGroup --from-beginning
hello world
fang love you
```

## 4 查询消费组信息

```bash
# 查询消费组列表
➜  ~ kafka-consumer-groups.sh  --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094  --list
fangGroup
# 查询消费组消费情况
➜  ~ kafka-consumer-groups.sh  --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094  --describe --group fangGroup

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                               HOST             CLIENT-ID
fangGroup       fang            0          5               5               0               consumer-fangGroup-1-b2ad52a9-e446-45a8-8ed6-74b0bdeb502f /192.168.137.128 consumer-fangGroup-1
```

## 吞吐量测试

```bash
kafka-producer-perf-test.sh --topic fang --num-records 100000 --record-size 150 --throughput -1 --producer-props bootstrap.servers=192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 acks=-1

62730 records sent, 12491.0 records/sec (1.79 MB/sec), 2520.9 ms avg latency, 3920.0 ms max latency.
100000 records sent, 12856.775521 records/sec (1.84 MB/sec), 3335.59 ms avg latency, 6028.00 ms max latency, 3404 ms 50th, 5393 ms 95th, 6010 ms 99th, 6026 ms 99.9th.
```

### kafka-console-consumer 参数说明

```bash
➜  ~ kafka-console-consumer.sh h
Exactly one of whitelist/topic is required.
Option                                   Description
------                                   -----------
--from-beginning                         If the consumer does not already have
                                           an established offset to consume
                                           from, start with the earliest
                                           message present in the log rather
                                           than the latest message.
--group <String: consumer group id>      The consumer group id of the consumer.
--max-messages <Integer: num_messages>   The maximum number of messages to
                                           consume before exiting. If not set,
                                           consumption is continual.
--offset <String: consume offset>        The offset id to consume from (a non-
                                           negative number), or 'earliest'
                                           which means from beginning, or
                                           'latest' which means from end
                                           (default: latest)
--partition <Integer: partition>         The partition to consume from.
                                           Consumption starts from the end of
                                           the partition unless '--offset' is
                                           specified.

```
