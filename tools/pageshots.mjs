// Screenshot the policy pages at desktop and phone width
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const dir = dirname(fileURLToPath(import.meta.url));
const port = 9336;
const proc = spawn("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", ["--headless=new","--disable-gpu","--hide-scrollbars",`--remote-debugging-port=${port}`,`--user-data-dir=${join(dir,"edge-prof3")}`,"about:blank"],{stdio:"ignore"});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let targets; for(let i=0;i<40;i++){try{targets=await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if(targets.some(t=>t.type==="page"))break;}catch{} await sleep(250);}
const ws=new WebSocket(targets.find(t=>t.type==="page").webSocketDebuggerUrl); await new Promise(r=>ws.addEventListener("open",r));
let id=0;const pend=new Map(); ws.addEventListener("message",e=>{const m=JSON.parse(e.data); if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
await send("Page.enable");
for (const f of ["privacy.html","terms.html"]) for (const [w,h] of [[1440,900],[390,844]]) {
  await send("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<800});
  await send("Page.navigate",{url:pathToFileURL(join(dir,f)).href});
  for(let i=0;i<40;i++){const r=(await send("Runtime.evaluate",{expression:"document.readyState",returnByValue:true})).result.result.value; if(r==="complete")break; await sleep(300);}
  await sleep(800);
  const hs=(await send("Runtime.evaluate",{expression:"document.documentElement.scrollWidth>innerWidth+1",returnByValue:true})).result.result.value;
  const s=await send("Page.captureScreenshot",{format:"jpeg",quality:65});
  writeFileSync(join(dir,"review",`page_${f.replace('.html','')}_${w}.jpg`),Buffer.from(s.result.data,"base64"));
  console.log(f,w,"hscroll:",hs);
}
ws.close(); proc.kill();
