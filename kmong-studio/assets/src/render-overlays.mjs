// Renders overlays.html sections to transparent 1920x1080 PNGs for compositing.
import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";
const here = path.dirname(fileURLToPath(import.meta.url));
const out = process.argv[2] || path.resolve(here, "../brand");
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ deviceScaleFactor: 1, viewport: { width: 1920, height: 1920 } });
await page.goto("file://" + path.join(here, process.env.OVL || "overlays.html"));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);
for (const id of await page.$$eval("section", (els) => els.map((e) => e.id))) {
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.locator("#" + id).screenshot({ path: path.join(out, id + ".png"), omitBackground: true });
  console.log("rendered", id);
}
await browser.close();
