> grep 查找, sed 编辑, awk 根据内容分析并处理.
> grep (global search regular expression(RE) and print out the line,全面搜索正则表达式并把行打印出来)
是一种强大的文本搜索工具，它能使用正则表达式搜索文本，并把匹配的行打印出来
#### 查看帮助
```
➜  ~ grep --help
用法: grep [选项]... PATTERN [FILE]...
在每个 FILE 或是标准输入中查找 PATTERN。
默认的 PATTERN 是一个基本正则表达式(缩写为 BRE)。
例如: grep -i 'hello world' menu.h main.c
````
|可选参数| 说明|
|--------|-------------|
|-E, --extended-regexp   |  PATTERN 是一个可扩展的正则表达式(缩写为 ERE)|
|-F, --fixed-strings    |   PATTERN 是一组由断行符分隔的定长字符串。|
|-G, --basic-regexp    |    PATTERN 是一个基本正则表达式(缩写为 BRE)|
|-e, --regexp=PATTERN | 用 PATTERN 来进行匹配操作|
|-f, --file=FILE |从 FILE 中取得 PATTERN|
|-i, --ignore-case |忽略大小写|
|-w, --word-regexp |强制 PATTERN 仅完全匹配字词|

|可选参数|说明|
|------------|-------------|
|  -c, --count | 只显示匹配的行数|
|  -m, --max-count=NUM |  NUM 次匹配后停止|
|  -b, --byte-offset |   输出的同时打印字节偏移|
|  -n, --line-number |   输出的同时打印行号|
| -H, --with-filename |   为每一匹配项打印文件名|
|  -h, --no-filename |   输出时不显示文件名前缀|