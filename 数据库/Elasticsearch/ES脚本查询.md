# ES脚本查询

## 参考

- [How to write scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-using.html)
- 

```
PUT my-index-000001/_doc/1
{
  "my_field": 5
}
```

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

