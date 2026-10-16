// Screenshot the services strip with a given panel open: node tools/panel_shots.mjs WxH idx [idx...]
import { spawn } from "node:child_process"; import { writeFileSync } from "node:fs"; import { join, dirname } from "node:path"; import { fileURLToPath, pathToFileURL } from "node:url";
const dir=dirname(fileURLToPath(import.meta.url)); const page=pathToFileURL(join(dir,"preview.html")).href; const port=9341;
const proc=spawn("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",["--headless=new","--disable-gpu","--hide-scrollbars",`--remote-debugging-port=${port}`,`--user-data-dir=${join(dir,"edge-prof4")}`,"about:blank"],{stdio:"ignore"});
const sleep=ms=>new Promise(r=>setTimeout(r,ms)); let t; for(let i=0;i<40;i++){try{t=await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if(t.some(x=>x.type==="page"))break;}catch{} await sleep(250);}
const ws=new WebSocket(t.find(x=>x.type==="page").webSocketDebuggerUrl); await new Promise(r=>ws.addEventListener("open",r));
let id=0;const pend=new Map(); ws.addEventListener("message",e=>{const m=JSON.parse(e.data); if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
const ev=ex=>send("Runtime.evaluate",{expression:ex,returnByValue:true});
const [w,h]=process.argv[2].split("x").map(Number); const idxs=process.argv.slice(3).map(Number);
await send("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<=820}); await send("Page.navigate",{url:page}); await sleep(3500);
for(const k of idxs){
  await ev(`document.documentElement.style.scrollBehavior='auto';window.scrollTo(0,document.getElementById('services').offsetTop);var ps=document.querySelectorAll('#strip .panel');ps[${k}].dispatchEvent(new MouseEvent('mouseenter',{bubbles:true}));ps[${k}].focus();if(window.innerWidth<=860)ps[${k}].scrollIntoView({inline:'start',block:'nearest'});`);
  await sleep(1400); const img=await send("Page.captureScreenshot",{format:"jpeg",quality:70});
  writeFileSync(join(dir,"audit",`panel_${w}x${h}_${k}.jpg`),Buffer.from(img.result.data,"base64"));
}
ws.close(); proc.kill();
