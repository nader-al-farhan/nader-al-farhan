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

    return re.sub(r"\{\{(S\d+)\}\}", embed, src_text)


if __name__ == "__main__":
    out = build((ROOT / "src" / "plan.src.html").read_text(encoding="utf-8"))
    (ROOT / "PMU-Admissions-Executive-Plan.html").write_text(out, encoding="utf-8")
    print(f"built {len(out):,} bytes")
