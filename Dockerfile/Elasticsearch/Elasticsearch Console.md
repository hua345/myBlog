## 创建索引

```json
POST book_index/_doc
{
    "mappings":{
        "_doc":{
            "properties":{
                "bookId":{
                    "type":"long"
                },
                "bookName":{
                    "type":"text"
                },
                "bookDate":{
                    "type":"date"
                }
            }
        }
    }
}

POST book_index2/_doc
{
    "mappings":{
        "_doc":{
            "properties":{
                "bookName":{
                    "type":"text"
                },
                "bookDate":{
                    "type":"date"
                }
            }
        }
    }
}
```

## 查询索引

`GET book_index/_search`

```yml
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "book_index",
        "_type" : "_doc",
        "_id" : "kryf53MBc-botRcuIZmh",
        "_score" : 1.0,
        "_source" : {
          "mappings" : {
            "_doc" : {
              "properties" : {
                "bookId" : {
                  "type" : "long"
                },
                "bookName" : {
                  "type" : "text"
                },
                "bookDate" : {
                  "type" : "date"
                }
              }
            }
          }
        }
      }
    ]
  }
}
```
