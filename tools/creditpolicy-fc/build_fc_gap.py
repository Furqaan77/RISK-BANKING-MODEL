# Builds, from fc_data.py (03-parameter-sheet.md is NOT written here; it is the source of truth):
#   04-benchmark-gap-report.md (into OUT_DIR)
#   gap_fc.html + "Benchmark and Gap Report - UAE Finance Company Retail Credit Policy.pdf"
# Usage: python build_fc_gap.py <OUT_DIR> [--md-only]
import html, math, pathlib, subprocess, sys
from collections import Counter

import fc_data as d

OUT = pathlib.Path(sys.argv[1])
WORK = pathlib.Path(__file__).parent
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
PDF_NAME = "Benchmark and Gap Report - UAE Finance Company Retail Credit Policy.pdf"
E = html.escape


def pmt(p, rate, n):
    i = rate / 12
    return p * i / (1 - (1 + i) ** -n)


def flat_inst(p, fr, n):
    return p * (1 + fr * n / 12) / n


def aed(x):
    return "AED {:,.0f}".format(x)


# ---------------- computed scenario numbers (all in fc_scen.py) ----------------
from fc_scen import *  # noqa: F401,F403
import fc_scen as sc

TOT = Counter(i[6] for i in d.ITEMS)
NITEMS = len(d.ITEMS)
assert sum(TOT.values()) == NITEMS == 60
SIGNOFF = [it for it in d.ITEMS if set(it[7].split("/")) & {"A", "P"}]
assert len(SIGNOFF) == 26
N_A = sum(1 for it in SIGNOFF if "A" in it[7].split("/"))
N_P = len(SIGNOFF) - N_A
N_REG = 10

# ---------------- palette (dataviz reference palette, light; validated) ----------------
SURF = "#ffffff"
INK, INK2, MUTED, GRID = "#14213d", "#52514e", "#6b7280", "#e3e6ea"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
GROUP_COL = {"us": CAT[0], "fc": CAT[1], "bank": CAT[2], "digital": CAT[3]}
GROUP_NAME = {"us": "Our finance-company policy", "fc": "UAE finance companies", "bank": "Top-5 banks", "digital": "Digital / BNPL lenders"}
RATING_COL = dict(zip(d.RATINGS, CAT))
TINT = {d.N: "#dce9f9", d.T: "#fde3d8", d.E: "#d3f1e6", d.X: "#fdefc9", d.R: "#fbe4ed", d.O: "#d6ecd6"}
FONT = "font-family:'IBM Plex Sans','Segoe UI',sans-serif"


# ---------------- SVG helpers ----------------
def donut_svg(rows, colors, centre_big, centre_small, aria):
    W = H = 210
    cx = cy = 105
    r, ri = 95, 56
    total = sum(v for _, v, *_ in rows)
    out = ['<svg viewBox="0 0 {} {}" class="pie" role="img" aria-label="{}" style="{}">'.format(W, H, E(aria), FONT)]
    a0 = -math.pi / 2
    for (row, col) in zip(rows, colors):
        v = row[1]
        a1 = a0 + 2 * math.pi * v / total
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if a1 - a0 > math.pi else 0
        out.append('<path d="M{:.2f},{:.2f} L{:.2f},{:.2f} A{r},{r} 0 {l} 1 {:.2f},{:.2f} Z" fill="{c}" stroke="{s}" stroke-width="2" stroke-linejoin="round"/>'.format(
            cx, cy, x0, y0, x1, y1, r=r, l=large, c=col, s=SURF))
        a0 = a1
    out.append('<circle cx="{}" cy="{}" r="{}" fill="{}"/>'.format(cx, cy, ri, SURF))
    out.append('<text x="{}" y="{}" text-anchor="middle" font-size="26" font-weight="700" fill="{}">{}</text>'.format(cx, cy + 4, INK, E(centre_big)))
    out.append('<text x="{}" y="{}" text-anchor="middle" font-size="10" fill="{}">{}</text>'.format(cx, cy + 21, INK2, E(centre_small)))
    out.append('</svg>')
    return "".join(out)


def pie_legend(rows, colors, unit="", pct=True):
    total = sum(r[1] for r in rows)
    h = ['<table class="plg"><tbody>']
    for row, col in zip(rows, colors):
        label, v = row[0], row[1]
        sub = row[2] if len(row) > 2 else ""
        val = ("{:g}{}".format(v, unit)) if not pct else "{:g}{} ({:.0f}%)".format(v, unit, 100 * v / total)
        h.append('<tr><td class="sw"><i style="background:{}"></i></td><td><b>{}</b>{}</td><td class="v">{}</td></tr>'.format(
            col, E(label), '<br><span class="small">' + E(sub) + '</span>' if sub else "", E(val)))
    h.append('</tbody></table>')
    return "".join(h)


def axis_ticks(vmin, vmax, step):
    v = vmin
    while v <= vmax + 1e-9:
        yield v
        v += step


def range_svg(rows, vmax, step, unit, aria):
    W, LBL, X0, X1 = 700, 200, 205, 640
    RH, TOP = 25, 22
    H = TOP + RH * len(rows) + 8
    sx = lambda v: X0 + (X1 - X0) * v / vmax
    out = ['<svg viewBox="0 0 {} {}" class="chart" role="img" aria-label="{}" style="{}">'.format(W, H, E(aria), FONT)]
    for t in axis_ticks(0, vmax, step):
        out.append('<line x1="{x:.1f}" x2="{x:.1f}" y1="{a}" y2="{b}" stroke="{g}" stroke-width="1"/>'.format(x=sx(t), a=TOP - 4, b=H - 6, g=GRID))
        out.append('<text x="{:.1f}" y="{}" font-size="9" fill="{}" text-anchor="middle">{:g}{}</text>'.format(sx(t), TOP - 9, MUTED, t, unit))
    for k, (label, grp, lo, hi, note) in enumerate(rows):
        y = TOP + RH * k + RH / 2
        col = GROUP_COL[grp]
        wt = "700" if grp == "us" else "400"
        out.append('<text x="{}" y="{:.1f}" font-size="10" fill="{}" text-anchor="end" font-weight="{}">{}</text>'.format(LBL - 4 + 4, y + 3.5, INK, wt, E(label)))
        if hi is not None:
            out.append('<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="8" rx="4" fill="{}"/>'.format(sx(lo), y - 4, sx(hi) - sx(lo), col))
            for v in (lo, hi):
                out.append('<circle cx="{:.1f}" cy="{:.1f}" r="5" fill="{}" stroke="{}" stroke-width="2"/>'.format(sx(v), y, col, SURF))
            txt = "{:g}–{:g}{}".format(lo, hi, unit)
            out.append('<text x="{:.1f}" y="{:.1f}" font-size="9.5" fill="{}">{}</text>'.format(sx(hi) + 9, y + 3.5, INK2, E(txt)))
        else:
            out.append('<circle cx="{:.1f}" cy="{:.1f}" r="5.5" fill="{}" stroke="{}" stroke-width="2"/>'.format(sx(lo), y, col, SURF))
            pre = "from " if note == "from" else ""
            post = " ({})".format(note) if note and note != "from" else ""
            out.append('<text x="{:.1f}" y="{:.1f}" font-size="9.5" fill="{}">{}{:g}{}{}</text>'.format(sx(lo) + 9, y + 3.5, INK2, pre, lo, unit, E(post)))
    out.append('</svg>')
    return "".join(out)


def bar_path(x, y, w, h, r=4):
    if w <= r:
        return '<rect x="{:.1f}" y="{:.1f}" width="{:.1f}" height="{}"/>'.format(x, y, max(w, 0.5), h)
    return ('M{x:.1f},{y:.1f} H{a:.1f} Q{b:.1f},{y:.1f} {b:.1f},{c:.1f} V{d:.1f} Q{b:.1f},{e:.1f} {a:.1f},{e:.1f} H{x:.1f} Z'
            .format(x=x, y=y, a=x + w - r, b=x + w, c=y + r, d=y + h - r, e=y + h))


def hbar_svg(rows, vmax, step, fmt, aria, label_w=230):
    W, X0, X1 = 700, label_w + 5, 615
    RH, TOP, BH = 24, 20, 14
    H = TOP + RH * len(rows) + 6
    sx = lambda v: X0 + (X1 - X0) * v / vmax
    out = ['<svg viewBox="0 0 {} {}" class="chart" role="img" aria-label="{}" style="{}">'.format(W, H, E(aria), FONT)]
    for t in axis_ticks(0, vmax, step):
        out.append('<line x1="{x:.1f}" x2="{x:.1f}" y1="{a}" y2="{b}" stroke="{g}" stroke-width="1"/>'.format(x=sx(t), a=TOP - 4, b=H - 4, g=GRID))
        out.append('<text x="{:.1f}" y="{}" font-size="9" fill="{}" text-anchor="middle">{}</text>'.format(sx(t), TOP - 8, MUTED, E(fmt(t, axis=True))))
    for k, row in enumerate(rows):
        label, grp, v, note = row
        y = TOP + RH * k + (RH - BH) / 2
        col = GROUP_COL[grp]
        wt = "700" if grp == "us" else "400"
        out.append('<text x="{}" y="{:.1f}" font-size="10" fill="{}" text-anchor="end" font-weight="{}">{}</text>'.format(label_w, y + BH / 2 + 3.5, INK, wt, E(label)))
        w = sx(v) - X0
        if v > 0:
            p = bar_path(X0, y, w, BH)
            if p.startswith("<rect"):
                out.append(p.replace("/>", ' fill="{}"/>'.format(col)))
            else:
                out.append('<path d="{}" fill="{}"/>'.format(p, col))
        txt = note if (note and v == 0) else fmt(v) + ((" (" + note + ")") if note else "")
        out.append('<text x="{:.1f}" y="{:.1f}" font-size="9.5" fill="{}">{}</text>'.format(X0 + max(w, 0) + 6, y + BH / 2 + 3.5, INK2, E(txt)))
    out.append('<line x1="{x}" x2="{x}" y1="{a}" y2="{b}" stroke="{c}" stroke-width="1"/>'.format(x=X0, a=TOP - 4, b=H - 4, c="#9aa3ad"))
    out.append('</svg>')
    return "".join(out)


def group_legend(groups=("us", "fc", "bank")):
    return '<div class="legend">' + "".join(
        '<span><i style="background:{}"></i>{}</span>'.format(GROUP_COL[g], E(GROUP_NAME[g])) for g in groups) + '</div>'


def fmt_aed(v, axis=False):
    if axis:
        return "0" if v == 0 else ("{:g}K".format(v / 1000))
    return "{:,.0f}".format(v)


def fmt_aedk(v, axis=False):
    if axis:
        return "0" if v == 0 else "{:g}K".format(v / 1000)
    return "{:,.0f}".format(v)


def chip(r):
    return '<span class="chip" style="background:{};border-color:{}">{}</span>'.format(TINT[r], RATING_COL[r], E(r))


# ---------------- narrative content ----------------
TITLE = "Benchmark and Gap Report: UAE Finance Company Retail Credit Policy"

KEY_MESSAGES = [
    "**What it is.** A retail credit policy for a pilot conventional finance company (FCR Part I licence, AED 150m capital). It keeps the bank-grade credit rules we recommended for UAE banks, and changes only what the finance-company rules or market require.",
    "**Where it stands.** Of {} policy items, {} sit inside the finance-company range, {} are better for customers than the typical finance company, {} are deliberately tighter, {} have no finance-company peer, {} are finance-company legal requirements, and {} products are not offered in the pilot.".format(
        NITEMS, TOT[d.N], TOT[d.E], TOT[d.T], TOT[d.X], TOT[d.R], TOT[d.O]),
    "**The one-line position.** Bank-grade customer selection, finance-company reach, and a price below the finance-company typical: employer-assigned loans from 12.99% against a typical 20–28%.",
    "**What limits growth is capital, not demand.** In years 0–2 liabilities may not exceed capital funds, so the whole loan book is capped at about AED 300m of assets. The policy caps the pilot at AED 250m of loans.",
    "**Before launch:** {} items need management sign-off ({} [A] adjusted, {} [P] proposals; list in section 7), and {} regulatory points need Legal & Compliance to confirm them against the FCR rulebook.".format(len(SIGNOFF), N_A, N_P, N_REG),
]

STANDOUT = [
    ("Bank-grade selection with finance-company reach",
     "Published AECB floors (541 / 560 / 600), DBR that counts cards and BNPL, a rate-rise stress test and 12 months of statements for the self-employed. No UAE finance company publishes credit floors."),
    ("A lower price for good risk",
     "Employer-assigned loans from 12.99% and non-assigned from 15.99%, against a finance-company typical of 20–28% and highs of 36–40%. Better selection pays for the lower price."),
    ("Bank-style security without moving the salary",
     "The employer-assigned track (assignment letter, EOS undertaking and direct debit) gives the security of a bank salary-transfer loan to customers who keep their salary account where it is. Most finance companies take only a cheque."),
    ("Small-ticket credit, done safely",
     "Salary advance from AED 3,000 net salary with a flat fee and at most 6 a year; BNPL (phase 2) capped below the legal limit. This serves workers banks do not lend to, without payday-loan pricing."),
    ("Gold loans with a clear safety margin",
     "70% loan-to-value (the only peer lends 75%) at 14.99%, with a published top-up call at 80% and sale at 85%. The customer has a 12.5% price cushion before any call."),
    ("Explainable AI inside capital-aware limits",
     "Policy always wins over the AI grade; every decision can be replayed; limits watch leverage, single-borrower and portfolio concentration every night."),
]

SCENARIOS = sc.SCENARIOS

TIGHTER = [
    ("F-16", "AECB floor (non-assigned ≥ 560; ≥ 600 for the AED 5,000 entry)",
     "No finance company publishes a floor; most lend to any customer in 'good standing' and price the risk.",
     "Keep for the pilot. After 6 months of performance data, consider opening 541–559 on the non-assigned track for AI grades 1–4 only.",
     "Lower volume in the near-prime segment; better loss rates against a sector NPL of 7.1%."),
    ("F-44", "Auto rate (new 3.49%, used 4.49% flat)",
     "Aafaq from 2.5% flat; Al Futtaim 3% (dealer-subsidised captive); banks 1.75–3.19%.",
     "Keep: lower prices lose money at finance-company funding costs. Seek dealer subsidies for 'from 2.99%' campaigns instead.",
     "Auto stays a small, access-led product."),
    ("F-49", "Gold loan-to-value 70% (peer 75%)",
     "Finance House lends 75%.",
     "Keep 70% for the pilot; review after one gold-price cycle.",
     "Slightly smaller loans; much lower risk of forced sales."),
    ("F-53", "BNPL caps (AED 10,000 / 1× income / 6 months)",
     "Legal cap is AED 20,000 or 3 months' income, 12 months, fees ≤ 30%. Tamara lends up to AED 20,000.",
     "Keep for phase 2 launch; raise towards the legal cap only with 12 months of clean data.",
     "Smaller baskets; low arrears in a product with high fraud and over-borrowing risk."),
]

NOPEER = [
    ("F-14", "Employer categories A–D", "No finance company publishes one", "Approve the category criteria (Annex B of the policy)"),
    ("F-29", "First-instalment grace up to 60 days (nationals)", "Banks offer 120–365 days", "Product approval; check funding cost"),
    ("F-51", "EOSB-backed (inside employer-assigned loans)", "No finance company offers it", "Legal opinion on EOS undertakings to a finance company"),
    ("F-57", "Delegation-of-authority matrix", "Internal to each lender", "Board approval (FCR); review at least every 2 years"),
    ("F-58", "Portfolio limits", "Internal to each lender", "Board Risk / Credit Committee approval"),
]

REG_CONFIRM = [
    "FCR article numbers and values (capital, leverage, large exposures, liquidity, governance): read from search extracts because the rulebook returned HTTP 403.",
    "Whether the short-term credit caps (AED 20,000 / 3 months' income / 12 months / fees ≤ 30%) bind a Part I finance company's salary advance and BNPL. The policy applies them anyway.",
    "Whether employer salary-assignment letters and EOS undertakings in favour of a finance company are enforceable (no salary account is held).",
    "Whether the November 2025 removal of the AED 5,000 minimum salary applies to finance companies and to cards.",
    "The CBUAE maximum write-off period, and whether the Credit Risk Management Regulation C 3/2024 applies in full to finance companies.",
    "Credit-card minimum income of AED 60,000 a year (Regulation 29/2011 Article 5).",
    "The full Appendix 2 fee table (deferment AED 100, rescheduling AED 250, late-fee caps by product).",
    "Disbursement within 10 business days, and the 5-business-day cooling-off waiver rules.",
    "WPS-agent approval if the payroll-card route is used for salary advances.",
    "No-objection letters needed for each phase 1 product line before launch.",
]

assert len(REG_CONFIRM) == N_REG

LAUNCH = [
    "CBUAE no-objection letter for each product line.",
    "Board approval of this policy, the credit approval matrix and the creditworthiness procedures.",
    "AECB membership and monthly data submission tested.",
    "UAEDDS sponsor bank and direct-debit mandates live.",
    "Funding: bank lines or legal-entity deposits in place; treasury liquidity buffer ≥ 10% of liabilities.",
    "KFS templates (Arabic and English, with APR) for every product.",
    "Sales staff: telemarketing training (≥ 15 hours) and consent records.",
    "AI Risk Score Card: grades validated on finance-company data; policy rules loaded from config and passing validation.",
]

DATA_NOTES = [
    "**Bank figures are not market shares.** Bank retail-book sizes quoted elsewhere include group and overseas books. Only CBUAE totals (credit to individuals AED 645.8bn, Aug 2026; finance-company loans about AED 11.2bn, FSR 2025) are used for market-size comparisons and pies.",
    "**Finance-company status pie:** the 20 entities on the CB Register (Aug 2026), grouped by our reading of their websites and KFS documents. 'Active' means a published retail product and KFS; it is not a measure of size.",
    "**Loan-mix pie:** FSR 2025 shares of the whole finance-company sector, not of any one company.",
    "**Rates:** reducing balance unless marked flat. Flat rates are converted to reducing only where stated (Aafaq 8% flat is about 14.5%; our used-car 4.49% flat is about {} reducing).".format(pc(A_RED)),
    "**Ranges:** a bar shows the lowest and highest published value; a single dot means only one value (often a 'from' rate) is published.",
    "**Digital / BNPL lenders** (botim / CashNow, e& easyCredit, Tamara) are shown separately from full finance companies because they sell small, short loans.",
    "**Confidence:** H = read directly from a KFS, report or register; M = search extract (the FCR rulebook returned HTTP 403, so FCR values must be confirmed by Legal & Compliance). Finance companies publish no AECB floors, so the AECB comparison is qualitative.",
    "**Scenarios** use illustrative customers; every number is calculated by the build script from the policy values.",
]

SOURCES = [
    ("CBUAE", "CB Register (Aug 2026): 20 finance companies", "https://centralbank.ae/media/hw0lreyi/cb-register-august-2026.pdf", "H"),
    ("CBUAE", "Financial Stability Report 2025: FC loans, NPL, loan mix", "https://centralbank.ae/media/44ianby2/financial-stability-report-en-2025.pdf", "H"),
    ("CBUAE", "Short-term credit (BNPL) framework press release", "https://www.centralbank.ae/media/izlhi5rb/cbuae-introduces-framework-for-the-regulation-of-short-term-credit-facilities_en.pdf", "H"),
    ("CBUAE", "Consumer Protection Standards", "https://centralbank.ae/media/fjof4adk/1.pdf", "H"),
    ("CBUAE", "Finance Companies Regulation (rulebook)", "https://rulebook.centralbank.ae/en/rulebook/finance-companies-regulation-0", "M"),
    ("CBUAE", "Statistical Bulletin Aug 2026: credit to individuals AED 645.8bn", "https://centralbank.ae/media/njajo2nc/statistical-bulletin-august-2026.pdf", "H"),
    ("Finance House", "FY2025 financial statements", "https://www.financehouse.ae/wp-content/uploads/2026/04/Finance-House-LLC-financial-statements-FY-2025.pdf", "H"),
    ("Finance House", "Sulfah KFS", "https://www.financehouse.ae/wp-content/uploads/2026/08/Sulfah-New-KFS-v1.7.pdf", "H"),
    ("Finance House", "Gold loan KFS", "https://www.financehouse.ae/wp-content/uploads/2025/03/Key-Fact-Statement_Gold-Loan_210225.pdf", "H"),
    ("Deem", "Personal loan KFS", "https://www.deem.io/wp-content/uploads/2026/03/Personal-Loan_March_2026.pdf", "H"),
    ("Deem", "Schedule of fees", "https://www.deem.io/wp-content/uploads/2026/09/Schedule-of-Fees-Charges-September-2026-English.pdf", "H"),
    ("Deem", "Salary advance KFS", "https://www.deem.io/wp-content/uploads/2025/04/Salary-Advance-KFS.pdf", "H"),
    ("Al Ain Finance", "KFS", "https://alainfinance.ae/images/subpages/aaf-key-fact-statement-english-6a9679c4d6487.pdf", "H"),
    ("Aafaq", "Personal finance KFS", "https://aafaq.ae/wp-content/uploads/2026/03/KFS_Personal_Finance_EN.pdf", "H"),
    ("Siraj", "Personal finance KFS", "https://www.sirajfinance.com/help-desk/key-fact-statement-personal-finance_en.pdf", "H"),
    ("Mawarid", "Schedule of tariffs", "https://ik.imagekit.io/tbc123/mawarid/media/schedule_of_tariffs_and_charges__202609_approved_F3RtKQ8z-.pdf", "H"),
    ("Al Futtaim Finance", "Auto loan KFS", "https://aff.alfuttaimfinance.ae/wp-content/uploads/sites/28/2026/09/Auto-Loan-Individual-EN-KFS-V4.1-28072026.pdf", "H"),
    ("Tamara", "KFS", "https://tamara.co/en-ae/key-fact-statement", "H"),
    ("botim / CashNow", "KFS", "https://www.cashnow.ai/key-facts-statement", "H"),
    ("e&", "easyCredit", "https://www.eandmoney.com/en/services/easy-credit.html", "H"),
    ("Banks", "Top-five conventional bank benchmark", "../credit-policy-uae-conventional/01-benchmark-conventional.md", "H/M"),
]


def md_bold_to_html(s):
    import re
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", E(s))


signoff = SIGNOFF

# =====================================================================
# 04-benchmark-gap-report.md
# =====================================================================
m = []
m.append("# " + TITLE + "\n")
m.append("*9 November 2026. For management and the credit team. The PDF version has the charts; this file holds the same content with the chart data as tables.*\n")
m.append("## 1. The answer in one page")
for k in KEY_MESSAGES:
    m.append("- " + k)
m.append("\n**Rating of the {} policy items** (chart: donut)\n".format(NITEMS))
m.append("| Rating | Items | Share | Meaning |\n|---|---|---|---|")
for r in d.RATINGS:
    m.append("| {} | {} | {:.0f}% | {} |".format(r, TOT[r], 100 * TOT[r] / NITEMS, d.RATING_TEXT[r]))
m.append("\n## 2. The finance-company market in pictures")
m.append("| Fact | Value | Source |\n|---|---|---|")
m.append("| Licensed finance companies | 20 (CB Register, Aug 2026) | CBUAE |")
m.append("| Finance-company loans | about AED 11.2bn (−8.8% in 2025) | FSR 2025 |")
m.append("| Bank credit to individuals | AED 645.8bn (Aug 2026), about 58 times the whole finance-company sector | CBUAE Statistical Bulletin |")
m.append("| Net NPL | finance companies 7.1%; banks 1.6% | FSR 2025 |")
m.append("| Our pilot cap | AED 250m of loans (about 2% of the sector) | Policy §4 |")
m.append("\n**The 20 licensed finance companies by status** (chart: donut)\n")
m.append("| Status | Count | Companies |\n|---|---|---|")
for lab, n, who in d.FC_STATUS:
    m.append("| {} | {} | {} |".format(lab, n, who))
m.append("\n**Finance-company loans by type** (FSR 2025; chart: donut)\n")
m.append("| Type | Share |\n|---|---|")
for lab, v in d.FC_LOAN_MIX:
    m.append("| {} | {:g}% |".format(lab, v))
m.append("\nPersonal and vehicle loans are only about 14% of finance-company lending: the retail space is small and run by a handful of active lenders.")
m.append("\n## 3. Where our policy stands on key numbers")
m.append("**Personal-loan interest rates, % a year (reducing)** (chart: ranges)\n")
m.append("| Lender | Group | From | To |\n|---|---|---|---|")
for lab, g, lo, hi, note in d.PL_RATES:
    m.append("| {} | {} | {:g}% | {} |".format(lab, GROUP_NAME["fc" if g == "digital" else g], lo, "{:g}%".format(hi) if hi else note or "–"))
m.append("\n**Minimum salary for a personal loan, AED a month** (chart: bars)\n")
m.append("| Lender | Group | Minimum salary |\n|---|---|---|")
for lab, g, v, note in d.PL_MIN_SALARY:
    m.append("| {} | {} | {} |".format(lab, GROUP_NAME["fc" if g == "digital" else g], note if v == 0 else "{:,}".format(v) + (" ({})".format(note) if note else "")))
m.append("\n**Maximum personal loan, AED** (chart: bars)\n")
m.append("| Lender | Group | Maximum |\n|---|---|---|")
for lab, g, v, note in d.PL_MAX_AMOUNT:
    m.append("| {} | {} | {:,} |".format(lab, GROUP_NAME["fc" if g == "digital" else g], v))
m.append("\n**Credit-card interest, % a month** (chart: ranges)\n")
m.append("| Lender | Group | From | To |\n|---|---|---|---|")
for lab, g, lo, hi, note in d.CARD_RATES:
    m.append("| {} | {} | {:g}% | {} |".format(lab, GROUP_NAME["fc" if g == "digital" else g], lo, "{:g}%".format(hi) if hi else "–"))
m.append("\n**Gold-backed loans**\n")
m.append("| | Our policy | Finance House | Top-5 banks |\n|---|---|---|---|")
m.append("| Loan-to-value | 70% (call 80%, sale 85%) | 75% | not offered |")
m.append("| Rate | 14.99% | 16% | – |")
m.append("| Size | AED 5,000–250,000 | AED 5,000–500,000 | – |")
m.append("\n## 4. How we stand out among finance companies")
for i, (h_, t_) in enumerate(STANDOUT, 1):
    m.append("{}. **{}.** {}".format(i, h_, t_))
m.append("\n## 5. Real-life scenarios")
m.append("Numbers are computed with the policy rules (reducing-balance instalments unless flat). Names are illustrative.\n")
m.append("| Customer | Product | Outcome | Key number |\n|---|---|---|---|")
for r in sc.SUMMARY:
    m.append("| {} | {} | {} | {} |".format(*r))
m.append("")
for i, s in enumerate(SCENARIOS, 1):
    m.append("### Scenario {}: {}".format(i, s["title"]))
    m.append("| | |\n|---|---|")
    for key, lab in (("who", "Customer"), ("ask", "Wants"), ("banks", "Banks"), ("market", "Finance companies"), ("ours", "Our policy"), ("result", "Result")):
        m.append("| **{}** | {} |".format(lab, s[key]))
    m.append("\n**The maths**\n")
    m.append("| Step | Working | Result |\n|---|---|---|")
    for st, wk, rs in s["maths"]:
        m.append("| {} | {} | {} |".format(st, wk, rs))
    m.append("")
m.append("**Mariam's AED 60,000 over 48 months: total interest** (chart: bars)\n")
m.append("| Lender / rate | Total interest |\n|---|---|")
for lab, v in (("Our policy, 17.99%", M_INT), ("Finance House from 20%", M_20_INT), ("Typical finance company, 24%", M_24_INT), ("Deem top rate, 39.99%", M_40_INT)):
    m.append("| {} | {} |".format(lab, aed(v)))
m.append("\n**Khalid's buyout: total still to pay over 36 months** (chart: bars)\n")
m.append("| Option | Total |\n|---|---|")
for lab, v in (("Keep the 28% finance-company loan", K_OLD_TOT), ("Our buyout at 13.99%", K_NEW_TOT), ("Bank at 5.49% (salary moved)", K_BANK_TOT)):
    m.append("| {} | {} |".format(lab, aed(v)))
m.append("\n## 6. Gaps and improvements")
m.append("### 6.1 Tighter than the market: keep or loosen?")
m.append("| ID | Item | What the market does | Recommendation | Trade-off |\n|---|---|---|---|---|")
for r in TIGHTER:
    m.append("| {} | {} | {} | {} | {} |".format(*r))
m.append("\n### 6.2 No finance-company peer: approvals needed")
m.append("| ID | Item | Market | Approval needed |\n|---|---|---|---|")
for r in NOPEER:
    m.append("| {} | {} | {} | {} |".format(*r))
m.append("\n### 6.3 Deliberate gaps")
m.append("- **Customers earning AED 3,000–4,999:** salary advance only, no personal loan. Payday-style loans at 36% (Finance House) serve this segment; revisit after 12 months of pilot data.")
m.append("- **Home finance and deposit-backed loans:** not in the pilot (licence and FCR).")
m.append("- **Price vs banks:** a customer who will move their salary gets a cheaper loan at a bank. The policy targets customers who will not or cannot.")
m.append("\n### 6.4 Regulatory points for Legal & Compliance to confirm")
for i, r in enumerate(REG_CONFIRM, 1):
    m.append("{}. {}".format(i, r))
m.append("\n### 6.5 Launch checklist")
for r in LAUNCH:
    m.append("- [ ] " + r)
m.append("\n## 7. Item-by-item comparison")
m.append("See `03-parameter-sheet.md` for the full table of {} items with source tags. Rating summary:\n".format(NITEMS))
m.append("| Product area | " + " | ".join(d.RATINGS) + " |")
m.append("|---|" + "---|" * len(d.RATINGS))
for g in d.GROUPS:
    c = Counter(it[6] for it in d.ITEMS if it[0] == g)
    m.append("| {} | ".format(d.GROUP_SHORT[g]) + " | ".join(str(c[r]) for r in d.RATINGS) + " |")
m.append("| **Total** | " + " | ".join("**{}**".format(TOT[r]) for r in d.RATINGS) + " |")
m.append("\n### Sign-off list: {} items ({} [A] adjusted, {} [P] proposals)".format(len(SIGNOFF), N_A, N_P))
m.append("| ID | Item | Tag | Policy value | Rating |\n|---|---|---|---|---|")
for it in SIGNOFF:
    m.append("| {} | {} | {} | {} | {} |".format(it[1], it[2], " ".join("[{}]".format(t) for t in it[7].split("/")), it[3], it[6]))
m.append("\nThe policy text also marks two rules [P]: repricing when a salary account is moved without clearance (§8.1) and the sector watch-list (§7.5).")
m.append("\n## 8. Data notes and confidence")
for t_ in DATA_NOTES:
    m.append("- " + t_)
m.append("\n## 9. Sources")
m.append("| Group | Source | Link | Confidence |\n|---|---|---|---|")
for s in SOURCES:
    m.append("| {} | {} | {} | {} |".format(*s))
m.append("\nConfidence: H = read directly (KFS, report, register); M = search extract (the FCR rulebook returned HTTP 403). All checked 9 November 2026.")
(OUT / "04-benchmark-gap-report.md").write_text("\n".join(m) + "\n", encoding="utf-8")
print("md written", dict(TOT), "| sign-off", len(SIGNOFF))
if "--md-only" in sys.argv:
    sys.exit(0)

# =====================================================================
# HTML / PDF
# =====================================================================
CSS = """
@page { size: A4; margin: 14mm 13mm 16mm 13mm;
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 8pt 'IBM Plex Sans','Segoe UI',sans-serif; color: #5B6475; }
  @bottom-left { content: "Benchmark and Gap Report  |  UAE finance company retail credit policy v0.1"; font: 8pt 'IBM Plex Sans','Segoe UI',sans-serif; color: #5B6475; } }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }
body { font: 9.6pt/1.5 'IBM Plex Sans','Segoe UI',sans-serif; color: #14213D; margin: 0; background: #fff; }
h2, h3, h4 { font-family: 'Plus Jakarta Sans','Segoe UI',sans-serif; color: #14213D; break-after: avoid; }
h2 { font-size: 15pt; margin: 18px 0 8px; padding-bottom: 4px; border-bottom: 2px solid #0F7B7B; }
h3 { font-size: 11.5pt; margin: 14px 0 6px; color: #0F6E6A; }
h4 { font-size: 10pt; margin: 4px 0 2px; }
p { margin: 0 0 8px; }
ul, ol { margin: 4px 0 8px; padding-left: 18px; } li { margin: 3px 0; }
.cover { background: #14213D; color: #fff; padding: 22px 24px 20px; border-radius: 8px; margin-bottom: 12px; }
.cover small { color: #7FC4C4; font-weight: 600; letter-spacing: .1em; font-size: 8pt; }
.cover h1 { color: #fff; font: 800 21pt/1.15 'Plus Jakarta Sans','Segoe UI',sans-serif; margin: 6px 0 6px; }
.cover p { color: #C9D2E0; margin: 0; }
.headline { background: #E3F1F1; border-left: 4px solid #0F7B7B; padding: 10px 14px; margin: 10px 0; font-weight: 600; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 12px; font-size: 8.4pt; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
th { background: #14213D; color: #fff; text-align: left; padding: 5px 6px; font-weight: 600; vertical-align: bottom; }
td { padding: 5px 6px; border-bottom: 1px solid #D5DAE1; vertical-align: top; }
tbody tr:nth-child(even) td { background: #F4F6F9; }
.chip { display: inline-block; border-radius: 10px; padding: 1px 7px; font-size: 7.6pt; font-weight: 700; border: 1px solid; white-space: nowrap; color: #14213D; }
.row2 { display: flex; gap: 16px; align-items: flex-start; break-inside: avoid; margin: 6px 0 10px; }
.row2 > div { flex: 1; }
.piebox { display: flex; gap: 12px; align-items: center; break-inside: avoid; border: 1px solid #D5DAE1; border-radius: 8px; padding: 10px 12px; margin: 0 0 10px; }
.piebox svg.pie { width: 150px; height: 150px; flex: none; }
.piebox h4 { margin-bottom: 4px; }
table.plg { margin: 0; font-size: 8.3pt; }
table.plg td { border: 0; padding: 2px 4px; background: transparent !important; }
table.plg td.sw { width: 14px; padding-top: 5px; }
table.plg td.sw i { display: block; width: 10px; height: 10px; border-radius: 2px; }
table.plg td.v { text-align: right; white-space: nowrap; font-weight: 600; }
.chartbox { break-inside: avoid; border: 1px solid #D5DAE1; border-radius: 8px; padding: 10px 12px 6px; margin: 0 0 10px; }
.chartbox .note { font-size: 8pt; color: #5B6475; margin: 0 0 4px; }
svg.chart { width: 100%; height: auto; display: block; }
.legend { display: flex; gap: 16px; font-size: 8.3pt; color: #52514e; margin: 2px 0 6px; flex-wrap: wrap; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; vertical-align: -1px; margin-right: 5px; }
.tiles { display: flex; gap: 10px; margin: 6px 0 12px; break-inside: avoid; }
.tile { flex: 1; border: 1px solid #D5DAE1; border-radius: 8px; padding: 9px 11px; }
.tile b { display: block; font: 800 17pt/1.1 'Plus Jakarta Sans','Segoe UI',sans-serif; color: #14213D; }
.tile span { font-size: 8pt; color: #52514e; line-height: 1.3; display: block; margin-top: 3px; }
.std { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.std div { border: 1px solid #D5DAE1; border-top: 4px solid #2a78d6; border-radius: 6px; padding: 9px 11px; break-inside: avoid; }
.std h4 { margin: 0 0 4px; }
.std p { font-size: 8.8pt; margin: 0; }
.scen { break-inside: avoid; border: 1px solid #D5DAE1; border-left: 5px solid #2a78d6; border-radius: 6px; padding: 9px 13px; margin: 0 0 10px; }
.scen h3 { margin: 0 0 6px; color: #14213D; }
.scen dl { display: grid; grid-template-columns: 112px 1fr; gap: 3px 12px; margin: 0; font-size: 8.8pt; }
.scen dt { font-weight: 700; color: #0F6E6A; }
.scen dd { margin: 0; }
.scen dd.res { background: #E3F1F1; border-radius: 4px; padding: 3px 7px; font-weight: 600; }
.pb { break-before: page; }
.small { font-size: 8pt; color: #5B6475; }
.url { word-break: break-all; font-size: 7.4pt; }
.keep { break-inside: avoid; }
.cmp td:first-child { white-space: nowrap; font-weight: 600; }
.tags { font-size: 8.3pt; color: #44506a; }
.heat td.c { text-align: center; font-weight: 700; }
.chk li { list-style: none; margin-left: -16px; }
.what { font-size: 8.2pt; color: #3d4a5c; margin: 6px 0 2px; line-height: 1.4; }
.what b { color: #0F6E6A; }
table.maths { font-size: 8pt; margin: 7px 0 2px; }
table.maths th { background: #0F7B7B; padding: 3px 6px; }
table.maths td { padding: 3px 6px; }
table.maths td:last-child { text-align: right; white-space: nowrap; font-weight: 700; }
.ok { color: #0a6b3d; font-weight: 700; } .no { color: #b3261e; font-weight: 700; }
.chk li::before { content: "\\2610  "; color: #0F6E6A; }
"""

h = []
h.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>FC Benchmark and Gap Report</title>')
h.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">')
h.append('<style>' + CSS + '</style></head><body>')
h.append('<div class="cover"><small>BENCHMARK &amp; GAP REPORT &middot; 9 NOVEMBER 2026</small><h1>{}</h1>'.format(E(TITLE)) +
         '<p>The retail credit policy for a pilot conventional finance company, compared with UAE finance companies, digital and BNPL lenders, and the top five conventional banks. Written in plain language for management and the credit team.</p></div>')

# 1. one page
h.append('<h2>1. The answer in one page</h2><ul>')
for k in KEY_MESSAGES:
    h.append('<li>{}</li>'.format(md_bold_to_html(k)))
h.append('</ul>')
rrows = [(r, TOT[r], d.RATING_TEXT[r]) for r in d.RATINGS]
h.append('<div class="piebox">' + donut_svg(rrows, CAT, str(NITEMS), "policy items", "Ratings of 60 policy items") +
         '<div><h4>How the {} policy items compare with the finance-company market</h4>'.format(NITEMS) + pie_legend(rrows, CAT, pct=True) +
         '<p class="what"><b>What this shows:</b> {} of {} items sit inside the finance-company range and {} are better for customers. Only {} are deliberately tighter, and none is looser than the CBUAE or the FCR.</p>'.format(TOT[d.N], NITEMS, TOT[d.E], TOT[d.T]) + '</div></div>')
h.append('<div class="headline">Bank-grade selection, finance-company reach, a price below the finance-company typical, and nothing looser than the CBUAE or the Finance Companies Regulation.</div>')

# 2. market
h.append('<h2 class="pb">2. The finance-company market in pictures</h2>')
h.append('<div class="tiles">'
         '<div class="tile"><b>20</b><span>licensed finance companies; only 9 actively lend to individuals</span></div>'
         '<div class="tile"><b>AED 11.2bn</b><span>all finance-company loans (−8.8% in 2025); banks lend AED 645.8bn to individuals, about ' + '{:.0f}'.format(645.8 / 11.2) + ' times more</span></div>'
         '<div class="tile"><b>7.1%</b><span>finance-company net NPL, against 1.6% for banks</span></div>'
         '<div class="tile"><b>AED 250m</b><span>our pilot loan cap: about 2% of the sector</span></div></div>')
st_rows = [(a, b, c) for a, b, c in d.FC_STATUS]
h.append('<div class="piebox">' + donut_svg(st_rows, CAT, "20", "finance companies", "20 finance companies by status") +
         '<div><h4>The 20 licensed finance companies by status</h4>' + pie_legend(st_rows, CAT, pct=False) +
         '<p class="what"><b>What this shows:</b> only 9 of the 20 licensed finance companies actively lend to individuals. Several legacy (mostly Islamic) companies are winding down; new entrants are digital. Source: CB Register, Aug 2026; status from our research. Counts of companies, not market shares.</p></div></div>')
mix_rows = [(a, b) for a, b in d.FC_LOAN_MIX]
h.append('<div class="piebox">' + donut_svg(mix_rows, CAT, "14%", "retail (personal + vehicle)", "Finance-company loans by type") +
         '<div><h4>What finance companies lend: loans by type</h4>' + pie_legend(mix_rows, CAT, unit="%", pct=False) +
         '<p class="what"><b>What this shows:</b> personal and vehicle loans are only about 14% of finance-company lending. The retail space is small and run by a handful of active lenders, so a disciplined new entrant can win share. Source: FSR 2025, shares of about AED 11.2bn.</p></div></div>')
h.append('<h3>The active retail finance companies</h3>')
h.append('<table><thead><tr><th>Company</th><th>Type</th><th>What they offer individuals</th><th>Price signal</th></tr></thead><tbody>')
for r in [
    ("Finance House", "Conventional", "Personal loans (Easy, Sulfah, Payday), cards, gold loans", "PL from 20%; Sulfah 24–28%; Payday 36%; gold 16%"),
    ("Deem Finance", "Conventional", "Cards, personal loans, salary advance", "PL 15.99–39.99%; cards 3.75–3.99% a month"),
    ("Al Ain Finance", "Conventional", "Purpose loans, cards", "PL 14–24% priced by AECB; cards 2.9% a month"),
    ("botim / CashNow", "Conventional, digital", "Small loans AED 300–30,000", "APR from 16% (Professional) and from 54% (Standard)"),
    ("e& easyCredit", "Conventional, digital", "AED 100–1,500 for 30 days", "Fee 8% + VAT"),
    ("Aafaq", "Islamic", "Personal, auto, cards", "From 8% flat (~14–15%); auto from 2.5% flat"),
    ("Mawarid, Siraj", "Islamic", "Personal, auto, cards; Siraj home", "Siraj ≥ 15% flat"),
    ("Tamara (BNPL)", "Restricted licence", "BNPL up to AED 20,000", "0–1% fee; no late fees"),
]:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')

# 3. where we stand
h.append('<h2>3. Where our policy stands on key numbers</h2>')
h.append('<p>Each chart has its own colour key. Our policy is always blue. Bars run from the lowest to the highest published value; a single dot means only one value is published.</p>')
h.append('<div class="chartbox"><h4>Personal-loan interest rate, % a year (reducing balance)</h4>' + group_legend(("us", "fc", "digital", "bank")) +
         range_svg(d.PL_RATES, 45, 5, "%", "Personal-loan interest rate ranges") +
         '<p class="what"><b>What this shows:</b> our 12.99% starting rate is below every finance company and digital lender, and our top rate (29.99%) is below the market highs of 36–40%. Banks are cheaper, but only for customers who move their salary.</p></div>')
h.append('<div class="chartbox"><h4>Minimum monthly salary for a personal loan, AED</h4>' + group_legend(("us", "fc", "digital", "bank")) +
         hbar_svg(d.PL_MIN_SALARY, 12000, 2000, fmt_aed, "Minimum salary for a personal loan") +
         '<p class="what"><b>What this shows:</b> we start at AED 5,000, the same as most finance companies and the bank median. Weaker profiles without employer assignment need AED 7,000. Customers below AED 5,000 get a salary advance, not a loan.</p></div>')
h.append('<div class="chartbox"><h4>Maximum personal loan, AED</h4>' + group_legend(("us", "fc", "digital", "bank")) +
         hbar_svg(d.PL_MAX_AMOUNT, 500000, 100000, fmt_aedk, "Maximum personal loan") +
         '<p class="what"><b>What this shows:</b> our caps (AED 150,000–300,000) are mid-market for a finance company. Banks lend up to AED 2m–4m with a salary transfer. Lower caps keep single-customer risk small against AED 150m of capital.</p></div>')
h.append('<div class="chartbox"><h4>Credit-card interest, % a month</h4>' + group_legend(("us", "fc", "bank")) +
         range_svg(d.CARD_RATES, 4.5, 0.5, "%", "Credit-card interest ranges") +
         '<p class="what"><b>What this shows:</b> our 3.59% standard rate (3.25% premium) is below Finance House, Deem and Aafaq and inside the bank range. Al Ain Finance and Mawarid are cheaper.</p></div>')
h.append('<div class="keep"><h3>Gold-backed loans</h3><table><thead><tr><th></th><th>Our policy</th><th>Finance House</th><th>Top-5 banks</th></tr></thead><tbody>'
         '<tr><td><b>Loan-to-value</b></td><td>70% (top-up call 80%, sale 85%)</td><td>75%</td><td>not offered</td></tr>'
         '<tr><td><b>Rate</b></td><td>14.99%</td><td>16%</td><td>–</td></tr>'
         '<tr><td><b>Size</b></td><td>AED 5,000–250,000</td><td>AED 5,000–500,000</td><td>–</td></tr></tbody></table></div>')

# 4. stand out
h.append('<h2>4. How we stand out among finance companies</h2><div class="std">')
for i, (h_, t_) in enumerate(STANDOUT, 1):
    h.append('<div><h4>{}. {}</h4><p>{}</p></div>'.format(i, E(h_), E(t_)))
h.append('</div>')

# 5. scenarios
h.append('<h2>5. Real-life scenarios</h2><p>Numbers are computed with the policy rules (reducing-balance instalments unless flat). Names are illustrative.</p>')
h.append('<table><thead><tr><th>Customer</th><th>Product</th><th>Outcome</th><th>Key number</th></tr></thead><tbody>')
for nm, pr, oc, kn in sc.SUMMARY:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td class="{}">{}</td><td>{}</td></tr>'.format(E(nm), E(pr), 'ok' if oc == 'Approved' else 'no', E(oc), E(kn)))
h.append('</tbody></table>')
for i, s in enumerate(SCENARIOS, 1):
    h.append('<div class="scen"><h3>Scenario {}: {}</h3><dl>'.format(i, E(s["title"])))
    for key, lab in (("who", "Customer"), ("ask", "Wants"), ("banks", "Banks"), ("market", "Finance companies"), ("ours", "Our policy")):
        h.append('<dt>{}</dt><dd>{}</dd>'.format(lab, md_bold_to_html(s[key])))
    h.append('<dt>Result</dt><dd class="res">{}</dd></dl>'.format(md_bold_to_html(s["result"])))
    h.append('<table class="maths"><thead><tr><th style="width:27%">The maths</th><th>Working</th><th style="width:22%;text-align:right">Result</th></tr></thead><tbody>')
    for st, wk, rs in s["maths"]:
        h.append('<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(E(st), E(wk), E(rs)))
    h.append('</tbody></table></div>')
    if i == 1:
        rows = [("Our policy, 17.99%", "us", M_INT, ""), ("Finance House from 20%", "fc", M_20_INT, ""),
                ("Typical finance company, 24%", "fc", M_24_INT, ""), ("Deem top rate, 39.99%", "fc", M_40_INT, "")]
        h.append('<div class="chartbox"><h4>Mariam: total interest on AED 60,000 over 48 months, AED</h4>' +
                 group_legend(("us", "fc")) + hbar_svg(rows, 70000, 10000, fmt_aed, "Total interest comparison for Mariam", label_w=200) +
                 '<p class="what"><b>What this shows:</b> the same loan costs Mariam {} in interest with us, against {} at a typical finance company and {} at the top of the market.</p></div>'.format(aed(M_INT), aed(M_24_INT), aed(M_40_INT)))
    if i == 3:
        rows = [("Keep the 28% loan", "fc", K_OLD_TOT, ""), ("Our buyout, 13.99%", "us", K_NEW_TOT, ""),
                ("Bank, 5.49% (salary moved)", "bank", K_BANK_TOT, "")]
        h.append('<div class="chartbox"><h4>Khalid: total still to pay over 36 months, AED</h4>' +
                 group_legend(("us", "fc", "bank")) + hbar_svg(rows, 200000, 50000, fmt_aedk, "Total repayments for Khalid", label_w=200) +
                 '<p class="what"><b>What this shows:</b> our buyout cuts what Khalid still has to pay by {}. A bank is cheaper still, but only if he moves his salary, and our cost comparison tells him so.</p></div>'.format(aed(K_OLD_TOT - K_NEW_TOT)))

# 6. gaps
h.append('<h2>6. Gaps and improvements</h2>')
h.append('<h3>6.1 Tighter than the market: keep or loosen?</h3>')
h.append('<table><thead><tr><th style="width:6%">ID</th><th style="width:18%">Item</th><th style="width:24%">What the market does</th><th style="width:30%">Recommendation</th><th>Trade-off</th></tr></thead><tbody>')
for r in TIGHTER:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
h.append('<div class="keep"><h3>6.2 No finance-company peer: approvals needed</h3>')
h.append('<table><thead><tr><th style="width:6%">ID</th><th style="width:32%">Item</th><th style="width:28%">Market</th><th>Approval needed</th></tr></thead><tbody>')
for r in NOPEER:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table></div>')
h.append('<div class="keep"><h3>6.3 Deliberate gaps</h3><ul>'
         '<li><b>Customers earning AED 3,000–4,999:</b> salary advance only, no personal loan. Payday-style loans at 36% (Finance House) serve this segment; revisit after 12 months of pilot data.</li>'
         '<li><b>Home finance and deposit-backed loans:</b> not in the pilot (licence and FCR).</li>'
         '<li><b>Price against banks:</b> a customer who will move their salary gets a cheaper loan at a bank. The policy targets customers who will not or cannot.</li></ul></div>')
h.append('<div class="keep"><h3>6.4 Regulatory points for Legal &amp; Compliance to confirm</h3><ol>')
for r in REG_CONFIRM:
    h.append('<li>{}</li>'.format(E(r)))
h.append('</ol></div>')
h.append('<div class="keep"><h3>6.5 Launch checklist</h3><ul class="chk">')
for r in LAUNCH:
    h.append('<li>{}</li>'.format(E(r)))
h.append('</ul></div>')

# 7. item by item
h.append('<h2>7. Item-by-item comparison</h2>')
h.append('<table class="heat"><thead><tr><th>Product area</th>' + "".join('<th style="text-align:center">{}</th>'.format(E(r)) for r in d.RATINGS) + '</tr></thead><tbody>')
for g in d.GROUPS:
    c = Counter(it[6] for it in d.ITEMS if it[0] == g)
    h.append('<tr><td><b>{}</b></td>'.format(E(d.GROUP_SHORT[g])) + "".join(
        '<td class="c" style="{}">{}</td>'.format("background:{} !important".format(TINT[r]) if c[r] else "color:#9AA6BA", c[r]) for r in d.RATINGS) + '</tr>')
h.append('<tr><td><b>Total</b></td>' + "".join('<td class="c" style="background:{} !important">{}</td>'.format(TINT[r], TOT[r]) for r in d.RATINGS) + '</tr></tbody></table>')
h.append('<p class="tags">Tags: [B] bank criterion carried over &middot; [C] CBUAE consumer rule &middot; [R] Finance Companies Regulation &middot; [A] adjusted for the finance-company market or rules (sign-off) &middot; [P] proposal (sign-off).</p>')
for g in d.GROUPS:
    h.append('<h3>{}</h3>'.format(E(g)))
    h.append('<table class="cmp"><thead><tr><th style="width:6%">ID</th><th style="width:14%">Item</th><th style="width:31%">Policy</th><th style="width:24%">Finance companies</th><th style="width:13%">Top-5 banks</th><th style="width:12%">Rating</th></tr></thead><tbody>')
    for it in d.ITEMS:
        if it[0] == g:
            tags = " ".join("[{}]".format(t) for t in it[7].split("/"))
            h.append('<tr><td>{}</td><td>{}</td><td>{} <span class="small">{}</span></td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                it[1], E(it[2]), E(it[3]), tags, E(it[4]), E(it[5]), chip(it[6])))
    h.append('</tbody></table>')

# 8. sources
h.append('<h3>Sign-off list: {} items ({} [A] adjusted, {} [P] proposals)</h3>'.format(len(SIGNOFF), N_A, N_P))
h.append('<table class="cmp"><thead><tr><th style="width:6%">ID</th><th style="width:18%">Item</th><th style="width:7%">Tag</th><th>Policy value</th><th style="width:12%">Rating</th></tr></thead><tbody>')
for it in SIGNOFF:
    h.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(it[1], E(it[2]), ' '.join('[{}]'.format(t) for t in it[7].split('/')), E(it[3]), chip(it[6])))
h.append('</tbody></table><p class="small">The policy text also marks two rules [P]: repricing when a salary account is moved without clearance (&sect;8.1) and the sector watch-list (&sect;7.5).</p>')
h.append('<div class="keep"><h2>8. Data notes and confidence</h2><ul>' + ''.join('<li>{}</li>'.format(md_bold_to_html(t_)) for t_ in DATA_NOTES) + '</ul></div>')
h.append('<h2>9. Sources</h2><p class="small">Confidence: H = read directly (KFS, report, register); M = search extract (the FCR rulebook returned HTTP 403). All checked 9 November 2026.</p>')
h.append('<table><thead><tr><th style="width:14%">Group</th><th style="width:32%">Source</th><th>Link</th><th style="width:7%">Conf.</th></tr></thead><tbody>')
for s in SOURCES:
    h.append('<tr><td>{}</td><td>{}</td><td class="url">{}</td><td>{}</td></tr>'.format(*[E(x) for x in s]))
h.append('</tbody></table></body></html>')

html_path = WORK / "gap_fc.html"
html_path.write_text("".join(h), encoding="utf-8")
pdf_path = OUT / PDF_NAME
subprocess.run([CHROME, "--headless=new", "--user-data-dir={}".format(WORK / "chrome-profile-fc-gap"), "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=10000", "--print-to-pdf={}".format(pdf_path), html_path.as_uri()], capture_output=True, timeout=240)
print("ratings", dict(TOT), "| sign-off", len(signoff), "| pdf", pdf_path.exists())
