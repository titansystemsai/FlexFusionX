// Screenshot every homepage section at several viewport sizes -> tools/review/<w>x<h>_<section>.jpg
import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const dir = dirname(fileURLToPath(import.meta.url));
const page = pathToFileURL(join(dir, "preview.html")).href;
const port = 9335;
const proc = spawn("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", ["--headless=new","--disable-gpu","--hide-scrollbars",`--remote-debugging-port=${port}`,`--user-data-dir=${join(dir,"edge-prof")}`,"about:blank"],{stdio:"ignore"});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let targets; for(let i=0;i<40;i++){try{targets=await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if(targets.some(t=>t.type==="page"))break;}catch{} await sleep(250);}
const ws=new WebSocket(targets.find(t=>t.type==="page").webSocketDebuggerUrl); await new Promise(r=>ws.addEventListener("open",r));
let id=0;const pend=new Map(); ws.addEventListener("message",e=>{const m=JSON.parse(e.data); if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
const waitReady=async()=>{for(let i=0;i<60;i++){const r=(await send("Runtime.evaluate",{expression:"document.readyState==='complete'&&!!document.getElementById('xstage')",returnByValue:true})).result.result.value; if(r)return true; await sleep(500);} return false;};
await send("Page.enable");
// warm-up load so the first size isn't captured blank
await send("Page.navigate",{url:page}); await waitReady(); await sleep(900);
const sizes=(process.argv[2]||"1280x720,1366x768,1536x864,1920x1080,2560x1440,1024x768,768x1024,390x844").split(",").map(s=>s.split("x").map(Number));
const secs=[["hero","window.scrollTo(0,0)"],["services","S('services')"],["why1","window.scrollTo(0,document.getElementById('why').offsetTop)"],["why2","window.scrollTo(0,document.getElementById('why').offsetTop+innerHeight)"],["approach","S('approach')"],["about","S('about')"],["partners","S('partners')"],["book","S('book')"],["contact","S('contact')"],["faq","S('faq')"],["footer","window.scrollTo(0,document.body.scrollHeight)"]];
for(const [w,h] of sizes){
  await send("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<=820});
  await send("Page.navigate",{url:page}); await waitReady(); await sleep(900);
  await send("Runtime.evaluate",{expression:"window.S=id=>window.scrollTo(0,document.getElementById(id).getBoundingClientRect().top+scrollY);document.documentElement.style.scrollBehavior='auto';document.documentElement.style.scrollSnapType='none'"});
  for(const [name,js] of secs){
    await send("Runtime.evaluate",{expression:js}); await sleep(name.startsWith("why")?1500:450);
    const s=await send("Page.captureScreenshot",{format:"jpeg",quality:62});
    writeFileSync(join(dir,"review",`${w}x${h}_${name}.jpg`),Buffer.from(s.result.data,"base64"));
  }
  console.log("done",w,h);
}
ws.close(); proc.kill();
