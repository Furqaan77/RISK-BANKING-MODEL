---
title: Income-Based Customer Segmentation Spec
product: AI Risk Score Card Global (US + UK)
created: 2026-11-07
status: final
decided_by: product owner (fixed salary bands; Global only; spec + walkthrough chapter + banker PDF section + graphs incl. pie charts)
binds: [FR-79..FR-86]
---

# Income-Based Customer Segmentation (US + UK)

All figures are **demo-bank defaults**: illustrative, configurable per bank, effective-dated, and maker-checker controlled. The regulator
packs always take priority. Every limit below is the *most* the segment allows; the final limit is the **lowest** of segment cap,
product cap, affordability / ability-to-pay result and any regulatory cap.

## 1. Segment definition

**Basis:** applicant's **annual gross income from verified sources** (payroll/employer verification, Open Banking or account cash flow,
tax data, bureau income tools).
- **Irregular income** (shift, gig, seasonal, self-employed): smoothed 12-month average of verified credits, with a volatility penalty.
- **Joint applications:** combined verified income.
- **Self-declared income alone never sets the segment.** The UK requires independent evidence (CONC 5.2A.16). The US must consider income and assets (CARD Act).

| Segment | US gross income (USD/yr) | UK gross income (GBP/yr) | Monthly equivalent (US / UK) |
|---|---|---|---|
| **S0 No verified income** | none verified | none verified | n/a |
| **S1 Entry** | < 30,000 | < 20,000 | < $2,500 / < £1,667 |
| **S2 Core / blue-collar** | 30,000 – 59,999 | 20,000 – 34,999 | $2,500–5,000 / £1,667–2,917 |
| **S3 Middle** | 60,000 – 119,999 | 35,000 – 59,999 | $5,000–10,000 / £2,917–5,000 |
| **S4 Upper-middle** | 120,000 – 249,999 | 60,000 – 99,999 | $10,000–20,833 / £5,000–8,333 |
| **S5 High** | ≥ 250,000 | ≥ 100,000 | ≥ $20,833 / ≥ £8,333 |

**Overlay tags** change how the customer is assessed, not their segment:

| Tag | Applies when | Effect |
|---|---|---|
| `GENZ` | Age 18–25 | Credit-builder path, smart limits, starter products |
| `THIN_FILE` | < 3 bureau tradelines or < 12 months of history | Starter caps; cash-flow/inclusion features weighted |
| `GIG_SELF_EMPLOYED` | ≥ 30% of income from platforms or self-employment | Smoothed income + volatility penalty; 2 years of evidence for mortgages |
| `RETIREE` | Pension is the main income | Pension income only; UK foreseeable change; US ATR on assets |
| `NEW_TO_COUNTRY` | < 24 months of local history | Thin-file treatment; no immigration-status feature (NY 296-a) without legal review |
| `UNDER_18_READINESS` | Age 16–17 | **No credit**; readiness record only (FR-39) |

**Re-segmentation:** recalculated in the nightly run.
- Moving **up** takes effect after 2 consecutive verified months.
- Moving **down** takes effect after 3 consecutive months (avoids one-month shocks). An immediate drop applies only on verified job loss or redundancy.
- Every change is logged. Limit decreases follow the bank's notice rules (US Reg Z change-in-terms; UK CONC).

## 2. Segment policy matrix (demo defaults)

| Policy item | S0 | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|
| Eligible products | secured card; credit-builder loan | + starter card; salary advance; small personal loan | + standard card; personal loan; auto | + mortgage; rewards card; HELOC (US) / second charge (UK) | + large mortgages (US jumbo); premium card | + private-bank / Lombard; bespoke |
| Card limit range US | secured ($200–500, deposit-backed) | $300–1,500 | $1,500–5,000 | $5,000–15,000 | $15,000–30,000 | $30,000+ |
| Card limit range UK | secured (£200–500) | £250–1,000 | £1,000–3,000 | £3,000–8,000 | £8,000–15,000 | £15,000+ |
| Personal loan max US / UK | — | $5k / £3k | $15k / £10k | $40k / £25k | $75k / £50k | $100k / £75k |
| Max DTI (US bank policy) | — | 35% | 40% | 43% | 45% | 50% |
| Min residual income / month after repayment: **loans & mortgages** (US / UK) | — | $600 / £150 | $800 / £200 | $1,200 / £300 | $2,000 / £500 | $3,000 / £800 |
| Min residual income / month after minimum payment: **cards & salary advance** (US / UK) | $300 / £100 | $300 / £100 | $300 / £100 | $300 / £100 | $300 / £100 | $300 / £100 |
| Salary advance cap (≤ 50% net pay) | — | $1,000 / £750 | $2,000 / £1,500 | $3,000 / £2,000 | not offered | not offered |
| UK mortgage LTI max (bank policy, within FPC 4.5x flow monitoring) | — | — | 4.0x | 4.5x | 4.5x (5.0x professionals) | 5.5x (case-by-case) |
| Automation allowed | no | starter products ≤ $/£1,000 & grade ≤ 12 | starter products ≤ $/£1,000 & grade ≤ 12 | cards ≤ $/£5,000 & grade ≤ 10 | human only | human only |
| Never auto-decline | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Limit growth reviews | 6 months (move to unsecured) | 6 & 12 months | 6 & 12 months | 12 months | 12 months | on request |
| Key risks | no income history | income volatility, payday reliance | redundancy, sector layoffs | over-borrowing, mortgage rate shock | large exposures, lifestyle above income | complex income, bonus cuts, fraud/AML referral |
| Early-warning emphasis | — | salary delays, payday/BNPL stacking, gambling | sector layoffs, overtime drop, utilisation | rate resets, utilisation, BNPL | spend > income, luxury spikes | bonus/investment drops, large transfers |
| Hardest stress scenario | — | recession / job loss | recession / sector layoffs | rate shock (+3pp) | rate shock + house prices | market crash (−30% equities) |

## 3. How segmentation is used in the decision (order of steps)
1. Verify income → compute gross annual and net monthly (smoothed where needed).
2. Assign the segment and overlay tags.
3. Apply the **regulator pack** (always first).
4. Apply segment policy: eligible products, caps, DTI/residual-income minimums, automation rule.
5. Run affordability (UK) / ability-to-pay (US) with the segment's minimum-residual requirement.
6. Score risk (PD/LGD/EAD/EL). **Income band is not a scoring penalty by itself.** The model uses behaviour, affordability and stability features. Segment-level calibration checks that PD is accurate within each band.
7. Limit = lowest of all caps; name the binding constraint.
8. Automation check (segment rule + grade). Declines always go to a person.

**Worked examples**
- **Maria (NY):** smoothed net $3,400/month ≈ $48k gross → **S2** + `THIN_FILE` + `GIG_SELF_EMPLOYED`.
  - S2 card range is $1,500–5,000, but the thin-file starter cap of **$1,500** is lower and binds.
  - Card residual check: $560 − $45 minimum payment = $515 ≥ $300 floor → pass. CARD Act ability-to-pay also passes.
  - The card is $1,500, above the $1,000 automation line, so it goes to an underwriter.
- **Tom (London):** net £1,650/month ≈ £24k gross → **S2** + `GENZ` + `THIN_FILE`.
  - Starter card £1,000 is within the S2 starter range.
  - Residual after the £42.40 repayment is £453 ≥ £100 floor → pass.
  - Auto-approved (≤ £1,000, grade 12) with Art 22C information.
- **Loan example (illustrative):** a US S3 customer earning $90k gross ($5,600 net/month) with $1,900 of existing obligations asks for a $30,000 loan over 60 months at 12% APR.
  - Instalment ≈ $667. DTI = (1,900 + 667) ÷ 7,500 gross monthly = 34% ≤ 43% → pass.
  - Residual = 5,600 − 1,900 − 667 − essentials 1,800 = $1,233 ≥ $1,200 S3 floor → pass, just. The binding constraint is minimum residual income.

## 4. Fairness and conduct safeguards
- Income segment is **not** a protected characteristic, but it can act as a proxy. Fairness suites (FR-50/51) report approval rate,
  average limit, APR and decline reasons **by segment × protected-group proxy**, and require a documented business justification for differences.
- UK Consumer Duty: outcome MI by segment, with a fair-value check that lower-income segments don't pay disproportionate fees.
- No "income-only" knockouts other than S0 product eligibility and regulatory minimums. S0 customers get a path (secured card / credit-builder), not a dead end.
- Marketing and next-best-offer respect segment eligibility, affordability first, and never promote credit to minors.

## 5. Demo portfolio (synthetic, illustrative; used for charts)

| Segment | US customers % (2M) | US balances % | UK customers % (1M) | UK balances % | Avg 12m PD US | Avg 12m PD UK |
|---|---|---|---|---|---|---|
| S0 | 3 | 0.5 | 3 | 0.5 | — (secured) | — (secured) |
| S1 | 18 | 6 | 20 | 7 | 6.0% | 5.5% |
| S2 | 30 | 20 | 32 | 22 | 3.5% | 3.2% |
| S3 | 30 | 35 | 28 | 34 | 1.8% | 1.7% |
| S4 | 14 | 25 | 12 | 23 | 1.0% | 1.0% |
| S5 | 5 | 13.5 | 5 | 13.5 | 0.7% | 0.8% |

**Approval rate, champion vs challenger (illustrative, US cards):**
- S1: 38% → 47%
- S2: 55% → 63%
- S3: 74% → 77%
- S4: 86% → 87%
- S5: 91% → 91%

The gains concentrate where inclusion features help.

**Expected-loss uplift under stress (illustrative, % of segment EL; bigger number = harder hit):**

| Scenario | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
| Recession | +60% | +55% | +35% | +25% | +20% |
| Rate shock +3pp | +20% | +25% | +40% | +45% | +20% |
| Market crash | +10% | +10% | +15% | +30% | +55% |

## 6. Requirements added to the PRD
FR-79 to FR-86 (see `prd.md` §4.15).
