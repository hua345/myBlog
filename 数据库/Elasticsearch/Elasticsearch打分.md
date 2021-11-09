[TOC]

## 参考

[Sort search results ](https://www.elastic.co/guide/en/elasticsearch/reference/current/sort-search-results.html)

[Search API boosts](https://www.elastic.co/guide/en/app-search/current/boosts.html)

[Function score query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html)

[Compound queries ](https://www.elastic.co/guide/en/elasticsearch/reference/current/compound-queries.html)

# Elasticsearch打分

```json
GET jd-product/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "productName": "伊利"
          }
        }
      ]
    }
  }
}
{
"hits" : [
      {
        "_index" : "jd-product",
        "_type" : "_doc",
        "_id" : "100007539289",
        "_score" : 8.174636,
        "_source" : {
          "productName" : "伊利 纯牛奶250ml*16盒/礼盒装"
        }
      },
      {
        "_index" : "jd-product",
        "_type" : "_doc",
        "_id" : "100013875646",
        "_score" : 7.114892,
        "_source" : {
          "productName" : "京东超市 伊利 纯牛奶250ml*21盒/箱 全脂牛奶 早餐奶"
        }
      }
    ]
}
```

默认搜索可以看到最高分是`8.174636`

## 通过`boost`提高权重

默认情况下，搜索条件的权重都是一样的，都是1

```json
GET jd-product/_search
{
  "_source": ["productName"], 
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "productName": "牛奶"
          }
        }
      ],
      "boost": 2
    }
  }
}

{
    "_index" : "jd-product",
    "_type" : "_doc",
    "_id" : "100007539289",
    "_score" : 16.349272,
    "_source" : {
        "productName" : "伊利 纯牛奶250ml*16盒/礼盒装"
    }
}
```

通过修改`boost`后,得到的分数变为`16.349272`

## 分数计算过程

> **score(freq=1.0)**, computed as **boost * idf * tf** from
> $$
> score = boost * idf * tf
> $$
> **idf**, computed as **log(1 + (N - n + 0.5) / (n + 0.5))** from
>
> 即此Term在此文档中出现了多少次。tf 越大说明越重要
> $$
> idf = log(1 + (N - n + 0.5) / (n + 0.5))
> $$
> n, number of documents containing term(当前文档包含Term数量)
> N, total number of documents with field(当前文档的字段总数)
>
> 
>
> **tf**, computed as **freq / (freq + k1 * (1 - b + b * dl / avgdl))** from:
>
> 即有多少文档包含次Term。df 越大说明越不重要。
> $$
> tf = freq / (freq + k1 * (1 - b + b * dl / avgdl))
> $$
> freq, occurrences of term within document(文档中关键字出现频率)
>
> k1, term saturation parameter
>
> b, length normalization parameter
>
> dl, length of field(字段长度)
>
> avgdl, average length of field(字段平均长度)



```json
GET jd-product/_search
{
  "_source": ["productName"], 
  "explain": true, 
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "productName": "伊利"
          }
        }
      ],
      "boost": 2
    }
  }
}
{
        "_shard" : "[jd-product][0]",
        "_node" : "NRpvHk1DRc2WPrtjQOcViw",
        "_index" : "jd-product",
        "_type" : "_doc",
        "_id" : "100007539289",
        "_score" : 8.366182,
        "_source" : {
          "productName" : "伊利 纯牛奶250ml*16盒/礼盒装"
        },
        "_explanation" : {
          "value" : 8.366182,
          "description" : "weight(productName:伊利 in 219) [PerFieldSimilarity], result of:",
          "details" : [
            {
              "value" : 8.366182,
              "description" : "score(freq=1.0), computed as boost * idf * tf from:",
              "details" : [
                {
                  "value" : 4.4,
                  "description" : "boost",
                  "details" : [ ]
                },
                {
                  "value" : 3.0769577,
                  "description" : "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
                  "details" : [
                    {
                      "value" : 6,
                      "description" : "n, number of documents containing term",
                      "details" : [ ]
                    },
                    {
                      "value" : 140,
                      "description" : "N, total number of documents with field",
                      "details" : [ ]
                    }
                  ]
                },
                {
                  "value" : 0.6179496,
                  "description" : "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
                  "details" : [
                    {
                      "value" : 1.0,
                      "description" : "freq, occurrences of term within document",
                      "details" : [ ]
                    },
                    {
                      "value" : 1.2,
                      "description" : "k1, term saturation parameter",
                      "details" : [ ]
                    },
                    {
                      "value" : 0.75,
                      "description" : "b, length normalization parameter",
                      "details" : [ ]
                    },
                    {
                      "value" : 11.0,
                      "description" : "dl, length of field",
                      "details" : [ ]
                    },
                    {
                      "value" : 31.107143,
                      "description" : "avgdl, average length of field",
                      "details" : [ ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
```

## 复合查询

### [bool query(布尔查询)](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html)

`bool query`可以组合任意多个简单查询，各个简单查询之间的逻辑表示如下：

| 属性     | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| must     | 文档必须匹配 must 选项下的查询条件，相当于逻辑运算的 AND     |
| should   | 文档可以匹配 should 选项下的查询条件，也可以不匹配，相当于逻辑运算的 OR |
| must_not | 与 must 相反，匹配该选项下的查询条件的文档不会被返回         |
| filter   | 和 must 一样，匹配 filter 选项下的查询条件的文档才会被返回，但是 filter 不评分，只起到过滤功能 |

#### 修改特定品牌权重

```
GET jd-product/_search
{
  "_source": [
    "productName",
    "shopName"
  ],
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "productName": "牛奶"
          }
        }
      ],
      "should": [
        {
          "match": {
            "shopName": {
              "query": "蒙牛",
              "boost": 2
            }
          }
        },
        {
          "match": {
            "shopName": {
              "query": "伊利",
              "boost": 1
            }
          }
        }
      ],
      "minimum_should_match": 0
    }
  }
}
```

### [`boosting query`(提高查询)](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-boosting-query.html)

> Return documents which match a query, but reduce the score of documents which also match a query.
>
> 返回匹配的文档，但是减少一些文档的分数

```json
GET jd-product/_search
{
  "_source": [
    "productName",
    "shopName"
  ],
  "query": {
    "boosting": {
      "positive": {
        "match": {
          "productName": "牛奶"
        }
      },
      "negative": {
        "bool": {
          "must_not": [
            {
              "terms": {
                "shopName.keyword": [
                  "伊利牛奶京东自营旗舰店",
                  "蒙牛京东自营旗舰店"
                ]
              }
            }
          ]
        }
      },
      "negative_boost": 0.8
    }
  }
}
```

### [`constant_score`（固定分数查询）](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-constant-score-query.html)

> A query which wraps another query, but executes it in filter context. All matching documents are given the same “constant” . `_score`
>
> 在filter查询中，所以匹配的文档返回相同的分数

```
GET jd-product/_search
{
  "explain": true, 
  "_source": [
    "productName",
    "shopName"
  ],
  "query": {
    "bool": {
      "must": [
        {
          "constant_score": {
            "filter": {
              "match": {
                "productName": "牛奶"
              }
            },
            "boost": 2
          }
        }
      ],
      "should": [
        {
          "constant_score": {
            "filter": {
              "match": {
                "shopName": {
                  "query": "蒙牛"
                }
              }
            },
            "boost": 1.2
          }
        },
        {
          "constant_score": {
            "filter": {
              "match": {
                "shopName": {
                  "query": "伊利"
                }
              }
            },
            "boost": 1
          }
        }
      ],
      "minimum_should_match": 0
    }
  }
}
```

### [function_score(函数分）](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html)

>  The `function_score` query provides several types of score functions.
>
> `function_score`查询提供下面几种`score functions`

#### `weight` 

对每份文档适用一个简单的提升，且该提升不会被归约：当weight为2时，结果为2 * _score。

#### `field_value_factor` 

> The `field_value_factor` function allows you to use a field from a document to influence the score. It’s similar to using the `script_score` function, however, it avoids the overhead of scripting
>
> `field_value_factor`函数使用文档中的字段的值来计算分数,和`script_score`函数类似，但是避免了脚本的开销。
>
> ```
> GET jd-product/_search
> {
>   "query": {
>     "function_score": {
>       "query": {
>         "match": {
>           "productName": "牛奶"
>         }
>       },
>       "field_value_factor": {
>         "field": "price",
>         "factor": 1.2,
>         "modifier": "sqrt",
>         "missing": 1
>       }
>     }
>   }
> ```
>
> 将转换为下面的评分方式
>
> `sqrt(1.2 * doc['my-int'].value)`
>
> | field_value_factor字段 | 描述                                                         |
> | ---------------------- | ------------------------------------------------------------ |
> | `field`                | 要从文档中提取的字段。                                       |
> | `factor`               | 可选因子将字段值乘以默认到 。`1`                             |
> | `modifier`             | `none`,`log`,`log1p`,`log2p`,`ln`,`ln1p`,`ln2p`,`square`,`sqrt`,`reciprocal`,`none` |



#### `random_score` 

使用一致性随机分值计算来对每个用户采用不同的结果排序方式，对相同用户仍然使用相同的排序方式。

#### [Decay functions衰减](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html#function-decay)

> Decay functions score a document with a function that decays depending on the distance of a numeric field value of the document from a user given origin. This is similar to a range query, but with smooth edges instead of boxes.
>
> 衰变函数对具有衰变函数的文档进行评分，该函数会根据文档从给定源源的文档数场值的距离进行衰变。这类似于范围查询，但边缘平滑，而不是框。
>
> The `DECAY_FUNCTION` should be one of `linear`, `exp`, or `gauss`
>
> The specified field must be a numeric, date, or geopoint field.
>
> `DECAY_FUNCTION`函数是`linear`, `exp`或者 `gauss`的一种
> 字段类型必须是numeric, date或者geopoint

![](./img/decay_2d.png)

>
> | `origin` | 用于计算距离的原点。必须给出数字字段的编号、日期字段的日期和地理字段的地理点。地理和数字字段所必需。对于日期字段，默认值为 。日期数学（例如）支持原点。`now``now-1h` |
> | -------- | ------------------------------------------------------------ |
> | `scale`  | 所有类型都需要。定义与原点的距离 = 计算分数等于参数的偏移距离。对于地理场：可定义为编号+单位（1公里，12米,...）。默认单位为仪表。对于日期字段：可以定义为数字+单位（"1h"、"10d",...）。默认单位为毫秒。对于数字字段：任何数字。`decay` |
> | `offset` | 如果定义了一个，衰变函数将只计算距离大于定义的文档的衰变函数。默认值为 0。`offset``offset` |
> | `decay`  | 参数定义了文档在给出的距离内如何评分。如果定义否，则距离中的文档将评分为 0.5。`decay``scale``decay``scale` |

script_score

使用自定义的脚本来完全控制分值计算逻辑。如果你需要以上预定义函数之外的功能，可以根据需要通过脚本进行实现

每个文档都按定义的`functions`函数进行评分。参数指定计算分数的组合方式：`score_mode`

| score_mode枚举 | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| `multiply`     | 分数乘以(scores are multiplied (default))                    |
| `sum`          | 分数相加(scores are summed)                                  |
| `avg`          | 平均分数( scores are averaged)                               |
| `first`        | 匹配的第一个函数分(the first function that has a matching filter is applied) |
| `max`          | 使用最高分(maximum score is used)                            |
| `min`          | 使用最低分(minimum score is used)                            |

参数：`boost_mode`，新计算的分数与查询的分数相结合。

| boost_mode枚举 | 描述                                 |
| -------------- | ------------------------------------ |
| `multiply`     | 查询分数和功能分数成倍增加（默认值） |
| `replace`      | 只使用函数分数，忽略查询分数         |
| `sum`          | 添加查询分数和功能分数               |
| `avg`          | 平均                                 |
| `max`          | 查询分数和函数分数的最大值           |
| `min`          | 查询分数和功能分数的分钟数           |

```json
GET jd-product/_search
{
  "query": {
    "function_score": {
      "query": {
        "bool": {
          "filter": [
            {
              "match": {
                "productName": "牛奶"
              }
            }
          ]
        }
      },
      "functions": [
        {
          "filter": {
            "match": {
              "productName": "纯牛奶"
            }
          },
          "weight": 3
        },
        {
          "filter": {
            "terms": {
              "shopName.keyword": [
                "伊利牛奶京东自营旗舰店",
                "蒙牛京东自营旗舰店"
              ]
            }
          },
          "weight": 2
        }
      ],
      "score_mode": "sum",
      "boost_mode": "sum"
    }
  }
}
```

