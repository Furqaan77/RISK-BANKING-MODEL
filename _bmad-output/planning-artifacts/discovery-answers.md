# Risk Banking Model: Discovery Answers Log

Answers captured during BMAD discovery (started 2026-11-06). Question IDs refer to `discovery-questionnaire.md`.

## Decisions already made (before discovery)
- Segments v1: retail AND corporate/SME
- Regulator: CBUAE (UAE). Bank credit policy supplied by the client; CBUAE rules researched (PROMPT.md Appendix A)
- Interface: local web dashboard
- AI: policy rules + scorecard, ML model, local LLM explanations
- Test data: synthetic until real data is available
- Outputs: risk score + ranking, decision + reasons, recommended limit
- LLM hardware: assume a GPU server at the bank
- Build happens on a SEPARATE machine; do not assume this PC's specs
- Research inputs: transcript, whiteboard, "Bank's Credit Assessment Framework" PDF, research.txt (AI across 13 risk departments)

## Discovery rounds
### Round 1: Business
- A1 Name: **AI Risk Score Card**
- A3 Pricing model: not decided yet (leave out of PRD)
- A4/A5 First pilot: **Islamic bank** (no specific institution named) → Islamic products/terminology matter in v1
- A6/A7 Buyers/users: CRO/Head of Risk, credit officers/analysts, relationship managers, management/CEO
### Round 2: Business
- A8 Pilot must prove: fewer defaults; more approvals at the same risk; faster decisions; ROI uplift in AED; **AND serve the low-salary category** (financial inclusion)
- A9 Demo date: no fixed date (plan by milestones)
- A10 Differentiators: on-premise/private; built on the bank's own policy; finds missed opportunities; Islamic-finance native
- A11 Expansion after UAE: Qatar, Saudi Arabia, other GCC → regulator layer must be pluggable per country
### Round 3: Islamic & scope
- B1 Islamic retail products in v1: personal finance (Tawarruq/Murabaha); Islamic credit card; auto/goods Murabaha; **Ijara/home finance** → auto + home finance CBUAE rules (LTV/tenor) now IN v1 scope
- B1b Terminology: **Islamic only** (finance amount, profit rate, customer/obligor); no conventional switch in v1
- B3 Corporate v1: SME finance + large corporates + sole proprietors on owner salary (all three)
- B4/B5 Usage: new applications AND existing-book review; batch upload AND single-application form
### Round 4: Features & customer types
- B6–B11 v1 features: opportunity finder; pre-approved offers; early warning/watch-list; risk-based profit rate; card limit increases; policy what-if simulator
- B8 Collections priority: NOT v1 → roadmap
- B12–B14 Retail customer types v1: self-employed; retirees/pensioners; non-residents; low-salary segment
- B15/B16: joint applicants/guarantors AND corporate group exposure in v1
- NOTE: v1 scope is now broad → phasing (MVP → pilot → full) to be agreed in section J
### Round 5: Policy control
- C1/C2 Policy format: BOTH a PDF/Word manual and an Excel parameter sheet → support both import paths
- C3/C4 Controls: maker-checker for policy edits; record exceptions/deviations; version history; user note "based on credit risk scoring" (interpretation: deviation eligibility and authority depend on the risk grade; confirmed in round 6)
- C5 Approval authority: **full workflow** (route cases to approver queues inside the tool) → requires auth, roles, queues
- C6 Employer classification: starter UAE list by us, overridden by the bank's own lists
### Round 6: Affordability rules
- C4b Exceptions: the grade decides BOTH whether a deviation is possible AND which authority approves it
- C7/C8 DBR income basis: **basic + housing only** (conservative). Card obligation % configurable (default 5% of limit)
- C9 Affordability profit rate: configurable stress add-on (default 0)
- C10/C11 Low-salary segment: bank sets the threshold and caps in config; no special model
### Round 7: Limits & restrictions
- C10 EOSB-backed finance: bank decides; configurable; demo default ≥ 5 yrs service, up to 80% of accrued EOSB
- C12 Age (demo): market typical, minimum 21 for all; max at maturity 65 (expat) / 70 (national)
- C13 Total unsecured exposure cap: **20× income across all unsecured products**
- C14/C15 Restricted nationality → Refer (not Decline); restricted sectors list for corporate (incl. Sharia-prohibited); opportunity finder reports what each restriction costs
### Round 8: Corporate policy, conflicts, simulator, data input
- C16 Corporate thresholds: the bank will provide (no proposed defaults; leave empty until received)
- C17 Model vs policy: **policy always wins** (model ranks; clarified in round 9)
- C18 What-if simulator: CRO/risk managers only; shows approval-rate change, expected-loss change, income/ROI change
- D1/D2 Data input: **API from bank systems + direct read-only DB connection** (CSV clarified in round 9)
### Round 9: Clarifications, systems, frequency
- C17b Policy pass + model grade E → **Refer to officer**. Policy decides Approve/Decline; the model can only escalate a pass to Refer (and drives the exception authority per C4b)
- D2b User answer: "it should read from credit policy of the bank" (re-asked in round 10)
- D1 First connector target: **Temenos T24/Transact**
- D3 Scoring frequency: **real-time per application** (API)
### Round 10: Data input clarified
- D2c Read the bank's credit policy file directly (PDF/Word + Excel) AND derive the required customer data fields from the policy
- D2d CSV/Excel customer upload: **No** (integration only). Demo and synthetic data load into a local DB that mimics T24/the data warehouse
- D3b Bulk re-score of the existing book: **nightly** (early warning, pre-approved offers, opportunity finder)
- D4 Pilot size: < 100k retail customers
### Round 11: Training data
- D5/D6 History: 1–2 years with defaults (validation weaker; use out-of-time carefully)
- D7 Default: 90+ DPD within 12 months
- D8 Rejected applications: **Yes**, available → reject inference possible
- D9/D10/D19/D20 Behaviour data: raw card/account transactions (with MCC), monthly summaries, salary-credit history, CASA/deposit balances → support raw transactions AND aggregates
### Round 12: Bureau, corporate data, PII, samples
- D11 AECB: read the bank's stored AECB data now; optional direct AECB API connector later (an outbound exception to the offline rule; must be optional/off by default)
- D12/D13 Corporate: spread financials from a system + PDF statements (document AI extraction needed) + collateral register
- D14/D16 PII: mask names/Emirates ID on load (role-based reveal); encrypt at rest; keep everything (no auto-purge; bank controls retention)
- D15/D17/D18 Data path: synthetic now; user will try for an anonymised real sample; we give bank IT a field template derived from the policy
### Round 13: Scale, grades, measures, weights
- E1 Score scale: the bank's own scale (configurable)
- E2/E3 Grades: **10 grades (1–10)**, PD bands configurable (supersedes A–E in PROMPT.md/banker PDF)
- E4/E11 Measures: **12-month PD only** per customer (no lifetime PD or per-customer EL). NOTE: the what-if simulator and ROI need a portfolio-level LGD assumption (confirm in K2)
- E5/E6 Weights/cut-offs: our expert defaults → replaced by the bank's scorecard → refined from data
### Round 14: ML method & governance
- E7 ML: **gradient boosting only** (with per-customer feature contributions for explanations)
- E8 Retraining: **automatic on drift**; activating a new model still needs human approval
- E9 Validation evidence: validation pack per model + CBUAE Model Management docs + exportable pack for external validators
- E10 Fairness: exclude nationality, gender, marital status, religion; **age allowed** as a model feature
### Round 15: Stress, concentration, overrides, signals
- E12 Stress scenarios: income cut; job loss/sector layoffs; profit-rate rise; oil/macro shock. User additions:
  - nationality-based scenario (scope clarified in round 16)
  - behaviour change in card spending habits
  - industry trend changing; profession in decline; job-skills decline
  - sudden purchase of expensive cars; excessive luxury spending
  - **"new expenses that don't connect the dots with salary and income"** → lifestyle-vs-income mismatch detection is a KEY capability
- E13 Concentration views: by employer; by sector; by product/grade; hidden links via AI clustering. User addition: **"remove high risk customers and corporates and individuals"** → de-risking / exit list (clarified in round 16)
- E14 Overrides: record with reason; override reports by officer/branch/grade; feed outcomes into learning
- E15 Behaviour signals: spending pattern & volatility; salary delays/irregularity; card utilisation & cash advances; spend location/MCC
### Round 16: Clarifications
- E12b Nationality-based stress: **dropped**
- E13b De-risking actions for existing high-risk customers: reduce limits; tighten collateral/covenants (corporate). No exit list, no blanket stop on new finance
- E15b Lifestyle-income mismatch: spend > income alert; sudden big purchases vs own history; hidden-income/fraud flag → refer to compliance (AML out of scope); trend vs peers (same salary band/profession)
- E12c Profession/industry decline: a bank-maintained table AND signals learned from the bank's own book
### Round 17: Corporate model & LLM
- E16/E17 Corporate: keep weights 35/20/15/10/20 and EBITDA −30% stress as configurable defaults
- F1 LLM family: **Qwen / Llama**
- F2/F6 LLM jobs in v1: explain each decision; draft credit memo/paper; ask-the-portfolio chat; read policy PDFs into draft rules (human review)
- F3/G4 Language: UI in English; explanations/memos in **English + Arabic**
### Round 18: LLM safety, access, UI
- F4/F5 LLM: strict number guardrail; humans approve memos (LLM memo = draft until signed); assume a GPU server. (Chat read-only not selected; clarified in round 19)
- F7 AI text is **internal only** (never customer-facing)
- G1/G2 Access: Active Directory/SSO; standard role set as default; roles configurable per bank
- G3/G10 UI: white-label per bank; browser web app. ("Show full calculations" and "demo mode" not selected; clarified in round 19)
### Round 19: Chat, detail, demo, priority screens
- F2b Portfolio chat: user chose "can act directly" → conflicts with maker-checker (C3) and CBUAE model governance; middle ground offered in round 20
- G11 Detail: summary + drill-down (DBR maths, every rule, limit waterfall on click)
- G9 Demo: **demo mode in the product** (synthetic "Demo Islamic Bank" tenant with T24-like data)
- G5/G6 Priority screens: application decision screen; approval queue/workflow; portfolio & early-warning dashboard; management KPI & ROI dashboard
### Round 20: Chat boundary & deployment
- F2c Chat acts directly only on **safe actions** (reports, what-ifs, re-scores, filters). Policy, decision and model changes become maker-checker requests
- H1/H2/H4 Install: **both** Docker (primary) and a Windows installer (fallback)
- H3/H8 Network: bank decides → support fully air-gapped (signed offline update packages) AND outbound-for-updates mode
- H5/H6/H7 Storage: PostgreSQL by default, with support for the bank's SQL Server/Oracle; encryption at rest. SIEM export not selected (audit stays in-app)
### Round 21: IP, compliance, support, governance
- H9 IP protection: signed licence key per bank (bank ID + expiry). No obfuscation, no escrow
- H10/H11 Onboarding packs: security pack; UAE PDPL data-protection pack; CBUAE outsourcing/third-party due-diligence pack; Sharia compliance note
- H12/H13 Support: remote (bank-approved sessions) AND on-site, per bank. Tenancy: **multi-bank install option** supported (strict data isolation per bank tenant)
- I1–I6 Governance: decision-support disclaimer; decision-record retention; replay any past decision exactly; fairness report per model (monitoring only)
### Round 22: Build process
- J1/J2 Builder: **a developer team** using BMAD (Claude assists) → the BMAD build prompt must serve humans and agents, with stories that can be assigned to people
- J3 Stack: **Python FastAPI + React**
- J4 Repo: private GitHub + CI
- J5/J6 Phasing: **3 releases**: R1 Demo MVP (retail scoring + decision screen + demo mode); R2 Pilot (corporate, workflow, T24, ML, LLM); R3 Full (early warning, opportunity, what-if, chat, compliance packs)
### Round 23: Team & quality
- J2b Team: **6+ developers** (multiple squads) → epics split so squads can work in parallel
- J7 Sprints: 2 weeks
- J8 Testing: unit tests on all rules and maths; end-to-end; performance (real-time API latency, nightly 100k re-score); security tests in CI
- J9 R1 "done": a retail applicant scored end-to-end; Demo Islamic Bank tenant; decision screen with drill-down; risk ranking of the book
### Round 24: Commercial & vision
- K1/K2 ROI inputs: bank supplies funding cost, profit rates and LGD per product; we provide defaults until then (resolves the E4 LGD dependency)
- K3 Pilot: **parallel run first**, then go live
- K4–K6 Commercial readiness in plan: NDA/DPA templates; support SLA definition; training materials
- L1/L14 Vision: **platform, credit first**. AI Risk Score Card is module 1; the architecture leaves room for other risk departments. The pitch stays focused on credit (roadmap not shown to banks yet)
### Round 25: Roadmap & AI ops
- L2 Roadmap after credit (priority order): retail collections & recoveries → credit administration (document AI) → model risk/validation → operational risk & fraud
- L3–L5 Doc/GenAI: PDF financials extraction in R2; credit memo drafting in R2; agentic annual review starts in R3 (basic) and completes in R4+ (user selected both)
- L10/L11 Monitoring: **auto-suspend ML + scorecard fallback + alert** on accuracy/drift breach
- L12 External data: optional inbound feeds, off by default; customer data never leaves (except AECB API if the bank enables it)
### Round 26: Principles, Sharia, outputs
- L13 Formal principle: **"AI recommends, scores, drafts and flags; bank staff decide and are accountable"**: in the PRD, UI disclaimers and pitch
- I4b Islamic specifics: no compounding late charges (late amounts go to charity, excluded from ROI income); profit rate/finance amount wording and maths; Sharia-prohibited sectors auto-declined (corporate); product-structure checks (Tawarruq/Murabaha asset step recorded; Ijara ownership rules)
- Docs: update the banker PDF; replace PROMPT.md with a new BMAD build prompt; keep the old files (archived unchanged)
- Planning deliverables: product brief + PRD; architecture; epics & stories by release; BMAD build prompt

## Discovery complete: 26 rounds, 104 questions asked (2026-11-07)
