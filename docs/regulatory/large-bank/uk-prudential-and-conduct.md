# UK Rules Reference (UK pack): PRA, FCA, Bank of England, ICO

> Researched 2026-11-07 for AI Risk Score Card Global. Rule text checked directly: CONC (Jul 2026), MCOB (Jun 2026), PRIN (Jun 2026),
> PRA Credit Risk 6.1, UK GDPR Arts 22A–22C, PRA SS1/23 page, PS1/26, FCA motor finance statement, FG26/11, HMT CCA policy statement (May 2026).
> Confidence H/M/L as in the US file. Not legal advice; validate with the bank's Legal & Compliance.

## Changes that matter (2024–2026)
| Area | Change | Status |
|---|---|---|
| Basel 3.1 | PS1/26: effective **1 Jan 2027**; FRTB IMA 1 Jan 2028; output floor 72.5% by 1 Jan 2030 | H |
| UK GDPR ADM | Art 22 replaced by **Arts 22A–22D**, in force **5 Feb 2026** (SI 2026/82) | H |
| ICO ADM guidance | Draft consulted Mar–May 2026; final not published | M |
| BNPL | Regulated from **15 Jul 2026** (PS26/1); CONC 5.2A applies unmodified | H |
| Motor finance | *Johnson v FirstRand* [2025] UKSC 33; FCA redress scheme PS26/3 (~£9.1bn total); parts suspended by Upper Tribunal 2 Jul 2026, hearing Feb–Mar 2027 | H/M |
| Mortgage LTI | Firm-level 15% cap (≥4.5x) removed from PRA rules **28 Oct 2026**; FPC 15% remains market-aggregate | H/M |
| CCA reform | Into FCA rules via FSM Bill; ss.56, 75, 140A–C retained | H |
| Consumer Duty | Unchanged; CP26/23 proposes proportionality changes (final ~Q1 2027) | M |
| PRA SS1/23 | Effective 17 May 2024; updated 23 Apr 2026 | H |
| FCA & AI | Mills Review (Jul 2026): no new AI rules; **AI Live Testing** cohort 2 to end-2026 | M/H |
| Critical Third Parties | First designations 13 Jul 2026 (AWS, Google Cloud, Microsoft, Oracle) | H |
| Incident & third-party reporting | Register + incidents from **18 Mar 2027** (PS26/2, PRA PS7/26) | H/M |
| FOS | Award limit **£455,000** (from 1 Apr 2026, acts on/after 1 Apr 2019) | H |
| CRA data | FCA CP26/7 mandatory credit-data reporting; CIGB replacing SCOR governance | M |

## A. Consumer credit
| Rule | Requirement | Product must |
|---|---|---|
| **CONC 5.2A.4–6** | Creditworthiness assessment before new agreement, significant credit/limit increase, **and cumulative** small increases | **Hard gate**; stored assessment per decision; cumulative-increase tracker |
| **CONC 5.2A.10–12** two limbs | **Credit risk AND affordability risk** (repay without undue difficulty over life of agreement) | **Separate outputs**; good score never overrides failed affordability; separate reason codes |
| **CONC 5.2A.15–18** income & expenditure | Determine/estimate income; foreseeable falls; **self-declared income alone not generally sufficient**; non-discretionary spend incl. priority debts; "obvious" exemption with burden of proof | Income-verification source flag (CRA / Open Banking / document); expenditure model; justification log |
| CONC 5.2A.20 proportionality | Depth scaled to product, amount, term, APR, consequences | Configurable depth by product tier |
| CONC 5.2A.33 | Written policy approved by governing body; record per transaction | Immutable decision log; policy-as-config approvals |
| CONC 5.2A.36 | Don't accept known/suspected untruthful info | Declared vs verified income consistency check |
| **CONC 6.7.27–36 persistent debt** | Monthly test: 18m where principal repaid < interest+fees (exempt if balance <£200 at any point); notice at 18m, review ~27m, at 36m offer repayment within ~3–4 yrs; else suspend/cancel | State machine PD18/PD27/PD36; block CLI in persistent debt |
| **CONC 5D** overdrafts | Monitor repeat use; financial-difficulty vs other; communications (1st, 2nd, then ≥ annual) | Segmentation + triggers |
| **CONC 7.3** arrears | Forbearance and due consideration (PS24/14, Nov 2024) | Collections support offers forbearance options |
| **Consumer Duty (PRIN 2A)** | Good faith, avoid foreseeable harm; 4 outcomes; outcome monitoring by customer group; fair value | Cohort outcome MI (vulnerability, proxies); explanations tested for understanding; LLM grounded in reason codes |
| FG21/1 vulnerable customers | Drivers: health, life events, resilience, capability | Vulnerability flags → human review; never auto-decline on flag alone |
| **MCOB 11.6** | Affordability on capital & interest; no general declaration; income evidence; **stress ≥5 yrs, min +1pp, forward curve** (fixed ≥5 yrs exempt) | Stress = max(forward-curve rate, current +1pp) |
| LTI | High LTI ≥ **4.5x**; firm cap removed 28 Oct 2026; market aggregate 15% | Tag LTI ≥4.5; configurable internal limit |
| 2022 BoE affordability test | Withdrawn | Not a rule (optional overlay) |
| **CCA s.140A–C** unfair relationships | Court can reopen; commission disclosure (*Johnson*); reverse burden | Store commission/disclosure evidence; long retention |
| CCA s.157 | Tell customer which CRA on request after refusal | Record CRA used |
| CCA notices & sanctions | In force until FSM Bill moves them to FCA rules | Configurable notice logic |
| Motor finance (PS26/3) | 2007–2024 redress; high commission ≥39% of cost of credit and ≥10% of loan; DCAs banned since Jan 2021 | Capture commission model and disclosure; block DCAs |
| BNPL (PS26/1) | CONC 5.2A unmodified; CONC 4.2A, 7.20 | Lightweight compliant affordability path |
| **Equality Act 2010** s.13, **s.19 indirect discrimination**, s.29 | 9 protected characteristics; age exception with reliable information | Proxy audit; disparity testing with justification; age only if justified |
| **UK GDPR Arts 22A–22D** | Solely automated = no *meaningful* human involvement; allowed on any lawful basis except special category (explicit consent / 9(2)(g)) and **not on "recognised legitimate interests"**; safeguards: information, representations, **human intervention, contest** | Mode 1 human-in-loop with evidence of meaningful review; Mode 2 automated with 22C workflow; block special category inputs; lawful-basis field |
| FOS | £455k (acts ≥ 1 Apr 2019), £205k earlier; "fair and reasonable" | Case-file export; readable explanations |

## B. Commercial / corporate / SME
| Rule | Requirement | Product must |
|---|---|---|
| **Large exposures** (Art 395) | ≤**25% Tier 1** per client/connected group; **15%** G-SII → G-SII | Connected-client aggregation; hard gate/refer |
| **Basel 3.1** (PS1/26) | From 1 Jan 2027; SME supporting factor removed (Pillar 2A offset); unrated SME corporate 85% RW; retail SME 75%; real-estate revaluation if value fell >10%; slotting for income-producing RE | Data attributes only (exposure class, Art 124E); no capital calc |
| **Definition of default** | **Retail: >£0 and >0%** (any amount counts); non-retail >EUR 500 equiv and >1%; 90 DPD; unlikeliness-to-pay | Counters by facility/obligor; UTP flags |
| SME Standards of Lending Practice (LSB) | Business customers ≤£25m turnover; declines with explanation | SME decline reasons + signposting |
| **Bank Referral Scheme** (SBEEA 2015) | Designated banks offer referral of declined SMEs (with consent) | Referral-offer event + consent flag |
| **SM&CR** | SMF owns credit & model risk (SMF4 CRO) | Model/policy inventory mapped to SMF owner |
| Ring-fencing | Core deposits ≥£35bn; exposure restrictions to financial institutions | Entity-aware decisioning; FI counterparty flag |
| Leveraged/private markets | Pillar 2/SREP; 2024 PE letter; Sept 2026 Dear CFO letter | Sponsor aggregation; leverage flags; covenant monitoring |

## C. Models & AI
- **PRA SS1/23** (5 principles: identification & tiering, governance, development/use incl. post-model adjustments, independent validation, mitigants). Covers **all models used for business decisions incl. vendor and AI/ML**. Deliver documentation pack per model; champion/challenger; monitoring; PMA logging; **LLM explainer treated as an inventoried model** (faithfulness, hallucination testing).
- **SS2/21** outsourcing/third-party (updated PS7/26): material arrangement; audit/access, escrow, exit plan, SBOM; register from 18 Mar 2027.
- **SS1/21 operational resilience**: important business services, impact tolerances; fallback mode (rules + scorecard if ML/LLM fail).
- CTP regime: on-prem vendor unlikely designated; document cloud dependencies.
- FCA AI: technology-neutral; AI Live Testing evidence pack. BoE/PRA (Apr 2026): no AI-specific rules; SS1/23 is the tool.
- **IRB boundary**: decision-support is not an IRB rating system; reconciliation report vs internal ratings (use test).

## D. Provisioning
IFRS 9: SICR backstop **>30 DPD**; default rebuttable **90 DPD**; regulatory default as above; forbearance/NPE definitions (distressed restructuring NPV loss >1% → default).

## E. Data & privacy
Lawful basis (contract / legitimate interests / legal obligation; "recognised legitimate interests" cannot support solely automated decisions); **DPIA mandatory**; special category data only in a segregated **fairness-testing zone** (DPA 2018 Sch 1 para 8); no UK localisation law but on-prem + UK-only support; **Open Banking** consented data for affordability; CRA reciprocity (SCOR → CIGB; CP26/7); retention: term + 6 years with litigation hold.

## F. Execution
~8–11 bodies (PRA, FCA, BoE FPC, ICO, FOS, CMA, PSR, HMT, EHRC, LSB, courts). Vendor onboarding 12–24 months (procurement 6–9). Redress: FOS £455k, s.140A, s.404 schemes.

## Config values (UK pack)
```yaml
jurisdiction: UK
as_of: 2026-11-07
consumer_credit:
  creditworthiness:
    require_assessment_on: [new_agreement, significant_credit_increase, significant_limit_increase, cumulative_significant_increase]
    dual_limb_required: {credit_risk: true, affordability_risk: true}
    self_declared_income_sufficient_alone: false
    obvious_affordability_exemption_requires_justification_log: true
    record_per_transaction: true
    policy_approval_by: governing_body
    applies_to_deferred_payment_credit_from: 2026-07-15
  persistent_debt: {test_frequency: monthly, lookback_months: 18, min_balance_gbp_exemption: 200, stage_2_review_window_months: [9, 10],
                    stage_3_months: 36, reasonable_repayment_period_years: {typical_min: 3, typical_max: 4}, action_on_no_response: suspend_or_cancel,
                    excludes_business_credit_cards: true}
  overdraft_repeat_use: {categories: [financial_difficulty_signs, other_repeat_use], other_repeat_use_comms: [first, second, then_at_least_annual]}
  arrears: {forbearance_required: true, approaching_arrears_trigger: customer_indicates_risk}
mortgages:
  stress_test: {horizon_years: 5, exempt_if_fixed_rate_years_gte: 5, min_rate_rise_pct_points: 1.0, rate_source: market_forward_curve, must_regard_fpc_recommendation: true}
  general_declaration_of_affordability_allowed: false
  high_lti_threshold_multiple: 4.5
  firm_level_high_lti_share_cap: null
  market_aggregate_high_lti_share_cap: 0.15
data_protection:
  adm_regime: UK_GDPR_Art22A_22D
  solely_automated_significant_safeguards: [information, representations, human_intervention, contest]
  recognised_legitimate_interests_for_solely_automated: false
  dpia_required: true
complaints: {fos_award_limit_gbp_acts_on_or_after_2019_04_01: 455000, fos_award_limit_gbp_acts_before_2019_04_01: 205000}
prudential:
  large_exposure_limit_pct_tier1: 25
  gsii_to_gsii_limit_pct_tier1: 15
  default_dpd: 90
  default_materiality_retail: {absolute_gbp: 0, relative_pct: 0}
  default_materiality_non_retail: {absolute: "EUR 500 sterling equivalent", relative_pct: 1}
  basel31_effective: 2027-01-01
  sme_unrated_corporate_rw_pct: 85
  retail_sme_rw_pct: 75
  ring_fence_core_deposit_threshold_gbp: 35000000000
ifrs9: {sicr_backstop_dpd: 30, default_rebuttable_dpd: 90}
model_risk: {framework: PRA_SS1_23, llm_explainer_is_inventoried_model: true, smf_owner_required: true}
third_party: {incident_and_third_party_reporting_effective: 2027-03-18}
sme: {lsb_business_standards_turnover_cap_gbp: 25000000, bank_referral_scheme_offer_on_decline: true}
motor_finance: {redress_period: {from: 2007-04-06, to: 2024-11-01}, high_commission_flag: {pct_of_cost_of_credit_gte: 39, pct_of_loan_gte: 10}, dca_permitted: false}
```

## Top 10 hardest UK requirements
1. Meaningful human involvement at scale (Art 22A) or full 22C safeguards.
2. Two-limb CONC 5.2A with verified income for every product.
3. SS1/23 validation of GBM and LLM explainer.
4. Equality Act indirect discrimination and proxy control (Sch 1 para 8 testing route).
5. Consumer Duty cohort outcome evidence.
6. Back-book liability (s.140A, FOS, s.404) → 10–20 year reproducible records.
7. SS2/21 material third-party onboarding.
8. Mortgage stress + LTI under change.
9. Regulatory churn 2026–27 → effective-dated policy-as-config.
10. Persistent-debt, overdraft repeat-use and forbearance state machines.

**Unconfirmed:** output-floor yearly path; post-2027 default-threshold location; motor scheme suspended parts; CP26/18 and CP26/23 finals; final ICO ADM guidance; LSB recognition renewal; 2026 persistent-debt update; SS1/23 April 2026 amendment content; FSM Bill wording; timelines.
