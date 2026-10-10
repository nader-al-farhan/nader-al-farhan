const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox'],proxy:{server:process.env.HTTPS_PROXY}});
 const ctx=await browser.newContext({viewport:{width:390,height:844},userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',ignoreHTTPSErrors:true});
 for(const u of ['https://www.pmu.edu.sa/admission/fees_tf_ro','https://www.pmu.edu.sa/admission/degrees_programs_fs_ro']){
  const p=await ctx.newPage();await p.goto(u,{waitUntil:'networkidle',timeout:60000});
  const r=await p.evaluate(()=>{
    const clean=s=>s.replace(/\s+/g,' ').trim();
    const tables=[...document.querySelectorAll('table')].map(t=>clean(t.textContent)).filter(x=>x.length>15);
    const panels=[...document.querySelectorAll('.panel, .accordion, .collapse, .tab-pane, .card')].map(e=>clean(e.textContent)).filter(x=>x.length>25&&x.length<4000);
    return {tables:tables.slice(0,25),panels:[...new Set(panels)].slice(0,15)};});
  console.log('=====',u,'tables',r.tables.length,'panels',r.panels.length);
  r.tables.forEach((t,i)=>console.log(' T'+i,t.slice(0,420)));
  if(!r.tables.length) r.panels.forEach((t,i)=>console.log(' P'+i,t.slice(0,420)));
  await p.close();}
 await browser.close();
})();
