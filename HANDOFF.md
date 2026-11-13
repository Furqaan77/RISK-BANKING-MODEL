# HANDOFF: full project context

Written 2026-11-09, updated 2026-11-13, so a fresh Claude (other machine / other account) can pick up without the original chat.

## 1. What the product is
**AI Risk Score Card**: a credit risk model sold as a service per bank, run **privately on the bank's own machines**. It reads the bank's central-bank rules, bank policy and credit policy, and scores retail applicants.

How decisions work:
1. **Three layers of rules**: CBUAE (regulator) → bank policy → credit policy. A lower layer can only be **tighter** than the one above ("tighten-only").
2. Rules are **policy-as-config**: YAML files with plain comparisons only (no inline lookup tables, no code). Tiered limits are split into separate rules (for example CRED.CC.001a, 001b, 001c).
3. The AI model gives a **grade 1–10**. Grade ≥ 7 goes to a human (Refer). Grades 9–10 are declined. **The policy always wins** over the model.
4. Rule changes use **maker-checker** (one person proposes, another approves).
5. Rule IDs by layer: `REG.*` (regulatory), `PRU.*` (prudential, finance company only), `CO.*` (company), `PORT.*` (portfolio limits), `CRED.*` (credit, per product).

## 2. What was built, in order
1. **UAE Islamic edition**: BMAD plan, build prompt, banker PDF, visual walkthrough.
2. **Global edition (US + UK, large global bank)**: same set, plus income segmentation by fixed salary bands, and an 81-page combined PDF.
3. **Retail credit policy, UAE Islamic bank** (`credit-policy-uae/`): complete.
4. **Retail credit policy, UAE conventional bank** (`credit-policy-uae-conventional/`): complete. Same criteria as Islamic, converted to conventional terms.
5. **Market-position report** (`credit-policy-uae-conventional/market-position/`): the bank policy compared with 33 UAE banks, with charts and "how we stand out" scenarios.
6. **Retail credit policy, UAE finance company** (`credit-policy-uae-finance-company/`): complete (pilot finance company, conventional).
7. **Problem statement agreed** (13 Nov): banks decide credit on scattered, hard-to-verify information; staff can't get citable answers; assessment is slow and inconsistent. Answer: an on-prem AI Credit Risk Assessment Platform (grades 1–10, internal + external data via controlled APIs, regulator → bank → credit policy engine where policy beats AI, higher risk goes to a human, plain-English Q&A with citations). Indicative AI share: ~80–90% of routine retail work, ~60–70% corporate/SME; humans handle the last 10–30%.
8. **Faisal's direction** (mentor meeting, `Research work/`): master rulebook of US/UK/UAE central-bank rules for retail, SME, corporate and finance houses, plus a comparison of ~4 real banks per market ("too rigid / too risky / missed opportunities"). Later: risk appetite (e.g. NPL 1% vs 2%), then legal/compliance/risk experts, then a business expert.
9. **Master rulebook** (`master-rulebook/`): Excel tool with live labels (12 banks: ENBD, FAB, ADCB, Mashreq; HSBC UK, Barclays, Lloyds, NatWest; JPMorgan Chase, BofA, Wells Fargo, Citi), finance-house / SME / corporate rulebooks, 379 sources, and 12 one-page bank checks (PDF). Rebuild: `python tools/master-rulebook/build.py`.
10. **BMAD research runs** (`_bmad-output/planning-artifacts/research/`): run 1 retail (complete, `research.md` written); run 2 finance houses / SME / corporate (digests complete, `research.md` synthesis **not yet written**).
11. **Platform blueprint** (`_bmad-output/planning-artifacts/blueprint/`): six capabilities (Decide, Monitor, Stress, Benchmark, Explain, Govern), architecture rules AD-17..AD-22, demo spec, roadmap (Skeleton → Muscles → Organs → Nerves → Skin → Blood supply). PDF built by `tools/blueprint/build_blueprint_pdf.py`.
12. **Working skeleton** (`risk-platform/`): Python, only needs PyYAML. A fictional "Demo Group" bank (UAE/UK/US) with 9 planted problems; all 9 detected, 6/6 tests pass. See `risk-platform/README.md`.

Published walkthrough pages (claude.ai artifacts, owned by the original account, may not be visible on another login):
- UAE: https://claude.ai/artifact/5cXyJktuz1fxfgfp7JXCcT
- Global v2: https://claude.ai/artifact/LaUXTi4DCT79vtzvHMvmsZ

## 3. The retail credit policy criteria (the user's basic criteria)
- Nationals and expats. Minimum salary AED 5,000. Age per CBUAE. Minimum service 3 months.
- Salary transfer (STL) **not required** for the bank policies. All employers accepted.
- Amount, term and debt-burden ratio (DBR) per CBUAE. Pricing at mid-market.
- Secured products: against the salary (salary-transfer / employer commitment) and unsecured without salary transfer.
- Home loans per CBUAE rules. Auto at mid-market. Deposit / gold / end-of-service-benefit backed lending at 90%.
- Salary-transfer confirmation and end-of-service undertaking. Check the last year of bank statements and financials where possible.
- Buyout and top-up facilities included.

## 4. Key UAE rules used (verify before relying)
- **CBUAE Reg 29/2011:** loan ≤ 20× salary, ≤ 48 months, DBR 50% gross (30% for retirees). Auto 80% LTV, 60 months. Top-up after 12 clean months.
- **Mortgage regulation:** LTV 85/80 (first home, nationals/expats), 75/70, 65/60, off-plan 50%; 25 years.
- **Fee caps (Res 96/2019):** early settlement 1%, max AED 10k. Late fees: personal ≤ 200, auto ≤ 500, home ≤ 700, card ≤ 230, all ex-VAT.
- **Consumer protection:** key facts statement, 5-business-day cooling-off, post-dated cheques ≤ 120%, no blank cheques, disbursement within 10 days.
- **AECB credit report** required. **IFRS 9:** significant increase in credit risk at 30 days past due, default at 90.
- **Finance Companies Regulation C 3/2023 (FCR):**
  - capital AED 150m
  - liabilities ≤ 100% of capital funds in years 0–2
  - single borrower ≤ 10%, group ≤ 15%
  - no lending to board members
  - liquid assets ≥ 10% of liabilities
  - no deposits from individuals, no Islamic window
  - CBUAE no-objection letter per product
  - BNPL: ≤ lower of AED 20k or 3 months' net income, ≤ 12 months, no interest, fees ≤ 30%
  - cards need AED 60k annual income

The FCR values came from search extracts because the CBUAE rulebook site blocked access. They are **medium confidence**. Legal and Compliance must confirm them (10 points are listed in the finance-company gap report).

## 5. Results at a glance
- **Islamic bank policy:** 54 parameters, 31 Near peers / 17 Slightly off / 6 Far (vs top-5 UAE retail banks).
- **Conventional bank policy:** 55 items, 46 Near / 4 Lenient edge / 5 No peer / 1 n/a. Market position: easier to qualify than all 16 conventional banks with data (5th of 22 overall), price at the market middle, 9th of 22 overall. One weaker measure: home fixed rate 4.24% vs 3.99% median. A 3.99% rate for salary-transfer customers would move it to 6th (an option for the pricing committee, not in the policy).
- **Finance company policy:** 60 items: 38 Near / 4 Tighter / 3 Competitive edge / 5 No FC peer / 8 Required by FCR / 2 Not offered. Personal-loan rates 12.99–24.99% (employer-assigned) and 15.99–29.99% (non-assigned) by grade. The model rules have 129 rules and the validator gives 76 checks: 73 pass, 3 flagged, 0 fail.

## 6. Open items (need human decisions)
- **Islamic [A] sign-offs:** P-04, 06, 10, 21, 31, 39, 52, 53.
- **Conventional conversions to confirm:** late fees, credit life insurance, overdraft option. Also the military/armed-forces 60-month exemption, 30-year home-rate relief, and cooling-off days.
- **Finance company: 26 sign-offs** (20 [A], 6 [P]). Main ones: AED 250m pilot book cap, AED 1m per individual, portfolio limits.
- **3 validator flags (finance company):**
  1. no CBUAE no-objection letters on file yet, so all products decline until they arrive (correct pre-launch);
  2. salary advance needs a minimum amount (below about AED 267 the fees break the 30% cap; proposed AED 500);
  3. the home-finance phase-2 cap (AED 3m) clashes with the AED 1m per-customer cap.
- **Finance company: conflicts between files:**
  - AECB floor for cards and auto (policy §7.2 says 541 / nationals 500; parameter F-16 covers personal loans only);
  - no BNPL AECB floor set;
  - AI grades 9–10 provisioning bands differ between the policy and the bank config.
- **Data conflicts in market research:** Emirates Islamic minimum salary 7,500 vs 5,000; ADIB rate basis unclear; CBD, CBI and Wio figures disagree; Citi UAE does not sell retail; Tabby holds an SVF licence only. Some bank figures come from comparison sites (the CSVs carry a confidence column: H / M / L).
- **CBUAE items marked "verify"** in the policy documents. The minimum-salary removal of Nov 2025 is press-reported only.

- **Bank internal policies will be supplied by the user** (pasted in later). Only ~20% of what a credit decision needs is public (regulator rules ~100%, bank policy ~10–20%, credit policy ~20–30%; corporate and compliance ~5–10%). Do not research or invent internal bank policies.
- **Master rulebook to verify:** US card late-fee safe harbor (disputed), SR 26-2 scope for AI models, HSBC/Barclays mortgage max age, UAE minimum-salary removal, UAE real-estate cap. Open the xlsx once in Excel to confirm the formula labels calculate.

## 7. Where things came from
- User answers to about 100 discovery questions are in `_bmad-output/planning-artifacts/discovery-answers.md` (UAE) and `_bmad-output/large-bank/planning-artifacts/discovery-answers.md` (Global).
- `research/research.txt` is the user's extra research document.
- Regulatory research is in `docs/regulatory/`.
- `archive/` holds v1 files that were superseded.

## 8. How to rebuild PDFs and charts (`tools/`)
- The scripts turn Markdown into HTML, then print to PDF with **headless Chrome**:
  `chrome --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=<ms> --print-to-pdf=<out.pdf> --user-data-dir=<a separate profile folder> <html>`
  Use a **separate `--user-data-dir` for each build**, or Chrome may not write the PDF.
- Word files are made with python-docx (no pandoc).
- `pypdfium2` renders PDF pages to PNG for a visual check of blank or overflowing pages.
- Scripts were written on Windows. Paths inside them (scratchpad, project folder) are **hard-coded** and need editing for the new machine.
- Needed Python packages: PyYAML, matplotlib (or the chart code used in each script), python-docx, pypdfium2, pypdf (merge).
- `tools/policydoc/build_policy*.py` build the three policy PDFs and DOCX. `tools/creditpolicy*/` build the gap reports. `tools/marketpos/` builds the market-position report. `tools/combine/` builds the 81-page pack.
- Some scripts in `tools/` are drafts or one-off patches (`patch*.py`, `*_draft.py`, `*_template.py`). Do not assume they run cleanly.

## 9. How to continue
- **Finance company:** resolve the sign-offs and flags above, then update `03-parameter-sheet.md`, `05-retail-credit-policy.md` and `config/` together, and rerun `config/validate_config.py`.
- **Building the real product:** run the BMAD build prompts (`BMAD-BUILD-PROMPT.md` for UAE Islamic, `BMAD-BUILD-PROMPT-GLOBAL.md` for Global) on the separate build machine. They were written to run there directly.
- **New markets or products:** copy a credit-policy pack and follow the numbered pattern.
- **When you change a value,** update the parameter sheet, policy document, config and gap report together. Rating counts in each parameter sheet must add up.
- **Next agreed steps (13 Nov):** (1) build a policy intake template + converter into `risk-platform/packs/` YAML with the tighten-only check, ready for the bank policies the user will paste; (2) write the run-2 `research.md` synthesis; (3) light public-rules research for collections/recovery, trade finance, Islamic corporate and financial-crime screening.
