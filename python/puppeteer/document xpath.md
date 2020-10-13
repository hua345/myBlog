# [Document.evaluate()](https://developer.mozilla.org/en-US/docs/Web/API/Document/evaluate)

## 简单结果类型

- `NUMBER_TYPE`
- `STRING_TYPE`
- `BOOLEAN_TYPE`

```js
var aCount = document.evaluate('count(//a)', document, null, XPathResult.ANY_TYPE, null );
aCount.numberValue
```

## 节点集类型

### Iterators

- UNORDERED_NODE_ITERATOR_TYPE
- ORDERED_NODE_ITERATOR_TYPE

如果文档内容发生改变会抛出异常

```js
var iterator = document.evaluate('//div[@id="content_left"]//div[contains(@class,"result")]/h3/a', document, null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null );

try {
  var thisNode = iterator.iterateNext();
  while (thisNode) {
    console.log(thisNode.textContent);
    thisNode = iterator.iterateNext();
  }
}
catch (e) {
  console.log( 'Error: Document tree modified during iteration ' + e );
}
```

### Snapshots快照

如果文档内容发生改变,内容可能会不一致

```js
var nodesSnapshot = document.evaluate('//div[@id="content_left"]//div[contains(@class,"result")]/h3/a', document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null );

for ( var i=0 ; i < nodesSnapshot.snapshotLength; i++ )
{
  console.log(nodesSnapshot.snapshotItem(i).textContent );
}
```

## XPathResult 定义的常量

| Result Type定义的常量             | 值  | 描述                                                                                                                   |
| ------------------------------ | --- | ---------------------------------------------------------------------------------------------------------------------- |
| `ANY_TYPE`                     | 0   | 包含任何类型的结果集自然都来自表达式的求值。如果结果是节点集，则`UNORDERED_NODE_ITERATOR_TYPE`始终是结果类型。 |
| `NUMBER_TYPE`                  | 1   | 包含单个数字的结果。例如，在使用 count()函数的 XPath 表达式中，这很有用。                                              |
| `STRING_TYPE`                  | 2   | 包含单个字符串的结果。                                                                                                 |
| `BOOLEAN_TYPE`                 | 3   | 包含单个布尔值的结果。例如，在使用 not()函数的 XPath 表达式中，这很有用。                                              |
| `UNORDERED_NODE_ITERATOR_TYPE` | 4   | 结果节点集，包含与表达式匹配的所有节点。节点可能不一定与它们在文档中出现的顺序相同。                                   |
| `ORDERED_NODE_ITERATOR_TYPE`   | 5   | 结果节点集，包含与表达式匹配的所有节点。结果集中的节点与它们在文档中出现的顺序相同。                                   |
| `UNORDERED_NODE_SNAPSHOT_TYPE` | 6   | 结果节点集，包含与表达式匹配的所有节点的快照。节点可能不一定与它们在文档中出现的顺序相同。                             |
| `ORDERED_NODE_SNAPSHOT_TYPE`   | 7   | 结果节点集，包含与表达式匹配的所有节点的快照。结果集中的节点与它们在文档中出现的顺序相同。                             |
| `ANY_UNORDERED_NODE_TYPE`      | 8   | 结果节点集，包含与表达式匹配的任何单个节点。该节点不一定是文档中与表达式匹配的第一个节点。                             |
| `FIRST_ORDERED_NODE_TYPE`      | 9   | 结果节点集，它包含文档中与表达式匹配的第一个节点。                                                                     |
