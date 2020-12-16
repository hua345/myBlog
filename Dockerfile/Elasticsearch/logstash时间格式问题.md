# logstash 时间格式问题

在 es 内部，`date`被转为 UTC，并被存储为时间戳，代表从`1970年1月1号0点`到现在的毫秒数

`date`格式可以在 put mapping 的时候用 `format` 参数指定，如果不指定的话，则启用默认格式，是`strict_date_optional_time||epoch_millis`。

```json
"create_at": {
"type": "date",
"format": "strict_date_optional_time||epoch_millis"
}
```

```log
{"type"=>"mapper_parsing_exception", "reason"=>"failed to parse field [create_at] of type [date] in document with id '14937'. Preview of field's value: '2020-08-17T19:00:47.000Z'", "caused_by"=>{"type"=>"illegal_argument_exception", "reason"=>"failed to parse date field [2020-08-17T19:00:47.000Z] with format [yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis]", "caused_by"=>{"type"=>"date_time_parse_exception", "reason"=>"Failed to parse with all enclosed parsers"}}}
```

`2020-08-17T19:00:47.000Z`时间格式为`UTC 时间`,其中`Z`表示的就是`UTC时间`。

## `协调世界时UTC`

`协调世界时`是以原子时秒长为基础，在时刻上尽量接近于世界时的一种时间计量系统。

因此`协调世界时`与`国际原子时`之间会出现若干整数秒的差别，两者之差逐年积累，便采用跳秒（闰秒）的方法使协调时与世界时的时刻相接近，其差不超过1s。

## CST中国标准时间

China Standard Time，是中国的标准时间。CST = GMT(UTC) + 8。

## 查询时带上时区

```java
// 检查默认时区是不是,Asia/Shanghai
ZoneId.systemDefault().toString()
// 如果不是需要加上时区
boolQueryBuilder.must(QueryBuilders.rangeQuery("create_at").gte(param.getBeginDate()).timeZone("Asia/Shanghai"));
```
