// READ-ONLY BFS crawl of the PMU admission section. GET navigation only. No clicks, forms, or logins.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const START = 'https://pmu.edu.sa/admission/admission';
const norm = (u) => { try { const x = new URL(u); if (!/(^|\.)pmu\.edu\.sa$/i.test(x.hostname)) return null;
  let p = x.pathname.replace(/\.aspx$/i,'').replace(/\/+$/,'').toLowerCase(); return 'https://www.pmu.edu.sa'+p; } catch(e){ return null; } };
const inScope = (n) => /^https:\/\/www\.pmu\.edu\.sa\/(admission\/|apply$|next-steps$)/.test(n+'');
const slug = (n) => n.replace('https://www.pmu.edu.sa/','').replace(/[^a-z0-9_-]+/g,'_');
(async () => {
  const browser = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium', args:['--no-sandbox'], proxy:{server:process.env.HTTPS_PROXY} });
  const ctx = await browser.newContext({ viewport:{width:390,height:844}, ignoreHTTPSErrors:true,
    userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148' });
  const queue = [norm(START)], seen = new Set(queue), reg = [], excluded = new Map(), files = new Map();
  const origin = new Map([[queue[0], 'START']]);
  while (queue.length) {
    const n = queue.shift(); const page = await ctx.newPage(); const rec = { url:n, foundOn: origin.get(n) };
    try {
      const r = await page.goto(n, { waitUntil:'networkidle', timeout:60000 });
      await page.waitForTimeout(1200);
      rec.status = r && r.status(); rec.finalUrl = page.url();
      const d = await page.evaluate(() => {
        const clean = s => s.replace(/ /g,' ').replace(/[ \t]+/g,' ').replace(/\n\s*\n+/g,'\n').trim();
        const root = document.body.cloneNode(true);
        root.querySelectorAll('script,style,noscript,nav,footer,header,form[action*="search"]').forEach(e=>e.remove());
        const hidden = [...document.querySelectorAll('[style*="display:none"],[hidden],.collapse:not(.in),.tab-pane')].length;
        return { title: document.title, lang: document.documentElement.lang,
          h: [...document.querySelectorAll('h1,h2,h3,h4')].map(h=>h.tagName+': '+clean(h.textContent)).filter(x=>x.length>4),
          text: clean(root.textContent), hiddenPanels: hidden,
          links: [...document.querySelectorAll('a[href]')].map(a=>({t:clean(a.textContent).slice(0,80),h:a.href})),
          imgs: document.images.length, imgsNoAlt: [...document.images].filter(i=>!i.hasAttribute('alt')).length,
          overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth+1 };
      });
      Object.assign(rec, { title:d.title, lang:d.lang, headings:d.h, chars:d.text.length, hiddenPanels:d.hiddenPanels, imgs:d.imgs, imgsNoAlt:d.imgsNoAlt, overflow:d.overflow });
      fs.writeFileSync('pages/'+slug(n)+'.txt', `URL: ${n}\nFINAL: ${rec.finalUrl}\nTITLE: ${d.title}\nCAPTURED: ${new Date().toISOString()}\n\n${d.text}\n`);
      for (const l of d.links) {
        if (/\.(pdf|docx?|xlsx?|pptx?|zip)(\?|$)/i.test(l.h)) { files.set(l.h, {t:l.t, from:n}); continue; }
        const m = norm(l.h);
        if (!m) { if (/^https?:/.test(l.h)) { const k=l.h.split('#')[0]; if(!excluded.has(k)) excluded.set(k,{t:l.t,from:n,reason:'external host'}); } continue; }
        if (inScope(m)) { if (!seen.has(m)) { seen.add(m); queue.push(m); origin.set(m, n); } }
        else if (!excluded.has(m)) excluded.set(m, {t:l.t, from:n, reason:'internal, outside admission scope'});
      }
    } catch (e) { rec.error = String(e).slice(0,200); }
    reg.push(rec); await page.close(); await new Promise(r=>setTimeout(r,300));
    if (reg.length % 10 === 0) console.log('crawled', reg.length, 'queue', queue.length);
  }
  fs.writeFileSync('register.json', JSON.stringify(reg,null,1));
  fs.writeFileSync('excluded.json', JSON.stringify([...excluded].map(([u,v])=>({url:u,...v})),null,1));
  fs.writeFileSync('files.json', JSON.stringify([...files].map(([u,v])=>({url:u,...v})),null,1));
  await browser.close(); console.log('DONE pages', reg.length, 'excluded', excluded.size, 'files', files.size);
})();
