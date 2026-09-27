"""Build PMU-Admissions-Executive-Plan.html from src/plan.src.html by embedding
evidence/screenshots/Sxx-*.png as base64 data URIs in place of {{Sxx}} placeholders."""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def build(src_text):
    shots = ROOT / "evidence" / "screenshots"

    def embed(m):
        files = sorted(shots.glob(f"{m.group(1)}-*.png"))
        if len(files) != 1:
            sys.exit(f"placeholder {m.group(0)}: expected 1 screenshot, found {len(files)}")
        return "data:image/png;base64," + base64.b64encode(files[0].read_bytes()).decode()

    body = re.sub(r"\{\{(S\d+)\}\}", embed, src_text)
    # The source is a fragment. A standalone file must declare its encoding and
    # language, or some viewers (e.g. mobile file previews) decode the Arabic as Latin-1.
    if not body.lstrip().lower().startswith("<!doctype"):
        body = HEAD + body + "\n</html>\n"
    return body


HEAD = (
    "<!doctype html>\n"
    '<html lang="ar">\n'
    '<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
)


if __name__ == "__main__":
    out = build((ROOT / "src" / "plan.src.html").read_text(encoding="utf-8"))
    # utf-8-sig writes a BOM, a second encoding signal for viewers that ignore <meta charset>
    (ROOT / "PMU-Admissions-Executive-Plan.html").write_text(out, encoding="utf-8-sig")
    print(f"built {len(out):,} bytes")
