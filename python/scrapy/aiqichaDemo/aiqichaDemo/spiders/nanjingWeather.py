# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
import time

# 无头浏览器设置
chorme_options = Options()

class nanjingweatherSpider(scrapy.Spider):
    name = 'aiqichaDemo'
    start_urls = ['https://aiqicha.baidu.com/company_detail_28676206903744']

    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chorme_options)
        super().__init__()
        # 整个爬虫结束后关闭浏览器

    # def close(self, spider):
    #     self.browser.quit()

    def start_requests(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        yield scrapy.Request(self.start_urls[0], callback=self.parse, headers=headers)

    # 可以拦截到response响应对象(拦截下载器传递给Spider的响应对象)
    def process_response(self, request, response, spider):
        """
        三个参数:
        # request: 响应对象所对应的请求对象
        # response: 拦截到的响应对象
        # spider: 爬虫文件中对应的爬虫类 WangyiSpider 的实例对象, 可以通过这个参数拿到 WangyiSpider 中的一些属性或方法
        """
        spider.browser.implicitly_wait(3)
        spider.browser.get(url=request.url)
        time.sleep(10)     # 等待加载,  可以用显示等待来优化.
        print(spider.browser.title)
        print('helloworld')
        row_response = spider.browser.page_source
        # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
        return scrapy.http.HtmlResponse(url=spider.browser.current_url, body=row_response, encoding="utf8", request=request)

    def parse(self, response):
        print('helloworld2')
        print(response.text)
        print(response.xpath('//title/text()').extract())
        print(response.xpath('//div[@class="content-title"]/h2/text()').extract())
        pass
