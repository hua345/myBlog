# [puppeteer](https://github.com/puppeteer/puppeteer)

- [https://github.com/puppeteer/puppeteer](https://github.com/puppeteer/puppeteer)
- [https://pptr.dev/](https://pptr.dev/)

> Puppeteer 是一个 Node 库，它提供了高级的 API 并通过 DevTools 协议来控制 Chrome.简单理解成我们日常使用的 Chrome 的无界面版本，可以使用 js 接口进行进行操控。意味凡是 Chrome 浏览器能干的事情，Puppeteer 都能出色的完成

- 生成网页截图或者 PDF
- 抓取单页应用(SPA)执行并渲染
- 自动执行表单提交，UI 测试，键盘输入，模拟用户登录等。
- 创建最新的自动化测试环境。使用最新的 JavaScript 和浏览器功能，直接在最新版本的 Chrome 中运行测试。

## 安装

```bash
# 默认会下载一个最新版本的Chromium
cnpm i puppeteer -S
```

## puppeteer 示例

`Puppeteer` 官方推荐的是使用高版本 `Node` 的 `async/await` 语法

```js
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://www.baidu.com");
  await page.screenshot({ path: "baidu.png" });

  await browser.close();
})();
```

```js
// headless默认为true
const browser = await puppeteer.launch({ headless: false });
// 使执行本地版本的Chrome或者Chromium
const browser = await puppeteer.launch({ executablePath: "/path/to/Chrome" });
```

- `page.type` 获取输入框焦点并输入文字
- `page.keyboard.press` 模拟键盘按下某个按键，目前 mac 上组合键无效为已知 bug
- `page.waitFor` 页面等待，可以是时间、某个元素、某个函数
- `page.frames()` 获取当前页面所有的 iframe，然后根据 iframe 的名字精确获取某个想要的 iframe
- `iframe.evaluate()` 在浏览器中执行函数，相当于在控制台中执行函数，返回一个 Promise
- `Array.from` 将类数组对象转化为对象
- `page.click()` 点击一个元素
- `iframe.$eval()` 相当于在 iframe 中运行 `document.queryselector` 获取指定元素，并将其作为第一个参数传递
- `iframe.$$eval` 相当于在 iframe 中运行 `document.querySelectorAll` 获取指定元素数组，并将其作为第一个参数传递
