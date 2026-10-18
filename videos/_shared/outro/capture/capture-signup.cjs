// Capture the "Get new lessons by email" sign-up box on the www.paisasamjhoraj.com homepage for the series outro (step 6).
// Usage (from this folder): node capture-signup.cjs <path to puppeteer-core>
// Writes home-full.png (1440 wide homepage at 2x, dark mode) and signup-boxes.json (heading text, email input and
// Notify me button, in page CSS px). Only looks at the form: never types into it or submits it.
const puppeteer = require(process.argv[2]);
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await p.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);
  await p.goto("https://www.paisasamjhoraj.com/", { waitUntil: "networkidle0", timeout: 60000 });
  await new Promise(r => setTimeout(r, 1500));
  // scroll through once so lazy / reveal-on-scroll content is painted, then back to the top
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
  await new Promise(r => setTimeout(r, 800));
  const boxes = await p.evaluate(() => {
    const box = r => ({ x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height });
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let head = null, n;
    while ((n = walker.nextNode())) if (/Get new lessons by email/i.test(n.textContent) && n.parentElement.offsetParent) {
      const i = n.textContent.search(/Get new lessons by email/i), rg = document.createRange();
      rg.setStart(n, i); rg.setEnd(n, i + "Get new lessons by email".length); head = box(rg.getBoundingClientRect()); break; }
    const input = [...document.querySelectorAll("input[type=email],input")].find(e => e.offsetParent && /example\.com|email/i.test(e.placeholder + e.type));
    const btn = [...document.querySelectorAll("button,input[type=submit]")].find(e => e.offsetParent && /notify me/i.test(e.innerText || e.value));
    return { page: { w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight },
             heading: head, input: input && { placeholder: input.placeholder, ...box(input.getBoundingClientRect()) },
             button: btn && box(btn.getBoundingClientRect()) };
  });
  require("fs").writeFileSync("signup-boxes.json", JSON.stringify(boxes, null, 1));
  await p.screenshot({ path: "home-full.png", fullPage: true });
  await b.close();
  console.log(JSON.stringify(boxes));
})();
