# Retail Credit Policy: Parameter Sheet (single source of truth)

**Basis:** UAE Islamic bank retail credit policy v0.1, built from the user's basic criteria and benchmarked against the **top five UAE retail banks** by retail financing book (FY2025 / 3Q26):
1. Emirates NBD (incl. Emirates Islamic)
2. ADIB
3. FAB (incl. FAB Islamic)
4. DIB
5. ADCB (incl. ADCB Islamic)

Mashreq and RAKBANK are extra reference points. Benchmark data: `01-benchmark-unsecured.md`, `02-benchmark-secured.md` (checked 2026-11-09). The policy document, gap report and model YAML are all generated from this sheet.

**Ratings** (user criterion vs top five):
- **Near:** within the top-five range, at or close to the median.
- **Slightly off:** inside the range but at an edge, or only partly specified.
- **Far:** outside the top-five range, no market precedent, or missing where it matters.

**Source tags for the recommended value:**
- **[U]** user criterion kept as given
- **[C]** CBUAE rule
- **[M]** top-five median
- **[P]** proposed by us (no clear market figure)
- **[A]** adjusted from the user criterion to match the top five (needs user sign-off)

Rates are reducing-balance unless marked flat. Fees exclude 5% VAT unless stated.

## 1. General (all products)
| ID | Item | User criterion | Top-five benchmark (lenient / typical / conservative) | Rating | Recommended policy value |
|---|---|---|---|---|---|
| P-01 | Eligible customers | UAE nationals and expats | All five lend to both | Near | Nationals and UAE-resident expats [U]. Non-residents out of scope for v1 [P] |
| P-02 | Minimum age | "CBUAE limit" (CBUAE sets **none** for personal finance) | 18 (ADCB/DIB home) / **21** / 21 | Slightly off | **21** for all products [M] |
| P-03 | Max age at maturity | "CBUAE limit" (none; mortgage cap abolished 2019) | PF: 70 / **65 nationals, 60 expats** / 60. Home: 70 for all / **70 nationals & self-employed, 65 salaried expats** / 60 | Slightly off | Personal finance, cards, auto: **65 nationals / 60 expats** [M]. Home: **70 nationals and self-employed / 65 salaried expats** [M]. Retirees: pension-based finance to 70 (nationals) [M] |
| P-04 | Minimum length of service | 3 months | none (ENBD) / **6 months** (FAB, Mashreq) / 18 months (FAB Islamic non-STL) | Near (STL) / Slightly off (non-STL, home) | Salary-assigned: **3 months** [U]. Non-STL: **6 months** [A]. Home finance: **6 months and probation completed** [A] |
| P-05 | Salary transfer | Not required; STL version = secured, non-STL = unsecured | Headline terms need STL; non-STL needs higher salary, higher rate and lower limits | Near (concept) | **Two tracks** [U]: (a) Salary-assigned (STL + EOS undertaking); (b) Unsecured non-STL with tighter terms (P-21 to P-23) |
| P-06 | Employer categories | All accepted | Listed / approved vs non-listed tiers with different minimum salary and caps (FAB non-listed 10k, max 500k) | Slightly off | All accepted [U], but **tiered** [A]: **Cat A** government, semi-government, MoD/AF; **Cat B** listed large private; **Cat C** other listed; **Cat D** non-listed. Tier drives caps, pricing and the non-STL rules |
| P-07 | DBR | CBUAE limit | 50% of gross + regular income; retirees 30% (all five) | Near | **50% of gross salary + regular income; 30% retirees; 60% government housing programmes** [C]. Model also reports a basic + housing DBR as a risk indicator (not a gate) [P] |
| P-08 | AECB credit score | Not specified | Only RAKBANK publishes floors: **541** expats and non-STL, 300 nationals STL. ENBD uses the score to waive requirements | **Far (missing)** | Unsecured, salary-assigned: **≥ 541** (nationals ≥ 500) [P]. Unsecured non-STL: **≥ 600** [P]. Cards: ≥ 541. Home / auto: ≥ 541. Deposit-backed: no floor (refer if < 541). **Knock-outs:** current DPD ≥ 30; any 90+ DPD or write-off / settlement in 24 months; > 6 AECB enquiries in 30 days → refer [P] |
| P-09 | Restricted nationalities / sectors | Not specified | No published nationality bans. EI temporarily tightened hospitality / travel / real-estate employers (2026) | Slightly off | **No nationality-based exclusion** (sanctions screening only) [P]. Sector watch-list with lower caps, not bans [P]. Sharia Board guidance on prohibited-activity employers [P] |
| P-10 | Bank statements / verification | Last 12 months' statements + financials if possible | 3 months (salaried STL), 6 months (self-employed, DIB), 2 years' audited (self-employed home) | Near (stricter for non-STL: good) | Salary-assigned: **3 months** or UAEFTS consent [A, market]. Non-STL and self-employed: **12 months** [U]. Self-employed home: **2 years' audited financials** [M] |
| P-11 | Self-employed | Statements + financials | PF: 1-yr business + AED 20k average balance (ENBD). Auto: average balance 10–25k. Home: business 2–3 yrs + 2 yrs audited | Slightly off | Trade licence **≥ 2 years** (PF, auto) / **≥ 3 years** (home) [M]. Average monthly balance **≥ AED 20,000** (PF), **≥ 15,000** (auto) [M]. Income from 12 months' turnover and audited accounts [U/M]. PF max AED 500,000 [P] |

## 2. Personal finance: salary-assigned (Commodity Murabaha / Tawarruq)
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-12 | Minimum salary | AED 5,000 | 3,000 (DIB) / **5,000** / 7,000 (FAB) | Near | **AED 5,000** nationals and expats [U] |
| P-13 | Max amount | Not given → CBUAE | 20× (CBUAE). AED: nationals 5m / **4m** / 3m; expats 3m / **2m** / 1.5m | Near | **Lower of 20× gross monthly income or AED 4m nationals / AED 2m expats** [C+M]. Cat D employers: max AED 500,000 [M] |
| P-14 | Max tenor | Not given → CBUAE | 48 months (60 MoD/AF) | Near | **48 months**; 60 months for MoD/AF only where the CBUAE exemption applies (verify) [C] |
| P-15 | Profit rate | Mid-market | Floor 4.75 / **~5.24–5.99** / 12.75; ceiling 13.99 / **19.99–21.99** / 31.99 | Near | Nationals **from 5.49%**, expats **from 5.99%**, up to **19.99%**, risk-based by AI grade (§9) [M] |
| P-16 | Processing fee | Mid-market | **1% (min 500, max 2,500) + VAT** at all five (CBUAE cap) | Near | **1% (min AED 500, max AED 2,500) + VAT** [C/M] |
| P-17 | Early settlement | Mid-market | 1% of outstanding, max AED 10,000 + VAT (CBUAE cap) | Near | **1%, max AED 10,000 + VAT**, by rebate of unearned profit (Ibra) [C/M] |
| P-18 | Late payment | Mid-market | Charity AED 100 (ADIB) / **175–210** / 210 | Near | **Undertaking to donate AED 175** per late instalment to charity (net of actual costs, Sharia-approved) [M] |
| P-19 | Salary assignment & security | STL confirmation + EOS undertaking | DIB, RAKBANK, ADCB: salary + EOSB assignment; ENBD security cheque; Mashreq PDCs | Near (in line with stronger peers) | **Employer STL on bank format + irrevocable EOS undertaking**; WPS salary credit verified [U]. Rate step-up **+2% p.a.** if salary is not credited for 3 consecutive months (RAKBANK practice) [P]. Undated security cheque as per market practice, subject to legal advice [M] |
| P-20 | First-instalment grace (nationals) | Not given | 365 (FAB) / **120–210** / 60 days | Slightly off | **Up to 120 days** for nationals [M, conservative end] |

## 3. Personal finance: unsecured (no salary transfer)
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-21 | Minimum salary | AED 5,000 | 5,000 + AECB 541 (RAKBANK) / **10,000** (FAB non-listed, ENBD) / 15,000 + 18 months (FAB Islamic) | **Far (most lenient)** | **AED 5,000 kept only with compensating controls** [A]: AECB ≥ 600, employer Cat A–C, ≥ 6 months' service, 12 months' statements showing regular salary. **Cat D employers or AECB 541–599: AED 10,000** [M] |
| P-22 | Max amount | Not given → CBUAE | RAKBANK non-STL: nationals 20× max 500k; expats 10× max 200k. FAB non-listed max 500k | Slightly off | **Nationals: 20×, max AED 500,000. Expats: 10×, max AED 200,000** [M] |
| P-23 | Pricing & repayment | Mid-market | FAB non-listed 8.99–11.99%; Mashreq NEO 10.49–17.49%; RAKBANK 12.99–22.49% | Near | **9.99%–21.99%** by grade [M]. Repayment by **UAE direct debit (UAEDDS)** from the salary account [M]. Tenor 48 months [C] |

## 4. Buyout and top-up
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-24 | Buyout (takeover from another bank) | STL confirmation + EOS undertaking | Liability letter; settle other bank in 30–90 days (ADIB); residual released after clearance + STL (Mashreq) | Slightly off (process missing) | STL + EOS undertaking [U]. Liability letter **≤ 15 days old** [P]. Bank pays the other bank directly **within 30 days** [M]. Residual funds released only after the **clearance letter** [M]. Combined amount ≤ 20× and ≤ 48 months [C]. No processing fee on pure buyout [M] |
| P-25 | Top-up | Not given → CBUAE | CBUAE: only after ≥ 12 months' clean repayment. Top-up Murabaha at ADIB, DIB | Near | **≥ 12 months clean repayment, fresh DBR and AECB, max one top-up per 12 months**, fee on the increment only [C/M] |
| P-26 | Rescheduling | Not given → CBUAE | Beyond 48 months only when DBR > 50% with **no new money** | Near | As CBUAE (collections policy) [C] |

## 5. Islamic credit cards
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-27 | Minimum salary | AED 5,000 | **5,000** entry at all five; premium 15–35k | Near | Entry **AED 5,000**; Gold 12,000; Platinum 20,000 [M] |
| P-28 | Card limit | Not given | Not published by any bank | Far (missing) | **Lower of 3× gross monthly income (salary-assigned) / 2× (non-STL)**, tier caps, and DBR headroom (5% of limit counted) [P] |
| P-29 | Profit rate & fees | Mid-market | Monthly 2.99 / **3.49–3.75%** / 3.99%. Minimum payment **5% or AED 100**. Late fee charity AED 100–236. Entry annual fee free | Near | **3.59% per month** standard, 3.25% premium [M]. Minimum payment 5% or AED 100 [M]. Late: donation undertaking AED 200 [M]. Entry card annual fee free [M] |
| P-30 | Self-employed card | Statements + financials | Average balance 50k / 3 months (ENBD); average quarterly balance 75k or turnover 150k (RAKBANK) | Slightly off | Average balance **≥ AED 50,000** over 3 months or deposit-backed card [M] |

## 6. Home finance (Ijarah Muntahia Bittamleek; Istisna'a + forward Ijarah for off-plan)
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-31 | Minimum salary | AED 5,000 | Nationals 8k (EI, ADCB) / **10k** / 15k. Expats 10k (DIB) / **15k** / 20k (EI) | **Far (well below market)** | **AED 10,000 nationals (AED 8,000 under government housing schemes) / AED 15,000 expats** [A] |
| P-32 | Finance-to-value | CBUAE | 85/80 at 7 of 8 banks | Near | First home ≤ AED 5m **85% nationals / 80% expats**; > 5m **75 / 70**; second+ home **65 / 60**; off-plan **50%** [C] |
| P-33 | Max tenor | CBUAE | 25 yrs (30 under the national rate-relief programme) | Near | **25 years** (30 only under the CBUAE rate-relief exception, nationals with income < AED 40k) [C] |
| P-34 | Max finance amount | Not given | 30m (ADIB) / **20–25m** / 13m (RAK) | Slightly off | **AED 20m** [M] |
| P-35 | Profit rate | Mid-market | 3-yr fixed teaser 3.85 / **~4.0–4.3%** / 4.69. Variable EIBOR + 1.25 / **1.49–1.69%**. Reversion ~ +1.6–1.99%. Floor 1.99 / **2.5–3.1%** / 3.99 | Near | 3-yr fixed **4.24%** salary-assigned / **4.49%** non-STL; 5-yr fixed **4.44% / 4.69%**; variable **3M EIBOR + 1.59%**; reversion **3M EIBOR + 1.79%**; floor **2.99%**; self-employed **+0.25%** [M] |
| P-36 | Fees | Mid-market | Processing 1% + VAT (caps 30k ADIB, 52.5k ADCB, 105k DIB, uncapped others); valuation 2,500–3,150; partial prepayment free 0 / **20–30%** / 0 | Near | Processing **1% + VAT (min 5,000, max 50,000)**; valuation **AED 2,500 + VAT**; **25%** free partial prepayment per year; early settlement 1% max 10,000 + VAT; **buyout: no processing fee, valuation refunded** [M] |
| P-37 | DBR & stress | CBUAE | 50%; no bank publishes a stress rate | Slightly off | **DBR 50%** [C], assessed at the **higher of the initial rate and the reversion rate** (current 3M EIBOR + reversion margin) [P] |
| P-38 | Off-plan | CBUAE | 50% LTV; project ≥ 35% complete and customer ≥ 50% paid (DIB, ADIB, Mashreq) | Near | **50%; project ≥ 35% complete; customer paid ≥ 50%; approved developer list** [C/M] |
| P-39 | Age / service / self-employed | Not given | 70/65; ENBD expats 3 yrs UAE + 1 yr job; self-employed 2 yrs audited | Slightly off | Age per P-03. Salaried **6 months + probation** [A]. Self-employed business **≥ 3 years + 2 years' audited financials** [M] |
| P-40 | Takaful | Not given | Life takaful ~0.011–0.025% per month; property ~0.03–0.06% p.a.; ADIB pays property takaful | Slightly off | **Mandatory life and property takaful**, bank as beneficiary [M] |
| P-41 | Government schemes | Not given | SZHP, MBRHE, ADHA top-up, Sharjah housing (all Islamic peers) | Slightly off | Participate subject to Board decision; government housing **DBR up to 60%** [C/P] |
| P-42 | Non-resident | Not in scope | 50–65% LTV | n/a | **Excluded in v1** [P] |

## 7. Auto finance (Murabaha)
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-43 | Minimum salary | AED 5,000 | 3k (DIB) / **5k** / 7k (ENBD, FAB) | Near | **AED 5,000** [U] |
| P-44 | Down payment / tenor | Mid-market (CBUAE floors) | 20% / 60 months everywhere | Near | **20% minimum / 60 months maximum** [C] |
| P-45 | Max amount | Mid-market | 2m (ENBD) / **1.5m** (EI, FAB, ADCB) / 1m (DIB, ADIB) | Near | **AED 1.5m** [M] |
| P-46 | Profit rate | Mid-market | New car flat 1.75–1.89 / **2.15–2.90%** / 3.19%+ | Near | New **2.49% flat nationals / 2.69% flat expats**; used **3.19% flat**; EV **1.99% flat**; APR shown in the KFS [M] |
| P-47 | Vehicle age | Mid-market | 12 yrs at maturity (ADCB, ENBD) / **10 yrs** (DIB, RAK) | Near | **≤ 10 years at end of finance** [M] |
| P-48 | Seller / valuation | Mid-market | Private sale allowed with approved-dealer valuation (ENBD, EI, DIB); dealer only (Mashreq) | Near | Dealer or **private sale with bank-approved valuation** [M] |
| P-49 | Self-employed | Statements | Average balance 10k (EI) / **20k** (ENBD) / 25k (FAB) | Slightly off | Trade licence ≥ 2 yrs; **average balance ≥ AED 15,000** [M] |
| P-50 | Security, takaful, settlement | Mid-market | Car mortgaged; comprehensive takaful (bank beneficiary); early settlement = lower of 1% (max 10k) or unearned profit + Ibra (ADIB, DIB); charity AED 100–210 | Near | Vehicle mortgaged with RTA in the bank's favour; **comprehensive motor takaful** (financeable); early settlement = lower of 1% (max 10k) or unearned profit, with Ibra; late donation **AED 175** [M] |

## 8. Other secured: deposit, gold, EOSB, salary advance
| ID | Item | User criterion | Top-five benchmark | Rating | Recommended |
|---|---|---|---|---|---|
| P-51 | Deposit-backed (Murabaha with lien on Wakala / term deposit) | **90%** of security | 90% (ENBD, ADCB, Mashreq); 95% (FAB, ADIB) | Near | **90%** of deposit [U]; max AED 10m; 48 months; **deposit profit rate + 2%**; no minimum salary [M] |
| P-52 | Gold-backed (rahn of allocated gold / gold certificates) | **90%** | Only EI lends: **50%** of gold certificates (Priority customers) | **Far (no precedent at 90%)** | **70% maximum** [A]. Top-up call at **80%**, sale at **85%** loan-to-value; daily revaluation; ≤ 24 months; Sharia Board approval [P] |
| P-53 | EOSB-backed | **90%** of accrued EOSB | **No top-five bank lends against EOSB alone**; DIB, RAKBANK, ADCB, Mashreq, ADIB (auto) take EOSB as **additional** security | **Far (no precedent)** | Only **inside salary-assigned finance**, as additional security. Finance against EOSB **≤ 80% of accrued EOSB** [A]. **≥ 3 years' service**; irrevocable employer undertaking; EOSB recalculated yearly; total still ≤ 20× and ≤ 48 months [C/P] |
| P-54 | Salary advance (Tawarruq-based) | (part of product group) | DIB FlexiSalary: min 2k, up to 13k, fixed profit 80–200. ADIB Yusr: 50% of net salary, max 50k, ≤ 51 days, 0.99–3.99% per month | Slightly off | Salary-assigned customers; min salary AED 5,000 [U]. **Up to 50% of net monthly salary, max AED 25,000**; repaid from next salary (≤ 35 days); fixed profit **AED 100–250 by band**; max 6 per year; blocked if any DPD [M/P] |

## 9. Risk-based pricing and decision bands (AI Risk Score Card grades 1–10)
| Grade | PD band | Decision (policy passed) | Personal finance rate add-on over floor |
|---|---|---|---|
| 1–3 | < 1% | Approve | + 0.00–1.00% |
| 4–6 | 1–5% | Approve | + 1.00–5.00% |
| 7–8 | 5–12% | **Refer** (model escalation) | + 5.00–10.00% (deviation authority) |
| 9–10 | ≥ 12% | Decline (policy) | n/a |

## 10. Delegation of authority (proposed)
| Authority | Unsecured (per customer, total) | Secured home finance | Deviations allowed |
|---|---|---|---|
| Credit Officer | up to AED 250,000, grade ≤ 6 | up to AED 3m, grade ≤ 6 | none |
| Senior Credit Officer | up to AED 1m, grade ≤ 6 | up to AED 7.5m | bank-policy items, grade ≤ 4 |
| Head of Retail Credit | up to AED 4m | up to AED 15m | bank-policy items, grade ≤ 6 |
| Chief Risk Officer | above Head limits | up to AED 20m | grade 7–8 cases |
| Credit Committee | any | above AED 20m / policy exceptions | — |

CBUAE rules can never be deviated. Grades 9–10 cannot be approved.

## 11. Rating summary
| Rating | Count | Items |
|---|---|---|
| Near | 31 | P-01, 04 (STL), 05, 07, 10, 12–19, 23, 25–27, 29, 32, 33, 35, 36, 38, 43–48, 50, 51 |
| Slightly off | 17 | P-02, 03, 04 (non-STL / home), 06, 09, 11, 20, 22, 24, 30, 34, 37, 39–41, 49, 54 |
| **Far** | **6** | **P-08** AECB missing; **P-21** non-STL minimum salary; **P-28** card limits missing; **P-31** home finance minimum salary; **P-52** gold 90%; **P-53** EOSB 90% |
| n/a | 1 | P-42 non-resident (out of scope) |

P-04 is counted twice (Near for salary-assigned, Slightly off for non-STL and home), so the rows add up to 55 for 54 items.

**Overall:** the basic criteria are close to the top five on pricing, fees, DBR, LTV, tenors and salary-assigned finance. They are **more lenient than every top-five bank** on unsecured non-STL entry and home-finance minimum salary, and on gold- and EOSB-backed advance rates. They are **silent** on credit-bureau floors and card limits. Closing those seven gaps puts the policy inside the top-five band on every item.
