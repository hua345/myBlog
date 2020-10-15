from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from lxml import etree
import time
import xlsxwriter
from saveImgUtil import downloadImgs

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

base_url = "https://www.zhihu.com/question/421019418"
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10, 0.5)
driver.implicitly_wait(3)
driver.get(base_url)
time.sleep(1)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="QuestionPage"]//h1[@class="QuestionHeader-title"]')))
title = driver.find_element_by_xpath('//div[@class="QuestionPage"]//h1[@class="QuestionHeader-title"]').text
print(title)
def execute_times(times):
    for i in range(times):
        print(i)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ActionChains(driver).key_down(Keys.ARROW_UP).perform()
        time.sleep(2)
# 生成当前页面快照并保存
# driver.save_screenshot("baidu.png")
wait.until(EC.presence_of_element_located((By.ID, 'QuestionAnswers-answers')))

execute_times(10)
answersList = driver.find_elements_by_xpath(
    '//div[@id="QuestionAnswers-answers"]//div[@class="List-item"]')
for answerItem in answersList:
    imgUrls = []
    imgElems = answerItem.find_elements_by_xpath('.//figure//img')
    for imgElem in imgElems:
        imgUrl = imgElem.get_attribute('data-original')
        if imgUrl is None:
            pass
        else:
            imgUrls.append(imgUrl)
    print(imgUrls)
    downloadImgs(title,imgUrls)

# 关闭当前页面，如果只有一个页面，会关闭浏览器
# driver.close()
# # 关闭浏览器
# driver.quit()
