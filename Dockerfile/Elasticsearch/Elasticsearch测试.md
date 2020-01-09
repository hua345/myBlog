```bash
curl -XPUT 'http://192.168.137.128:9200/twitter/_doc/1?pretty' -H 'Content-Type: application/json' -d '
{
    "user": "kimchy",
    "post_date": "2009-11-15T13:12:00",
    "message": "Trying out Elasticsearch, so far so good?"
}'

curl -XPUT 'http://192.168.137.128:9200/twitter/_doc/2?pretty' -H 'Content-Type: application/json' -d '
{
    "user": "kimchy",
    "post_date": "2009-11-15T14:12:12",
    "message": "Another tweet, will it be indexed?"
}'

curl -XPUT 'http://192.168.137.128:9200/twitter/_doc/3?pretty' -H 'Content-Type: application/json' -d '
{
    "user": "elastic",
    "post_date": "2010-01-15T01:46:38",
    "message": "Building the site, should be kewl"
}'
```

```bash
➜  ~ curl -XGET 'http://192.168.137.128:9200/twitter/_doc/1?pretty=true'
{
  "_index" : "twitter",
  "_type" : "_doc",
  "_id" : "1",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "user" : "kimchy",
    "post_date" : "2009-11-15T13:12:00",
    "message" : "Trying out Elasticsearch, so far so good?"
  }
}
curl -XGET 'http://192.168.137.128:9200/twitter/_doc/2?pretty=true'
curl -XGET 'http://192.168.137.128:9200/twitter/_doc/3?pretty=true'
```
