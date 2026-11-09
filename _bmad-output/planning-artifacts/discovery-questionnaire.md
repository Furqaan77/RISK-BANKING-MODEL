# Risk Banking Model: BMAD Discovery Questionnaire

**Phase:** BMAD 1-Analysis (Analyst "Mary") → 2-Planning (PM "John") → 3-Solutioning (Architect "Winston")
**Purpose:** Get full clarity before writing the Product Brief, PRD, Architecture, Epics and the **BMAD Build Prompt**.
**How to answer:** Answer in the chat rounds, or write your answer after `→` in this file. Answers are logged in
`discovery-answers.md`. "Rec." marks my recommended default if you have no strong view.

---

## A. Business & company (Product Brief)
- A1. What is the company / product name to use in the documents? →
- A2. Who is on the team (roles), and who will maintain the product after the build? →
- A3. Business model: annual licence per bank / fee per customer scored / subscription / share of ROI uplift / mix? →
- A4. First pilot client type: finance house / small conventional bank / Islamic bank / large bank? →
- A5. Is a specific pilot institution already lined up? If yes, how big is it (customers, loan book)? →
- A6. Who is the buyer inside the bank: CRO / Head of Retail / Head of Credit / CEO / CDO? →
- A7. Who uses it day to day: credit officers / risk analysts / relationship managers / management? →
- A8. What one result must the pilot prove: more approvals at the same risk / fewer defaults / faster decisions / ROI uplift in AED? →
- A9. Target date for a working demo, and for the first pilot? →
- A10. Competitors you know of (FICO, Experian, Moody's, AECB scores, local fintechs)? What makes us different? →
- A11. Markets after the UAE (Qatar, KSA, India, other GCC), and when? →
- A12. Is "increase ROI by ~2%" the headline claim we must be able to show with numbers? →

## B. Scope & use cases
- B1. Islamic finance products (murabaha, ijara, tawarruq, Islamic cards) in v1? →
- B2. Retail v1 products, confirm: personal loan / credit card / EOSB-backed loan / overdraft / salary advance / BNPL? →
- B3. Corporate v1: SME and large corporates both? What turnover separates SME from corporate? →
- B4. When is it used: new applications (origination) / existing book review (behaviour scoring) / both? →
- B5. Mode: batch upload of many customers / single application screen / both? →
- B6. Should it produce pre-approved offers (proactive limits for existing customers)? →
- B7. Should it flag existing customers who are deteriorating (early warning / watch-list)? →
- B8. Should it rank overdue customers for collections priority? →
- B9. Opportunity finder: show "customers your policy declines who are actually low risk" with the AED value? →
- B10. Risk-based pricing: recommend an interest / profit rate per grade? →
- B11. Limit increase recommendations for existing card holders? →
- B12. Self-employed individuals: in v1 or later? →
- B13. Retirees: in v1? →
- B14. Non-resident borrowers: in v1? →
- B15. Joint applicants / guarantors (retail): needed? →
- B16. Group exposure (corporate groups, related companies): needed in v1? →

## C. Policy & rules
- C1. What format is the bank's credit policy in (PDF / Word / Excel parameter sheet)? About how many pages and parameters? →
- C2. Who in the bank owns the policy, and how often does it change? →
- C3. Should a policy change in the tool require maker-checker approval (one person edits, another approves)? →
- C4. When a rule fails, can the bank approve as an exception (deviation)? Should the tool record who approved it and why? →
- C5. Should the tool route each case to the right approval authority by amount (delegation of authority matrix)? →
- C6. Employer categories: does the bank already have a list (government / semi-gov / blue-chip / A-B-C company lists)? →
- C7. DBR: gross salary including all allowances, or basic + fixed allowances only? →
- C8. Credit card obligation in DBR: 5% of limit / 5% of outstanding balance / other? →
- C9. DBR instalment for the new loan: at the actual rate, or at a stressed rate (rate + 2%)? →
- C10. EOSB-backed loans: what % of accrued EOSB can be lent, and after how many years of service? →
- C11. Minimum salary for personal loans and cards (now that CBUAE removed the AED 5,000 floor)? →
- C12. Age limits (min age, max age at maturity) for nationals and expats? →
- C13. Maximum total unsecured exposure per customer across all products (e.g. 20× salary in total)? →
- C14. Restricted nationalities: does the bank have a list? Decline or refer? →
- C15. Corporate: restricted or high-risk sectors (real estate, contracting, crypto, etc.)? →
- C16. Corporate minimum thresholds (e.g. min DSCR 1.25x, max Debt/EBITDA 4x)? Does the bank have them, or do we propose them? →
- C17. If the model's risk opinion and the policy disagree, which wins: policy always / model can raise to Refer / model can override? →
- C18. Should the bank be able to run "what-if" policy changes (e.g. DBR 45% vs 50%) and see the impact on approvals and risk? →

## D. Data
- D1. Bank core systems likely to be the source (T24, Finacle, Flexcube, others, unknown)? →
- D2. How will data arrive: CSV/Excel export / direct database read (Oracle, SQL Server) / API? →
- D3. How often: one-off analysis / monthly / daily / real-time per application? →
- D4. Expected volume: retail customers? corporate customers? →
- D5. How many years of history will the bank provide? →
- D6. Will the bank provide default outcomes (who defaulted) for training? →
- D7. The bank's definition of default (90+ DPD / write-off / restructured / other)? →
- D8. Will rejected applications be available (needed to correct the bias of only learning from approved loans)? →
- D9. Card / account transactions: raw transactions or monthly summaries only? →
- D10. Do transactions have merchant category codes (MCC) for spend-category analysis? →
- D11. AECB: does the bank store AECB scores and reports? Should we integrate with the AECB API later? →
- D12. Corporate financials: structured (spreadsheet / spreading system) or PDF statements needing extraction? →
- D13. Corporate collateral data: available with values and valuation dates? →
- D14. Will data include names / Emirates ID / phone numbers? Should the tool mask (pseudonymise) them on load? →
- D15. Who at the bank prepares the extract (IT / MIS / risk team)? Can we give them a template? →
- D16. Should we keep scored data inside the tool after a run, or delete inputs after scoring? How long is data retained? →
- D17. Can you get an anonymised real sample before the pilot to check column formats? →
- D18. OK to build and demo entirely on synthetic data until the pilot? →
- D19. Salary-credit data (monthly salary credits) available to measure income stability? →
- D20. Liability data (CASA balances, deposits) available for relationship features? →

## E. Scoring & modelling
- E1. Score scale: 0–1000 / 300–900 (like AECB) / PD % only / match the bank's own scale? →
- E2. Grades: 5 grades (A–E) / 10 grades (1–10) / map to the bank's internal rating scale? →
- E3. Does the bank have an internal rating scale we must map to? →
- E4. PD horizon: 12 months only, or lifetime too (for IFRS 9)? →
- E5. Who sets the Approve / Refer / Decline cut-offs: the bank, or our defaults? →
- E6. Starting scorecard weights: our expert defaults / the bank's existing scorecard / derived from data? →
- E7. ML method: gradient boosting + explanations (more accurate) / logistic regression only (simplest to explain to the regulator) / both with champion-challenger? →
- E8. Retraining: manual on request / quarterly / automatic when drift is detected? →
- E9. Model validation: the bank's validation team / an external validator / both? Do we produce a validation pack? →
- E10. Exclude nationality, gender, marital status and age from the ML model: confirm? →
- E11. Compute Expected Loss (PD × LGD × EAD) as well, or PD only? →
- E12. Stress tests per customer or portfolio (salary cut 20%, job loss, rate +2%, oil-price shock)? →
- E13. Portfolio view: concentrations by employer, sector, nationality group, product? →
- E14. Capture credit-officer overrides and use them to improve the model? →
- E15. Behaviour signals to include: spending volatility / gambling-type MCC / cash advances / salary delays / bonus-month behaviour / anything else from the call? →
- E16. Corporate dimension weights (35/20/15/10/20): keep as defaults, or set them yourself? →
- E17. Corporate: use stressed cash flow for limit sizing, and what stress (EBITDA −30%)? →
- E18. Minimum acceptable model quality before the ML switches on (Gini ≥ 0.30?) →

## F. AI / LLM
- F1. LLM preference: Llama / Qwen / Mistral / **Falcon (UAE, TII)** / **Jais (Arabic, UAE)** / no preference? →
- F2. LLM jobs: explain decisions / help convert policy PDFs into rules at onboarding / chat "ask the portfolio" / write credit memos? →
- F3. Explanation language: English / Arabic / both? →
- F4. Will banks have GPU servers, or must it run on CPU? →
- F5. Must every LLM sentence be checked against the facts (strict guardrail), even if that makes it plainer? →
- F6. Should the LLM draft a full credit memo (PDF) per customer for the credit file? →
- F7. Should customers ever see LLM text (e.g. decline reason letters), or is it internal only? →

## G. User experience
- G1. Login required? Single sign-on with the bank's Active Directory? →
- G2. Roles: viewer / credit officer / risk manager / admin (policy editor) / auditor? →
- G3. White-label each bank's logo and colours? →
- G4. Arabic interface (right-to-left) needed? →
- G5. Top 3 screens that matter most? →
- G6. Report outputs: Excel / PDF credit memo / PDF portfolio report / PowerPoint for the board? →
- G7. Manual single-customer entry form (for walk-in applications)? →
- G8. Management dashboard KPIs (approval rate, average grade, expected loss, ROI)? →
- G9. Demo mode with synthetic data for sales presentations? →
- G10. Web app in the browser (Rec.) or desktop app? →
- G11. Should the user see the full calculation (DBR maths, limit waterfall), or just results? →

## H. Deployment & security
- H1. Bank servers: Windows Server / Linux / unknown? →
- H2. Docker / containers allowed at the target banks? →
- H3. Fully air-gapped (no internet ever) or internet allowed for updates? →
- H4. Packaging: Docker image / Windows installer / Python package + script? →
- H5. Database for results and audit: SQLite (simple) / PostgreSQL / the bank's SQL Server or Oracle? →
- H6. Encryption of stored data at rest required? →
- H7. Audit log retention (years)? Export to the bank's SIEM? →
- H8. How do we deliver updates to an air-gapped bank (signed package via USB / secure file transfer)? →
- H9. Protecting our IP: licence keys / code obfuscation / compiled binaries / trust contract only? →
- H10. Will banks run a penetration test or security review before installation? →
- H11. UAE data law (PDPL) and CBUAE outsourcing / third-party rules: do we need a compliance pack? →
- H12. Remote support access to the installed system, or on-site only? →
- H13. Multiple banks on one machine (e.g. for a consultancy using it), or always one bank per install? →

## I. Governance & compliance
- I1. Produce model documentation to CBUAE Model Management Standards (development + validation docs)? →
- I2. Disclaimer: the tool is decision support and the bank remains responsible. Agreed? →
- I3. Must decline reasons be suitable to share with the customer (consumer protection)? →
- I4. Islamic products: Sharia-board review of the terms used (profit rate vs interest)? →
- I5. Bias / fairness testing report per model version? →
- I6. Record keeping: keep every decision with full inputs for how many years? →

## J. Build process (BMAD)
- J1. Build machine OS (Windows / Linux / Mac)? →
- J2. Who runs the build: you with Claude Code / a developer / a team? →
- J3. Tech stack: Python (Rec.) / other preference? UI: Streamlit (fast) / React + FastAPI (more polished, more work)? →
- J4. Source control: private GitHub / GitLab / none? CI (automated tests on each change)? →
- J5. Milestones: demo MVP → pilot-ready → production. Which do we plan in detail now? →
- J6. BMAD depth: full flow (brief → PRD → architecture → epics → stories → build) or a lighter quick-spec flow? →
- J7. Sprint length and how many stories per sprint? →
- J8. Test expectations: unit tests only / plus end-to-end / plus performance tests? →
- J9. "Done" for the demo MVP? →
- J10. Budget limits on hardware or paid tools (everything open source)? →

## K. Commercial & pilot
- K1. Include an ROI calculator (extra lending × margin − expected loss = extra income in AED)? →
- K2. Inputs we can use for ROI: funding cost, average lending rate, LGD assumptions: from the bank or our defaults? →
- K3. Pilot structure: parallel run on historical data first (Rec.), then live? →
- K4. NDA / data-processing agreement templates needed? →
- K5. Support model after go-live: SLA, response times? →
- K6. Training for bank staff: user guide / video / on-site training? →

## L. AI across the risk function (from `research.txt`: "AI in the Bank's Risk Function")
- L1. Product vision: a credit-risk tool only, or the first module of a risk-AI platform that grows across the 13 risk departments? →
- L2. After credit risk, which departments go on the roadmap, and in what order? Options: portfolio management / workout & early warning / retail collections / credit administration / model risk / operational risk & fraud / liquidity / IRRBB / market / counterparty / country / climate-ESG →
- L3. Document AI in v1: read corporate financial statements (PDF) and extract the numbers automatically? →
- L4. Generative AI drafts credit papers / committee memos for the analyst to review: v1 or later? →
- L5. Agentic annual review for corporates (pull financials → re-rate → flag changes → draft review): v1 or later? →
- L6. Hidden concentration discovery (borrowers sharing the same supplier, landlord, employer or commodity): v1 or later? →
- L7. Re-score the whole book nightly / monthly (continuous) vs only when someone uploads a file? →
- L8. Watch-list as a model output (early warning of deterioration before delinquency): v1? →
- L9. Collections: cure-propensity models and restructuring suggestions (dynamic forbearance): roadmap? →
- L10. Continuous model monitoring with automatic suspension when performance degrades: v1? →
- L11. Credit administration: extract covenants from loan agreements and track them: roadmap? →
- L12. News, sentiment or market feeds need outside data, which conflicts with "no internet". Allow an optional, one-way external feed, or none at all? →
- L13. Product principle "AI recommends, scores, drafts, flags; humans decide and are accountable": adopt it formally in the PRD? →
- L14. Should the banker PDF and pitch present this platform roadmap, or stay focused on credit risk only? →
