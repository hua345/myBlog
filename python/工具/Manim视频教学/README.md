# Manim

- [https://github.com/3b1b/manim](https://github.com/3b1b/manim)
- [manim在windows系统下安装](https://www.cnblogs.com/noticeable/p/12651585.html)
- [pip install manimlib出现UnicodeDecodeError: 'gbk'](https://blog.csdn.net/qq_35020200/article/details/100516383)

> Manim是一款数学教学的动画引擎

```bash
pip3 install latex ffmpeg numpy opencv-python pycairo

# 安装MiKTeX
# 为了支持laTex格式文本，需要到官网[https://miktex.org/download](https://miktex.org/download)下载MiKTeX

#安装ffmpeg及dvisvgm
# FFmpeg是一套可以用来记录、转换数字音频、视频，并能将其转化为流的开源计算机程序。windows下下载ffmpeg，首先需要到官网[https://ffmpeg.org/download.html#build-windows]下载对应软件包。
# 命令行工具dvisvgm将由TeX/LaTeX创建的DVI文件转换为基于XML的SVG格式。同理[https://sourceforge.net/projects/dvisvgm/files/latest/download]下载软件包。
# 解压加入环境变量

$ dvisvgm --version
dvisvgm 1.10
$ ffmpeg.exe -version
ffmpeg version N-99577-g2b5e18a953 Copyright (c) 2000-2020 the FFmpeg developers
built with gcc 9.3-win32 (GCC) 20200320
configuration: --prefix=/ffbuild/prefix --pkg-config-flags=--static --pkg-config=pkg-config --cross-prefix=x86_64-w64-mingw32- --arch=x86_64 --target-os=mingw32 --enable-gpl --enable-version3 --disable-debug --enable-iconv --enable-zlib --enable-libxml2 --enable-libfreetype --enable-libfribidi --enable-gmp --enable-lzma --enable-fontconfig --enable-opencl --enable-libvmaf --disable-vulkan --enable-libvorbis --enable-amf --enable-libaom --enable-avisynth --enable-libdav1d --enable-libdavs2 --enable-ffnvcodec --enable-cuda-llvm --disable-libglslang --enable-libass --enable-libbluray --enable-libmp3lame --enable-libopus --enable-libtheora --enable-libvpx --enable-libwebp --enable-libmfx --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librav1e --enable-schannel --enable-sdl2 --enable-libsoxr --enable-libsrt --enable-libsvtav1 --enable-libtwolame --enable-libuavs3d --enable-libvidstab --enable-libx264 --enable-libx265 --enable-libxavs2 --enable-libxvid --enable-libzimg --extra-cflags=-DLIBTWOLAME_STATIC --extra-cxxflags= --extra-ldflags=-pthread --extra-libs=-lgomp
libavutil      56. 60.100 / 56. 60.100
libavcodec     58.111.101 / 58.111.101
libavformat    58. 62.100 / 58. 62.100
libavdevice    58. 11.102 / 58. 11.102
libavfilter     7. 87.100 /  7. 87.100
libswscale      5.  8.100 /  5.  8.100
libswresample   3.  8.100 /  3.  8.100
libpostproc    55.  8.100 / 55.  8.100

pip3 install manimlib -i https://mirrors.aliyun.com/pypi/simple/
# 出现UnicodeDecodeError: 'gbk' codec can't decode byte 0xff in position 0......
# 下载pip3日志中的manimlib-0.1.11.tar.gz
# 解压manimlib-0.1.11.tar.gz
# 编辑PKG-INFO,修改编码格式为ANSI或者ASCII
$ pip install manimlib-0.1.11/
Processing c:\users\22909\downloads\manimlib-0.1.11\manimlib-0.1.11
```

```bash
$ python -m manim example_scenes.py SquareToCircle -pl
Animation 0: ShowCreationSquare:  73%|#######3  | 11/15 [00:00<00:00, 107.19it/s                                                                                Media will be written to C:\Code\github\manim\media\. You can change this behavior with the --media_dir flag.

File ready at C:\Code\github\manim\media\videos\example_scenes\480p15\SquareToCircle.mp4

Played 3 animations
```

## 通过源码执行

```bash
# D:\Program File\dvisvgm-1.10-win64
git clone --depth=1 git@github.com:3b1b/manim.git

pip3 install -r requirements.txt
# -pl参数是生成低画质的动画
$ python manim.py example_scenes.py SquareToCircle -pl
Media will be written to C:\Code\github\manim\media\. You can change this behavior with the --media_dir flag.

File ready at C:\Code\github\manim\media\videos\example_scenes\480p15\SquareToCircle.mp4

Played 3 animations
```
