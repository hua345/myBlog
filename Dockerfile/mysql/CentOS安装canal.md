# 简介

- [https://github.com/alibaba/canal](https://github.com/alibaba/canal)

![canal](./img/canal.png)

**canal [kə'næl]**，译意为水道/管道/沟渠，主要用途是基于 MySQL 数据库增量日志解析，提供增量数据订阅和消费

早期阿里巴巴因为杭州和美国双机房部署，存在跨机房同步的业务需求，实现方式主要是基于业务 trigger 获取增量变更。从 2010 年开始，业务逐步尝试数据库日志解析获取增量变更进行同步，由此衍生出了大量的数据库增量订阅和消费业务。

基于日志增量订阅和消费的业务包括

- 数据库镜像
- 数据库实时备份
- 索引构建和实时维护(拆分异构索引、倒排索引等)
- 业务 cache 刷新
- 带业务逻辑的增量数据处理

## 工作原理

### MySQL 主备复制原理

- MySQL master 将数据变更写入二进制日志( binary log, 其中记录叫做二进制日志事件 binary log events，可以通过 show binlog events 进行查看)
- MySQL slave 将 master 的 binary log events 拷贝到它的中继日志(relay log)
- MySQL slave 重放 relay log 中事件，将数据变更反映它自己的数据

### canal 工作原理

- canal 模拟 MySQL slave 的交互协议，伪装自己为 MySQL slave ，向 MySQL master 发送 dump 协议
- MySQL master 收到 dump 请求，开始推送 binary log 给 slave (即 canal )
- canal 解析 binary log 对象(原始为 byte 流)

Canal 为 C/S 架构，分为 Server 端和 Client 端

- Server 的包名为`canal-deployer`，server 端部署好以后，可以直接监听`mysql binlog`,因为 server 端是把自己模拟成了`mysql slave`，所以，只能接受数据，没有进行任何逻辑的处理，具体的逻辑处理，需要 client 端进行处理。
- Client 的包名为`canal-adapter`,client 可以自动开发或者使用官方提供的`canal-adapter`,Adapter 是可以将`canal server`端获取的数据转换成几个常用的中间件数据源，现在支持`kafka、rocketmq、hbase、elasticsearch`，针对这几个中间件的支持，直接配置即可，无需开发

### 环境信息

| 软件           | IP              | 端口        | 版本号 |
| -------------- | --------------- | ----------- | ------ |
| Mysql          | 192.168.137.129 | 3306        | 8.0.21 |
| elasticsearch  | 192.168.137.129 | 9200/9300   | 7.8.1  |
| canal.deployer | 192.168.137.129 | 11111/11112 | 1.1.4  |
| canal.adapter  | 192.168.137.129 | 8081        | 1.1.4  |

## 安装

```bash
wget https://github.com/alibaba/canal/releases/download/canal-1.1.5-alpha-1/canal.deployer-1.1.5-SNAPSHOT.tar.gz
wget https://github.com/alibaba/canal/releases/download/canal-1.1.5-alpha-1/canal.adapter-1.1.5-SNAPSHOT.tar.gz
wget https://github.com/alibaba/canal/releases/download/canal-1.1.5-alpha-1/canal.admin-1.1.5-SNAPSHOT.tar.gz

mkdir /usr/local/canal_deployer
mkdir /usr/local/canal_adapter
mkdir /usr/local/canal_admin
tar zxvf canal.deployer-1.1.5-SNAPSHOT.tar.gz  -C /usr/local/canal_deployer
tar zxvf canal.adapter-1.1.5-SNAPSHOT.tar.gz  -C /usr/local/canal_adapter
tar zxvf canal.admin-1.1.5-SNAPSHOT.tar.gz  -C /usr/local/canal_admin
```

## `canal deployer`配置

`vi /usr/local/canal_deployer/conf/canal.properties`

```conf
#################################################
#########               common argument         #############
#################################################
# tcp bind ip
canal.ip =192.168.137.129
# register ip to zookeeper
canal.register.ip =192.168.137.129
canal.port = 11111
canal.metrics.pull.port = 11112
# canal instance user/passwd
# canal.user = canal
# canal.passwd = E3619321C1A937C46A0D8BD1DAC39F93B27D4458

# canal admin config
#canal.admin.manager = 127.0.0.1:8089
canal.admin.port = 11110
canal.admin.user = admin
canal.admin.passwd = 4ACFE3202A5FF5CF467898FC58AAB1D615029441

#################################################
#########               destinations            #############
#################################################
canal.destinations = example
# conf root dir
canal.conf.dir = ../conf
# auto scan instance dir add/remove and start/stop instance
canal.auto.scan = true
canal.auto.scan.interval = 5
```

`vi /usr/local/canal_deployer/conf/example/instance.properties`

```conf
#################################################
## mysql serverId , v1.0.26+ will autoGen
# canal.instance.mysql.slaveId=0

# enable gtid use true/false
canal.instance.gtidon=false

# position info
canal.instance.master.address=192.168.137.129:3306
canal.instance.master.journal.name=
canal.instance.master.position=
canal.instance.master.timestamp=
canal.instance.master.gtid=

# rds oss binlog
canal.instance.rds.accesskey=
canal.instance.rds.secretkey=
canal.instance.rds.instanceId=

# table meta tsdb info
canal.instance.tsdb.enable=true
#canal.instance.tsdb.url=jdbc:mysql://127.0.0.1:3306/canal_tsdb
#canal.instance.tsdb.dbUsername=canal
#canal.instance.tsdb.dbPassword=canal

#canal.instance.standby.address =
#canal.instance.standby.journal.name =
#canal.instance.standby.position =
#canal.instance.standby.timestamp =
#canal.instance.standby.gtid=

# username/password
canal.instance.dbUsername=canal
canal.instance.dbPassword=Aa123456.
canal.instance.connectionCharset = UTF-8
# enable druid Decrypt database password
canal.instance.enableDruid=false
#canal.instance.pwdPublicKey=MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALK4BUxdDltRRE5/zXpVEVPUgunvscYFtEip3pmLlhrWpacX7y7GCMo2/JM6LeHmiiNdH1FWgGCpUfircSwlWKUCAwEAAQ==

# table regex
canal.instance.filter.regex=.*\\..*
# table black regex
canal.instance.filter.black.regex=
# table field filter(format: schema1.tableName1:field1/field2,schema2.tableName2:field1/field2)
#canal.instance.filter.field=test1.t_product:id/subject/keywords,test2.t_company:id/name/contact/ch
# table field black filter(format: schema1.tableName1:field1/field2,schema2.tableName2:field1/field2)
#canal.instance.filter.black.field=test1.t_product:subject/product_image,test2.t_company:id/name/contact/ch

# mq config
canal.mq.topic=example
# dynamic topic route by schema or table regex
#canal.mq.dynamicTopic=mytest1.user,mytest2\\..*,.*\\..*
canal.mq.partition=0
# hash partition config
#canal.mq.partitionsNum=3
#canal.mq.partitionHash=test.table:id^name,.*\\..*
#################################################
```

### 启动

```bash
/usr/local/canal_deployer/bin/startup.sh
```

查看 server 日志

```log
tail -f /usr/local/canal_deployer/logs/canal/canal.log
2020-08-13 12:08:17.786 [main] INFO  com.alibaba.otter.canal.deployer.CanalLauncher - ## set default uncaught exception handler
2020-08-13 12:08:17.812 [main] INFO  com.alibaba.otter.canal.deployer.CanalLauncher - ## load canal configurations
2020-08-13 12:08:17.831 [main] INFO  com.alibaba.otter.canal.deployer.CanalStarter - ## start the canal server.
2020-08-13 12:08:17.860 [main] INFO  com.alibaba.otter.canal.deployer.CanalController - ## start the canal server[172.17.0.1(172.17.0.1):11111]
2020-08-13 12:08:18.932 [main] INFO  com.alibaba.otter.canal.deployer.CanalStarter - ## the canal server is running now ......
```

查看 instance 的日志

```log
tail -f /usr/local/canal_deployer/logs/example/example.log
2020-08-13 12:18:35.087 [main] INFO  c.a.o.c.i.spring.support.PropertyPlaceholderConfigurer - Loading properties file from class path resource [canal.properties]
2020-08-13 12:18:35.087 [main] INFO  c.a.o.c.i.spring.support.PropertyPlaceholderConfigurer - Loading properties file from class path resource [example/instance.properties]
2020-08-13 12:18:35.412 [main] INFO  c.a.otter.canal.instance.spring.CanalInstanceWithSpring - start CannalInstance for 1-example
2020-08-13 12:18:35.418 [main] WARN  c.a.o.canal.parse.inbound.mysql.dbsync.LogEventConvert - --> init table filter : ^.db_example\..*$
2020-08-13 12:18:35.418 [main] WARN  c.a.o.canal.parse.inbound.mysql.dbsync.LogEventConvert - --> init table black filter :
2020-08-13 12:18:35.424 [main] INFO  c.a.otter.canal.instance.core.AbstractCanalInstance - start successful....
2020-08-13 12:18:35.573 [destination = example , address = /192.168.137.129:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - ---> begin to find start position, it will be long time for reset or first position
2020-08-13 12:18:35.573 [destination = example , address = /192.168.137.129:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - prepare to find start position just show master status
2020-08-13 12:18:35.830 [destination = example , address = /192.168.137.129:3306 , EventParser] WARN  c.a.o.c.p.inbound.mysql.rds.RdsBinlogEventParserProxy - ---> find start position successfully, EntryPosition[included=false,journalName=binlog.000022,position=4,serverId=1,gtid=<null>,timestamp=1597231219000] cost : 249ms , the next step is binlog dump
2020-08-13 12:18:35.920 [MultiStageCoprocessor-other-example-0] WARN  c.a.o.canal.parse.inbound.mysql.tsdb.DatabaseTableMeta - dup apply for sql : ALTER USER 'root'@'%' IDENTIFIED WITH 'caching_sha2_password' AS '$A$005$C.c\"wGU}bFClSvR!i.#vUuD6YszPwUv6PhkbPwaYN0LjhTap4o2fI1jzb1Dj3lA'
2020-08-13 12:18:35.922 [MultiStageCoprocessor-other-example-0] WARN  c.a.o.canal.parse.inbound.mysql.tsdb.DatabaseTableMeta - dup apply for sql : ALTER USER 'canal'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*9C36E4A592665FDA293CFFB78A65B2C321AF5484'
```

关闭

```bash
bin/stop.sh
```

## `canal adapter`配置

```bash
vi /usr/local/canal_adapter/conf/application.yml
```

```yml
server:
  port: 8081
spring:
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: GMT+8
    default-property-inclusion: non_null

canal.conf:
  mode: tcp #tcp kafka rocketMQ rabbitMQ
  flatMessage: true
  #zookeeperHosts:
  syncBatchSize: 1000
  retries: 0
  timeout:
  accessKey:
  secretKey:
  consumerProperties:
    # canal tcp consumer
    canal.tcp.server.host: 192.168.137.129:11111
    #canal.tcp.zookeeper.hosts:
    canal.tcp.batch.size: 500
    canal.tcp.username:
    canal.tcp.password:
#    # kafka consumer
#    kafka.bootstrap.servers: 127.0.0.1:9092
#    kafka.enable.auto.commit: false
#    kafka.auto.commit.interval.ms: 1000
#    kafka.auto.offset.reset: latest
#    kafka.request.timeout.ms: 40000
#    kafka.session.timeout.ms: 30000
#    kafka.isolation.level: read_committed
#    kafka.max.poll.records: 1000
#    # rocketMQ consumer
#    rocketmq.namespace:
#    rocketmq.namesrv.addr: 127.0.0.1:9876
#    rocketmq.batch.size: 1000
#    rocketmq.enable.message.trace: false
#    rocketmq.customized.trace.topic:
#    rocketmq.access.channel:
#    rocketmq.subscribe.filter:
#    # rabbitMQ consumer
#    rabbitmq.host:
#    rabbitmq.virtual.host:
#    rabbitmq.username:
#    rabbitmq.password:
#    rabbitmq.resource.ownerId:

  srcDataSources:
    defaultDS:
      url: jdbc:mysql://192.168.137.129:3306/db_example?useUnicode=true
      username: canal
      password: Aa123456.
  canalAdapters:
  - instance: example # canal instance Name or mq topic name
    groups:
    - groupId: g1
      outerAdapters:
      - name: logger
#      - name: rdb
#        key: mysql1
#        properties:
#          jdbc.driverClassName: com.mysql.jdbc.Driver
#          jdbc.url: jdbc:mysql://127.0.0.1:3306/mytest2?useUnicode=true
#          jdbc.username: root
#          jdbc.password: 121212
#      - name: rdb
#        key: oracle1
#        properties:
#          jdbc.driverClassName: oracle.jdbc.OracleDriver
#          jdbc.url: jdbc:oracle:thin:@localhost:49161:XE
#          jdbc.username: mytest
#          jdbc.password: m121212
#      - name: rdb
#        key: postgres1
#        properties:
#          jdbc.driverClassName: org.postgresql.Driver
#          jdbc.url: jdbc:postgresql://localhost:5432/postgres
#          jdbc.username: postgres
#          jdbc.password: 121212
#          threads: 1
#          commitSize: 3000
#      - name: hbase
#        properties:
#          hbase.zookeeper.quorum: 127.0.0.1
#          hbase.zookeeper.property.clientPort: 2181
#          zookeeper.znode.parent: /hbase
      - name: es7 #集群版本，支持 es6 与 es7
        hosts: 192.168.137.129:9200 # 127.0.0.1:9200 for rest mode
        properties:
          mode: rest # transport or rest #rest方式通过http API 访问ES(没有语言限制),transport通过TCP方式访问ES在 es8.0将会被移除
          # security.auth: test:123456 #  only used for rest mode
          cluster.name: my-application #指定elasticsearch集群名称
```

### es 配置

```sql
-- auto-generated definition
create table book
(
    bookId   int auto_increment
        primary key,
    bookName varchar(20)                         not null,
    bookDate timestamp default CURRENT_TIMESTAMP null
);
```

```bash
cp conf/es/customer.yml conf/es/book.yml
vi conf/es/book.yml
```

```yml
dataSourceKey: defaultDS
destination: example
groupId: g1
esMapping:
  _index: book_index
  _type: _doc
  _id: _id
  sql: "select bookId as _id, bookName, date_format(bookDate, '%Y-%m-%d %H:%i:%s') bookDate from book
"
  commitBatch: 3000
```

### 添加`mysql 8.0.21`驱动

```java
Caused by: java.lang.NullPointerException: null
        at com.mysql.jdbc.ConnectionImpl.getServerCharset
```

使用`mysql connector 8`版本，问题即解决。所以应该来说是 mysql 驱动版本的问题

```bash
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.21/mysql-connector-java-8.0.21.jar
```

### `canal adapter`启动

```bash
/usr/local/canal_adapter/bin/startup.sh
```

```log
➜  tail -f /usr/local/canal_adapter/logs/adapter/adapter.log
2020-08-17 13:51:47.964 [main] INFO  c.a.o.c.client.adapter.es.core.config.ESSyncConfigLoader - ## Start loading es mapping config ... 
2020-08-17 13:51:48.002 [main] INFO  c.a.o.c.client.adapter.es.core.config.ESSyncConfigLoader - ## ES mapping config loaded
2020-08-17 13:51:48.068 [main] INFO  c.a.o.canal.adapter.launcher.loader.CanalAdapterLoader - Load canal adapter: es7 succeed
2020-08-17 13:51:48.072 [main] INFO  c.alibaba.otter.canal.connector.core.spi.ExtensionLoader - extension classpath dir: F:\Code\canal\client-adapter\launcher\target\canal-adapter\plugin
2020-08-17 13:51:48.085 [main] INFO  c.a.o.canal.adapter.launcher.loader.CanalAdapterLoader - Start adapter for canal-client mq topic: example-g1 succeed
2020-08-17 13:51:48.085 [Thread-28] INFO  c.a.otter.canal.adapter.launcher.loader.AdapterProcessor - =============> Start to connect destination: example <=============
2020-08-17 13:51:48.085 [main] INFO  c.a.o.canal.adapter.launcher.loader.CanalAdapterService - ## the canal client adapters are running now ......
2020-08-17 13:51:48.089 [main] INFO  org.apache.coyote.http11.Http11NioProtocol - Starting ProtocolHandler ["http-nio-8081"]
2020-08-17 13:51:48.090 [main] INFO  org.apache.tomcat.util.net.NioSelectorPool - Using a shared selector for servlet write/read
2020-08-17 13:51:48.106 [main] INFO  o.s.boot.web.embedded.tomcat.TomcatWebServer - Tomcat started on port(s): 8081 (http) with context path ''
2020-08-17 13:51:48.108 [main] INFO  c.a.otter.canal.adapter.launcher.CanalAdapterApplication - Started CanalAdapterApplication in 12.187 seconds (JVM running for 13.106)
2020-08-17 13:51:48.164 [Thread-28] INFO  c.a.otter.canal.adapter.launcher.loader.AdapterProcessor - =============> Subscribe destination: example succeed <=============
2020-08-17 13:52:05.030 [pool-2-thread-1] INFO  c.a.o.canal.client.adapter.logger.LoggerAdapterExample - DML: {"data":[{"bookId":26,"bookName":"算法之美","bookDate":1597643523000}],"database":"db_example","destination":"example","es":1597643523000,"groupId":"g1","isDdl":false,"old":null,"pkNames":["bookId"],"sql":"","table":"book","ts":1597643524949,"type":"INSERT"}
2020-08-17 13:52:05.128 [pool-2-thread-1] DEBUG c.a.o.canal.client.adapter.es.core.service.ESSyncService - DML: {"data":[{"bookId":26,"bookName":"算法之美","bookDate":1597643523000}],"database":"db_example","destination":"example","es":1597643523000,"groupId":"g1","isDdl":false,"old":null,"pkNames":["bookId"],"sql":"","table":"book","ts":1597643524949,"type":"INSERT"} 
Affected indexes: book_index 
```

## Http管理状态

```yml
# 查询所有订阅同步的canal instance
http http://192.168.137.129:8081/destinations
HTTP/1.1 200
Content-Type: application/json;charset=UTF-8
Date: Thu, 13 Aug 2020 13:00:54 GMT
Transfer-Encoding: chunked

[
    {
        "destination": "example",
        "status": "on"
    }
]
```
