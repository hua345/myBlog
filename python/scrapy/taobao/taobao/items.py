# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    shop = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    pass

class TaobaoAddressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    mobile = scrapy.Field()
    area = scrapy.Field()
    detail_area = scrapy.Field()
    youbian = scrapy.Field()
    pass

class TaobaoTradeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tradeId = scrapy.Field()
    prouductInfo = scrapy.Field()
    shop = scrapy.Field()
    prouductPrice = scrapy.Field()
    pass
