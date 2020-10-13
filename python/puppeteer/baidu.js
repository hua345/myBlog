const puppeteer = require("puppeteer");

async function getBaiduLocation(page, href) {
  const response = await page.goto(href);
  const chain = response.request().redirectChain();
  return chain[0].response().headers().location;
}

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
  await page.type("#kw", "js", { delay: 0 });
  const inputElem = await page.$eval("#kw", (el) => el.outerHTML);
  console.log("inputElem", inputElem);
  // 回车
  await page.keyboard.press("Enter");
  await page.waitForSelector("#content_left");
  const result = await page.$$eval("#content_left > .result > h3 > a", (eles) =>
    eles.map((ele) => {
      return { href: ele.href.replace("http:","https:"), content: ele.innerText };
    })
  );
  console.log(result);
  const response = await page.goto(result[0].href);
  const chain = response.request().redirectChain();
  const locationURL = chain[0].response().headers().location;
  const locationURL2 = await getBaiduLocation(page, result[0].href);
  console.log(locationURL,locationURL2);
  for (var elem of result) {
    const location = await getBaiduLocation(page, elem.href);
    elem.location = location;
    console.log(elem)
  }
  await browser.close();
})();
