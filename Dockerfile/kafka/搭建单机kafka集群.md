# 修改配置

```bash
➜  kafka cp $KAFKA_HOME/config/server.properties ~/kafka/server01.properties
➜  kafka cp $KAFKA_HOME/config/server.properties ~/kafka/server02.properties
➜  kafka cp $KAFKA_HOME/config/server.properties ~/kafka/server03.properties
```

## server01.properties

```properties
broker.id=0
listeners=PLAINTEXT://192.168.137.128:9092
advertised.listeners=PLAINTEXT://192.168.137.128:9092
log.dirs=~/kafka/data01
```

## server02.properties

```properties
broker.id=1
listeners=PLAINTEXT://192.168.137.128:9093
advertised.listeners=PLAINTEXT://192.168.137.128:9093
log.dirs=~/kafka/data02
```

## server03.properties

```properties
broker.id=1
listeners=PLAINTEXT://192.168.137.128:9094
advertised.listeners=PLAINTEXT://192.168.137.128:9094
log.dirs=~/kafka/data03
```

## 2. 启动集群

```bash
kafka-server-start.sh ~/kafka/server01.properties
kafka-server-start.sh ~/kafka/server02.properties
kafka-server-start.sh ~/kafka/server03.properties
```

```bash
nohup kafka-server-start.sh ~/kafka/server01.properties > ~/kafka/data01/kafka.log 2>&1 &
nohup kafka-server-start.sh ~/kafka/server02.properties > ~/kafka/data02/kafka.log 2>&1 &
nohup kafka-server-start.sh ~/kafka/server03.properties > ~/kafka/data03/kafka.log 2>&1 &
```
