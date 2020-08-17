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

`POST book_index/_doc`

```json
{
  "mappings": {
    "_doc": {
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

## 修改 Index 类型

### 新建新的 Index

`POST book_index2/_doc`

```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 2
  },
  "mappings": {
    "_doc": {
      "properties": {
        "bookName": {
          "type": "text"
        },
        "bookDate": {
          "type": "date"
        }
      }
    }
  }
}
```
