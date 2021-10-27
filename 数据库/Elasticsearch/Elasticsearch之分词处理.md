[TOC]

# [分词处理](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/indices-analyze.html)

> 文本分析就是把全文本转换成一系列单词`term/token`的过程，也叫分词
> 比如你输入`Hello World`,会自动帮你分成两个单词,`hello`和`world`,可以看出单词也被转化成了小写的

## 分词器`analyzer`的组成

分词器`analyzer`是专门处理分词的组件，分词器由以下三部分组成：

`char_filter`：将文本中 html 标签剔除掉。
`tokenizer`：按照规则进行分词，在英文中按照`空格`分词
`filter`：将切分的单词进行加工，比如大写转小写，删除 stopwords(停顿词，a、an、the、is 等),增加同义词

ES [内置分词器`analyzer`](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)

- [`Standard Analyzer`](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-standard-analyzer.html) - 默认分词器，按词切分，小写处理
- [`Simple Analyzer`](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-simple-analyzer.html) - 按照非字母切分（符号被过滤），小写处理
- `Stop`- 小写处理，停用词过滤（the ，a，is）
- [`Whitespace Analyzer`](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-whitespace-analyzer.html) - 按照空格切分，不转小写
- [`Keyword Analyzer`](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-keyword-analyzer.html) - 不分词，直接将输入当做输出
- `Pattern` - 正则表达式，默认 \W+
- [`Language Analyzers`](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-lang-analyzer.html) - 提供了 30 多种常见语言的分词器
- `Customer` - 自定义分词器

## [`standard`默认分词](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/indices-analyze.html#analyze-api-example)

`ALPHANUM`字母数字,`IDEOGRAPHIC`象形文字

```json
GET /_analyze
{
  "analyzer": "standard",
  "text": "Hello World"
}
```

## [自定义分词器](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/indices-analyze.html#analyze-api-custom-analyzer-ex)

```json
GET /_analyze
{
  "tokenizer" : "keyword",
  "filter" : ["lowercase"],
  "char_filter" : ["html_strip"],
  "text" : "This is a <b>test</b>"
}

GET /_analyze
{
  "tokenizer" : "whitespace",
  "filter" : ["lowercase", {"type": "stop", "stopwords": ["a", "is", "this"]}],
  "text" : "this is a test"
}
```

## [ik 中文扩展分词器](https://github.com/medcl/elasticsearch-analysis-ik)

```bash
wget https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.14.2/elasticsearch-analysis-ik-7.14.2.zip
/home/elasticsearch/elasticsearch-7.14.2/plugins && mkdir ik
cp ~/elasticsearch-analysis-ik-7.14.2.zip ./
unzip elasticsearch-analysis-ik-7.14.2.zip
# 重启elasticsearch
systemctl restart elasticsearch.service
# 启动日志中会有加载日志
[INFO ][o.e.p.PluginsService     ] [node-1] loaded plugin [analysis-ik]
```

Analyzer: `ik_smart` , `ik_max_word` , Tokenizer: `ik_smart` , `ik_max_word`

- `ik_max_word`: 会将文本做最细粒度的拆分，比如会将“`中华人民共和国国歌`”拆分为“`中华人民共和国`,`中华人民`,`中华`,`华人`,`人民共和国`,`人民`,`人`,`民`,`共和国`,`共和`,`和`,`国国`,`国歌`”，会穷尽各种可能的组合，适合 Term Query；
- `ik_smart`: 会做最粗粒度的拆分，比如会将“`中华人民共和国国歌`”拆分为“`中华人民共和国`,`国歌`”，适合 `Phrase` 查询。

```json
GET /_analyze
{
  "tokenizer" : "ik_smart",
  "text" : "我要吃苹果"
}
```

```json
{
  "tokens": [
    {
      "token": "我",
      "start_offset": 0,
      "end_offset": 1,
      "type": "CN_CHAR",
      "position": 0
    },
    {
      "token": "要吃",
      "start_offset": 1,
      "end_offset": 3,
      "type": "CN_WORD",
      "position": 1
    },
    {
      "token": "苹果",
      "start_offset": 3,
      "end_offset": 5,
      "type": "CN_WORD",
      "position": 2
    }
  ]
}
```

```json
PUT book_index3
{
  "mappings": {
    "properties": {
      "bookName": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      },
      "bookDate": {
        "type": "date",
        "format": "strict_date_optional_time||epoch_millis"
      }
    }
  }
}
```

## 自定义分词

### 新增自定义分词`my_word.dic`文件

```
芳芳
```

### 编辑`\plugins\ik\config\IKAnalyzer.cfg.xml`文件

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">
<properties>
	<comment>IK Analyzer 扩展配置</comment>
	<!--用户可以在这里配置自己的扩展字典 -->
	<entry key="ext_dict">my_word.dic</entry>
	 <!--用户可以在这里配置自己的扩展停止词字典-->
	<entry key="ext_stopwords"></entry>
	<!--用户可以在这里配置远程扩展字典 -->
	<!-- <entry key="remote_ext_dict">words_location</entry> -->
	<!--用户可以在这里配置远程扩展停止词字典-->
	<!-- <entry key="remote_ext_stopwords">words_location</entry> -->
</properties>
```

### 使用自定义分词前

```
GET /_analyze
{
  "tokenizer" : "ik_max_word",
  "text" : "我爱你芳芳"
}
{
  "tokens" : [
    {
      "token" : "我爱你",
      "start_offset" : 0,
      "end_offset" : 3,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "爱你",
      "start_offset" : 1,
      "end_offset" : 3,
      "type" : "CN_WORD",
      "position" : 1
    },
    {
      "token" : "芳",
      "start_offset" : 3,
      "end_offset" : 4,
      "type" : "CN_CHAR",
      "position" : 2
    },
    {
      "token" : "芳",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "CN_CHAR",
      "position" : 3
    }
  ]
}

```

### 使用自定义分词后

```
GET /_analyze
{
  "tokenizer" : "ik_max_word",
  "text" : "我爱你芳芳"
}
{
  "tokens" : [
    {
      "token" : "我爱你",
      "start_offset" : 0,
      "end_offset" : 3,
      "type" : "CN_WORD",
      "position" : 0
    },
    {
      "token" : "芳芳",
      "start_offset" : 3,
      "end_offset" : 5,
      "type" : "CN_WORD",
      "position" : 1
    }
  ]
}
```



## [ES插件管理](https://www.elastic.co/guide/en/elasticsearch/plugins/current/index.html)

```
# 启动日志中会有加载日志
[INFO ][o.e.p.PluginsService     ] [node-1] loaded plugin [analysis-ik]
# 安装插件
bin/elasticsearch-plugin install [plugin_name]
# Unix安装/path/to/plugin.zip
sudo bin/elasticsearch-plugin install file:///path/to/plugin.zip
# Windows安装C:\path\to\plugin.zip
bin\elasticsearch-plugin install file:///C:/path/to/plugin.zip
# analysis-smartcn分词器
sudo bin/elasticsearch-plugin install analysis-smartcn
# 查询安装的插件列表
bin/elasticsearch-plugin list
ik
```



## 安装ik分词的问题

```
java.security.AccessControlException: access denied ("java.io.FilePermission" "Program%20Files\ES\elasticsearch-7.14.2\plugins\ik\config\IKAnalyzer.cfg.xml" "read")
```

`Program Files`有空格
