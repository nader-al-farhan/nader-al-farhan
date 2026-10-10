const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const urls = process.argv.slice(2);
(async () => {
  const proxy = process.env.HTTPS_PROXY;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args:['--no-sandbox'], proxy: proxy ? { server: proxy } : undefined });
  const out = [];
  for (const u of urls) {
    for (const vp of [{n:'mobile',w:390,h:844},{n:'desktop',w:1366,h:900}]) {
      const ctx = await browser.newContext({ viewport:{width:vp.w,height:vp.h}, ignoreHTTPSErrors:true, userAgent: vp.n==='mobile' ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148' : undefined });
      const page = await ctx.newPage();
      const rec = { url:u, viewport:vp.n };
      try {
        const resp = await page.goto(u, { waitUntil:'networkidle', timeout:45000 });
        rec.status = resp && resp.status(); rec.finalUrl = page.url();
        rec.probe = await page.evaluate(() => {
          const q = s => [...document.querySelectorAll(s)];
          const docW = document.documentElement.clientWidth;
          const overflowEls = q('body *').filter(e => { const r=e.getBoundingClientRect(); return r.width>0 && r.right > docW+1; }).slice(0,5).map(e=>e.tagName+'.'+e.className);
          return {
            title: document.title, lang: document.documentElement.lang, dir: document.documentElement.dir || document.body.dir,
            scrollW: document.documentElement.scrollWidth, clientW: docW,
            hOverflow: document.documentElement.scrollWidth > docW+1, overflowSample: overflowEls,
            tables: q('table').map(t=>({w:t.scrollWidth,cw:t.parentElement.clientWidth})),
            headings: q('h1,h2,h3,h4').map(h=>h.tagName+': '+h.textContent.trim().slice(0,60)).slice(0,30),
            imgs: q('img').length, imgsNoAlt: q('img').filter(i=>!i.hasAttribute('alt')).length, imgsEmptyAlt: q('img').filter(i=>i.getAttribute('alt')==='').length,
            metaViewport: (document.querySelector('meta[name=viewport]')||{}).content||null,
            metaDesc: (document.querySelector('meta[name=description]')||{}).content||null,
            canonical: (document.querySelector('link[rel=canonical]')||{}).href||null,
            robots: (document.querySelector('meta[name=robots]')||{}).content||null,
            ctas: q('a').filter(a=>/apply|click here|read more|learn more|admission query|contact|qabool|study in saudi|sadad/i.test(a.textContent)).map(a=>({t:a.textContent.trim().replace(/\s+/g,' ').slice(0,50),h:a.href})).slice(0,40),
            langSwitch: q('a').filter(a=>/عربي|العربية|arabic|english|ar\b/i.test(a.textContent.trim()) && a.textContent.trim().length<15).map(a=>({t:a.textContent.trim(),h:a.href})),
            formCount: q('form').length, inputsNoLabel: q('input:not([type=hidden]),select,textarea').filter(i=>!(i.labels&&i.labels.length) && !i.getAttribute('aria-label') && !i.getAttribute('placeholder')).length,
            links: q('a[href]').length
          };
        });
        if (u.endsWith('/admission/admission') || u.includes('undergraduate_programs_admission')) {
          await page.screenshot({ path:`shot_${vp.n}_${u.split('/').pop()||'root'}.png`, fullPage:false });
        }
      } catch(e) { rec.error = String(e).slice(0,300); }
      out.push(rec); await ctx.close();
    }
  }
  fs.writeFileSync('result.json', JSON.stringify(out,null,1));
  await browser.close();
  console.log('done', out.length);
})();
