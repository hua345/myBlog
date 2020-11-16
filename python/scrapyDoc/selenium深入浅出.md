# selenium

- [https://github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium)
- [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/)
- [https://selenium-python.readthedocs.io/index.html](https://selenium-python.readthedocs.io/index.html)
- [Python爬虫利器五之Selenium的用法](https://cuiqingcai.com/2599.html)

## 安装selenium

```bash
pip3 install selenium
```

## 安装驱动

下载当前浏览器对应的驱动`chromedriver_win32.zip`,解压后将`chromedriver.exe`放到`python.exe`同一级目录下

## 运行测试代码

```py
from selenium import webdriver

base_url = "https://www.baidu.com/"
driver = webdriver.Chrome()
driver.implicitly_wait(3)
driver.get(base_url)

driver.find_element_by_id("kw").click()
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
```

## 元素选取

```py
# 单元素选取
find_element_by_id
find_element_by_name
find_element_by_xpath
find_element_by_link_text
find_element_by_partial_link_text
find_element_by_tag_name
find_element_by_class_name
find_element_by_css_selector
# 多个元素选取
find_elements_by_name
find_elements_by_xpath
find_elements_by_link_text
find_elements_by_partial_link_text
find_elements_by_tag_name
find_elements_by_class_name
find_elements_by_css_selector
# By 类来确定哪种选择方式
from selenium.webdriver.common.by import By


ID = "id"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
NAME = "name"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"
```

## 页面等待

这是非常重要的一部分，现在的网页越来越多采用了`Ajax`技术，这样程序便不能确定何时某个元素完全加载出来了。

所以 Selenium 提供了两种等待方式，一种是隐式等待，一种是显式等待。

### 显式等待

```py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
finally:
    driver.quit()
```

```py
#这两个条件验证元素是否出现，传入的参数都是元组类型的locator，如(By.ID, 'kw')
#一个只要一个符合条件的元素加载出来就通过；另一个必须所有符合条件的元素都加载出来才行
EC.presence_of_element_located((By.CSS_SELECTOR,'.ui-page > div.ui-page-wrap'))
EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.ui-page > div.ui-page-wrap'))
#这三个条件验证元素是否可见，前两个传入参数是元组类型的locator，第三个传入WebElement
#第一个和第三个其实质是一样的
EC.visibility_of_element_located
EC.invisibility_of_element_located
EC.visibility_of
#这两个人条件判断某段文本是否出现在某元素中，一个判断元素的text，一个判断元素的value属性
EC.text_to_be_present_in_element
EC.text_to_be_present_in_element_value
#这个条件判断是否有alert出现
EC.alert_is_present
#这个条件判断元素是否可点击，传入locator
EC.element_to_be_clickable
#这四个条件判断元素是否被选中，第一个条件传入WebElement对象，第二个传入locator元组
#第三个传入WebElement对象以及状态，相等返回True，否则返回False
#第四个传入locator以及状态，相等返回True，否则返回False
EC.element_to_be_selected
EC.element_located_to_be_selected
EC.element_selection_state_to_be
EC.element_located_selection_state_to_be
#最后一个条件判断一个元素是否仍在页面中，传入WebElement对象，可以判断页面是否刷新
EC.staleness_of
```

### 隐式等待

隐式等待比较简单，就是简单地设置一个等待时间，单位为秒。

```py
from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10) # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```
