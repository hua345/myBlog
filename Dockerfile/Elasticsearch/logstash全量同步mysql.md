# `logstash`

## 1.`logstash`安装

```bash
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.8.1.tar.gz

tar -zvxf logstash-7.8.1.tar.gz
cd logstash-7.8.1
vim config/logstash.yml
```

[`logstashlogstash-7.8`](https://www.elastic.co/cn/downloads/logstash)自带的[`JDBC Integration Plugin`](https://www.elastic.co/guide/en/logstash/7.9/plugins-integrations-jdbc.html)插件已经包含[`plugins-inputs-jdbc`](https://www.elastic.co/guide/en/logstash/7.9/plugins-inputs-jdbc.html)和[`Jdbc_streaming filter plugin`](https://www.elastic.co/guide/en/logstash/7.9/plugins-filters-jdbc_streaming.html)插件

## 2.创建 index

```json
PUT book_index2
{
  "mappings": {
    "properties": {
      "id": {
        "type": "text"
      },
      "bookDate": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      }
    }
  }
}
```

## 3.同步 mysql

### 3.1 全量同步一次`config/book_index.conf`

```conf
input {
    jdbc {
        jdbc_driver_library => "/home/elasticsearch/logstash-7.8.1/mysql-connector-java-8.0.21.jar"
        # 数据库连接驱动，新版的有cj
        jdbc_driver_class => "com.mysql.cj.jdbc.Driver"
        # 表名需要检查准确
        jdbc_connection_string => "jdbc:mysql://192.168.137.129:3306/db_example?useUnicode=true&characterEncoding=utf-8&useSSL=false"
        jdbc_user => "canal"
        jdbc_password => "Aa123456."
        # 每秒都执行"* * * * * *",每分钟"0 * * * * *",每小时"0 0 * * * *"
        # schedule注释表示只执行一次
        # schedule => "* * * * * *"
        statement => "select bookId as id, bookName, bookDate bookDate from book ORDER BY bookId ASC"
    }
}

output {
    elasticsearch {
        # 索引名称
        index => "book_index2"
        # es文档的id为数据库表的id
        document_id => "%{id}"
        hosts => ["http://192.168.137.129:9200"]
    }
}
```

```log
[2020-08-19T14:56:20,465][INFO ][logstash.javapipeline    ][main] Pipeline started {"pipeline.id"=>"main"}
[2020-08-19T14:56:20,527][INFO ][logstash.agent           ] Pipelines running {:count=>1, :running_pipelines=>[:main], :non_running_pipelines=>[]}
[2020-08-19T14:56:20,776][INFO ][logstash.agent           ] Successfully started Logstash API endpoint {:port=>9600}
Loading class `com.mysql.jdbc.Driver'. This is deprecated. The new driver class is `com.mysql.cj.jdbc.Driver'. The driver is automatically registered via the SPI and manual loading of the driver class is generally unnecessary.
[2020-08-19T14:56:21,406][INFO ][logstash.inputs.jdbc     ][main][3954ba12da715b220c13ea1193c504d01cfc83cb67f6923eaf5b49377c8779c0] (0.015541s) select bookId as id, bookName, bookDate bookDate from book ORDER BY bookId ASC
[2020-08-19T14:56:23,155][INFO ][logstash.runner          ] Logstash shut down.
```

```json
{
  "_index": "book_index2",
  "_type": "_doc",
  "_id": "1",
  "_version": 1,
  "_score": 0,
  "_source": {
    "@version": "1",
    "bookdate": "2020-08-14T00:16:48.000Z",
    "@timestamp": "2020-08-19T07:21:03.821Z",
    "bookname": "刻意练习",
    "id": 1
  },
  "fields": {
    "@timestamp": ["2020-08-19T07:21:03.821Z"],
    "bookdate": ["2020-08-14T00:16:48.000Z"]
  }
}
```

### 3.2文档删除

不知道你是否已经发现，如果一个文档从`MySQL`中删除，并不会同步到 `ElasticSearch` 。关于这个问题，列举一些可供我们考虑的方案，如下：

- `MySQL` 中的记录可通过包含 `is_deleted` 字段用以表明该条记录是否有效。一旦发生更新，`is_deleted` 也会同步更新到 `ElasticSearch` 中。如果通过这种方式，在执行 `MySQL` 或 `ElasticSearch` 查询时，我们需要重写查询语句来过滤掉 `is_deleted` 为 `true` 的记录。
- 使用`canal`增量同步,`canal`可以同步被删除的记录

### 3.3[定时任务增量同步`config/book_index.conf`](https://www.elastic.co/guide/en/logstash/7.9/plugins-inputs-jdbc.html#_usage)

```conf
input {
    jdbc {
        jdbc_driver_library => "/home/elasticsearch/logstash-7.8.1/mysql-connector-java-8.0.21.jar"
        # 数据库连接驱动，新版的有cj
        jdbc_driver_class => "com.mysql.cj.jdbc.Driver"
        # 表名需要检查准确
        jdbc_connection_string => "jdbc:mysql://192.168.137.129:3306/db_example?useUnicode=true&characterEncoding=utf-8&useSSL=false"
        jdbc_user => "canal"
        jdbc_password => "Aa123456."
        # 每分钟都执行"* * * * *",每小时"0 * * * *",每天"0 0 * * *"
        # schedule注释表示只执行一次
        schedule => "* * * * *"
        # 时区设置为上海
        jdbc_default_timezone => "Asia/Shanghai"
        statement => "select bookId as id , bookName, bookDate bookDate from book WHERE bookId > :sql_last_value  ORDER BY bookId ASC"
        # 默认为false,如果为true,tracking_column追踪字段会被设置到`:sql_last_value`
        use_column_value => true
        #默认true
        lowercase_column_names => true
        # numeric, timestamp中的一种
        tracking_column_type => "numeric"
        tracking_column => "id"
        #默认为true,保存状态到`last_run_metadata_path`
        record_last_run => "true"
        last_run_metadata_path => "/home/elasticsearch/logstash-7.8.1/config/book_index2_last_id"
    }
}

output {
    elasticsearch {
        # 索引名称
        index => "book_index2"
        # es文档的id为数据库表的id
        document_id => "%{id}"
        hosts => ["http://192.168.137.129:9200"]
    }
}
```

```log
[2020-08-19T16:14:00,703][INFO ][logstash.inputs.jdbc     ][main][d8fbe37a3912f1de07597f10808720fbb15dd8595fd5e2c383c560c580eac9a3] (0.014688s) select bookId as id , bookName, bookDate bookDate from book WHERE bookId > 0  ORDER BY bookId ASC
[2020-08-19T16:15:00,327][INFO ][logstash.inputs.jdbc     ][main][d8fbe37a3912f1de07597f10808720fbb15dd8595fd5e2c383c560c580eac9a3] (0.001118s) select bookId as id , bookName, bookDate bookDate from book WHERE bookId > 28  ORDER BY bookId ASC
[2020-08-19T16:16:00,222][INFO ][logstash.inputs.jdbc     ][main][d8fbe37a3912f1de07597f10808720fbb15dd8595fd5e2c383c560c580eac9a3] (0.000739s) select bookId as id , bookName, bookDate bookDate from book WHERE bookId > 28  ORDER BY bookId ASC
```

### 3.4 定时任务分页增量同步`

```conf
input {
    jdbc {
        ...
        jdbc_page_size => 10000
        # 默认false,是否开启分页查询
        jdbc_paging_enabled => true
        ...
    }
}

output {
    elasticsearch {
        # 索引名称
        index => "book_index2"
        # es文档的id为数据库表的id
        document_id => "%{id}"
        hosts => ["http://192.168.137.129:9200"]
    }
}
```

```log
[2020-08-19T16:37:00,877][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.014472s) SELECT version()
[2020-08-19T16:37:01,420][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.000583s) SELECT version()
[2020-08-19T16:37:01,530][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.000697s) SELECT count(*) AS `count` FROM (select bookId as id , bookName, bookDate bookDate from book WHERE bookId > 0  ORDER BY bookId ASC) AS `t1` LIMIT 1
[2020-08-19T16:37:01,557][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.000963s) SELECT * FROM (select bookId as id , bookName, bookDate bookDate from book WHERE bookId > 0  ORDER BY bookId ASC) AS `t1` LIMIT 10000 OFFSET 0
[2020-08-19T16:38:00,231][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.000486s) SELECT version()
[2020-08-19T16:38:00,236][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.000493s) SELECT version()
[2020-08-19T16:38:00,243][INFO ][logstash.inputs.jdbc     ][main][8323d6bc4c517079e1d0cc6ea70fd5028bad918cf4b1dfc2b29efa13647356b1] (0.001616s) SELECT count(*) AS `count` FROM (select bookId as id , bookName, bookDate bookDate from book WHERE bookId > 28  ORDER BY bookId ASC) AS `t1` LIMIT 1
```

### 3.5 根据时间增量同步

```conf
input {
    jdbc {
        jdbc_driver_library => "/home/elasticsearch/logstash-7.8.1/mysql-connector-java-8.0.21.jar"
        # 数据库连接驱动，新版的有cj
        jdbc_driver_class => "com.mysql.cj.jdbc.Driver"
        # 表名需要检查准确
        jdbc_connection_string => "jdbc:mysql://192.168.137.129:3306/db_example?useUnicode=true&characterEncoding=utf-8&useSSL=false"
        jdbc_user => "canal"
        jdbc_password => "Aa123456."
        # 每分钟都执行"* * * * *",每小时"0 * * * *",每天"0 0 * * *"
        # schedule注释表示只执行一次
        schedule => "* * * * *"
        # 时区设置为上海
        jdbc_default_timezone => "Asia/Shanghai"
        jdbc_page_size => 10000
        # 默认false,是否开启分页查询
        jdbc_paging_enabled => true
        statement => "select bookId as id , bookName, bookDate from book where bookDate > :sql_last_value AND bookDate < NOW() ORDER BY bookDate desc"
        # 默认为false,如果为true,tracking_column追踪字段会被设置到`:sql_last_value`
        use_column_value => true
        #默认true
        lowercase_column_names => true
        # numeric, timestamp中的一种
        tracking_column_type => "timestamp"
        tracking_column => "bookdate"
        #默认为true,保存状态到`last_run_metadata_path`
        record_last_run => "true"
        last_run_metadata_path => "/home/elasticsearch/logstash-7.8.1/config/book_index2_last_id"
    }
}

date {
match => [ "modification_time", "yyyyMMddHHmm" ]
timezone => "Asia/Shanghai"
}

output {
    elasticsearch {
        # 索引名称
        index => "book_index2"
        # es文档的id为数据库表的id
        document_id => "%{id}"
        hosts => ["http://192.168.137.129:9200"]
    }
}
```

```log
[2020-08-19T17:36:00,980][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.012726s) SELECT version()
[2020-08-19T17:36:01,016][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.000614s) SELECT version()
[2020-08-19T17:36:01,222][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.000954s) SELECT count(*) AS `count` FROM (select bookId as id , bookName, bookDate from book where bookDate > '1970-01-01 08:00:00' AND bookDate < NOW() ORDER BY bookDate desc) AS `t1` LIMIT 1
[2020-08-19T17:36:01,260][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.001160s) SELECT * FROM (select bookId as id , bookName, bookDate from book where bookDate > '1970-01-01 08:00:00' AND bookDate < NOW() ORDER BY bookDate desc) AS `t1` LIMIT 10000 OFFSET 0
[2020-08-19T17:37:00,246][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.000626s) SELECT version()
[2020-08-19T17:37:00,255][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.000419s) SELECT version()
[2020-08-19T17:37:00,266][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.000589s) SELECT count(*) AS `count` FROM (select bookId as id , bookName, bookDate from book where bookDate > '2020-08-14 08:16:48' AND bookDate < NOW() ORDER BY bookDate desc) AS `t1` LIMIT 1
[2020-08-19T17:37:00,275][INFO ][logstash.inputs.jdbc     ][main][6794240898e152ffa9e4c466a180124af7ebe6ac2d0f43d44028ef390132274c] (0.000838s) SELECT * FROM (select bookId as id , bookName, bookDate from book where bookDate > '2020-08-14 08:16:48' AND bookDate < NOW() ORDER BY bookDate desc) AS `t1` LIMIT 10000 OFFSET 0
```
