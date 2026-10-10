const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox'],proxy:{server:process.env.HTTPS_PROXY}});
 const ctx=await browser.newContext({viewport:{width:390,height:844},userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',ignoreHTTPSErrors:true});
 for(const u of ['https://www.pmu.edu.sa/Admission/application_form_MSID_GDP.aspx','https://www.pmu.edu.sa/Admission/Fees_TF_RO.aspx','https://www.pmu.edu.sa/Admission/Application_Form_MBA_GDP.aspx','https://www.pmu.edu.sa/admission/fees_tf_ro','https://www.pmu.edu.sa/admission/application_form_mba_gdp']){
  const p=await ctx.newPage();const t=Date.now();
  try{const r=await p.goto(u,{waitUntil:'domcontentloaded',timeout:90000});await p.waitForTimeout(1500);
   console.log(r.status(),Date.now()-t,'ms',u,'->',p.url(),'|',(await p.title()).slice(0,60),'|',(await p.evaluate(()=>document.body.innerText.length)));
   if(/fees_tf|mba_gdp/i.test(u)&&!/MSID/.test(u)) console.log((await p.evaluate(()=>document.body.innerText)).replace(/\s+/g,' ').slice(0,700));
  }catch(e){console.log('ERR',u,String(e).slice(0,120))}
  await p.close();}
 await browser.close();
})();
