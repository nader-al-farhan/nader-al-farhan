// Read-only: for each content issue, open the page (curlroute), expand collapsed sections
// locally, highlight the quoted text and capture the region around it. No clicks or input.
const { chromium } = require("playwright");
const fs = require("fs");
const { attach } = require("../curlroute");
const ONLY = (process.env.ONLY || "").split(",").filter(Boolean);
const jobs = JSON.parse(fs.readFileSync("content/shot-jobs.json", "utf8")).filter(j => !ONLY.length || ONLY.includes(j.id));
fs.mkdirSync("content/shots", { recursive: true });
(async () => {
  const b = await chromium.launch();
  const res = ONLY.length && fs.existsSync("content/shots.json") ? JSON.parse(fs.readFileSync("content/shots.json", "utf8")) : {};
  const byPage = {}; for (const j of jobs) (byPage[j.id] ||= []).push(j);
  for (const [id, list] of Object.entries(byPage)) {
    const p = await b.newPage({ viewport: { width: 1366, height: 900 } }); await attach(p);
    let ok = false;
    for (let t = 0; t < 3 && !ok; t++) { try { await p.goto(list[0].url, { waitUntil: "load", timeout: 120000 }); ok = true; } catch (e) { await p.waitForTimeout(3000); } }
    if (!ok) { for (const j of list) res[`${j.id}-${j.n}`] = { error: "page did not load" }; await p.close(); continue; }
    await p.waitForTimeout(800);
    await p.evaluate(() => { const root = document.querySelector(".col-md-8.pulling-side-left") || document.body;
      root.querySelectorAll("*").forEach(e => { if (!/^(SCRIPT|STYLE|NOSCRIPT)$/.test(e.tagName) && getComputedStyle(e).display === "none" && !e.closest("header,.header,footer,.footer,nav")) e.style.display = e.tagName === "TR" ? "table-row" : "block"; }); });
    for (const j of list) {
      const box = await p.evaluate(({ quotes, sev }) => {
        const n = s => s.replace(/\s+/g, " ").replace(/’/g, "'").replace(/–/g, "-").trim().toLowerCase();
        const color = sev === "H" ? "#c62828" : sev === "M" ? "#e08a00" : "#2f6db5";
        document.querySelectorAll("[data-hl]").forEach(e => { e.style.outline = ""; e.style.background = ""; e.removeAttribute("data-hl"); });
        const hits = [];
        for (const q of quotes) {
          const nq = n(q);
          const cands = [...document.querySelectorAll("body *")].filter(e => !/^(SCRIPT|STYLE|HTML|BODY)$/.test(e.tagName) && e.offsetParent !== null && n(e.innerText || "").includes(nq));
          const leaf = cands.filter(e => ![...e.children].some(c => cands.includes(c)));
          const el = leaf[0]; if (!el) continue;
          el.setAttribute("data-hl", "1"); el.style.outline = `3px solid ${color}`; el.style.background = "#fff59d";
          const r = el.getBoundingClientRect(); hits.push({ y: r.top + scrollY, b: r.bottom + scrollY });
        }
        if (!hits.length) return null;
        const top = Math.min(...hits.map(h => h.y)), bot = Math.max(...hits.map(h => h.b));
        return { top, bot, found: hits.length };
      }, j);
      const key = `${j.id}-${j.n}`;
      if (!box) { res[key] = { error: "quote not located" }; continue; }
      const H = Math.min(Math.max(bot(box) - box.top + 260, 420), 1400), y = Math.max(0, box.top - 130);
      await p.screenshot({ path: `content/shots/${key}.jpg`, type: "jpeg", quality: 65, fullPage: true, clip: { x: 0, y, width: 1366, height: H } });
      res[key] = { shot: `content/shots/${key}.jpg`, found: box.found, of: j.quotes.length };
      process.stdout.write(key + " ");
    }
    await p.close();
  }
  fs.writeFileSync("content/shots.json", JSON.stringify(res, null, 1)); await b.close(); console.log();
})();
function bot(b) { return b.bot; }
