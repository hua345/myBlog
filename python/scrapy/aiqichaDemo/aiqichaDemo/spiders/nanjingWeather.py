# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options    # 使用无头浏览器
from aiqichaDemo.items import AiqichademoItem

# 无头浏览器设置
chrome_options = Options()
chrome_options.add_argument('headless') 
chrome_options.add_argument('--no-sandbox') 
chrome_options.add_argument('--disable-gpu')

class nanjingweatherSpider(scrapy.Spider):
    name = 'aiqichaDemo'
    start_urls = ['https://aiqicha.baidu.com/company_detail_28676206903744']

    # 实例化一个浏览器对象
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        super().__init__()
        # 整个爬虫结束后关闭浏览器

    def close(self, spider):
        self.browser.quit()

    def start_requests(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        yield scrapy.Request(self.start_urls[0], callback=self.parse, headers=headers)

    def parse(self, response):
        items = []
        item = AiqichademoItem()
        companyHeader = response.xpath('//div[@class="header-content"]')
        companyName = companyHeader.xpath(
            './/h2[@class="name"]/text()').extract()
        companyPhone = companyHeader.xpath(
            './/div[@class="content-info-child"][1]/p[1]/span/text()').extract()
        companyEmail = companyHeader.xpath(
            './/div[@class="content-info-child"][1]/p[2]/span/text()').extract()
        officialWebsite = companyHeader.xpath(
            './/div[@class="content-info-child"][2]/p[1]/a/text()').extract()
        companyAddress = companyHeader.xpath(
            './/div[@class="content-info-child"][2]/p[2]/span/text()').extract()
        companyProfile = companyHeader.xpath(
            './/div[@class="content-info-child-brief"]/div/text()').extract()
        item["companyName"] = companyName
        item["companyPhone"] = companyPhone
        item["companyEmail"] = companyEmail
        item["officialWebsite"] = officialWebsite
        item["companyAddress"] = companyAddress
        item["companyProfile"] = companyProfile
        # 工商注册信息
        basicBusiness = response.xpath('//div[@id="basic-business"]')
        # 法定代表人
        legalRepresentative = basicBusiness.xpath(
            './/div[@class="title portrait-text"]/a[1]/text()').extract_first().replace('\n', '').strip()
        # 经营状态
        operatingStatus = basicBusiness.xpath(
            './/tr[1]/td[last()]/text()').extract_first().strip()
        # 注册资本
        registeredCapital = basicBusiness.xpath(
            './/tr[2]/td[2]/text()').extract_first().strip()
        # 实缴资本
        paidInCapital = basicBusiness.xpath(
            './/tr[2]/td[last()]/text()').extract_first().strip()
        # 所属行业
        industry = basicBusiness.xpath(
            './/tr[3]/td[last()]/text()').extract_first().strip()
        # 统一社会信用代码
        socialCreditCode = basicBusiness.xpath(
            './/tr[4]/td[2]/text()').extract_first().strip()
        # 纳税人识别号
        taxpayerIdentificationNumber = basicBusiness.xpath(
            './/tr[4]/td[last()]/text()').extract_first().strip()
        # 工商注册号
        businessRegistrationNumber = basicBusiness.xpath(
            './/tr[5]/td[2]/text()').extract_first().strip()
        # 组织机构代码
        organizationCode = basicBusiness.xpath(
            './/tr[5]/td[last()]/text()').extract_first().strip()
        # 登记机关
        registrationAuthority = basicBusiness.xpath(
            './/tr[6]/td[2]/text()').extract_first().strip()
        # 成立日期
        establishmentDate = basicBusiness.xpath(
            './/tr[6]/td[last()]/text()').extract_first().strip()
        # 企业类型
        enterpriseType = basicBusiness.xpath(
            './/tr[7]/td[2]/text()').extract_first().strip()
        # 营业期限
        operatingPeriod = basicBusiness.xpath(
            './/tr[7]/td[last()]/text()').extract_first().strip()
        # 行政区划
        administrativeDivisions = basicBusiness.xpath(
            './/tr[8]/td[2]/text()').extract_first().strip()
        # 审核/年检日期
        annualInspectionDate = basicBusiness.xpath(
            './/tr[8]/td[last()]/text()').extract_first().strip()
        # 注册地址
        registeredAddress = basicBusiness.xpath(
            './/tr[9]/td[2]/text()').extract_first().strip()
        # 经营范围
        businessScope = basicBusiness.xpath(
            './/tr[10]/td[last()]/div/text()').extract_first().strip()

        item["businessRegistration"] = {}
        # 法定代表人
        item["businessRegistration"]["legalRepresentative"] = legalRepresentative
        # 经营状态
        item["businessRegistration"]["operatingStatus"] = operatingStatus
        # 注册资本
        item["businessRegistration"]["registeredCapital"] = registeredCapital
        # 实缴资本
        item["businessRegistration"]["paidInCapital"] = paidInCapital
        # 所属行业
        item["businessRegistration"]["industry"] = industry
        # 统一社会信用代码
        item["businessRegistration"]["socialCreditCode"] = socialCreditCode
        # 纳税人识别号
        item["businessRegistration"]["taxpayerIdentificationNumber"] = taxpayerIdentificationNumber
        # 工商注册号
        item["businessRegistration"]["businessRegistrationNumber"] = businessRegistrationNumber
        # 组织机构代码
        item["businessRegistration"]["organizationCode"] = organizationCode
        # 登记机关
        item["businessRegistration"]["registrationAuthority"] = registrationAuthority
        # 成立日期
        item["businessRegistration"]["establishmentDate"] = establishmentDate
        # 企业类型
        item["businessRegistration"]["enterpriseType"] = enterpriseType
        # 营业期限
        item["businessRegistration"]["operatingPeriod"] = operatingPeriod
        # 行政区划
        item["businessRegistration"]["administrativeDivisions"] = administrativeDivisions
        # 审核/年检日期
        item["businessRegistration"]["annualInspectionDate"] = annualInspectionDate
        # 注册地址
        item["businessRegistration"]["registeredAddress"] = registeredAddress
        # 经营范围
        item["businessRegistration"]["businessScope"] = businessScope

        items.append(item)
        return items
        pass
