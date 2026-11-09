# Retail Credit Policy: Model Configuration (demo_islamic_bank, v0.1 draft)

These files turn the UAE Islamic bank retail credit policy (`../03-parameter-sheet.md`) into AI Risk Score Card rule files.
They use the **recommended** values. Wherever a value was **adjusted** from your basic criteria to match the top five UAE retail
banks, the file says so in a comment, together with your original value.

| File | Layer | Contents |
|---|---|---|
| `bank_policy.yaml` | Layer 2: bank policy | Eligibility (customer groups, ages, service per track), repayment tracks, employer categories A–D, AECB floors and knock-outs, sector watch-list, documents, self-employed rules, affordability references, delegation of authority, deviation rules, decision bands |
| `credit_policy.yaml` | Layer 3: credit policy | Products (salary-assigned and unsecured personal finance, buyout, top-up, cards, home, auto, deposit-, gold- and EOSB-backed, salary advance) with income minimums, amount caps, tenors, finance-to-value limits, pricing grids, fees, takaful and grade bands |
| `rules.yaml` | Executable rules (AD-3 format) | 65 rules: `BANK.RET.*` (Layer 2) and `CRED.*` (Layer 3), plus `cbuae_references` pointing to the CBUAE layer (not duplicated). Every condition is a plain comparison expression. There are no inline lookup tables: the card-tier minimum and the home finance-to-value table are split into one rule per value (CRED.CC.001a–c, CRED.HF.002a–f), each selected by `applies_to` |
| `validate_config.py` | Check | Parses the files, checks rule keys, runs the tighten-only checks against CBUAE, and evaluates three worked examples |

## Mapping to the parameter sheet

| Parameter sheet IDs | Where |
|---|---|
| P-01–P-11 (general) | `bank_policy.yaml` (eligibility, tracks, employer_categories, aecb, sector_watch_list, documents, self_employed, affordability); rules BANK.RET.001–034 |
| P-12–P-20 (salary-assigned personal finance) | `credit_policy.yaml` products.personal_finance_salary_assigned; rules CRED.PF.001–004 |
| P-21–P-23 (unsecured, no salary transfer) | products.personal_finance_unsecured; rules CRED.PFU.001–004 |
| P-24–P-26 (buyout, top-up, rescheduling) | products.buyout / top_up / rescheduling; rules CRED.BO.*, CRED.TU.001 |
| P-27–P-30 (cards) | products.credit_card; rules CRED.CC.001a (classic AED 5,000), 001b (gold 12,000), 001c (platinum 20,000), CRED.CC.002–003 |
| P-31–P-42 (home finance) | products.home_finance; rules CRED.HF.001; CRED.HF.002a–f (finance-to-value: national/expat × first home ≤ 5m, first home > 5m, second+ home = 85/80, 75/70, 65/60); CRED.HF.003 (off-plan 50%); CRED.HF.004–010 |
| P-43–P-50 (auto) | products.auto_finance; rules CRED.AF.001–005 |
| P-51–P-54 (deposit, gold, EOSB, salary advance) | products.deposit_backed / gold_backed / eosb_backed / salary_advance; rules CRED.DEP.001, CRED.GOLD.*, CRED.EOS.*, CRED.SA.001 |
| §9 grades / §10 authority | `credit_policy.yaml` grades; `bank_policy.yaml` decision_bands, delegation_of_authority, deviation_rules; rules CRED.GRD.* |

## Values adjusted from your basic criteria ([A], needs your sign-off)

| ID | Your criterion | Configured value | Why |
|---|---|---|---|
| P-04 | 3 months' service (all) | 6 months for unsecured non-STL and home finance; 3 months kept for salary-assigned | Top-five median is 6 months |
| P-21 | AED 5,000 unsecured, no conditions | AED 5,000 only with AECB ≥ 600, employer A–C, 6 months' service and 12 months' statements; otherwise AED 10,000 | Top-five median for non-STL is AED 10,000 |
| P-31 | AED 5,000 home finance | AED 10,000 nationals (8,000 under government schemes) / AED 15,000 expats | Top-five range 8–20k |
| P-52 | Gold-backed 90% | 70% maximum, margin call at 80%, sale at 85% | Only top-five lender: EI at 50% |
| P-53 | EOSB-backed 90% | 80% of accrued EOSB, ≥ 3 years' service, only inside salary-assigned finance | No top-five bank lends against EOSB alone |
| P-10 | 12 months' statements (all) | 3 months or UAEFTS consent for salary-assigned; 12 months kept for non-STL and self-employed | Market practice for salary-transfer customers |
| P-06 | All employers, no tiers | All accepted, but tiered A–D for caps and pricing | All top-five banks tier employers |
| P-39 | 3 months' service; age per "CBUAE" (no limit exists) | Home finance: salaried 6 months + probation completed; age at maturity 70 nationals / self-employed, 65 salaried expats; self-employed ≥ 3 yrs business + 2 yrs audited | Top-five home-finance practice (CBUAE abolished the age cap in 2019) |

**Proposed ([P]) where neither you nor the market gave a figure:**
- AECB floors and knock-outs
- card limit multiples
- gold margin-call and sale levels
- EOSB minimum service
- salary-advance cap and frequency
- home-finance stress rate
- delegation of authority
- sector watch-list

**Your criteria kept as given ([U]):**
- nationals and expats eligible
- AED 5,000 minimum (salary-assigned personal finance, cards entry, auto, salary advance)
- 3 months' service (salary-assigned)
- salary transfer not required (two tracks)
- all employers accepted
- 90% deposit-backed
- salary transfer confirmation + EOS undertaking for salary-assigned finance and buyouts
- 12 months' statements for non-STL and self-employed customers

## Loading into the demo tenant

1. Copy the three YAML files to `banks/demo_islamic_bank/`:
   - `bank_policy.yaml`
   - `credit_policy.yaml`
   - `rules.yaml` (rules)
2. Run `python credit-policy-uae/config/validate_config.py`. Every tighten-only check must pass.
3. Publish through maker-checker (FR-6). The loader re-runs tighten-only validation against `config/regulators/cbuae.yaml` (FR-3, AD-3).
4. Resolve the items marked "VERIFY" (MoD/AF 60-month exemption) and sign off the [A] items before using this outside the demo.
