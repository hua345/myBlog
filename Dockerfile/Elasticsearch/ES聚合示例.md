# ES 聚合示例

## 按月去重统计

```json
GET my_index/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "company_id": "company_id"
          }
        },
        {
          "term": {
            "online_status": true
          }
        },
        {
          "range": {
            "create_at": {
              "gte": "2020-11-01"
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "create_at_date_histogram": {
      "date_histogram": {
        "field": "create_at",
        "calendar_interval": "month",
        "format": "yyyy-MM",
        "time_zone": "+08:00"
      },
      "aggs": {
        "distinct_num": {
          "cardinality": {
            "field": "name"
          }
        }
      }
    }
  }
}
```

对应的java示例代码

```java
//范围查询
BoolQueryBuilder boolQueryBuilder = QueryBuilders.boolQuery();
boolQueryBuilder.must(QueryBuilders.termQuery("company_id", param.getCompanyId()));
boolQueryBuilder.must(QueryBuilders.termQuery("online_status", true));
RangeQueryBuilder rangeQueryBuilder = QueryBuilders.rangeQuery("create_at");
if (Objects.nonNull(param.getStartDate())) {
    rangeQueryBuilder.gte(param.getStartDate());
}
if (Objects.nonNull(param.getEndDate())) {
    rangeQueryBuilder.lte(param.getEndDate());
}
boolQueryBuilder.must(rangeQueryBuilder);

AggregationBuilder aggregationBuilder = AggregationBuilders.dateHistogram("create_at_date_histogram")
        .calendarInterval(DateHistogramInterval.MONTH)
        .minDocCount(0)
        .field("create_at")
        .format("yyyy-MM")
        .timeZone(ZoneId.systemDefault());

// 设置子查询
CardinalityAggregationBuilder cardinalityAggregationBuilder = AggregationBuilders.cardinality("distinct_num").field("name");
aggregationBuilder.subAggregation(cardinalityAggregationBuilder);
SearchSourceBuilder builder = new SearchSourceBuilder();
//指定size为0 不返回文档 因为只需要数量
builder.query(boolQueryBuilder).aggregation(aggregationBuilder).size(0);
builder.timeout(new TimeValue(60, TimeUnit.SECONDS));
//创建查询请求，规定查询的索引
SearchRequest searchRequest = new SearchRequest("my_index");
//将构造好的条件放入请求中
searchRequest.source(builder);

SearchResponse searchResponse = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
Aggregation agg = searchResponse.getAggregations().get("create_at_date_histogram");

List<? extends Histogram.Bucket> buckets = ((Histogram) agg).getBuckets();
List<StatisticVmOnlineOfMonthVo> bucketList = new ArrayList<>(16);
for (Histogram.Bucket bucket : buckets) {
    StatisticVmOnlineOfMonthVo statisticVmOnlineOfMonthVo = new StatisticVmOnlineOfMonthVo();
    statisticVmOnlineOfMonthVo.setKeyAsString(bucket.getKeyAsString());
    statisticVmOnlineOfMonthVo.setDocCount(bucket.getDocCount());
    ParsedCardinality parsedCardinality = bucket.getAggregations().get("vm_code_distinct_num");
    if(Objects.nonNull(parsedCardinality)){
        statisticVmOnlineOfMonthVo.setValue(parsedCardinality.getValue());
    }
    bucketList.add(statisticVmOnlineOfMonthVo);
}
log.info("searchResponse Bucket:{}", bucketList);
```
