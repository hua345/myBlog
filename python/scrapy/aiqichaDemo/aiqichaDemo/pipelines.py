# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
import codecs
import json
import os
import codecs


class AiqichademoPipeline:
    def __init__(self):
        super().__init__()  # 执行父类的构造方法
        today = time.strftime('%Y-%m-%d', time.localtime())
        self.fp = codecs.open('scraped_data'+today +
                              '.json', 'w', encoding='utf-8')
        self.fp.write('[')

    def process_item(self, item, spider):
        # 将item转为字典
        d = dict(item)
        # 将字典转为json格式
        string = json.dumps(d, ensure_ascii=False)
        self.fp.write(string + ',\n')  # 每行数据之后加入逗号和换行
        return item

    def close_spider(self, spider):
        self.fp.seek(-2, os.SEEK_END)  # 定位到倒数第二个字符，即最后一个逗号
        self.fp.truncate()  # 删除最后一个逗号
        self.fp.write(']')  # 文件末尾加入一个‘]’
        self.fp.close()   # 关闭文件
