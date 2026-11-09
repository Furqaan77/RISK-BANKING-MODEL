# UAE Conventional Retail Credit Policies: Decisions Log

Started 2026-11-09.

## Requests
1. "Prepare the same retail credit risk policy for a **conventional bank** in the UAE; keep the same credit criteria as we recommended, based on UAE Central Bank rules, and compare with the top conventional banks in the UAE."
2. Mid-task context: "We are creating credit risk criteria and a lending policy for a **pilot finance company** in the UAE."

## Decisions (round 1, 2026-11-09)
- **FC-1:** the pilot finance company is **conventional**.
- **FC-2:** **build both**: (a) the conventional **bank** policy and (b) the conventional **finance-company** policy.
- **FC-3:** the finance-company policy is compared with: UAE finance companies; the top 5 retail banks; digital / BNPL lenders.
- **FC-4:** finance-company products, subject to its CBUAE licence: personal finance (salary-assigned + non-STL, buyout, top-up); auto finance; cards / salary advance / BNPL; home & asset-backed (home, gold, EOSB). Deposit-backed lending is unlikely because finance companies generally cannot take deposits; to be confirmed by the regulatory research.

## Track A: Conventional bank policy (this folder)
- **Credit criteria:** identical to the recommended Islamic policy (`../credit-policy-uae/03-parameter-sheet.md`, including the 8 [A] adjustments).
- **Conventional conversion** (structure and pricing language only):
  - Murabaha / Tawarruq → personal loan; IMBT / Istisna'a → conventional mortgage; auto Murabaha → auto loan; rahn → pledge / lien; profit rate → interest rate.
  - Late payment: charity → **fee retained as income**, at the conventional market median.
  - Early settlement: 1% of outstanding, max AED 10,000 + VAT (no Ibra).
  - Takaful → credit life and property / motor insurance.
  - No Sharia committee.
  - Deposit-backed: loan **or overdraft** against fixed deposit.
- **Benchmark:** top five **conventional** UAE retail lenders: Emirates NBD (conventional), FAB, ADCB, Mashreq, RAKBANK. Islamic arms are excluded. CBD is not ranked (retail split not disclosed).
- **Data:** the 9-Nov-2026 research in `../credit-policy-uae/01-benchmark-unsecured.md` and `02-benchmark-secured.md` (conventional products only).
- **Outputs:** parameter sheet; policy (MD + PDF + DOCX); benchmark & gap report (MD + PDF); config YAML.
- **AI Risk Score Card note:** the UAE edition uses Islamic vocabulary only in v1 (PRD B1b, AD-12). Loading conventional configs needs a vocabulary switch or a conventional tenant profile.

### Track A outputs (2026-11-09): complete
| File | What it is |
|---|---|
| 01-benchmark-conventional.md | Top five conventional lenders: ranking + product tables |
| 03-parameter-sheet.md | 55 items: 46 Near, 4 Lenient edge, 5 No peer product, 1 n/a |
| 04-benchmark-gap-report.md + PDF | Benchmark & gap report (18 pages) |
| 05-retail-credit-policy.md + PDF + DOCX | Conventional Retail Credit Policy v0.1 (12 pages) |
| config/ | 70 rules; validation 48 pass, 2 flagged (MoD 60 months, 30-yr rate relief), 0 fail; vocabulary_profile: conventional |

## Track B: Pilot finance company policy (`../credit-policy-uae-finance-company/`)
- Waiting on research: CBUAE Finance Companies Regulation; UAE finance companies' retail criteria; digital / BNPL lenders.
- Starting point: the same recommended criteria, adjusted to finance-company rules and that market.
