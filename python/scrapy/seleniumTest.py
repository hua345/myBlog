from selenium import webdriver

base_url = "https://www.baidu.com/"
driver = webdriver.Chrome()
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
# 关闭当前页面，如果只有一个页面，会关闭浏览器
# driver.close()
# # 关闭浏览器
# driver.quit()