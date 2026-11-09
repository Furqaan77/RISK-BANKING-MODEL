# Conventional Bank Retail Credit Policy: Model Configuration (demo_conventional_bank, v0.1 draft)

These files turn the conventional bank retail credit policy (`../03-parameter-sheet.md`) into AI Risk Score Card rule files.

**Credit criteria are identical to the recommended Islamic policy** (`../../credit-policy-uae/config/`): ages, service, minimum salaries, AECB floors, caps, loan-to-value limits, tenors, DBR, rates, grade bands and the authority matrix. Only these change:
- the structures become a conventional personal loan, mortgage, auto loan, pledge / lien, and loan or overdraft against deposit
- pricing language becomes interest rate
- fees: late payment fee retained as income; early settlement 1% of outstanding principal
- insurance becomes conventional credit life, property and motor insurance

> **Vocabulary note:** the UAE edition of AI Risk Score Card uses Islamic vocabulary only in v1 (PRD decision B1b; the AD-12 lint rejects conventional terms). To load this conventional configuration, the tenant needs a **conventional vocabulary profile**, as in AI Risk Score Card Global, or the UAE edition needs a vocabulary switch. Every file is marked `vocabulary_profile: conventional`.

| File | Layer | Contents |
|---|---|---|
| `bank_policy.yaml` | Layer 2: bank policy | Eligibility (customer groups, ages, service per track), repayment tracks, employer categories A–D, AECB floors and knock-outs, sector watch-list, documents (incl. insurance documents), self-employed rules, affordability references, delegation of authority, deviation rules, decision bands |
| `credit_policy.yaml` | Layer 3: credit policy | Products (`personal_loan_salary_assigned`, `personal_loan_unsecured`, `buyout`, `top_up`, `rescheduling`, `credit_card`, `home_loan`, `auto_loan`, `deposit_backed`, `gold_backed`, `eosb_backed`, `salary_advance`) with income minimums, amount caps, tenors, loan-to-value limits, interest-rate grids, fees, insurance and grade bands; shared fee definitions |
| `rules.yaml` | Executable rules (AD-3 format) | 70 rules: `BANK.RET.*` (Layer 2) and `CRED.*` (Layer 3), plus `cbuae_references` pointing to the CBUAE layer. Every condition is a plain expression with no inline lookup tables (card tiers CRED.CC.001a–c and home loan-to-value CRED.HL.002a–f are one rule per value) |
| `validate_config.py` | Check | Parses the files, checks rule keys and product names, runs the tighten-only checks against CBUAE, checks the conventional fee and insurance conversion, scans for Islamic-only terms, and evaluates three worked examples |

## Changes from the Islamic configuration
| Area | Islamic config | Conventional config |
|---|---|---|
| Product keys | personal finance, home finance, auto finance | `personal_loan_*`, `home_loan`, `auto_loan` (others unchanged) |
| Rule IDs | CRED.PF / PFU / HF / AF | CRED.PL / PLU / HL / AL (BANK.RET.*, CC, BO, TU, DEP, GOLD, EOS, SA, FEE, GRD unchanged) |
| Late payment | donation undertaking (AED 175; cards AED 200) | **fee retained as income: 2% of overdue instalment, min AED 50, max AED 200 + VAT** (personal and auto loans); **cards AED 230 + VAT** (= AED 241.50, market standard) |
| Early settlement | 1% max AED 10,000 + VAT, with rebate of unearned profit | **1% of outstanding principal, max AED 10,000 + VAT** |
| Insurance | Islamic insurance cover | **credit life insurance mandatory for personal loans (new item P-20a)**; life + property insurance (home); comprehensive motor insurance, bank first beneficiary (auto) |
| Deposit-backed | finance with lien on deposit | **term loan or overdraft** against fixed deposit at 90%; overdraft 12 months, renewable |
| Gold-backed | pledge of gold, religious-board approval | pledge of gold; **new product approval committee** |
| Governance | religious-board approval of structures | none; Board Risk Committee only |
| New rules (+5) | — | CRED.PL.005 (credit life), CRED.AL.006 (motor insurance), CRED.DEP.002 (overdraft 12 months), CRED.FEE.002 (late fee cap), CRED.FEE.003 (card late fee cap) |

## Mapping to the parameter sheet
| Parameter sheet IDs | Where |
|---|---|
| P-01–P-11 (general) | `bank_policy.yaml`; rules BANK.RET.001–034 |
| P-12–P-20a (salary-assigned personal loan) | `credit_policy.yaml` products.personal_loan_salary_assigned; rules CRED.PL.001–005 |
| P-21–P-23 (unsecured, no salary transfer) | products.personal_loan_unsecured; rules CRED.PLU.001–004 |
| P-24–P-26 (buyout, top-up, rescheduling) | products.buyout / top_up / rescheduling; rules CRED.BO.*, CRED.TU.001 |
| P-27–P-30 (cards) | products.credit_card; rules CRED.CC.001a–c, CRED.CC.002–003, CRED.FEE.003 |
| P-31–P-42 (home loans) | products.home_loan; rules CRED.HL.001, 002a–f, 003–007, 010 |
| P-43–P-50 (auto loans) | products.auto_loan; rules CRED.AL.001–006 |
| P-51–P-54 (deposit, gold, EOSB, salary advance) | products.deposit_backed / gold_backed / eosb_backed / salary_advance; rules CRED.DEP.001–002, CRED.GOLD.*, CRED.EOS.*, CRED.SA.001 |
| Fees, §9 grades, §10 authority | `credit_policy.yaml` fee_definitions and grades; `bank_policy.yaml` decision_bands, delegation_of_authority, deviation_rules; rules CRED.FEE.*, CRED.GRD.* |

## Sign-off still needed
The 8 items adjusted from the original basic criteria in the Islamic policy keep the same values here and need the same management sign-off:
- P-04 service
- P-06 employer tiers
- P-10 statements
- P-21 unsecured minimum salary
- P-31 home minimum salary
- P-39 home service / age
- P-52 gold 70%
- P-53 EOSB 80%

**Lenient edge against the five conventional banks** (consider tightening for a lower risk appetite):
- P-31 home-loan minimum salary for nationals (10k vs median 10–15k)
- P-39 salaried expat home service
- P-43 auto minimum salary (5k vs median 7k)
- P-49 self-employed auto balance (15k vs 20–25k)

**No conventional peer product:** P-28 card limits, P-37 home DBR stress, P-52 gold, P-53 EOSB, P-54 salary advance.

## Loading into a demo tenant
1. Create a conventional tenant profile, e.g. `banks/demo_conventional_bank/`, with the conventional vocabulary switch on.
2. Copy `bank_policy.yaml`, `credit_policy.yaml` and `rules.yaml` there.
3. Run `python credit-policy-uae-conventional/config/validate_config.py`. Every tighten-only check must pass.
4. Publish through maker-checker (FR-6). The loader re-runs tighten-only validation against `config/regulators/cbuae.yaml` (FR-3, AD-3).
5. Resolve the "VERIFY" items (MoD/AF 60-month exemption; 30-year home tenor only under the CBUAE rate-relief exception) before use outside the demo.
