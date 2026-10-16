// Real-time frame capture of the intro over CDP (headless Edge).
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const dir = dirname(fileURLToPath(import.meta.url));
const page = pathToFileURL(join(dir, "preview_home2.html")).href;
const edge = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const port = 9333;
const proc = spawn(edge, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`,
  `--user-data-dir=${join(dir, "edge-prof")}`, "--window-size=1440,900", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let targets;
for (let i = 0; i < 40; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (targets.some(t => t.type === "page")) break; } catch {}
  await sleep(250);
}
const target = targets.find((t) => t.type === "page");
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 0.5, mobile: false });
await send("Page.navigate", { url: page });
const t0 = Date.now();
const ids = ["services","why","why2","faq"];
await sleep(2500);
for (const id of ids) {
  const idx = id === "services" ? 5 : 0;
  const ev = await send("Runtime.evaluate", { expression: "(" + (id==='why2' ? "document.getElementById('why').nextElementSibling" : "document.getElementById('" + id + "')") + ").scrollIntoView({behavior:'instant'}); window.scrollBy(0,-72); document.querySelectorAll('#strip .panel')[" + idx + "].dispatchEvent(new Event('mouseenter')); JSON.stringify([...document.querySelectorAll('main>section')].map(s=>Math.round(s.getBoundingClientRect().height)))" });
  console.log(id, JSON.stringify(ev.result.result));
  await sleep(900);
  const r = await send("Page.captureScreenshot", { format: "jpeg", quality: 70 });
  writeFileSync(join(dir, `s_${id}.jpg`), Buffer.from(r.result.data, "base64"));
}
ws.close(); proc.kill();
