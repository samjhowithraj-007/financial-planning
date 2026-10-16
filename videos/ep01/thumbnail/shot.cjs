// Screenshot thumb.html (1280x720) and cover.html (1080x1920) with headless Chrome.
// Usage: node shot.cjs <path to puppeteer-core>   (run from this folder)
const puppeteer = require(process.argv[2]);
const { pathToFileURL } = require("url");
const path = require("path");
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new",
    args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  for (const [f, w, h, out] of [["thumb.html", 1280, 720, "thumb-1280x720.png"], ["cover.html", 1080, 1920, "cover-1080x1920.png"]]) {
    await p.setViewport({ width: w, height: h, deviceScaleFactor: 1 });
    await p.goto(pathToFileURL(path.resolve(f)).href, { waitUntil: "networkidle0" });
    await new Promise(r => setTimeout(r, 500));
    await p.screenshot({ path: out });
  }
  await b.close();
})();
