[TOC]

# ES索引重建

## [修改已经存在字段类型](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html#updating-field-mappings)

另外一种是字段已经存在，这种情况下，`ES` 是不允许直接修改字段的类型的，因为 ES 是根据 `Lucene` 实现的倒排索引，一旦生成后就不允许修改，如果希望改变字段类型，必须使用`_reindex`重建索引。



```yaml
# 备份索引
POST /_reindex
{
  "source": {
    "index": "jd-product"
  },
  "dest": {
    "index": "jd-product-bak"
  }
}
# 删除索引
DELETE jd-product
```



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

