---
title: 'domain research: Master rulebook (retail credit) US, UK, UAE + 4-bank comparison'
type: 'domain'
topic: 'Master rulebook (retail credit) US, UK, UAE + 4-bank comparison'
decision: "Build central-bank retail master rulebooks for US, UK, UAE and compare 4 banks per market (too rigid / in line / high risk) for Faisal's comparison tool"
source: 'run (+ UAE import from prior sourced research 2026-11-09)'
status: complete
preset: 'standard'
validation: 'normal'
created: '2026-11-12'
updated: '2026-11-12'
claims_verified: 4
claims_disputed: 1
---

# Domain research: retail master rulebook (US, UK, UAE) and 4-bank comparison

**Decision this research serves:** build the central-bank "master rulebook" for retail credit in the US, UK and UAE, and compare four real banks per market against it. This is Faisal's step 1. The labels are too rigid, in line, or higher risk.

## Executive summary

**Verdict: the comparison is buildable from public data for retail, and it has been built.** Deliverables:
- [Master Rulebook and Bank Comparison.xlsx](../../../../master-rulebook/Master%20Rulebook%20and%20Bank%20Comparison.xlsx): rulebooks plus a live comparison with formula labels.
- [Retail Bank Check - One-Pagers.pdf](../../../../master-rulebook/Retail%20Bank%20Check%20-%20One-Pagers.pdf): 12 banks, one page each.

Three findings drive how to use it:

1. **The three markets regulate in different ways, so the pitch differs by market.**
   - **UAE:** hard numbers. DBR 50%, 20x salary, 48 months, home LTV 85/80%, auto 80% / 60 months [U1]. The four UAE banks already lend at most of these limits (4 "at rule limit" measures each). They compete on salary entry level and price, so the useful advice is about entry criteria, pricing and segments, not "loosen the limits".
   - **US [1][2][3] and UK [8][9][10]:** mostly principles (ability to repay, affordability, Consumer Duty) with very few numeric caps. Almost every bank limit is the bank's own choice. This is where "you are too rigid / you take more risk than peers" adds most value.
2. **The rules moved in 2025–26, so the rulebook must be dated and refreshed.**
   - **US:**
     - SR 11-7 was replaced by SR 26-2 (17 Apr 2026) [4].
     - Reg B now removes disparate-impact liability (effective 21 Jul 2026, under court challenge) [5][6].
     - The CFPB withdrew its AI and BNPL guidance in May 2025 [7].
   - **UK:**
     - The per-lender 15% high-LTI cap was removed from 28 Oct 2026 [11][12].
     - BNPL has been regulated since 15 Jul 2026 [13].
     - Fully automated credit declines are allowed under the Data (Use and Access) Act 2025, with a right to human review [14].
3. **Public data covers terms well and risk appetite poorly.**
   - Banks publish rates, amounts, LTV and LTI, but not credit-score floors or internal policy.
   - Risk results (card charge-offs, Stage 3, book LTV) exist but are not like-for-like across banks [15][16].
   - The labels are therefore a conversation starter for a bank, not a verdict.

**Biggest caveat:** UK Lloyds terms and some HSBC/Barclays mortgage criteria rest on search extracts or trade press (M confidence). The US credit-card late-fee safe harbour is disputed [17].

## US rulebook (retail)
- **Full table:** 29 rows. Source: `digests/us-rules-r1-1.md` Part A, also in the xlsx "US rulebook" sheet.
- **No federal caps on:** personal-loan size, auto loans, or general rates. States set usury limits; national banks export their home-state rate. The Military Lending Act sets a 36% cap for service members [1].
- **Mortgages:**
  - No DTI cap since the 2021 General QM rule; QM status is a price test instead [2].
  - Fannie Mae's automated limit is DTI 50%.
  - QM limits the term to 30 years, with no negative amortisation, interest-only or balloon.
  - The 2026 conforming loan limit is $832,750 [3].
- **Cards:** ability-to-pay test, under-21 rules, limits on rate increases [1].
- **Fair lending:** adverse-action notices with specific reasons remain mandatory; disparate impact is removed [5][6].
- **Classification and model risk:** charge-off at 120/180 days (FFIEC 2000). Model risk now follows SR 26-2 [4].

## UK rulebook (retail)
- **Full table:** 17 rows. Source: `digests/uk-rules-r1-1.md` Part A, also in the xlsx "UK rulebook" sheet.
- **No caps on:** mainstream rates, loan size, LTV or term. The only hard price cap is for high-cost short-term credit: 0.8% a day, £15 default fee, 100% total cost [8].
- **Hard rules that exist:**
  - Card minimum payment of at least interest + fees + 1% [8].
  - Early-repayment compensation capped at 1% / 0.5% [9].
  - 14-day withdrawal right [9].
  - Mortgage affordability with a stress of at least +1 percentage point over 5 years (MCOB 11.6.18R) [10].
- **Mortgages:** the FPC market-wide limit stays (at most 15% of new mortgages at LTI ≥ 4.5x); the per-lender cap has gone [11][12].
- **BNPL:** regulated as deferred payment credit since 15 Jul 2026 [13].
- **Automated decisions:** allowed with safeguards [14].
- **Model risk:** PRA SS1/23 [10].

## UAE rulebook (retail)
- **Imported** from the 2026-11-09 sourced research; see `imports/`.
- **Hard caps:** DBR 50% (30% retirees); personal loans max 20x salary and 48 months; auto 80% LTV and 60 months; mortgage LTV 85/80% for a first home up to AED 5m (lower for higher values and second homes); 25 years; fee and late-fee caps [U1][U2].
- **Minimum salary rule:** its removal (Nov 2025) is press-reported only; verify against the CBUAE text.

## Four banks per market (what the comparison shows)
- **UAE (ENBD, FAB, ADCB, Mashreq) [U3]:**
  - All four lend at the 48-month, 85/80% LTV and 20%-down limits.
  - FAB is stricter on entry: personal-loan minimum salary 7,000 vs 5,000.
  - Mashreq prices highest (top personal-loan rate 31.99%, auto 3.19% flat) but has the lowest no-salary-transfer entry (AED 5,000).
  - ENBD is the loosest on amounts.
- **UK (HSBC UK, Barclays, Lloyds, NatWest) [15][18]:**
  - All lend to 95% LTV over 40 years.
  - NatWest allows the highest income multiple (6.5x for high earners) but is strictest on age (75 at end of term) and on non-residents (max 75% LTV).
  - Lloyds has the lowest book LTV (45%, group) and goes to 100% LTV with family support.
  - Personal-loan APRs are 6.8–7.9%; cards about 25%; the late fee is £12 at all four.
- **US (Chase, BofA, Wells Fargo, Citi) [16][19]:**
  - Chase and BofA offer no ordinary personal loan.
  - All four offer a 3% down mortgage (the investor limit).
  - Wells Fargo is loosest (personal loans to $100k / 84 months, 40-year mortgages outside QM) and has the highest card charge-off rate (3.73% in 3Q26).
  - Chase has the lowest charge-offs (2.91%).

## Cross-dimension insights
- **Rule style predicts where advice lands.** Where rules are numeric (UAE), banks bunch at the limits and the advice is about entry criteria, pricing and segments. Where rules are principles (US/UK), banks spread widely and the advice is "too rigid / too loose vs peers".
- **Looser terms line up with worse results in the US sample.** Wells Fargo is loosest on terms and worst on card charge-offs. Four banks are too few to prove a link, but it is exactly the "peel the onion" conversation Faisal described.
- **Regulatory direction differs.**
  - **US:** deregulating fair-lending and AI guidance.
  - **UK:** loosening mortgage LTI limits but tightening BNPL and keeping Consumer Duty.
  - **Effect on our AI score:** explainability and human review stay essential in both markets. US adverse-action reasons are still required; UK Arts 22A–22D require a human-review route.

## Recommendations
1. **Use the xlsx as the master tool and the PDF as the conversation starter** with a bank (confidence H for structure, M for some UK/US values). Feeds: product brief (positioning as "rulebook + peer check").
2. **Lead with US/UK banks for the "too rigid / too risky" pitch.** In the UAE, lead with entry criteria and pricing, since the limits are already maxed. Basis: the pattern holds across all 12 banks in the sample.
3. **Add a refresh cycle:** regulatory rows every 6 months, prices every 3 months (see staleness map). Feeds: PRD (data-refresh requirement).
4. **Next research runs, in Faisal's order:** finance houses (US/UK), then SME, then corporate. For SME and corporate, expect to rely on annual-report disclosures (sector exposure, NPL ratios), because banks do not publish those credit policies. Feeds: architecture (data sources).

## Open questions
- **Card late-fee safe harbour:** the exact US amount now in force [17]. Needs the Federal Register / court order text.
- **SR 26-2 scope:** whether it covers generative and agentic AI; secondary sources conflict. Read the primary letter [4].
- **Unconfirmed bank figures:** HSBC/Barclays maximum age (80) and Barclays personal-loan max and term have conflicting sources; Lloyds product pages blocked direct reading.
- **Risk results not like-for-like:** Stage 3 and days-past-due figures differ by basis. They need the same definition from Pillar 3 disclosures before ranking banks.
- **UAE minimum salary:** the removal needs the CBUAE text.

## Source appendix
| # | Supports | Publisher | Pub date | Accessed | Confidence |
|---|---|---|---|---|---|
| [1] | US consumer-credit rules (Reg Z cards, MLA, usury export) | [eCFR 12 CFR 1026.51 (and 32 CFR 232, 12 USC 85 in digest)](https://www.ecfr.gov/current/title-12/chapter-X/part-1026/subpart-G/section-1026.51) | 2026-11 | 2026-11-12 | H |
| [2] | General QM price test, ATR factors | [eCFR 12 CFR 1026.43](https://www.ecfr.gov/current/title-12/chapter-X/part-1026/subpart-E/section-1026.43) | 2026-11 | 2026-11-12 | H |
| [3] | 2026 conforming loan limit $832,750 | [FHFA](https://www.fhfa.gov/news/news-release/fhfa-announces-conforming-loan-limit-values-for-2026) | 2025-11 | 2026-11-12 | H |
| [4] | SR 26-2 supersedes SR 11-7 | [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm) | 2026-04 | 2026-11-12 | H |
| [5] | Reg B disparate-impact final rule, eff. 21 Jul 2026 | [Venable](https://www.venable.com/insights/publications/2026/05/cfpb-makes-significant-changes-to-regulation-b) | 2026-05 | 2026-11-12 | H |
| [6] | Same, plus litigation | [Husch Blackwell](https://www.huschblackwell.com/newsandinsights/cfpb-finalizes-major-regulation-b-overhaul-disparate-impact-out-discouragement-narrowed-and-spcps-restricted) | 2026-05 | 2026-11-12 | H |
| [7] | CFPB withdrawal of AI circulars and BNPL rule (May 2025) | [Federal Register 2025-08286](https://www.federalregister.gov/documents/2025/05/12/2025-08286/interpretive-rules-policy-statements-and-advisory-opinions-withdrawal) | 2025-05 | 2026-11-12 | M |
| [8] | UK CONC: HCSTC cap, card minimum payment | [FCA CONC sourcebook PDF](https://api-handbook.fca.org.uk/files/sourcebook/CONC.pdf) | 2026-07 | 2026-11-12 | H |
| [9] | CCA s.66A withdrawal, s.95A compensation | [CCA 1974 s.66A](https://www.legislation.gov.uk/ukpga/1974/39/section/66A) / [s.95A](https://www.legislation.gov.uk/ukpga/1974/39/section/95A) | current | 2026-11-12 | H |
| [10] | MCOB affordability +1pp stress; PRA SS1/23 | [FCA MCOB sourcebook PDF](https://api-handbook.fca.org.uk/files/sourcebook/MCOB.pdf) / [PRA SS1/23](https://www.bankofengland.co.uk/prudential-regulation/publication/2023/may/model-risk-management-principles-for-banks-ss) | 2026-06 | 2026-11-12 | H |
| [11] | Per-lender LTI flow cap removed 28 Oct 2026 | [Bank of England PS19/26](https://www.bankofengland.co.uk/prudential-regulation/publication/2026/october/high-loan-to-income-lending-policy-statement) | 2026-10 | 2026-11-12 | H |
| [12] | Same (second source) | [Mortgage Solutions](https://www.mortgagesolutions.co.uk/mortgage-news/2026/10/14/fca-and-pra-confirm-permanent-removal-of-high-lti-mortgage-cap/) | 2026-10 | 2026-11-12 | M |
| [13] | BNPL (DPC) regulated from 15 Jul 2026 | [FCA PS26/1](https://www.fca.org.uk/publications/policy-statements/ps26-1-regulation-deferred-payment-credit) | 2026-02 | 2026-11-12 | H |
| [14] | Automated decisions Arts 22A–22D (DUAA 2025) | [DUAA 2025 s.80](https://www.legislation.gov.uk/ukpga/2025/18/section/80) | 2025-06 | 2026-11-12 | M |
| [15] | UK bank terms and risk data | `digests/uk-banks-r1-1.md` (57 URLs: bank pages, intermediary criteria, annual reports) | 2025–26 | 2026-11-12 | M/H |
| [16] | US bank terms and 3Q26 risk data | `digests/us-banks-r1-1.md` (43 URLs: product pages, card agreements, 3Q26 earnings) | 2026 | 2026-11-12 | H |
| [17] | Card late-fee safe harbour in dispute | [Husch Blackwell](https://www.huschblackwell.com/newsandinsights/cfpb-drastically-cuts-credit-card-late-fee-safe-harbor-amount) / [PolicyRisk](https://policyrisk.com/wiki/credit-card-late-fee-cap) | 2024–26 | 2026-11-12 | L/M |
| [18] | NatWest LTI grid, age, non-resident rules | [NatWest intermediary affordability](https://www.intermediary.natwest.com/intermediary-solutions/affordability.html) | 2026 | 2026-11-12 | M/H |
| [19] | Wells Fargo personal loan terms | [Wells Fargo](https://www.wellsfargo.com/personal-loans/) | 2026 | 2026-11-12 | H |
| [U1] | UAE retail caps (Reg 29/2011, mortgage regulation) | `imports/uae-01-benchmark-conventional.md` (CBUAE sources) | 2011–2025 | 2026-11-09 | H/M |
| [U2] | UAE market and FSR 2025 caps | [CBUAE FSR 2025](https://centralbank.ae/media/0hve4xxg/fsr-2025-en.pdf) | 2025 | 2026-11-09 | H |
| [U3] | UAE bank terms | `imports/banks_core.csv` (bank URLs per row) | 2026 | 2026-11-09 | H/M/L |

## Staleness map
Computed with `recon_kit.py staleness` (windows: regulatory 6 months, pricing 3 months, player data 6 months). Every regulatory row was checked as current on 2026-11-12, so "stale by publication date" means re-check on the next refresh, not that the row is wrong today.

| Claim | Re-check by |
|---|---|
| US card late-fee safe harbour | 2026-11 (overdue: still disputed) |
| SR 26-2, Reg B disparate impact (litigation) | 2026-10 (re-check on next refresh) |
| UK BNPL regime | 2026-08 (re-check on next refresh) |
| Bank product terms and APRs (all markets) | 2027-02 |
| Bank risk results | 2027-04 |
| UK per-lender LTI change | 2027-04 |

**Earliest:** the US card late-fee safe harbour, which is already due.
