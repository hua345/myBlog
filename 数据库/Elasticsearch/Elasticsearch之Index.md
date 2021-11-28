[TOC]

## 参考

[Index modules](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html)

## 1.创建索引

- [date](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html)
- [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
- [number](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html)

`POST book_index`

```json
{
  "mappings": {
    "properties": {
      "bookId": {
        "type": "long"
      },
      "bookName": {
        "type": "text"
      },
      "bookDate": {
        "type": "date"
      }
    }
  }
}
```

## 2.索引设置

### 静态索引设置

**`index.number_of_shards`**

> The number of primary shards that an index should have. Defaults to `1`. This setting can only be set at index creation time. 

### 动态索引设置

**`index.number_of_replicas`**

> The number of replicas each primary shard has. Defaults to 1.
>
> ```console
> PUT /my-index-000001/_settings
> {
>   "index" : {
>     "number_of_replicas" : 2
>   }
> }
> ```

**`index.refresh_interval`**

> How often to perform a refresh operation, which makes recent changes to the index visible to search. Defaults to `1s`. Can be set to `-1` to disable refresh. 
>
> 执行刷新操作的频率，这使得最近的数据被搜索到

**`index.max_result_window`**

> The maximum value of `from + size` for searches to this index. Defaults to `10000`. Search requests take heap memory and time proportional to `from + size` and this limits that memory. 
>
> 搜索时`from + size`最大的数量,默认是`10000`。

```json
{
  "index.search.slowlog.level": "info",
  "index.search.slowlog.threshold.fetch.warn": "200ms",
  "index.search.slowlog.threshold.fetch.trace": "50ms",
  "index.search.slowlog.threshold.fetch.debug": "80ms",
  "index.search.slowlog.threshold.fetch.info": "100ms",
  "index.search.slowlog.threshold.query.warn": "500ms",
  "index.search.slowlog.threshold.query.trace": "50ms",
  "index.search.slowlog.threshold.query.debug": "100ms",
  "index.search.slowlog.threshold.query.info": "200ms",
  "index.refresh_interval": "10s",
  "index.max_result_window": "10000",
  "index.number_of_replicas": "1"
}
```



## 新增ES文档

```
POST book_index2/_doc/1
{
	"bookName":"刻意练习"
}
```



## 修改 Index 类型

### 新建新的 Index

`PUT book_index2`

```json
PUT book_index2
{
  "mappings": {
    "properties": {
      "bookName": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "bookDate": {
        "type": "date",
        "format": "strict_date_optional_time||yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
      }
    }
  }
}
```

### [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/7.8/docs-reindex.html)复制数据

```json
POST _reindex
{
  "source": {
    "index": "book_index"
  },
  "dest": {
    "index": "book_index2"
  }
}
```
