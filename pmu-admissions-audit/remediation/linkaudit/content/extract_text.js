// Read-only: main-content text of each of the 36 hub links (C01–C36), including collapsed
// tabs/accordions (made visible in the local render only). No clicks, no input.
const { chromium } = require("playwright");
const fs = require("fs");
const { attach } = require("../curlroute");
const ids = JSON.parse(fs.readFileSync("ids.json", "utf8")).filter(x => x.id.startsWith("C"));
const links = JSON.parse(fs.readFileSync("links.json", "utf8")).desktop.links;
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const x of ids) {
    if (/Staff_List/i.test(x.abs)) { out[x.id] = { label: links[x.i].text, url: x.abs, skipped: "staff list (personal names)" }; continue; }
    const p = await b.newPage({ viewport: { width: 1366, height: 900 } }); await attach(p);
    try {
      await p.goto(x.abs, { waitUntil: "load", timeout: 120000 }); await p.waitForTimeout(800);
      out[x.id] = await p.evaluate(() => {
        const root = document.querySelector(".col-md-8.pulling-side-left") || document.querySelector(".inner-wrapper") || document.querySelector("main") || document.body;
        // open every collapsed accordion / tab inside the content area (local render only)
        root.querySelectorAll("*").forEach(e => { if (!/^(SCRIPT|STYLE|NOSCRIPT)$/.test(e.tagName) && getComputedStyle(e).display === "none") { e.style.display = e.tagName === "TR" ? "table-row" : "block"; e.hidden = false; } });
        return { final: location.href, title: document.title, text: root.innerText.replace(/\n{3,}/g, "\n\n").trim(),
          docs: [...new Set([...root.querySelectorAll("a[href]")].map(a => a.textContent.trim().replace(/\s+/g, " ") + " | " + a.href))] };
      });
      out[x.id].label = links[x.i].text; out[x.id].url = x.abs;
      fs.writeFileSync(`content/text/${x.id}.txt`, `${x.id} | ${links[x.i].text}\n${out[x.id].final}\n${out[x.id].title}\n\n${out[x.id].text}\n\n--- links ---\n${out[x.id].docs.join("\n")}\n`);
    } catch (e) { out[x.id] = { label: links[x.i].text, url: x.abs, error: String(e).slice(0, 150) }; }
    await p.close(); process.stdout.write(x.id + " ");
  }
  fs.writeFileSync("content/texts.json", JSON.stringify(out, null, 1)); await b.close();
})();
