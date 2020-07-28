# 搭建单机 kafka 集群

## 1. 修改配置

```bash
mkdir /var/kafka
mkdir /var/kafka/data01
mkdir /var/kafka/data02
mkdir /var/kafka/data03

mkdir /etc/kafka/
cp $KAFKA_HOME/config/server.properties /etc/kafka/server01.properties
cp $KAFKA_HOME/config/server.properties /etc/kafka/server02.properties
cp $KAFKA_HOME/config/server.properties /etc/kafka/server03.properties
```

### server01.properties

```properties
broker.id=0
listeners=PLAINTEXT://192.168.137.128:9092
advertised.listeners=PLAINTEXT://192.168.137.128:9092
log.dirs=/var/kafka/data01
```

### server02.properties

```properties
broker.id=1
listeners=PLAINTEXT://192.168.137.128:9093
advertised.listeners=PLAINTEXT://192.168.137.128:9093
log.dirs=/var/kafka/data02
```

### server03.properties

```properties
broker.id=2
listeners=PLAINTEXT://192.168.137.128:9094
advertised.listeners=PLAINTEXT://192.168.137.128:9094
log.dirs=/var/kafka/data03
```

## 2. 加入`systemctl`服务

```bash
vi /lib/systemd/system/kafka01.service
```

```conf
[Unit]
Description=Kafka Service 01
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
Group=root
ExecStart=/usr/local/kafka/bin/kafka-server-start.sh /etc/kafka/server01.properties
ExecStop=/usr/local/kafka/bin/kafka-server-stop.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable kafka01
systemctl start kafka01
```

## 5. 检查是否启动成功

```bash
➜  netstat -nltup
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp6       0      0 192.168.137.128:9092    :::*                    LISTEN      6075/java

#添加端口访问权限
firewall-cmd --zone=public --add-port=9092/tcp --permanent
firewall-cmd --zone=public --add-port=9093/tcp --permanent
firewall-cmd --zone=public --add-port=9094/tcp --permanent

firewall-cmd --reload
# 查看开放的端口
firewall-cmd --zone=public --list-ports
```

### 手动启动集群

```bash
kafka-server-start.sh /etc/kafka/server01.properties
kafka-server-start.sh /etc/kafka/server02.properties
kafka-server-start.sh /etc/kafka/server03.properties
```

```bash
nohup kafka-server-start.sh ~/kafka/server01.properties > ~/kafka/data01/kafka.log 2>&1 &
nohup kafka-server-start.sh ~/kafka/server02.properties > ~/kafka/data02/kafka.log 2>&1 &
nohup kafka-server-start.sh ~/kafka/server03.properties > ~/kafka/data03/kafka.log 2>&1 &
```
