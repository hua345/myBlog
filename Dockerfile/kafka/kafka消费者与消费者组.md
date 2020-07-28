# 消费者与消费者组

> `consumer group`是kafka提供的可扩展且具有容错性的消费者机制。既然是一个组，那么组内必然可以有多个消费者或消费者实例`(consumer instance)`，它们共享一个公共的ID，即`group ID`。组内的所有消费者协调在一起来消费订阅主题`(subscribed topics)`的所有分区(`partition`)。当然，每个分区只能由同一个消费组内的一个`consumer`来消费。

消费者在消费的过程中需要记录自己消费了多少数据，即消费位置信息。在Kafka中这个位置信息有个专门的术语：位移(offset)。很多消息引擎都把这部分信息保存在服务器端(broker端)。

这样做的好处当然是实现简单，但会有三个主要的问题：1. broker从此变成有状态的，会影响伸缩性；2. 需要引入应答机制(acknowledgement)来确认消费成功。3. 由于要保存很多consumer的offset信息，必然引入复杂的数据结构，造成资源浪费。而Kafka选择了不同的方式：每个consumer group保存自己的位移信息，那么只需要简单的一个整数表示位置就够了；同时可以引入checkpoint机制定期持久化，简化了应答机制的实现。

## 1. 创建 topic

```bash
# 创建单测试分区
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 1 --topic fang
# 创建双测试分区
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 2 --topic fangfang
```

## 2.测试单分区场景

### 2.1 启动同一个消费者组两个消费者

```bash
# fangGroup消费者组消费者1
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fang --group fangGroup
# fangGroup消费者组消费者2
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fang --group fangGroup
```

消费者的数量`2`大于分区的数量`1`

### 2.2 启动生产者

```bash
kafka-console-producer.sh --broker-list 192.168.137.128:9092 --topic fang
>fang01
>fang02
>fang03
```

```bash
# fangGroup消费者组消费者1
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic f
fang01
fang02
fang03
# fangGroup消费者组消费者2
➜  fang-0 kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fang --group fangGroup
```

> 同一个分区内的消息只能被同一个组中的一个消费者消费，当消费者数量多于分区数量时，多于的消费者空闲（不能消费数据）

## 3. 测试两个分区同一个消费者组

### 3.1 启动同一个消费者组两个消费者

```bash
# fangGroup消费者组消费者1
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
# fangGroup消费者组消费者2
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
```

消费者的数量`2`大于分区的数量`1`

### 3.2 启动生产者

```bash
# 查询topic信息
kafka-topics.sh --describe --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang
# 启动生产者
kafka-console-producer.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang
>fangfang01
>fangfang02
>fangfang03
>fangfang04
>fangfang05
```

```bash
# fangGroup消费者组消费者1
➜ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
fangfang01
fangfang03
fangfang05
# fangGroup消费者组消费者2
➜ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
fangfang02
fangfang04
```

## 4. 测试两个分区不同消费者组

### 4.1 查看消费组信息

```bash
# 查看消费组列表
➜  ~ kafka-consumer-groups.sh  --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094  --list
fangGroup01
fangGroup
# 查看消费组详情
➜  ~ kafka-consumer-groups.sh  --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094  --describe --group fangGroup01

Consumer group 'fangGroup01' has no active members.

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID     HOST            CLIENT-ID
fangGroup01     fangfang        1          5               5               0               -               -               -
fangGroup01     fangfang        0          6               6               0               -               -               -
# 删除消费组
➜  ~ kafka-consumer-groups.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --delete --group fangGroup01
Deletion of requested consumer groups ('fangGroup01') was successful.
```

### 4.2 启动不同消费者组两个消费者

```bash
# fangGroup01消费者组消费者1
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang --group fangGroup01
# fangGroup02消费者组消费者2
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang --group fangGroup02
```

消费者的数量`2`大于分区的数量`1`

### 4.2 启动生产者

```bash
# 查询topic信息
kafka-topics.sh --describe --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang
# 启动生产者
kafka-console-producer.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang
>fangfang01
>fangfang02
>fangfang03
```

```bash
# fangGroup消费者组消费者1
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang --group fangGroup01
fangfang01
fangfang02
fangfang03

# fangGroup消费者组消费者2
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --topic fangfang --group fangGroup02
fangfang01
fangfang02
fangfang03
```

## 参考

- [Kafka消费组(consumer group)](https://www.cnblogs.com/huxi2b/p/6223228.html)