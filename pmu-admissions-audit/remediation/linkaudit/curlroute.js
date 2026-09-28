// Playwright helper: every request made by the page is fetched with curl (full TLS
// verification against the environment CA bundle) and handed to Chromium.
// The browser itself never makes a network connection and its trust store is untouched.
const { execFile } = require("child_process");
const fs = require("fs"), os = require("os"), path = require("path");
const cache = new Map();
function curl(url, method) {
  return new Promise((resolve) => {
    const body = path.join(os.tmpdir(), "cr-" + Math.random().toString(36).slice(2));
    const hdr = body + ".h";
    execFile("curl", ["-sS", "-m", "40", "-D", hdr, "-o", body, "-w", "%{http_code}", "-A", "PMU-Admissions-LinkAudit/1.0 (read-only)", url],
      { maxBuffer: 1 << 20 }, (err, stdout) => {
        let status = parseInt(stdout, 10) || 0, headers = {}, buf = Buffer.alloc(0);
        try { buf = fs.readFileSync(body); } catch (e) {}
        try {
          const blocks = fs.readFileSync(hdr, "utf8").trim().split(/\r?\n\r?\n/);
          for (const line of blocks[blocks.length - 1].split(/\r?\n/).slice(1)) {
            const i = line.indexOf(":"); if (i > 0) headers[line.slice(0, i).trim().toLowerCase()] = line.slice(i + 1).trim();
          }
        } catch (e) {}
        for (const f of [body, hdr]) try { fs.unlinkSync(f); } catch (e) {}
        resolve({ status, headers, buf, err: err ? String(err).slice(0, 120) : null });
      });
  });
}
async function attach(page) {
  await page.route("**/*", async (route) => {
    const req = route.request(), url = req.url();
    if (!/^https?:/.test(url) || req.method() !== "GET") return route.abort();
    let r = cache.get(url);
    if (!r) { r = await curl(url); cache.set(url, r); }
    if (!r.status) return route.abort();
    const h = {};
    for (const k of ["content-type", "location"]) if (r.headers[k]) h[k] = r.headers[k];
    await route.fulfill({ status: r.status, headers: h, body: r.buf });
  });
}
module.exports = { attach, curl };
