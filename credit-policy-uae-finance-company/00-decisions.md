# Pilot Finance Company Retail Credit Policy: Decisions Log

Started 2026-11-09. Track B of the conventional work (Track A, the conventional bank policy, is in `../credit-policy-uae-conventional/`).

## Request
"We are creating a credit risk criteria and lending policy for a **pilot finance company** in the UAE."

## Decisions from the user (round 1, 2026-11-09)
| ID | Decision |
|---|---|
| FC-1 | The pilot finance company is **conventional** |
| FC-2 | Build **both** policies: the conventional bank policy (Track A) and this finance-company policy (Track B) |
| FC-3 | Compare the finance-company policy with: **UAE finance companies**, the **top five retail banks**, and **digital / BNPL lenders** |
| FC-4 | Products, subject to the CBUAE licence: personal finance (employer-assigned and non-assigned, buyout, top-up); auto; cards / salary advance / BNPL; home and asset-backed |

## Working assumptions (need management sign-off)
These are not user decisions. They are the defaults this package uses. Change any of them and the policy, parameter sheet and config change with it.

| ID | Assumption | Why | Sign-off |
|---|---|---|---|
| A-01 | **Licence:** Finance Companies Regulation (FCR, Circular C 3/2023 as amended) **Part I full finance company**, conventional only (no Islamic window). Retail finance activities: personal loans, credit cards, vehicle loans, short-term credit | Covers every pilot product except home finance | ☐ |
| A-02 | **Capital:** paid-up capital **AED 150m** (the regulatory minimum); capital funds taken as AED 150m for every limit | All prudential limits scale with capital funds | ☐ |
| A-03 | **Pilot book cap:** gross retail loans **≤ AED 250m** in licence years 0–2 | Leverage ≤ 100% of capital funds means total assets ≤ about AED 300m; less a 10% liquidity buffer and fixed assets | ☐ |
| A-04 | **Phase 1 products:** personal loans (employer-assigned and non-assigned, buyout, top-up), credit cards, auto loans, gold-backed loans, salary advance. **Phase 2:** own BNPL, and home finance only if the licence covers mortgage finance | Each new product line needs a CBUAE no-objection letter | ☐ |
| A-05 | **Not offered:** deposit-backed loans and overdrafts | Finance companies cannot take deposits from or hold accounts for individuals | ☐ |
| A-06 | **Collection model:** the company cannot hold salary accounts, so "salary transfer" becomes an **employer salary-assignment letter + irrevocable EOS undertaking + UAEDDS direct debit** on the customer's salary account. A WPS-agent payroll-card route is optional and needs its own approval | Keeps the security of a salary-assigned loan without a bank account | ☐ |
| A-07 | **Starting point:** the recommended bank criteria (tag [B]), unchanged unless FCR or the finance-company market requires a change (tag [A]) | Bank-grade credit discipline with finance-company reach | ☐ |
| A-08 | **Pricing position:** below the finance-company typical (20–28%) and above banks; risk-based by AI grade | Better risk selection funds a lower price; funding costs keep it above banks | ☐ |
| A-09 | **Benchmark set:** finance companies (Finance House, Deem, Al Ain Finance, Aafaq, Mawarid, Siraj, botim / CashNow, e& easyCredit), BNPL (Tamara, Tabby), top five conventional banks (Emirates NBD, FAB, ADCB, Mashreq, RAKBANK) | FC-3 | ☐ |
| A-10 | **Regulatory confidence:** the FCR rulebook returned HTTP 403, so FCR article numbers and values are from search extracts (confidence M). Legal & Compliance must confirm them before adoption | See `01-regulation-and-benchmark.md`, "Gaps to close" | ☐ |

## Outputs (this folder)
| File | What it is |
|---|---|
| 01-regulation-and-benchmark.md | Research: FCR rules, finance-company list, product tables, benchmark |
| 03-parameter-sheet.md | 60 policy items rated against the finance-company market (single source of truth) |
| 04-benchmark-gap-report.md + PDF | Simple benchmark and gap report with charts and real-life scenarios |
| 05-retail-credit-policy.md + PDF + DOCX | Retail Credit Policy: UAE Finance Company v0.1 |
| config/ | Executable rules and parameters for the AI Risk Score Card, with a validator |
