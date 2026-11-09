# Pilot Finance Company Retail Credit Policy: Model Configuration (demo_finance_company, v0.1 draft)

These files turn the finance-company retail credit policy (`../05-retail-credit-policy.md`, with values from `../03-parameter-sheet.md`, items F-01 to F-60) into rule files the AI Risk Score Card can run.

The company is a **conventional** finance company licensed under the **Finance Companies Regulation (FCR, Circular C 3/2023), Part I**. That changes three things compared with the bank configuration:
- **Prudential limits:** capital, leverage, liquidity, large exposures and related parties are checked before every approval.
- **No deposits:** the company cannot hold deposits or accounts for individuals, so there are no deposit-backed loans, no overdrafts and no Islamic window.
- **Approval letters:** every product line needs a CBUAE no-objection letter before launch.

Every file is marked `vocabulary_profile: conventional`.

## 1. The three layers (read this first)

```
 Layer 1  REGULATORY   CBUAE consumer rules + FCR prudential rules      <- the law; can never be relaxed
    |
 Layer 2  COMPANY      the company's own limits (tighter or equal)      <- Board-approved risk appetite
    |
 Layer 3  CREDIT       product rules: amounts, rates, tenors, fees      <- what credit staff apply daily
```

- **Tighten-only:** a lower layer may be **stricter** than the layer above, never looser. Example: the CBUAE allows an AED 500 late fee on auto loans; our auto late fee is capped at AED 200.
- **Policy always wins:** the AI grade can turn an approval into a referral, but it can never approve a case the rules decline.
- **Grades:**

| AI grade | What happens |
|---|---|
| 1–6 | Approve, if every rule passes |
| 7–8 | Refer to the Chief Risk Officer |
| 9–10 | Decline |

| File | Layer | What is in it |
|---|---|---|
| `rules.yaml` → `regulatory_baseline`, `cbuae_references` | 1 | The CBUAE and FCR numbers: 20× income, 48 months, DBR 50% / 30%, fee caps, AED 150m capital, 100% leverage, 10% liquidity, 10% / 15% exposure limits, short-term credit caps |
| `bank_policy.yaml` | 2 (company) | Licence scope, prudential limits, eligibility, the two repayment tracks, employer categories A–D, AECB floors, documents, self-employed rules, DBR, **pricing grid by AI grade**, **approval matrix**, deviations, decision bands, **portfolio limits**, monitoring and provisioning. (The file keeps the name `bank_policy.yaml` so the loader finds it.) |
| `credit_policy.yaml` | 3 (credit) | One block per product, covering amounts, tenors, rates, fees, security and phase. Each block has `offered_in_pilot` and `cbuae_nol_received`. |
| `rules.yaml` → `prudential_rules` | 1 + 2 | Company-level checks on a balance-sheet snapshot (PRU.FCR.*, PRU.CO.*, PORT.*) |
| `rules.yaml` → `rules` | 1 + 2 + 3 | Checks on each application (REG.*, CO.RET.*, CRED.*) |
| `validate_config.py` | — | Proves the files are consistent and tighten-only, and runs the worked examples through the rules |

## 2. How to read a rule

```yaml
  - id: CRED.PEA.002                       # CRED = Layer 3; PEA = personal loan, employer-assigned
    layer: credit_policy
    applies_to: {products: [personal_loan_employer_assigned]}   # which applications it checks
    condition: "loan_amount <= min(20 * monthly_gross_income, 300000, (150000 if employer_category == 'D' else 300000))"
    severity: knockout                     # if the condition is FALSE -> Decline
    direction: max
    limit: {income_multiple: 20, cap_aed: 300000, cap_aed_employer_cat_d: 150000}
    message: "Employer-assigned: amount above 20x income, AED 300,000, or AED 150,000 for category D."
    source: "F-21 [A] -> CBUAE.RET.PF.MULTIPLE"   # parameter-sheet item, tag, regulatory reference
    confidence: H
```

- **`condition`** is what must be **true** for the application to pass. It uses only plain comparisons (`<=`, `==`, `and`, `or`), `min()` / `max()` and `in [..]`. There are no hidden lookup tables.
- **Tiered values are split into separate rules.** The three card tiers become CRED.CC.001a–c and 003a–c, and the three salary-advance fee bands become CRED.SA.005a–c.
- **`severity`:**

| Severity | On a customer rule | On a portfolio rule |
|---|---|---|
| `knockout` | Decline | New disbursements of those products are **held** |
| `refer` | At most Refer | A named owner takes the listed action |
| `warn` | Note on file | Report only |

- **ID prefixes:**

| Prefix | Layer |
|---|---|
| `REG.*`, `PRU.FCR.*` | Layer 1 (regulatory) |
| `CO.RET.*`, `PRU.CO.*`, `PORT.*` | Layer 2 (company) |
| `CRED.*` | Layer 3 (credit) |

- **Buyout and top-up** are not separate products. They are personal-loan applications with `transaction: buyout` or `transaction: top_up`, so every personal-loan rule also applies. EOSB-backed lending works the same way, through the flag `uses_eosb_security: true`.

## 3. How a decision is made
1. The application runs through every `rules` entry whose `applies_to` matches it: Layer 1, then 2, then 3.
2. It also runs through the `prudential_rules` with scope `pre_approval`, using today's balance-sheet snapshot. These cover the book cap, single borrower, connected group, board members, related parties and the AED 1m per-individual cap.
3. Any portfolio **hold** in force also applies, for example gold above 5% of the book, or liquidity below 12%.
4. The outcome:
   - any failed knockout → **Decline**
   - else any failed refer → **Refer**
   - else → **Approve**
5. The recommended amount is the **lowest** of all caps, and the binding cap is shown.

## 4. How to change a value safely (maker-checker)
1. **Maker** (Credit Risk analyst):
   - Change the value in the YAML file. Keep the `# F-xx [tag]` comment.
   - If the value also appears in a rule `condition` or `limit`, change it there too. For example, the AED 300,000 cap sits in `credit_policy.yaml` and in CRED.PEA.002.
2. Run `python credit-policy-uae-finance-company/config/validate_config.py`. **Every check must be PASS or an explained FLAG; 0 FAIL.** The validator catches a value that is looser than the CBUAE or FCR, or that differs between files.
3. Update `03-parameter-sheet.md` and the policy document in the same change, so the documents and config never disagree.
4. **Checker** (Head of Credit, or CRO for prudential and portfolio limits): reviews the diff and the validator output, then publishes. Every decision is stamped with the policy version.
5. **Never edit** `regulatory_baseline` to make a rule pass. It changes only when the CBUAE or FCR changes, with Legal & Compliance sign-off.
6. **Launching a product:** set `cbuae_nol_received: true` for that product only when the CBUAE no-objection letter is on file. Record the letter reference in the change note.

## 5. Rule counts (129 rules)

**By layer**

| Layer | Customer rules | Prudential / portfolio rules | Total |
|---|---|---|---|
| 1 Regulatory (CBUAE + FCR) | 20 (REG.CB 12, REG.FCR 3, REG.STC 5) | 10 (PRU.FCR) | 30 |
| 2 Company | 26 (CO.RET) | 12 (PRU.CO 5, PORT 7) | 38 |
| 3 Credit | 61 (CRED) | — | 61 |
| **Total** | **107** | **22** | **129** |

**Layer 3 by product**

| Product | Rules | IDs |
|---|---|---|
| Personal loan, employer-assigned | 7 | CRED.PEA.001–007 (007 also covers non-assigned) |
| Personal loan, non-assigned | 6 | CRED.PNA.001, 001s, 002–005 |
| Buyout / top-up / rescheduling | 5 / 1 / 2 | CRED.BO.001–005, CRED.TU.001, CRED.RS.001–002 |
| Credit cards | 10 | CRED.CC.001a–c, 002, 003a–c, 004–006 |
| Auto loans | 7 | CRED.AL.001–007 |
| Gold-backed | 4 | CRED.GOLD.001–004 |
| EOSB as added security | 3 | CRED.EOS.001–003 |
| Salary advance | 8 | CRED.SA.001–004, 005a–c, 006 |
| BNPL (phase 2, off) | 4 | CRED.BNPL.001–004 |
| Home finance (not offered) | 1 | CRED.HL.001 (licence gate) |
| Fees, AI grade | 1 + 2 | CRED.FEE.001, CRED.GRD.001–002 |

**Layer 1 FCR rules:**
- Prudential: capital AED 150m (PRU.FCR.001), leverage 100% (002), liquidity 10% (003), single borrower 10% (004), connected group 15% (005), large exposure 7% (006), **no lending to board members** (007), shareholder / affiliate exposure 10% / 20% (008–009), no individual deposits (010).
- Customer level: AECB report before every credit (REG.FCR.001), **no-objection letter per product** (REG.FCR.002), no overdraft, deposit-backed or Islamic-window contracts (REG.FCR.003), short-term credit caps for salary advance and BNPL (REG.STC.001–005: ≤ lower of AED 20,000 or 3× net income, ≤ 12 months, no interest, fees ≤ 30%, bureau check from AED 5,000).
- Card income of AED 60,000 a year: REG.CB.002.

## 6. Sign-off items that change the config
Until these are approved, the config holds the proposed values. Each item maps to config entries as follows.

| Item | Tag | Config value | Where |
|---|---|---|---|
| F-02 | [R] [P] | Book cap AED 250m; early warning at 85% | `prudential`; PRU.CO.001–002 |
| F-03 | [R] [P] | AED 1m per individual | `prudential`; PRU.CO.004; approval matrix CRO limit |
| F-06 | [R] [P] | Liquidity trigger 12% | PRU.CO.003 |
| F-13, F-27 | [A] | Employer-assigned track (assignment letter + EOS undertaking + UAEDDS); repricing if salary moved | `tracks`; CRED.PEA.004 |
| F-16 | [A] | AECB 541 / nationals 500; non-assigned 560 (600 at AED 5,000); knock-outs | `aecb`; CO.RET.010–017 |
| F-17, F-18 | [A] | Statements 3 / 6 / 12 months; self-employed licence ≥ 2 yrs, PL cap 250k | `documents`, `self_employed`; CO.RET.020–031 |
| F-21, F-23 | [A] | Employer-assigned cap 300k (cat D 150k); 12.99–24.99% | CRED.PEA.002, 005; `pricing_grid` |
| F-29 | [A] | Grace ≤ 60 days (nationals) | CRED.PEA.006 |
| F-30, F-31, F-32 | [A] | Non-assigned AED 5,000 / 7,000 entry; 20× ≤ 250k / 10× ≤ 150k; 15.99–29.99% | CRED.PNA.001–005 |
| F-38 | [P] | Card tier caps 25k / 60k / 100k | CRED.CC.003a–c |
| F-40 | [A] [R] | Self-employed card: 3-month average balance AED 50k | CRED.CC.004 |
| F-43, F-44 | [A] | Auto max 500k; new 3.49–4.99%, used 4.49–5.99% flat | CRED.AL.002, 007 |
| F-49, F-50 | [A] | Gold LTV 70 / 80 / 85; AED 5k–250k; 14.99% | CRED.GOLD.001–003 |
| F-52 | [A] [R] | Salary advance: net 3,000 WPS; 50% ≤ 5,000; 35 days; fees 30 / 60 / 120 | CRED.SA.* |
| F-53 | [A] [R] | BNPL 10k / 1× / 6 m / fees ≤ 10%; **off** | CRED.BNPL.*; `offered_in_pilot: false` |
| F-55 | [A] | Home finance not offered (phase 2 max AED 3m) | CRED.HL.001; `offered_in_pilot: false` |
| F-56 | [B] [P] | Price floors cover funding + cost + loss + capital | `pricing_grid.floor_must_cover` |
| F-57 | [A] [R] | Approval matrix 100k / 300k / 750k / 1m / Board Credit Committee | `delegation_of_authority` |
| F-58 | [P] | Portfolio limits 35 / 25 / 5 / 5 / 2 / 25 / 5% | `portfolio_limits`; PORT.001–007 |

## 7. Validation result (run 2026-11-09)
`validate_config.py`: **76 checks: 73 pass, 3 flagged, 0 fail.**

**The 3 flags (intentional; each needs a decision, not a code fix):**
1. **CBUAE no-objection letters not yet on file.**
   - All 10 offered product entries have `cbuae_nol_received: false`: 6 product lines, plus the buyout, top-up, rescheduling and EOSB overlays.
   - Until a letter arrives, REG.FCR.002 declines every application for that product. This is the correct pre-launch state.
   - The worked examples run under a "launched" assumption.
2. **Salary advance has no minimum amount.**
   - For an advance below about AED 267, the AED 30 fee plus the AED 50 late fee would exceed the 30% legal cap.
   - REG.STC.004 already blocks any such case.
   - Proposal [P]: set a minimum advance (e.g. AED 300), or waive the late fee on advances under AED 267.
3. **Home finance (phase 2) maximum of AED 3m is above the AED 1m per-individual cap.**
   - The product is disabled now.
   - Before phase 2, decide between Board Credit Committee exceptions and raising the cap for secured home finance.

**Worked examples, evaluated through the rules by the validator:**

| Case | Result | Key numbers |
|---|---|---|
| **Mariam:** expat nurse, cat C, AED 6,500, AECB 585, AED 60k / 48 m, employer-assigned, grade 5 | **Approve** | 17.99% → AED 1,762 a month; DBR 34.8%; max 20× = AED 130,000 |
| Mariam on the non-assigned track | **Decline** (CRED.PNA.001) | AECB 585 < 600, so the entry salary is AED 7,000 |
| Mariam before the no-objection letter | **Decline** (REG.FCR.002) | Launch gate works |
| Mariam at AI grade 7 | **Refer** (CRED.GRD.001) | Model escalation; policy passed |
| **Ravi:** WPS worker, cat D, AED 3,500, AECB 610, salary advance AED 1,500 | **Approve** | Fee AED 60 + VAT = AED 63; max AED 1,750; DBR 42.9% |
| Ravi, second advance while one is open | **Decline** (CRED.SA.004) | One at a time, no rollover |
| **Khalid:** national, government, AED 18,000, buyout of AED 120k at 28% (36 m left) | **Approve** | 13.99% → AED 4,144 vs AED 4,964; saves AED 820 a month, AED 29,514 in total; no processing fee |
| Khalid without a signed cost comparison | **Decline** (CRED.BO.004) | Consumer Protection Standards |
| **Fatima:** self-employed, AED 25,000, gold AED 100k, AED 70k / 24 m (AECB 620 assumed for the test) | **Approve** | 14.99% → AED 3,394 a month; DBR 13.6%; top-up call only if gold falls 12.5% |
| Fatima at 75% LTV (peer level) | **Decline** (CRED.GOLD.001) | Our cap is 70% |
| **Arjun:** expat, cat C, AED 5,000, AECB 620, used car, AED 36,000 / 48 m | **Approve** | 4.49% flat → AED 885 a month; DBR 17.7% |
| **Sara:** expat, AED 9,000; obligations 3,200 + 1,000 (cards) + 600 (BNPL) | **Decline** (REG.CB.001) | DBR 53.3% before the new loan |
| Sara if BNPL were ignored | Would be approved | A lender blind to BNPL would lend about AED 9,606; the rule prevents this |
| BNPL plan during the pilot | **Decline** (CO.RET.000, REG.FCR.002) | Phase 2, off |
| Board member applies | **Decline** (PRU.FCR.007) | FCR prohibition |
| Liquidity at 11% of liabilities | **Held** (PRU.CO.003) | Internal trigger 12%; the legal 10% still met |

## 8. Points to confirm (interpretation, not errors)
- **AECB floor for cards and auto loans:**
  - Policy §7.2 puts "employer-assigned personal loans, cards, auto" in one row at 541 (nationals 500). F-16 in the parameter sheet mentions only the personal-loan tracks.
  - The config follows §7.2: CO.RET.014 applies 541 / 500 to cards and auto on both tracks.
  - Confirm, or raise non-assigned cards and auto to 560.
- **No BNPL score floor:**
  - The policy sets no AECB score floor for BNPL. The phase-2 BNPL product relies on the AECB report for every plan, DBR including all plans, the general knock-outs and the 3-plan cap.
  - Set a floor before launch if wanted.
- **FCR values:**
  - The FCR values (capital, leverage, liquidity, exposure limits, short-term credit caps) were read from search extracts, so their confidence is M (the rulebook page returned HTTP 403).
  - Legal & Compliance should confirm them against the rulebook. Also confirm whether the short-term credit caps bind a Part I company's salary advance; the config applies them anyway.
- **Pricing for grades 9–10:** no rate is set for these grades, as they are declined. PD bands 9 and 10 use the bank configuration's upper bounds (20% / 100%); the policy shows "≥ 12%" for both.

## 9. Mapping to the parameter sheet
| Parameter sheet | Config |
|---|---|
| F-01–F-08 (licence and prudential) | `bank_policy.yaml` licence_scope, prudential; PRU.FCR.*, PRU.CO.*, REG.FCR.* |
| F-09–F-19 (general) | `bank_policy.yaml` eligibility, tracks, employer_categories, aecb, documents, self_employed, affordability; CO.RET.*, REG.CB.001 |
| F-20–F-29 (employer-assigned) | products.personal_loan_employer_assigned; CRED.PEA.* |
| F-30–F-33 (non-assigned) | products.personal_loan_non_assigned; CRED.PNA.* |
| F-34–F-36 (buyout, top-up, rescheduling) | products.buyout / top_up / rescheduling; CRED.BO.*, CRED.TU.001, CRED.RS.*, REG.CB.008–009 |
| F-37–F-40 (cards) | products.credit_card; CRED.CC.*, REG.CB.002, REG.CB.007 |
| F-41–F-48 (auto) | products.auto_loan; CRED.AL.*, REG.CB.006 |
| F-49–F-55 (gold, EOSB, salary advance, BNPL, deposit, home) | products.gold_backed / eosb_backed / salary_advance / bnpl / deposit_backed / home_loan; CRED.GOLD.*, CRED.EOS.*, CRED.SA.*, CRED.BNPL.*, CRED.HL.001, REG.STC.*, CO.RET.000 |
| F-56–F-60 (pricing, matrix, portfolio, conduct, provisioning) | `bank_policy.yaml` pricing_grid, delegation_of_authority, portfolio_limits, consumer_protection, provisioning; CRED.GRD.*, PORT.*, REG.CB.010–012 |

## 10. Loading into a demo tenant
1. Create `banks/demo_finance_company/` with the conventional vocabulary profile and the finance-company prudential module switched on, for the snapshot variables in `rules.yaml`.
2. Copy `bank_policy.yaml`, `credit_policy.yaml` and `rules.yaml` there. In the product, move `regulatory_baseline` and the REG.* / PRU.FCR.* rules into `config/regulators/` (cbuae.yaml + fcr.yaml).
3. Run the validator: 0 FAIL.
4. Publish through maker-checker. The loader re-runs the tighten-only checks.
5. For each product, set `cbuae_nol_received: true` only when its CBUAE letter is on file.
