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

`GET book_index/_search`

`GET book_index/_mapping`

- `number_of_shards`,每个索引的主分片数,这个配置在索引创建后不能修改
- `number_of_replicas`,每个主分片的副本数,这个配置可以随时修改

## 3.分词处理

```json
GET book_index/_analyze
{
  "text" : "Hello World"
}
```

```json
{
  "tokens": [
    {
      "token": "hello",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "world",
      "start_offset": 6,
      "end_offset": 11,
      "type": "<ALPHANUM>",
      "position": 1
    }
  ]
}
```

## 4.[查询数据](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/search-search.html#search-search-api-example)

- [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/query-dsl.html)
- `term`代表完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词，所以我们的搜索词必须是文档分词集合中的一个
- `match`查询会先对搜索词进行分词，分词完毕后再逐个对分词结果进行匹配
- `match_phrase` 称为短语搜索，要求所有的分词必须同时出现在文档中，同时位置必须紧邻一致。

`GET book_index/_search?q=bookName:爱`

`GET book_index/_doc/26`

`GET /book_index/_search`

```json
{
  "query": {
    "term": {
      "bookName": "爱"
    }
  }
}
```

`GET /book_index/_search`

```json
{
  "query": {
    "bool": {
      "must": [{ "match": { "bookName": "爱" } }]
    }
  }
}
```

### 搜索排序

- [fielddata](https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html)

`GET /book_index/_search`

```json
{
  "query": {
    "term": {
      "bookName": "爱"
    }
  },
  "sort": [
    {
      "bookDate": { "order": "desc" }
    }
  ]
}
```

```json
{
  "shard": 0,
  "index": "book_index",
  "node": "JrQYgdP0RtaN2IWQga7x6A",
  "reason": {
    "type": "illegal_argument_exception",
    "reason": "Text fields are not optimised for operations that require per-document field data like aggregations and sorting, so these operations are disabled by default. Please use a keyword field instead. Alternatively, set fielddata=true on [bookDate] in order to load field data by uninverting the inverted index. Note that this can use significant memory."
  }
}
```

没有优化的字段 es 默认是禁止`聚合/排序`操作的。所以需要将要聚合的字段添加优化

`PUT book_index/_mapping`

```json
{
  "properties": {
    "bookDate": {
      "type": "date",
      "fielddata": true,
      "fields": {
        "keyword": {
          "type": "keyword",
          "ignore_above": 256
        }
      }
    }
  }
}
```

## 修改 Index 类型

### 新建新的 Index

`PUT book_index2`

```json
{
  "mappings": {
    "properties": {
      "bookName": {
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
