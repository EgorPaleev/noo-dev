// Снимки страницы по экрану через Chrome DevTools Protocol (Chromium из кеша Playwright).
// Полностраничный снимок не годится: блоки Reveal проявляются только при входе в экран.
//
// node shot.mjs <url> <папка> [--sizes 1440x900,390x844] [--themes dark,light] [--ys 0,900,1800]
// Пример: node shot.mjs http://localhost:5173/cases/cipr-2026/ /tmp/shots --ys 0,1200,2400
// Без --ys снимает экран через каждые 80% высоты до конца страницы.
import { spawn } from "node:child_process";
import { mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { join } from "node:path";

const [url, outDir, ...rest] = process.argv.slice(2);
if (!url || !outDir) { console.error("node shot.mjs <url> <папка> [--sizes …] [--themes …] [--ys …]"); process.exit(1); }
const flag = (name, fallback) => { const i = rest.indexOf(`--${name}`); return i === -1 ? fallback : rest[i + 1]; };
const sizes = flag("sizes", "1440x900,390x844").split(",").map((s) => s.split("x").map(Number));
const themes = flag("themes", "dark,light").split(",");
const fixedYs = flag("ys", "");

const cache = join(homedir(), ".cache/ms-playwright");
const chromeDir = readdirSync(cache).filter((d) => d.startsWith("chromium-")).sort().pop();
const chromePath = join(cache, chromeDir, "chrome-linux64/chrome");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const port = 9400 + Math.floor(Math.random() * 400);
const chrome = spawn(chromePath, ["--headless=new", `--remote-debugging-port=${port}`, "--no-sandbox", "--hide-scrollbars", `--user-data-dir=${join(tmpdir(), `shot-${Date.now()}`)}`, "about:blank"], { stdio: "ignore" });
let tabs; for (let i = 0; i < 50; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); break; } catch { await sleep(200); } }
const ws = new WebSocket(tabs.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evalJs = async (expr) => (await send("Runtime.evaluate", { expression: expr, returnByValue: true })).result?.result?.value;

mkdirSync(outDir, { recursive: true });
const slug = new URL(url).pathname.replace(/\W+/g, "-").replace(/^-|-$/g, "") || "home";
for (const theme of themes) {
  for (const [w, h] of sizes) {
    await send("Emulation.setDeviceMetricsOverride", { width: w, height: h, deviceScaleFactor: 1, mobile: w < 600 });
    await send("Page.navigate", { url }); await sleep(1200);
    await evalJs(`localStorage.setItem("sovpa-color-mode", "${theme}")`);
    await send("Page.navigate", { url }); await sleep(2500);
    const total = await evalJs("document.documentElement.scrollHeight");
    const overflow = await evalJs("document.documentElement.scrollWidth > innerWidth");
    const ys = fixedYs ? fixedYs.split(",").map(Number) : Array.from({ length: Math.ceil(total / (h * 0.8)) }, (_, i) => Math.round(i * h * 0.8));
    for (const [i, y] of ys.entries()) {
      await evalJs(`window.scrollTo(0, ${y})`); await sleep(1800);
      const shot = await send("Page.captureScreenshot", { format: "png" });
      writeFileSync(join(outDir, `${slug}-${w}-${theme}-${String(i).padStart(2, "0")}.png`), Buffer.from(shot.result.data, "base64"));
    }
    console.log(`${slug} ${w}×${h} ${theme}: ${ys.length} снимков, высота ${total}px, горизонтальная прокрутка: ${overflow ? "ЕСТЬ" : "нет"}`);
  }
}
ws.close(); chrome.kill();
