const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
(async () => {
  const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium', args:['--no-sandbox'], proxy:{server:process.env.HTTPS_PROXY} });
  const ua='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148';
  const mk = async()=>{const c=await browser.newContext({viewport:{width:390,height:844},userAgent:ua,ignoreHTTPSErrors:true});return c;};
  const out={};
  // 1. Apply CTA landing (GET navigation only; no clicks/forms)
  const applyUrls=['https://www.pmu.edu.sa/apply','https://www.pmu.edu.sa/apply.aspx','https://pmu.edu.sa/apply','https://pmu.edu.sa/Apply','https://www.pmu.edu.sa/Admission/Apply_Now_ADS.aspx','https://pmu.edu.sa/admission/apply_now_ads.aspx','https://pmu.edu.sa/admission/Apply_Now_ADS'];
  out.apply=[];
  for(const u of applyUrls){const c=await mk();const p=await c.newPage();const chain=[];p.on('framenavigated',f=>{if(f===p.mainFrame())chain.push(f.url())});
    try{const r=await p.goto(u,{waitUntil:'networkidle',timeout:45000});await p.waitForTimeout(2500);
      const info=await p.evaluate(()=>({title:document.title,lang:document.documentElement.lang,text:document.body.innerText.slice(0,2500),h:[...document.querySelectorAll('h1,h2')].map(h=>h.textContent.trim()).slice(0,6),forms:document.forms.length,links:[...document.querySelectorAll('a[href]')].map(a=>a.textContent.trim().slice(0,30)+' -> '+a.href).slice(0,25)}));
      out.apply.push({u,status:r&&r.status(),final:p.url(),chain,info});}catch(e){out.apply.push({u,error:String(e).slice(0,200)})}
    await c.close();}
  // 2. welcome page both lang? just rendered text of final (already in apply[0]); 3. degrees rendered list
  {const c=await mk();const p=await c.newPage();await p.goto('https://www.pmu.edu.sa/admission/degrees_programs_fs_ro',{waitUntil:'networkidle',timeout:45000});
   out.degrees=await p.evaluate(()=>{const h=[...document.querySelectorAll('h1,h2,h3,table')];return document.querySelector('.col-md-9, #ContentPlaceHolder_ContentArea, main')?document.body.innerText:document.body.innerText});await c.close();}
  // 4. next-steps overflow culprits
  {const c=await mk();const p=await c.newPage();await p.goto('https://www.pmu.edu.sa/next-steps/',{waitUntil:'networkidle',timeout:45000});
   out.nextSteps=await p.evaluate(()=>{const W=document.documentElement.clientWidth;return {scrollW:document.documentElement.scrollWidth,W,els:[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>W+1).slice(0,12).map(e=>e.tagName+'#'+e.id+'.'+e.className+' right='+Math.round(e.getBoundingClientRect().right)+' text='+e.textContent.trim().slice(0,40))}});await c.close();}
  // 5. credit transfer policy page
  {const c=await mk();const p=await c.newPage();try{const r=await p.goto('https://www.pmu.edu.sa/admission/transfer-student-admission-and-credit-transfer-policy',{waitUntil:'networkidle',timeout:45000});out.credit={status:r.status(),text:await p.evaluate(()=>document.body.innerText.slice(0,6000))};}catch(e){out.credit={error:String(e)}}await c.close();}
  fs.writeFileSync('result3.json',JSON.stringify(out,null,1));await browser.close();console.log('done');
})();
