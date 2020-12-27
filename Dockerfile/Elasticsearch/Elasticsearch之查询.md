# 1.[查询数据](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/search-search.html#search-search-api-example)

- [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/query-dsl.html)
- [search-your-data](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/search-your-data.html)

## 1.1 基本查询

- `term`是代表完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词
- `match`查询会先对搜索词进行分词,分词完毕后再逐个对分词结果进行匹配，因此相比于term的精确搜索，match是分词匹配搜索

### 1.1.1 分页(以 match 为例)

默认查询`10`条结果

```json
GET book_index/_search
{
    "from":0,
    "size":100,
    "query":{
        "match":{
            "bookName":"玉米"
        }
    }
}
```

### 1.1.2 只返回指定字段(以 match 为例)

```json
GET book_index/_search
{
    "_source":["bookName"],
    "query":{
        "match":{
            "bookName":"玉米"
        }
    }
}
```

### 1.1.3 搜索结果排序

- [fielddata](https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html)

默认是按照`_score`得分排序

```json
GET /book_index/_search
{
  "query": {
    "term": {
      "bookName": "玉米"
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
      "fielddata": true
    }
  }
}
```

## 1.2 `match`分词查询

`match`查询会先对搜索词进行分词，分词完毕后再逐个对分词结果进行匹配

```json
{
  "query": {
    "match": {
      "bookName": "玉米"
    }
  }
}
```

`match_all`：查询所有文档

```json
{
  "query": {
    "match_all": {}
  }
}
```

## 1.3 `match_phrase`短语查询

`match_phrase` 称为短语搜索，要求所有的分词必须同时出现在文档中，同时位置必须紧邻一致。

```json
{
  "query": {
    "match": {
      "bookName": "玉米"
    }
  }
}
```

## 1.4 `term`不分词精确查询

`term`代表完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词，所以我们的`搜索词`必须是`文档分词集合`中的一个

```json
GET /book_index/_search
{
  "query": {
    "term": {
      "bookName": "米"
    }
  }
}
```

`terms`查询某个字段里含有多个关键词的文档

```json
GET /book_index/_search
{
  "query": {
    "terms": {
      "bookName": ["玉","米"]
    }
  }
}
```

## `range`范围查询

```json
GET /book_index/_search
{
  "query": {
    "range": {
      "bookDate": {
        "gte": "2020-08-01 00:00:00",
        "lte": "2020-08-30 23:59:59",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}
```

## `ids`主键查询

对 index`_id`查询

```json
GET /book_index/_search
{
  "query": {
    "ids": {
      "values": [
        "1",
        "2"
      ]
    }
  }
}
```

## 1.7 [`bool` 查询](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/query-dsl-bool-query.html#query-dsl-bool-query)

`bool query`可以组合任意多个简单查询，各个简单查询之间的逻辑表示如下：

| 属性     | 说明                                                                                           |
| -------- | ---------------------------------------------------------------------------------------------- |
| must     | 文档必须匹配 must 选项下的查询条件，相当于逻辑运算的 AND                                       |
| should   | 文档可以匹配 should 选项下的查询条件，也可以不匹配，相当于逻辑运算的 OR                        |
| must_not | 与 must 相反，匹配该选项下的查询条件的文档不会被返回                                           |
| filter   | 和 must 一样，匹配 filter 选项下的查询条件的文档才会被返回，但是 filter 不评分，只起到过滤功能 |

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "bookName": "米"
          }
        }
      ],
      "filter": [
        {
          "term": {
            "company_id": "802795ea-f988-4ba9-836e-d88c6be28e7d"
          }
        }
      ]
    }
  }
}
```
