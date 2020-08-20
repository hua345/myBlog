# elasticsearch 控制台

- [https://www.elastic.co/guide/en/elasticsearch/reference/7.8/rest-apis.html](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/rest-apis.html)

```bash
# 检测集群是否健康
GET _cat/health?v
# 查询集群的节点
GET _cat/nodes?v
# 查询所有索引
GET _cat/indices?v
```

## 1.创建索引

- [date](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html)
- [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
- [number](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html)

`POST book_index`

```json
{
  "mappings": {
    "properties": {
      "bookId": {
        "type": "long"
      },
      "bookName": {
        "type": "text"
      },
      "bookDate": {
        "type": "date"
      }
    }
  }
}
```

## 2.查询索引

- `number_of_shards`,每个索引的主分片数,这个配置在索引创建后不能修改
- `number_of_replicas`,每个主分片的副本数,这个配置可以随时修改

## 修改 Index 类型

### 新建新的 Index

`PUT book_index2`

```json
PUT book_index2
{
  "mappings": {
    "properties": {
      "bookName": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "bookDate": {
        "type": "date",
        "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      }
    }
  }
}
```

### [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/docs-reindex.html)复制数据

```json
POST _reindex
{
  "source": {
    "index": "book_index"
  },
  "dest": {
    "index": "book_index2"
  }
}
```
