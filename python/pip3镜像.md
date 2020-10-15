# python包镜像

## 国内的pip源

- 阿里云：[https://mirrors.aliyun.com/pypi/simple/](https://mirrors.aliyun.com/pypi/simple/)
- 清华：[https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
- 中国科技大学 [https://pypi.mirrors.ustc.edu.cn/simple/](https://pypi.mirrors.ustc.edu.cn/simple/)

## 修改配置文件

```bash
mkdir ~/.pip
vim ~/.pip/pip.conf
```

```conf
[global]
index-url = https://mirrors.aliyun.com/pypi/simple
```

## 临时更换

```bash
pip3 install tensorflow -i https://mirrors.aliyun.com/pypi/simple/
pip3 install tensorflow-gpu -i https://mirrors.aliyun.com/pypi/simple/
pip3 install --upgrade tensorflow -i https://mirrors.aliyun.com/pypi/simple/
```
