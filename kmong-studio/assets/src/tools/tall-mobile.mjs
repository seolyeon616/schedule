// Render a tall board at 1x (700px wide) for sharing/preview: PAGE=apple.html ID=apple-full OUT=../apple/apple-full-mobile.jpg
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";
const here = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const p = await b.newPage({ deviceScaleFactor: 1, viewport: { width: 900, height: 900 } });
await p.goto("file://" + path.join(here, process.env.PAGE || "apple.html"));
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
await p.locator("#" + (process.env.ID || "apple-full")).screenshot({ path: path.resolve(here, process.env.OUT || "../apple/apple-full-mobile.jpg"), type: "jpeg", quality: 88 });
await b.close();
