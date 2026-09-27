// Read-only DOM/mobile probe (Gate G5 baseline). Usage: PROBE_DATE=$(date +%F) node dom_probe.js
// Needs Playwright (global) and Chromium at /opt/pw-browsers; the proxy CA must be in the NSS store (~/.pki/nssdb).
const fs = require('fs'), path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const ROOT = path.resolve(__dirname, '../..');
const cfg = JSON.parse(fs.readFileSync(ROOT + '/remediation/verification/checks.json'));
const DATE = process.env.PROBE_DATE;
const SHOTS = { medical_fees: 'S30-medical-fees-mobile', payment_policy: 'S31-payment-policy-mobile',
  emgms: 'S32-emgms-mobile', medicine: 'S33-medicine-admission-mobile', calendar: 'S34-admissions-calendar-mobile',
  freshman: 'S35-freshman-mobile' };
const VPS = [{ w: 390, h: 844, mobile: true }, { w: 1366, h: 768, mobile: false }];
function measure() {
  const vw = document.documentElement.clientWidth;
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')];
  const visHeads = heads.filter(vis).map(h => ({ level: +h.tagName[1], text: h.innerText.trim().slice(0, 80) }));
  const skips = [];
  for (let i = 1; i < visHeads.length; i++) if (visHeads[i].level > visHeads[i-1].level + 1)
    skips.push(`h${visHeads[i-1].level}→h${visHeads[i].level} ("${visHeads[i].text}")`);
  const scrollAnc = e => { for (let p = e.parentElement; p; p = p.parentElement) {
    const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll') return true; } return false; };
  const tables = [...document.querySelectorAll('table')].filter(vis).map(t => {
    const r = t.getBoundingClientRect(); return { width: Math.round(r.width), right: Math.round(r.right), in_scroll_container: scrollAnc(t) }; })
    .filter(t => t.width > vw || t.right > vw + 1);
  const wide = [...document.body.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect();
    return r.width > 0 && r.right > vw + 1 && vis(e) && !scrollAnc(e); }).slice(0, 5)
    .map(e => `${e.tagName.toLowerCase()}${e.id ? '#' + e.id : ''}${e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : ''} right=${Math.round(e.getBoundingClientRect().right)}`);
  const imgs = [...document.querySelectorAll('img')];
  const links = [...document.querySelectorAll('a[href]')];
  const hash = links.filter(a => a.getAttribute('href').trim() === '#');
  const http = links.filter(a => /^http:\/\//i.test(a.getAttribute('href').trim())).map(a => ({ text: a.innerText.trim().slice(0, 60), href: a.getAttribute('href').trim() }));
  const applyRe = /apply|قدّم|قدم/i;
  const apply = [...document.querySelectorAll('a,button,input[type=submit],input[type=button]')]
    .filter(e => applyRe.test(e.innerText || e.value || ''))
    .map(e => ({ tag: e.tagName.toLowerCase(), text: (e.innerText || e.value).trim().replace(/\s+/g, ' ').slice(0, 80),
      href: e.getAttribute('href'), onclick: e.getAttribute('onclick'), visible: vis(e) }));
  return { lang: document.documentElement.getAttribute('lang'), dir: document.documentElement.getAttribute('dir'),
    body_dir: document.body.getAttribute('dir'), computed_direction: getComputedStyle(document.body).direction,
    title: document.title, viewport_width: vw, scroll_width: document.documentElement.scrollWidth,
    horizontal_overflow: document.documentElement.scrollWidth > vw, overflowing_elements_sample: wide,
    tables_wider_than_viewport: tables, h1_count_dom: document.querySelectorAll('h1').length,
    h1_count_visible: visHeads.filter(h => h.level === 1).length, h1_texts: visHeads.filter(h => h.level === 1).map(h => h.text),
    heading_outline: visHeads.map(h => 'h' + h.level).join(' '), heading_skips: skips,
    images_total: imgs.length, images_missing_alt_attr: imgs.filter(i => !i.hasAttribute('alt')).map(i => (i.getAttribute('src') || '').slice(0, 120)),
    images_empty_alt: imgs.filter(i => i.getAttribute('alt') === '').length,
    links_total: links.length, links_hash_only: hash.length, links_hash_texts: [...new Set(hash.map(a => a.innerText.trim().slice(0, 40)))].slice(0, 15),
    links_http: http, apply_controls: apply };
}
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    proxy: { server: process.env.HTTPS_PROXY } });
  const out = { run_utc: new Date().toISOString(), tool: 'Playwright ' + require('/opt/node22/lib/node_modules/playwright/package.json').version + ' / Chromium headless',
    method: 'read-only: page.goto + DOM reads; no clicks, no form input', pages: {} };
  for (const [key, url] of Object.entries(cfg.pages)) {
    out.pages[key] = { url, viewports: {} };
    for (const vp of VPS) {
      const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, isMobile: vp.mobile, hasTouch: vp.mobile, deviceScaleFactor: 1,
        userAgent: vp.mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
      const page = await ctx.newPage();
      const rec = {};
      try {
        const resp = await page.goto(url, { waitUntil: 'load', timeout: 60000 });
        await page.waitForTimeout(key === 'portal' ? 6000 : 2500);
        rec.status = resp && resp.status(); rec.final_url = page.url();
        rec.redirected_to_login = /login|signin|sso|auth/i.test(new URL(page.url()).pathname);
        if (key === 'portal' && rec.redirected_to_login) { rec.skipped = 'portal redirected to login'; }
        else Object.assign(rec, await page.evaluate(measure));
        if (vp.mobile && cfg.render && cfg.render.includes(key) && !rec.skipped) {
          const txt = await page.evaluate(() => document.body.innerText + ' ' + [...document.querySelectorAll('[href],[src]')].map(e => e.getAttribute('href') || e.getAttribute('src')).join(' '));
          fs.mkdirSync(ROOT + '/remediation/verification/rendered-' + DATE, { recursive: true });
          fs.writeFileSync(ROOT + `/remediation/verification/rendered-${DATE}/${key}.txt`, txt);
        }
        if (vp.mobile && SHOTS[key]) {
          const f = `${ROOT}/evidence/screenshots/${SHOTS[key]}.png`;
          await page.screenshot({ path: f, fullPage: true });
          rec.screenshot = path.relative(ROOT, f);
        }
      } catch (e) { rec.error = String(e).slice(0, 300); }
      out.pages[key].viewports[`${vp.w}x${vp.h}`] = rec;
      console.log(key, `${vp.w}`, rec.status, rec.error || '', rec.horizontal_overflow);
      await ctx.close();
    }
  }
  await browser.close();
  fs.writeFileSync(`${ROOT}/evidence/dom-probes-${DATE}.json`, JSON.stringify(out, null, 2));
})();
