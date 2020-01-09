# 参考

- [https://www.python.org/](https://www.python.org/)
- [https://npm.taobao.org/mirrors/python/](https://npm.taobao.org/mirrors/python/)

## 查看当前python版本

```bash
➜  ~ python --version
Python 2.7.5
```

## 安装依赖

3.7版本需要一个新的包`libffi-devel`

```bash
yum install libffi-devel -y
```

否则会报下面的错误

```bash
Failed to build these modules:
_ctypes
```

## 下载python3

下载`python3`

```bash
➜  ~ wget https://npm.taobao.org/mirrors/python/3.7.4/Python-3.7.4.tgz
➜  ~ tar -zvxf Python-3.7.4.tgz
➜  ~ cd Python-3.7.4

```

## 编译`python3`

```bash
./configure
make -j4
make install
```

## 查看python安装位置

```bash
# python3安装位置
➜  Python-3.7.4 ll /usr/local/bin/python*
lrwxrwxrwx. 1 root root    9 8月  31 15:39 /usr/local/bin/python3 -> python3.7
-rwxr-xr-x. 2 root root  14M 8月  31 15:38 /usr/local/bin/python3.7
lrwxrwxrwx. 1 root root   17 8月  31 15:39 /usr/local/bin/python3.7-config -> python3.7m-config
-rwxr-xr-x. 2 root root  14M 8月  31 15:38 /usr/local/bin/python3.7m
-rwxr-xr-x. 1 root root 2.9K 8月  31 15:39 /usr/local/bin/python3.7m-config
lrwxrwxrwx. 1 root root   16 8月  31 15:39 /usr/local/bin/python3-config -> python3.7-config

# python2安装位置
➜  Python-3.7.4 ll /usr/bin/python*
lrwxrwxrwx. 1 root root    7 7月   1 23:07 /usr/bin/python -> python2
lrwxrwxrwx. 1 root root    9 7月   1 23:07 /usr/bin/python2 -> python2.7
-rwxr-xr-x. 1 root root 7.1K 6月  21 04:28 /usr/bin/python2.7
-rwxr-xr-x. 1 root root  293 7月   5 2016 /usr/bin/python2-http

# 备份python2
mv /usr/bin/python /usr/bin/python_bak_

# 软链接python3
ln -s /usr/local/bin/python3 /usr/bin/python
```

## 查看现在python版本

```bash
➜  ~ python -V
Python 3.7.4
```

## 为了使yum命令正常使用，需要将其配置的python依然指向2.x版本

```bash
/usr/bin/yum
/usr/libexec/urlgrabber-ext-down

!/usr/bin/python --> !/usr/bin/python2.7
```
