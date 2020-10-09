# selenium

- [https://github.com/SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium)
- [https://npm.taobao.org/mirrors/chromedriver/](https://npm.taobao.org/mirrors/chromedriver/)
- [https://selenium-python.readthedocs.io/index.html](https://selenium-python.readthedocs.io/index.html)

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
