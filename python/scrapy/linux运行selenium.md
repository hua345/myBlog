# selenium

## 下载chrome与chromedriver

```bash
# 下载chrome
yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

# 查看chrome版本
google-chrome --version

Google Chrome 86.0.4240.75

# 下载chromedriver
http://npm.taobao.org/mirrors/chromedriver/
wget https://npm.taobao.org/mirrors/chromedriver/86.0.4240.22/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
# 移动chromedriver到/usr/bin
mv chromedriver /usr/bin/

# 查看chromedriver版本
chromedriver --version

ChromeDriver 86.0.4240.22 (398b0743353ff36fb1b82468f63a3a93b4e2e89e-refs/branch-heads/4240@{#378})
```
