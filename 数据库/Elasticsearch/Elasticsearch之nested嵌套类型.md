[TOC]

# Elasticsearch之nested嵌套类型

## 参考

- [Nested field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html)
- [索引内部命中 ](https://www.elastic.co/guide/en/elasticsearch/reference/current/inner-hits.html#inner-hits)
- [Nested aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/7.14/search-aggregations-bucket-nested-aggregation.html)



## [数组对象是如何扁平化的](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html#nested-arrays-flattening-objects)

>  Elasticsearch has no concept of inner objects. Therefore, it flattens object hierarchies into a simple list of field names and values. 
>
> Elasticsearch 没有内部对象概念，将复杂对象扁平化为包含names和values的简单列表

```
PUT my-index-000001/_doc/1
{
  "group" : "fans",
  "user" : [ 
    {
      "first" : "John",
      "last" :  "Smith"
    },
    {
      "first" : "Alice",
      "last" :  "White"
    }
  ]
}
```

文档会内部转换为下面的文档

```
{
  "group" :        "fans",
  "user.first" : [ "alice", "john" ],
  "user.last" :  [ "smith", "white" ]
}
```

> The and fields are flattened into multi-value fields, and the association between and is lost.
>
> 文档扁平化成有多个值得字段，关联关系也丢失了。

下面不正确的查询也能查询出文档

```
GET my-index-000001/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "user.first": "Alice" }},
        { "match": { "user.last":  "Smith" }}
      ]
    }
  }
}
```

## [对象数组使用Nested类型](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html#nested-fields-array-objects)

> If you need to index arrays of objects and to maintain the independence of each object in the array, use the data type instead of the [`object`](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html) data type.`nested`
>
> Internally, nested objects index each object in the array as a separate hidden document, meaning that each nested object can be queried independently of the others with the [`nested` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html):
>
> 如果你需要维护数组内对象的关系，可以使用`nested`类型。
>
> 在内部，嵌套对象索引的时候将数组中的每个对象作为单独的隐藏文档，这意味着每个嵌套对象可以独立于的其他对象进行[nested query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html)

```
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "user": {
        "type": "nested" 
      }
    }
  }
}

PUT my-index-000001/_doc/1
{
  "group" : "fans",
  "user" : [
    {
      "first" : "John",
      "last" :  "Smith"
    },
    {
      "first" : "Alice",
      "last" :  "White"
    }
  ]
}
GET my-index-000001/_search
{
  "query": {
    "nested": {
      "path": "user",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "Smith" }} 
          ]
        }
      }
    }
  }
}

GET my-index-000001/_search
{
  "query": {
    "nested": {
      "path": "user",
      "query": {
        "bool": {
          "must": [
            { "match": { "user.first": "Alice" }},
            { "match": { "user.last":  "White" }} 
          ]
        }
      },
      "inner_hits": {}
    }
  }
}
```

## 与nested类型进行交互

- queried with the [`nested`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html) query.
- analyzed with the [`nested`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-nested-aggregation.html) and [`reverse_nested`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-reverse-nested-aggregation.html) aggregations.
- sorted with [nested sorting](https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html#nested-sorting).
- retrieved and highlighted with [nested inner hits](https://www.elastic.co/guide/en/elasticsearch/reference/current/inner-hits.html#nested-inner-hits).

## [Nested查询](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html)

> The `nested` query searches nested field objects as if they were indexed as separate documents. If an object matches the search, the `nested` query returns the root parent document.
>
>  `nested` 查询Nested对象时,如果匹配搜索, `nested` 查询返回根文档

```
PUT /products
{
  "mappings": {
    "properties": {
      "resellers": { 
        "type": "nested",
        "properties": {
          "reseller": {
            "type": "keyword"
          },
          "price": {
            "type": "double"
          }
        }
      }
    }
  }
}
```

```
PUT /products/_doc/0?refresh
{
  "name": "LED TV", 
  "resellers": [
    {
      "reseller": "companyA",
      "price": 350
    },
    {
      "reseller": "companyB",
      "price": 500
    }
  ]
}
```

```
GET /products/_search?size=0
{
  "query": {
    "match": {
      "name": "led tv"
    }
  },
  "aggs": {
    "resellers": {
      "nested": {
        "path": "resellers"
      },
      "aggs": {
        "filter_reseller": {
          "filter": {
            "bool": {
              "filter": [
                {
                  "term": {
                    "resellers.reseller": "companyB"
                  }
                }
              ]
            }
          },
          "aggs": {
            "min_price": {
              "min": {
                "field": "resellers.price"
              }
            }
          }
        }
      }
    }
  }
}
```

