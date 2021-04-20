# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from lxml import etree
import time
import xlsxwriter

options = webdriver.ChromeOptions()
# 找到本地安装的浏览器启动路径，例如Chrome
# 设置--user-data-dir是为了不影响自己的浏览器
# chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\Program File\chromeUserData"
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")


base_url = "https://www.baidu.com/"
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10, 0.5)

driver.implicitly_wait(3)
driver.get(base_url)

# 打印页面标题 "百度一下，你就知道"
print(driver.title)
# 生成当前页面快照并保存
# driver.save_screenshot("baidu.png")
wait.until(EC.presence_of_element_located((By.ID, 's-top-username')))
print(driver.find_element_by_xpath(
    '//a[@id="s-top-username"]/span[last()]').text)
print(driver.find_element_by_id('s-top-username').text)
print(driver.find_element_by_id(
    's-top-username').find_element_by_xpath('./span[last()]').text)
driver.find_element_by_id("kw").click()
driver.find_element_by_id("kw").send_keys("taobao")
driver.find_element_by_id("su").click()
# 打印网页渲染后的源代码
# print(driver.page_source)
# 获取当前url
print(driver.current_url)
wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
time.sleep(1)
firstElem = driver.find_element_by_xpath(
    '//div[@id="content_left"]//div[contains(@class,"result")][1]/h3/a')
print(firstElem.text)
firstElem.click()

# 获取所有的打开的浏览器窗口
windowstabs = driver.window_handles
print(windowstabs)
# 获取当前浏览器的窗口
currenttab = driver.current_window_handle
print(currenttab)
# 切换到新窗口
driver.switch_to.window(windowstabs[1])
print(driver.current_url)
time.sleep(1)
driver.close()
driver.switch_to.window(windowstabs[0])
print(driver.current_url)


# html_str = driver.page_source
# obj_list = etree.HTML(html_str).xpath(
#     '//div[@id="content_left"]//div[contains(@class,"result")]/h3/a')
# result = ['标题']
# for obj in obj_list:
#     title = obj.xpath('string(.)').replace('\n', '').strip()
#     print(title)
#     result.append(title)

# workbook = xlsxwriter.Workbook('baidu.xlsx')  #创建一个Excel文件
# worksheet = workbook.add_worksheet()               #创建一个sheet
# # 列宽
# worksheet.set_column('A:J', 20)
# #向 excel 中写入数据
# worksheet.write_column('A1',result)
# workbook.close()

# 关闭当前页面，如果只有一个页面，会关闭浏览器
# driver.close()
# # 关闭浏览器
# driver.quit()
