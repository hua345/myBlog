# 参考

- [http://kafka.apache.org/](http://kafka.apache.org/)
- [http://kafka.apache.org/quickstart](http://kafka.apache.org/quickstart)

## 1. 安装 kafka

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.7.0/kafka_2.12-2.7.0.tgz

tar -xzf kafka_2.12-2.7.0.tgz
mv kafka_2.12-2.7.0 /usr/local/kafka

vi /etc/profile
export KAFKA_HOME=/usr/local/kafka
export PATH=$KAFKA_HOME/bin:$PATH
source /etc/profile
```

## 2. [启动 zookeeper 服务](../zookeeper/搭建单机集群.md)

```bash
#启动服务 - start
zkServer.sh start ~/zookeeper/zoo01.cfg
zkServer.sh start ~/zookeeper/zoo02.cfg
zkServer.sh start ~/zookeeper/zoo03.cfg

# 连接服务器 zkCli -server IP:PORT
zkCli.sh -server 192.168.137.128:2181
```

## 3. 启动 Kafka

```bash
vi $KAFKA_HOME/config/server.properties
```

```conf
############################# Socket Server Settings #############################

# The address the socket server listens on. It will get the value returned from
# java.net.InetAddress.getCanonicalHostName() if not configured.
#   FORMAT:
#     listeners = listener_name://host_name:port
#   EXAMPLE:
#     listeners = PLAINTEXT://your.host.name:9092
#listeners=PLAINTEXT://:9092

# Hostname and port the broker will advertise to producers and consumers. If not set,
# it uses the value for "listeners" if configured.  Otherwise, it will use the value
# returned from java.net.InetAddress.getCanonicalHostName().
#advertised.listeners=PLAINTEXT://your.host.name:9092

listeners=PLAINTEXT://192.168.137.128:9092
advertised.listeners=PLAINTEXT://192.168.137.128:9092

# zookeeper配置
zookeeper.connect=192.168.137.128:2181,192.168.137.128:22181,192.168.137.128:32181
# Timeout in ms for connecting to zookeeper
zookeeper.connection.timeout.ms=20000
```

```bash
kafka-server-start.sh $KAFKA_HOME/config/server.properties

[2019-08-12 00:04:13,933] INFO Kafka version: 2.3.0 (org.apache.kafka.common.utils.AppInfoParser)
[2019-08-12 00:04:13,933] INFO Kafka commitId: fc1aaa116b661c8a (org.apache.kafka.common.utils.AppInfoParser)
[2019-08-12 00:04:13,934] INFO Kafka startTimeMs: 1565539453905 (org.apache.kafka.common.utils.AppInfoParser)
[2019-08-12 00:04:13,943] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
```

## zkCli.sh 查看 kafka

```bash
[zk: 192.168.137.128:2181(CONNECTED) 4] ls /
[admin, brokers, cluster, config, consumers, controller, controller_epoch, isr_change_notification, latest_producer_id_block, log_dir_event_notification]
```

## 4. 创建 topic

Let's create a topic named "test" with a single partition and only one replica

```bash
➜  ~ kafka-topics.sh --create --bootstrap-server 192.168.137.128:9092 --replication-factor 1 --partitions 1 --topic test
```

可以通过命令行查看有哪些`topic`

```bash
➜  ~ kafka-topics.sh --list --bootstrap-server 192.168.137.128:9092
test
```

## 5. 发送消息

```bash
➜  ~ kafka-console-producer.sh --broker-list 192.168.137.128:9092 --topic test
>hello world
>fang love you
```

## 6. 启动简单的消费者

```bash
➜  ~ kafka-console-consumer.sh --bootstrap-server 192.168.137.128:9092 --topic test --from-beginning
hello world
fang love you
```
