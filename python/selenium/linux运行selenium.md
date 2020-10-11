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

## ubantu

```bash
# 找到ubantu版本号
cat /etc/apt/sources.list
# https://mirrors.ustc.edu.cn/repogen
# https://developer.aliyun.com/mirror/ubuntu?spm=a2c6h.13651102.0.0.3e221b11wiisVv
wget https://mirrors.ustc.edu.cn/repogen/conf/ubuntu-https-4-focal

mv ubuntu-https-4-focal /etc/apt/sources.list
apt update
# E: Release file for https://mirrors.ustc.edu.cn/ubuntu/dists/focal-security/InRelease is not valid yet (invalid for another 7h 34min 25s). Updates for this repository will not be applied.
# 更新主机时间


apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome*.deb

# 查看版本
google-chrome --version

docker commit --change='CMD ["/bin/bash", "/app/docker_init.sh"]' master tikazyq/crawlab:latest
```
