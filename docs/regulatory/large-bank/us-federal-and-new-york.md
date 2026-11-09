# US Federal + New York Rules Reference (US pack)

> Researched 2026-11-07 for AI Risk Score Card Global. Confidence: H = primary source/settled law; M = consistent secondary; L = estimate.
> **[2°]** = secondary source only; **[UNCONFIRMED]** = could not confirm. Not legal advice; validate with the bank's Legal & Compliance.

## Headline changes 2025–2026
1. **Reg B amended** (91 FR 21620, effective **2026-07-21**): ECOA "effects test" / disparate impact removed; discouragement now intent-based; SPCPs may not use race, color, national origin or sex. Intentional neutral proxies are still disparate treatment. **In litigation** (NFHA v. CFPB, D.D.C.; second suit D. Mass.), no stay.
2. **SR 11-7 replaced by SR 26-2 / OCC 2026-13 / FDIC (2026-04-17).** Principles-based, non-enforceable, materiality-driven (>$30B assets "most relevant"). Rule-based deterministic processes are not "models". **Generative/agentic AI out of scope.**
3. **Leveraged lending guidance rescinded by OCC/FDIC (2025-12-05)**; the Fed's SR 13-3 still posted.
4. **Colorado SB 24-205 repealed → SB 26-189** (effective 2027-01-01): ADMT notice, 30-day explanation of adverse outcome, human review on request; enforcement stayed by court pending rulemaking.
5. **Basel III endgame re-proposed 2026-03-19**; not final.
6. **Section 1071** final rule: compliance 2028-01-01 (≥1,000 originations in 2026 and 2027).
7. **TPRM 2023 interagency guidance still in force**; replacement proposed 2026-09-11.
8. **NY FAIR Act** (effective 2026-02-17): adds "unfair" and "abusive" to GBL 349 (AG enforcement).
9. OCC/FDIC final rule removing reputation risk from supervision (2026-04-07).
10. CFPB Circulars 2022-03 / 2023-03 (AI adverse-action reasons) **withdrawn 2025-05-12**, but the Reg B 1002.9 duty is unchanged; build as if they apply.
11. Disparate impact: EO 14281 (2025); OCC, FDIC and CFPB stopped examining for it; **Fair Housing Act disparate impact survives by statute**; state AGs active (MA AG v. Earnest, Jul 2025, $2.5M, AI underwriting). **ECOA statute of limitations 5 years.**

## A. Consumer credit
| Rule | Requirement | Product must |
|---|---|---|
| ECOA/Reg B prohibited bases (12 CFR 1002.2(z), 1002.4) | Race, color, religion, national origin, sex, marital status, age (if able to contract), public-assistance income, CCPA rights | Block these and declared proxies from features; feature allow-list + lineage audit |
| Reg B scoring & age (1002.2(p), 1002.6(b)(2)) | Empirically derived, statistically sound, periodically revalidated; age may be scored but **62+ never negative** | Revalidation schedule; age rule in scorecard |
| Reg B adverse action timing (1002.9(a)) | **30 days** after complete application; **90 days** after unaccepted counteroffer; business ≤$1M revenue similar; >$1M reasonable time | SLA timers, notice queue, escalation |
| Reg B specific principal reasons (1002.9(b)(2)) | Specific reasons reflecting factors actually scored; >4 unlikely helpful; "internal standards" not acceptable | **Deterministic reason codes from scorecard/ML attribution; LLM never selects reasons**, only paraphrases; versioned reason library |
| FCRA (15 USC 1681b, 1681m, 1681g(f)) | Permissible purpose; adverse action discloses score, range, **≤4 key factors (5 if inquiries)**, CRA details, free report within 60 days, dispute right | Purpose code per pull; notice template; bureau key factors kept separate from bank reasons |
| Reg V risk-based pricing (12 CFR 1022.70–.75) | Notice when terms materially less favourable based on a consumer report | Pricing-tier flag → notice |
| FCRA medical info (1022.30) | No medical information in eligibility (limited exceptions) | Block medical-derived features |
| CARD Act ability to pay (12 CFR 1026.51) | Consider ability to make minimum payments (income/assets, obligations). **Under 21: independent ability or cosigner 21+**; CLI on cosigned under-21 accounts needs cosigner consent | **Hard gate:** ability-to-pay calc; under-21 branch |
| Card penalty fees | 2024 $8 rule vacated (2025); safe-harbor amounts configurable [UNCONFIRMED current values] | Config |
| ATR/QM (1026.43) | 8 ATR factors; **General QM price-based, no 43% DTI cap**; must consider and verify DTI or residual income. 2026 APR–APOR: first lien ≥$137,958 <2.25pp; $82,775–137,958 <3.5pp; <$82,775 <6.5pp; safe harbor <APOR+1.5pp. Points & fees 2026: 3% (≥$137,958) … 8% (<$17,245). HOEPA 2026: $27,592 / $1,380 | Annual threshold table; QM classifier; DTI/residual income required, no hard cap (bank policy sets) |
| HMDA/Reg C (12 CFR 1003) | ~48 data points incl. score, DTI, CLTV, AUS result, ≤4 denial reasons, demographics; 2026 asset exemption $59M | Map reasons → HMDA denial codes; demographics firewalled from decisions |
| UDAAP + **NY FAIR Act** (GBL 349, from 2026-02-17) | Unfair, deceptive, abusive | LLM text accurate, consistent with notices; explanation audit log |
| MLA (32 CFR 232) | **36% MAPR** cap; covered-borrower check (DoD); no mandatory arbitration | **Hard gate** before pricing |
| SCRA (50 USC 3937) | **6%** cap on pre-service obligations | Rate override flag |
| NY usury | Civil **16%** (Banking Law 14-a; GOL 5-501); criminal **>25%** (Penal 190.40); civil not for loans ≥$250k (non 1–2 family); ≥$2.5M exempt from both; national banks export home-state rates (12 USC 85) | Rate-cap table keyed by charter, entity, state, size |
| NY Human Rights Law 296-a | Adds creed, **citizenship/immigration status**, sexual orientation, gender identity, military status, DV-victim status, disability, familial status; **bans aggregate group statistics** | Broader prohibited list; no group-statistic features |
| Fed SR 26-4 (2026-08-13) | Lending to people not authorised to work in US may be elevated risk | **Conflicts with NY 296-a** → legal-review-required feature, not default |
| NYDFS AI | No banking AI-lending guidance; AI cyber letter (Part 500); bills A.773/S.8115 in committee | Watch list; impact-assessment export ready |
| NYC LL144 / NY RAISE / GBL 349-a | LL144 employment-only; RAISE (frontier developers) n/a; algorithmic pricing disclosure exempts GLBA FIs | No NY AI-lending statute today |
| Colorado SB 26-189 (2027-01-01) | ADMT notice, 30-day plain explanation, access/correction, human review on request; developer must give deployer documentation | Deployer documentation pack; CO workflow |
| CA CCPA ADMT (2027-01-01), TX TRAIGA (2026), NJ LAD disparate impact | State layer | Jurisdiction rules config |
| Disparate impact | Federal ECOA removed; FHA keeps it; state law; 5-yr SOL | **Keep DI testing on by default** (AIR, SMD, LDA search, BISG for testing only) |

## B. Commercial / corporate / SME
| Rule | Requirement | Product must |
|---|---|---|
| Credit risk rating (OCC Handbook; SNC ≥$100M, 3+ institutions) | Regulatory rating, SNC review | PD/LGD rating mapped to regulatory grades; SNC flag |
| Leveraged lending | OCC/FDIC rescinded; Fed SR 13-3 active | Configurable heightened review (e.g. total debt/EBITDA >6x), not hard decline |
| **SCCL** (12 CFR 252.72) | ≤**25% Tier 1** per counterparty; **15%** major covered company → major counterparty | Connected-counterparty aggregation; pre-deal limit check |
| Legal lending limit (12 CFR 32.3) | **15%** capital & surplus + **10%** if fully secured by readily marketable collateral | Hard gate + borrower combination (32.5) |
| Reg W (23A/23B) | ≤10% per affiliate, ≤20% aggregate; collateral 100–130%; market terms | Affiliate flag → compliance workflow |
| Reg O (12 CFR 215.4) | No preferential terms; board approval > greater of $25k or 5% of capital (always > $500k) | Insider registry check |
| CRE concentration (2006) | Construction ≥100% / total CRE ≥300% (+50% growth in 36m) triggers review | Dashboard thresholds |
| Section 1071 | Compliance 2028-01-01; ≤$1M revenue small business | Data model ready; demographics firewalled |
| CRA | In flux | Geocoding/assessment-area tags (not decision input) |
| Basel III endgame | Re-proposed 2026-03-19, not final | PD/LGD/EAD internal outputs only |

## C. Models & AI governance
- **SR 26-2 / OCC 2026-13**: effective challenge, validation (conceptual soundness incl. interpretability, outcomes analysis, monitoring), inventory, documentation. Vendor models: bank must understand design, **development data**, performance. Scorecard + GBM = models; rules engine not a model but needs change control; **LLM outside SR 26-2 → ship a separate LLM control pack.**
- **TPRM (2023 guidance)**: due diligence, contract (audit/exam access, subcontractors, incident notice, termination, IP/escrow), monitoring; regulators may examine the vendor (12 USC 1867(c)).
- **Incident notice**: bank → regulator within **36 hours**; service provider → bank ASAP if disruption ≥ **4 hours**.
- **NIST AI RMF 1.0** + GenAI profile (AI 600-1): map controls (Govern/Map/Measure/Manage).
- Fair-lending testing: AIR, marginal effects, proxy testing, LDA search, business-justification record.
- FFIEC IT handbooks; NIST CSF 2.0.

## D. Provisioning / classification
- **CECL (ASC 326)**: lifetime ECL; reasonable & supportable forecast + reversion.
- Grades: **Pass, Special Mention, Substandard, Doubtful, Loss.**
- Nonaccrual 90+ DPD (unless well secured and in collection).
- **URCCP (2000)**: open-end charge-off **180 DPD**, closed-end **120 DPD**; retail 90+ DPD Substandard; bankruptcy charge-off within 60 days of notice; fraud within 90 days; re-aging limits.

## E. Data & privacy
GLBA privacy (Reg P) and interagency safeguards; NY SHIELD; **NY Part 500** (MFA, asset inventory, 72-hour DFS notice; applies to DFS licensees); state privacy laws (CA/OR/MN data-level GLBA exemption only); **DOJ bulk sensitive-data rule** (no access from countries of concern; scrutiny of China-origin AI models); retention: Reg B 25 months (consumer), 12 months (small business), HMDA 3 years.

## F. Execution
~12+ regulators/enforcers (Fed, OCC or NYDFS, FDIC, CFPB, NYDFS, SEC/FINRA, FinCEN, DOJ, HUD, FTC, NY AG, other state AGs). GSIB vendor onboarding 12–24 months (consumer decisioning at scale 24–36). Litigation: ECOA punitive ≤$10k individual, class ≤ lesser of $500k or 1% net worth; FCRA $100–1,000 per willful violation + punitive.

## Config values (US pack)
```yaml
jurisdiction_as_of: "2026-11-07"
reg_b: {adverse_action_days_complete_app: 30, adverse_action_days_counteroffer: 90, max_principal_reasons: 4,
        business_revenue_threshold_usd: 1000000, record_retention_months_consumer: 25, record_retention_months_business_le_1m: 12,
        age_protected_negative_weight_floor_age: 62, effects_test_in_reg_b: false, disparate_impact_testing_enabled: true,
        llm_may_generate_reasons: false}
fcra: {max_key_factors: 4, max_key_factors_if_inquiries: 5, free_report_request_window_days: 60}
reg_z:
  card_min_age_without_cosigner: 21
  card_ability_to_pay_required: true
  qm_general_dti_cap: null
  qm_2026_apr_apor_spread_pp: {first_lien_ge_137958: 2.25, first_lien_82775_to_137958: 3.5, first_lien_lt_82775: 6.5,
                               manufactured_home_lt_137958: 6.5, subordinate_ge_82775: 3.5, subordinate_lt_82775: 6.5}
  qm_safe_harbor_first_lien_pp: 1.5
  qm_2026_points_fees: {ge_137958: "3%", 82775_to_137958_usd: 4139, 27592_to_82775: "5%", 17245_to_27592_usd: 1380, lt_17245: "8%"}
  hoepa_2026_total_loan_threshold_usd: 27592
  hoepa_2026_points_fees_trigger_usd: 1380
hmda: {asset_exemption_2026_usd: 59000000, max_denial_reasons: 4}
mla: {mapr_cap_pct: 36}
scra: {rate_cap_pct: 6}
ny_usury: {civil_max_pct: 16, criminal_threshold_pct: 25, civil_exempt_loan_ge_usd: 250000, all_usury_exempt_loan_ge_usd: 2500000, apply_only_if_ny_rate_governs: true}
ny_hrl_extra_protected: [creed, citizenship_or_immigration_status, sexual_orientation, gender_identity_or_expression, military_status, domestic_violence_victim_status, disability, familial_status]
ny_hrl_ban_group_aggregate_statistics: true
lending_limits: {occ_general_pct_capital_surplus: 15, occ_additional_marketable_collateral_pct: 10, sccl_general_pct_tier1: 25,
                 sccl_major_to_major_pct_tier1: 15, reg_w_single_affiliate_pct: 10, reg_w_aggregate_affiliates_pct: 20,
                 reg_o_prior_approval_usd: 25000, reg_o_prior_approval_pct: 5, reg_o_prior_approval_absolute_usd: 500000}
leveraged_lending: {occ_fdic_guidance_active: false, fed_sr_13_3_active: true, heightened_review_total_debt_ebitda_x: 6.0}
cre_concentration_review: {construction_pct_total_capital: 100, total_cre_pct_total_capital: 300, growth_pct_36m: 50}
classification: {grades: [Pass, Special Mention, Substandard, Doubtful, Loss], nonaccrual_dpd: 90, retail_substandard_dpd: 90,
                 chargeoff_closed_end_dpd: 120, chargeoff_open_end_dpd: 180, bankruptcy_chargeoff_days_after_notice: 60, fraud_chargeoff_days_after_discovery: 90}
model_risk: {guidance: "SR 26-2 / OCC 2026-13 (2026-04-17)", genai_in_scope: false, rules_engine_is_model: false}
incident_notice: {bank_to_regulator_hours: 36, service_provider_disruption_threshold_hours: 4, ny_part500_dfs_notice_hours: 72}
section_1071: {compliance_date: "2028-01-01", origination_threshold: 1000}
colorado_admt: {law: "SB26-189", effective: "2027-01-01", adverse_outcome_explanation_days: 30, human_review_on_request: true}
```

## Top 10 hardest US requirements
1. Specific, accurate adverse-action reasons from a GBM (Reg B, FCRA). LLM excluded from reason selection.
2. Fair-lending defensibility without a stable federal standard (FHA, NY 296-a, NJ, MA, 5-yr SOL).
3. Vendor model validation under SR 26-2 + TPRM (development data, on-prem validator access).
4. Governing the local LLM (outside SR 26-2; UDAAP/FAIR Act accuracy).
5. GSIB security/TPRM: Part 500, safeguards, 36h/4h incident rules, DOJ data rule, SBOM, escrow.
6. Multi-jurisdiction rules layer (rate caps by charter/state, MLA/SCRA, CO/CA 2027).
7. CARD Act ability-to-pay + ATR/QM annual thresholds.
8. Commercial aggregation: SCCL, legal lending limit, Reg O, Reg W pre-decision.
9. Policy volatility → versioned, date-effective rules.
10. Lineage & retention (HMDA, 1071, Reg B 25 months, explanation logs for discovery).

**Unconfirmed:** Fed exam stance on disparate impact; Fed CRA final position; final Basel endgame; current card penalty-fee safe harbors; HUD final FHA DI action; NY GOL 5-501(6) threshold wording; FFIEC CAT sunset; X.AI v. Weiser stay details; timelines.
