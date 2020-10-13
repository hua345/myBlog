from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import time

base_url = "https://www.baidu.com/"
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10, 0.5)

driver.implicitly_wait(3)
driver.get(base_url)

# 打印页面标题 "百度一下，你就知道"
print(driver.title)
# 生成当前页面快照并保存
# driver.save_screenshot("baidu.png")

driver.find_element_by_id("kw").click()
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
# 打印网页渲染后的源代码
# print(driver.page_source)
# 获取当前url
print(driver.current_url)
wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
time.sleep(1)
html_str = driver.page_source
obj_list = etree.HTML(html_str).xpath(
    '//div[@id="content_left"]//div[contains(@class,"result")]/h3/a')
for obj in obj_list:
    title = obj.xpath('string(.)').replace('\n', '').strip()
    print(title)

# 关闭当前页面，如果只有一个页面，会关闭浏览器
# driver.close()
# # 关闭浏览器
# driver.quit()
