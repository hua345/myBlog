# 参考

- [How to use the tools provided to train Tesseract 4.00](https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00#creating-training-data)
- [Tesseract训练中文字体识别](https://www.jianshu.com/p/31afd7fc5813)

## 将图片转换为tif格式

通过格式工厂将图片转换为`tif`格式

## 合并多个tif文件为一个

这里需要用到一个软件jTessBoxEditor

打开`Tools－>Merge TIFF...`，选择多个tif文件，保存为name.tif

```bash
# tif文面命名格式[lang].[fontname].exp[num].tif
# lang是语言           fontname是字体

#比如我们要训练自定义字库idcard,字体名test
idcard.front.exp0.tif
```

## 生成box文件

```bash
./tesseract.exe ./img/idcard.front.exp0.tif ./img/idcard.front.exp0  -l chi_sim batch.nochop makebox
```

## 打开jTessBoxEditor矫正错误并训练

打开`train.bat`
用`jTessBoxEditor`打开tif文件，然后根据实际情况修改box文件

## 训练，生成.tr文件

```bash
./tesseract.exe ./img/idcard.front.exp0.tif ./img/idcard.front.exp0 nobatch box.train
```

生成一个unicharset文件

```bash
./unicharset_extractor.exe ./img/idcard.front.exp0.box
```

## 创建字体特征文件

新建一个`front_properties`文件

```bash
front 0 0 0 0 0
```

```bash
./shapeclustering.exe -F ./img/front_properties.txt -U unicharset ./img/idcard.front.exp0.tr
```

## 生成字典数据

```bash
./mftraining.exe -F ./img/front_properties.txt -U unicharset -O unicharset ./img/idcard.front.exp0.tr

./cntraining.exe ./img/idcard.front.exp0.tr
```

## 合并数据文件

