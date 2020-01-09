# 参考

## 查看tesseract版本

```bash
➜  ~ tesseract -v
tesseract 4.1.0
 leptonica-1.78.0
  libjpeg 6b (libjpeg-turbo 1.2.90) : libpng 1.5.13 : zlib 1.2.7
```

## 查看帮助

```bash
➜  tesseract tesseract --help-extra
Usage:
  tesseract --help | --help-extra | --help-psm | --help-oem | --version
  tesseract --list-langs [--tessdata-dir PATH]
  tesseract --print-parameters [options...] [configfile...]
  tesseract imagename|imagelist|stdin outputbase|stdout [options...] [configfile...]

OCR options:
  --tessdata-dir PATH   Specify the location of tessdata path.
  --user-words PATH     Specify the location of user words file.
  --user-patterns PATH  Specify the location of user patterns file.
  --dpi VALUE           Specify DPI for input image.
  -l LANG[+LANG]        Specify language(s) used for OCR.
  -c VAR=VALUE          Set value for config variables.
                        Multiple -c arguments are allowed.
  --psm NUM             Specify page segmentation mode.
  --oem NUM             Specify OCR Engine mode.
NOTE: These options must occur before any configfile.

Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR. (not implemented)
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
       bypassing hacks that are Tesseract-specific.

OCR Engine modes: (see https://github.com/tesseract-ocr/tesseract/wiki#linux)
  0    Legacy engine only.
  1    Neural nets LSTM engine only.
  2    Legacy + LSTM engines.
  3    Default, based on what is available.
Single options:
  -h, --help            Show minimal help message.
  --help-extra          Show extra help for advanced users.
  --help-psm            Show page segmentation modes.
  --help-oem            Show OCR Engine modes.
  -v, --version         Show version information.
  --list-langs          List available languages for tesseract engine.
  --print-parameters    Print tesseract parameters.
```

## 查看训练数据

```bash
ls  /usr/share/tesseract/4/tessdata/
configs  deu.traineddata  eng.traineddata  osd.traineddata

# https://github.com/tesseract-ocr/tessdata
# 下载中文训练数据
chi_sim.traineddata

➜  tesseract tesseract --list-langs
List of available languages (4):
chi_sim
deu
eng
osd
```

## 选择使用的引擎

Use `--oem 1` for LSTM, `--oem 0` for Legacy Tesseract.

## OCR

```bash
➜  tesseract aa.jpg ouput --oem 1 -l chi_sim
Error in pixReadMemTiff: function not present
Error in pixReadMem: tiff: no pix returned
Error in pixaGenerateFontFromString: pix not made
Error in bmfCreate: font pixa not made
Tesseract Open Source OCR Engine v4.1.0 with Leptonica
Warning: Invalid resolution 0 dpi. Using 70 instead.
Estimating resolution as 665

➜  tesseract cat ouput.txt
烨 名 陈 建 华
伴 别 男 民 熔 汪
“ 生 1992 年 吗 月 29 日
仪 址 “ 江 西 相 捐 州 市 临 川 区 桐 源
乡 青 均 村 三 组 55

```
