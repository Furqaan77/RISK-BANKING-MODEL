import sys
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

proj = sys.argv[1]
parts = [
    ("Part 1", "Inside AI Risk Score Card Global", "Plain-language, step-by-step walkthrough for new risk staff: Maria (New York) and Tom (London), income segments, charts, quiz and glossary.", "part1_walkthrough.pdf"),
    ("Part 2", "Plan for Bank Leadership", "The banker-facing plan: how the model works, the 12 steps of a decision, US and UK rules, income segments with pie charts, governance, roll-out.", proj + "/AI Risk Score Card Global - Plan for Bank Leadership.pdf"),
    ("Part 3", "Income-Based Customer Segmentation Spec", "The technical specification: segments S0–S5, overlay tags, segment policy matrix, decision order, fairness safeguards, demo portfolio.", "part3_spec.pdf"),
]
readers = [PdfReader(p[3]) for p in parts]
counts = [len(r.pages) for r in readers]
starts = []; pg = 2
for c in counts:
    starts.append(pg); pg += c
total = pg - 1

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("SU", F + "segoeui.ttf")); pdfmetrics.registerFont(TTFont("SU-B", F + "segoeuib.ttf")); pdfmetrics.registerFont(TTFont("SU-L", F + "segoeuil.ttf"))
NAVY = colors.HexColor("#14213D"); TEAL = colors.HexColor("#0F7B7B"); LIGHT = colors.HexColor("#C9D2E0"); MUTE = colors.HexColor("#9AA6BA")
W, H = A4; M = 20 * 2.8346
c = canvas.Canvas("cover.pdf", pagesize=A4)
c.setFillColor(NAVY); c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(TEAL); c.rect(0, H - 26, W, 26, stroke=0, fill=1)
c.setFillColor(colors.HexColor("#7FC4C4")); c.setFont("SU-B", 10); c.drawString(M, H - 120, "COMPLETE PACK  /  NEW YORK AND LONDON")
c.setFillColor(colors.white)
TITLE = "AI Risk Score Modelling for Banks"
fs = 30
while c.stringWidth(TITLE, "SU-B", fs) > W - 2 * M and fs > 18: fs -= 1
c.setFont("SU-B", fs); c.drawString(M, H - 162, TITLE)
c.setFont("SU-L", 15); c.drawString(M, H - 188, "Walkthrough, bank leadership plan and income-segmentation spec")
c.setFont("SU-L", 15); c.drawString(M, H - 208, "in one document")
c.setFillColor(TEAL); c.rect(M, H - 232, 110, 4, stroke=0, fill=1)
y = H - 290
c.setFillColor(LIGHT); c.setFont("SU-B", 11); c.drawString(M, y, "CONTENTS"); y -= 30
for (tag, title, desc, _), s, n in zip(parts, starts, counts):
    c.setFillColor(colors.HexColor("#7FC4C4")); c.setFont("SU-B", 10); c.drawString(M, y, tag.upper())
    c.setFillColor(colors.white); c.setFont("SU-B", 15); c.drawString(M + 62, y, title)
    c.setFillColor(LIGHT); c.setFont("SU", 10); c.drawRightString(W - M, y, f"pages {s}–{s + n - 1}")
    y -= 17
    c.setFillColor(MUTE); c.setFont("SU", 9.5)
    words = desc.split(); line = ""
    for w_ in words:
        t = (line + " " + w_).strip()
        if c.stringWidth(t, "SU", 9.5) > W - 2 * M - 62:
            c.drawString(M + 62, y, line); y -= 13; line = w_
        else:
            line = t
    if line: c.drawString(M + 62, y, line); y -= 13
    y -= 22
c.setFillColor(MUTE); c.setFont("SU", 9)
c.drawString(M, 90, f"{total} pages  |  November 2026  |  Discussion document")
c.drawString(M, 76, "All customers, figures and portfolio data are illustrative. Regulatory summaries are not legal advice.")
c.drawString(M, 62, "Use the PDF bookmarks panel to jump between parts.")
c.showPage(); c.save()

w = PdfWriter()
w.append(PdfReader("cover.pdf"))
w.add_outline_item("Cover & contents", 0)
for (tag, title, _, _), r, s in zip(parts, readers, starts):
    w.append(r)
    w.add_outline_item(f"{tag}: {title}", s - 1)
w.add_metadata({"/Title": "AI Risk Score Modelling for Banks", "/Author": "AI Risk Score Card team", "/Subject": "Walkthrough, bank leadership plan and income-segmentation spec"})
out = proj + "/AI Risk Score Card Global - Complete Pack.pdf"
with open(out, "wb") as f: w.write(f)
print("pages", total, "starts", starts, "counts", counts, "->", out)
