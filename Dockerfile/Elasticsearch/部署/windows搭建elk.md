[TOC]

# [ElasticSeearch](https://www.elastic.co/cn/products/elasticsearch)

- [https://www.elastic.co/cn/products/elasticsearch](https://www.elastic.co/cn/products/elasticsearch)
- [Get Started with Elasticsearch](https://www.elastic.co/cn/start)
- [Download Elasticsearch](https://www.elastic.co/cn/downloads/elasticsearch)
- [Download Kibana](https://www.elastic.co/cn/downloads/kibana)
- [Set up minimal security for Elasticsearch ](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-minimal-setup.html)

## 启动elasticsearch

```bash
# 修改es配置
vi config/elasticsearch.yml
# 启动elasticsearch
bin\elasticsearch.bat
```

## 访问[http://localhost:9200/](http://localhost:9200/)

```json
{
  "name" : "fang",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "C3Y9KRRdQD-NNchgcrGFQw",
  "version" : {
    "number" : "7.14.2",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "6bc13727ce758c0e943c3c21653b3da82f627f75",
    "build_date" : "2021-09-15T10:18:09.722761972Z",
    "build_snapshot" : false,
    "lucene_version" : "8.9.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

## 启动kibana

```bash
# 修改kibana配置
vi config/kibana.yml
# 启动kibana
bin\kibana.bat
[info][server][Kibana][http] http server running at http://localhost:5601
```

