# scrapy

- [https://github.com/scrapy/scrapy](https://github.com/scrapy/scrapy)
- [https://scrapy.org/](https://scrapy.org/)
- [https://github.com/marchtea/scrapy_doc_chs](https://github.com/marchtea/scrapy_doc_chs)

## scrapy安装

```bash
pip3 install scrapy
```

## 创建项目

```bash
PS F:\Code\dockerBlog\python> scrapy startproject helloworld
New Scrapy project 'helloworld', using template directory 'd:\program file\python\lib\site-packages\scrapy\templates\project', created in:
    F:\Code\dockerBlog\python\helloworld

You can start your first spider with:
    cd helloworld
    scrapy genspider example example.com
```

## 爬取天气

### 编辑`spiders/nanjingWeather.py`

```py
# -*- coding: utf-8 -*-
import scrapy
from helloworld.items import HelloworldItem

class nanjingweatherSpider(scrapy.Spider):
    name = 'helloworld'
    allowed_domains = ['http://www.tianqi.com/nanjing/']
    start_urls = ['http://www.tianqi.com/nanjing/']

    def start_requests(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        yield scrapy.Request(self.start_urls[0], callback=self.parse, headers=headers)

    def parse(self, response):
        items = []
        city = response.xpath('//dd[@class="name"]/h2/text()').extract()
        selector = response.xpath('//div[@class="day7"]')
        date = selector.xpath('ul[@class="week"]/li/b/text()').extract()
        week = selector.xpath('ul[@class="week"]/li/span/text()').extract()
        wind = selector.xpath('ul[@class="txt"]/li/text()').extract()
        weather = selector.xpath('ul[@class="txt txt2"]/li/text()').extract()
        wendu1 = selector.xpath('div[@class="zxt_shuju"]/ul/li/span/text()').extract()
        wendu2 = selector.xpath('div[@class="zxt_shuju"]/ul/li/b/text()').extract()
        for i in range(7):
            item = HelloworldItem()
            try:
                item["cityDate"] = city[0] + date[i]  # 城市及日期
                item["week"] = week[i]  # 星期
                item["temperature"] = wendu1[i] + "~" + wendu2[i]  # 温度
                item["weather"] = weather[i]  # 天气
                item["wind"] = wind[i]  # 风力
                print(item)
            except IndexError as e:
                exit()
            items.append(item)
        return items
        pass
```

### 编辑`item.py`

```py
class HelloworldItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cityDate = scrapy.Field()  # 城市及日期
    week = scrapy.Field()  # 星期
    temperature = scrapy.Field()  # 温度
    weather = scrapy.Field()  # 天气
    wind = scrapy.Field()  # 风力

    pass
```

### 编辑`pipelines.py`

```py
class HelloworldPipeline:
    def process_item(self, item, spider):
        today = time.strftime('%Y-%m-%d', time.localtime())
        filename = today + '南京天气.txt'
        with codecs.open(filename,'a','utf-8') as fp:
            fp.write("%s \t %s \t %s \t %s \t %s \r\n"
                     %(item['cityDate'],
                       item['week'],
                       item['temperature'],
                       item['weather'],
                       item['wind']))
        return item
```

### 编辑`settings.py`

```conf
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'helloworld.pipelines.HelloworldPipeline': 300,
}
```

## 运行爬虫

```bash
PS F:\Code\dockerBlog\python\helloworld> scrapy.exe crawl helloworld
```
