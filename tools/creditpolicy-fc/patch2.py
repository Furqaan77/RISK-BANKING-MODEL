import pathlib

p = pathlib.Path(__file__).with_name("build_fc_gap.py")
s = p.read_text(encoding="utf-8")

rep = [
    # MD: scenario summary + maths tables
    ('for i, s in enumerate(SCENARIOS, 1):\n    m.append("### Scenario',
     'm.append("| Customer | Product | Outcome | Key number |\\n|---|---|---|---|")\n'
     'for r in sc.SUMMARY:\n    m.append("| {} | {} | {} | {} |".format(*r))\n'
     'm.append("")\n'
     'for i, s in enumerate(SCENARIOS, 1):\n    m.append("### Scenario'),
    ('        m.append("| **{}** | {} |".format(lab, s[key]))\n    m.append("")\n',
     '        m.append("| **{}** | {} |".format(lab, s[key]))\n'
     '    m.append("\\n**The maths**\\n")\n'
     '    m.append("| Step | Working | Result |\\n|---|---|---|")\n'
     '    for st, wk, rs in s["maths"]:\n'
     '        m.append("| {} | {} | {} |".format(st, wk, rs))\n'
     '    m.append("")\n'),
    # MD: sign-off + data notes before sources
    ('m.append("\\n## 8. Sources")',
     'm.append("\\n### Sign-off list: {} items ({} [A] adjusted, {} [P] proposals)".format(len(SIGNOFF), N_A, N_P))\n'
     'm.append("| ID | Item | Tag | Policy value | Rating |\\n|---|---|---|---|---|")\n'
     'for it in SIGNOFF:\n'
     '    m.append("| {} | {} | {} | {} | {} |".format(it[1], it[2], " ".join("[{}]".format(t) for t in it[7].split("/")), it[3], it[6]))\n'
     'm.append("\\nThe policy text also marks two rules [P]: repricing when a salary account is moved without clearance (§8.1) and the sector watch-list (§7.5).")\n'
     'm.append("\\n## 8. Data notes and confidence")\n'
     'for t_ in DATA_NOTES:\n'
     '    m.append("- " + t_)\n'
     'm.append("\\n## 9. Sources")'),
]
for a, b in rep:
    n = s.count(a)
    assert n == 1, (n, a[:70])
    s = s.replace(a, b)

DATA_NOTES = '''DATA_NOTES = [
    "**Bank figures are not market shares.** Bank retail-book sizes quoted elsewhere include group and overseas books. Only CBUAE totals (credit to individuals AED 645.8bn, Aug 2026; finance-company loans about AED 11.2bn, FSR 2025) are used for market-size comparisons and pies.",
    "**Finance-company status pie:** the 20 entities on the CB Register (Aug 2026), grouped by our reading of their websites and KFS documents. 'Active' means a published retail product and KFS; it is not a measure of size.",
    "**Loan-mix pie:** FSR 2025 shares of the whole finance-company sector, not of any one company.",
    "**Rates:** reducing balance unless marked flat. Flat rates are converted to reducing only where stated (Aafaq 8% flat is about 14.5%; our used-car 4.49% flat is about {} reducing).".format(pc(A_RED)),
    "**Ranges:** a bar shows the lowest and highest published value; a single dot means only one value (often a 'from' rate) is published.",
    "**Digital / BNPL lenders** (botim / CashNow, e& easyCredit, Tamara) are shown separately from full finance companies because they sell small, short loans.",
    "**Confidence:** H = read directly from a KFS, report or register; M = search extract (the FCR rulebook returned HTTP 403, so FCR values must be confirmed by Legal & Compliance). Finance companies publish no AECB floors, so the AECB comparison is qualitative.",
    "**Scenarios** use illustrative customers; every number is calculated by the build script from the policy values.",
]

'''
assert s.count("SOURCES = [") == 1
s = s.replace("SOURCES = [", DATA_NOTES + "SOURCES = [", 1)
p.write_text(s, encoding="utf-8", newline="\n")
print("patch2 ok")
