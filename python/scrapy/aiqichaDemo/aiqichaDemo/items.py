# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AiqichademoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    companyName = scrapy.Field()
    # 公司电话
    companyPhone = scrapy.Field()
    # 公司邮箱
    companyEmail = scrapy.Field()
    # 官网
    officialWebsite = scrapy.Field()
    # 公司地址
    companyAddress = scrapy.Field()
    # 公司简介
    companyProfile = scrapy.Field()
    # 工商注册
    businessRegistration= scrapy.Field()
    pass
