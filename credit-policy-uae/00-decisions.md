# UAE Islamic Bank: Retail Credit Policy Project: Decisions Log

Started 2026-11-09. Product: AI Risk Score Card (UAE Islamic edition). Goal: draft a retail credit policy (secured + unsecured)
from the user's basic criteria, benchmark it against the top five UAE retail banks (plus Islamic peers), rate how close it is,
and recommend improvements so it matches the top five while staying safe.

## Decisions (round 1)
- **Products in scope:**
  - Unsecured: personal finance (Tawarruq/Murabaha; salaried & self-employed); Islamic credit cards
  - Secured: home finance (Ijara / Diminishing Musharaka); auto finance (Murabaha/Ijara); cash/deposit-, gold- and EOSB-backed finance; salary advance
  - **Salary-assigned finance:** secured by the employer's salary transfer commitment (salary transfer letter + EOSB undertaking/employer liability letter)
  - **Buyout facility:** takeover of finance from other banks, incl. top-up rules
- **Benchmark set:** top 5 UAE retail banks overall (ranking confirmed from annual reports) + their Islamic arms shown separately
- **Positioning:** competitive but safe: at or slightly better than the market median for customers, never looser than CBUAE, stronger risk controls (AI score, DBR on basic + housing)
- **Outputs:** credit policy document (PDF); benchmark & gap report (user criteria vs top 5, near/far rating, improvements); model config YAML (demo bank rule files); Word (.docx) editable policy

## Inputs
- User's basic criteria: pending (to be pasted)
- Public bank criteria: research running (unsecured; secured + top-5 ranking)
- CBUAE rules: docs/regulatory/cbuae-rules.md

## User's basic criteria (received 2026-11-09)
| Item | User criterion | How it will be applied |
|---|---|---|
| Who can apply | UAE nationals and expats | Both, in all products |
| Minimum salary | AED 5,000 (nationals and expats) | All products unless the benchmark shows a product needs more (e.g. home finance) → flagged as a gap, not changed silently |
| Age min/max | "UAE Central Bank limit" | **CBUAE sets no age limit for personal finance and abolished the mortgage age cap in 2019** → use the top-5 market median, marked *proposed* |
| Minimum length of service | 3 months | All salaried products |
| Salary transfer | Not required | Two variants: **salary-assigned (with STL + EOS undertaking) = secured/quasi-secured**, and **without salary transfer = unsecured** |
| Employer categories | All accepted | No employer exclusion; employer category still used for pricing/limits/risk |
| Max finance amount & term | Not given | CBUAE caps: personal finance 20× monthly income, 48 months; auto 60 months; home 25 years |
| DBR | "Take it from UAE Central Bank limits" | **50% of gross salary + regular income (CBUAE Reg 29/2011 Art 7); retirees 30%.** This replaces the earlier demo assumption of basic + housing for this policy; the gap report shows both |
| Pricing | Mid range of the market | Profit rates, processing fee, early settlement = market median (early settlement within the CBUAE cap: 1% / max AED 10,000) |
| Secured vs unsecured personal finance | "Secured against salary; unsecured without salary transfer" | Salary-assigned finance treated as quasi-secured (better pricing/limits); non-STL as unsecured |
| Home finance | CBUAE | LTV 85/80% first home ≤ AED 5m (nationals/expats), 75/70% > AED 5m, 65/60% second home, 50% off-plan; max 25 years; DBR 50% |
| Auto finance | Mid range of the market | Down payment (CBUAE minimum 20%), car age limits, tenor ≤ 60 months: market median |
| Deposit / gold / EOSB-backed | Lend 90% of security value | Applied as given; gap report checks it against market practice and risk (gold price volatility, EOSB contingency) |
| Salary-assigned & buyout | Salary transfer confirmation + end-of-service undertaking | Required for salary-assigned finance and for buyouts on that basis; top-up after ≥ 12 months clean repayment (CBUAE Art 6(g)); transfer fee ≤ 1% / AED 10,000 |
| Self-employed / other | Last 12 months' bank statements + financials if possible | Applied to self-employed and to non-STL applicants; AECB thresholds and restricted lists = proposed from market |

## Outputs (2026-11-09)
| File | What it is |
|---|---|
| 01-benchmark-unsecured.md | Top-five + Mashreq/RAKBANK published criteria: personal finance, cards (sources, confidence) |
| 02-benchmark-secured.md | Top-five ranking + home, auto, deposit/gold/EOSB-backed criteria |
| 03-parameter-sheet.md | Single source of truth: 54 items, user criterion vs top five, rating, recommended value |
| 04-benchmark-gap-report.md + PDF | Benchmark & gap report (19 pages): 31 near / 17 slightly off / 6 far; how to close; 8 sign-off items |
| 05-retail-credit-policy.md + PDF + DOCX | Retail Credit Policy v0.1 (12 pages), recommended values, [A]/[P] markers |
| config/ | bank_policy.yaml, credit_policy.yaml, rules.yaml (65 rules), README, validate_config.py (37 pass, 2 flagged, 0 fail) |

## Pending user sign-off ([A] items)
P-04 service, P-06 employer tiers, P-10 statements, P-21 unsecured minimum salary, P-31 home finance minimum salary, P-39 home finance service/age, P-52 gold 70%, P-53 EOSB 80%.
