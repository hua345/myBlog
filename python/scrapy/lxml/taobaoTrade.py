from lxml import etree
html = etree.parse('taobaoTrade.html', etree.HTMLParser(encoding="utf-8"))

print(html.xpath('//div[@id="tp-bought-root"]'))
print(html.xpath('//div[@id="tp-bought-root"]//div[contains(@class, "js-order-container")]'))
tradeList = html.xpath('//div[@id="tp-bought-root"]//div[contains(@class, "js-order-container")]')

print(tradeList[0].xpath(
    './/td[@class="bought-wrapper-mod__head-info-cell___29cDO"]/span[last()]/span[last()]//text()'))
print(tradeList[0].xpath(
    './/div[contains(@class,"suborder-mod__production___3WebF")]/div[last()]/p[1]/a/span[2]//text()'))
print(tradeList[0].xpath(
    './/div[@class="bought-wrapper-mod__seller-container___3dAK3"]/span/a//text()'))
print(tradeList[0].xpath(
    './/div[@class="price-mod__price___cYafX"]/p/strong/span[last()]//text()'))