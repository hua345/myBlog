# 消费者与消费者组

## 1. 创建 topic

```bash
# 创建单测试分区
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 1 --topic fang
# 创建双测试分区
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 3 --partitions 2 --topic fangfang
```

## 2.测试单分区场景

### 2.1启动两个消费者

```bash
# 消费者1
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fang --group fangGroup
# 消费者2
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
# 消费者1
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic f
fang01
fang02
fang03
# 消费者2
➜  fang-0 kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fang --group fangGroup
```

> 同一个分区内的消息只能被同一个组中的一个消费者消费，当消费者数量多于分区数量时，多于的消费者空闲（不能消费数据）

## 3. 测试两个分区

### 3.1启动两个消费者

```bash
# 消费者1
kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
# 消费者2
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
# 消费者1
➜ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
fangfang01
fangfang03
fangfang05
# 消费者2
➜ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9094 --topic fangfang --group fangGroup
fangfang02
fangfang04
```
