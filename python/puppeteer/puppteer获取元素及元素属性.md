# [puppeteer](https://github.com/puppeteer/puppeteer)

- [https://github.com/puppeteer/puppeteer](https://github.com/puppeteer/puppeteer)
- [https://pptr.dev/](https://pptr.dev/)
- [http://puppeteerjs.com](http://puppeteerjs.com/#?product=Puppeteer&version=v5.3.1&show=api-pageselector)
- [https://developer.mozilla.org/en-US/docs/Web/API/Document/evaluate](https://developer.mozilla.org/en-US/docs/Web/API/Document/evaluate)
- [https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- `document.evaluate`
- `document.querySelectorAll`

## 获取元素及元素属性

### `page.$(selector)`

- `selector <string>` 选择器,参考[CSS_Selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- 此方法在页面内执行 `document.querySelector`。如果没有元素匹配指定选择器，返回值是 null。
- `page.mainFrame().$(selector)`的缩写

### `page.$$(selector)`

- `selector <string>` 选择器,参考[CSS_Selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- 此方法在页面内执行 `document.querySelectorAll`。如果没有元素匹配指定选择器，返回值是 []。
- `page.mainFrame().$$(selector)` 的简写。

### `page.$eval(selector, pageFunction[, ...args])`

- `selector <string>` 选择器,参考[CSS_Selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- `pageFunction <function>` 在浏览器实例上下文中要执行的方法
- `...args <...Serializable|JSHandle>` 要传给 pageFunction 的参数。（比如你的代码里生成了一个变量，在页面中执行方法时需要用到，可以通过这个 args 传进去）
- 此方法在页面内执行 `document.querySelector`，然后把匹配到的元素作为第一个参数传给 `pageFunction`。
- `page.mainFrame().$eval(selector, pageFunction)` 的简写。

```js
const searchValue = await page.$eval('#search', el => el.value);
const preloadHref = await page.$eval('link[rel=preload]', el => el.href);
const text = await page.$eval('.text', el => el.textContent);
const html = await page.$eval('.main-container',e => e.outerHTML);
```

### `page.$$eval(selector, pageFunction[, ...args])`

- `selector <string>` 选择器,参考[CSS_Selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)
- `pageFunction <function>` 在浏览器实例上下文中要执行的方法
- `...args <...Serializable|JSHandle>` 要传给 pageFunction 的参数。（比如你的代码里生成了一个变量，在页面中执行方法时需要用到，可以通过这个 args 传进去）
- 此方法在页面内执行 `Array.from(document.querySelectorAll(selector))`，然后把匹配到的元素数组作为第一个参数传给 `pageFunction`。

```js
const divCount = await page.$$eval('div', divs => divs.length);
const options = await page.$$eval('div > span.options', options => options.map(option => option.textContent))
```

### `page.$x(expression)`

- `expression <string>` XPath表达式，参考： [evaluate](https://developer.mozilla.org/en-US/docs/Web/API/Document/evaluate).
- 返回: `<Promise<Array<ElementHandle>>>`
- 此方法解析指定的XPath表达式。
- `document.evaluate("/html/body//h2", document, null, XPathResult.ANY_TYPE, null)`
- `page.mainFrame().$x(expression)` 的简写。

### `page.evaluate(pageFunction[, ...args])`

- `pageFunction <function|string>` 要在页面实例上下文中执行的方法
- `...args <...Serializable|JSHandle>` 要传给 pageFunction 的参数
- 返回: `<Promise<Serializable>>` pageFunction执行的结果
- 如果`pageFunction`返回的是不能`JSON`序列化的值，将返回undefined,比如:`JSON: -0, NaN, Infinity, -Infinity`

```js
const result = await page.evaluate(x => {
  return Promise.resolve(8 * x);
}, 7);
console.log(result); // prints "56"
```

### `page.waitForSelector(selector[, options])`

- `selector <string>` 要等待的元素选择器
- `options <Object>` 可选参数：
  - `visible <boolean>` 等元素出现在dom中并且可以看到, 比如。 没有 display: none 或者 visibility: hidden 样式。 默认是 false。
  - `hidden <boolean>` 等元素在dom中消失或看不到, 比如。 有 display: none 或者 visibility: hidden 样式。 默认是 false。
  - `timeout <number>` 最大等待时间，单位是毫秒，默认是30000 (30 seconds)，传0表示不会超时
- `page.mainFrame().waitForSelector(selector[, options])` 的简写

```js
  page
    .waitForSelector('img')
    .then(() => console.log('First URL with image: ' + currentURL));
```

### `page.waitForXPath(xpath[, options])`

- `xpath <string>` 要等待的元素的xpath
- `options <Object>` 可选参数：
  - `visible <boolean>` 等元素出现在dom中并且可以看到, 比如. 没有 display: none 或者 visibility: hidden 样式. 默认是 false.
  - `hidden <boolean>` 等元素在dom中消失或看不到, 比如. 有 display: none 或者 visibility: hidden 样式. 默认是 false.
  - `timeout <number>` 最大等待时间，单位是毫秒，默认是30000 (30 seconds)，传0表示不会超时
- `page.mainFrame().waitForXPath(xpath[, options])` 的简写

```js
page
    .waitForXPath('//img')
    .then(() => console.log('First URL with image: ' + currentURL));
```
