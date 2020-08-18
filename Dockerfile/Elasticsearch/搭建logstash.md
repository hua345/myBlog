### [logstash](https://www.elastic.co/cn/products/logstash)

- [logstash](https://www.elastic.co/cn/products/logstash)
- [https://github.com/elastic/logstash](https://github.com/elastic/logstash)

![elasticsearch02](./img/elasticsearch02.png)

其实它就是一个 收集器 而已，我们需要为它指定Input和Output（当然Input和Output可以为多个）。由于我们需要把Java代码中Log4j的日志输出到ElasticSearch中，因此这里的Input就是Log4j，而Output就是`ElasticSearch`。

#### 集中、转换和存储数据

`Logstash` 是开源的服务器端数据处理管道，能够同时从多个来源采集数据，转换数据，然后将数据发送到您最喜欢的“存储库”中。
采集各种样式、大小和来源的数据

#### 采集各种样式、大小和来源的数据

数据往往以各种各样的形式，或分散或集中地存在于很多系统中。 Logstash 支持 各种输入选择 ，可以在同一时间从众多常用来源捕捉事件。

![logstash](./img/diagram-logstash-inputs.svg)

#### 实时解析和转换数据

数据从源传输到存储库的过程中，`Logstash` 过滤器能够解析各个事件，识别已命名的字段以构建结构，并将它们转换成通用格式，以便更轻松、更快速地分析和实现商业价值。

![logstash](./img/diagram-logstash-filters.svg)

#### 选择您的存储库，导出您的数据

尽管 Elasticsearch 是我们的首选输出方向，能够为我们的搜索和分析带来无限可能，但它并非唯一选择。

![logstash](./img/diagram-logstash-outputs.svg)

```bash
wget https://artifacts.elastic.co/downloads/logstash/logstash-7.8.1.tar.gz

tar -zvxf logstash-7.8.1.tar.gz
cd logstash-7.8.1
vim config/logstash.yml
```

#### 使用命令行命令调试

```bash
./bin/logstash -e 'input { stdin { } } output { stdout {} }'
#The stdin plugin is now waiting for input:
hello
2016-11-22T14:14:57.851Z learnLinux hello
./bin/logstash -e 'input { stdin { } } output { stdout { codec => rubydebug } }'
goodnight
{
    "@timestamp" => 2016-11-22T14:35:40.557Z,
      "@version" => "1",
          "host" => "learnLinux",
       "message" => "goodnight",
          "tags" => []
}
```

通过修改`output { stdout {}}`的参数，我们改变了`Logstash`输出格式．类似我们可以修改`input`,`filter`,`output`配置，生成我们想要的格式化日志方便查询．

#### 输出到`elasticsearch`,新建`config/simple.conf`文件

```conf
input { stdin { } }
filter {
  grok {
    match => { "message" => "%{COMBINEDAPACHELOG}" }
  }
  date {
    match => [ "timestamp" , "dd/MMM/yyyy:HH:mm:ss Z" ]
  }
}
output {
  elasticsearch { hosts => ["localhost:9200"] }
  stdout { codec => rubydebug }
}
```

```bash
./bin/logstash  -f config/simple.conf
#在终端输入一条访问日志
127.0.0.1 - - [11/Dec/2013:00:01:45 -0800] "GET /xampp/status.php HTTP/1.1" 200 3891 "http://cadenza/xampp/navi.php" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0"
{
        "request" => "/xampp/status.php",
          "agent" => "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0\"",
           "auth" => "-",
          "ident" => "-",
           "verb" => "GET",
        "message" => "127.0.0.1 - - [11/Dec/2013:00:01:45 -0800] \"GET /xampp/status.php HTTP/1.1\" 200 3891 \"http://cadenza/xampp/navi.php\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0\"",
           "tags" => [],
       "referrer" => "\"http://cadenza/xampp/navi.php\"",
     "@timestamp" => 2013-12-11T08:01:45.000Z,
       "response" => "200",
          "bytes" => "3891",
       "clientip" => "127.0.0.1",
       "@version" => "1",
           "host" => "learnLinux",
    "httpversion" => "1.1",
      "timestamp" => "11/Dec/2013:00:01:45 -0800"
}
```