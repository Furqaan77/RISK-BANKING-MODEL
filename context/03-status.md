# 03. Status: what is built (as of 13 Nov 2026)

| # | Item | Where | State |
|---|---|---|---|
| 1 | UAE Islamic edition: plan, build prompt, banker PDF | `BMAD-BUILD-PROMPT.md`, `BUILD-PLAN.md`, `AI Risk Score Card - Plan for Bank Leadership.pdf` | Done |
| 2 | Global edition (US+UK): plan, build prompt, 81-page pack | `BMAD-BUILD-PROMPT-GLOBAL.md`, `BUILD-PLAN-GLOBAL.md`, `AI Risk Score Card Global - *.pdf` | Done |
| 3 | Retail credit policy, UAE Islamic bank | `credit-policy-uae/` | Done (sign-offs open) |
| 4 | Retail credit policy, UAE conventional bank + market position vs 33 banks | `credit-policy-uae-conventional/` | Done |
| 5 | Retail credit policy, UAE finance company (pilot) | `credit-policy-uae-finance-company/` | Done: 129 rules; validator 73/76 pass, 3 flags |
| 6 | **Master rulebook + 12-bank comparison** (mentor's step 1) | `master-rulebook/` | Retail done with live Excel labels; finance houses, SME and corporate rulebooks added; wholesale bank data not like-for-like, so no labels |
| 7 | Research run 1: retail US/UK/UAE | `_bmad-output/planning-artifacts/research/domain-master-rulebook-retail-credit-us-uk-uae-2026-11-12/` | Complete |
| 8 | Research run 2: finance houses, SME, corporate | `_bmad-output/planning-artifacts/research/domain-master-rulebook-fh-sme-corporate-us-uk-uae-2026-11-13/` | Digests done; **`research.md` summary not written** |
| 9 | **Platform blueprint v1** | `_bmad-output/planning-artifacts/blueprint/` (md + PDF) | Done |
| 10 | **Working skeleton** | `risk-platform/` | Runs end to end; **9/9 planted problems found, 6/6 tests pass** |
| 11 | Handoff docs | `CLAUDE.md`, `HANDOFF.md`, `README.md`, `SHIFT-PROMPT.md`, `context/` | Done |

## The master rulebook in short
- **Excel:** `master-rulebook/Master Rulebook and Bank Comparison.xlsx`. It holds rulebooks per country, comparison sheets with formula labels, a bank summary, settings (5% band), 379 sources, and finance-house / SME / corporate sheets.
- **Banks:**
  - UAE: Emirates NBD, FAB, ADCB, Mashreq.
  - UK: HSBC UK, Barclays, Lloyds, NatWest.
  - US: JPMorgan Chase, Bank of America, Wells Fargo, Citi.
- **Labels:** Too rigid / Higher risk / In line (vs the peer median ±5%); At rule limit / Above rule limit (vs the regulator); Cheaper / More expensive; Better / Worse.
- **One-pagers:** `Retail Bank Check - One-Pagers.pdf` (13 pages).
- **Rebuild:** `python tools/master-rulebook/build.py` (needs openpyxl, and Chrome for the PDF).

## Key regulatory facts found (checked with a second source; still "verify" before client use)
- **US:**
  - SR 26-2 replaced SR 11-7 for model risk (17 Apr 2026).
  - Reg B disparate-impact change effective 21 Jul 2026 (under litigation).
  - The card late-fee safe harbor is disputed.
  - SBA SOP 50 10 8.1 (DSCR 1.15).
  - Section 1071 small-business data from 1 Jan 2028.
- **UK:**
  - The per-lender 15% loan-to-income flow limit was removed 28 Oct 2026 (PS19/26); the FPC aggregate limit stays.
  - BNPL regulated from 15 Jul 2026 (PS26/1).
  - Growth Guarantee Scheme 70% / £2m.
- **UAE:**
  - C 1/2023 large exposures; C 3/2024 credit risk.
  - 1.5% provision floor.
  - SME Circular 2/2026.
  - Retail DBR 50%; personal loan 20× salary / 48 months; mortgage LTV 85/80; auto 80.
- **All three markets:** single-borrower limit ~25% of Tier 1 (US national banks: 15% + 10%).

## The skeleton's demo bank
- **"Demo Group":**
  - UAE01: AED, equity 6bn.
  - UK01: GBP, 900m.
  - US01: USD, 1.5bn.
- About 1,800 customers, 1,805 facilities and 203 applications. All data is **synthetic**.
- **9 planted problems (P1–P9).** For example, P1 is the Falcon Holdings group over its limit (USD 490m vs 408m); P9 is a bank rule looser than the regulator (DBR 55 vs 50).
