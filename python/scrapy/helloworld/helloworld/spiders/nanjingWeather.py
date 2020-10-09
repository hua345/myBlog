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
