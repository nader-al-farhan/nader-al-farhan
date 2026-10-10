const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox'],proxy:{server:process.env.HTTPS_PROXY}});
 const ua='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148';
 const ctx=await browser.newContext({viewport:{width:390,height:844},userAgent:ua,ignoreHTTPSErrors:true});
 const out={};
 const p=await ctx.newPage();
 await p.goto('https://www.pmu.edu.sa/admission/degrees_programs_fs_ro',{waitUntil:'networkidle',timeout:45000});
 const grab=()=>p.evaluate(()=>[...document.querySelectorAll('table')].map(t=>t.innerText.replace(/\s+/g,' ').trim()).filter(Boolean));
 for(const label of ['Undergraduate Programs','Graduate Programs']){
   try{await p.getByText(label,{exact:true}).first().click({timeout:5000});await p.waitForTimeout(800);}catch(e){out['err_'+label]=String(e).slice(0,100)}
   out[label]=await p.evaluate(()=>[...document.querySelectorAll('h3,h4,table')].filter(e=>e.offsetParent!==null).map(e=>e.tagName+': '+e.innerText.replace(/\s+/g,' ').trim().slice(0,200)));
 }
 // link status check over hrefs from key admission pages
 const pages=['https://www.pmu.edu.sa/admission/admission','https://www.pmu.edu.sa/admission/undergraduate_programs_admission','https://www.pmu.edu.sa/admission/international_students','https://www.pmu.edu.sa/admission/admission_graduate_degree_programs'];
 const hrefs=new Set();
 for(const u of pages){const q=await ctx.newPage();await q.goto(u,{waitUntil:'networkidle',timeout:45000});
   (await q.evaluate(()=>[...document.querySelectorAll('a[href]')].map(a=>a.href))).forEach(h=>{if(/^https?:\/\/(www\.)?pmu\.edu\.sa\/(admission|Admission|apply|next|About)/i.test(h))hrefs.add(h.split('#')[0])});await q.close();}
 out.checked=[];
 const list=[...hrefs];
 for(const h of list){try{const r=await ctx.request.get(h,{maxRedirects:5,timeout:30000});out.checked.push({h,s:r.status(),final:r.url()});}catch(e){out.checked.push({h,err:String(e).slice(0,80)})}}
 fs.writeFileSync('result4.json',JSON.stringify(out,null,1));await browser.close();console.log('done',list.length);
})();
