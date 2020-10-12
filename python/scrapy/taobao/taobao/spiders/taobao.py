# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote

from taobao.items import TaobaoProductItem
from taobao.items import TaobaoAddressItem
from taobao.items import TaobaoTradeItem


class taobaoSpider(scrapy.Spider):
    name = 'taobao'
    taobao_username = "淘宝账号"  # 改成你的淘宝账号
    taobao_password = "淘宝密码"  # 改成你的淘宝密码
    productUrl = 'https://s.taobao.com/search?q='
    addressUrl = 'https://member1.taobao.com/member/fresh/deliver_address.htm'
    tradeUrl = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'
    productKeyWord = ['牛奶', '核桃']
    loginUrl = 'https://login.taobao.com/member/login.jhtml'
    # 实例化一个浏览器对象

    def __init__(self):
        # 无头浏览器设置
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(chrome_options=options)
        self.wait = WebDriverWait(self.browser, 10, 0.5)  # 超时时长为10s

    def start_requests(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        self.login()
        time.sleep(1)
        self.browser.implicitly_wait(3)
        yield scrapy.Request(url=self.tradeUrl, callback=self.parseTrade, headers=headers)
        for keyword in self.productKeyWord:
            url = self.productUrl + quote(keyword)
            yield scrapy.Request(url=url, callback=self.parseProduct, headers=headers)
        yield scrapy.Request(url=self.addressUrl, callback=self.parseAddr, headers=headers)


    def login(self):
        self.browser.implicitly_wait(3)
        # 打开网页
        self.browser.get(self.loginUrl)
        time.sleep(1)
        # 等待 淘宝账号 出现
        self.browser.find_element_by_id(
            "fm-login-id").send_keys(self.taobao_username)
        self.browser.find_element_by_id(
            "fm-login-password").send_keys(self.taobao_password)
        self.browser.find_element_by_css_selector(
            "#login-form > div.fm-btn > button").click()
        # time.sleep(1)
        self.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 's-baseinfo')))
        taobaoName = self.browser.find_element_by_xpath(
            '//div[@class="s-baseinfo"]/div[@class="s-name"]/a/em').text
        print(taobaoName)
        print(self.browser.current_url)

    # 爬取淘宝 我已买到的宝贝商品数据
    def parseTrade(self, response):
        tradeList = response.xpath(
            '//div[@id="tp-bought-root"]//div[contains(@class, "js-order-container")]')
        items = []
        for tradeItem in tradeList:
            item = TaobaoTradeItem()
            item['tradeId'] = tradeItem.xpath(
                './/td[@class="bought-wrapper-mod__head-info-cell___29cDO"]/span[last()]/span[last()]//text()').get()
            item['prouductInfo'] = tradeItem.xpath(
                './/div[contains(@class,"suborder-mod__production___3WebF")]/div[last()]/p[1]/a/span[2]//text()').get()
            item['shop'] = tradeItem.xpath(
                './/div[@class="bought-wrapper-mod__seller-container___3dAK3"]/span/a//text()').get()
            item['prouductPrice'] = tradeItem.xpath(
                './/div[@class="price-mod__price___cYafX"]/p/strong/span[last()]//text()').get()
            items.append(item)
        return items
    # 地址

    def parseAddr(self, response):
        addressList = response.xpath(
            '//tbody[@class="next-table-body"]/tr')
        items = []
        for addr in addressList:
            item = TaobaoAddressItem()
            item['name'] = addr.xpath('.//td[1]//text()').get()
            item['area'] = addr.xpath('.//td[2]//text()').get()
            item['detail_area'] = addr.xpath('.//td[3]//text()').get()
            item['youbian'] = addr.xpath('.//td[4]//text()').get()
            item['mobile'] = addr.xpath('.//td[5]//text()').get()
            items.append(item)
        return items

    def parseProduct(self, response):
        items = []
        products = response.xpath(
            '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div')
        for product in products:
            item = TaobaoProductItem()
            item['price'] = ''.join(product.xpath(
                './/div[contains(@class, "price")]//strong//text()').getall()).strip()
            item['title'] = ''.join(product.xpath(
                './/div[contains(@class, "title")]//text()').getall()).strip()
            item['shop'] = ''.join(product.xpath(
                './/div[contains(@class, "shop")]//text()').getall()).strip()
            item['link'] = product.xpath(
                './/div[contains(@class, "title")]//@href').get()
            item['id'] = product.xpath(
                './/div[contains(@class, "title")]//@id').get()
            items.append(item)
        return items
