# [beats](https://www.elastic.co/cn/products/beats)

- [https://www.elastic.co/cn/products/beats](https://www.elastic.co/cn/products/beats)
- [https://github.com/elastic/beats](https://github.com/elastic/beats)

## 轻量型数据采集器

Beats 平台集合了多种单一用途数据采集器。它们从成百上千或成千上万台机器和系统向 Logstash 或 Elasticsearch 发送数据。

收集端logstash替换为beats，更灵活，消耗资源更少，扩展性更强

## Beats 系列

![elk_beats.png](./img/elk_beats.png)

### [filebeat](https://www.elastic.co/cn/products/beats/filebeat)轻量型日志采集器

当您要面对成百上千、甚至成千上万的服务器、虚拟机和容器生成的日志时，请告别 SSH 吧。 filebeat将为您提供一种轻量型方法，用于转发和汇总日志与文件，让简单的事情不再繁杂。

![filebeat](./img/icon-filebeat-bb.svg)

![file_beats.png](./img/file_beats.png)

`Filebeat` 内置有多种模块（auditd、Apache、NGINX、System、MySQL 等等），可针对常见格式的日志大大简化收集、解析和可视化过程，只需一条命令即可。

输送至 `Elasticsearch` 或 `Logstash`。在`Kibana`中实现可视化。
`Filebeat` 是 `Elastic Stack` 的一部分，因此能够与 `Logstash`、`Elasticsearch` 和 `Kibana` 无缝协作。无论您要使用 `Logstash` 转换或充实日志和文件，还是在 `Elasticsearch` 中随意处理一些数据分析，亦或在 `Kibana` 中构建和分享仪表板，`Filebeat` 都能轻松地将您的数据发送至最关键的地方。

### 下载filebeat

```bash
tar -zvxf filebeat-7.2.0-linux-x86_64.tar.gz
filebeat-7.2.0-linux-x86_64
```

### 配置Filebeat

配置文件：`filebeat.yml`

为了配置Filebeat：

#### 定义日志文件路径

对于最基本的Filebeat配置，你可以使用单个路径。例如：

```yaml
#=========================== Filebeat inputs =============================

filebeat.inputs:

# Each - is an input. Most options can be set at the input level, so
# you can use different inputs for various configurations.
# Below are the input specific configurations.

- type: log

  # Change to true to enable this input configuration.
  enabled: true

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /root/kafka/data01/*.log
    - /root/kafka/data02/*.log
    - /root/kafka/data03/*.log
    #- c:\programdata\elasticsearch\logs\*
```

#### 设置输出目录到Elasticsearch

那么设置IP地址和端口以便能够找到Elasticsearch

```yaml
#================================ Outputs =====================================

# Configure what output to use when sending the data collected by the beat.

#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["192.168.137.128:9200"]

  # Optional protocol and basic auth credentials.
  #protocol: "https"
  #username: "elastic"
  #password: "changeme"
```

如果你打算用Kibana仪表盘，可以这样配置Kibana端点

```yaml
#============================== Kibana =====================================

# Starting with Beats version 6.0.0, the dashboards are loaded via the Kibana API.
# This requires a Kibana endpoint configuration.
setup.kibana:

  # Kibana Host
  # Scheme and port can be left out and will be set to the default (http and 5601)
  # In case you specify and additional path, the scheme is required: http://localhost:5601/path
  # IPv6 addresses should always be defined as: https://[2001:db8::1]:5601
  host: "192.168.137.128:5601"
```

## 启动Filebeat

```bash
./filebeat -e -c filebeat.yml -d "publish"
```
