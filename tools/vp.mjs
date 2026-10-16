import { spawn } from "node:child_process";
import { writeFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
const dir = dirname(fileURLToPath(import.meta.url));
const page = pathToFileURL(join(dir, "preview.html")).href;
const port = 9334;
const proc = spawn("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", ["--headless=new","--disable-gpu","--hide-scrollbars",`--remote-debugging-port=${port}`,`--user-data-dir=${join(dir,"edge-prof2")}`,"about:blank"],{stdio:"ignore"});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let targets; for(let i=0;i<40;i++){try{targets=await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if(targets.some(t=>t.type==="page"))break;}catch{} await sleep(250);}
const ws=new WebSocket(targets.find(t=>t.type==="page").webSocketDebuggerUrl); await new Promise(r=>ws.addEventListener("open",r));
let id=0;const pend=new Map(); ws.addEventListener("message",e=>{const m=JSON.parse(e.data); if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id);}});
const send=(method,params={})=>new Promise(r=>{const i=++id;pend.set(i,r);ws.send(JSON.stringify({id:i,method,params}));});
const evalj=async ex=>{const r=(await send("Runtime.evaluate",{expression:ex,returnByValue:true})).result; if(r.exceptionDetails){console.log("EXC",JSON.stringify(r.exceptionDetails).slice(0,600)); return {issues:["probe error"],hscroll:false};} return JSON.parse(r.result.value);};
const waitReady=async()=>{for(let i=0;i<60;i++){const r=(await send("Runtime.evaluate",{expression:"document.readyState==='complete'&&!!document.getElementById('xstage')",returnByValue:true})).result.result.value; if(r)return true; await sleep(500);} return false;};
await send("Page.enable");
await send("Page.navigate",{url:page}); await waitReady(); await sleep(900);
const sizes=[[1280,600],[1280,720],[1366,768],[1440,900],[1536,864],[1920,1080],[2560,1440],[1024,768],[768,1024],[390,844],[360,640]];
const probe=`JSON.stringify((()=>{
 const H=innerHeight, W=innerWidth, out={W,H,hscroll:document.documentElement.scrollWidth>W+1,issues:[]};
 const secs=[...document.querySelectorAll('main>section, main>.xscene')];
 out.secs=secs.map(s=>{const r=s.getBoundingClientRect();return (s.id||s.className.split(' ').slice(-1)[0])+':'+Math.round(r.height)});
 // clipped content inside fixed-height, overflow-hidden containers
 const checks=[['hero','.hero .in'],['services','#services .wrap'],['about','#about .copy'],['partners','#partners .plist-wrap'],['contact','#contact .fbody'],['contactcard','#contact .fcard']];
 for(const [n,sel] of checks){const el=document.querySelector(sel); if(!el)continue; const sec=el.closest('section'); const sr=sec.getBoundingClientRect(), er=el.getBoundingClientRect();
   if(el.scrollHeight>el.clientHeight+2 && !sec.classList.contains('grow')) out.issues.push(n+': CLIPPED '+(el.scrollHeight-el.clientHeight)+'px');
   if(er.bottom>sr.bottom+1||er.top<sr.top-1) out.issues.push(n+': outside section by '+Math.round(Math.max(er.bottom-sr.bottom,sr.top-er.top))+'px');}
 // xscene text must fit inside the sticky stage
 const st=document.getElementById('xstage'); if(getComputedStyle(st).position==='sticky'){ for(const t of document.querySelectorAll('.xtext')){const r=t.getBoundingClientRect(), s=st.getBoundingClientRect(); if(r.height>s.height-72) out.issues.push('xscene text taller than stage: '+Math.round(r.height)+' vs '+Math.round(s.height-72));}}
 // hero copy must clear the fixed nav and the AHPRA line
 const h=document.querySelector('.hero .in').getBoundingClientRect(), reg=document.querySelector('.hero .reg').getBoundingClientRect(); if(h.top<72) out.issues.push('hero copy under nav'); if(h.bottom>reg.top-4 && W>820) out.issues.push('hero copy hits AHPRA line');
 // tall sections (min-height) that exceed the viewport
 secs.forEach(s=>{const r=s.getBoundingClientRect(); if(!s.classList.contains('xscene') && r.height>H+2) out.issues.push((s.id||'section')+' +'+Math.round(r.height-H)+'px'+(s.classList.contains('nosnap')?' (snap off)':' (SNAP ON)'));});
 return out;})())`;
const results=[];
for(const [w,h] of sizes){
  await send("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<=820});
  await send("Page.navigate",{url:page}); await waitReady(); await sleep(900);
  const r=await evalj(probe); results.push(r);
  console.log(`${w}x${h}`, r.hscroll?'HSCROLL':'', r.issues.length?r.issues.join(' | '):'ok');
  }
writeFileSync(join(dir,"vp.json"),JSON.stringify(results,null,1));
ws.close(); proc.kill();
