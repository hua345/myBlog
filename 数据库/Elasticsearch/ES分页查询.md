# ES分页查询

## 参考

- [https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html](https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html)
- [解决ElasticSearch深度分页机制中Result window is too large问题](https://blog.csdn.net/lisongjia123/article/details/79041402)

## 1. From + size 分页查询


## 1.1 分布式系统中的深度分页

> 为了理解为什么深度分页会带来问题，让我们想象一下，我们在具有五个主分片的单个索引中进行搜索。当我们请求结果的第一页（结果1至10）时，每个分片都会产生自己的前10个结果，并将它们返回给协调节点，然后该节点对所有50个结果进行排序，以选择总的前10个结果。

现在想象一下，我们要1000页-结果为10,001至10,010。除了每个分片必须产生其最高的10,010个结果以外，其他所有事情的工作方式都相同。然后，协调节点对所有50,050个结果进行排序，并丢弃其中的50,040个结果！

您会看到，在分布式系统中，对结果的排序成本成指数增长，这随着我们页面的深入而增加。网络搜索引擎为任何查询返回的结果均不超过`10000`个是有充分的理由的。

## 查询结果中 hits.total.value 值最大为 10000 的限制

请求时设置 `"track_total_hits": true`

```json
GET book_index/_search
{
    "track_total_hits": true,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "bookName": "elasticsearch"
          }
        }
      ]
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
