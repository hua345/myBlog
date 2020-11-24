# canal同步mysql数据

## 参考[CentOS安装canal](./CentOS安装canal.md)

## 创建同步后的表

```sql
-- auto-generated definition
create table book_2020
(
    id          bigint                               not null
        primary key,
    book_name   varchar(20)                          not null,
    version     int        default 0                 null,
    creator     varchar(32)                          null comment '创建人',
    create_time timestamp  default CURRENT_TIMESTAMP not null comment '创建时间',
    updator     varchar(32)                          null comment '更新人',
    update_time timestamp                            null comment '更新时间',
    deleted     tinyint(1) default 0                 null
);
```

## 修改canal_deployer的example配置

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

### 编辑`application.yml`

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
      - name: rdb
        key: mysqltest
        properties:
          jdbc.driverClassName: com.mysql.jdbc.Driver
          jdbc.url: jdbc:mysql://192.168.137.129:3306/db_example?useUnicode=true
          jdbc.username: root
          jdbc.password: 123456
```

### 编辑``

```yml
dataSourceKey: defaultDS        # 源数据源的key, 对应上面配置的srcDataSources中的值
destination: example            # cannal的instance或者MQ的topic
groupId: g1                     # 对应MQ模式下的groupId, 只会同步对应groupId的数据
outerAdapterKey: mysqltest      # adapter key, 对应上面配置outAdapters中的key
concurrent: true                # 是否按主键hash并行同步, 并行同步的表必须保证主键不会更改及主键不能为其他同步表的外键!!
dbMapping:
  database: db_example          # 源数据源的database/shcema
  table: book                   # 源数据源表名
  targetTable: db_example.book_2020   # 目标数据源的库名.表名
  targetPk:                     # 主键映射
    id: id                      # 如果是复合主键可以换行映射多个
  #  mapAll: true                 # 是否整表映射, 要求源表和目标表字段名一模一样 (如果targetColumns也配置了映射,则以targetColumns配置为准)
  targetColumns:                # 字段映射, 格式: 目标表字段: 源表字段, 如果字段名一样源表字段名可不填
    id:
    old_id: id
    book_name:
    version:
    creator:
    create_time:
    updator:
    update_time:
    deleted:
```

```log
2020-11-24 18:24:58.499 [pool-7-thread-1] INFO  c.a.o.canal.client.adapter.logger.LoggerAdapterExample - DML: {"data":[{"id":1010,"book_name":"刻意练习","version":0,"creator":null,"create_time":1605755850000,"updator":null,"update_time":1605755850000,"deleted":0}],"database":"db_example","destination":"example","es":1606213497000,"groupId":"g1","isDdl":false,"old":null,"pkNames":["id"],"sql":"","table":"book","ts":1606213498387,"type":"INSERT"}
2020-11-24 18:24:58.518 [pool-3-thread-1] DEBUG c.a.o.canal.client.adapter.rdb.service.RdbSyncService - DML: {"data":{"id":1010,"book_name":"刻意练习","version":0,"creator":null,"create_time":1605755850000,"updator":null,"update_time":1605755850000,"deleted":0},"database":"db_example","destination":"example","old":null,"table":"book","type":"INSERT"}
2020-11-24 18:24:59.029 [pool-7-thread-1] INFO  c.a.o.canal.client.adapter.logger.LoggerAdapterExample - DML: {"data":[{"id":1010,"old_id":1010,"book_name":"刻意练习","version":0,"creator":null,"create_time":1605755850000,"updator":null,"update_time":1605755850000,"deleted":0}],"database":"db_example","destination":"example","es":1606213498000,"groupId":"g1","isDdl":false,"old":null,"pkNames":["id"],"sql":"","table":"book_2020","ts":1606213499028,"type":"INSERT"}
```
