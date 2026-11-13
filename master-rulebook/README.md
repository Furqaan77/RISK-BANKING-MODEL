# Master Rulebook and Bank Comparison (Faisal's step 1)

Retail comparison with live labels, plus finance houses, SME and corporate rulebooks and bank data. US / UK / UAE, public data as of 12–13 November 2026.

| File | What it is |
|---|---|
| `Master Rulebook and Bank Comparison.xlsx` | **The tool.** Rulebook per country, comparison per country with live labels, bank summary, settings, sources |
| `Retail Bank Check - One-Pagers.pdf` | Cover page plus one page per bank (12 banks), with "what we would tell this bank" |
| `update-for-tanveer.md` | Plain-language update on what Faisal asked for and our plan |
| `data/compare_*.csv` | The comparison values. Edit these, then rebuild |
| `data/rulebook_*.csv` | Rulebook tables (US/UK extracted from the research; UAE from earlier research) |

**Banks compared:**

| Country | Banks |
|---|---|
| UAE | Emirates NBD, FAB, ADCB, Mashreq |
| UK | HSBC UK, Barclays, Lloyds, NatWest |
| US | JPMorgan Chase, Bank of America, Wells Fargo, Citi |

**Labels:**
- **Too rigid / Higher risk:** stricter or looser than the median of the four banks, by more than 5%.
- **At rule limit / Above rule limit:** compared with the regulator's number.
- **Cheaper / More expensive:** for rates and fees.
- **Better / Worse:** for results such as charge-offs.

Change the 5% on the Settings sheet; the labels in the spreadsheet update by themselves.

**Rebuild after editing data:** `python tools/master-rulebook/build.py`. It needs openpyxl, and Chrome for the PDF.

**Research behind it (BMAD deep recon):** `_bmad-output/planning-artifacts/research/domain-master-rulebook-retail-credit-us-uk-uae-2026-11-12/`. That folder holds:
- `research.md`, the summary
- `digests/`, the four research files with about 180 source links
- `.memlog.md`, the decisions and checks

**Next, in Faisal's order:** finance houses (US/UK), then SME, then corporate.
