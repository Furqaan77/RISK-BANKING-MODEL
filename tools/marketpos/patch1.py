import pathlib
p = pathlib.Path(__file__).parent / "build_report.py"; s = p.read_text(encoding="utf-8")
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:70], s.count(old)); s = s.replace(old, new)

# 1. joint-best verdict
rep('MBY = {m["key"]: m for m in MEASURES}', 'for m in MEASURES:\n    if m["friendlier"] == 0: m["verdict"] = "Joint best"\nMBY = {m["key"]: m for m in MEASURES}')
rep('vc = {"Ahead of most": BLUE, "Market middle": "#8a939d", "Behind most": ORANGE}[v]\n            badge = " · joint best" if m["joint_best"] else ""',
    'vc = {"Joint best": BLUE, "Ahead of most": BLUE, "Market middle": "#8a939d", "Behind most": ORANGE}[v]\n            badge = f" · shared with {s}" if m["joint_best"] else ""')
s = s.replace('{"Ahead of most": "v-ahead", "Market middle": "v-mid", "Behind most": "v-behind"}[m["verdict"]]',
              '{"Joint best": "v-best", "Ahead of most": "v-ahead", "Market middle": "v-mid", "Behind most": "v-behind"}[m["verdict"]]')
rep(".v-ahead {{", ".v-best {{ background: #1a5aa6; color: #fff; }} .v-ahead {{")
rep("""            jb = ' <span class="jb">joint best</span>' if m["joint_best"] else \"\"""",
    """            jb = f' <span class="jb">shared with {m["same"]}</span>' if m["joint_best"] else \"\"""")
rep("""<div class="callout"><b>Score:</b> ahead of most banks on <b>{VERD['Ahead of most']}</b> of 16 measures, in the market middle on <b>{VERD['Market middle']}</b>, behind most on <b>{VERD['Behind most']}</b> (the home-loan fixed rate). Joint best on {len(JOINT)}: {esc(", ".join(group_of(m['key']).lower() + ": " + SHORTLBL[m['key']].lower() for m in JOINT))}.</div>""",
    """<div class="callout"><b>Score across 16 measures:</b> joint best on <b>{VERD['Joint best']}</b> (no bank is easier: {esc("; ".join(group_of(m['key']).lower() + ", " + SHORTLBL[m['key']].lower() for m in JOINT))}), ahead of most on <b>{VERD['Ahead of most']}</b>, market middle on <b>{VERD['Market middle']}</b>, behind most on <b>{VERD['Behind most']}</b> (the home-loan fixed rate, 4.24% vs a 3.99% median).</div>""")
rep("""md.append(f"\\nAhead of most on {VERD['Ahead of most']} of 16, market middle on {VERD['Market middle']}, behind most on {VERD['Behind most']}.\\n")""",
    """md.append(f"\\nJoint best on {VERD['Joint best']} of 16 (no bank easier), ahead of most on {VERD['Ahead of most']}, market middle on {VERD['Market middle']}, behind most on {VERD['Behind most']}.\\n")""")
rep("""{m['verdict']}{' (joint best)' if m['joint_best'] else ''} |")""",
    """{m['verdict']}{(' (shared with ' + str(m['same']) + ')') if m['joint_best'] else ''} |")""")

# 2. headline wording (N_CONV includes our policy)
rep('assert CONV_ACCESS_RANK == 1, CONV_ACCESS_RANK',
    'assert CONV_ACCESS_RANK == 1, CONV_ACCESS_RANK\n'
    'AHEAD_ON_ACCESS = [r for r in LEAGUE if r["access"] > next(x for x in LEAGUE if x["segment"] == "Policy")["access"]]\n'
    'assert all("islamic" in r["type"] for r in AHEAD_ON_ACCESS), AHEAD_ON_ACCESS')
rep("""S1 = (f"Our credit policy is one of the easiest in the UAE to qualify for: <b>first of {N_CONV} conventional banks</b> and "
      f"<b>{OURS['access_rank']}th of {N_LEAGUE} banks</b> on ease of access. Its prices sit in the <b>middle of the market</b>, as intended. "
      f"Overall it ranks <b>{OURS['overall_rank']}th of {N_LEAGUE}</b>, in the upper half of the market.")""",
    """S1 = (f"Our credit policy is one of the easiest in the UAE to qualify for. It is <b>easier than all {N_CONV-1} conventional banks</b> with enough published data, and "
      f"<b>{OURS['access_rank']}th of {N_LEAGUE} banks</b> on ease of access, behind only {len(AHEAD_ON_ACCESS)} Islamic banks. Its prices sit in the <b>middle of the market</b>, as intended. "
      f"Overall it ranks <b>{OURS['overall_rank']}th of {N_LEAGUE}</b>, in the upper half of the market.")""")
rep("""    (f"#1 of {N_CONV}", "conventional banks for ease of access", f"#{OURS['access_rank']} of all {N_LEAGUE} banks with enough data. Only 4 Islamic banks score higher."),""",
    """    ("#1", "for ease of access among conventional banks", f"Ahead of all {N_CONV-1} conventional banks with enough data; #{OURS['access_rank']} of {N_LEAGUE} counting Islamic banks."),""")

# 3. retail bars value area
rep('lw, vw = 170, 120; bw = width - lw - vw', 'lw, vw = 150, 205; bw = width - lw - vw')

# 4. scenario first column unescaped (trusted strings)
rep("""\"\".join(f'<tr><td>{esc(a)}</td><td>{b}</td></tr>' for a, b in rows)""", """\"\".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in rows)""")

# 5. value labels drawn last with a white halo
rep("""out.append(f'<text x="{lw+w+4:.1f}" y="{y+bh-0.5}" font-size="9" font-weight="{700 if pol else 400}" fill="{INK if pol else MUTED}">{esc(fmt_short(v, unit))}</text>')""",
    """vals.append(f'<text x="{lw+w+4:.1f}" y="{y+bh-0.5}" font-size="9" font-weight="{700 if pol else 400}" fill="{INK if pol else MUTED}" stroke="#fff" stroke-width="3" paint-order="stroke">{esc(fmt_short(v, unit))}</text>')""")
rep("""    out.append(f'<line x1="{lw}" y1="{top-4}" x2="{lw}" y2="{h-2}" stroke="{LINE}" stroke-width="1"/>')
    for i, (name, v, pol) in enumerate(ents):""", """    out.append(f'<line x1="{lw}" y1="{top-4}" x2="{lw}" y2="{h-2}" stroke="{LINE}" stroke-width="1"/>')
    vals = []
    for i, (name, v, pol) in enumerate(ents):""")
rep("""    out.append(f'<text x="{tx:.1f}" y="{top-9}" text-anchor="{anchor}" font-size="9" fill="{INK2}">Market median {esc(fmt_short(med, unit))}</text>')
    out.append("</svg>")""", """    out.append(f'<text x="{tx:.1f}" y="{top-9}" text-anchor="{anchor}" font-size="9" fill="{INK2}">Market median {esc(fmt_short(med, unit))}</text>')
    out.extend(vals); out.append("</svg>")""")

# 6. product charts: one flowing grid, product name on each card
rep("""    return (f'<div class="chart card"><div class="ch-head"><h4>{esc(SHORTLBL[m["key"]])}</h4>""",
    """    return (f'<div class="chart card"><div class="ptag">{esc(group_of(m["key"]))}</div><div class="ch-head"><h4>{esc(SHORTLBL[m["key"]])}</h4>""")
rep("""        out.append(f'<div class="prod"><h3>{esc(g)}</h3><p class="lead-s">{esc(intro[g])}</p><div class="grid2">' + "".join(chart_card(m) for m in ms) + "</div></div>")
    return "".join(out)""", """        out.extend(chart_card(m) for m in ms)
    return '<div class="grid2">' + "".join(out) + "</div>\"""")
rep(".prod {{ break-before: page; }} .prod:first-of-type {{ break-before: auto; }}",
    ".ptag {{ font-size: 9px; text-transform: uppercase; letter-spacing: .8px; color: {TEAL}; font-weight: 700; margin-bottom: 1px; }}")
rep("""Values are the banks' own published terms.</p>""",
    """Values are the banks' own published terms. The badge gives our position: <span class="verdict v-best">Joint best</span> <span class="verdict v-ahead">Ahead of most</span> <span class="verdict v-mid">Market middle</span> <span class="verdict v-behind">Behind most</span></p>""")

# 7. page-1 takeaways
rep("""Full scores are in the league table.</p>
</section>""", """Full scores are in the league table.</p>
<div class="callout"><b>Three things to remember</b><ol style="margin:4px 0 0;padding-left:18px">
<li><b>Easy to get.</b> Entry salaries are at or below the market median on every product, and AED 5,000 without salary transfer (with safeguards) is the joint lowest in the UAE.</li>
<li><b>Fairly priced.</b> Rates sit near the market median. Only the home-loan fixed rate (4.24% vs a 3.99% median) is dearer than most banks.</li>
<li><b>Different.</b> Salary advance, end-of-service-backed finance and gold-backed lending are products the big conventional banks do not offer.</li></ol></div>
</section>""")

# 8. final verdicts back into position_table.csv / .md
rep('# ---------------- Markdown twin ----------------', '''import csv
with open(MP / "position_table.csv", "w", newline="", encoding="utf-8") as fh:
    keys = ["key", "measure", "unit", "better", "policy", "n", "friendlier", "same", "less_friendly", "rank", "median", "policy_pct", "verdict"]
    w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(MEASURES)
with open(MP / "position_table.md", "w", encoding="utf-8") as fh:
    fh.write("# Where our policy stands, per measure\\n\\nEasier = banks easier or cheaper than us; Stricter = banks stricter or dearer. Score = share of banks beaten (ties count half), 0-100.\\n\\n")
    fh.write("| Measure | Our policy | Banks | Easier | Same | Stricter | Median | Score | Verdict |\\n|---|---|---|---|---|---|---|---|---|\\n")
    for m in MEASURES:
        fh.write(f"| {m['measure']} | {fmt(m['policy'], m['unit'])} | {m['n']} | {m['friendlier']} | {m['same']} | {m['less_friendly']} | {fmt(m['median'], m['unit'])} | {m['policy_pct']:.0f} | {m['verdict']} |\\n")
# ---------------- Markdown twin ----------------''')
p.write_text(s, encoding="utf-8"); print("patched OK")
