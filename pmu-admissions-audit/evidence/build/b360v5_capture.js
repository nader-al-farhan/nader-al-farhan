// Read-only original captures: navigate, locate published text, record its box, clip a screenshot. No styling changes.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const OUT = process.argv[2]; const JOBS = JSON.parse(fs.readFileSync(process.argv[3])).filter(j => j.url);
const DPR = 1.5, VW = 1280;
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'], proxy: { server: process.env.HTTPS_PROXY } });
  const ctx = await browser.newContext({ viewport: { width: VW, height: 900 }, deviceScaleFactor: DPR, ignoreHTTPSErrors: true, locale: 'en-US', userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36' });
  const ctxNoJs = await browser.newContext({ viewport: { width: VW, height: 900 }, deviceScaleFactor: DPR, ignoreHTTPSErrors: true, javaScriptEnabled: false, locale: 'en-US', userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36' });
  const res = [];
  for (const j of JOBS) {
    const page = await (j.block ? ctxNoJs : ctx).newPage(); const rec = { eid: j.eid, url: j.url, snip: j.snip };
    if (j.block) await page.route(u => u.pathname === '/apply', async r => { const resp = await r.fetch(); let body = await resp.text();
      rec.held = /http-equiv="refresh"/i.test(body); body = body.replace(/<meta[^>]*http-equiv="refresh"[^>]*>/i, '');
      await r.fulfill({ response: resp, body }); });
    try {
      await page.goto(j.url, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => { rec.navnote = String(e).slice(0, 120); });
      await page.waitForTimeout(1500);
      rec.final = page.url(); rec.title = await page.title();
      const info = await page.evaluate(([snip, minH]) => {
        const norm = s => s.replace(/\s+/g, ' ').trim();
        const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT); let best = null;
        while (w.nextNode()) { const el = w.currentNode; if (['SCRIPT','STYLE'].includes(el.tagName)) continue; const t = norm(el.textContent || '');
          if (t.includes(snip)) { if (!best || t.length < norm(best.textContent).length) best = el; } }
        if (!best) return null;
        let revealed = false, a = best;
        while (a && a !== document.body) { if (getComputedStyle(a).display === 'none') { a.style.display = 'block'; revealed = true; } a = a.parentElement; }
        let ctxEl = best; while (ctxEl.parentElement && ctxEl.getBoundingClientRect().height < minH && ctxEl.parentElement !== document.body) ctxEl = ctxEl.parentElement;
        ctxEl.scrollIntoView({ block: 'center' });
        let b = best.getBoundingClientRect(); const c = ctxEl.getBoundingClientRect();
        const tw = document.createTreeWalker(best, NodeFilter.SHOW_TEXT);
        while (tw.nextNode()) { const n = tw.currentNode, k = n.data.replace(/\s+/g, ' ').indexOf(snip), k2 = n.data.indexOf(snip);
          if (k2 >= 0) { const r = document.createRange(); r.setStart(n, k2); r.setEnd(n, k2 + snip.length); const rr = r.getBoundingClientRect(); if (rr.width > 0) { b = rr; } break; } }
        return { revealed, box: { x: b.x, y: b.y, w: b.width, h: b.height }, ctx: { x: c.x, y: c.y, w: c.width, h: c.height }, scrollY: window.scrollY, tag: best.tagName };
      }, [j.snip, j.minH || 0]);
      if (!info) rec.found = false; else {
        rec.found = true; Object.assign(rec, info); await page.waitForTimeout(300);
        const sy = await page.evaluate(() => window.scrollY);
        rec.doc = { box: { x: info.box.x, y: info.box.y + sy, w: info.box.w, h: info.box.h }, ctx: { x: info.ctx.x, y: info.ctx.y + sy, w: info.ctx.w, h: info.ctx.h } };
        rec.at = new Date().toISOString();
        await page.screenshot({ path: `${OUT}/${j.eid}_page.png`, fullPage: true });
      }
    } catch (e) { rec.error = String(e).slice(0, 200); }
    res.push(rec); await page.close(); console.log(j.eid, rec.found, rec.revealed || '', rec.final, rec.error || '');
  }
  fs.writeFileSync(`${OUT}/capture.json`, JSON.stringify(res, null, 1)); await browser.close();
})();
