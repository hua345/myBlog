# [ElasticSeearch](https://www.elastic.co/cn/products/elasticsearch)

- [https://www.elastic.co/cn/products/elasticsearch](https://www.elastic.co/cn/products/elasticsearch)
- [Get Started with Elasticsearch](https://www.elastic.co/cn/start)
- [https://github.com/elastic/elasticsearch](https://github.com/elastic/elasticsearch)

## 简介

> Elasticsearch 是一个分布式、RESTful 风格的搜索和数据分析引擎，能够解决不断涌现出的各种用例。 作为 Elastic Stack 的核心，它集中存储您的数据，帮助您发现意料之中以及意料之外的情况。
>
> 通过 Elasticsearch，您能够执行及合并多种类型的搜索（结构化数据、非结构化数据、地理位置、指标），搜索方式随心而变。先从一个简单的问题出发，试试看能够从中发现些什么。找到与查询最匹配的 10 个文档是一回事。但如果面对的是十亿行日志，又该如何解读呢？Elasticsearch 聚合让您能够从大处着眼，探索数据的趋势和模式。

`ELK`由[ElasticSearch](https://www.elastic.co/downloads/elasticsearch)、[Logstash](https://www.elastic.co/products/logstash)和[Kiabana](https://www.elastic.co/downloads/kibana)三个开源工具组成。

![elasticsearch01](./img/elasticsearch01.png)

`ElasticSearch`是一个基于[Apache Lucene](https://lucene.apache.org/core/)(TM)的开源搜索引擎。`Elasticsearch`也使用 Java 开发并使用`Lucene`作为其核心来实现所有索引和搜索的功能，但是它的目的是通过简单的`RESTful API`来隐藏 Lucene 的复杂性，从而让全文搜索变得简单。

### 添加 elasticsearch 用户

```bash
adduser elasticsearch
passwd elasticsearch
chown -R elasticsearch:elasticsearch elasticsearch
```

### 使用新用户运行`Elasticsearch`

[elasticsearch 下载页面](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html)

```bash
ssh elasticsearch@192.168.137.128

➜  ~ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.1-linux-x86_64.tar.gz

➜  ~ tar -zvxf elasticsearch-7.8.1-linux-x86_64.tar.gz
➜  ~ mv elasticsearch-7.8.1/ /home/elasticsearch/elasticsearch-7.8.1/
➜  ~ chown -R elasticsearch:elasticsearch /home/elasticsearch/elasticsearch-7.8.1
➜  ~ mkdir /var/elasticsearch
➜  ~ mkdir /var/elasticsearch/data
➜  ~ mkdir /var/elasticsearch/logs
➜  ~ chown -R elasticsearch:elasticsearch /var/elasticsearch
```

| 文件类型 | 说明                                       | 默认位置                                |
| -------- | ------------------------------------------ | --------------------------------------- |
| home     | Elasticsearch home directory or `$ES_HOME` | Elasticsearch 解压后目录                |
| conf     | 配置文件包含`elasticsearch.yml`            | `$ES_HOME/config`                       |
| data     | index/shard 数据文件                       | `$ES_HOME/data` 配置文件对应`path.data` |
| logs     | 日志文件位置                               | `$ES_HOME/logs` 配置文件对应`path.logs` |
| plugins  | plugins 插件位置                           | `$ES_HOME/plugins`                      |

#### 修改配置`config/elasticsearch.yml`

```conf
# ------------------------------------ Node ------------------------------------
#
# Use a descriptive name for the node:
#
node.name: node01

# ---------------------------------- Network -----------------------------------
#
# Set the bind address to a specific IP (IPv4 or IPv6):
#
network.host: 192.168.137.128
#
# Set a custom port for HTTP:
#
http.port: 9200

# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when this node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
discovery.seed_hosts: ["host1"]
#
# Bootstrap the cluster using an initial set of master-eligible nodes:
#
cluster.initial_master_nodes: ["node01"]
```

### 启动出现的问题

```bash
ERROR: [3] bootstrap checks failed
[1]: max file descriptors [4096] for elasticsearch process is too low, increase to at least [65535]
[2]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
[3]: the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
```

解决方法

```bash
#解决[1]: max file descriptors [4096]
➜  ~ ulimit -Hn
4096

ulimit -u 65536
➜  ~ vi /etc/security/limits.d/20-nproc.conf
*          soft    nofile    65536
*          hard    nofile    65536
root       soft    nproc     unlimited
➜  ~ vi /etc/security/limits.conf
* soft nofile 65536
* hard nofile 65536
* soft nproc 4096
* hard nproc 4096
# 重启电脑

#解决[2]: max virtual memory areas vm.max_map_count [65530] is too low
➜  ~ vi /etc/sysctl.conf
vm.max_map_count=262144

# 使得修改生效
➜  ~ sysctl -p
vm.max_map_count = 262144

#解决[3]: the default discovery settings are unsuitable for production use;
#修改配置`config/elasticsearch.yml`
# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when this node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
discovery.seed_hosts: ["host1"]
#
# Bootstrap the cluster using an initial set of master-eligible nodes:
#
cluster.initial_master_nodes: ["node01"]
```

### 加入`systemctl`服务

```bash
vi /lib/systemd/system/elasticsearch.service
```

```conf
[Unit]
Description=elasticsearch Service 01
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=elasticsearch
Group=elasticsearch
LimitNOFILE=65536
LimitNPROC=65536
ExecStart=/home/elasticsearch/elasticsearch-7.8.1/bin/elasticsearch
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable elasticsearch
systemctl start elasticsearch
```

#### 设置默认索引

![esSetDefaultIndex](./img/esSetDefaultIndex.png)

#### 打开另一个终端进行测试

```json
➜  ~ http http://192.168.137.129:9200/
HTTP/1.1 200 OK
content-encoding: gzip
content-length: 329
content-type: application/json; charset=UTF-8

{
    "cluster_name": "elasticsearch",
    "cluster_uuid": "uzfkMxgBQUmpqwSEP-SqXQ",
    "name": "node01",
    "tagline": "You Know, for Search",
    "version": {
        "build_date": "2020-07-21T16:40:44.668009Z",
        "build_flavor": "default",
        "build_hash": "b5ca9c58fb664ca8bf9e4057fc229b3396bf3a89",
        "build_snapshot": false,
        "build_type": "tar",
        "lucene_version": "8.5.1",
        "minimum_index_compatibility_version": "6.0.0-beta1",
        "minimum_wire_compatibility_version": "6.8.0",
        "number": "7.8.1"
    }
}
```

这说明你的`ELasticsearch`集群已经启动并且正常运行

### 后台运行

```bash
# nohup ./bin/elasticsearch > ~/elastic.log 2>&1 &
./bin/elasticsearch

[2019-07-21T20:39:34,412][DEBUG][o.e.a.ActionModule       ] [consul01] Using REST wrapper from plugin org.elasticsearch.xpack.security.Security
[2019-07-21T20:39:35,035][INFO ][o.e.d.DiscoveryModule    ] [consul01] using discovery type [zen] and seed hosts providers [settings]
[2019-07-21T20:39:37,367][INFO ][o.e.n.Node               ] [consul01] initialized
[2019-07-21T20:39:37,368][INFO ][o.e.n.Node               ] [consul01] starting ...
[2019-07-21T20:39:52,775][INFO ][o.e.t.TransportService   ] [consul01] publish_address {127.0.0.1:9300}, bound_addresses {[::1]:9300}, {127.0.0.1:9300}
...
[2019-07-21T20:39:56,247][INFO ][o.e.h.AbstractHttpServerTransport] [consul01] publish_address {127.0.0.1:9200}, bound_addresses {[::1]:9200}, {127.0.0.1:9200}
[2019-07-21T20:39:56,249][INFO ][o.e.n.Node               ] [consul01] started
[2019-07-21T20:39:56,352][INFO ][o.e.g.GatewayService     ] [consul01] recovered [0] indices into cluster_state
```

如果想在后台以守护进程模式运行，添加`-d`参数。

```bash
➜  ~ netstat -lntup
tcp6       0      0 127.0.0.1:9200          :::*                    LISTEN      45705/java
tcp6       0      0 ::1:9200                :::*                    LISTEN      45705/java
tcp6       0      0 127.0.0.1:9300          :::*                    LISTEN      45705/java
tcp6       0      0 ::1:9300                :::*                    LISTEN      45705/java
```

#### [Elasticsearch 权威指南中文版](https://github.com/looly/elasticsearch-definitive-guide-cn)
