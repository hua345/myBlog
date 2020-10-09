# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
import codecs


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
