// Capture the Money Planner on www.paisasamjhoraj.com for the series outro and the in-episode website window.
// Usage (from this folder): node capture-planner.cjs <path to puppeteer-core>
// Writes planner-full.png (1440 wide page at 2x, dark mode, Verma family example loaded), planner-top.png (first
// screen) and planner-boxes.json (where the nav tab, example button and result sections sit, in page CSS px).
const puppeteer = require(process.argv[2]);
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new" });
  const p = await b.newPage();
  await p.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await p.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);
  await p.goto("https://www.paisasamjhoraj.com/#planner", { waitUntil: "networkidle0", timeout: 60000 });
  await new Promise(r => setTimeout(r, 1500));
  // load the Verma family example if the planner offers it
  const loaded = await p.evaluate(() => {
    const btn = [...document.querySelectorAll("button,a")].find(e => /verma/i.test(e.innerText || ""));
    if (btn) { btn.click(); return btn.innerText.trim(); }
    return null;
  });
  await new Promise(r => setTimeout(r, 1200));
  const boxes = await p.evaluate(() => {
    const box = e => { const r = e.getBoundingClientRect(); return { x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height }; };
    const byText = (sel, re) => [...document.querySelectorAll(sel)].filter(e => re.test(e.innerText || "") && e.offsetParent);
    const tab = byText("a", /^\s*Money Planner\s*$/i)[0];
    const ex = byText("button,a", /verma/i)[0];
    const heads = byText("h1,h2,h3,h4,legend,summary,.title,[class*=head]", /.+/).slice(0, 40)
      .map(e => ({ t: e.innerText.trim().slice(0, 60), ...box(e) }));
    const inputs = [...document.querySelectorAll("input,select")].filter(e => e.offsetParent).slice(0, 30)
      .map(e => ({ t: (e.labels && e.labels[0] ? e.labels[0].innerText : e.name || e.id || "").trim().slice(0, 40), ...box(e) }));
    return { page: { w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight },
             tab: tab && box(tab), example: ex && box(ex), heads, inputs };
  });
  boxes.loaded = loaded;
  require("fs").writeFileSync("planner-boxes.json", JSON.stringify(boxes, null, 1));
  await p.screenshot({ path: "planner-top.png" });
  await p.screenshot({ path: "planner-full.png", fullPage: true });
  await b.close();
  console.log("page", boxes.page, "loaded:", loaded, "heads:", boxes.heads.length);
})();
