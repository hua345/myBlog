[TOC]

## 参考

- [Mapping parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-params.html)

# mapping

## 1.字段类型

### 1.1 字符串类型

- [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
- [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)

在 ES 7.x 有两种字符串类型：`text`和`keyword`

> `text` fields are best suited for unstructured but human-readable content. If you need to index unstructured machine-generated content, see [Mapping unstructured content](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html#mapping-unstructured-content).
>
> If you need to index structured content such as email addresses, hostnames, status codes, or tags, it is likely that you should rather use a [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) field.
>
> `text` fields are searchable by default, but by default are not available for aggregations, sorting, or scripting.  If you try to sort, aggregate, or access values from a script on a `text` field, you will see this exception:
>
> Fielddata is disabled on text fields by default. Set `fielddata=true` on `your_field_name` in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory.
>
> `text` 类型适用于非结构化人类可读的内容，如果是机器生成的非结构化内容可以看[Mapping unstructured content](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html#mapping-unstructured-content).
>
> `keyword` 适合简短、结构化字符串，例如姓名、商品名称等，可以用于过滤、排序、聚合检索，也可以用于精确查询。
>
> `text` 类型字段默认是可以搜索的,`text` 类型会被 `Lucene` 分词器`Analyzer`处理为一个个词项，并使用 `Lucene` 倒排索引存储。但是不能被用于聚合、排序和脚本。如果尝试聚合、排序和脚本一个`text`类型字段，会有下面的异常:
>
> `text`类型是默认禁止`Fielddata `，设置 `fielddata=true`可以取消倒排索引加载字段数据到内存中。(请注意，这可能会占用大量内存)

> ### [Before enabling fielddata]([Text type family | Elasticsearch Guide [7.15\] | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html#before-enabling-fielddata))
>
> It usually doesn’t make sense to enable fielddata on text fields. Field data is stored in the heap with the [field data cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-fielddata.html) because it is expensive to calculate. Calculating the field data can cause latency spikes, and increasing heap usage is a cause of cluster performance issues.
>
> Most users who want to do more with text fields use [multi-field mappings](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html) by having both a `text` field for full text searches, and an unanalyzed [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) field for aggregations, as follows:
>
> 在`text`字段上启用`fielddata`通常没有意义。字段数据与字段数据缓存一起存储在堆中，因为计算成本很高。计算字段数据可能会导致延迟峰值，而堆使用率的增加是集群性能问题的一个原因。
> 大多数希望对`text`字段进行更多操作的用户都使用[multi-field mappings](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html) ，包括用于全文搜索的文本字段和用于聚合的未分析[`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) 字段，如下所示：
>
> ```
> PUT my-index-000001
> {
>   "mappings": {
>     "properties": {
>       "my_field": { 
>         "type": "text",
>         "fields": {
>           "keyword": { 
>             "type": "keyword"
>           }
>         }
>       }
>     }
>   }
> }
> ```
>
> - 用`my_field`字段进行搜索
>- 用`my_field.keyword`字段进行聚合、排序和脚本处理

### 1.2[number](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html)

数字类型分为 `long、integer、short、byte、double、float、half_float、scaled_floa`t。

数字类型的字段在满足需求的前提下应当尽量选择范围较小的数据类型，字段长度越短，搜索效率越高，对于浮点数，可以优先考虑使用 `scaled_float` 类型，该类型可以通过缩放因子来精确浮点数，例如输入 `12.34` 可以转换为 `1234` 存储到ES中。

```json
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "number_of_bytes": {
        "type": "integer"
      },
      "price": {
        "type": "scaled_float",
        "scaling_factor": 100
      }
    }
  }
}
```

### 1.3[date](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html)

在 es 内部，`date`被转为 UTC，并被存储为时间戳，代表从`1970年1月1号0点`到现在的毫秒数

`date`格式可以在 put mapping 的时候用 `format` 参数指定，如果不指定的话，则启用默认格式，是`strict_date_optional_time||epoch_millis`。这表明只接受符合`strict_date_optional_time`格式的字符串值，或者`long`型数字。

支持`yyyy-MM-dd`、`yyyyMMdd`、`yyyyMMddHHmmss`、`yyyy-MM-ddTHH:mm:ss`、`yyyy-MM-ddTHH:mm:ss.SSS"`格式

如果保存`yyyy-MM-dd HH:mm:ss`格式,需要设置`format`格式`"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"`

```json
PUT book_index
{
  "mappings": {
    "properties": {
      "book_name": {
        "type": "keyword"
      },
      "book_date": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      }
    }
  }
}
```

### 1.4[boolean 类型](https://www.elastic.co/guide/en/elasticsearch/reference/current/boolean.html)

`ES`接收 json 中布尔类型`true`or`false`,也接受字符串类型`"true"`or`"false"`,布尔类型常用于检索中的过滤条件。

### 1.5[binary 类型](https://www.elastic.co/guide/en/elasticsearch/reference/current/binary.html)

二进制类型 `binary` 接受 `BASE64` 编码的字符串，默认 store 属性为 false，并且不可以被搜索。

### 1.6[object 类型](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html)

`JSON` 字符串允许嵌套对象，一个文档可以嵌套多个、多层对象。可以通过对象类型来存储二级文档，不过由于`Lucene`并没有内部对象的概念，ES 会将原 `JSON` 文档扁平化

```json
PUT my-index-000001/_doc/1
{
  "region": "US",
  "manager": {
    "age": 30,
    "name": {
      "first": "John",
      "last": "Smith"
    }
  }
}
```

实际上 ES 会将其转换为以下格式，并通过 Lucene 存储，即使 name 是 object 类型

```json
{
  "region": "US",
  "manager.age": 30,
  "manager.name.first": "John",
  "manager.name.last": "Smith"
}
```

## 2.[Dynamic Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic-mapping.html)

`Dynamic Mapping` 机制使我们不需要手动定义 `Mapping`，`ES` 会自动根据文档信息来判断字段合适的类型，但是有时候也会推算的不对，比如地理位置信息有可能会判断为 `Text`

`date`类型推断需要`[ "strict_date_optional_time","yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"]`类型字符串

## 3.[修改 Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html)

### 3.1 动态新增字段类型

如果是新增加的字段，根据 [`dynamic`](https://www.elastic.co/guide/en/elasticsearch/reference/current/dynamic.html) 的设置分为以下三种状况

- `dynamic` 默认为 `true` ，一旦有新增字段的文档写入，`mapping`也同时被更新。
- 当 `dynamic` 设置为 `false` 时，索引的`mapping`是不会被更新的，新增字段的数据无法被索引，也就是无法被搜索，但是信息会出现在`_source`中返回。
- 当 `dynamic` 设置为 `strict` 时，文档写入会失败。

### 3.2 修改`mapping`中`dynamic`参数

```json
PUT my-index-000001/_mapping
{
  "dynamic":false
}
```

### 3.3[手动新增字段](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html)

```json
PUT /my-index-000001/_mapping
{
  "properties": {
    "email": {
      "type": "keyword"
    }
  }
}
```

### 3.4 [修改已经存在字段类型](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html#updating-field-mappings)

另外一种是字段已经存在，这种情况下，`ES` 是不允许直接修改字段的类型的，因为 ES 是根据 `Lucene` 实现的倒排索引，一旦生成后就不允许修改，如果希望改变字段类型，必须使用`_reindex`重建索引。

```yml
# 创建索引
PUT /my-index-000001
{
  "mappings" : {
    "properties": {
      "user_id": {
        "type": "long"
      }
    }
  }
}

# 推送一条数据
POST /my-index-000001/_doc
{
  "user_id" : 12345
}

# 创建新的索引
PUT /my-index-000002
{
  "mappings" : {
    "properties": {
      "user_id": {
        "type": "keyword"
      }
    }
  }
}

# 复制数据
POST /_reindex
{
  "source": {
    "index": "my-index-000001"
  },
  "dest": {
    "index": "my-index-000002"
  }
}
```

### 3.5[重命名`mapping`字段](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html#rename-existing-field)

可以创建昵称字段`user_id`来重命名已经存在的字段`user_identifier`

```yml
# 删除测试索引
DELETE my-index-000002
# 创建索引
PUT /my-index-000002
{
  "mappings": {
    "properties": {
      "user_identifier": {
        "type": "keyword"
      }
    }
  }
}

# 创建昵称字段
PUT /my-index-000001/_mapping
{
  "properties": {
    "my_user_id": {
      "type": "alias",
      "path": "user_id"
    }
  }
}

# 查看mapping
GET my-index-000002/_mapping
{
  "my-index-000002" : {
    "mappings" : {
      "properties" : {
        "user_id" : {
          "type" : "alias",
          "path" : "user_identifier"
        },
        "user_identifier" : {
          "type" : "keyword"
        }
      }
    }
  }
}
```



