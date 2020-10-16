# Manim

- [https://github.com/3b1b/manim](https://github.com/3b1b/manim)
- [manim在windows系统下安装](https://www.cnblogs.com/noticeable/p/12651585.html)

> Manim是一款数学教学的动画引擎

```bash
pip3 install latex ffmpeg numpy opencv-python pycairo

# 安装MiKTeX
# 为了支持laTex格式文本，需要到官网https://miktex.org/download下载MiKTeX

#安装ffmpeg及dvisvgm
# FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。windows下下载ffmpeg，首先需要到官网https://ffmpeg.org/download.html#build-windows下载对应软件包。
# 命令行工具dvisvgm将由TeX/LaTeX创建的DVI文件转换为基于XML的SVG格式。同理https://sourceforge.net/projects/dvisvgm/files/latest/download下载软件包。
# 解压加入环境变量
# D:\Program File\dvisvgm-1.10-win64
git clone --depth=1 git@github.com:3b1b/manim.git
pip3 install -r requirements.txt
```
