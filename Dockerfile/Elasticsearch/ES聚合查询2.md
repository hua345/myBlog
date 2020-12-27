# ES聚合查询

- [https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
 

## 聚合

ES对`aggs`聚合查询结果的展示默认只显示10条，要想展示更对，需要在请求体中加上size参数。

### `terms`聚合

```json
GET /my-index-000001/_search
{
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
```

### 添加`query`参数限制查询范围

```json
GET /my-index-000001/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1d/d",
        "lt": "now/d"
      }
    }
  },
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
```

### 设置`size：0`只查询聚合结果

### 多个聚合

```json
GET /my-index-000001/_search
{
  "aggs": {
    "my-first-agg-name": {
      "terms": {
        "field": "my-field"
      }
    },
    "my-second-agg-name": {
      "avg": {
        "field": "my-other-field"
      }
    }
  }
}
```

### 子聚合

```json
GET /my-index-000001/_search
{
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      },
      "aggs": {
        "my-sub-agg-name": {
          "avg": {
            "field": "my-other-field"
          }
        }
      }
    }
  }
}
```

```json
GET my_index/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": {
        "term": {
          "company_id": "my_company"
        }
      },
      "filter": {
        "range": {
          "create_at": {
            "gte": "2020-11-01"
          }
        }
      }
    }
  },
  "aggs": {
    "articles_over_time": {
      "date_histogram": {
        "field": "create_at",
        "calendar_interval": "month",
        "format": "yyyy-MM-dd",
        "time_zone": "+08:00"
      }
    }
  }
}
```