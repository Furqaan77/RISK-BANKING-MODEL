"""Build the Retail Credit Policy PDF (via HTML + Chrome) and DOCX (python-docx) from the markdown source."""
import re, sys, subprocess, pathlib, markdown
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = pathlib.Path(sys.argv[1])
OUT_DIR = pathlib.Path(sys.argv[2])
WORK = pathlib.Path(__file__).parent
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
TITLE = "Retail Credit Policy: UAE Finance Company (Conventional)"
PDF_NAME = "Retail Credit Policy - UAE Finance Company v0.1.pdf"
DOCX_NAME = "Retail Credit Policy - UAE Finance Company v0.1.docx"

md = SRC.read_text(encoding="utf-8")
body_md = re.sub(r"^# .*\n", "", md, count=1, flags=re.M)

# ---------------- HTML / PDF ----------------
html_body = markdown.markdown(body_md, extensions=["tables", "sane_lists"])
html_body = html_body.replace("[A]", '<span class="tag a">A</span>').replace("[P]", '<span class="tag p">P</span>').replace("[R]", '<span class="tag r">R</span>')
css = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm;
  @bottom-right { content: counter(page); font: 8pt 'IBM Plex Sans', sans-serif; color: #5b6475; } }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }
body { font: 9.6pt/1.5 'IBM Plex Sans', 'Segoe UI', sans-serif; color: #14213d; margin: 0; }
.cover { background: #14213d; color: #fff; height: 258mm; padding: 34mm 18mm 0; position: relative; break-after: page; }
.cover .bar { position: absolute; top: 0; left: 0; right: 0; height: 9mm; background: #0f7b7b; }
.cover small { color: #7fc4c4; font-weight: 600; letter-spacing: .12em; font-size: 9pt; }
.cover h1 { font: 800 27pt/1.15 'Plus Jakarta Sans', 'Segoe UI', sans-serif; margin: 10px 0 8px; color: #fff; }
.cover p { color: #c9d2e0; font-size: 11pt; max-width: 150mm; }
.cover .rule { width: 40mm; height: 4px; background: #0f7b7b; margin: 18px 0; }
.cover .meta { position: absolute; bottom: 24mm; left: 18mm; right: 18mm; color: #9aa6ba; font-size: 9pt; }
h2 { font: 700 14pt/1.3 'Plus Jakarta Sans', sans-serif; color: #14213d; margin: 20px 0 6px; padding-top: 6px; border-top: 2px solid #0f7b7b; break-after: avoid; }
h3 { font: 700 11pt/1.3 'Plus Jakarta Sans', sans-serif; color: #0f6e6a; margin: 14px 0 4px; break-after: avoid; }
p { margin: 4px 0 8px; }
table { border-collapse: collapse; width: 100%; font-size: 8.4pt; margin: 6px 0 12px; }
tr { break-inside: avoid; }
th { background: #14213d; color: #fff; text-align: left; padding: 5px 6px; font-weight: 600; vertical-align: top; }
td { padding: 5px 6px; border-bottom: 1px solid #d5dae1; vertical-align: top; }
tr:nth-child(even) td { background: #f4f6f9; }
ul, ol { margin: 4px 0 8px; padding-left: 18px; } li { margin: 2px 0; }
hr { border: 0; height: 0; margin: 4px 0; }
.tag { display: inline-block; font: 700 7pt/1 'IBM Plex Sans', sans-serif; padding: 2px 4px; border-radius: 3px; vertical-align: 1px; }
.tag.a { background: #fde7c2; color: #7a4a00; }
.tag.p { background: #dbe7f7; color: #1c4f8f; }
.tag.r { background: #e3f1f1; color: #0f5e5a; }
.legend { font-size: 8.5pt; color: #5b6475; }
"""
cover = f"""<div class="cover"><div class="bar"></div>
<small>RETAIL CREDIT POLICY &nbsp;/&nbsp; PILOT UAE FINANCE COMPANY</small>
<h1>{TITLE}</h1>
<p>Retail lending for a pilot conventional finance company: personal loans, credit cards, auto loans, gold-backed loans and short-term credit.</p>
<div class="rule"></div>
<p>Version 0.1, draft for management and Board review, 9 November 2026. Built on the credit criteria recommended for UAE banks, adjusted to the Finance Companies Regulation and benchmarked against UAE finance companies, digital and BNPL lenders and the top five banks.</p>
<p><span class="tag a">A</span> adjusted for the finance-company market or rules &nbsp;&nbsp;
<span class="tag p">P</span> proposal where the market publishes no figure &nbsp;&nbsp;
<span class="tag r">R</span> Finance Companies Regulation rule to confirm</p>
<div class="meta">Policy owner: Head of Credit &nbsp;|&nbsp; Approval: Board of Directors (Board Credit Committee)<br>
Draft for discussion. Regulatory references must be confirmed by Legal & Compliance before adoption.</div></div>"""
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{TITLE}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=Plus+Jakarta+Sans:wght@700;800&display=swap">
<style>{css}</style></head><body>{cover}{html_body}</body></html>"""
html_path = WORK / "policy_fc.html"
html_path.write_text(html, encoding="utf-8")
pdf_path = OUT_DIR / PDF_NAME
subprocess.run([CHROME, "--headless=new", f"--user-data-dir={WORK / 'chrome-profile-fc'}", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                f"--print-to-pdf={pdf_path}", html_path.as_uri()], capture_output=True)
print("pdf", pdf_path.exists(), pdf_path)

# ---------------- DOCX ----------------
NAVY = RGBColor(0x14, 0x21, 0x3D); TEAL = RGBColor(0x0F, 0x6E, 0x6A)
doc = Document()
sec = doc.sections[0]
sec.page_height = Cm(29.7); sec.page_width = Cm(21.0)
for side in ("left_margin", "right_margin"): setattr(sec, side, Cm(1.8))
sec.top_margin = Cm(1.8); sec.bottom_margin = Cm(1.8)
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
for lvl, size, color in ((1, 16, NAVY), (2, 13, NAVY), (3, 11, TEAL)):
    hs = doc.styles[f"Heading {lvl}"]; hs.font.name = "Calibri"; hs.font.size = Pt(size); hs.font.color.rgb = color; hs.font.bold = True

def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_fill); tcPr.append(shd)

def add_runs(par, text, bold_all=False, color=None, size=None):
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part: continue
        b = part.startswith("**") and part.endswith("**")
        t = part[2:-2] if b else part
        t = t.replace("`", "")
        r = par.add_run(t); r.bold = b or bold_all
        if color: r.font.color.rgb = color
        if size: r.font.size = Pt(size)

# cover
p = doc.add_paragraph(); add_runs(p, "RETAIL CREDIT POLICY / PILOT UAE FINANCE COMPANY", bold_all=True, color=TEAL, size=9)
p = doc.add_paragraph(); add_runs(p, TITLE, bold_all=True, color=NAVY, size=24)
p = doc.add_paragraph(); add_runs(p, "Retail lending for a pilot conventional finance company: personal loans, credit cards, auto loans, gold-backed loans and short-term credit.", size=11)
p = doc.add_paragraph(); add_runs(p, "Version 0.1, draft for management and Board review, 9 November 2026. Built on the credit criteria recommended for UAE banks, adjusted to the Finance Companies Regulation and benchmarked against UAE finance companies, digital and BNPL lenders and the top five banks. [A] marks items adjusted for the finance-company market or rules; [P] marks proposals; [R] marks Finance Companies Regulation rules to confirm.", size=9.5)
doc.add_page_break()

lines = body_md.splitlines(); i = 0
while i < len(lines):
    line = lines[i].rstrip()
    if not line.strip() or line.strip() == "---":
        i += 1; continue
    m = re.match(r"^(#{2,4})\s+(.*)", line)
    if m:
        lvl = len(m.group(1)) - 1
        doc.add_heading(m.group(2).replace("**", ""), level=min(lvl, 3)); i += 1; continue
    if line.lstrip().startswith("|"):
        rows = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c): rows.append(cells)
            i += 1
        ncol = max(len(r) for r in rows)
        t = doc.add_table(rows=len(rows), cols=ncol); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for ri, r in enumerate(rows):
            for ci in range(ncol):
                cell = t.cell(ri, ci); cell.text = ""
                par = cell.paragraphs[0]
                txt = r[ci] if ci < len(r) else ""
                add_runs(par, txt, bold_all=(ri == 0), color=(RGBColor(0xFF, 0xFF, 0xFF) if ri == 0 else None), size=8.5)
                if ri == 0: shade(cell, "14213D")
                elif ri % 2 == 0: shade(cell, "F4F6F9")
        doc.add_paragraph(); continue
    m = re.match(r"^(\s*)[-*]\s+(.*)", line)
    if m:
        par = doc.add_paragraph(style="List Bullet" if not m.group(1) else "List Bullet 2"); add_runs(par, m.group(2)); i += 1; continue
    m = re.match(r"^(\s*)\d+\.\s+(.*)", line)
    if m:
        par = doc.add_paragraph(style="List Number"); add_runs(par, m.group(2)); i += 1; continue
    par = doc.add_paragraph(); add_runs(par, line.strip()); i += 1

docx_path = OUT_DIR / DOCX_NAME
doc.save(docx_path)
print("docx", docx_path.exists(), docx_path)
