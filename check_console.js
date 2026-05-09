const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.toString()));
  await page.goto('http://localhost:5174/');
  await new Promise(r => setTimeout(r, 1000));
  // 点击 W01
  await page.evaluate(() => {
    const cards = Array.from(document.querySelectorAll('.module-card'));
    if (cards.length > 0) cards[0].click();
  });
  await new Promise(r => setTimeout(r, 2000));
  await browser.close();
})();
