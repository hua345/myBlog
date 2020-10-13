const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch((options = { timeout: 50000 }));
  const page = await browser.newPage();
  await page.goto("https://github.com/trending");
  await page.screenshot({
    path: "github.png",
    type: "png",
    fullPage: true,
    // 指定区域截图，clip和fullPage两者只能设置一个
    // clip: {
    //   x: 0,
    //   y: 0,
    //   width: 1000,
    //   height: 40
    // }
  });
  // await page.waitForSelector(".Box > .Box-row");
  const result = await page.$$eval(".Box > .Box-row > h1", (eles) =>
    eles.map((ele) => ele.innerText)
  );
  console.log(result);

  await browser.close();
})();
