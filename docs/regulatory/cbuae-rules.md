# CBUAE Rules Reference (Layer 1)

> Source: archive/PROMPT_v1_2026-11-06.md, Appendix A (researched 2026-11-06). Applies to AI Risk Score Card. Islamic products use the same CBUAE limits (personal finance = personal loan rules; Ijara home finance = mortgage rules; auto Murabaha = car loan rules).


Researched 2026-11-06. The CBUAE Rulebook (rulebook.centralbank.ae) blocked automated reading, so some values
were read from search extracts of rulebook pages. **Confidence:** H = primary text read or quoted verbatim;
M = rulebook extract / official press release plus consistent secondary sources; L = secondary only;
UNCONFIRMED = no primary source found. Carry these levels into `cbuae.yaml` as `confidence:` and show
anything below H as "to verify" in the dashboard.

### A.1 Key instruments
| Instrument | Status | Link |
|---|---|---|
| Regulation 29/2011 *Bank Loans & Other Services Offered to Individual Customers* (amended; consolidated 14/06/2022) | In force | https://rulebook.centralbank.ae/en/rulebook/regulation-no-292011-regarding-bank-loans-other-services-offered-individual-customers |
| Circular 31/2013 *Mortgage Loans* (amended 2019, 2020, 2023) | In force (out of scope v1) | https://rulebook.centralbank.ae/en/rulebook/regulations-regarding-mortgage-loans |
| Resolution 96/By Circulation/2019: Appendix 2 fee caps | In force | https://rulebook.centralbank.ae/en/rulebook/central-bank-board-directors%E2%80%99-resolution-no-96by-circulation2019-amending-appendix-2 |
| Large Exposures Regulation C 1/2023 (eff. 26 Jul 2023) | In force | https://rulebook.centralbank.ae/en/rulebook/large-exposures-regulation |
| Credit Risk Management Regulation & Standards C 3/2024 (eff. 30 Nov 2024; repeals Circular 28/2010) | In force | https://rulebook.centralbank.ae/en/rulebook/credit-risk-management-regulation |
| SME Customer Protection Regulation C 2/2026 (eff. 13 Sep 2026; replaces C 1/2021) | In force | https://rulebook.centralbank.ae/en/rulebook/small-medium-sized-enterprises-sme-customer-protection-regulation |
| Consumer Protection Standards, Art 7 *Responsible Financing* | In force | https://rulebook.centralbank.ae/en/rulebook/article-7-responsible-financing-practice |
| AECB Business Regulations (Board Res. 67/5/2015) | In force | https://etihadbureau.ae/faqs |

### A.2 Retail rules that matter for v1
| Rule | Value | Applies to | Source | Conf. |
|---|---|---|---|---|
| Personal loan max amount | **20 × monthly salary / total income** | All individuals. Also sole proprietorships / companies whose loan is secured by the owner's salary | Reg 29/2011 Art 2(b),(e) | H |
| Personal loan max tenor | **48 months** | Same | Art 2(c) | H |
| DBR cap | **50% of gross salary + regular income from a defined source**, at all times, counting **all** lenders: personal, car, housing, overdraft, cards | All borrowers | Art 7(a) | H |
| DBR cap, retirees | **30%** of income/pension. A loan running past retirement must fit this | Retirees | Art 7(b) | H |
| What counts as "gross salary" | No official allowance list. Banks use gross incl. fixed allowances | — | Art 7(a) | UNCONFIRMED → bank policy |
| Credit card in DBR | Cards count. **No CBUAE % factor.** "5% of limit" is market convention | — | Art 7(a) | H that cards count; 5% = **bank policy** |
| Don't auto-lend at the cap | Consider individual circumstances. No tenor/balloon structures to get around DBR or limits | All | Mortgage Reg Art 3; CPS Art 7 | M |
| Minimum salary for a personal loan | **None since Nov 2025** (old AED 5,000 floor removed) → bank policy | All | Press reports, Nov 2025 (no circular no. found) | M |
| Credit card minimum income | **AED 60,000 p.a.** or pledged deposit ≥ AED 60,000 | Card applicants | Art 5(c) | H (orig. text). Status after Nov 2025 UNCONFIRMED |
| Card limit increase | Only with express consent. AECB check required | Card holders | CPS Art 7 | M |
| Overdrafts | Pre-arranged with purpose and repayment source. Count in DBR. Personal loans must not be disguised as overdrafts | Individuals | Art 4 | H/M |
| Top-up loans | Only after ≥ **12 months** of clean repayment on the original loan | Personal / car | Art 6(g) | H (orig. text) |
| Rescheduling | May extend beyond 48 m when DBR > 50%, **with no new money** | Existing personal loans | Notice 4501/2011 | M |
| **End-of-service benefit (EOSB)** | Personal loans may be repaid from **"salary and end of service indemnity"**. The lender must confirm salary and EOSB with the employer. (EOSB is **not** an allowed source for mortgages) | Personal loans | Art 2(a); Clarifications Manual | H |
| Salary transfer requirement | **Not a CBUAE rule** → bank policy | — | — | UNCONFIRMED |
| Min / max age | **No CBUAE rule found for personal loans** → bank policy (e.g. 21/18 min, 60/65 at maturity) | — | — | UNCONFIRMED |
| Non-residents | No specific CBUAE quantitative rule → bank policy | — | — | UNCONFIRMED |
| Car loan (future module) | LTV ≤ **80%**, tenor ≤ **60 m**, down payment from own funds | Private cars | Art 3 | H |
| Early settlement fee | ≤ **1%** of outstanding, max **AED 10,000** | Personal/consumer loans | Res. 96/2019 | M |
| AECB | Report required before lending, with **prior written consent**. Score **300–900** (higher = lower risk, predicts the next 12 months). **No official bands** | All | CPS Art 7; Res. 67/5/2015; AECB FAQ | M / H |
| AECB delinquency record | Default, or write-off with ≥ AED 1,000 unpaid > 180 days | — | Res. 67/5/2015 Art 1 | H |

UAE Labour Law EOSB formula (for the EOSB feature; config-driven, verify with the bank): 21 days' **basic**
salary per year for the first 5 years, 30 days per year after that, total capped at 2 years' wages. Pro-rated
for part years. The bank's own treatment (e.g. % of EOSB lendable) is bank policy.

### A.3 Corporate / SME rules
| Rule | Value | Source | Conf. |
|---|---|---|---|
| Large exposure definition | ≥ **10% of Tier 1** | LE Reg C 1/2023 | H |
| Single counterparty / connected group | ≤ **25% of Tier 1** | LE Reg Art 3, Annex 1.1 | H |
| Identify connected groups by economic interdependence | When exposure > **5%** of Tier 1 | LE Reg | M |
| Commercial GREs | **25%** individual / **100%** aggregate | Annex 1.6 | H |
| Local governments | **150%** aggregate | Annex 1.4 | H |
| Shareholders ≥ 5% (+ related) | **20%** individual / **50%** aggregate | Annex 1.11 | H |
| Non-bank subsidiaries / affiliates | **10%** / **25%** | Annex 1.12 | H |
| Board members | **5%** / **25%** | Annex 1.13 | H |
| Federal govt / CBUAE | Exempt (reportable) | Annex 1 | H |
| Lending to the bank's external auditor | Prohibited | LE Reg | M |
| Real-estate exposure | Legacy 20%-of-deposits cap superseded (2021). Monitored by risk-weighted assets → internal limit | CBUAE press release 20 Dec 2021 | M |
| Underwriting framework | Documented underwriting policy; independent credit review | CRM Reg C 3/2024 | H |
| Annual review | Wholesale obligors reviewed and re-rated **at least annually** | CRM Standards | M |
| Rating scale | One internal scale for risk, provisioning and capital; documented granularity | Model Mgmt Standards | M |
| Real-estate collateral | Independent third-party valuation required. Indicative haircuts: residential RE 25–30%, commercial RE 30–40%, listed equity 15–20%, unlisted 30–40%, govt bonds 1–8% | CRM Std Art 10; KPMG summary | M (haircuts L/M) |
| SME conduct | Affordability and suitability assessment before credit; Key Facts Statement; 60 days' notice of changes | SME CP Reg C 2/2026 | M |
| Sole proprietorship secured by owner's salary | Treated as retail (20×, 48 m, 50% DBR) | Reg 29/2011 Art 2(e) | H |

### A.4 Classification (for the IFRS 9 stage hint)
| Item | Value | Source | Conf. |
|---|---|---|---|
| Stage 2 (significant increase in credit risk) | **> 30 DPD** (rebuttable); watch-list required | CRM Std 7.6/7.8 | H |
| Stage 3 / default | **> 90 DPD** or unlikely to pay. Retail at facility level, wholesale at obligor level | CRM Reg Art 6 | H |
| Restructuring | ≥ 3 distressed restructurings → Stage 3. Non-distressed moratorium > 6 m → Stage 2 | CRM Std | M |
| Stage 3 sub-bands | Retail 91–120 / 121–180 / > 180 DPD. Wholesale 91–180 / 181–365 / > 365 | CRM Std Art 9 | M |
| Stage 1+2 provision floor | ≥ 1.5% of credit risk-weighted assets | CRM Std 9.21 | H |

### A.5 Values for `config/regulators/cbuae.yaml`
```yaml
# "POLICY" = not a CBUAE rule (belongs in bank_policy.yaml). "VERIFY" = confirm manually before production.
retail:
  personal_loan:
    max_multiple_monthly_income: {value: 20, direction: max, source: "Reg 29/2011 Art 2(b)", confidence: H}
    max_tenor_months:            {value: 48, direction: max, source: "Reg 29/2011 Art 2(c)", confidence: H}
    min_monthly_salary_aed:      null   # abolished Nov 2025 -> POLICY
    topup_min_clean_repayment_months: {value: 12, direction: min, source: "Art 6(g)", confidence: H}
    eosb_allowed_as_repayment_source: true   # Art 2(a)
  dbr:
    max_pct_gross_income: {value: 50, direction: max, source: "Reg 29/2011 Art 7(a)", confidence: H}
    max_pct_retiree:      {value: 30, direction: max, source: "Reg 29/2011 Art 7(b)", confidence: H}
    include_all_lenders_cards_overdrafts: true
    # credit_card_limit_factor_pct: 5  -> POLICY (market convention)
  credit_card:
    min_annual_income_aed: {value: 60000, direction: min, source: "Reg 29/2011 Art 5(c)", confidence: M}  # VERIFY post-Nov-2025
    limit_increase_requires_express_consent: true
  auto_loan:   {max_ltv_pct: 80, max_tenor_months: 60}     # future module
  fees:        {early_settlement_consumer_pct: 1, early_settlement_consumer_cap_aed: 10000}  # VERIFY cap
  aecb:
    report_required_before_credit: true
    written_consent_required: true
    score_min: 300
    score_max: 900
    bands_unofficial: {poor: [300,540], fair: [541,650], good: [651,710], very_good: [711,745], excellent: [746,900]}  # ADCB-published; VERIFY
corporate:
  large_exposure_pct_tier1:
    definition_threshold: 10
    single_or_group_limit: {value: 25, direction: max, confidence: H}
    group_identification_trigger: 5
    gre_commercial_individual: 25
    gre_commercial_aggregate: 100
    local_govt_aggregate: 150
    shareholder_ge5pct_individual: 20
    shareholder_ge5pct_aggregate: 50
    nonbank_subsidiary_affiliate_individual: 10
    nonbank_subsidiary_affiliate_aggregate: 25
    board_member_individual: 5
    board_member_aggregate: 25
    external_auditor: prohibited
    federal_govt_and_cbuae: exempt
  annual_review_required: true
  re_collateral_independent_valuation: true
  collateral_haircut_pct_indicative: {residential_re: 30, commercial_re: 40, listed_equity: 20, unlisted_equity: 40, govt_bond_short: 2, govt_bond_long: 8, cash: 0}  # VERIFY
classification:
  sicr_dpd: 30
  default_dpd: 90
  restructure_count_to_stage3: 3
  nondistressed_moratorium_months_to_stage2: 6
  stage12_min_provision_pct_crwa: 1.5
```

### A.6 Verify manually before production (in a browser)
1. Large Exposures Regulation, Annex 1.
2. CRM Standards PDF (CBUAE_EN_5996_VER1), Tables 2–4: Stage 3 floors and collateral haircuts.
3. The current consolidated Appendix 2 fee table.
4. Whether the Nov 2025 removal of the minimum salary also lifted the AED 60,000 card income floor.
5. Any CBUAE notice issued after 2026-11-06.

### A.7 Home finance: Ijara (CBUAE mortgage regulation, Circular 31/2013 as amended)
Now IN scope (discovery round 3). Rulebook: https://rulebook.centralbank.ae/en/rulebook/regulations-regarding-mortgage-loans

| Rule | UAE national | Expat | Source | Conf. |
|---|---|---|---|---|
| First home, owner-occupied, value ≤ AED 5m: max LTV | **85%** | **80%** | Board Res. 31/2/2020 (eff. 8 Apr 2020) | H (national) / M (expat) |
| First home, value > AED 5m | **75%** | **70%** | same | M |
| Second / investment home (any value) | **65%** | **60%** | Art 3 | M |
| Off-plan property (any buyer) | **50%** | 50% | Art 3 | H |
| Max tenor | **25 years** | 25 years | Art 3 | H |
| Tenor exception | up to 30 years to absorb rate rises, income < AED 40k/month (bank bears uncovered profit) | n/a | CBUAE notice 4 Jul 2023 | H |
| Max age at final repayment | **Abolished 2019**; lender policy (legacy: national 70, expat 65, self-employed expat 70) | same | Res. 96/2019 | H |
| DBR | **50%** (60% for government-guaranteed housing programmes, e.g. SZHP; retirees on SZHP up to 50%) | 50% | Art 3/5; SZHP notice 2022 | H |
| EOSB as repayment source | **Not allowed** | Not allowed | Art 3 | M |
| Early settlement fee | ≤ 1% of outstanding or AED 10,000, whichever is less | same | Res. 96/2019 | H |
| Structure | Reducing balance; first-class registered security in the bank's name | same | Art 3 | M |

### A.8 Auto finance: Murabaha (Reg 29/2011 Art 3)
| Rule | Value | Conf. |
|---|---|---|
| Max finance-to-value | **80%** of vehicle value (new or used private car) | H |
| Max tenor | **60 months** | H |
| Down payment | From the customer's own funds (not from personal finance or a card) | H |
| Security | Charge over the vehicle | H |
| Early settlement fee | 1% of outstanding | M |

### A.9 Islamic-finance note
CBUAE consumer limits apply equally to Islamic products: Tawarruq/Murabaha personal finance follows the personal-loan limits,
Ijara home finance follows the mortgage regulation, and auto Murabaha follows the car-loan rules. Higher Sharia Authority (HSA) standards
govern product structure. The bank's own Sharia board approves product terms (outside CBUAE numeric limits).
