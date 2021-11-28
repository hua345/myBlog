[TOC]

# ES脚本查询

## 参考

- [How to write scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html)
- [Painless scripting language](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-painless.html)
- [Painless Guide](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-guide.html)
- [store and retrieve scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html#script-stored-scripts)
- [Script APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/script-apis.html)
- [Using Datetime in Painless ](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-datetime.html)
- [Painless 可以用的一些类和函数 ]([https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-api-reference.html)

## [Painless脚本语言](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-painless.html)

> *Painless* is a performant, secure scripting language designed specifically for Elasticsearch.
>
> Painless是专门为Elasticsearch设计的高性能，安全的脚本语言
>
> Painless scripts are parsed and compiled using the [ANTLR4](https://www.antlr.org/) and [ASM](https://asm.ow2.org/) libraries. Scripts are compiled directly into Java Virtual Machine (JVM) byte code and executed against a standard JVM
>
> Painless直接编译成JVM字节码，以利用JVM提供的所有可能的优化。

## [脚本格式](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html#modules-scripting-using)

```
  "script": {
    "lang":   "...",
    "source" | "id": "...",
    "params": { ... }
  }
```

- **`lang`**脚本类型。默认是 `painless`
- **`source`, `id`**, `source` 为脚本字符串或者 `id` 为`stored scripts`. 使用 [stored script APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/script-apis.html#stored-script-apis) 创建和管理`stored scripts`
- **params**,传递给脚本的参数,可以减少脚本编译时间



```
PUT my-index-000001/_doc/1
{
  "my_field": 5
}
```

### 脚本示例

```
GET my-index-000001/_search
{
  "script_fields": {
    "my_doubled_field": {
      "script": { 
        "source": "doc['my_field'].value * params['multiplier']", 
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
```

### 获取文档数据

```java
//获取文档字段数据
doc['field_name'].value
// 判断是否有值
doc['field_name'].size() == 0
doc['field_name'].empty
// date类型,判断时间大小
doc['beginTime'].value.isBefore(doc['endTime'].value);
// date类型,判断时间大小
doc['aaTime'].value.toInstant().toEpochMilli() > doc['bbTime'].value.toInstant().toEpochMilli()

```



## [Painless参数](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html#prefer-params)

> The first time Elasticsearch sees a new script, it compiles the script and stores the compiled version in a cache. Compilation can be a heavy process. Rather than hard-coding values in your script, pass them as named `params` instead.
>
> Elasticsearch执行一个新的脚本的时候，会编译和存储在缓存中。编译是一个比较慢的过程，与其在脚本中硬编码值，不如将它们作为`params`传递。
>
> ```painless
> "source": "return doc['my_field'].value * 2"
> ```
>
> 虽然它是有效的，但这个解决方案是相当死板的。我们必须修改脚本源以更改乘数，而Elasticsearch必须在每次乘数更改时重新编译脚本。
>
> Instead of hard-coding values, use named `params` to make scripts flexible, and also reduce compilation time when the script runs. You can now make changes to the `multiplier` parameter without Elasticsearch recompiling the script.
>
> 不要硬编码值，而是使用`params`使脚本灵活，并在脚本运行时减少编译时间。您现在可以更改乘数参数，而无需Elasticsearch重新编译脚本。
>
> ```painless
> "source": "doc['my_field'].value * params['multiplier']",
> "params": {
>   "multiplier": 2
> }
> ```
>
> 虽然它是有效的，但这个解决方案是相当死板的。

> For most contexts, you can compile up to 75 scripts per 5 minutes by default. 
>
> 默认5分钟内最多编译75个不同脚本
>
> If you compile too many unique scripts within a short time, Elasticsearch rejects the new dynamic scripts with a `circuit_breaking_exception` error.
>
> 如果短时间编译大量不同的脚本,Elasticsearch会报`circuit_breaking_exception`错误

## 脚本调试

```
POST /my-index-000001/_explain/1
{
  "query": {
    "script": {
      "script": "Debug.explain(doc['my_field'])"
    }
  }
}
```

可以获取到字段具体类型

    "painless_class" : "org.elasticsearch.index.fielddata.ScriptDocValues.Longs",
    "java_class" : "org.elasticsearch.index.fielddata.ScriptDocValues$Longs"

通过字段类型查询[Shared API ](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-api-reference-shared.html)有哪些方法

## 预编译脚本

> You can store and retrieve scripts from the cluster state using the [stored script APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/script-apis.html#stored-script-apis). Stored scripts reduce compilation time and make searches faster.
>
> 预编译脚本减少编译时间使搜索更快

### 创建预编译脚本

`PUT _scripts/<script-id>`

```
POST _scripts/multiplier
{
  "script": {
    "lang": "painless",
    "source": "doc['my_field'].value * params['multiplier']"
  }
}
```

### 查询预编译脚本

`GET _scripts/<script-id>`

`DELETE _scripts/<script-id>`删除预编译脚本

```
GET _scripts/multiplier
```

### 使用预编译脚本

```
GET my-index-000001/_search
{
  "script_fields": {
    "my_doubled_field": {
      "script": { 
        "id": "multiplier", 
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
```

## 脚本修改文档

直接修改文档

```
PUT my-index-000001/_doc/1
{
  "my_field" : 5,
  "tags" : ["red"]
}
```

修改字段值

```
POST my-index-000001/_update/1
{
  "script" : {
    "source": "ctx._source.my_field += params.count",
    "params" : {
      "count" : 2
    }
  }
}
POST jd-product/_update_by_query
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "productName": "牛奶"
          }
        },
        {
          "term": {
            "price": {
              "value": "59.90"
            }
          }
        }
      ]
      
    }
  },
  "script": {
    "source": "ctx._source['price']= null"
  }
}
```

列表添加数据

```
POST my-index-000001/_update/1
{
  "script": {
    "source": "ctx._source.tags.add(params['tag'])",
    "lang": "painless",
    "params": {
      "tag": "blue"
    }
  }
}
```

列表移除数据

```
POST my-index-000001/_update/1
{
  "script": {
    "source": "if (ctx._source.tags.contains(params['tag'])) { ctx._source.tags.remove(ctx._source.tags.indexOf(params['tag'])) }",
    "lang": "painless",
    "params": {
      "tag": "blue"
    }
  }
}
```

## 获取支持的脚本语言列表

```console
GET _script_language
{
  "types_allowed" : [
    "inline",
    "stored"
  ],
  "language_contexts" : [
    {
      "language" : "expression",
      "contexts" : [
        "aggregation_selector",
        "aggs",
        "bucket_aggregation",
        "field",
        "filter",
        "number_sort",
        "score",
        "terms_set"
      ]
    },
    {
      "language" : "mustache",
      "contexts" : [
        "ingest_template",
        "template"
      ]
    },
    {
      "language" : "painless",
      "contexts" : [
        "aggregation_selector",
        "aggs",
        "aggs_combine",
        "aggs_init",
        "aggs_map",
        "aggs_reduce",
        "analysis",
        "boolean_field",
        "bucket_aggregation",
        "date_field",
        "double_field",
        "field",
        "filter",
        "geo_point_field",
        "ingest",
        "ingest_template",
        "interval",
        "ip_field",
        "keyword_field",
        "long_field",
        "moving-function",
        "number_sort",
        "painless_test",
        "processor_conditional",
        "score",
        "script_heuristic",
        "similarity",
        "similarity_weight",
        "string_sort",
        "template",
        "terms_set",
        "update",
        "watcher_condition",
        "watcher_transform",
        "xpack_template"
      ]
    }
  ]
}
```

