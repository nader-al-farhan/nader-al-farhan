"""Gate G5 static baseline: read-only measurements from the server-delivered HTML of the
core admissions pages (checks.json "pages"). No browser, no clicks, no form submission.

Measures what the HTML source can prove: <html lang/dir>, viewport meta, H1 count and
heading-order skips, <img> without alt, links with href="#" or http://, and the href of
every link/button whose text contains Apply / قدّم. It cannot measure layout (horizontal
overflow, table width) or text injected by JavaScript; those need dom_probe.mjs in a browser.

Usage: python3 static_probe.py OUT.json
"""
import html.parser
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
APPLY = re.compile(r"apply|قدّم|قدم الآن|قدم هنا", re.I)


def clip(s):
    return re.sub(r"\s+", " ", s or "").strip()[:80]


class Probe(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = self.dir = None
        self.viewport = None
        self.heads, self.imgs, self.links, self.controls = [], [], [], []
        self.tables = 0
        self._stack = []  # open heading / a / button capturing text
        self._skip = 0    # inside script/style

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
        elif tag == "html":
            self.lang, self.dir = a.get("lang"), a.get("dir")
        elif tag == "meta" and (a.get("name") or "").lower() == "viewport":
            self.viewport = a.get("content")
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "table":
            self.tables += 1
        elif tag == "input" and (a.get("type") or "").lower() in ("submit", "button"):
            if APPLY.search(a.get("value") or ""):
                self.controls.append({"tag": "input", "text": clip(a.get("value")), "href": None})
        if re.fullmatch(r"h[1-6]|a|button", tag):
            self._stack.append({"tag": tag, "attrs": a, "text": ""})

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        for i in range(len(self._stack) - 1, -1, -1):
            if self._stack[i]["tag"] == tag:
                el = self._stack.pop(i)
                text = clip(el["text"])
                for outer in self._stack:
                    outer["text"] += " " + el["text"]
                if tag[0] == "h":
                    self.heads.append((int(tag[1]), text))
                else:
                    if tag == "a" and el["attrs"].get("href") is not None:
                        self.links.append(el["attrs"]["href"].strip())
                    if APPLY.search(text):
                        self.controls.append({"tag": tag, "text": text, "href": el["attrs"].get("href"),
                                              "onclick": el["attrs"].get("onclick")})
                break

    def handle_data(self, data):
        if not self._skip and self._stack:
            self._stack[-1]["text"] += data


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PMU-Admissions-G5-StaticProbe/1.0 (read-only audit)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        status, final, raw = r.status, r.geturl(), r.read().decode("utf-8", "replace")
    p = Probe()
    p.feed(raw)
    skips, prev = [], 0
    for lvl, text in p.heads:
        if lvl > prev + 1:
            skips.append({"from": f"h{prev}" if prev else "(start)", "to": f"h{lvl}", "text": text})
        prev = lvl
    for c in p.controls:
        c["resolved"] = urllib.parse.urljoin(final, c["href"]) if c.get("href") else None
    return {
        "status": status, "final_url": final, "html_bytes": len(raw),
        "redirected_to_login": bool(re.search(r"login|signin|sso", final, re.I)),
        "lang": p.lang, "dir": p.dir, "viewport_meta": p.viewport,
        "h1_count": sum(1 for lvl, _ in p.heads if lvl == 1),
        "h1_text": [t for lvl, t in p.heads if lvl == 1],
        "heading_sequence": " ".join(f"h{lvl}" for lvl, _ in p.heads),
        "heading_skips": skips,
        "tables_total": p.tables,
        "images_total": len(p.imgs),
        "images_missing_alt": [i.get("src") for i in p.imgs if "alt" not in i],
        "images_empty_alt": sum(1 for i in p.imgs if i.get("alt") == ""),
        "links_total": len(p.links),
        "links_hash": sum(1 for h in p.links if h == "#"),
        "links_http": sorted({h for h in p.links if h.lower().startswith("http://")}),
        "apply_controls": p.controls,
    }


def main(out):
    cfg = json.loads((HERE / "checks.json").read_text(encoding="utf-8"))
    res = {"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "method": "static HTML (urllib via audit egress proxy); no JavaScript, no layout", "pages": {}}
    for key, url in cfg["pages"].items():
        try:
            res["pages"][key] = {"url": url, **probe(url)}
        except Exception as e:
            res["pages"][key] = {"url": url, "error": f"{type(e).__name__}: {e}"}
    pathlib.Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1])
