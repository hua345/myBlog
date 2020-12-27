# ES聚合查询

```json
PUT employee
{
  "mappings": {
    "properties": {
      "id": {
        "type": "integer"
      },
      "name": {
        "type": "keyword"
      },
      "job": {
        "type": "keyword"
      },
      "age": {
        "type": "integer"
      },
      "gender": {
        "type": "keyword"
      }
    }
  }
}
```

```json
PUT employee/_bulk
{"index": {"_id": 1}}
{"id": 1, "name": "Bob", "job": "java", "age": 21, "sal": 8000, "gender": "male"}
{"index": {"_id": 2}}
{"id": 2, "name": "Rod", "job": "html", "age": 31, "sal": 18000, "gender": "female"}
{"index": {"_id": 3}}
{"id": 3, "name": "Gaving", "job": "java", "age": 24, "sal": 12000, "gender": "male"}
{"index": {"_id": 4}}
{"id": 4, "name": "King", "job": "dba", "age": 26, "sal": 15000, "gender": "female"}
{"index": {"_id": 5}}
{"id": 5, "name": "Jonhson", "job": "dba", "age": 29, "sal": 16000, "gender": "male"}
{"index": {"_id": 6}}
{"id": 6, "name": "Douge", "job": "java", "age": 41, "sal": 20000, "gender": "female"}
{"index": {"_id": 7}}
{"id": 7, "name": "cutting", "job": "dba", "age": 27, "sal": 7000, "gender": "male"}
{"index": {"_id": 8}}
{"id": 8, "name": "Bona", "job": "html", "age": 22, "sal": 14000, "gender": "female"}
{"index": {"_id": 9}}
{"id": 9, "name": "Shyon", "job": "dba", "age": 20, "sal": 19000, "gender": "female"}
{"index": {"_id": 10}}
{"id": 10, "name": "James", "job": "html", "age": 18, "sal": 22000, "gender": "male"}
{"index": {"_id": 11}}
{"id": 11, "name": "Golsling", "job": "java", "age": 32, "sal": 23000, "gender": "female"}
{"index": {"_id": 12}}
{"id": 12, "name": "Lily", "job": "java", "age": 24, "sal": 2000, "gender": "male"}
{"index": {"_id": 13}}
{"id": 13, "name": "Jack", "job": "html", "age": 23, "sal": 3000, "gender": "female"}
{"index": {"_id": 14}}
{"id": 14, "name": "Rose", "job": "java", "age": 36, "sal": 6000, "gender": "female"}
{"index": {"_id": 15}}
{"id": 15, "name": "Will", "job": "dba", "age": 38, "sal": 4500, "gender": "male"}
{"index": {"_id": 16}}
{"id": 16, "name": "smith", "job": "java", "age": 32, "sal": 23000, "gender": "male"}
```

## 查询工种的数量

```json
GET employee/_search
{
  "size": 0, 
  "aggs": {
    "job_category_count": {
      "cardinality": {
        "field": "job"
      }
    }
  }
}
```

## 查询每个工种的分桶信息

```json
GET employee/_search
{
  "size": 0,
  "aggs": {
    "job_category_num": {
      "cardinality": {
        "field": "job"
      }
    }
  }
}
```

## 查询不同工种的员工的数量，并查询每个工种最大年龄的员工信息。

```json
GET employee/_search
{
  "size": 0, 
  "aggs": {
    "job_analysis": {
      "terms": {
        "field": "job"
      },
      "aggs": {
        "age_top_1": {
          "top_hits": {
            "size": 1,
            "sort": [
              {
                "age": {
                  "order": "desc"
                }
              }  
            ]
          }
        }
      }
    }
  }
}
```

## 以每5000为一个区间，查询工资在对应范围内的员工的数量

```json
GET employee/_search
{
  "size": 0, 
  "aggs": {
    "sal_histogram": {
      "histogram": {
        "field": "sal",
        "interval": 5000,
        "extended_bounds": {
          "min": 0,
          "max": 25000
        }
      }
    }
  }
}
```

## 查询每个工种的数量，以及不同工种的工资统计信息

```json
GET employee/_search
{
  "size": 0, 
  "aggs": {
    "job_and_salary_info": {
      "terms": {
        "field": "job"
      },
      "aggs": {
        "sal_info": {
          "stats": {
            "field": "sal"
          }
        }
      }
    }
  }
}
```

## 不同工种下男女员工的数量，以及男女员工的薪资信息

```json
GET employee/_search
{
  "size": 0, 
  "aggs": {
    "job_gender_sal_info": {
      "terms": {
        "field": "job"
      },
      "aggs": {
        "gender_info": {
          "terms": {
            "field": "gender"
          },
          "aggs": {
            "sal_info": {
              "stats": {
                "field": "sal"
              }
            }
          }
        }
      }
    }
  }
}
```
