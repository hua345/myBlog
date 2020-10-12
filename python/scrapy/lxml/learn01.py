from lxml import etree
html = etree.parse('hello.html',etree.HTMLParser())
print(etree.tostring(html))
# 获取所有book标签
print(html.xpath('//book'))
# 根据属性获取所有book标签
print(html.xpath('//book[@category="web"]/price/text()'))
print(html.xpath('//bookstore//price/text()'))
