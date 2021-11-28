[TOC]

# elasticsearch 控制台

- [Compact and aligned text (CAT) APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html)

- [Tune for indexing speed](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html)
- [Index modules](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html)

```bash
GET _cat/
=^.^=
/_cat/allocation
/_cat/shards
/_cat/shards/{index}
/_cat/master
/_cat/nodes
/_cat/tasks
/_cat/indices
/_cat/indices/{index}
/_cat/segments
/_cat/segments/{index}
/_cat/count
/_cat/count/{index}
/_cat/recovery
/_cat/recovery/{index}
/_cat/health
/_cat/pending_tasks
/_cat/aliases
/_cat/aliases/{alias}
/_cat/thread_pool
/_cat/thread_pool/{thread_pools}
/_cat/plugins
/_cat/fielddata
/_cat/fielddata/{fields}
/_cat/nodeattrs
/_cat/repositories
/_cat/snapshots/{repository}

# 查看ES信息
GET /
{
  "name" : "node-1",
  "cluster_name" : "my-application",
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

# 检测集群是否健康
GET _cat/health?v
# 查询集群的节点
GET _cat/nodes?v
# 查询所有索引
GET _cat/indices?v
# 查询segments信息
GET /_cat/segments/jd-product?v
index      shard prirep ip        segment generation docs.count docs.deleted   size size.memory committed searchable version compound
jd-product 0     p      127.0.0.1 _0               0         50           40  106kb        6132 true      true       8.9.0   true
jd-product 0     p      127.0.0.1 _1               1         30            0 39.9kb        5868 true      true       8.9.0   true
jd-product 0     p      127.0.0.1 _2               2         60            0   77kb        5868 true      true       8.9.0   true
# 使用_forcemerge合并segments
POST task_sit/_forcemerge?max_num_segments=10
# 如果segment的committed和searchable是false
# 刷新jd-product数据到磁盘
POST /jd-product/_flush
```



