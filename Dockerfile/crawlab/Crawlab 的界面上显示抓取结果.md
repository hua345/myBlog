# 显示抓取结果

## 参考

- [爬虫集成](https://docs.crawlab.cn/zh/Integration/)
- [与Scrapy集成](https://docs.crawlab.cn/zh/Integration/Scrapy.html)

以下是爬虫集成的前提条件:

- 需要设置结果集；
- 需要将数据写在与 Crawlab 一个数据库中，例如 crawlab_test；
- 需要在爬虫中将结果写回指定的数据集中（CRAWLAB_COLLECTION），并且在 task_id （CRAWLAB_TASK_ID）字段上赋值。

## 集成 Scrapy

在 `settings.py` 中找到 `ITEM_PIPELINES`（dict 类型的变量），在其中添加如下内容。

```conf
ITEM_PIPELINES = {
    'crawlab.pipelines.CrawlabMongoPipeline': 888,
}
```
