# [https://github.com/soimort/you-get](https://github.com/soimort/you-get)

[you-get](https://github.com/soimort/you-get)乃一小小哒命令行程序，提供便利的方式来下载网络上的媒体信息。

## `you-get`安装

```bash
pip3 install --upgrade you-get
```

## 视频下载

```bash
# 当观赏感兴趣之视频，您可以使用 --info/-i,以查看所有可用画质与格式
# 标有DEFAULT 为默认画质
you-get -i https://www.bilibili.com/video/av6731067
you-get: This is a multipart video. (use --playlist to download all parts.)
site:                Bilibili
title:               【官方双语/合集】线性代数的本质 - 系列合集 (P1. 00 - 序言)
streams:             # Available quality and codecs
    [ DEFAULT ] _________________________________
    - format:        flv
      container:     flv
      quality:       高清 1080P
      size:          26.0 MiB (27291583 bytes)
    # download-with: you-get --format=flv [URL]

    - format:        flv720
      container:     flv
      quality:       高清 720P
      size:          26.0 MiB (27284602 bytes)
    # download-with: you-get --format=flv720 [URL]

    - format:        flv480
      container:     flv
      quality:       清晰 480P
      size:          25.9 MiB (27152992 bytes)
    # download-with: you-get --format=flv480 [URL]

    - format:        flv360
      container:     flv
      quality:       流畅 360P
      size:          17.5 MiB (18365033 bytes)
    # download-with: you-get --format=flv360 [URL]

# --playlist,下载播放列表
you-get --playlist --format=flv  https://www.bilibili.com/video/av6731067

# 使用 --player/-p,观看视频
you-get -p chromium https://www.bilibili.com/video/av6731067

# 舌尖上的中国
you-get -i https://v.youku.com/v_show/id_XNTAyNTk1MjQ4.html
# vip视频
you-get -i https://v.youku.com/v_show/id_XMTMzMDI2NjUzNg==.html
# 浏览器console -> document.cookie

```
