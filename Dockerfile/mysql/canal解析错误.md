# cannal解析日志错误

```log
Caused by: com.alibaba.otter.canal.parse.exception.CanalParseException: com.alibaba.otter.canal.parse.exception.CanalParseException: parse row data failed.
Caused by: com.alibaba.otter.canal.parse.exception.CanalParseException: parse row data failed.
Caused by: com.alibaba.otter.canal.parse.exception.CanalParseException: column size is not match for table:db_example.book,8 vs 3
```

## 原因 

数据表的表结构发生了变化引起的，导致不在读取binlog日志

## 解决方法

新建数据库 `canal_tsdb`

```sql
mysql> create database canal_tsdb;
Query OK, 1 row affected (0.01 sec)

mysql> select * from mysql.user where user='canal' and host='%' \G;
*************************** 1. row ***************************
                    Host: %
                    User: canal
             Select_priv: Y
             Insert_priv: Y
             Update_priv: N
             Delete_priv: N
             Create_priv: N
mysql> show grants for 'canal'@'%';
+-----------------------------------------------------------------------------------+
| Grants for canal@%                                                                |
+-----------------------------------------------------------------------------------+
| GRANT SELECT, INSERT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO `canal`@`%` |
| GRANT ALL PRIVILEGES ON `canal_manager`.* TO `canal`@`%` WITH GRANT OPTION        |
| GRANT ALL PRIVILEGES ON `canal_tsdb`.* TO `canal`@`%` WITH GRANT OPTION           |
+-----------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

## `/usr/local/canal_deployer/conf/canal.properties`

```conf
# table meta tsdb info
canal.instance.tsdb.enable = true
canal.instance.tsdb.dir = ${canal.file.data.dir:../conf}/${canal.instance.destination:}
#canal.instance.tsdb.url = jdbc:h2:${canal.instance.tsdb.dir}/h2;CACHE_SIZE=1000;MODE=MYSQL;
canal.instance.tsdb.url = jdbc:mysql://192.168.137.129:3306/canal_tsdb
canal.instance.tsdb.dbUsername = canal
canal.instance.tsdb.dbPassword = Aa123456.
# dump snapshot interval, default 24 hour
canal.instance.tsdb.snapshot.interval = 24
# purge snapshot expire , default 360 hour(15 days)
canal.instance.tsdb.snapshot.expire = 360

# aliyun ak/sk , support rds/mq
canal.aliyun.accessKey =
canal.aliyun.secretKey =

#################################################
#########               destinations            #############
#################################################
canal.destinations = example
# conf root dir
canal.conf.dir = ../conf
# auto scan instance dir add/remove and start/stop instance
canal.auto.scan = true
canal.auto.scan.interval = 5

#canal.instance.tsdb.spring.xml = classpath:spring/tsdb/h2-tsdb.xml
canal.instance.tsdb.spring.xml = classpath:spring/tsdb/mysql-tsdb.xml
```
