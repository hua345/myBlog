# 使用Selenium控制已经打开的浏览器

## 找到本地安装的浏览器启动路径，例如Chrome

```bash
C:\Users\Administrator\AppData\Local\Google\Chrome\Application
# 通过命令行打开
#设置--user-data-dir是为了不影响自己的浏览器
chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\Program File\chromeUserData"
```

```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)
```
