# 时间格式问题

- [Date field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html)

在 es 内部，`date`被转为 `UTC`，并被存储为时间戳，代表从`1970年1月1号0点`到现在的毫秒数

`date`格式可以在 put mapping 的时候用 `format` 参数指定，如果不指定的话，则启用默认格式，是`strict_date_optional_time||epoch_millis`。

```json
"create_at": {
  "type": "date",
  "format": "strict_date_optional_time||epoch_millis"
}
```

## `协调世界时UTC`

`协调世界时`是以原子时秒长为基础，在时刻上尽量接近于世界时的一种时间计量系统。

因此`协调世界时`与`国际原子时`之间会出现若干整数秒的差别，两者之差逐年积累，便采用跳秒（闰秒）的方法使协调时与世界时的时刻相接近，其差不超过 1s。

## CST 中国标准时间

China Standard Time，是中国的标准时间。CST = GMT(UTC) + 8。

**从_source获取存储的文档, 不做任何处理,原样返回**

```java
# 查询
GET my_date/_search
{ 
  "query": {
    "match_all": {}
  }
}
```

## logstash 同步

`2020-08-17T19:00:47.000Z`时间格式为`UTC 时间`,其中`Z`表示的就是`UTC时间`。

时区都设置为`Asia/Shanghai`

```conf
input {
    jdbc {
        jdbc_driver_library => "/home/elasticsearch/logstash-7.8.1/mysql-connector-java-8.0.21.jar"
        # 数据库连接驱动，新版的有cj
        jdbc_driver_class => "com.mysql.cj.jdbc.Driver"
        # 表名需要检查准确,时区只对保存mysql数据有用
        jdbc_connection_string => "jdbc:mysql://192.168.137.129:3306/db_example?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai"
        # 时区设置为上海
        jdbc_default_timezone => "Asia/Shanghai"
    }
}
```

## canal 同步

同步日志中`DEBUG c.a.o.canal.client.adapter.es.core.service.ESSyncService - DML:`中时间为时间戳格式`"create_at":1608173496000`

写入到 ES 的格式为`2020-12-17T09:53:47+08:00`

```java
ZonedDateTime dateTime = ZonedDateTime.now(ZoneId.systemDefault());
log.info("ISO_OFFSET_DATE_TIME:{}",dateTime.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME));
log.info("ISO_ZONED_DATE_TIME:{}",dateTime.format(DateTimeFormatter.ISO_ZONED_DATE_TIME));
log.info("ISO_LOCAL_DATE_TIME:{}",dateTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
// ISO_OFFSET_DATE_TIME:2020-12-17T11:23:35.894+08:00
// ISO_ZONED_DATE_TIME:2020-12-17T11:23:35.894+08:00[Asia/Shanghai]
// ISO_LOCAL_DATE_TIME:2020-12-17T11:23:35.894
ZonedDateTime dateTime = ZonedDateTime.now(ZoneId.of("UTC"));
// ISO_OFFSET_DATE_TIME:2020-12-17T03:31:18.303Z
// ISO_ZONED_DATE_TIME:2020-12-17T03:31:18.303Z[UTC]
// ISO_LOCAL_DATE_TIME:2020-12-17T03:31:18.303

// 将ISO和TUC格式转换为java8 ZonedDateTime
ZonedDateTime zonedDateTime = ZonedDateTime.parse(isoStr, DateTimeFormatter.ISO_OFFSET_DATE_TIME);
zonedDateTime.toInstant().atZone(ZoneId.systemDefault());
```

```yml
spring:
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: GMT+8
    default-property-inclusion: non_null
  srcDataSources:
    defaultDS:
      url: jdbc:mysql://mysql.fat.szkunton.com:3307/guldan20?useSSL=false&useLegacyDatetimeCode=false&serverTimezone=UTC
```

## 查询时带上时区

```java
// 检查默认时区是不是,Asia/Shanghai
ZoneId.systemDefault().toString()
// 如果不是需要加上时区
boolQueryBuilder.must(QueryBuilders.rangeQuery("create_at").gte(param.getBeginDate()).timeZone("Asia/Shanghai"));
```
