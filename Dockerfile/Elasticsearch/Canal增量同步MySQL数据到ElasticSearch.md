# Canal增量同步MySQL数据到ElasticSearch

## 参考

- [Canal——增量同步MySQL数据到ElasticSearch](https://www.cnblogs.com/caoweixiong/p/11825303.html)

## mysql配置

需要先开启MySQL的 `binlog` 写入功能，配置 `binlog-format` 为 `ROW` 模式

命令检查一下`binlog`是否正确启动

```sql
mysql> show variables like 'log_bin%';
+---------------------------------+-----------------------------+
| Variable_name                   | Value                       |
+---------------------------------+-----------------------------+
| log_bin                         | ON                          |
| log_bin_basename                | /var/lib/mysql/binlog       |
| log_bin_index                   | /var/lib/mysql/binlog.index |
| log_bin_trust_function_creators | OFF                         |
| log_bin_use_v1_row_events       | OFF                         |
+---------------------------------+-----------------------------+
5 rows in set (0.00 sec)
mysql> show variables like 'binlog_format%';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | ROW   |
+---------------+-------+
1 row in set (0.00 sec)
```

授权 `canal` MySQL 账号具有作为`MySQL slave` 的权限, 如果已有账户可直接 grant

```sql
CREATE USER canal IDENTIFIED BY 'Aa123456.';
-- MySQL 8.0 使用了新的登录验证方式 caching_sha2_password 代替旧的 mysql_native_password
-- Caused by: java.io.IOException: caching_sha2_password Auth failed
ALTER USER 'canal'@'%' IDENTIFIED WITH mysql_native_password BY 'Aa123456.';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
FLUSH PRIVILEGES;
```

## [CentOS安装canal](../mysql/CentOS安装canal.md)

## 查看mysql进程

```sql
mysql> show processlist;
+----+-----------------+-----------------------+------------+-------------+-------+---------------------------------------------------------------+------------------+
| Id | User            | Host                  | db         | Command     | Time  | State                                                         | Info             |
+----+-----------------+-----------------------+------------+-------------+-------+---------------------------------------------------------------+------------------+
|  5 | event_scheduler | localhost             | NULL       | Daemon      | 13628 | Waiting on empty queue                                        | NULL             |
|  9 | canal           | fangfang01:50850      | NULL       | Sleep       |  1067 |                                                               | NULL             |
| 15 | canal           | fangfang01:50862      | NULL       | Binlog Dump |  1067 | Master has sent all binlog to slave; waiting for more updates | NULL             |
| 16 | canal           | fangfang01:50864      | db_example | Sleep       |   810 |                                                               | NULL             |
| 17 | root            | 192.168.137.133:34507 | db_example | Sleep       |   111 |                                                               | NULL             |
| 18 | root            | 192.168.137.133:34669 | db_example | Sleep       |    49 |                                                               | NULL             |
| 19 | root            | localhost             | NULL       | Query       |     0 | starting                                                      | show processlist |
+----+-----------------+-----------------------+------------+-------------+-------+---------------------------------------------------------------+------------------+
7 rows in set (0.00 sec)
```

## 写入数据

```yml
insert into book (bookName) values ('简爱');

# 查看canal-deployer服务端日志
tail -f /usr/local/canal_deployer/logs/example/meta.log

2020-08-13 20:10:53.661 - clientId:1001 cursor:[binlog.000023,2359,1597320652000,1,] address[fangfang01/192.168.137.129:3306]

# 查看canal-apadter客户端日志
tail -f /usr/local/canal_adapter/logs/adapter/adapter.log

2020-08-14 17:23:36.735 [pool-3-thread-1] ERROR c.a.otter.canal.client.adapter.es.service.ESSyncService - sync error, es index: book_index, DML : Dml{destination='example', database='db_example', table='book', type='INSERT', es=1597397016000, ts=1597397016733, sql='', data=[{bookId=3, bookName=非暴力沟通, bookDate=2020-08-13 19:27:09.0}], old=null}
2020-08-14 17:23:36.736 [pool-3-thread-1] ERROR c.a.o.canal.adapter.launcher.loader.CanalAdapterWorker - java.lang.IllegalArgumentException: Not found the mapping info of index: book_index
java.lang.RuntimeException: java.lang.IllegalArgumentException: Not found the mapping info of index: book_index
Caused by: java.lang.IllegalArgumentException: Not found the mapping info of index: book_index
        at com.alibaba.otter.canal.client.adapter.es.support.ESTemplate.getEsType(ESTemplate.java:497)
        at com.alibaba.otter.canal.client.adapter.es.support.ESTemplate.getValFromData(ESTemplate.java:345)
        at com.alibaba.otter.canal.client.adapter.es.support.ESTemplate.getESDataFromDmlData(ESTemplate.java:376)
        at com.alibaba.otter.canal.client.adapter.es.service.ESSyncService.singleTableSimpleFiledInsert(ESSyncService.java:433)
        at com.alibaba.otter.canal.client.adapter.es.service.ESSyncService.insert(ESSyncService.java:133)
        at com.alibaba.otter.canal.client.adapter.es.service.ESSyncService.sync(ESSyncService.java:93)
        ... 11 common frames omitted
2020-08-14 17:51:28.266 [Thread-4] ERROR c.a.o.canal.adapter.launcher.loader.CanalAdapterWorker - Outer adapter sync failed!  Error sync but ACK!

#canal适配器会通过GET `http://192.168.137.129:9200/book_index2/_mapping`的方式读取`es mapping`，如果创建索引的时候没有配置mappings信息，会报`Not found the mapping info of index`异常；

2020-08-14 17:49:18.185 [main] ERROR c.a.o.canal.adapter.launcher.loader.CanalAdapterLoader - Load canal adapter: es failed
java.lang.RuntimeException: java.lang.IllegalArgumentException: unknown setting [mode] please check that any required plugins are installed, or check the breaking changes documentation for removed settings
        at com.alibaba.otter.canal.client.adapter.es.ESAdapter.init(ESAdapter.java:137)
# mode: transport # transport # or rest //注释了这行，是1.1.4的坑

2020-08-14 18:47:50.457 [pool-2-thread-1] ERROR c.a.o.canal.adapter.launcher.loader.CanalAdapterWorker - NoNodeAvailableException[None of the configured nodes are available: [{#transport#-1}{A6sMjo3fTRCFzl8ae8_3kA}{192.168.137.129}{192.168.137.129:9300}]]
java.lang.RuntimeException: NoNodeAvailableException[None of the configured nodes are available: [{#transport#-1}{A6sMjo3fTRCFzl8ae8_3kA}{192.168.137.129}{192.168.137.129:9300}]]
# 打开es日志
[2020-08-14T18:52:59,290][WARN ][o.e.t.TcpTransport       ] [node01] exception caught on transport layer [Netty4TcpChannel{localAddress=/192.168.137.129:9300, remoteAddress=/192.168.137.129:58802}], closing connection
java.lang.IllegalStateException: Received message from unsupported version: [6.4.3] minimal compatible version is: [6.8.0]
        at org.elasticsearch.transport.InboundDecoder.ensureVersionCompatibility(InboundDecoder.java:210) ~[elasticsearch-7.8.1.jar:7.8.1]
# 手动编译canal或者canal升级到1.1.5

2020-08-14 17:41:03.978 [pool-5-thread-1] INFO  c.a.o.canal.client.adapter.logger.LoggerAdapterExample - DML: {"data":[{"bookId":4,"bookName":"爱的艺术","bookDate":1597319169000}],"database":"db_example","destination":"example","es":1597398063000,"groupId":null,"isDdl":false,"old":null,"pkNames":["bookId"],"sql":"","table":"book","ts":1597398063978,"type":"INSERT"}
2020-08-14 17:41:21.016 [pool-5-thread-1] INFO  c.a.o.canal.client.adapter.logger.LoggerAdapterExample - DML: {"data":[{"bookId":5,"bookName":"围城","bookDate":1597319457000}],"database":"db_example","destination":"example","es":1597398080000,"groupId":null,"isDdl":false,"old":null,"pkNames":["bookId"],"sql":"","table":"book","ts":1597398081016,"type":"INSERT"}
2020-08-14 17:43:36.026 [pool-5-thread-1] INFO  c.a.o.canal.client.adapter.logger.LoggerAdapterExample - DML: {"data":[{"bookId":6,"bookName":"学习之道","bookDate":1597320232000}],"database":"db_example","destination":"example","es":1597398215000,"groupId":null,"isDdl":false,"old":null,"pkNames":["bookId"],"sql":"","table":"book","ts":1597398216025,"type":"INSERT"}
```
