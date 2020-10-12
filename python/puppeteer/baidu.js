const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://www.baidu.com/");
  // await page.screenshot({
  //   path: "github.png",
  //   type: "png",
  //   fullPage: true,
  //   // 指定区域截图，clip和fullPage两者只能设置一个
  //   // clip: {
  //   //   x: 0,
  //   //   y: 0,
  //   //   width: 1000,
  //   //   height: 40
  //   // }
  // });
  // 获取输入框元素并在输入框内输入
  await page.type("#kw", "nodejs", { delay: 0 });
  const inputElem = await page.$eval("#kw", (el) => el.outerHTML);
  console.log("inputElem", inputElem);
  // 回车
  await page.keyboard.press("Enter");
  await page.waitForSelector("#content_left");
  const result = await page.$$eval("#content_left > .result > h3 > a", eles => eles.map(ele => ele.innerText));
  console.log(result);
  // let iframe = await page.mainFrame();
  // iframe.$$('.result')
  // console.log(iframe.$$('.result'))
  await browser.close();
})();
