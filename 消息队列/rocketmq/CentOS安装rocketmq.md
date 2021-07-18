# rocketmq部署

- [https://github.com/apache/rocketmq.git](https://github.com/apache/rocketmq.git)
- [《RocketMQ 分布式消息中间件：核心原理与最佳实践》随书实战](https://start.aliyun.com/course?spm=a2ck6.17690074.0.0.53c52e7dSi19ML&id=eAz6VTK5)
- [https://rocketmq.apache.org/docs/quick-start/](https://rocketmq.apache.org/docs/quick-start/)
- [http://rocketmq.apache.org/dowloading/releases/](http://rocketmq.apache.org/dowloading/releases/)

## 源码编译

```bash
git clone https://github.com/apache/rocketmq.git --depth=1
mvn -Prelease-all -DskipTests clean install -U
```

## 启动Name Server

```bash
sh bin/mqnamesrv
# The Name Server boot success. serializeType=JSON
```

## 启动Broker
```bash
sh bin/mqbroker -n localhost:9876
# The broker[chenjianhuadeMacBook-Pro.local, 192.168.1.101:10911] boot success. serializeType=JSON and name server is localhost:9876
# 修改runbroker.sh参数
JAVA_OPT="${JAVA_OPT} -server -Xms8g -Xmx8g -Xmn4g"
# 修改内存参数
JAVA_OPT="${JAVA_OPT} -server -Xms128m -Xmx128m -Xmn128m"
```

## 关闭服务

```bash
> sh bin/mqshutdown broker
The mqbroker(36695) is running...
Send shutdown request to mqbroker(36695) OK

> sh bin/mqshutdown namesrv
The mqnamesrv(36664) is running...
Send shutdown request to mqnamesrv(36664) OK
```
