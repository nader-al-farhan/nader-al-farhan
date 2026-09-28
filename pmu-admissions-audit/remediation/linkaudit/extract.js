// Read-only: loads the live Admissions Office hub (via curlroute), lists every <a>,
// its region, the nearest group heading, and its box. No clicks, no form input.
const { chromium } = require("playwright");
const { attach } = require("./curlroute");
const HUB = "https://pmu.edu.sa/admission/admission";
(async () => {
  const b = await chromium.launch();
  const out = {};
  for (const [name, vp] of [["desktop", { width: 1366, height: 900 }], ["mobile", { width: 390, height: 844 }]]) {
    const page = await b.newPage({ viewport: vp });
    await attach(page);
    await page.goto(HUB, { waitUntil: "load", timeout: 120000 });
    await page.waitForTimeout(1500);
    out[name] = await page.evaluate(() => {
      const region = (a) => {
        if (a.closest("footer,.footer,#footer")) return "footer";
        if (a.closest(".breadcrumb,[class*=bread]") && a.getBoundingClientRect().y + scrollY < 400) return "breadcrumb";
        if (a.closest("header,.header,#header,nav,.navbar,[class*=menu],[class*=nav]")) return "header";
        return "main";
      };
      const heading = (a) => {
        let n = a;
        while (n && n !== document.body) {
          let s = n.previousElementSibling;
          while (s) {
            const h = s.matches("h1,h2,h3,h4,h5,h6") ? s : s.querySelector && [...s.querySelectorAll("h1,h2,h3,h4,h5,h6")].pop();
            if (h && h.innerText.trim()) return h.innerText.trim().replace(/\s+/g, " ");
            s = s.previousElementSibling;
          }
          n = n.parentElement;
        }
        return "";
      };
      return {
        title: document.title, lang: document.documentElement.getAttribute("lang"),
        docW: document.documentElement.scrollWidth, docH: document.documentElement.scrollHeight,
        h1: [...document.querySelectorAll("h1")].map(h => h.innerText.trim()),
        links: [...document.querySelectorAll("a")].map((a, i) => {
          const r = a.getBoundingClientRect(), cs = getComputedStyle(a);
          return { i, text: (a.innerText || a.textContent || a.getAttribute("aria-label") || a.title || (a.querySelector("img") || {}).alt || "").trim().replace(/\s+/g, " "),
            href: a.getAttribute("href"), abs: a.href, target: a.target || null, region: region(a), heading: heading(a),
            visible: r.width > 0 && r.height > 0 && cs.visibility !== "hidden" && cs.display !== "none",
            box: { x: Math.round(r.x + scrollX), y: Math.round(r.y + scrollY), w: Math.round(r.width), h: Math.round(r.height) } };
        }),
      };
    });
    await page.screenshot({ path: `/tmp/hub-${name}.png`, fullPage: true });
    await page.close();
  }
  require("fs").writeFileSync("/tmp/hub-links.json", JSON.stringify(out, null, 1));
  await b.close();
  console.log(out.desktop.title, out.desktop.links.length, out.mobile.links.length, out.desktop.docW, out.mobile.docW);
})();
