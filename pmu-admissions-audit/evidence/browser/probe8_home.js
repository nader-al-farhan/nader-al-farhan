const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium',proxy:{server:process.env.HTTPS_PROXY}});
  const ctx = await b.newContext({userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',viewport:{width:390,height:844}});
  const p = await ctx.newPage();
  const r = await p.goto('https://www.pmu.edu.sa/default',{waitUntil:'networkidle',timeout:60000});
  const out = {status:r.status(), url:p.url()};
  out.ncaa = await p.evaluate(()=>{const t='All the program learning outcomes are in alignment';
    const els=[...document.querySelectorAll('p,div,span,li')].filter(e=>e.children.length===0&&e.textContent.includes(t));
    return els.map(e=>({vis:!!(e.offsetWidth||e.offsetHeight),cls:e.className,inSlider:!!e.closest('[class*=slick],[class*=carousel],[class*=swiper],[class*=owl]'),text:e.textContent.trim().slice(0,60)}))});
  out.title=await p.title();
  out.overflow = await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  out.lang = await p.evaluate(()=>document.documentElement.lang);
  out.h1 = await p.evaluate(()=>[...document.querySelectorAll('h1')].map(h=>h.textContent.trim().slice(0,60)));
  await p.screenshot({path:'shot_mobile_home.png'});
  require('fs').writeFileSync('result8_home.json',JSON.stringify(out,null,1));
  console.log(JSON.stringify(out,null,1));
  await b.close();
})();
