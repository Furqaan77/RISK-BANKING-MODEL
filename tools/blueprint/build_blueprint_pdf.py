"""Render the platform blueprint markdown (with mermaid diagrams) to PDF via headless Chrome."""
import os, re, subprocess, sys
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "_bmad-output/planning-artifacts/blueprint/platform-blueprint-v1.md"
OUT = ROOT / "_bmad-output/planning-artifacts/blueprint/AI Risk Platform - Blueprint v1.pdf"
WORK = Path(os.environ.get("BUILD_WORK", ROOT / "tools/blueprint/_work"))
CHROME = os.environ.get("CHROME", r"C:/Program Files/Google/Chrome/Application/chrome.exe")

md = SRC.read_text(encoding="utf-8")
md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)                       # drop front matter
mermaids = []
def keep(m):
    mermaids.append(m.group(1))
    return f"\n\nMERMAID{len(mermaids) - 1}\n\n"
md = re.sub(r"```mermaid\n(.*?)```", keep, md, flags=re.S)
lines, fixed = md.split("\n"), []
for ln in lines:   # python-markdown needs a blank line before a list that follows a paragraph line
    if re.match(r"^(\s*[-*] |\s*\d+\. )", ln) and fixed and fixed[-1].strip() and not re.match(r"^(\s*[-*] |\s*\d+\. )", fixed[-1]):
        fixed.append("")
    fixed.append(ln)
md = "\n".join(fixed)
body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
for i, src in enumerate(mermaids):
    body = body.replace(f"<p>MERMAID{i}</p>", f'<div class="diagram"><pre class="mermaid">{src}</pre></div>')

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>AI Risk Platform Blueprint</title>
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1d2433; font-size: 11px; line-height: 1.45; }}
.cover {{ background: #14213D; color: #fff; padding: 28px 26px; border-radius: 6px; margin-bottom: 18px; }}
.cover h1 {{ margin: 0 0 6px; font-size: 26px; color: #fff; }} .cover p {{ margin: 2px 0; color: #cfe3e3; }}
h1 {{ color: #14213D; font-size: 20px; }} h2 {{ color: #14213D; font-size: 15px; border-bottom: 2px solid #0F7B7B; padding-bottom: 3px; margin-top: 18px; page-break-after: avoid; }}
blockquote {{ border-left: 4px solid #0F7B7B; background: #f2f7f7; margin: 8px 0; padding: 6px 10px; }}
table {{ border-collapse: collapse; width: 100%; margin: 6px 0 10px; page-break-inside: auto; }}
tr {{ page-break-inside: avoid; }}
th {{ background: #14213D; color: #fff; text-align: left; padding: 4px 6px; font-size: 10px; }}
td {{ border-bottom: 1px solid #e3e6ec; padding: 4px 6px; vertical-align: top; font-size: 10px; }}
code {{ background: #f1f3f6; padding: 0 3px; border-radius: 3px; font-size: 9.5px; }}
pre {{ background: #f6f8fa; padding: 8px; border-radius: 4px; font-size: 9.5px; white-space: pre-wrap; }}
.diagram {{ text-align: center; margin: 10px 0; page-break-inside: avoid; }} .diagram pre {{ background: none; }}
</style></head><body>
<div class="cover"><h1>AI Risk Platform: Blueprint v1</h1>
<p>The skeleton: every part, how the parts connect, and the rules they obey</p>
<p>Draft, 13 November 2026 &middot; Working code: risk-platform/ (9 of 9 planted problems detected; 6 of 6 tests pass)</p></div>
{body}
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, theme:'neutral', flowchart:{{useMaxWidth:true}}}});</script>
</body></html>"""
WORK.mkdir(parents=True, exist_ok=True)
src = WORK / "blueprint.html"
src.write_text(html, encoding="utf-8")
subprocess.run([CHROME, "--headless=new", f"--user-data-dir={WORK / 'chrome-profile'}", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=15000", f"--print-to-pdf={OUT}", src.as_uri()], check=False, capture_output=True, timeout=180)
print(OUT, OUT.exists())
