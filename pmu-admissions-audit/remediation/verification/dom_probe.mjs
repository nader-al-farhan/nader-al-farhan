// Gate G5 baseline probe: read-only DOM / mobile measurements of the core admissions pages.
// Loads each page in checks.json "pages" at 390x844 and 1366x768, never clicks, types or submits.
// Usage: NODE_PATH=$(npm root -g) node dom_probe.mjs <out.json> <screenshot-dir>
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const HERE = path.dirname(new URL(import.meta.url).pathname);
const cfg = JSON.parse(fs.readFileSync(path.join(HERE, "checks.json"), "utf8"));
const [out, shotDir] = process.argv.slice(2);
const VIEWPORTS = { mobile: { width: 390, height: 844 }, desktop: { width: 1366, height: 768 } };
const SHOTS = {
  medical_fees: "S30-medical-fees-fullpage.png",
  payment_policy: "S31-payment-policy-fullpage.png",
  emgms: "S32-emgms-fullpage.png",
  medicine: "S33-medicine-admission-fullpage.png",
  calendar: "S34-admissions-calendar-fullpage.png",
  freshman: "S35-freshman-fullpage.png",
};

function measure(strings) {
  const vw = document.documentElement.clientWidth;
  const clip = (s) => (s || "").replace(/\s+/g, " ").trim().slice(0, 80);
  const heads = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].filter((h) => h.offsetParent !== null || h.getClientRects().length);
  const skips = [];
  heads.forEach((h, i) => {
    const lvl = +h.tagName[1], prev = i ? +heads[i - 1].tagName[1] : 0;
    if (lvl > prev + 1) skips.push({ from: prev ? `h${prev}` : "(start)", to: h.tagName.toLowerCase(), text: clip(h.textContent) });
  });
  const imgs = [...document.images];
  const links = [...document.querySelectorAll("a[href]")];
  const applyRe = /apply|قدّم|قدم الآن|قدم هنا/i;
  const apply = [...document.querySelectorAll("a, button, input[type=submit], input[type=button]")]
    .filter((e) => applyRe.test(e.textContent || e.value || ""))
    .map((e) => ({ tag: e.tagName.toLowerCase(), text: clip(e.textContent || e.value),
                   href: e.getAttribute("href"), resolved: e.href || null,
                   form_action: e.form ? e.form.getAttribute("action") : null,
                   visible: !!e.getClientRects().length }));
  const wide = [...document.querySelectorAll("table")].map((t) => ({ w: Math.round(t.getBoundingClientRect().width), sw: t.scrollWidth }))
    .filter((t) => t.w > vw || t.sw > vw);
  return {
    final_url: location.href,
    title: document.title,
    lang: document.documentElement.getAttribute("lang"),
    dir: document.documentElement.getAttribute("dir"),
    computed_dir: getComputedStyle(document.documentElement).direction,
    client_width: vw,
    scroll_width: document.documentElement.scrollWidth,
    horizontal_overflow: document.documentElement.scrollWidth > vw,
    tables_total: document.querySelectorAll("table").length,
    tables_wider_than_viewport: wide,
    h1_count: document.querySelectorAll("h1").length,
    h1_text: [...document.querySelectorAll("h1")].map((h) => clip(h.textContent)),
    heading_sequence: heads.map((h) => h.tagName.toLowerCase()).join(" "),
    heading_skips: skips,
    images_total: imgs.length,
    images_missing_alt: imgs.filter((i) => !i.hasAttribute("alt")).map((i) => i.getAttribute("src")),
    images_empty_alt: imgs.filter((i) => i.getAttribute("alt") === "").length,
    links_total: links.length,
    links_hash: links.filter((a) => a.getAttribute("href").trim() === "#").length,
    links_http: [...new Set(links.map((a) => a.getAttribute("href").trim()).filter((h) => /^http:\/\//i.test(h)))],
    apply_controls: apply,
    // rendered-text presence of this page's checks.json forbidden strings only (no full text kept)
    rendered_forbidden: Object.fromEntries(strings.map((t) => [t, (document.body ? document.body.innerText : "").includes(t)])),
  };
}

const browser = await chromium.launch();
const results = { run_at: new Date().toISOString(), tool: "playwright chromium (headless)", viewports: VIEWPORTS, pages: {} };
for (const [key, url] of Object.entries(cfg.pages)) {
  results.pages[key] = { url };
  for (const [vname, vp] of Object.entries(VIEWPORTS)) {
    const ctx = await browser.newContext({ viewport: vp, userAgent: "PMU-Admissions-G5-Probe/1.0 (read-only audit)" });
    const page = await ctx.newPage();
    try {
      const resp = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
      await page.waitForLoadState("networkidle", { timeout: 20000 }).catch(() => {});
      const m = await page.evaluate(measure, cfg.forbidden.filter((c) => c.page === key).map((c) => c.text));
      m.status = resp ? resp.status() : null;
      m.redirected_to_login = /login|signin|sso/i.test(m.final_url);
      results.pages[key][vname] = m;
      if (vname === "desktop" && SHOTS[key] && shotDir) {
        await page.screenshot({ path: path.join(shotDir, SHOTS[key]), fullPage: true });
        results.pages[key].screenshot = SHOTS[key];
      }
    } catch (e) {
      results.pages[key][vname] = { error: String(e).slice(0, 300) };
    }
    await ctx.close();
  }
}
await browser.close();
fs.writeFileSync(out, JSON.stringify(results, null, 2));
console.log(`wrote ${out}`);
