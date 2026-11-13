"""Build the retail Master Rulebook + Bank Comparison tool (XLSX) and the bank one-pagers (PDF).

Inputs:  master-rulebook/data/compare_{uae,uk,us}.csv, rulebook_uae.csv
         BMAD research digests (US/UK rulebook tables, source URLs)
Outputs: master-rulebook/Retail Master Rulebook and Bank Comparison.xlsx
         master-rulebook/Retail Bank Check - One-Pagers.pdf
         master-rulebook/data/rulebook_{us,uk}.csv (extracted)
Run with a Python that has openpyxl. Chrome is needed for the PDF.
"""
import csv, html, re, statistics, subprocess, sys, os
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "master-rulebook"
DATA = OUT / "data"
RUN = ROOT / "_bmad-output/planning-artifacts/research/domain-master-rulebook-retail-credit-us-uk-uae-2026-11-12"
DIG = RUN / "digests"
CHROME = os.environ.get("CHROME", r"C:/Program Files/Google/Chrome/Application/chrome.exe")
WORK = Path(os.environ.get("BUILD_WORK", ROOT / "tools/master-rulebook/_work"))
THRESHOLD = 0.05  # 5% away from the peer median counts as different
AS_OF = "12 November 2026"

NAVY, TEAL = "14213D", "0F7B7B"
LABEL_COLORS = {  # fill, text
    "Too rigid": ("FDEBD2", "8A4B00"),
    "Higher risk": ("FADBD2", "9C2B0E"),
    "In line": ("D9F2E6", "0B6B47"),
    "At rule limit": ("DCE9F9", "1D4F91"),
    "Above rule limit": ("F5C6C6", "8B1111"),
    "Cheaper": ("D9F2E6", "0B6B47"),
    "More expensive": ("FDEBD2", "8A4B00"),
    "Better": ("D9F2E6", "0B6B47"),
    "Worse": ("FADBD2", "9C2B0E"),
    "No peer data": ("EEEEEE", "555555"),
}
MARKETS = [("UAE", "compare_uae.csv", "rulebook_uae.csv", "AED"),
           ("UK", "compare_uk.csv", "rulebook_uk.csv", "GBP"),
           ("US", "compare_us.csv", "rulebook_us.csv", "USD")]


# ---------- data ----------
def num(x):
    try:
        return float(str(x).replace(",", ""))
    except (TypeError, ValueError):
        return None


def label(v, vals, cap, direction, kind, t=THRESHOLD):
    v = num(v)
    if kind == "info" or v is None:
        return ""
    cap = num(cap)
    if cap is not None:
        if (v > cap) if direction == "higher" else (v < cap):
            return "Above rule limit"
        if v == cap:
            return "At rule limit"
    nums = [num(x) for x in vals if num(x) is not None]
    if len(nums) < 2:
        return "No peer data"
    m = statistics.median(nums)
    looser = v > m * (1 + t) if direction == "higher" else v < m * (1 - t)
    stricter = v < m * (1 - t) if direction == "higher" else v > m * (1 + t)
    if looser:
        return {"risk": "Higher risk", "price": "Cheaper", "outcome": "Worse"}[kind]
    if stricter:
        return {"risk": "Too rigid", "price": "More expensive", "outcome": "Better"}[kind]
    return "In line"


def load_compare(fname):
    with open(DATA / fname, encoding="utf-8") as f:
        r = csv.reader(f)
        head = next(r)
        rows = [dict(zip(head, x)) for x in r if x]
    banks = head[7:11]
    return banks, rows


def extract_rulebook(digest, out_csv, country):
    """Pull Part A markdown table from a digest into a CSV."""
    t = (DIG / digest).read_text(encoding="utf-8")
    part = re.split(r"^## Part A.*$", t, flags=re.M)[1]
    part = re.split(r"^## Part B|^---", part, flags=re.M)[0]
    rows = []
    for line in part.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line) and "param_id" not in line:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 5:
                rows.append(cells[:5] + ["see digest"])
    with open(DATA / out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["param_id", "parameter", f"{country} rule (hard limit or requirement)", "type", "citation", "confidence"])
        w.writerows(rows)
    return len(rows)


def load_rulebook(fname):
    with open(DATA / fname, encoding="utf-8") as f:
        return list(csv.reader(f))


def collect_sources():
    out = []
    for f in sorted(DIG.glob("*.md")) + sorted((ROOT / "_bmad-output/planning-artifacts/research/domain-master-rulebook-fh-sme-corporate-us-uk-uae-2026-11-13/digests").glob("*.md")):
        seen = set()
        for u in re.findall(r"https?://[^\s)\]|>,\"'`]+", f.read_text(encoding="utf-8")):
            u = u.rstrip(".;")
            if u not in seen:
                seen.add(u)
                out.append((f.name, u))
    imp = RUN / "imports/banks_core.csv"
    if imp.exists():
        with open(imp, encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if row["bank"] in ("Emirates NBD", "FAB", "ADCB", "Mashreq"):
                    out.append(("imports/banks_core.csv (UAE)", row["key_source_url"]))
    return out


# ---------- workbook ----------
thin = Side(style="thin", color="D0D5DD")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HFILL = PatternFill("solid", fgColor=NAVY)
HFONT = Font(color="FFFFFF", bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")


def header(ws, row, values, widths=None):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.fill, c.font, c.alignment, c.border = HFILL, HFONT, WRAP, BORDER
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w


def compare_sheet(wb, market, banks, rows):
    ws = wb.create_sheet(f"{market} compare")
    ws["A1"] = f"{market}: banks against the central bank / regulator rulebook (retail)"
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    ws["A2"] = ("Change any yellow value and the labels update. Labels compare each bank with the "
                "middle (median) of the four banks and with the rule limit. Threshold is on the Settings sheet.")
    ws["A2"].alignment = WRAP
    ws.merge_cells("A2:R2")
    ws.row_dimensions[2].height = 32
    cols = (["ID", "Measure", "Unit", "Kind", "Looser when", "Regulator rule", "Rule limit"]
            + banks + ["Peer median"] + [f"Label: {b}" for b in banks] + ["Notes", "Confidence"])
    header(ws, 4, cols, [11, 38, 13, 9, 11, 46, 10, 15, 15, 15, 15, 12, 16, 16, 16, 16, 46, 11])
    T = "Settings!$B$3"
    yellow = PatternFill("solid", fgColor="FFF8DC")
    for i, r in enumerate(rows):
        n = 5 + i
        vals = [r["param_id"], r["parameter"], r["unit"], r["kind"], r["direction"], r["reg_rule"],
                num(r["reg_cap"]) if num(r["reg_cap"]) is not None else ""]
        vals += [num(r[b]) if num(r[b]) is not None else r[b] for b in banks]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=n, column=j, value=v)
            c.alignment, c.border = WRAP, BORDER
            if 8 <= j <= 11:
                c.fill = yellow
        rng = f"H{n}:K{n}"
        ws.cell(row=n, column=12, value=f'=IF(COUNT({rng})=0,"",MEDIAN({rng}))').border = BORDER
        for k, col in enumerate("HIJK"):
            X, D, E, G, M = f"{col}{n}", f"$D{n}", f"$E{n}", f"$G{n}", f"$L{n}"
            L = (f'IF(COUNT({rng})<2,"No peer data",'
                 f'IF(IF({E}="higher",{X}>{M}*(1+{T}),{X}<{M}*(1-{T})),IF({D}="risk","Higher risk",IF({D}="price","Cheaper","Worse")),'
                 f'IF(IF({E}="higher",{X}<{M}*(1-{T}),{X}>{M}*(1+{T})),IF({D}="risk","Too rigid",IF({D}="price","More expensive","Better")),"In line")))')
            f = (f'=IF(OR({D}="info",NOT(ISNUMBER({X}))),"",IF(ISNUMBER({G}),'
                 f'IF(IF({E}="higher",{X}>{G},{X}<{G}),"Above rule limit",IF({X}={G},"At rule limit",{L})),{L}))')
            c = ws.cell(row=n, column=13 + k, value=f)
            c.border, c.alignment = BORDER, Alignment(horizontal="center", vertical="top", wrap_text=True)
        ws.cell(row=n, column=17, value=r["notes"]).alignment = WRAP
        ws.cell(row=n, column=18, value=r["confidence"]).alignment = WRAP
        for j in (17, 18):
            ws.cell(row=n, column=j).border = BORDER
    last = 4 + len(rows)
    for name, (fill, font) in LABEL_COLORS.items():
        ws.conditional_formatting.add(
            f"M5:P{last}",
            FormulaRule(formula=[f'M5="{name}"'], fill=PatternFill("solid", fgColor=fill),
                        font=Font(color=font, bold=True)))
    ws.freeze_panes = "C5"
    return ws


def rulebook_sheet(wb, market, data):
    ws = wb.create_sheet(f"{market} rulebook")
    ws["A1"] = f"{market} master rulebook: retail credit (what the central bank / regulator requires)"
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    ws["A2"] = f"As of {AS_OF}. 'verify' = check against the regulator's text before relying on it."
    header(ws, 4, data[0], [11, 34, 90, 18, 42, 12])
    for i, row in enumerate(data[1:]):
        for j, v in enumerate(row, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.alignment, c.border = WRAP, BORDER
    ws.freeze_panes = "C5"


def build_xlsx(markets, rulebooks, sources):
    wb = Workbook()
    ws = wb.active
    ws.title = "Start here"
    lines = [
        ("Master Rulebook and Bank Comparison", Font(bold=True, size=16, color=NAVY)),
        (f"US, UK and UAE. Retail comparison with live labels, plus finance houses, SME and corporate rulebooks and bank data (sheets FH, SME, Corporate, Banks SME+corp). Public data as of {AS_OF}; run 2 on 13 November 2026.", Font(italic=True)),
        ("", None),
        ("What this is", Font(bold=True, color=TEAL)),
        ("1. A 'master rulebook' per country: the hard limits and must-do rules set by the central bank / regulator.", None),
        ("2. A comparison per country: four real banks' published terms next to those rules and next to each other.", None),
        ("3. Automatic labels for every bank and measure, so you can see where a bank is too strict or takes more risk.", None),
        ("", None),
        ("What the labels mean", Font(bold=True, color=TEAL)),
        ("Too rigid: stricter than the middle of its peers. The bank may be turning away customers others accept.", None),
        ("Higher risk: looser than its peers. Not wrong in itself; check it matches the bank's risk appetite.", None),
        ("In line: within 5% of the middle of its peers (change the 5% on the Settings sheet).", None),
        ("At rule limit: the bank already lends to the regulator's maximum. No room to loosen further.", None),
        ("Above rule limit: outside a standard rule (e.g. a US 40-year mortgage is outside the 30-year Qualified Mortgage).", None),
        ("Cheaper / More expensive: for prices (rates and fees).", None),
        ("Better / Worse: for results such as bad-debt write-offs.", None),
        ("", None),
        ("Read with care", Font(bold=True, color=TEAL)),
        ("Only published information is used. Banks do not publish everything (e.g. minimum credit scores).", None),
        ("Each row has a confidence grade: H = bank or regulator page; M = search extract or trade press; L = comparison site.", None),
        ("The US and UK mostly set principles, not numbers. So most US/UK bank limits are the bank's own choice.", None),
        ("Bank loan-book sizes are group or segment figures, not market shares.", None),
        ("Full research, with every source: _bmad-output/planning-artifacts/research/domain-master-rulebook-retail-credit-us-uk-uae-2026-11-12/", None),
    ]
    for i, (t, f) in enumerate(lines, 1):
        c = ws.cell(row=i, column=1, value=t)
        if f:
            c.font = f
    ws.column_dimensions["A"].width = 120

    # Bank summary sheet with live COUNTIFs
    sm = wb.create_sheet("Bank summary")
    sm["A1"] = "How many measures fall in each label, per bank (updates automatically)"
    sm["A1"].font = Font(bold=True, size=14, color=NAVY)
    labs = ["Too rigid", "Higher risk", "In line", "At rule limit", "Above rule limit",
            "Cheaper", "More expensive", "Better", "Worse"]
    header(sm, 3, ["Market", "Bank"] + labs, [8, 22] + [13] * len(labs))
    r = 4
    for market, banks, rows in markets:
        for k, b in enumerate(banks):
            col = "MNOP"[k]
            sm.cell(row=r, column=1, value=market)
            sm.cell(row=r, column=2, value=b)
            for j, lab in enumerate(labs):
                sm.cell(row=r, column=3 + j,
                        value=f"=COUNTIF('{market} compare'!{col}5:{col}{4 + len(rows)},\"{lab}\")")
            for j in range(1, 3 + len(labs)):
                sm.cell(row=r, column=j).border = BORDER
            r += 1

    for market, banks, rows in markets:
        compare_sheet(wb, market, banks, rows)
    for market, data in rulebooks:
        rulebook_sheet(wb, market, data)

    st = wb.create_sheet("Settings")
    st["A1"] = "Settings"
    st["A1"].font = Font(bold=True, size=14, color=NAVY)
    st["A3"], st["B3"] = "Difference from peer median that counts as 'different'", THRESHOLD
    st["B3"].number_format = "0%"
    st["B3"].fill = PatternFill("solid", fgColor="FFF8DC")
    st.column_dimensions["A"].width = 55

    so = wb.create_sheet("Sources")
    header(so, 1, ["From (research file)", "Source URL"], [44, 120])
    for i, (f, u) in enumerate(sources, 2):
        so.cell(row=i, column=1, value=f)
        so.cell(row=i, column=2, value=u)
    add_extra_sheets(wb)
    path = OUT / "Master Rulebook and Bank Comparison.xlsx"
    wb.save(path)
    return path


# ---------- run 2: finance houses, SME, corporate ----------
RUN2 = ROOT / "_bmad-output/planning-artifacts/research/domain-master-rulebook-fh-sme-corporate-us-uk-uae-2026-11-13/digests"
EXTRA = [  # (sheet, digest, kind, note)
    ("FH rulebook US", "us-fh-r1-1.md", "md", "US non-bank consumer lenders: state licensing, state rate caps, pawn laws"),
    ("FH rulebook UK", "uk-fh-r1-1.md", "md", "UK consumer credit firms: FCA authorisation, HCSTC cap, pawnbroking, motor finance"),
    ("FH lenders US", "us-fh-r1-1.md", "csv", "Published terms and 3Q26 results of 4 US non-bank lenders"),
    ("FH lenders UK", "uk-fh-r1-1.md", "csv", "Published terms and latest results of 4 UK lenders (Vanquis, Close Brothers hold bank licences)"),
    ("SME rulebook", "sme-rules-r1-1.md", "md", "SME definitions, special lending rules, guarantee schemes, capital: UAE, UK, US"),
    ("Corporate rulebook", "corp-rules-r1-1.md", "md", "Single-borrower / large-exposure, related-party, concentration, provisioning, capital: UAE, UK, US"),
    ("Banks SME+corp UAE", "uae-banks-wholesale-r1-1.md", "csv", "Published SME/corporate data. Definitions differ by bank: NOT like-for-like"),
    ("Banks SME+corp UK", "uk-banks-wholesale-r1-1.md", "csv", "Published SME/corporate data. Definitions differ by bank: NOT like-for-like"),
    ("Banks SME+corp US", "us-banks-wholesale-r1-1.md", "csv", "Published SME/commercial data. Criticized exposure is not comparable across banks"),
]


def extract_md_tables(text):
    """All markdown table rows from tables whose header starts with param_id (header once)."""
    head, rows = None, []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "param_id":
            head = head or cells
            continue
        if re.match(r"^\|\s*-", line) or head is None:
            continue
        if len(cells) >= len(head) - 1:
            rows.append(cells[:len(head)])
    return [head] + rows if head else []


def extract_csv_block(text):
    m = re.search(r"```csv\n(.*?)```", text, re.S)
    return list(csv.reader(m.group(1).strip().splitlines())) if m else []


def add_extra_sheets(wb):
    if not RUN2.exists():
        return
    for sheet, dig, kind, note in EXTRA:
        f = RUN2 / dig
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        data = extract_md_tables(t) if kind == "md" else extract_csv_block(t)
        if not data:
            continue
        with open(DATA / (sheet.lower().replace(" ", "_").replace("+", "_") + ".csv"), "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(data)
        ws = wb.create_sheet(sheet[:31])
        ws["A1"] = sheet
        ws["A1"].font = Font(bold=True, size=14, color=NAVY)
        ws["A2"] = f"{note}. Public data as of 13 Nov 2026. Sources and confidence: research digest {dig}."
        header(ws, 4, data[0], [16] + [28] * (len(data[0]) - 1))
        for i, row in enumerate(data[1:]):
            for j, v in enumerate(row, 1):
                c = ws.cell(row=5 + i, column=j, value=v)
                c.alignment, c.border = WRAP, BORDER
        ws.freeze_panes = "B5"


# ---------- one-pagers ----------
def fmt(v, unit):
    n = num(v)
    if n is None:
        return html.escape(str(v)) if v else "&ndash;"
    if unit in ("AED", "GBP", "USD", "AED/month", "GBP/year") or n >= 1000:
        return f"{n:,.0f}"
    s = f"{n:,.2f}".rstrip("0").rstrip(".")
    return s


def chip(lab):
    if not lab:
        return ""
    bg, fg = LABEL_COLORS.get(lab, ("EEEEEE", "333333"))
    return f'<span class="chip" style="background:#{bg};color:#{fg}">{lab}</span>'


def advice(bank, rows, banks):
    groups = {}
    for r in rows:
        if r["kind"] == "info":
            continue
        vals = [r[b] for b in banks]
        lab = label(r[bank], vals, r["reg_cap"], r["direction"], r["kind"])
        if lab:
            med = [num(x) for x in vals if num(x) is not None]
            groups.setdefault(lab, []).append((r, fmt(r[bank], r["unit"]),
                                               fmt(statistics.median(med), r["unit"]) if med else "&ndash;"))
    msgs = []
    def items(lab, with_med=True):
        return "; ".join(f"{html.escape(r['parameter'][0].lower() + r['parameter'][1:])} ({v}{' vs typical ' + m if with_med else ''})"
                         for r, v, m in groups.get(lab, []))
    if "Too rigid" in groups:
        msgs.append(("Where you may be missing business",
                     f"You are stricter than similar banks on: {items('Too rigid')}. Other banks accept customers you may be turning away."))
    if "Higher risk" in groups:
        msgs.append(("Where you take more risk than peers",
                     f"You are looser than similar banks on: {items('Higher risk')}. Check this matches your risk appetite and pricing."))
    if "Above rule limit" in groups:
        msgs.append(("Outside a standard rule",
                     f"{items('Above rule limit', False)}. Allowed, but outside the standard safe harbour; check pricing, capital and disclosures."))
    if "At rule limit" in groups:
        msgs.append(("Already at the regulator's maximum",
                     f"{items('At rule limit', False)}. No room to loosen these; compete on price and service instead."))
    if "More expensive" in groups:
        msgs.append(("Priced above peers", f"{items('More expensive')}."))
    if "Cheaper" in groups:
        msgs.append(("Priced below peers", f"{items('Cheaper')}. Check the margin still covers expected losses."))
    if "Worse" in groups:
        msgs.append(("Results worse than peers", f"{items('Worse')}. Tighten where losses come from before loosening anywhere else."))
    if "Better" in groups:
        msgs.append(("Results better than peers", f"{items('Better')}. There may be room to take a little more risk safely."))
    if not msgs:
        msgs.append(("Overall", "Mostly in line with peers on the published measures."))
    return msgs, {k: len(v) for k, v in groups.items()}


def bar_svg(counts, width=260):
    order = ["Too rigid", "Higher risk", "Above rule limit", "At rule limit", "In line",
             "Cheaper", "More expensive", "Better", "Worse", "No peer data"]
    total = sum(counts.get(k, 0) for k in order) or 1
    x, parts = 0, []
    for k in order:
        c = counts.get(k, 0)
        if not c:
            continue
        w = width * c / total
        bg, fg = LABEL_COLORS[k]
        parts.append(f'<rect x="{x:.1f}" y="0" width="{w:.1f}" height="16" fill="#{bg}" stroke="#fff"/>'
                     f'<text x="{x + w / 2:.1f}" y="12" font-size="10" text-anchor="middle" fill="#{fg}">{c}</text>')
        x += w
    return f'<svg width="{width}" height="16" role="img">{"".join(parts)}</svg>'


CSS = """
@page { size: A4; margin: 14mm 13mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #1d2433; font-size: 10.5px; }
h1 { color: #14213D; font-size: 22px; margin: 0 0 4px; }
h2 { color: #14213D; font-size: 17px; margin: 0; }
.sub { color: #0F7B7B; font-size: 11px; margin-bottom: 8px; }
.page { page-break-after: always; }
table { border-collapse: collapse; width: 100%; margin-top: 6px; }
th { background: #14213D; color: #fff; text-align: left; padding: 4px 5px; font-size: 9.5px; }
td { border-bottom: 1px solid #e3e6ec; padding: 3px 5px; vertical-align: top; font-size: 9.5px; }
.chip { padding: 1px 6px; border-radius: 8px; font-weight: 600; font-size: 9px; white-space: nowrap; }
.box { border-left: 4px solid #0F7B7B; background: #f4f8f8; padding: 5px 8px; margin: 5px 0; }
.box b { color: #14213D; }
.foot { color: #667085; font-size: 8.5px; margin-top: 8px; }
.legend span { margin-right: 6px; }
"""


def build_pdf(markets):
    pages, cover_rows = [], []
    for market, banks, rows in markets:
        for bank in banks:
            msgs, counts = advice(bank, rows, banks)
            cover_rows.append(f"<tr><td>{market}</td><td><b>{html.escape(bank)}</b></td>"
                              f"<td>{counts.get('Too rigid', 0)}</td><td>{counts.get('Higher risk', 0)}</td>"
                              f"<td>{counts.get('At rule limit', 0) + counts.get('Above rule limit', 0)}</td>"
                              f"<td>{bar_svg(counts)}</td></tr>")
            trs = []
            for r in rows:
                vals = [r[b] for b in banks]
                lab = label(r[bank], vals, r["reg_cap"], r["direction"], r["kind"])
                med = [num(x) for x in vals if num(x) is not None]
                trs.append(f"<tr><td>{html.escape(r['parameter'])}<br><span style='color:#667085'>{html.escape(r['unit'])}</span></td>"
                           f"<td><b>{fmt(r[bank], r['unit'])}</b></td>"
                           f"<td>{fmt(statistics.median(med), r['unit']) if med and r['kind'] != 'info' else '&ndash;'}</td>"
                           f"<td>{html.escape(r['reg_rule'])}</td><td>{chip(lab)}</td>"
                           f"<td style='color:#667085'>{html.escape(r['confidence'])}</td></tr>")
            boxes = "".join(f'<div class="box"><b>{t}.</b> {m}</div>' for t, m in msgs[:6])
            pages.append(f"""<div class="page">
<h2>{html.escape(bank)} <span style="color:#0F7B7B;font-size:12px">{market} &middot; retail</span></h2>
<div class="sub">Compared with {', '.join(html.escape(b) for b in banks if b != bank)} and the {market} rulebook &middot; public data as of {AS_OF}</div>
<div>{bar_svg(counts, 420)}</div>
<h3 style="color:#14213D;margin:8px 0 2px">What we would tell this bank</h3>{boxes}
<table><tr><th style="width:27%">Measure</th><th>This bank</th><th>Peer median</th><th style="width:33%">Regulator rule</th><th>Label</th><th>Conf.</th></tr>{''.join(trs)}</table>
<div class="foot">Labels: compared with the middle of the four banks (5% band) and with the rule limit. Confidence: H = bank/regulator page, M = search extract/trade press, L = comparison site. Published terms only; banks' internal credit policies are not public. Not investment or legal advice.</div>
</div>""")
    legend = "".join(chip(k) + " " for k in ["Too rigid", "Higher risk", "In line", "At rule limit", "Above rule limit", "Cheaper", "More expensive", "Better", "Worse"])
    cover = f"""<div class="page"><h1>Retail Bank Check</h1>
<div class="sub">12 banks &middot; US, UK and UAE &middot; each bank compared with its own regulator's rules and with three peers &middot; {AS_OF}</div>
<div class="box"><b>How to read this.</b> Each page shows one bank. <b>Too rigid</b> = stricter than similar banks, so it may be missing business. <b>Higher risk</b> = looser than similar banks; check it matches the bank's risk appetite. <b>At rule limit</b> = already at the regulator's maximum.</div>
<div class="legend" style="margin:6px 0">{legend}</div>
<table><tr><th>Market</th><th>Bank</th><th>Too rigid</th><th>Higher risk</th><th>At / above rule limit</th><th>All labels</th></tr>{''.join(cover_rows)}</table>
<div class="box" style="margin-top:10px"><b>Big picture.</b> The UAE sets hard numbers (debt-burden 50%, 48-month loans, 85/80% home LTV), and the four UAE banks already lend to most of those limits, so they compete on salary entry levels and price. The US and UK set principles, not numbers, so almost every limit is the bank's own choice and the gaps between banks are wider.</div>
<div class="foot">Source data and every citation: Retail Master Rulebook and Bank Comparison.xlsx (Sources sheet) and the BMAD research folder. Retail only; SME, corporate and finance houses come next.</div></div>"""
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>Retail Bank Check</title><style>{CSS}</style></head><body>{cover}{''.join(pages)}</body></html>"
    WORK.mkdir(parents=True, exist_ok=True)
    src = WORK / "onepagers.html"
    src.write_text(doc, encoding="utf-8")
    pdf = OUT / "Retail Bank Check - One-Pagers.pdf"
    subprocess.run([CHROME, "--headless=new", f"--user-data-dir={WORK / 'chrome-profile'}", "--disable-gpu",
                    "--no-pdf-header-footer", "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", src.as_uri()],
                   check=False, capture_output=True, timeout=180)
    return pdf


def main():
    n_us = extract_rulebook("us-rules-r1-1.md", "rulebook_us.csv", "US")
    n_uk = extract_rulebook("uk-rules-r1-1.md", "rulebook_uk.csv", "UK")
    markets, rulebooks = [], []
    for market, cfile, rfile, _ in MARKETS:
        banks, rows = load_compare(cfile)
        markets.append((market, banks, rows))
        rulebooks.append((market, load_rulebook(rfile)))
    sources = collect_sources()
    x = build_xlsx(markets, rulebooks, sources)
    p = build_pdf(markets) if "--no-pdf" not in sys.argv else None
    print(f"rulebook rows US={n_us} UK={n_uk}; sources={len(sources)}")
    print("xlsx:", x)
    print("pdf:", p, "exists" if p and p.exists() else "")
    # print label summary for checking
    for market, banks, rows in markets:
        for b in banks:
            _, c = advice(b, rows, banks)
            print(market, b, c)


if __name__ == "__main__":
    main()
