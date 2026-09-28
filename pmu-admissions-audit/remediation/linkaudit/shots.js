// Read-only screenshots for the link audit. Loads pages through curlroute (no browser
// network access), never clicks, types or submits. Staff-list pages are not captured
// (they show personal names).
const { chromium } = require("playwright");
const fs = require("fs");
const { attach } = require("./curlroute");
const HUB = "https://pmu.edu.sa/admission/admission";
const ids = JSON.parse(fs.readFileSync("ids.json", "utf8"));        // [{id, i, abs, region, visible}]
const res = JSON.parse(fs.readFileSync("checks-result.json", "utf8")).results;
const OUT = "shots"; fs.mkdirSync(OUT, { recursive: true });
const HL = { "C33": ["Visting"] };                                 // extra highlights on the hub

async function badges(page, list, extra) {
  await page.evaluate(({ list, extra }) => {
    const A = [...document.querySelectorAll("a")];
    for (const { id, i, flag } of list) {
      const a = A[i]; if (!a) continue;
      const r = a.getBoundingClientRect(); if (!r.width) continue;
      const b = document.createElement("div");
      b.textContent = id;
      Object.assign(b.style, { position: "absolute", left: (r.left + scrollX - 4) + "px", top: (r.top + scrollY - 2) + "px",
        transform: "translateX(-100%)", font: "bold 11px/1 Arial,sans-serif", padding: "3px 4px", borderRadius: "3px",
        background: flag ? "#c62828" : "#1a237e", color: "#fff", zIndex: 99999, pointerEvents: "none" });
      document.body.appendChild(b);
      a.style.outline = flag ? "2px solid #c62828" : "1px dashed #1a237e";
    }
    for (const t of extra) for (const a of A) if (a.textContent.includes(t)) a.style.background = "#ffeb3b";
  }, { list, extra });
}

async function mark(page, texts) {
  // outline the smallest element containing each issue string; scroll the first into view
  return page.evaluate((texts) => {
    const found = [];
    for (const t of texts) {
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let n; while ((n = w.nextNode())) {
        if (n.nodeValue.includes(t) && n.parentElement.offsetParent !== null) {
          const el = n.parentElement; el.style.outline = "3px solid #c62828"; el.style.background = "#fff59d";
          found.push({ t, y: el.getBoundingClientRect().top + scrollY }); break;
        }
      }
    }
    if (found.length) window.scrollTo(0, Math.max(0, found[0].y - 250));
    return found.map(f => f.t);
  }, texts);
}

(async () => {
  const b = await chromium.launch();
  const meta = {};
  const ONLY = (process.env.ONLY || "").split(",").filter(Boolean);
  if (ONLY.length) Object.assign(meta, JSON.parse(fs.readFileSync("page-meta.json", "utf8")));
  // 1) hub, annotated, desktop + mobile full page
  if (!ONLY.length) for (const [name, vp] of [["hub-annotated-desktop", { width: 1366, height: 900 }], ["hub-annotated-mobile", { width: 390, height: 844 }]]) {
    const page = await b.newPage({ viewport: vp }); await attach(page);
    await page.goto(HUB, { waitUntil: "load", timeout: 120000 }); await page.waitForTimeout(1000);
    await badges(page, ids.filter(x => x.region !== "header").map(x => ({ id: x.id, i: x.i, flag: x.flag })), HL.C33);
    await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: true });
    await page.close();
  }
  // 2) each content / footer / breadcrumb target, above the fold, with issue strings marked
  const targets = ids.filter(x => x.region !== "header" && /^https?:/.test(x.abs) && (!ONLY.length || ONLY.includes(x.id)));
  const seen = new Set();
  for (const x of targets) {
    const r = res[x.abs] || {};
    if (!r.tested || r.status !== 200) continue;
    if (/staff_list|DepartmentStaffList/i.test(x.abs + (r.final_url || ""))) { meta[x.id] = { skipped: "staff list shows personal names; not captured" }; continue; }
    const key = r.final_url; if (seen.has(key) && !x.id.startsWith("C")) continue; seen.add(key);
    const page = await b.newPage({ viewport: { width: 1366, height: 900 } }); await attach(page);
    try {
      await page.goto(x.abs, { waitUntil: "load", timeout: 120000 }); await page.waitForTimeout(600);
      const info = await page.evaluate(() => ({
        final: location.href, title: document.title, lang: document.documentElement.getAttribute("lang"),
        h1: [...document.querySelectorAll("h1")].map(h => h.innerText.trim().replace(/\s+/g, " ")).filter(Boolean),
        h2: [...document.querySelectorAll("#content h2, .content h2, main h2, h2")].slice(0, 3).map(h => h.innerText.trim().replace(/\s+/g, " ")),
        imgs_no_alt: [...document.querySelectorAll("img")].filter(i => !i.hasAttribute("alt")).length,
        http_links: [...new Set([...document.querySelectorAll("a[href^='http://']")].map(a => a.getAttribute("href")))],
        hash_links: document.querySelectorAll("a[href='#']").length,
        pdf_links: [...new Set([...document.querySelectorAll("a[href$='.pdf' i]")].map(a => a.href))].length,
        overflow: document.documentElement.scrollWidth > innerWidth,
      }));
      const marked = await mark(page, (r.issue_strings || []).map(s => s.text));
      await page.screenshot({ path: `${OUT}/${x.id}.jpg`, type: "jpeg", quality: 62 });
      meta[x.id] = { ...info, marked, shot: `${OUT}/${x.id}.jpg` };
    } catch (e) { meta[x.id] = { error: String(e).slice(0, 160) }; }
    await page.close();
    process.stdout.write(x.id + " ");
  }
  fs.writeFileSync("page-meta.json", JSON.stringify(meta, null, 1));
  await b.close(); console.log("\ndone", Object.keys(meta).length);
})();
