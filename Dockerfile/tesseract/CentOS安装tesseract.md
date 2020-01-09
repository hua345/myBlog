# 参考

- [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- [源码编译](https://github.com/tesseract-ocr/tesseract/wiki/Compiling-%E2%80%93-GitInstallation)
- [Leptonica 1.74 or higher is required. 的解决办法](https://blog.csdn.net/xjmxym/article/details/79040514)

## 简介

> [tesseract](https://github.com/tesseract-ocr/tesseract)包含OCR引擎`libtesseract`和命令行程序`tesseract`
>
> `esseract 4`增加了一个基于OCR引擎的新神经网络（LSTM），该引擎专注于线路识别，但仍然支持`Tesseract 3`的传统`Tesseract OCR引擎`，该引擎通过识别字符模式来工作。
>
> 通过使用`Legacy OCR Engine模式（--oem 0）`启用与`Tesseract 3`的兼容性。 它还需要训练有素的数据文件，这些文件支持传统引擎，例如来自tessdata存储库的文件。
>
> `Tesseract` 支持`utf-8`,能够识别100多种语言

## 安装Tesseract

### yum安装

![https://github.com/tesseract-ocr/tesseract/wiki](https://github.com/tesseract-ocr/tesseract/wiki)

```basg
yum install yum-utils

yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/

rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/public_key

yum update
# 安装识别图片的依赖包
yum install libjpeg-devel libpng-devel
yum install tesseract tesseract-langpack-deu
```

### 源码编译

#### 环境依赖

```bash
yum install automake ca-certificates g++ git libtool libleptonica-dev make pkg-config
```

如果需要构建`asciidoc`和`Tesseract training tools`需要

```bash
yum install asciidoc libpango1.0-dev
```

#### 下载源码

```bash
git clone --depth 1  https://github.com/tesseract-ocr/tesseract.git
```

#### 安装libleptonica-dev

- [leptonica](http://www.leptonica.org/download.html)
- [https://github.com/DanBloomberg/leptonica](https://github.com/DanBloomberg/leptonica)

```bash
# https://github.com/DanBloomberg/leptonica/releases
# 下载releases包

# 安装识别图片的依赖包
yum install libjpeg-devel libpng-devel

tar -zvxf leptonica-1.78.0.tar.gz
./configure
make -j4
make install

#/usr/local/include/leptonica
#/usr/local/lib
vim /etc/profile
export LD_LIBRARY_PATH=$LD_LIBRARY_PAYT:/usr/local/lib
export LIBLEPT_HEADERSDIR=/usr/local/include
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
```

#### 构建源码

```bash
cd tesseract
./autogen.sh
./configure --with-extra-includes=/usr/local/include --with-extra-libraries=/usr/local/include
# make -j4会出错,只使用make
make
make install
ldconfig
```

## 查看tesseract版本

```bash
➜  ~ tesseract -v
tesseract 4.1.0
 leptonica-1.78.0
  libjpeg 6b (libjpeg-turbo 1.2.90) : libpng 1.5.13 : zlib 1.2.7
```
