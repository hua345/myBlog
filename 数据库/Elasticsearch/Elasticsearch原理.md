[TOC]

# elasticsearch

- [Lucene 查询原理](https://zhuanlan.zhihu.com/p/35814539)
- [ES底层原理解析](https://www.cnblogs.com/cangqiongbingchen/p/14139000.html)
- [Elasticsearch 中为什么选择倒排索引而不选择 B 树索引](https://www.cnblogs.com/lonely-wolf/p/15464556.html#字典树（tria-tree）)
- [Elasticsearch 如何做到快速检索 - 倒排索引的秘密](https://juejin.cn/post/6889020742366920712)
- [关于Lucene的词典FST深入剖析](https://www.shenyanchao.cn/blog/2018/12/04/lucene-fst/)
- [ElasticSearch 2 (9) - 在ElasticSearch之下（图解搜索的故事）](https://www.cnblogs.com/richaaaard/p/5226334.html)
- [ES索引存储原理](https://blog.csdn.net/guoyuguang0/article/details/76769184)

## 简介

`ES`是`Elasticsearch`的简称，`Elasticsearch`是一个分布式可扩展的实时搜索和分析引擎，一个建立在全文搜索引擎`Apache Lucene`基础上的搜索引擎。`Lucene`只是一个框架，要充分利用它的功能，需要使用JAVA，并且在程序中集成`Lucene`，学习成本高，且`Lucene`确实非常复杂。

相对于数据库，Elasticsearch的强大之处就是可以**模糊查询**。

有的同学可能就会说：我数据库怎么就不能模糊查询了？：

```sql
select * from product where productName like '%helloworld%'
```

的确，这样做的确可以。但是要明白的是：`productNamelike %helloworld%`这类的查询是不走**索引**的，不走索引意味着：只要你的数据库的量很大（1亿条），你的查询肯定会是非常慢的并且占用数据库性能。

## RDBMS & ES

我相信大家对关系型数据库（简称 RDBMS）应该比较了解，因此接下来拿关系型数据库和 ES 做一个类比，让大家更容易理解：

| RDBMS  | ElasticSearch |
| ------ | ------------- |
| Table  | Index         |
| Row    | Document      |
| Column | Filed         |
| Schema | Mapping       |
| SQL    | DSL           |

## Lucene 和 ES

`Lucene` 是 `Elasticsearch`所基于的 Java 库，它引入了按段搜索的概念。

`Segment`：也叫段，类似于倒排索引，相当于一个数据集。

`Commit point`：提交点，记录着所有已知的段。

`Lucene index`：**a collection of segments plus a commit point**。由一堆 Segment 的集合加上一个提交点组成。

一个 `Elasticsearch Index` 由一个或者`多个 shard （分片）` 组成

![](D:/Code/myBlog/数据库/Elasticsearch/img/segment.png)

`Lucene` 中包含了四种基本数据类型，分别是：

`Index`：索引，由很多的 `Document` 组成。
`Document`：由很多的`Field`组成，是`Index`和`Search`的最小单位。
`Field`：由很多的`分词Term`组成，包括 Field Name 和`Field Value`。
`分词Term`：由很多的字节组成。一般将 Text 类型的 Field Value 分词之后的每个最小单元叫做`Term`。

**Segment数据集**有着许多数据结构

### Inverted Index

![](./img/Inverted%20Index.png)

`Inverted Index`主要包括两部分：

1. 一个有序的数据字典`Dictionary`（包括`单词Term`和它出现的`频率`）。
2. 与单词Term对应的`Postings`（即存在这个单词的文件）。

当我们搜索的时候，首先将搜索的内容分词，然后在字典里找到对应Term，从而查找到与搜索相关的文件内容。

### Stored Field

当我们想要查找包含某个特定标题内容的文件时，`Inverted Index`就不能很好的解决这个问题，所以Lucene提供了另外一种数据结构`Stored Fields`来解决这个问题。本质上，`Stored Fields`是一个简单的键值对`key-value`。默认情况下，ElasticSearch会存储整个文件的JSON source。

![](D:/Code/myBlog/数据库/Elasticsearch/img/storedField.png)

> By default, field values are [indexed](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-index.html) to make them searchable, but they are not *stored*. This means that the field can be queried, but the original field value cannot be retrieved.
>
> 字段默认是被索引可以搜索但是没有`stored`,以为着字段可以被查询，但是原始字段不会返回

Elasticsearch 一些内置的字段默认开启了**store**属性，例如 **_id**、**_source**字段。

当store为默认配置false时，这些field只存储在**_source**中

当store为true时，这些field的value会存储在一个跟**_source**平级的独立的field中。同时也会存储在**_source**中，所以有两份拷贝。

```
PUT my-index-000001
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "store": true 
      },
      "content": {
        "type": "text"
      }
    }
  }
}
PUT my-index-000001/_doc/1
{
  "title":   "Some short title",
  "content": "A very long content field..."
}

GET my-index-000001/_search
{
  "stored_fields": [ "title", "content"] 
}
```



### Document Values为了排序，聚合

即使这样，我们发现以上结构仍然无法解决诸如：排序、聚合，因为我们可能会要读取大量不需要的信息。

所以，另一种数据结构解决了此种问题：`Document Values`。这种结构本质上就是一个列式的存储，它高度优化了具有相同类型的数据的存储结构。

![](D:/Code/myBlog/数据库/Elasticsearch/img/docValue.png)

为了提高效率，`ElasticSearch`可以将索引下某一个`Document Value`全部读取到内存中进行操作，这大大提升访问速度，但是也同时会消耗掉大量的内存空间。

总之，这些数据结构`Inverted Index`、`Stored Fields`、`Document Values`及其缓存，都在`segment`内部。


## 倒排索引

索引，初衷都是为了快速检索到你要的数据。

我相信你一定知道`mysql`的索引，如果对某一个字段加了索引，一般来说查询该字段速度是可以有显著的提升。
每种数据库都有自己要解决的问题（或者说擅长的领域），对应的就有自己的数据结构，而不同的使用场景和数据结构，需要用不同的索引，才能起到最大化加快查询的目的。
对 `Mysql` 来说，是 `B+树`，对 `Elasticsearch/Lucene` 来说，是`倒排索引`。

`ES的JSON文档中的每一个字段，都有自己的倒排索引`，当然你可以指定某些字段不做索引，优点是这样可以节省磁盘空间。但是不做索引的话字段无法被搜索到。

`Lucene`中最重要的就是它的几种数据结构，这决定了数据是如何被检索的，本文再简单描述一下几种数据结构：

- `Finite State Transducers(有限状态转换器)`：保存`分词term字典`，可以在`FST`上实现单 Term、Term 范围、Term 前缀和通配符查询等。
- `skipList倒排链`：保存了每个`term`对应的`docId`的列表，采用`skipList`的结构保存，用于`快速跳跃`。
- `DocValues`：基于`docId`的列式存储，由于列式存储的特点，可以有效提升排序聚合的性能。

为了方便大家理解，我们以人名字，年龄，学号为例，如何实现查某个名字（有重名）的列表。

| docId | name  | age  | id   |
| ----- | ----- | ---- | ---- |
| 1     | Alice | 18   | 101  |
| 2     | Alice | 20   | 102  |
| 3     | Alice | 21   | 103  |
| 4     | Alan  | 21   | 104  |
| 5     | Alan  | 18   | 105  |



在 `lucene` 中为了查询 name=XXX 的这样一个条件，会建立基于 name 的倒排链。以上面的数据为例，倒排链如下：
姓名

| 分词 Term | 倒排链skipList |
| --------- | -------------- |
| Alice     | [1,2,3]        |
| Alan      | [4,5]          |

如果我们还希望按照年龄查询，例如想查年龄=18 的列表，我们还可以建立另一个倒排链：

| 分词 Term | 倒排链skipList |
| --------- | -------------- |
| 18        | [1,5]          |
| 20        | [2]            |
| 21        | [3,4]          |

如果没有倒排索引`Inverted Index`，想要去找其中的分词，需要遍历整个文档，才能找到对应的文档的 id，这样做效率是十分低的，所以为了提高效率，我们就给输入的所有数据的都建立索引，并且把这样的索引和对应的文档建立一个关联关系，相当于一个词典。当我们在寻找`分词term`的时候就可以直接像查字典一样，直接找到所有包含这个数据的文档的 id，然后找到数据。

#### Term Dictionary

Elasticsearch为了能快速找到某个term，将所有的term排序，二分法查找term，logN的查找效率，就像通过字典查找一样，这就是Term Dictionary。类似于传统数据库的B-Tree的，但是Term Dictionary较B-Tree的查询快。

#### Term Index

`B-Tree`通过减少磁盘寻道次数来提高查询性能，Elasticsearch也是采用同样的思路，直接通过内存查找term，不读磁盘，但是如果term太多，`term dictionary`也会很大，放内存不现实，于是有了**Term Index**，就像字典里的索引页一样，A开头的有哪些term，分别在哪页，`term index`其实是一颗[前缀树(Tria Tree)](https://www.cs.usfca.edu/~galles/visualization/Trie.html)

字典树又称之为前缀树（`Prefix Tree`），是一种哈希树的变种，可以用于搜索时的自动补全、拼写检查、最长前缀匹配等。 

字典树有以下三个特点：

1. 根节点不包含字符，除根节点外的其余每个节点都只包含一个字符。
2. 从根节点到某一节点，将路径上经过的所有字符连接起来，即为该节点对应的字符串。
3. 每个节点的所有子节点包含的字符都不相同。

![](D:/Code/myBlog/数据库/Elasticsearch/img/trieTree.png)

![es_term02](D:\Code\myBlog\数据库\Elasticsearch\img\es-term02.jpg)

所以`term index`不需要存下所有的term，而仅仅是他们的一些前缀与`Term Dictionary`的block之间的映射关系，再结合`FST(Finite State Transducers)`的压缩技术，可以使`term index`缓存到内存中。从`term index`查到对应的`term dictionary`的block位置之后，再去磁盘上找term，大大减少了磁盘随机读的次数。

#### 压缩技巧

Elasticsearch里除了上面说到用FST压缩term index外，对posting list也有压缩技巧。如果Elasticsearch需要对人的性别进行索引，如果有上千万个人，而性别只分男/女，每个posting list都会有至少百万个文档id。Elasticsearch采用一定的压缩算法对这些文档id进行压缩：

**增量编码压缩，将大数变小数，按字节存储**

首先，Elasticsearch要求`posting list`是有序的(为了提高搜索的性能)，这样做的好处是方便压缩，看下面这个图例：

![](D:/Code/myBlog/数据库/Elasticsearch/img/es-compressed.png)

**Roaring bitmaps 压缩算法**(`RBM`)

`Roaring bitmaps`基于bitmap。`Bitmap`是一种数据结构，假设某个`posting list`：[1,3,4,7,10]，其对应的bitmap就是：[1,0,1,1,0,0,1,0,0,1]。
用0/1表示某个值是否存在，存在的值对应的bit值是1，即一个字节 (8位) 可以代表8个文档id，旧版本 (5.0之前) 的Lucene就是用这样的方式来压缩的，但这样的压缩方式仍然不够高效，如果有1亿个文档，那么需要12.5MB的存储空间，这仅仅是对应一个索引字段。于是衍生出了Roaring bitmaps这样更高效的数据结构。
将posting list按照65535为界限分块 (block) ，比如第一块所包含的文档id范围在0~65535之间，第二块的id范围是65536~131071，以此类推。再用<商，余数>的组合表示每一组id，这样每组里的id范围都在0~65535内了。

Bitmap的缺点是存储空间随着文档个数线性增长，`Roaring bitmaps`利用了某些指数特性来规避这一点：

”为什么是以65535为界限?”

65535=2^16-1，正好是2个字节能表示的最大数，一个short的存储单位，注意到上图里的最后一行“If a block has more than 4096 values, encode as a bit set, and otherwise as a simple array using 2 bytes per value”，如果是较大的 (block) 块，用`bitset`存，小块用一个`short[]`存储。

那为什么用4096来区分采用数组还是bitmap的阀值呢？

这个是从内存大小考虑的，当block块里元素超过4096后，用bitmap更省空间： 采用bitmap需要的空间是恒定的: 65536/8 = 8192bytes 而如果采用short[]，所需的空间是: 2*N(N为数组元素个数) N=4096刚好是边界：

![](D:/Code/myBlog/数据库/Elasticsearch/img/bitmap.png)

#### 倒排合并

上述都是单field索引，如果是多个field索引的联合查询，倒排索引如何满足快速查询的要求呢？

利用跳表(Skip list)的数据结构快速做**与**运算，或者利用上面提到的bitset按位**与**。先看看跳表的数据结构：

![](D:/Code/myBlog/数据库/Elasticsearch/img/skipList.jpg)

1. 元素排序的，对应到我们的倒排链，lucene是按照docid进行排序，从小到大。
2. 跳跃有一个固定的间隔，这个是需要建立SkipList的时候指定好，例如上图的间隔是3
3. SkipList的层次，这个是指整个SkipList有几层

假设有下面三个`posting list`需要联合索引

![](D:/Code/myBlog/数据库/Elasticsearch/img/PostingList.png)

如果使用跳表，对**最短的posting list**中的每个id，逐个在另外两个`posting list`中查找看是否存在，最后得到交集的结果。如果使用`bitset`，就很直观了，直接按位与，得到的结果就是最后的交集。

## ES 写入的流程

1. 不断将 Document 写入到 In-memory buffer （内存缓冲区）。
2. 当满足一定条件后内存缓冲区中的 Documents 刷新到 高速缓存（**cache**）。
3. 生成新的 segment ，这个 segment 还在 cache 中。
4. 这时候还没有 commit ，但是已经可以被读取了。

![](D:/Code/myBlog/数据库/Elasticsearch/img/write01.png)

## ES查询过程

在初始查询阶段，查询将广播到索引中每个分片的分片副本（主或副本分片）。每个分片在本地执行搜索，并建立一个匹配文档的优先级队列。

### 优先队列

一个优先级队列仅仅是持有排序列表前 N 个匹配的文件。优先级队列的大小取决于分页参数 `from` 和 `size`。例如，以下搜索请求将需要一个足以容纳 `100` 个文档的优先级队列：

```json
GET / _search
{ "from": 90, "size": 10 }
```



### 查询阶段

当一个节点接收到一个搜索请求，则这个节点就变成了协调节点。

![es_query01](D:/Code/myBlog/数据库/Elasticsearch/img/es_query01.png)

每个分片将会在本地构建一个优先级队列。如果客户端要求返回结果排序中从第from名开始的数量为size的结果集，则每个节点都需要生成一个from+size大小的结果集，因此优先级队列的大小也是from+size。分片仅会返回一个轻量级的结果给协调节点，包含结果集中的每一个文档的ID和进行排序所需要的信息。

协调节点会将所有分片的结果汇总，并进行全局排序，得到最终的查询排序结果。此时查询阶段结束。

### 取回阶段

查询过程得到的是一个排序结果，标记出哪些文档是符合搜索要求的，此时仍然需要获取这些文档返回客户端。

协调节点会确定实际需要返回的文档，并向含有该文档的分片发送get请求；分片获取文档返回给协调节点；协调节点将结果返回给客户端。

![](D:/Code/myBlog/数据库/Elasticsearch/img/es_fetch.png)

### 深度分页

`query-then-fetch`流程支持使用`from`和`size` 参数分页，但限制在范围内。请记住，每个分片必须建立一个长度为优先级的队列`from + size`，所有这些队列都必须传递回协调节点。并且协调节点需要对 `number_of_shards * (from + size)`文档进行排序以找到正确的 `size`文档。

根据文档的大小，分片的数量以及所使用的硬件，完全可以分页`10,000`到`50,000`个结果（1,000到5,000页）。`但是使用足够大的from值，使用大量的CPU，内存和带宽`，排序过程的确会变得非常繁重。因此，我们`强烈建议您不要进行深度分页`。

实际上，`深度分页`很少是人类。人类将在两三页后停止分页，并将更改搜索条件。罪魁祸首通常是僵尸程序或网络蜘蛛，他们不知疲倦地不断一页一页地获取信息，直到您的服务器崩溃为止。

如果您确实需要从集群中获取大量文档，则可以通过没有排序的`scroll query`
