// Renders brand.html boards to ../brand/<id>.png (logo lockups with transparent background).
import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.resolve(here, "../brand");
fs.mkdirSync(out, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 1000, height: 900 } });
await page.goto("file://" + path.join(here, "brand.html"));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);
await page.addStyleTag({ content: "body{background:transparent!important}" });

for (const id of await page.$$eval("section.board", (els) => els.map((e) => e.id))) {
  const transparent = id.startsWith("logo-");
  const scale = id === "endcard" ? 1 : 2;
  const el = page.locator("#" + id);
  await page.evaluate(() => window.scrollTo(0, 0));
  if (scale === 1) {
    const p2 = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 2000, height: 1200 } });
    await p2.goto("file://" + path.join(here, "brand.html"));
    await p2.evaluate(() => document.fonts.ready);
    await p2.waitForTimeout(300);
    await p2.locator("#" + id).screenshot({ path: path.join(out, id + ".png") });
    await p2.close();
  } else {
    await el.screenshot({ path: path.join(out, id + ".png"), omitBackground: transparent });
  }
  console.log("rendered", id);
}
await browser.close();
