// Renders every <section class="board"> in index.html to ../<id>.png at 2x.
// usage: npm i && node render.mjs [id ...]
import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "..");
const only = process.argv.slice(2);

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 900, height: 900 } });
await page.goto("file://" + path.join(here, "index.html"));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);

const ids = await page.$$eval("section.board", (els) => els.map((e) => e.id));
for (const id of ids) {
  if (only.length && !only.includes(id)) continue;
  await page.locator("#" + id).screenshot({ path: path.join(out, id + ".png") });
  console.log("rendered", id);
}
// full-length detail page: all detail sections stacked with no gaps
if (!only.length || only.includes("detail-full")) {
  await page.evaluate(() => {
    const wrap = document.createElement("div");
    wrap.id = "detail-full";
    wrap.style.cssText = "display:flex;flex-direction:column;width:700px";
    document.querySelectorAll("section.detail").forEach((s) => wrap.appendChild(s));
    document.body.appendChild(wrap);
  });
  await page.locator("#detail-full").screenshot({ path: path.join(out, "detail-full.jpg"), type: "jpeg", quality: 90 });
  console.log("rendered detail-full");
}
await browser.close();
