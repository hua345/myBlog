[TOC]

# 1.[查询数据](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/search-search.html#search-search-api-example)

- [Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/query-dsl.html)
- [search-your-data](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/search-your-data.html)

## 1.1 基本查询

- `term`是代表完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词
- `match`查询会先对搜索词进行分词,分词完毕后再逐个对分词结果进行匹配，因此相比于term的精确搜索，match是分词匹配搜索

### 1.1.1 分页(以 match 为例)

默认查询`10`条结果

```json
GET jd-product/_search
{
  "from": 0,
  "size": 100,
  "query": {
    "match": {
      "productName": "伊利纯牛奶"
    }
  }
}
```

### 1.1.2 只返回指定字段(以 match 为例)

```json
GET jd-product/_search
{
  "_source": ["productName"], 
  "query": {
    "match": {
      "productName": "伊利纯牛奶"
    }
  }
}
```

### 1.1.3 搜索结果排序

- [fielddata](https://www.elastic.co/guide/en/elasticsearch/reference/current/fielddata.html)

默认是按照`_score`得分排序

```json
GET jd-product/_search
{
  "query": {
    "match": {
      "productName": "伊利纯牛奶"
    }
  },
  "sort": [
    {
      "_score": {
        "order": "desc"
      }
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
GET jd-product/_search
{
  "query": {
    "match": {
      "productName": "伊利牛奶"
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
GET jd-product/_search
{
  "query": {
    "match_phrase": {
      "productName": "伊利纯牛奶"
    }
  }
}
```

## 1.4 `term`不分词精确查询

`term`代表完全匹配，也就是精确查询，搜索前不会再对搜索词进行分词，所以我们的`搜索词`必须是`文档分词集合`中的一个

```json
GET jd-product/_search
{
  "query": {
    "term": {
      "productName": "牛奶"
    }
  }
}
```

`terms`查询某个字段里含有多个关键词的文档

```json
GET jd-product/_search
{
  "query": {
    "terms": {
      "productName": ["牛奶","伊利"]
    }
  }
}
```

## 1.5 `range`范围查询

- `from`范围开始
- `include_lower`是否包含范围的左边界，默认是true
- `include_upper`是否包含范围的右边界，默认是true
- `time_zone`时区
- `format`时间格式

```json
GET jd-product/_search
{
  "query": {
    "range": {
      "syncTime": {
        "gte": "2021-09-01 00:00:00",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}
```

## 1.6 `prefix`前缀模糊查询

匹配`bookName`以`玉`为前缀的文档

```
GET jd-product/_search
{
  "query": {
    "prefix": {
      "productName": "牛奶"
    }
  }
}
```

## 1.7 `wildcard`通配符查询

wildcard 查询：允许你使用通配符 `*` 和 `?` 来进行查询

- `*`代表一个或多个字符
- `?`仅代表一个字符
- 注意：这个查询功能影响性能

```
GET jd-product/_search
{
  "query": {
    "wildcard": {
      "productName": "牛奶*"
    }
  }
}
```

## 1.8 `ids`主键查询

对 index`_id`查询

```json
GET jd-product/_search
{
  "query": {
    "ids": {
      "values": ["2693720"]
    }
  }
}
```

## 1.9 [Boolean query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html#query-dsl-bool-query)

`bool query`可以组合任意多个简单查询，各个简单查询之间的逻辑表示如下：

| 属性     | 说明                                                                                           |
| -------- | ---------------------------------------------------------------------------------------------- |
| must     | 文档必须匹配 must 选项下的查询条件，相当于逻辑运算的 AND                                       |
| should   | 文档可以匹配 should 选项下的查询条件，也可以不匹配，相当于逻辑运算的 OR                        |
| must_not | 与 must 相反，匹配该选项下的查询条件的文档不会被返回                                           |
| filter   | 和 must 一样，匹配 filter 选项下的查询条件的文档才会被返回，但是 filter 不评分，只起到过滤功能 |

> You can use the `minimum_should_match` parameter to specify the number or percentage of `should` clauses returned documents *must* match.
>
> `minimum_should_match`参数可以设置至少匹配`should`的数量



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

## 查询示例

```json
{
  "from": 0,
  "size": 10,
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "bookName": {
              "value": "elasticSearch"
            }
          }
        },
        {
          "range": {
            "create_at": {
              "gte": "2021-05-18T00:00:00+08:00",
              "lte": "2021-05-19T00:00:00+08:00"
            }
          }
        }
      ]
    }
  },
  "_source": [
    "id",
    "bookName",
    "create_at"
  ],
  "sort": [
    {
      "id": {
        "order": "desc"
      }
    }
  ]
}
```

