"""Build 'Where Our Credit Policy Stands - UAE Bank Market' (HTML -> PDF) and the MD twin."""
import json, math, statistics, subprocess, sys, pathlib, html, copy

S = pathlib.Path(__file__).parent
MP = pathlib.Path(r"C:/Users/mac/OneDrive/Desktop/Risk banking model/credit-policy-uae-conventional/market-position")
PDF = MP / "Where Our Credit Policy Stands - UAE Bank Market.pdf"
MD = MP / "market-position-report.md"
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"

d = json.load(open(S / "data.json", encoding="utf-8"))
BANKS = d["banks"]; MEASURES = d["measures"]
TEAL = "#0f7b7b"; GRAYBAR = "#c3c9d0"; BLUE = "#2a78d6"; ORANGE = "#eb6834"; AQUA = "#1baf7a"; YELLOW = "#eda100"; MAGENTA = "#e87ba4"
INK = "#16202a"; INK2 = "#46505c"; MUTED = "#6b7480"; LINE = "#dfe3e8"
PRICE = {"pl_rate_min", "card_rate_month", "home_fixed_rate", "auto_rate_flat"}

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None
def esc(s): return html.escape(str(s))
def aed(v):
    if v >= 1e6: return f"{v/1e6:.2f}".rstrip("0").rstrip(".") + "m"
    if v >= 1e5: return f"{v/1e3:.0f}k"
    return f"{v:,.0f}"
def pc(v): return f"{v:.2f}".rstrip("0").rstrip(".") + "%"
def fmt(v, unit): return ("AED " + aed(v)) if unit == "AED" else pc(v)
def fmt_short(v, unit): return aed(v) if unit == "AED" else pc(v)

SHORTLBL = {
 "pl_min_salary_stl": "Minimum salary (salary transferred)", "pl_min_salary_nonstl": "Minimum salary (no salary transfer)",
 "pl_max_nat_aed": "Maximum loan, UAE nationals", "pl_max_exp_aed": "Maximum loan, expats", "pl_rate_min": "Lowest interest rate",
 "card_min_salary": "Minimum salary", "card_rate_month": "Monthly interest rate",
 "home_min_salary_nat": "Minimum salary, UAE nationals", "home_min_salary_exp": "Minimum salary, expats",
 "home_ltv_nat": "Max loan-to-value, nationals", "home_ltv_exp": "Max loan-to-value, expats", "home_fixed_rate": "Fixed interest rate",
 "auto_min_salary": "Minimum salary", "auto_max_aed": "Maximum loan", "auto_rate_flat": "Flat interest rate (new car)",
 "deposit_advance_pct": "Advance as % of the deposit"}
GROUPS = [("Personal loans", "pl_"), ("Credit cards", "card_"), ("Home loans", "home_"), ("Car loans", "auto_"), ("Loans against deposits", "deposit_")]
def group_of(k): return next(g for g, p in GROUPS if k.startswith(p))
for m in MEASURES:
    if m["friendlier"] == 0: m["verdict"] = "Joint best"
MBY = {m["key"]: m for m in MEASURES}

# ---------------- scoring (re-usable for what-ifs) ----------------
def score(banks, overrides=None):
    banks = copy.deepcopy(banks)
    pol = next(b for b in banks if b["segment"] == "Policy")
    for k, v in (overrides or {}).items(): pol[k] = v
    for b in banks: b["pct"] = {}
    for m in MEASURES:
        k = m["key"]; ents = [num(b[k]) for b in banks if num(b[k]) is not None]; n = len(ents)
        for b in banks:
            v = num(b[k])
            if v is None: continue
            worse = sum(1 for x in ents if (x > v if m["better"] == "low" else x < v))
            ties = sum(1 for x in ents if x == v) - 1
            b["pct"][k] = 100 * (worse + 0.5 * ties) / (n - 1)
    lg = []
    for b in banks:
        acc = [v for k, v in b["pct"].items() if k not in PRICE]; pr = [v for k, v in b["pct"].items() if k in PRICE]
        if len(acc) >= 5 and len(pr) >= 2:
            a, p = statistics.mean(acc), statistics.mean(pr)
            lg.append(dict(short=b["short"], segment=b["segment"], type=b["type"], access=a, price=p, overall=(a + p) / 2))
    for key in ("overall", "access", "price"):
        for i, r in enumerate(sorted(lg, key=lambda r: -r[key]), 1): r[key + "_rank"] = i
    lg.sort(key=lambda r: r["overall_rank"])
    return lg, banks

LEAGUE, SB = score(BANKS)
N_LEAGUE = len(LEAGUE)
OURS = next(r for r in LEAGUE if r["segment"] == "Policy")
conv = sorted([r for r in LEAGUE if "islamic" not in r["type"]], key=lambda r: -r["access"])
CONV_ACCESS_RANK = next(i for i, r in enumerate(conv, 1) if r["segment"] == "Policy"); N_CONV = len(conv)
assert CONV_ACCESS_RANK == 1, CONV_ACCESS_RANK
AHEAD_ON_ACCESS = [r for r in LEAGUE if r["access"] > next(x for x in LEAGUE if x["segment"] == "Policy")["access"]]
assert all("islamic" in r["type"] for r in AHEAD_ON_ACCESS), AHEAD_ON_ACCESS
OTHERS = [b for b in BANKS if b["segment"] != "Policy"]
N_BANKS = len(OTHERS)
N_NAT = sum(1 for b in OTHERS if b["segment"] != "Foreign"); N_FOR = N_BANKS - N_NAT
from collections import Counter
VERD = Counter(m["verdict"] for m in MEASURES)
JOINT = [m for m in MEASURES if m["joint_best"]]

# what-ifs (levers)
LEVERS = []
for label, ov in [("Home-loan fixed rate 4.24% → 3.99% for salary-transfer customers", {"home_fixed_rate": "3.99"}),
                  ("Credit-card rate 3.59% → 3.49% a month", {"card_rate_month": "3.49"}),
                  ("Both changes together", {"home_fixed_rate": "3.99", "card_rate_month": "3.49"})]:
    lg, _ = score(BANKS, ov); o = next(r for r in lg if r["segment"] == "Policy")
    LEVERS.append(dict(label=label, price=o["price"], overall=o["overall"], rank=o["overall_rank"], price_rank=o["price_rank"]))

# ---------------- SVG helpers ----------------
def bar_path(x, y, w, h, r=3):
    r = min(r, w, h / 2)
    if w <= r: return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,1):.1f}" height="{h}" />'
    return (f'M{x:.1f},{y:.1f} h{w-r:.1f} a{r},{r} 0 0 1 {r},{r} v{h-2*r:.1f} a{r},{r} 0 0 1 -{r},{r} h-{w-r:.1f} z')

def hbar(m, width=336):
    k, better, unit = m["key"], m["better"], m["unit"]
    ents = [(b["short"], num(b[k]), b["segment"] == "Policy") for b in BANKS if num(b[k]) is not None]
    ents.sort(key=lambda e: ((e[1] if better == "low" else -e[1]), 0 if e[2] else 1, e[0]))
    lw, vw = 112, 46; bw = width - lw - vw - 4; pitch, bh, top = 13, 9, 20
    vmax = max(v for _, v, _ in ents); sc = bw / vmax
    h = top + pitch * len(ents) + 4
    med = statistics.median([v for _, v, p in ents if not p]); mx = lw + med * sc
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" role="img" aria-label="{esc(m["measure"])}">']
    out.append(f'<line x1="{lw}" y1="{top-4}" x2="{lw}" y2="{h-2}" stroke="{LINE}" stroke-width="1"/>')
    vals = []
    for i, (name, v, pol) in enumerate(ents):
        y = top + i * pitch; w = v * sc
        fill = TEAL if pol else GRAYBAR
        out.append(f'<text x="{lw-6}" y="{y+bh-0.5}" text-anchor="end" font-size="{10 if pol else 9.5}" font-weight="{700 if pol else 400}" fill="{INK if pol else INK2}">{esc(name)}</text>')
        out.append(f'<path d="{bar_path(lw, y, w, bh)}" fill="{fill}"/>')
        vals.append(f'<text x="{lw+w+4:.1f}" y="{y+bh-0.5}" font-size="9" font-weight="{700 if pol else 400}" fill="{INK if pol else MUTED}" stroke="#fff" stroke-width="3" paint-order="stroke">{esc(fmt_short(v, unit))}</text>')
    out.append(f'<line x1="{mx:.1f}" y1="{top-6}" x2="{mx:.1f}" y2="{h-2}" stroke="{INK2}" stroke-width="1" stroke-dasharray="3 2"/>')
    anchor = "end" if mx > lw + bw * 0.6 else "start"; tx = mx - 3 if anchor == "end" else mx + 3
    out.append(f'<text x="{tx:.1f}" y="{top-9}" text-anchor="{anchor}" font-size="9" fill="{INK2}">Market median {esc(fmt_short(med, unit))}</text>')
    out.extend(vals); out.append("</svg>")
    return "".join(out)

def donut(slices, size=148, center_big="", center_small=""):
    cx = cy = size / 2; R = size / 2 - 2; r = R * 0.6
    tot = sum(v for _, v, _ in slices); a0 = -math.pi / 2
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img">']
    for lab, v, col in slices:
        a1 = a0 + 2 * math.pi * v / tot; large = 1 if a1 - a0 > math.pi else 0
        p = (f'M{cx+R*math.cos(a0):.2f},{cy+R*math.sin(a0):.2f} A{R},{R} 0 {large} 1 {cx+R*math.cos(a1):.2f},{cy+R*math.sin(a1):.2f} '
             f'L{cx+r*math.cos(a1):.2f},{cy+r*math.sin(a1):.2f} A{r},{r} 0 {large} 0 {cx+r*math.cos(a0):.2f},{cy+r*math.sin(a0):.2f} Z')
        out.append(f'<path d="{p}" fill="{col}" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'); a0 = a1
    out.append(f'<text x="{cx}" y="{cy+2}" text-anchor="middle" font-size="19" font-weight="700" fill="{INK}">{esc(center_big)}</text>')
    out.append(f'<text x="{cx}" y="{cy+17}" text-anchor="middle" font-size="9" fill="{MUTED}">{esc(center_small)}</text></svg>')
    return "".join(out)

def pie_block(title, sub, slices, center_big, center_small, unit="", mark=None, note=""):
    tot = sum(v for _, v, _ in slices)
    rows = []
    for lab, v, col in slices:
        val = (f"{v:,.1f}" if isinstance(v, float) else f"{v}") + unit
        tag = ' <span class="us-tag">our policy</span>' if mark == lab else ""
        rows.append(f'<li><span class="sw" style="background:{col}"></span><span class="lg-l">{esc(lab)}{tag}</span>'
                    f'<span class="lg-v">{esc(val)}</span><span class="lg-p">{100*v/tot:.0f}%</span></li>')
    return (f'<div class="pie card"><h4>{esc(title)}</h4><p class="sub">{esc(sub)}</p><div class="pie-row">'
            f'{donut(slices, center_big=center_big, center_small=center_small)}<ul class="legend">{"".join(rows)}</ul></div>'
            + (f'<p class="note">{note}</p>' if note else "") + '</div>')

def strip():
    lw, bw, vw = 214, 300, 150; width = lw + bw + vw; pitch = 24; bh = 15
    rows = []; y = 30
    out_rows = []
    for g, p in GROUPS:
        ms = [m for m in MEASURES if m["key"].startswith(p)]
        out_rows.append(f'<text x="0" y="{y+11}" font-size="10.5" font-weight="700" fill="{INK}">{esc(g)}</text>'); y += 18
        for m in ms:
            n = m["n"]; f, s, w = m["friendlier"], m["same"], m["less_friendly"]
            out_rows.append(f'<text x="10" y="{y+bh-3}" font-size="10" fill="{INK2}">{esc(SHORTLBL[m["key"]])}</text>')
            x = lw
            for cnt, col, tcol in ((f, ORANGE, "#fff"), (s, "#d5dae0", INK), (w, BLUE, "#fff")):
                if cnt == 0: continue
                ww = bw * cnt / n
                out_rows.append(f'<rect x="{x:.1f}" y="{y}" width="{max(ww-2,1):.1f}" height="{bh}" rx="2" fill="{col}"/>')
                if ww >= 16:
                    out_rows.append(f'<text x="{x+ww/2-1:.1f}" y="{y+bh-4}" text-anchor="middle" font-size="9.5" font-weight="700" fill="{tcol}">{cnt}</text>')
                x += ww
            v = m["verdict"]; vc = {"Joint best": BLUE, "Ahead of most": BLUE, "Market middle": "#8a939d", "Behind most": ORANGE}[v]
            badge = f" · shared with {s}" if m["joint_best"] else ""
            out_rows.append(f'<circle cx="{lw+bw+12}" cy="{y+bh/2}" r="4" fill="{vc}"/>'
                            f'<text x="{lw+bw+20}" y="{y+bh-3}" font-size="10" font-weight="600" fill="{INK}">{esc(v)}<tspan font-weight="400" fill="{MUTED}">{badge}</tspan></text>')
            y += pitch
        y += 4
    h = y + 4
    head = (f'<text x="{lw}" y="12" font-size="9.5" fill="{INK2}">Each bar = all banks with published terms, split three ways</text>'
            f'<text x="{lw+bw+12}" y="12" font-size="9.5" fill="{INK2}">Where we sit</text>')
    return f'<svg viewBox="0 0 {width} {h}" width="100%" role="img" aria-label="Position strip">{head}{"".join(out_rows)}</svg>'

def scatter(width=680, height=372):
    ml, mr, mt, mb = 48, 14, 14, 40; pw, ph = width - ml - mr, height - mt - mb
    X = lambda a: ml + pw * a / 100; Y = lambda p: mt + ph * (1 - p / 100)
    out = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="Access versus price map">']
    out.append(f'<rect x="{X(50)}" y="{Y(100)}" width="{pw/2}" height="{ph/2}" fill="#eef6f6"/>')
    for t in (0, 25, 50, 75, 100):
        out.append(f'<line x1="{X(t)}" y1="{mt}" x2="{X(t)}" y2="{mt+ph}" stroke="{LINE}" stroke-width="{1.2 if t==50 else 0.8}" {"stroke-dasharray=\"4 3\"" if t==50 else ""}/>')
        out.append(f'<line x1="{ml}" y1="{Y(t)}" x2="{ml+pw}" y2="{Y(t)}" stroke="{LINE}" stroke-width="{1.2 if t==50 else 0.8}" {"stroke-dasharray=\"4 3\"" if t==50 else ""}/>')
        out.append(f'<text x="{X(t)}" y="{mt+ph+13}" text-anchor="middle" font-size="9" fill="{MUTED}">{t}</text>')
        out.append(f'<text x="{ml-6}" y="{Y(t)+3}" text-anchor="end" font-size="9" fill="{MUTED}">{t}</text>')
    out.append(f'<text x="{ml+pw/2}" y="{height-6}" text-anchor="middle" font-size="10" fill="{INK2}">Ease of getting a loan (access score, 0–100) →</text>')
    out.append(f'<text transform="translate(12,{mt+ph/2}) rotate(-90)" text-anchor="middle" font-size="10" fill="{INK2}">Low prices (price score, 0–100) →</text>')
    for tx, ty, anc, lab in ((X(98), Y(97), "end", "Easy to get · cheaper"), (X(2), Y(97), "start", "Harder to get · cheaper"),
                             (X(98), Y(3), "end", "Easy to get · dearer"), (X(2), Y(3), "start", "Harder to get · dearer")):
        out.append(f'<text x="{tx}" y="{ty}" text-anchor="{anc}" font-size="9.5" font-weight="600" fill="#9aa2ab">{lab}</text>')
    pts = sorted(LEAGUE, key=lambda r: (r["segment"] != "Policy", r["segment"] != "Top-5"))
    boxes = []
    for r in pts:
        x, y = X(r["access"]), Y(r["price"]); rad = 8 if r["segment"] == "Policy" else 5
        boxes.append((x - rad, y - rad, x + rad, y + rad))
    labels = []
    def free(b):
        if b[0] < ml or b[2] > ml + pw or b[1] < mt or b[3] > mt + ph: return False
        return all(b[2] < o[0] or b[0] > o[2] or b[3] < o[1] or b[1] > o[3] for o in boxes)
    for r in pts:
        pol = r["segment"] == "Policy"; x, y = X(r["access"]), Y(r["price"]); rad = 8 if pol else 5
        fs = 11 if pol else 9; tw = len(r["short"]) * fs * 0.55 + 2
        for dx, dy, anc in ((rad + 3, 3, "start"), (-rad - 3, 3, "end"), (0, -rad - 4, "middle"), (0, rad + 11, "middle"),
                            (rad + 2, -rad - 1, "start"), (rad + 2, rad + 8, "start"), (-rad - 2, -rad - 1, "end"), (-rad - 2, rad + 8, "end")):
            tx, ty = x + dx, y + dy
            x0 = tx if anc == "start" else (tx - tw if anc == "end" else tx - tw / 2)
            b = (x0, ty - fs + 2, x0 + tw, ty + 2)
            if free(b):
                boxes.append(b); labels.append((tx, ty, anc, r, fs)); break
    for r in pts[::-1]:
        x, y = X(r["access"]), Y(r["price"])
        if r["segment"] == "Policy": out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{TEAL}" stroke="#fff" stroke-width="2"/>')
        elif r["segment"] == "Top-5": out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#4b5563" stroke="#fff" stroke-width="2"/>')
        else: out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#aab2bb" stroke="#fff" stroke-width="2"/>')
    for tx, ty, anc, r, fs in labels:
        pol = r["segment"] == "Policy"
        out.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anc}" font-size="{fs}" font-weight="{700 if pol else 400}" fill="{INK if pol or r["segment"]=="Top-5" else INK2}">{esc(r["short"])}</text>')
    out.append("</svg>")
    unl = [r["short"] for r in LEAGUE if not any(l[3] is r for l in labels)]
    return "".join(out), unl

def mini_bars(items, vmax, limit=None, limit_label="", width=318):
    lw = 150; bw = width - lw - 54; pitch = 20; bh = 12; top = 16 if limit else 4
    h = top + pitch * len(items) + 2
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" role="img">']; vals = []
    for i, (lab, v, ours) in enumerate(items):
        y = top + i * pitch; w = bw * v / vmax
        out.append(f'<text x="{lw-6}" y="{y+bh-2}" text-anchor="end" font-size="9.5" font-weight="{700 if ours else 400}" fill="{INK if ours else INK2}">{esc(lab)}</text>')
        out.append(f'<path d="{bar_path(lw, y, w, bh)}" fill="{TEAL if ours else GRAYBAR}"/>')
        vals.append(f'<text x="{lw+w+4:.1f}" y="{y+bh-2}" font-size="9.5" font-weight="{700 if ours else 400}" fill="{INK}" stroke="#fff" stroke-width="3" paint-order="stroke">{v:,.0f}</text>')
    if limit:
        lx = lw + bw * limit / vmax
        out.append(f'<line x1="{lx:.1f}" y1="{top-6}" x2="{lx:.1f}" y2="{h}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="3 2"/>')
        anc = "end" if lx > lw + bw * 0.55 else "start"
        out.append(f'<text x="{lx + (-3 if anc=="end" else 3):.1f}" y="{top-7}" text-anchor="{anc}" font-size="9" fill="{INK2}">{esc(limit_label)}</text>')
    out.extend(vals)
    out.append("</svg>")
    return "".join(out)

def hbar_simple(items, unit_suffix="", width=680, color=BLUE):
    lw, vw = 150, 205; bw = width - lw - vw; pitch, bh = 19, 12
    vmax = max(v for _, v, _ in items); h = pitch * len(items) + 4
    out = [f'<svg viewBox="0 0 {width} {h}" width="100%" role="img">']
    for i, (lab, v, note) in enumerate(items):
        y = 2 + i * pitch; w = bw * v / vmax
        out.append(f'<text x="{lw-6}" y="{y+bh-2}" text-anchor="end" font-size="10" fill="{INK2}">{esc(lab)}</text>')
        out.append(f'<path d="{bar_path(lw, y, max(w,1.5), bh)}" fill="{color}"/>')
        out.append(f'<text x="{lw+w+5:.1f}" y="{y+bh-2}" font-size="9.5" fill="{INK}">{v:,.1f}{unit_suffix}<tspan fill="{MUTED}">{("  " + note) if note else ""}</tspan></text>')
    out.append("</svg>")
    return "".join(out)

# ---------------- content ----------------
S1 = (f"Our credit policy is one of the easiest in the UAE to qualify for. It is <b>easier than all {N_CONV-1} conventional banks</b> with enough published data, and "
      f"<b>{OURS['access_rank']}th of {N_LEAGUE} banks</b> on ease of access, behind only {len(AHEAD_ON_ACCESS)} Islamic banks. Its prices sit in the <b>middle of the market</b>, as intended. "
      f"Overall it ranks <b>{OURS['overall_rank']}th of {N_LEAGUE}</b>, in the upper half of the market.")

mby = MBY
nonstl = mby["pl_min_salary_nonstl"]
tiles = [
    (f"{N_BANKS}", "UAE banks compared", f"Every bank that publishes retail lending terms: {N_NAT} national (incl. digital), {N_FOR} foreign."),
    ("#1", "for ease of access among conventional banks", f"Ahead of all {N_CONV-1} conventional banks with enough data; #{OURS['access_rank']} of {N_LEAGUE} counting Islamic banks."),
    ("AED 5,000", "entry salary without salary transfer", f"Joint lowest of {nonstl['n']} banks that publish one (with Mashreq and RAKBANK). Most big banks ask AED 10,000."),
    (f"{OURS['price']:.0f} / 100", "price score: market middle", "Rates priced by risk grade, near the market median. Only one measure, the home-loan fixed rate, is dearer than most."),
]

def tiles_html():
    return '<div class="tiles">' + "".join(
        f'<div class="tile"><div class="t-big">{esc(a)}</div><div class="t-lbl">{esc(b)}</div><div class="t-sub">{esc(c)}</div></div>' for a, b, c in tiles) + '</div>'

SCATTER_SVG, UNLABELLED = scatter()

# market pies (CBUAE)
pies_market = [
    pie_block("62 licensed banks in the UAE", "CBUAE, June 2026", [("National banks", 24, BLUE), ("Foreign banks, full licence", 26, ORANGE), ("Foreign banks, wholesale only", 12, AQUA)], "62", "banks"),
    pie_block("Conventional or Islamic", "CBUAE, June 2026 (incl. wholesale)", [("Conventional", 52, BLUE), ("Islamic", 10, ORANGE)], "52 / 10", "conv. / Islamic"),
    pie_block("Who borrows: UAE domestic credit", "AED bn, CBUAE, August 2026", [("Companies", 984.9, BLUE), ("Individuals (retail)", 645.8, ORANGE), ("Government, GREs & other", 638.1, AQUA)], "2,269", "AED bn", note="Retail lending to individuals grew 19.3% in a year. Government, GREs &amp; other = total minus private sector (derived)."),
    pie_block("Which banks lend: domestic credit", "AED bn, CBUAE, August 2026", [("National conventional banks", 1573.0, BLUE), ("Islamic banks", 544.2, ORANGE), ("Foreign banks", 151.6, AQUA)], "2,269", "AED bn", note="National conventional = total minus Islamic and foreign (derived)."),
]
BOOKS = [("Emirates NBD (group)", 184.0, "incl. Emirates Islamic"), ("ADIB", 109.2, ""), ("FAB", 94.0, "incl. international"), ("DIB", 79.0, ""),
         ("ADCB", 75.0, ""), ("Emirates Islamic", 52.8, "segment assets; inside ENBD group"), ("Mashreq", 36.0, "segment assets"), ("CBD", 27.8, ""),
         ("RAKBANK", 23.1, ""), ("Standard Chartered", 9.8, ""), ("Citibank", 5.3, "retail being exited"), ("Mbank", 0.68, "")]

# where-we-sit pies
bands = Counter()
for b in OTHERS:
    v = num(b["pl_min_salary_stl"])
    if v is None: continue
    bands["AED 4,000 or less" if v <= 4000 else "AED 5,000" if v <= 5000 else "AED 6,000–8,000" if v <= 8000 else "AED 10,000–12,500" if v <= 12500 else "AED 15,000 or more"] += 1
band_order = ["AED 4,000 or less", "AED 5,000", "AED 6,000–8,000", "AED 10,000–12,500", "AED 15,000 or more"]
cols5 = [BLUE, ORANGE, AQUA, YELLOW, MAGENTA]
NB = sum(bands.values())
pie_bands = pie_block("Personal-loan entry salary (salary transferred)", f"{NB} banks that publish one", [(b, bands[b], c) for b, c in zip(band_order, cols5)],
                      str(NB), "banks", mark="AED 5,000", note=f"Our AED 5,000 sits with the {bands['AED 5,000']} banks at the market's most common level; {NB - bands['AED 5,000'] - bands['AED 4,000 or less']} banks ask for more.")
ns = Counter(b["nonstl_pl"] for b in OTHERS)
pie_ns = pie_block("Personal loan without salary transfer?", f"All {N_BANKS} banks", [("Yes", ns["Y"], BLUE), ("Only cards, car or home loans", ns["P"], ORANGE), ("No", ns["N"], AQUA), ("Not published", ns["?"], YELLOW)],
                   str(N_BANKS), "banks", mark="Yes", note="We offer it from AED 5,000, but only with AECB ≥ 600, a listed employer (A–C) and 6 months' service; otherwise AED 10,000.")

# product chart cards
NOTES = {"pl_min_salary_nonstl": "Ours: AED 5,000 only with AECB ≥ 600, employer A–C and 6 months' service; otherwise AED 10,000.",
         "pl_rate_min": "Our floor for expats is 5.99%. Some figures are converted from flat rates.",
         "home_ltv_nat": "85% is the Central Bank maximum for a first home up to AED 5m.",
         "home_ltv_exp": "80% is the Central Bank maximum for a first home up to AED 5m.",
         "home_fixed_rate": "Headline fixed rates; package or salary-transfer offers can be lower.",
         "card_min_salary": "AED 5,000 is the market floor; most banks use it.",
         "auto_rate_flat": "New-car headline rate; used cars cost more."}
def chart_card(m):
    better = "Lower = easier for customers" if (m["better"] == "low" and m["unit"] == "AED") else ("Lower = cheaper" if m["better"] == "low" else "Higher = more generous")
    res = f'We are at <b>{esc(fmt(m["policy"], m["unit"]))}</b>: {m["friendlier"]} banks {"easier" if m["key"] not in PRICE else "cheaper"}, {m["same"]} the same, {m["less_friendly"]} {"stricter" if m["key"] not in PRICE else "dearer"}.'
    vc = {"Joint best": "v-best", "Ahead of most": "v-ahead", "Market middle": "v-mid", "Behind most": "v-behind"}[m["verdict"]]
    return (f'<div class="chart card"><div class="ptag">{esc(group_of(m["key"]))}</div><div class="ch-head"><h4>{esc(SHORTLBL[m["key"]])}</h4><span class="verdict {vc}">{esc(m["verdict"])}</span></div>'
            f'<p class="sub">{better} · {m["n"]} banks</p><p class="res">{res}</p>{hbar(m)}'
            + (f'<p class="note">{esc(NOTES[m["key"]])}</p>' if m["key"] in NOTES else "") + '</div>')

def product_sections():
    intro = {"Personal loans": "The biggest retail product. Entry salary and loan size decide who can borrow; the rate decides what it costs.",
             "Credit cards": "Almost every bank starts cards at AED 5,000. Prices cluster around 3.5% a month.",
             "Home loans": "Loan-to-value limits are set by the Central Bank. Banks compete on entry salary and rate.",
             "Car loans": "Car loans are quoted as flat rates. Entry salary varies most between banks.",
             "Loans against deposits": "A fully secured product: the customer borrows against their own deposit."}
    out = []
    for g, p in GROUPS:
        ms = [m for m in MEASURES if m["key"].startswith(p)]
        out.extend(chart_card(m) for m in ms)
    return '<div class="grid2">' + "".join(out) + "</div>"

def league_html():
    rows = []
    for r in LEAGUE:
        pol = r["segment"] == "Policy"
        segl = {"Policy": "Draft policy", "Top-5": "Top 5", "Other national": "National", "Islamic": "Islamic", "Digital": "Digital", "Foreign": "Foreign"}[r["segment"]]
        rows.append(f'<tr class="{"us" if pol else ""}"><td class="rk">{r["overall_rank"]}</td><td>{esc(r["short"])}</td><td class="seg">{segl}</td>'
                    f'<td class="barcell"><div class="lbar" style="width:{r["overall"]:.0f}%;background:{TEAL if pol else GRAYBAR}"></div><span>{r["overall"]:.0f}</span></td>'
                    f'<td class="num">{r["access"]:.0f} <small>(#{r["access_rank"]})</small></td><td class="num">{r["price"]:.0f} <small>(#{r["price_rank"]})</small></td></tr>')
    return ('<table class="league"><thead><tr><th>#</th><th>Bank</th><th>Type</th><th>Overall score (0–100)</th><th>Access</th><th>Price</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table>")

def verdict_table():
    rows = []
    for g, p in GROUPS:
        for m in [m for m in MEASURES if m["key"].startswith(p)]:
            vc = {"Joint best": "v-best", "Ahead of most": "v-ahead", "Market middle": "v-mid", "Behind most": "v-behind"}[m["verdict"]]
            jb = f' <span class="jb">shared with {m["same"]}</span>' if m["joint_best"] else ""
            rows.append(f'<tr><td>{esc(g)}</td><td>{esc(SHORTLBL[m["key"]])}</td><td class="num"><b>{esc(fmt(m["policy"], m["unit"]))}</b></td>'
                        f'<td class="num">{esc(fmt(m["median"], m["unit"]))}</td><td class="num">{m["friendlier"]} / {m["same"]} / {m["less_friendly"]}</td>'
                        f'<td><span class="verdict {vc}">{esc(m["verdict"])}</span>{jb}</td></tr>')
    return ('<table class="vt"><thead><tr><th>Product</th><th>Measure</th><th>Our policy</th><th>Market median</th><th>Banks easier / same / stricter</th><th>Verdict</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table>")

STANDOUT = [
    ("We say “yes” where others say “no”, safely", ["<b>No salary transfer:</b> most top banks want AED 8,000–10,000. We accept <b>AED 5,000</b> with AECB ≥ 600, a listed employer and 6 months in the job.",
        "<b>Car loans:</b> most top banks want AED 7,000. We accept <b>AED 5,000</b>.",
        "<b>First home, UAE nationals:</b> Mashreq and RAKBANK want AED 15,000. We accept <b>AED 10,000</b>, after a stress test."]),
    ("Products the big conventional banks don’t offer", ["<b>Salary advance</b> before payday.", "<b>Finance secured by end-of-service benefits</b>, priced near the floor.",
        "<b>Lending against gold</b>, plus a clear published rule for card limits."]),
    ("Fair, transparent pricing", ["Rates near the market middle, <b>priced by risk grade</b>, so good customers pay less.", "<b>No processing fee</b> on buyouts.",
        "Home loans: <b>25% free prepayment</b> a year, lower valuation fee, processing capped at AED 50,000."]),
    ("Speed", ["The AI Risk Score Card decides in <b>about 3 seconds</b>.", "Buyouts paid to the other bank <b>within 30 days</b>.", "UAE nationals get up to <b>120 days</b> before the first instalment."]),
    ("Safety built in", ["<b>Credit-score floors</b> and automatic declines for serious arrears.", "Home loans <b>stress-tested</b> at a higher rate.",
        "<b>Nightly early warning</b> on every customer; rate +2% if salary stops; portfolio limits."]),
    ("Fair to everyone", ["<b>No nationality bans.</b>", "Employers are <b>grouped by risk, not excluded</b>.", "Every decision comes with clear reasons the customer can understand."]),
]
def standout_html():
    return '<div class="grid2 so">' + "".join(
        f'<div class="card socard"><div class="so-n">{i}</div><h4>{t}</h4><ul>' + "".join(f"<li>{b}</li>" for b in bs) + "</ul></div>"
        for i, (t, bs) in enumerate(STANDOUT, 1)) + "</div>"

def lever_html():
    rows = "".join(f'<tr><td>{esc(l["label"])}</td><td class="num">{l["price"]:.0f} <small>(#{l["price_rank"]})</small></td><td class="num">{l["overall"]:.0f}</td><td class="num"><b>#{l["rank"]}</b> of {N_LEAGUE}</td></tr>' for l in LEVERS)
    base = f'<tr class="us"><td>Policy as drafted today</td><td class="num">{OURS["price"]:.0f} <small>(#{OURS["price_rank"]})</small></td><td class="num">{OURS["overall"]:.0f}</td><td class="num"><b>#{OURS["overall_rank"]}</b> of {N_LEAGUE}</td></tr>'
    return ('<table class="vt lever"><thead><tr><th>Change (optional, for pricing committee)</th><th>Price score</th><th>Overall score</th><th>Overall rank</th></tr></thead><tbody>'
            + base + rows + "</tbody></table>")

def other_banks(rows):
    return '<table class="ob">' + "".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in rows) + "</table>"

SCEN = [
 ("1", "A nurse whose salary goes to another bank", "Anita, 29, expat nurse at a listed private hospital (category C). Salary AED 6,500, paid to another bank. AECB 655, 14 months in the job, one card with an AED 10,000 limit.",
  other_banks([("FAB (no salary transfer)", "Needs AED 10,000 → <b>no</b>"), ("Emirates NBD (no salary transfer)", "Needs AED 10,000 → <b>no</b>"),
               ("RAKBANK (no salary transfer)", "Yes: AECB ≥ 541; 10× salary at 12.99–22.49%"), ("Mashreq NEO", "Yes: up to AED 150,000 at 10.49–17.49%"),
               ("<b>Our policy</b>", "<b>Yes.</b> AECB 655 ≥ 600; listed employer; 14 months > 6")]),
  ["<b>Limit:</b> lower of 10× salary and the AED 200,000 cap = <b>AED 65,000</b>.", "<b>Room each month:</b> 50% of AED 6,500 = 3,250, minus AED 500 for the card = <b>AED 2,750</b>.",
   "<b>Instalment:</b> grade 4 (11.99%), 48 months ≈ <b>AED 1,711</b>, inside the room."],
  mini_bars([("Our instalment, 11.99%", 1711, True), ("At RAKBANK's lowest, 12.99%", 1743, False)], 3000, 2750, "Room under the 50% rule: 2,750")),
 ("2", "Moving a loan to us (buyout), UAE national", "Khalid, 34, UAE national, Abu Dhabi government (category A). Salary AED 32,000. Existing loan: AED 400,000 left at 8.49%, 36 months to go.",
  other_banks([("Other bank today", "8.49% on AED 400,000"), ("<b>Our policy</b>", "<b>5.49%</b> (grades 1–3), paid to the other bank within 30 days, <b>no processing fee</b>")]),
  ["Instalment falls from about <b>AED 12,625</b> to <b>AED 12,077</b>: <b>AED 549 a month</b>, about <b>AED 19,750</b> over 36 months.", "After the other bank's 1% early-settlement charge (AED 4,000): <b>net ≈ AED 15,750</b>.",
   "<b>Top-up:</b> +AED 100,000 → AED 500,000 (limit 20× = 640,000); over 48 months ≈ AED 11,626 = <b>36% of salary</b>, under 50%."],
  mini_bars([("Other bank, 8.49%", 12625, False), ("With us, 5.49%", 12077, True)], 13500)),
 ("3", "First car for a lower-paid worker", "Joseph, 31, expat supervisor at a logistics company. Salary AED 5,500, transferred to us. Wants a 4-year-old used car for AED 60,000.",
  other_banks([("Emirates NBD, FAB, Mashreq", "Need AED 7,000 → <b>no</b>"), ("ADCB, RAKBANK", "AED 5,000 → yes"), ("<b>Our policy</b>", "<b>Yes</b>, minimum AED 5,000")]),
  ["<b>Loan:</b> AED 12,000 down (20%), <b>AED 48,000</b> at 3.19% flat over 60 months.", "<b>Instalment:</b> interest AED 7,656 → about <b>AED 928 a month = 17% of salary</b>.",
   "<b>Car age:</b> 4 + 5 = 9 years at the end, inside the 10-year limit."],
  mini_bars([("Monthly salary", 5500, False), ("Our instalment", 928, True)], 6000, 2750, "50% limit: 2,750")),
 ("4", "First home for a young Emirati", "Mariam, 28, UAE national, semi-government employer (category A). Salary AED 12,000. First home in Sharjah, AED 900,000.",
  other_banks([("Mashreq, RAKBANK", "Need AED 15,000 → <b>no</b>"), ("Emirates NBD (10,000), ADCB (8,000)", "Yes"), ("<b>Our policy</b>", "<b>Yes</b>, AED 10,000 minimum for nationals")]),
  ["<b>Loan:</b> 85% of value = <b>AED 765,000</b> over 25 years.", "<b>At our 3-year fixed rate (4.24%):</b> about <b>AED 4,140 a month</b>.",
   "<b>Stress test</b> at 3M EIBOR 4.39% + 1.79% = 6.18%: about <b>AED 5,013 = 42%</b> of salary. She passes."],
  mini_bars([("Today, 4.24% fixed", 4140, True), ("Stress test, 6.18%", 5013, False)], 6600, 6000, "50% limit: 6,000")),
 ("5", "End-of-service benefits for a better rate", "Suresh, 45, expat engineer, listed large company (category B), 9 years' service. Basic AED 14,000, gross 22,000. Needs AED 100,000 for university fees.",
  other_banks([("Large UAE banks", "Take end-of-service benefits only as <b>extra</b> security; none lends against them"), ("<b>Our policy</b>", "<b>Yes</b>, with the employer's undertaking")]),
  ["<b>Benefit:</b> 21 days × 5 years + 30 days × 4 years = 225 days ≈ <b>AED 103,562</b>; 80% ≈ <b>AED 82,849</b> = 83% of the loan.",
   "<b>Rate:</b> <b>5.99%</b> instead of 9.99%.", "<b>Saving:</b> AED 2,348 a month instead of 2,536 ≈ <b>AED 9,000</b> over 48 months."],
  mini_bars([("Unsecured, 9.99%", 2536, False), ("Benefit-backed, 5.99%", 2348, True)], 2800)),
 ("6", "Help before payday", "Ramesh, 40, construction foreman. Net salary AED 5,200, transferred to us. Needs AED 2,500 for school fees 10 days before payday.",
  other_banks([("Five largest conventional banks", "No published salary advance"), ("DIB, ADIB (Islamic)", "Offer one"), ("<b>Our policy</b>", "<b>Yes</b>: up to 50% of net salary")]),
  ["<b>Maximum:</b> 50% of AED 5,200 = <b>AED 2,600</b>.", "<b>Approved:</b> AED 2,500 for a fixed fee of <b>AED 100</b>.", "<b>Repaid</b> automatically from the next salary."],
  mini_bars([("Maximum advance", 2600, False), ("Approved advance", 2500, True)], 3000)),
 ("7", "Borrowing against gold", "Fatima, 50, holds gold certificates for 200 g, worth about AED 90,000 at an illustrative AED 450 per gram.",
  other_banks([("Conventional UAE banks", "None offers it"), ("Emirates Islamic", "50%, Priority customers only"), ("<b>Our policy</b>", "<b>70%</b> of gold value")]),
  ["<b>Advance:</b> 70% ≈ <b>AED 63,000</b>.", "<b>Top-up call</b> if gold falls <b>12.5%</b> (value AED 78,750).", "<b>Sale after notice</b> if it falls <b>17.6%</b> (value about AED 74,160)."],
  mini_bars([("Gold value today", 90000, False), ("Top-up call level", 78750, False), ("Sale level", 74160, False), ("Our advance", 63000, True)], 100000)),
 ("8", "Where we say “no”, and why that is good", "Same profile as Anita, but AECB 560 and a non-listed employer (category D).",
  other_banks([("No salary transfer", "Needs AED 10,000 and AECB 600 → <b>declined</b>"), ("<b>Counter-offer</b>", "Move the salary to us: from AED 5,000 with AECB ≥ 541, the salary-assigned loan is open")]),
  ["The customer is <b>not just turned away</b>; she is offered a safer route.", "<b>Four months later</b>, if her salary stops arriving, the <b>nightly check</b> flags it.",
   "The rate steps up 2% and collections call her <b>within 5 working days</b>, before a missed payment becomes a default."],
  '<div class="flow"><span>Decline without salary transfer</span>→<span>Offer salary-transfer loan</span>→<span>Nightly check</span>→<span>Call within 5 days</span></div>'),
]
def scen_html():
    out = []
    for n, t, who, ob, ours, chart in SCEN:
        out.append(f'<div class="card scen"><div class="sc-head"><span class="sc-n">Scenario {n}</span><h4>{esc(t)}</h4></div><p class="who">{esc(who)}</p>'
                   f'<div class="sc-body"><div class="sc-l"><div class="mini-h">What banks say</div>{ob}</div>'
                   f'<div class="sc-r"><div class="mini-h">Our answer</div><ul>' + "".join(f"<li>{x}</li>" for x in ours) + f'</ul><div class="mc">{chart}</div></div></div></div>')
    return "".join(out)

TIMELINE = [("10:02:00", "Application arrives from the mobile app or branch system"), ("10:02:01", "Credit bureau (AECB) report pulled, with the customer's consent"),
            ("10:02:02", "Central Bank rules → bank policy → product rules checked"), ("10:02:02", "AI risk grade and safe amount calculated"),
            ("10:02:03", "Decision: approve, refer or decline, with reasons"), ("10:05", "Customer e-signs the offer after seeing the Key Facts Statement"),
            ("Same day", "Salary-assigned loan paid out once the employer letter is verified"), ("Every night", "Whole book re-checked for early-warning signs")]
def timeline_html():
    rows = "".join(f'<div class="tl-row{" fast" if i < 5 else ""}"><div class="tl-t">{esc(t)}</div><div class="tl-dot"></div><div class="tl-x">{esc(x)}</div></div>' for i, (t, x) in enumerate(TIMELINE))
    return f'<div class="tl"><div class="tl-brace">about 3 seconds</div>{rows}</div>'

css = f"""
@page {{ size: A4; margin: 13mm 13mm 15mm 13mm;
  @bottom-left {{ content: "Where Our Credit Policy Stands · UAE Bank Market · draft for discussion"; font: 8px 'Segoe UI', Arial, sans-serif; color: {MUTED}; }}
  @bottom-right {{ content: "Page " counter(page) " of " counter(pages); font: 8px 'Segoe UI', Arial, sans-serif; color: {MUTED}; }} }}
@page :first {{ @bottom-left {{ content: none; }} @bottom-right {{ content: none; }} }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 12.5px; line-height: 1.45; color: {INK}; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
h1 {{ font-size: 27px; line-height: 1.15; margin: 0 0 6px; letter-spacing: -0.3px; }}
h2 {{ font-size: 20px; margin: 0 0 4px; letter-spacing: -0.2px; }}
h3 {{ font-size: 15px; margin: 14px 0 2px; color: {TEAL}; }}
h4 {{ font-size: 12.5px; margin: 0; }}
p {{ margin: 4px 0 8px; }}
.eyebrow {{ font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase; color: {TEAL}; font-weight: 700; margin-bottom: 4px; }}
.pb {{ break-before: page; }}
.lead {{ font-size: 14px; color: {INK2}; }}
.lead-s {{ color: {INK2}; margin: 0 0 8px; }}
.answer {{ border-left: 5px solid {TEAL}; background: #eef6f6; padding: 12px 14px; font-size: 15px; line-height: 1.45; border-radius: 0 8px 8px 0; margin: 12px 0 14px; }}
.tiles {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; }}
.tile {{ border: 1px solid {LINE}; border-radius: 8px; padding: 10px; background: #fff; }}
.t-big {{ font-size: 22px; font-weight: 700; color: {TEAL}; line-height: 1.1; }}
.t-lbl {{ font-weight: 600; font-size: 11.5px; margin: 2px 0 4px; }}
.t-sub {{ font-size: 10px; color: {INK2}; line-height: 1.35; }}
.card {{ border: 1px solid {LINE}; border-radius: 8px; padding: 10px 11px; break-inside: avoid; background: #fff; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.sub {{ font-size: 10px; color: {MUTED}; margin: 1px 0 6px; }}
.note {{ font-size: 9.5px; color: {MUTED}; margin: 6px 0 0; }}
.res {{ font-size: 10.5px; margin: 0 0 6px; color: {INK2}; }}
.pie-row {{ display: flex; gap: 10px; align-items: center; }}
.legend {{ list-style: none; padding: 0; margin: 0; flex: 1; font-size: 10.5px; }}
.legend li {{ display: grid; grid-template-columns: 11px 1fr auto 34px; gap: 6px; align-items: center; padding: 3px 0; border-bottom: 1px solid #f0f2f4; }}
.sw {{ width: 10px; height: 10px; border-radius: 2px; display: inline-block; }}
.lg-v {{ font-weight: 600; text-align: right; }} .lg-p {{ text-align: right; color: {MUTED}; }}
.us-tag {{ display: inline-block; font-size: 8.5px; font-weight: 700; color: #fff; background: {TEAL}; border-radius: 3px; padding: 0 4px; margin-left: 3px; }}
.ch-head {{ display: flex; justify-content: space-between; align-items: center; gap: 6px; }}
.verdict {{ font-size: 9.5px; font-weight: 700; border-radius: 10px; padding: 1px 7px; white-space: nowrap; }}
.v-best {{ background: #1a5aa6; color: #fff; }} .v-ahead {{ background: #e3eefb; color: #1a5aa6; }} .v-mid {{ background: #eceff2; color: #4a5260; }} .v-behind {{ background: #fdeee6; color: #a8431a; }}
.jb {{ font-size: 9px; color: {TEAL}; font-weight: 700; margin-left: 4px; }}
.keyrow {{ display: flex; gap: 14px; font-size: 10px; color: {INK2}; margin: 4px 0 8px; flex-wrap: wrap; }}
.key {{ display: inline-flex; align-items: center; gap: 5px; }}
.dotk {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
.boxk {{ width: 14px; height: 9px; border-radius: 2px; display: inline-block; }}
table {{ border-collapse: collapse; width: 100%; }}
.vt th, .league th {{ text-align: left; font-size: 10px; color: {INK2}; border-bottom: 1.5px solid {INK}; padding: 4px 5px; }}
.vt td, .league td {{ font-size: 10.5px; padding: 3.5px 5px; border-bottom: 1px solid #edf0f3; vertical-align: middle; }}
.num {{ text-align: right; white-space: nowrap; }} small {{ color: {MUTED}; font-size: 9px; }}
tr.us td {{ background: #eef6f6; font-weight: 700; }}
.league .rk {{ width: 22px; color: {MUTED}; }} .league .seg {{ color: {MUTED}; font-size: 9.5px; }}
.barcell {{ position: relative; width: 38%; }} .barcell .lbar {{ height: 9px; border-radius: 0 3px 3px 0; display: inline-block; vertical-align: middle; max-width: 80%; }}
.barcell span {{ font-size: 9.5px; margin-left: 5px; vertical-align: middle; }}
.socard {{ position: relative; padding-left: 40px; }} .so-n {{ position: absolute; left: 10px; top: 10px; width: 22px; height: 22px; border-radius: 50%; background: {TEAL}; color: #fff; font-weight: 700; text-align: center; line-height: 22px; font-size: 12px; }}
.socard ul, .scen ul {{ margin: 5px 0 0; padding-left: 16px; }} .socard li, .scen li {{ margin: 2px 0; font-size: 11px; }}
.scen {{ margin-bottom: 9px; }} .sc-head {{ display: flex; align-items: baseline; gap: 8px; }}
.sc-n {{ font-size: 9.5px; font-weight: 700; color: #fff; background: {TEAL}; border-radius: 3px; padding: 1px 6px; text-transform: uppercase; letter-spacing: .6px; }}
.who {{ font-size: 10.5px; color: {INK2}; margin: 4px 0 6px; }}
.sc-body {{ display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 12px; }}
.mini-h {{ font-size: 9.5px; text-transform: uppercase; letter-spacing: .8px; color: {MUTED}; font-weight: 700; margin-bottom: 3px; }}
.ob td {{ font-size: 10px; padding: 3px 4px; border-bottom: 1px solid #edf0f3; vertical-align: top; }} .ob td:first-child {{ color: {INK2}; width: 44%; }}
.mc {{ margin-top: 6px; }}
.flow {{ display: flex; flex-wrap: wrap; gap: 4px; align-items: center; font-size: 10px; margin-top: 6px; color: {MUTED}; }}
.flow span {{ background: #eef6f6; color: {INK}; border: 1px solid #cfe4e4; border-radius: 4px; padding: 2px 6px; }}
.tl {{ position: relative; margin: 10px 0 0 0; padding-left: 0; }}
.tl-row {{ display: grid; grid-template-columns: 86px 22px 1fr; align-items: center; min-height: 30px; }}
.tl-t {{ font-weight: 700; font-size: 12px; text-align: right; padding-right: 8px; font-variant-numeric: tabular-nums; }}
.tl-dot {{ width: 12px; height: 12px; border-radius: 50%; background: {GRAYBAR}; margin-left: 5px; }}
.tl-row.fast .tl-dot {{ background: {TEAL}; }} .tl-row.fast .tl-t {{ color: {TEAL}; }}
.tl-x {{ font-size: 12px; padding-left: 6px; }}
.tl-brace {{ position: absolute; left: 480px; top: 6px; height: 140px; border-left: 3px solid {TEAL}; padding-left: 8px; font-weight: 700; color: {TEAL}; display: flex; align-items: center; font-size: 13px; }}
.notes li {{ font-size: 10.5px; margin: 3px 0; }}
.ptag {{ font-size: 9px; text-transform: uppercase; letter-spacing: .8px; color: {TEAL}; font-weight: 700; margin-bottom: 1px; }}
.callout {{ background: #f4f6f8; border-radius: 8px; padding: 9px 11px; font-size: 11px; margin: 8px 0; }}
.lever td:first-child {{ width: 52%; }}
.mapnote {{ font-size: 9.5px; color: {MUTED}; }}
"""

key_strip = (f'<div class="keyrow"><span class="key"><span class="boxk" style="background:{ORANGE}"></span>Banks easier or cheaper than us</span>'
             f'<span class="key"><span class="boxk" style="background:#d5dae0"></span>Same as us</span>'
             f'<span class="key"><span class="boxk" style="background:{BLUE}"></span>Banks stricter or dearer than us</span></div>')
key_map = (f'<div class="keyrow"><span class="key"><span class="dotk" style="background:{TEAL}"></span>Our policy</span>'
           f'<span class="key"><span class="dotk" style="background:#4b5563"></span>Top 5 banks by retail book</span>'
           f'<span class="key"><span class="dotk" style="background:#aab2bb"></span>Other banks</span>'
           f'<span class="key">Shaded = easier to get and cheaper than the market middle</span></div>')

top5_access = sorted([r for r in LEAGUE if r["segment"] in ("Top-5", "Policy")], key=lambda r: -r["access"])
HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Where Our Credit Policy Stands - UAE Bank Market</title><style>{css}</style></head><body>

<section>
<div class="eyebrow">UAE conventional bank · retail credit policy v0.1 · market check 9 November 2026</div>
<h1>Where Our Credit Policy Stands<br>in the UAE Bank Market</h1>
<p class="lead">We compared our draft retail credit policy with every UAE bank that publishes its retail lending terms: {N_BANKS} banks, 16 measures, five products.</p>
<div class="answer"><b>The short answer.</b> {S1}</div>
{tiles_html()}
<h3>The market map: how easy, how cheap</h3>
<p class="lead-s">Each dot is a bank. Further right = easier to qualify and borrow more. Higher = lower prices. 50 = market middle.</p>
{key_map}
{SCATTER_SVG}
<p class="mapnote">{N_LEAGUE} banks have enough published data for the map (at least 5 access and 2 price measures).{(" Unlabelled for space: " + esc(", ".join(UNLABELLED)) + ".") if UNLABELLED else ""} Full scores are in the league table.</p>
<div class="callout"><b>Three things to remember</b><ol style="margin:4px 0 0;padding-left:18px">
<li><b>Easy to get.</b> Entry salaries are at or below the market median on every product, and AED 5,000 without salary transfer (with safeguards) is the joint lowest in the UAE.</li>
<li><b>Fairly priced.</b> Rates sit near the market median. Only the home-loan fixed rate (4.24% vs a 3.99% median) is dearer than most banks.</li>
<li><b>Different.</b> Salary advance, end-of-service-backed finance and gold-backed lending are products the big conventional banks do not offer.</li></ol></div>
</section>

<section class="pb">
<div class="eyebrow">Part 1</div>
<h2>The UAE market at a glance</h2>
<p class="lead-s">These charts use Central Bank (CBUAE) totals, so every slice is a true share of the market.</p>
<div class="grid2">{"".join(pies_market)}</div>
<h3>The biggest retail lenders</h3>
<p class="lead-s">Retail loan books in AED billions, as published by each bank.</p>
<div class="card">{hbar_simple(BOOKS, "bn")}<p class="note"><b>Not additive.</b> Some figures include overseas or group books, or are segment assets, so they add up to roughly the whole CBUAE individual-credit total (AED 645.8bn). Read them as sizes, not market shares. Our policy is new, so it has no book yet.</p></div>
</section>

<section class="pb">
<div class="eyebrow">Part 2</div>
<h2>Where we sit, measure by measure</h2>
<p class="lead-s">For each measure, the bar splits all banks with published terms into three groups. A long blue part means most banks are stricter or dearer than us.</p>
{key_strip}
<div class="card">{strip()}</div>
<div class="callout"><b>Score across 16 measures:</b> joint best on <b>{VERD['Joint best']}</b> (no bank is easier: {esc("; ".join(group_of(m['key']).lower() + ", " + SHORTLBL[m['key']].lower() for m in JOINT))}), ahead of most on <b>{VERD['Ahead of most']}</b>, market middle on <b>{VERD['Market middle']}</b>, behind most on <b>{VERD['Behind most']}</b> (the home-loan fixed rate, 4.24% vs a 3.99% median).</div>
<div class="grid2">{pie_bands}{pie_ns}</div>
</section>

<section class="pb">
<div class="eyebrow">Part 3</div>
<h2>Product by product</h2>
<p class="lead-s">Bars are sorted from the easiest or cheapest bank at the top. <b style="color:{TEAL}">Teal</b> is our policy; the dashed line is the market median. Values are the banks' own published terms. The badge gives our position: <span class="verdict v-best">Joint best</span> <span class="verdict v-ahead">Ahead of most</span> <span class="verdict v-mid">Market middle</span> <span class="verdict v-behind">Behind most</span></p>
{product_sections()}
</section>

<section class="pb">
<div class="eyebrow">Part 4</div>
<h2>League table</h2>
<p class="lead-s"><b>How the score works:</b> on each measure, a bank scores 0–100 by how many banks it beats (ties count half). <b>Access</b> averages the 12 entry-salary, loan-size and loan-to-value measures; <b>Price</b> averages the 4 rate measures; <b>Overall</b> is the average of the two. Rank in brackets.</p>
{league_html()}
<p class="note">Banks with too little published data are left out of the table but are in the charts. Islamic banks' profit rates are compared like interest rates; some were converted from flat rates.</p>
</section>

<section class="pb">
<div class="eyebrow">Part 4 (continued)</div>
<h2>All 16 measures in one table</h2>
{verdict_table()}
<div class="callout">Among the top five banks and our policy, ease of access ranks: {esc(" · ".join(f"{i}. {r['short']} ({r['access']:.0f})" for i, r in enumerate(top5_access, 1)))}. Only the two large Islamic banks score higher; we lead every large conventional bank.</div>
</section>

<section class="pb">
<div class="eyebrow">Part 5</div>
<h2>How our policy stands out</h2>
<p class="lead-s">Six things a customer, a broker or a regulator will notice.</p>
{standout_html()}
<h3>What would move us further up</h3>
<p class="lead-s">Our price score is in the middle by design. Two small pricing changes would lift the overall rank. These are options for the pricing committee, not part of the draft policy.</p>
{lever_html()}
</section>

<section class="pb">
<div class="eyebrow">Part 6</div>
<h2>Real customers, real answers</h2>
<p class="lead-s">Eight realistic cases. The people are illustrative; market answers come from the banks' published terms (9 November 2026); the numbers use our policy's rates and rules.</p>
{scen_html()}
</section>

<section class="pb">
<div class="eyebrow">Part 7</div>
<h2>The decision in about three seconds</h2>
<p class="lead-s">What happens behind the scenes for any of the scenarios above.</p>
<div class="card">{timeline_html()}</div>
<div class="callout">The AI never decides alone. Central Bank rules and the bank's policy are checked first, every decision is logged with its reasons, and anything unusual is referred to a credit officer.</div>

<h2 style="margin-top:22px">Data notes</h2>
<ul class="notes">
<li><b>Sources:</b> each bank's own product pages and Key Facts Statements, checked 9 November 2026; a few values from search extracts or comparison sites, marked by confidence (H/M/L) in <i>all_banks.csv</i>. Market totals: CBUAE Statistical Bulletin (August 2026), Financial Stability Report 2025, Q2 2026 quarterly report.</li>
<li><b>Banks covered:</b> {N_BANKS} banks ({N_NAT} national incl. digital, {N_FOR} foreign). Left out because they do not lend to the public in the UAE: Emirates Investment Bank (private bank), Zand (no retail lending), Emirates Development Bank (government housing), Mal (not launched), Doha Bank UAE (legacy fees only), and foreign branches with no onshore retail lending (e.g. HBL, Janata, MCB, SBI, ICICI, the wholesale banks).</li>
<li><b>Published terms are not approvals.</b> Banks may approve below or above their published figures. Where a bank publishes several numbers (for example, nationals vs expats) we used the headline figure for the segment shown.</li>
<li><b>Rates:</b> personal-loan and home rates are reducing-balance; car rates are flat. Some Islamic profit rates were converted from flat to reducing (approximate). Our expat personal-loan floor is 5.99%.</li>
<li><b>Known data conflicts</b> (e.g. CBD national maximum 2.5m vs 3m; CBI home-loan minimum salary; Wio rate floor) are listed in <i>notes_national_rest.md</i>. We used the bank's own document where there was a conflict.</li>
<li><b>Our policy</b> is draft v0.1 for the conventional bank (<i>05-retail-credit-policy.md</i>), not yet approved. Its numbers come from <i>03-parameter-sheet.md</i>. Retail loan books are group or segment figures and are not additive.</li>
<li><b>Files:</b> all_banks.csv (merged data), position_table.csv (per-measure position), market-position-report.md (text version of this report).</li>
</ul>
</section>
</body></html>"""

out_html = S / "report.html"
out_html.write_text(HTML, encoding="utf-8")
prof = S / "chrome-profile-mp"
r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={prof}",
                    f"--print-to-pdf={PDF}", out_html.as_uri()], capture_output=True, text=True, timeout=180)
print("chrome rc", r.returncode, r.stderr[-300:] if r.returncode else "")

import csv
with open(MP / "position_table.csv", "w", newline="", encoding="utf-8") as fh:
    keys = ["key", "measure", "unit", "better", "policy", "n", "friendlier", "same", "less_friendly", "rank", "median", "policy_pct", "verdict"]
    w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(MEASURES)
with open(MP / "position_table.md", "w", encoding="utf-8") as fh:
    fh.write("# Where our policy stands, per measure\n\nEasier = banks easier or cheaper than us; Stricter = banks stricter or dearer. Score = share of banks beaten (ties count half), 0-100.\n\n")
    fh.write("| Measure | Our policy | Banks | Easier | Same | Stricter | Median | Score | Verdict |\n|---|---|---|---|---|---|---|---|---|\n")
    for m in MEASURES:
        fh.write(f"| {m['measure']} | {fmt(m['policy'], m['unit'])} | {m['n']} | {m['friendlier']} | {m['same']} | {m['less_friendly']} | {fmt(m['median'], m['unit'])} | {m['policy_pct']:.0f} | {m['verdict']} |\n")
# ---------------- Markdown twin ----------------
md = []
md.append("# Where Our Credit Policy Stands in the UAE Bank Market\n")
md.append(f"UAE conventional bank, retail credit policy v0.1. Market checked 9 November 2026. PDF version: *Where Our Credit Policy Stands - UAE Bank Market.pdf*.\n")
md.append("## The short answer\n")
md.append(html.unescape(S1.replace("<b>", "**").replace("</b>", "**")) + "\n")
md.append("| Headline | Detail |\n|---|---|")
for a, b, c in tiles: md.append(f"| **{a}** {b} | {c} |")
md.append("\n## The UAE market at a glance (CBUAE)\n")
md.append("| Measure | Value |\n|---|---|\n| Licensed banks | 62: 24 national, 26 foreign full-licence, 12 foreign wholesale |\n| Conventional / Islamic | 52 / 10 |\n| Domestic credit (Aug 2026) | AED 2,268.8bn: companies 984.9, individuals 645.8, government, GREs & other 638.1 (derived) |\n| Domestic credit by bank group | National conventional 1,573.0 (derived), Islamic banks 544.2, foreign banks 151.6 |\n")
md.append("**Biggest retail lenders (AED bn, not additive):** " + "; ".join(f"{a} {v:g}" + (f" ({n})" if n else "") for a, v, n in BOOKS) + ".\n")
md.append("## Where we sit, measure by measure\n")
md.append("| Product | Measure | Our policy | Market median | Banks easier / same / stricter | Verdict |\n|---|---|---|---|---|---|")
for g, p in GROUPS:
    for m in [m for m in MEASURES if m["key"].startswith(p)]:
        md.append(f"| {g} | {SHORTLBL[m['key']]} | {fmt(m['policy'], m['unit'])} | {fmt(m['median'], m['unit'])} | {m['friendlier']} / {m['same']} / {m['less_friendly']} | {m['verdict']}{(' (shared with ' + str(m['same']) + ')') if m['joint_best'] else ''} |")
md.append(f"\nJoint best on {VERD['Joint best']} of 16 (no bank easier), ahead of most on {VERD['Ahead of most']}, market middle on {VERD['Market middle']}, behind most on {VERD['Behind most']}.\n")
md.append("**Entry salary (personal loan, salary transferred):** " + ", ".join(f"{b}: {bands[b]}" for b in band_order) + f" banks. Ours: AED 5,000.\n")
md.append(f"**Personal loan without salary transfer:** Yes {ns['Y']}, only cards/car/home {ns['P']}, no {ns['N']}, not published {ns['?']}. Ours: yes, AED 5,000 with AECB ≥ 600, employer A–C and 6 months' service (otherwise AED 10,000).\n")
md.append("## League table\n")
md.append("Score per measure = share of banks beaten (ties half), 0–100. Access = 12 entry/size/LTV measures; Price = 4 rate measures; Overall = average.\n")
md.append("| # | Bank | Type | Overall | Access (rank) | Price (rank) |\n|---|---|---|---|---|---|")
for r in LEAGUE:
    nm = f"**{r['short']}**" if r["segment"] == "Policy" else r["short"]
    md.append(f"| {r['overall_rank']} | {nm} | {r['segment']} | {r['overall']:.0f} | {r['access']:.0f} (#{r['access_rank']}) | {r['price']:.0f} (#{r['price_rank']}) |")
md.append("\n## How our policy stands out\n")
import re
strip_tags = lambda s: html.unescape(re.sub(r"</?b>", "**", s))
for i, (t, bs) in enumerate(STANDOUT, 1):
    md.append(f"{i}. **{html.unescape(t)}**")
    for b in bs: md.append(f"   - {strip_tags(b)}")
md.append("\n**What would move us further up (options for the pricing committee):**\n")
md.append("| Change | Price score (rank) | Overall | Overall rank |\n|---|---|---|---|")
md.append(f"| Policy as drafted | {OURS['price']:.0f} (#{OURS['price_rank']}) | {OURS['overall']:.0f} | #{OURS['overall_rank']} of {N_LEAGUE} |")
for l in LEVERS: md.append(f"| {l['label']} | {l['price']:.0f} (#{l['price_rank']}) | {l['overall']:.0f} | #{l['rank']} of {N_LEAGUE} |")
md.append("\n## Real customers, real answers\n")
for n, t, who, ob, ours, chart in SCEN:
    md.append(f"### Scenario {n}: {html.unescape(t)}\n{who}\n")
    for row in re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td></tr>", ob): md.append(f"- {strip_tags(row[0])}: {strip_tags(row[1])}")
    md.append("")
    for x in ours: md.append(f"- {strip_tags(x)}")
    md.append("")
md.append("## The decision in about three seconds\n\n| Time | What happens |\n|---|---|")
for t, x in TIMELINE: md.append(f"| {t} | {x} |")
md.append("\n## Data notes\n")
md.append(f"- {N_BANKS} banks ({N_NAT} national incl. digital, {N_FOR} foreign); banks that do not lend to the public onshore are excluded (Emirates Investment Bank, Zand, EDB, Mal, Doha Bank UAE legacy, wholesale/DIFC-only branches).")
md.append("- Sources: banks' own pages and KFS (checked 9 Nov 2026), confidence H/M/L in all_banks.csv; CBUAE Statistical Bulletin Aug 2026, FSR 2025, Q2 2026 report.")
md.append("- Published terms are not approvals. Retail books are group/segment figures, not additive. Our policy is draft v0.1, not yet approved.")
MD.write_text("\n".join(md) + "\n", encoding="utf-8")
print("OURS", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in OURS.items()})
print("conv access rank", CONV_ACCESS_RANK, "of", N_CONV, "| levers", [(l["label"][:30], round(l["price"], 1), l["rank"]) for l in LEVERS])
print("unlabelled", UNLABELLED)
