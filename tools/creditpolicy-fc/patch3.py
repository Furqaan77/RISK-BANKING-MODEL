import pathlib

p = pathlib.Path(__file__).with_name("build_fc_gap.py")
s = p.read_text(encoding="utf-8")


def R(a, b):
    global s
    n = s.count(a)
    assert n == 1, (n, a[:80])
    s = s.replace(a, b)


# --md-only exit right after the markdown file is written
R('(OUT / "04-benchmark-gap-report.md").write_text("\\n".join(m) + "\\n", encoding="utf-8")\n',
  '(OUT / "04-benchmark-gap-report.md").write_text("\\n".join(m) + "\\n", encoding="utf-8")\n'
  'print("md written", dict(TOT), "| sign-off", len(SIGNOFF))\n'
  'if "--md-only" in sys.argv:\n    sys.exit(0)\n')

# section 4 title
R('m.append("\\n## 4. How the policy stands out")', 'm.append("\\n## 4. How we stand out among finance companies")')
R("h.append('<h2 class=\"pb\">4. How the policy stands out</h2><div class=\"std\">')",
  "h.append('<h2 class=\"pb\">4. How we stand out among finance companies</h2><div class=\"std\">')")

# CSS additions
R('.chk li::before', '.what { font-size: 8.2pt; color: #3d4a5c; margin: 6px 0 2px; line-height: 1.4; }\n'
  '.what b { color: #0F6E6A; }\n'
  'table.maths { font-size: 8pt; margin: 7px 0 2px; }\n'
  'table.maths th { background: #0F7B7B; padding: 3px 6px; }\n'
  'table.maths td { padding: 3px 6px; }\n'
  'table.maths td:last-child { text-align: right; white-space: nowrap; font-weight: 700; }\n'
  '.ok { color: #0a6b3d; font-weight: 700; } .no { color: #b3261e; font-weight: 700; }\n'
  '.chk li::before')

# rating donut caption
R("'<div><h4>How the {} policy items compare with the finance-company market</h4>'.format(NITEMS) + pie_legend(rrows, CAT, pct=True) + '</div></div>')",
  "'<div><h4>How the {} policy items compare with the finance-company market</h4>'.format(NITEMS) + pie_legend(rrows, CAT, pct=True) +\n"
  "         '<p class=\"what\"><b>What this shows:</b> {} of {} items sit inside the finance-company range and {} are better for customers. Only {} are deliberately tighter, and none is looser than the CBUAE or the FCR.</p>'.format(TOT[d.N], NITEMS, TOT[d.E], TOT[d.T]) + '</div></div>')")

# status donut caption
R("'<p class=\"small\" style=\"margin-top:4px\">CB Register, Aug 2026; status from our research. Several legacy (mostly Islamic) companies are winding down; new entrants are digital.</p></div></div>')",
  "'<p class=\"what\"><b>What this shows:</b> only 9 of the 20 licensed finance companies actively lend to individuals. Several legacy (mostly Islamic) companies are winding down; new entrants are digital. Source: CB Register, Aug 2026; status from our research. Counts of companies, not market shares.</p></div></div>')")

# mix donut caption
R("'<p class=\"small\" style=\"margin-top:4px\">FSR 2025, shares of about AED 11.2bn. Personal and vehicle loans are only about 14% of finance-company lending: the retail space is small and run by a handful of active lenders.</p></div></div>')",
  "'<p class=\"what\"><b>What this shows:</b> personal and vehicle loans are only about 14% of finance-company lending. The retail space is small and run by a handful of active lenders, so a disciplined new entrant can win share. Source: FSR 2025, shares of about AED 11.2bn.</p></div></div>')")

# 58 times computed
R("banks lend AED 645.8bn to individuals, 58 times more", "banks lend AED 645.8bn to individuals, about ' + '{:.0f}'.format(645.8 / 11.2) + ' times more")

# section 3 charts: own legend per chart + "what this shows"
R("h.append('<p>Our policy is shown in blue, finance companies in orange and the top five banks in green. Bars run from the lowest to the highest published value; a single dot means only one value is published.</p>')\nh.append(group_legend())\n",
  "h.append('<p>Each chart has its own colour key. Our policy is always blue. Bars run from the lowest to the highest published value; a single dot means only one value is published.</p>')\n")
R("h.append('<div class=\"chartbox\"><h4>Personal-loan interest rate, % a year (reducing balance)</h4><p class=\"note\">Below the finance-company typical, above the banks.</p>' +\n         range_svg(d.PL_RATES, 40, 5, \"%\", \"Personal-loan interest rate ranges\") + '</div>')",
  "h.append('<div class=\"chartbox\"><h4>Personal-loan interest rate, % a year (reducing balance)</h4>' + group_legend((\"us\", \"fc\", \"digital\", \"bank\")) +\n"
  "         range_svg(d.PL_RATES, 40, 5, \"%\", \"Personal-loan interest rate ranges\") +\n"
  "         '<p class=\"what\"><b>What this shows:</b> our 12.99% starting rate is below every finance company and digital lender, and our top rate (29.99%) is below the market highs of 36–40%. Banks are cheaper, but only for customers who move their salary.</p></div>')")
R("h.append('<div class=\"chartbox\"><h4>Minimum monthly salary for a personal loan, AED</h4><p class=\"note\">Same entry point as most finance companies (AED 5,000); AED 7,000 for weaker profiles without employer assignment.</p>' +\n         hbar_svg(d.PL_MIN_SALARY, 10000, 2000, fmt_aed, \"Minimum salary for a personal loan\") + '</div>')",
  "h.append('<div class=\"chartbox\"><h4>Minimum monthly salary for a personal loan, AED</h4>' + group_legend((\"us\", \"fc\", \"digital\", \"bank\")) +\n"
  "         hbar_svg(d.PL_MIN_SALARY, 10000, 2000, fmt_aed, \"Minimum salary for a personal loan\") +\n"
  "         '<p class=\"what\"><b>What this shows:</b> we start at AED 5,000, the same as most finance companies and the bank median. Weaker profiles without employer assignment need AED 7,000. Customers below AED 5,000 get a salary advance, not a loan.</p></div>')")
R("h.append('<div class=\"chartbox\"><h4>Maximum personal loan, AED</h4><p class=\"note\">Mid-market for a finance company; well below banks, which keeps single-customer risk small against AED 150m of capital.</p>' +\n         hbar_svg(d.PL_MAX_AMOUNT, 500000, 100000, fmt_aedk, \"Maximum personal loan\") + '</div>')",
  "h.append('<div class=\"chartbox\"><h4>Maximum personal loan, AED</h4>' + group_legend((\"us\", \"fc\", \"digital\", \"bank\")) +\n"
  "         hbar_svg(d.PL_MAX_AMOUNT, 500000, 100000, fmt_aedk, \"Maximum personal loan\") +\n"
  "         '<p class=\"what\"><b>What this shows:</b> our caps (AED 150,000–300,000) are mid-market for a finance company and well below banks. This keeps single-customer risk small against AED 150m of capital.</p></div>')")
R("h.append('<div class=\"chartbox\"><h4>Credit-card interest, % a month</h4><p class=\"note\">3.59% standard (3.25% premium): below Finance House, Deem and Aafaq.</p>' +\n         range_svg(d.CARD_RATES, 4.5, 0.5, \"%\", \"Credit-card interest ranges\") + '</div>')",
  "h.append('<div class=\"chartbox\"><h4>Credit-card interest, % a month</h4>' + group_legend((\"us\", \"fc\", \"bank\")) +\n"
  "         range_svg(d.CARD_RATES, 4.5, 0.5, \"%\", \"Credit-card interest ranges\") +\n"
  "         '<p class=\"what\"><b>What this shows:</b> our 3.59% standard rate (3.25% premium) is below Finance House, Deem and Aafaq and inside the bank range. Al Ain Finance and Mawarid are cheaper.</p></div>')")

# scenarios: summary table, maths tables, chart captions
R("h.append('<h2 class=\"pb\">5. Real-life scenarios</h2><p>Numbers are computed with the policy rules (reducing-balance instalments unless flat). Names are illustrative.</p>')\n",
  "h.append('<h2 class=\"pb\">5. Real-life scenarios</h2><p>Numbers are computed with the policy rules (reducing-balance instalments unless flat). Names are illustrative.</p>')\n"
  "h.append('<table><thead><tr><th>Customer</th><th>Product</th><th>Outcome</th><th>Key number</th></tr></thead><tbody>')\n"
  "for nm, pr, oc, kn in sc.SUMMARY:\n"
  "    h.append('<tr><td><b>{}</b></td><td>{}</td><td class=\"{}\">{}</td><td>{}</td></tr>'.format(E(nm), E(pr), 'ok' if oc == 'Approved' else 'no', E(oc), E(kn)))\n"
  "h.append('</tbody></table>')\n")
R("    h.append('<dt>Result</dt><dd class=\"res\">{}</dd></dl></div>'.format(md_bold_to_html(s[\"result\"])))\n",
  "    h.append('<dt>Result</dt><dd class=\"res\">{}</dd></dl>'.format(md_bold_to_html(s[\"result\"])))\n"
  "    h.append('<table class=\"maths\"><thead><tr><th style=\"width:27%\">The maths</th><th>Working</th><th style=\"width:22%;text-align:right\">Result</th></tr></thead><tbody>')\n"
  "    for st, wk, rs in s[\"maths\"]:\n"
  "        h.append('<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(E(st), E(wk), E(rs)))\n"
  "    h.append('</tbody></table></div>')\n")
R("hbar_svg(rows, 70000, 10000, fmt_aed, \"Total interest comparison for Mariam\", label_w=200) + '</div>')",
  "group_legend((\"us\", \"fc\")) + hbar_svg(rows, 70000, 10000, fmt_aed, \"Total interest comparison for Mariam\", label_w=200) +\n"
  "                 '<p class=\"what\"><b>What this shows:</b> the same loan costs Mariam {} in interest with us, against {} at a typical finance company and {} at the top of the market.</p></div>'.format(aed(M_INT), aed(M_24_INT), aed(M_40_INT)))")
R("hbar_svg(rows, 200000, 50000, fmt_aedk, \"Total repayments for Khalid\", label_w=200) + '</div>')",
  "group_legend((\"us\", \"fc\", \"bank\")) + hbar_svg(rows, 200000, 50000, fmt_aedk, \"Total repayments for Khalid\", label_w=200) +\n"
  "                 '<p class=\"what\"><b>What this shows:</b> our buyout cuts what Khalid still has to pay by {}. A bank is cheaper still, but only if he moves his salary, and our cost comparison tells him so.</p></div>'.format(aed(K_OLD_TOT - K_NEW_TOT)))")

# sign-off list + data notes + sources renumbered
R("h.append('<h2 class=\"pb\">8. Sources</h2>",
  "h.append('<h3 class=\"pb\">Sign-off list: {} items ({} [A] adjusted, {} [P] proposals)</h3>'.format(len(SIGNOFF), N_A, N_P))\n"
  "h.append('<table class=\"cmp\"><thead><tr><th style=\"width:6%\">ID</th><th style=\"width:18%\">Item</th><th style=\"width:7%\">Tag</th><th>Policy value</th><th style=\"width:12%\">Rating</th></tr></thead><tbody>')\n"
  "for it in SIGNOFF:\n"
  "    h.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(it[1], E(it[2]), ' '.join('[{}]'.format(t) for t in it[7].split('/')), E(it[3]), chip(it[6])))\n"
  "h.append('</tbody></table><p class=\"small\">The policy text also marks two rules [P]: repricing when a salary account is moved without clearance (&sect;8.1) and the sector watch-list (&sect;7.5).</p>')\n"
  "h.append('<div class=\"keep\"><h2>8. Data notes and confidence</h2><ul>' + ''.join('<li>{}</li>'.format(md_bold_to_html(t_)) for t_ in DATA_NOTES) + '</ul></div>')\n"
  "h.append('<h2>9. Sources</h2>")

p.write_text(s, encoding="utf-8", newline="\n")
print("patch3 ok")
