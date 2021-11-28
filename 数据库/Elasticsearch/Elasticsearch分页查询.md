[TOC]

# ES分页查询

## 参考

- [https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html](https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html)
- [Paginate search results ](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after)
- [解决ElasticSearch深度分页机制中Result window is too large问题](https://blog.csdn.net/lisongjia123/article/details/79041402)

## 1. From + size 分页查询


## 1.1 分布式系统中的深度分页

> 为了理解为什么深度分页会带来问题，让我们想象一下，我们在具有五个主分片的单个索引中进行搜索。当我们请求结果的第一页（结果1至10）时，每个分片都会产生自己的前10个结果，并将它们返回给协调节点，然后该节点对所有50个结果进行排序，以选择总的前10个结果。

现在想象一下，我们要1000页-结果为10,001至10,010。除了每个分片必须产生其最高的10,010个结果以外，其他所有事情的工作方式都相同。然后，协调节点对所有50,050个结果进行排序，并丢弃其中的50,040个结果！

您会看到，在分布式系统中，对结果的排序成本成指数增长，这随着我们页面的深入而增加。网络搜索引擎为任何查询返回的结果均不超过`10000`个是有充分的理由的。

## 查询结果中 hits.total.value 值最大为 10000 的限制

请求时设置 `"track_total_hits": true`，可以查询超过1万的总数

```json
GET jd-product/_search
{
  "track_total_hits": true,
  "query": {
    "match": {
      "productName": "牛奶"
    }
  }
}
```

```java
BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
if (StringUtils.hasText(param.getBookName())) {
    boolQueryBuilder.must(QueryBuilders.termQuery("bookName", param.getBookName()));
}
builder.query(boolQueryBuilder);
builder.trackTotalHits(true);
```

## 分页查询 from 大于 10000 时的数据异常

修改 `max_result_window` 设置的最大索引值，注意以 put 方式提交

```json
PUT /book_index/_settings
{
  "index":{
    "max_result_window":1000000
  }
}
```

不再建议使用`scroll API`进行深度分页。如果要分页检索超过 `Top 10,000+` 结果时，推荐使用：`PIT+search_after`

## scroll查询

当一个搜索请求返回单页结果时，可以使用 scroll API 检索体积大量（甚至全部）结果，这和在传统数据库中使用游标的方式非常相似。

不要把 `scroll` 用于实时请求，它主要用于大数据量的场景。例如：将一个索引的内容索引到另一个不同配置的新索引中。

```json
POST /jd-product/_search?scroll=10m
{
    "size": 10,
    "query": {
        "match" : {
            "productName": "牛奶"
        }
    }
}
{
  "_scroll_id" : "FGluY2x1ZGVfY29udGV4dF91dWlkDXF1ZXJ5QW5kRmV0Y2gBFk9RR1g3MmYwUThpWHFjQWtEN3U2bEEAAAAAAADochZOUnB2SGsxRFJjMldQcnRqUU9jVml3",
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  }
}
POST  /_search/scroll 
{
    "scroll" : "10m", 
    "scroll_id" : "FGluY2x1ZGVfY29udGV4dF91dWlkDXF1ZXJ5QW5kRmV0Y2gBFk9RR1g3MmYwUThpWHFjQWtEN3U2bEEAAAAAAADochZOUnB2SGsxRFJjMldQcnRqUU9jVml3" 
}
DELETE /_search/scroll
{
    "scroll_id" : "FGluY2x1ZGVfY29udGV4dF91dWlkDXF1ZXJ5QW5kRmV0Y2gBFk9RR1g3MmYwUThpWHFjQWtEN3U2bEEAAAAAAADochZOUnB2SGsxRFJjMldQcnRqUU9jVml3"
}
```

- `scroll`参数表示快照保持时间
- 第一次搜索返回`scroll_id`和`size`数量大小数据
- 当超出了 `scroll timeout` 时，搜索上下文会被自动删除。保持 scrolls 打开是有成本的，当不再使用`scroll`时应当使用 `clear-scroll` API 进行显式清除。

## [search after](https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html#search-after)

```yaml
GET /jd-product/_search
{
  "from": 0,
  "size": 10,
  "_source": ["price"], 
  "query": {
    "match": {
      "productName": "牛奶"
    }
  },
  "sort": [
    {
      "price": {
        "order": "asc"
      },
      "_score":{
        "order": "desc"
      }
    }
  ]
}
# 结果
[
  {
    "_index": "jd-product",
    "_type": "_doc",
    "_id": "862229",
    "_score": 1.5517712,
    "_source": {
      "price": "56.90"
    },
    "sort": [56.9, 1.5517712]
  },
  {
    "_index": "jd-product",
    "_type": "_doc",
    "_id": "100000770480",
    "_score": 1.7800024,
    "_source": {
      "price": "57.90"
    },
    "sort": [57.9, 1.7800024]
  }
]
```

使用**search_after**

```yaml
GET /jd-product/_search
{
  "from": 0,
  "size": 10,
  "_source": [
    "price"
  ],
  "query": {
    "match": {
      "productName": "牛奶"
    }
  },
  "search_after": [
    57.9,
    1.7800024
  ],
  "sort": [
    {
      "price": {
        "order": "asc"
      },
      "_score": {
        "order": "desc"
      }
    }
  ]
}
# 结果
[
  {
    "_index": "jd-product",
    "_type": "_doc",
    "_id": "100001600621",
    "_score": 1.5781026,
    "_source": {
      "price": "69.90 "
    },
    "sort": [69.9, 1.5781026]
  },
  {
    "_index": "jd-product",
    "_type": "_doc",
    "_id": "1281671",
    "_score": 1.5517712,
    "_source": {
      "price": "69.90 "
    },
    "sort": [69.9, 1.5517712]
  }
]

```



> Using requires multiple search requests with the same and values. If a [refresh](https://www.elastic.co/guide/en/elasticsearch/reference/current/near-real-time.html) occurs between these requests, the order of your results may change, causing inconsistent results across pages. To prevent this, you can create a [point in time (PIT)](https://www.elastic.co/guide/en/elasticsearch/reference/current/point-in-time-api.html) to preserve the current index state over your searches.
>
> 需要多次查询返回相同结果。如果在这些请求之间发生[刷新](https://www.elastic.co/guide/en/elasticsearch/reference/current/near-real-time.html)数据，则结果的顺序可能会更改，导致整个页面的结果不一致。为了防止这种情况，您可以创建一个[时间点 （PIT）](https://www.elastic.co/guide/en/elasticsearch/reference/current/point-in-time-api.html)来在搜索中保留当前的索引状态

```json
POST /jd-product/_pit?keep_alive=1m
# 返回
{
  "id" : "y-ezAwEKamQtcHJvZHVjdBZHdDhleTRoMlFGMjVzWkp2SjlfQ0h3ABZOUnB2SGsxRFJjMldQcnRqUU9jVml3AAAAAAAAASGsFk9RR1g3MmYwUThpWHFjQWtEN3U2bEEAARZHdDhleTRoMlFGMjVzWkp2SjlfQ0h3AAA="
}
# 使用pit进行查询
GET /_search
{
  "size": 10,
  "query": {
    "match": {
      "productName": "牛奶"
    }
  },
  "pit": {
    "id": "y-ezAwEKamQtcHJvZHVjdBZHdDhleTRoMlFGMjVzWkp2SjlfQ0h3ABZOUnB2SGsxRFJjMldQcnRqUU9jVml3AAAAAAAAASKvFk9RR1g3MmYwUThpWHFjQWtEN3U2bEEAARZHdDhleTRoMlFGMjVzWkp2SjlfQ0h3AAA=",
    "keep_alive": "1m"
  }
}
```

