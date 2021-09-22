# ES嵌套聚合

## 参考

- [Nested aggregation | Elasticsearch Guide ](https://www.elastic.co/guide/en/elasticsearch/reference/7.14/search-aggregations-bucket-nested-aggregation.html)

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

