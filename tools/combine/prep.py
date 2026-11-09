import sys, pathlib, re, markdown

S = pathlib.Path(sys.argv[1])
proj = pathlib.Path(sys.argv[2])

# 1) walkthrough -> printable html (light theme, A4, quiz answers open, cards kept whole)
body = (S / "walkthrough-global" / "ai-risk-score-card-global-walkthrough.html").read_text(encoding="utf-8")
print_css = """<style>
@page { size: A4; margin: 12mm 10mm; }
@media print {
  html, body { background: #ffffff !important; }
  .tip { display: none !important; }
  .stepcard, .card, .note, .signal, .layer, .q, details, figure, svg, .grades, .readout,
  .mistake, .role, .team, .tiles, .jflow, .person, .verdict, .control, .math, tr { break-inside: avoid; }
  .chapter, h2, h3 { break-after: avoid; }
  section { display: block !important; }
  section > * + * { margin-top: 16px; }
  .steps { display: block !important; }
  .steps > li { margin: 0 0 12px; }
  .stepcard { display: block !important; }
  .stepcard > * + * { margin-top: 10px; }
  a { color: inherit; text-decoration: none; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
</style>
<script>
function openAll(){ document.querySelectorAll('details').forEach(function(d){ d.open = true; }); }
document.addEventListener('DOMContentLoaded', openAll);
window.addEventListener('load', openAll);
</script>"""
html = ('<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">' + print_css + '</head><body>' + body + '</body></html>')
(S / "combine" / "walkthrough_print.html").write_text(html, encoding="utf-8")

# 2) spec markdown -> html
md = (proj / "_bmad-output" / "large-bank" / "planning-artifacts" / "income-segmentation-spec.md").read_text(encoding="utf-8")
if md.startswith("---"):
    md = md.split("---", 2)[2]
list_re = re.compile(r"^\s*(- |\d+\. )")
out = []
for line in md.splitlines():
    if list_re.match(line) and out and out[-1].strip() and not list_re.match(out[-1]) and not out[-1].lstrip().startswith("|"):
        out.append("")
    out.append(line)
md = "\n".join(out)
md = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)
content = markdown.markdown(md, extensions=["tables", "sane_lists"])
spec_html = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=Plus+Jakarta+Sans:wght@700;800&display=swap">
<style>
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font: 10pt/1.5 "IBM Plex Sans", "Segoe UI", sans-serif; color: #14213d; }
.band { background: #14213d; color: #fff; padding: 14px 18px; border-radius: 6px; margin-bottom: 14px; }
.band small { color: #9fb4d9; letter-spacing: .1em; font-weight: 600; font-size: 8pt; }
.band h1 { font: 800 18pt/1.2 "Plus Jakarta Sans", "Segoe UI", sans-serif; margin: 4px 0 0; color: #fff; }
.band p { color: #c9d2e0; margin: 4px 0 0; font-size: 9pt; }
h2 { font: 700 13pt/1.3 "Plus Jakarta Sans", sans-serif; margin: 18px 0 6px; color: #0f6e6a; border-bottom: 1px solid #d5dae1; padding-bottom: 3px; break-after: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 8.3pt; margin: 8px 0 12px; }
tr { break-inside: avoid; }
th { background: #14213d; color: #fff; text-align: left; padding: 5px 6px; font-weight: 600; }
td { padding: 5px 6px; border-bottom: 1px solid #d5dae1; vertical-align: top; }
tr:nth-child(even) td { background: #f4f6f9; }
code { font-family: Consolas, monospace; font-size: 8.5pt; background: #eef2f6; padding: 0 3px; border-radius: 3px; }
blockquote { border-left: 3px solid #0f6e6a; background: #e3f1f1; margin: 10px 0; padding: 8px 12px; }
ul, ol { padding-left: 18px; margin: 4px 0 8px; } li { margin: 2px 0; }
</style></head><body>
<div class="band"><small>PART 3 &middot; TECHNICAL SPECIFICATION</small><h1>Income-Based Customer Segmentation (US + UK)</h1>
<p>AI Risk Score Card Global &middot; income-segmentation-spec.md &middot; 7 Nov 2026</p></div>
""" + content + "</body></html>"
(S / "combine" / "spec_print.html").write_text(spec_html, encoding="utf-8")
print("prepared")
