// Screenshot cover.html (1080x1920) with headless Chrome. Usage: node shot.cjs <path to puppeteer-core>
const puppeteer = require(process.argv[2]);
const { pathToFileURL } = require("url");
const path = require("path");
(async () => {
  const b = await puppeteer.launch({ executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: "new",
    args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await p.goto(pathToFileURL(path.resolve("cover.html")).href, { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 500));
  await p.screenshot({ path: "cover-1080x1920.png" });
  await b.close();
})();
