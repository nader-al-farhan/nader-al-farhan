"""Build PMU-Admissions-Executive-Plan.html: replace each {{Sxx}} with the base64 PNG evidence/screenshots/Sxx-*.png."""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "src" / "plan.src.html").read_text(encoding="utf-8")


def embed(m):
    shot = next((ROOT / "evidence" / "screenshots").glob(f"{m[1]}-*.png"))
    return "data:image/png;base64," + base64.b64encode(shot.read_bytes()).decode()


out = re.sub(r"\{\{(S\d+)\}\}", embed, src)
assert "{{S" not in out
(ROOT / "PMU-Admissions-Executive-Plan.html").write_text(out, encoding="utf-8")
print(len(re.findall(r"\{\{S\d+\}\}", src)), "images embedded,", len(out), "bytes")
