# es搜索原理

- [query_phase](https://www.elastic.co/guide/en/elasticsearch/guide/current/_query_phase.html)
- [fetch_phase](https://www.elastic.co/guide/en/elasticsearch/guide/current/_fetch_phase.html)
- [Refresh API ](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-refresh.html)
- [Near real-time search](https://www.elastic.co/guide/en/elasticsearch/reference/current/near-real-time.html)

## 近实时搜索

![](./img/lucene-written-not-committed.png)

![](./img/lucene-in-memory-buffer.png)

## 查询阶段

在初始查询阶段，查询将广播到索引中每个分片的分片副本（主或副本分片）。每个分片在本地执行搜索，并建立一个匹配文档的优先级队列。

### 优先队列

一个优先级队列仅仅是持有排序列表前 N 个匹配的文件。优先级队列的大小取决于分页参数 `from` 和 `size`。例如，以下搜索请求将需要一个足以容纳 `100` 个文档的优先级队列：

```json
GET / _search
{ "from": 90, "size": 10 }
```

![es_query01](./img/es_query01.png)

## 深度分页

`query-then-fetch`流程支持使用`from`和`size` 参数分页，但限制在范围内。请记住，每个分片必须建立一个长度为优先级的队列`from + size`，所有这些队列都必须传递回协调节点。并且协调节点需要对 `number_of_shards * (from + size)`文档进行排序以找到正确的 `size`文档。

根据文档的大小，分片的数量以及所使用的硬件，完全可以分页`10,000`到`50,000`个结果（1,000到5,000页）。`但是使用足够大的from值，使用大量的CPU，内存和带宽`，排序过程的确会变得非常繁重。因此，我们`强烈建议您不要进行深度分页`。

实际上，`深度分页`很少是人类。人类将在两三页后停止分页，并将更改搜索条件。罪魁祸首通常是僵尸程序或网络蜘蛛，他们不知疲倦地不断一页一页地获取信息，直到您的服务器崩溃为止。

如果您确实需要从集群中获取大量文档，则可以通过没有排序的`scroll query`
