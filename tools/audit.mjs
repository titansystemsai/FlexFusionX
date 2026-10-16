// Fine-toothed layout audit: every section at real-world viewport sizes.
// Usage: node tools/audit.mjs [WxH,WxH,...] [--shots]
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const dir = dirname(fileURLToPath(import.meta.url));
const page = process.env.AUDIT_URL || pathToFileURL(join(dir, "preview.html")).href;
const port = 9337;
const proc = spawn("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", ["--headless=new","--disable-gpu","--hide-scrollbars",`--remote-debugging-port=${port}`,`--user-data-dir=${join(dir,"edge-prof4")}`,"about:blank"],{stdio:"ignore"});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let targets; for(let i=0;i<40;i++){try{targets=await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if(targets.some(t=>t.type==="page"))break;}catch{} await sleep(250);}
const ws=new WebSocket(targets.find(t=>t.type==="page").webSocketDebuggerUrl); await new Promise(r=>ws.addEventListener("open",r));
let id=0;const pend=new Map(); ws.addEventListener("message",e=>{const m=JSON.parse(e.data); if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
const ev=async ex=>{const r=(await send("Runtime.evaluate",{expression:ex,returnByValue:true})).result; if(r.exceptionDetails) return {err:r.exceptionDetails.exception&&r.exceptionDetails.exception.description}; return r.result.value;};
await send("Page.enable");
const waitReady=async()=>{for(let i=0;i<60;i++){if(await ev("document.readyState==='complete'&&!!document.getElementById('xstage')"))return; await sleep(400);}};
await send("Page.navigate",{url:page}); await waitReady(); await sleep(1500);

const arg=process.argv[2]&&!process.argv[2].startsWith("--")?process.argv[2]:null;
const sizes=(arg||[
 "1280x577","1280x657","1366x625","1440x789","1470x835","1512x865","1536x730","1600x789","1728x1001","1920x961","2560x1305",
 "1180x740","1024x695","820x1106","768x954","1024x1294",
 "430x739","390x664","360x640"].join(",")).split(",").map(s=>s.split("x").map(Number));
const shots=process.argv.includes("--shots");
mkdirSync(join(dir,"audit"),{recursive:true});

const probe=`(()=>{
 const H=innerHeight,W=innerWidth,nav=document.getElementById('nav').getBoundingClientRect().height;
 const out={W,H,hscroll:document.documentElement.scrollWidth>W+1,xmode:document.querySelector('.xscene').classList.contains('xstack')?'stacked':'side-by-side',secs:[],issues:[]};
 const vis=e=>{for(let n=e;n&&n!==document.body;n=n.parentElement){const s=getComputedStyle(n);if(s.display==='none'||s.visibility==='hidden'||+s.opacity===0)return false;}const r=e.getBoundingClientRect();if(!(r.width>0&&r.height>0))return false;if(e.tagName!=='DETAILS'&&e.closest('details:not([open])')&&!e.closest('summary'))return false;const strip=e.closest('.strip');if(strip){const sr=strip.getBoundingClientRect();if(r.left>=sr.right-1||r.right<=sr.left+1)return false;}return true};
 let minFont=99,minFontEl='';
 document.querySelectorAll('main h1,main h2,main h3,main p,main li,main a,main span,main dd,main dt,main summary,footer *').forEach(e=>{
   if(!vis(e)||!e.childNodes.length||![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;
   const f=parseFloat(getComputedStyle(e).fontSize); if(f<minFont){minFont=f;minFontEl=(e.className||e.tagName)+': '+e.textContent.trim().slice(0,30)}
   const r=e.getBoundingClientRect(); const clip=e.closest('.strip,.panel'); if(!clip&&(r.right>W+1||r.left<-1)) out.issues.push('text past screen edge: '+e.textContent.trim().slice(0,40));
 });
 out.minFont=minFont+'px ('+minFontEl+')';
 const list=[...document.querySelectorAll('main>section, main>.xscene')];
 for(const s of list){
   const name=s.id||(s.classList.contains('hero')?'hero':s.className.split(' ')[0]);
   const sr=s.getBoundingClientRect();
   const els=[...s.querySelectorAll('h1,h2,h3,p,li,.btn,.panel,.card,.widget,.ckwrap,.apx>div,details,.finfo,.ask,.prow,.xfig img,.portrait,.ph img,.fcard,.strip,.plist')].filter(vis);
   if(name==='why'){ // measure the first exposure only
     const a=s.querySelector('.xl.a'); const ar=a.getBoundingClientRect();
     const ae=[...a.querySelectorAll('h2,li,p,.xfig img')].filter(vis).map(e=>e.getBoundingClientRect());
     const top=Math.min(...ae.map(r=>r.top))-ar.top, bot=ar.bottom-Math.max(...ae.map(r=>r.bottom));
     const img=a.querySelector('.xfig img'); const ir=img.getBoundingClientRect();
     out.secs.push({name:'why(gap)',h:Math.round(ar.height),fill:Math.round(ar.height)>=H-1,topGap:Math.round(top),botGap:Math.round(bot),occ:Math.round((ar.height-top-bot)/ar.height*100),xray:vis(img)?Math.round(ir.width)+'x'+Math.round(ir.height):'hidden'});
     // clipping inside the sticky stage
     if(out.xmode==='side-by-side'){s.querySelectorAll('.xtext').forEach(t=>{const g=t.closest('.xgrid').getBoundingClientRect();const tr=t.getBoundingClientRect();if(tr.top<g.top+nav-2||tr.bottom>g.bottom+1)out.issues.push('x-ray text clipped');});}
     continue;
   }
   if(!els.length){out.secs.push({name,h:Math.round(sr.height)});continue}
   const rs=els.map(e=>e.getBoundingClientRect());
   const top=Math.min(...rs.map(r=>r.top))-sr.top, bot=sr.bottom-Math.max(...rs.map(r=>r.bottom));
   const ov=getComputedStyle(s).overflow==='hidden';
   if(ov){els.forEach((e,k)=>{const r=rs[k];if(r.bottom>sr.bottom+2&&!e.closest('.strip'))out.issues.push(name+': content cut off at bottom ('+(e.className||e.tagName)+')');});}
   if(top<nav-1&&name!=='hero'&&!s.classList.contains('about')&&!s.classList.contains('findus')&&!s.classList.contains('partners'))out.issues.push(name+': content starts under the nav');
   out.secs.push({name,h:Math.round(sr.height),fill:Math.round(sr.height)>=H-1,exact:Math.abs(sr.height-H)<2,topGap:Math.round(top),botGap:Math.round(bot),occ:Math.round((sr.height-Math.max(top,0)-Math.max(bot,0))/sr.height*100)});
 }
 return JSON.stringify(out);
})()`;

const rows=[];
for(const [w,h] of sizes){
  await send("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<=820});
  await send("Page.navigate",{url:page}); await waitReady(); await sleep(1200);
  await ev("document.documentElement.style.scrollBehavior='auto';document.documentElement.style.scrollSnapType='none';window.dispatchEvent(new Event('resize'))");
  await sleep(300);
  const raw=await ev(probe); if(raw&&raw.err){console.log(w,h,"ERR",raw.err);continue}
  const r=JSON.parse(raw); rows.push(r);
  const notFill=r.secs.filter(s=>s.fill===false).map(s=>s.name);
  const sparse=r.secs.filter(s=>s.occ!==undefined&&s.occ<55).map(s=>s.name+' '+s.occ+'%');
  console.log(`${w}x${h} | x-ray ${r.xmode} ${(r.secs.find(s=>s.name==='why(gap)')||{}).xray||''} | min font ${r.minFont}${r.hscroll?' | HSCROLL':''}`);
  if(notFill.length)console.log('   not filling screen:',notFill.join(', '));
  if(sparse.length)console.log('   sparse (<55% used):',sparse.join(', '));
  if(r.issues.length)console.log('   issues:',[...new Set(r.issues)].join(' | '));
  if(shots){
    const ids=["top","services","why","approach","about","partners","book","contact","faq"];
    for(const s of ids){
      await ev(s==="top"?"window.scrollTo(0,0)":`window.scrollTo(0,document.getElementById('${s}').getBoundingClientRect().top+scrollY)`); await sleep(350);
      const img=await send("Page.captureScreenshot",{format:"jpeg",quality:60});
      writeFileSync(join(dir,"audit",`${w}x${h}_${s}.jpg`),Buffer.from(img.result.data,"base64"));
    }
  }
}
writeFileSync(join(dir,"audit","audit.json"),JSON.stringify(rows,null,1));
ws.close(); proc.kill();
