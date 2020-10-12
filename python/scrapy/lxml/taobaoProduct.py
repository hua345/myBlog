from lxml import etree
html = etree.parse('taobaoProduct.html', etree.HTMLParser(encoding="utf-8"))

print(html.xpath('//div[@id="mainsrp-itemlist"]'))
print(html.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div'))

obj_list = html.xpath(
    '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div')

print(html.xpath(
    '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div[1]//div[@class="price g_price g_price-highlight"]/strong/text()'))
print(html.xpath(
    '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div[1]//div[@class="row row-2 title"]/a/text()'))
print(html.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div[1]//div[@class="row row-2 title"]/a')
      [0].xpath('string(.)').replace('\n', '').strip())
print(html.xpath(
    '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]/div[1]//div[@class="shop"]/a/span[last()]/text()'))

data_list = []
for obj in obj_list:
    item = {}
    item['price'] = obj.xpath(
        './/div[@class="price g_price g_price-highlight"]/strong/text()')[0]
    item['title'] = obj.xpath(
        './/div[@class="row row-2 title"]/a')[0].xpath('string(.)').replace('\n', '').strip()
    item['shop'] = obj.xpath(
        './/div[@class="shop"]/a/span[last()]/text()')[0]
    print(item)
