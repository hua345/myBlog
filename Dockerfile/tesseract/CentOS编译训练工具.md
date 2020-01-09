# 参考

[TrainingTesseract](https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00#overview-of-training-process)

## 训练过程

- Prepare training text.
- Render text to image + box file. (Or create hand-made box files for existing image data.)
- Make unicharset file. (Can be partially specified, ie created manually).
- Make a starter traineddata from the unicharset and optional dictionary data.
- Run tesseract to process image + box file to make training data set.
- Run training on training data set.
- Combine data files.

```bash
yum install libicu-dev libpango1.0-dev libcairo2-dev
```
