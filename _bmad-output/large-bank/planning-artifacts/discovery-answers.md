# AI Risk Score Card: Large Bank (NYC or London) Discovery Answers Log

Track started 2026-11-07. Goal: repeat the UAE Islamic-bank process (research → 100+ questions → brief, PRD,
architecture, epics, BMAD build prompt, banker PDF, walkthrough page) for a large New York or London bank.
Jurisdiction choice (Fed vs Bank of England) is based on the research comparison; the user asked for whichever
has the easier regulations and execution.

Reference examples named by the user: HSBC (London), JPMorgan Chase (New York). These are illustrations of bank
size only. The product is never branded or modelled as a specific bank.

## Discovery rounds
### Round 1: Product, bank type, segments, use cases
- LB-A1 Relationship to UAE product: **completely separate product** (own codebase)
- LB-A2 First target: **global systemic bank (GSIB)**, HSBC/JPMC scale. Long vendor onboarding expected
- LB-A3 Segments: retail cards & personal loans; mortgages & auto; SME/business banking; corporate & commercial. User additions:
  - **blue-collar segment**
  - **new-to-bank juniors / Gen Z, including under-18s**. Legal constraint: minors cannot hold credit in their own name in the UK or US; US CARD Act limits under-21 cards. Approach clarified in round 2
- LB-A4 Jobs: underwriting decision support; challenger model / 2nd line; early warning & portfolio monitoring; fair-lending & explainability. User addition: **highlight macro and external risks: war, natural calamity/disasters, recession, redundancy** → macro/climate/geopolitical scenario module
### Round 2: Juniors, blue-collar, name, macro risk
- LB-A3b Gen Z / juniors: **credit-readiness score for under-18s (no credit given)** + **authorised user / guarantor** routes where the law allows. No direct credit to minors
- LB-A3c Blue-collar: score irregular income fairly (shift/overtime/gig, cash-flow based); thin-file/no-bureau scoring (rent, utilities, bank data with consent); smaller, safer starter products that grow; redundancy/job-loss risk in affordability. User example: **one-month salary advance as a loan + credit card with a capped limit**
- LB-A1b Product name: **AI Risk Score Card Global**
- LB-A4b Macro & external risk: portfolio stress scenarios (recession, rate shock, unemployment, war/sanctions, pandemic); climate & disaster exposure of collateral and borrowers; sector & job-loss early warning; **live (point-in-time) adjustment of scores** with macro indicators
### Round 3: Jurisdiction, salary advance, starter card, juniors
- **Jurisdiction: BOTH US (Fed/OCC/CFPB + New York) AND UK (PRA/FCA/BoE) from day one** (user overrode the UK-first recommendation) → two regulator packs in v1; see jurisdiction-comparison.md
- LB-A3d Salary advance: the model scores eligibility and amount only; **pricing from bank policy** (UK HCSTC caps and US MLA/state small-dollar rules become pack gates if pricing crosses thresholds)
- LB-A3e Capped starter card: low starting limit; grows with good behaviour (fresh affordability check at each increase); customer-chosen spending controls (e.g. block gambling); persistent-debt protection. User addition: **use credit-bureau history: Equifax, Experian, TransUnion (US: FICO/VantageScore; UK: CRA files)**, bureau-agnostic adapters
- LB-A3f Under-18 credit readiness: junior-account habits (parent consent); financial-education signals; pre-assessed starter offer at 18 (full affordability check); parent-linked view. User addition: **help Gen Z 16–18 build a good credit history** → US: authorised-user tradelines reported to bureaus; UK: credit files start at 18, so internal readiness record + guided credit-building plan from 18 (e.g. starter card, rent/utility reporting with consent)
### Round 4: Win reason, fit, pilot, first products
- LB-A6 Why a GSIB buys: underserved segments (blue-collar, thin-file, Gen Z); explainable AI + fair lending; macro & climate early warning; on-prem and fast to validate. User addition: **capture Gen Z students (16–18, school/university) as future customers via strong loyalty programmes**. Legal guardrail: UK CCA s.50 makes it an offence to invite minors to borrow; US CARD Act 1026.57 bans campus inducements for cards; loyalty is for non-credit products before 18 / credit eligibility
- LB-C2 Fit with existing decision engines: **both modes** (API add-on to FICO/Experian/SAS/Pega engines AND full decision engine). User addition: **AI-based risk decisions plus more value-added services so banks choose us over their own models; recommend the best** (menu in round 5)
- LB-A8 Pilot: back-test → challenger → limited live
- LB-B First products (all four): credit cards incl. starter card; personal loans + salary advance; mortgages; SME & corporate. User addition: **design competitive products for Gen Z and blue-collar**
### Round 5: Value-added services & headline
- LB-VAS1 Risk services v1: macro/climate stress engine; fair-lending & LDA search; model-risk "validator in a box" (for our AND the bank's models); early-warning & collections cure. User addition: **show opportunity-loss segments, not only risk**: the risk vs opportunity trade-off (approvals, profit, loss per policy option, efficient frontier)
- LB-VAS2 Growth services v1: inclusion engine (cash-flow / rent / utility / Open Banking); product designer (AI proposes terms and simulates loss and profit); next-best-offer & customer lifetime value; Gen Z loyalty & readiness (non-credit before 18)
- LB-VAS3 Operations services v1: document AI for commercial; income & fraud consistency; regulatory notice generator (deterministic reasons); policy copilot
- LB-VAS4 Pitch headline: **"Better than your champion model"** (challenger beating the bank's scorecards on accuracy AND fairness), with inclusion, explainability and macro early warning as proof points
- NOTE: v1 scope is very large (2 markets × all segments × 12 services) → phasing to be agreed in section J
### Round 6: Integration & data
- LB-D1/D2 Integration: real-time scoring API (called by FICO/Experian/Pega/in-house engines); batch from the data platform (Snowflake/Databricks/Teradata/Oracle); event streaming (Kafka) for early warning; SFTP file drop for pilots/back-tests. (UAE track had no file upload; GSIB pilots need it)
- LB-D3–D5 External data: credit bureaus (Equifax, Experian, TransUnion; FICO/VantageScore in US; UK CRA files); Open Banking/cash-flow (UK consented; US aggregators, 1033 rule in flux); income & employment verification; rent/utility/telecom
- LB-D14 Macro data: Fed/BoE stress scenarios + NGFS climate; physical climate maps by ZIP/postcode; labour & sector data (BLS, ONS); geopolitical/sanctions events (offline import or optional feed)
- LB-D12 Residency: **separate US and UK installs**; no cross-border data access
### Round 7: Measures, models, PIT/TTC, fairness
- LB-E1–E3 Outputs: 12-month PD + grade (bank master scale); **LGD, EAD, expected loss** per customer; **UK affordability verdict** (separate, CONC 5.2A). Lifetime PD NOT in scope (bank IFRS 9/CECL models consume our 12m PD)
- LB-E4 Models: constrained GBM + explainable boosting/GAM + logistic scorecard, **champion-challenger, best on accuracy AND fairness wins**
- LB-E8/E9 Macro: **two scores**: through-the-cycle for decisions; point-in-time macro-adjusted PD for monitoring, pricing and stress
- LB-E10 Fairness: US AIR + LDA search (BISG for testing only); UK Equality Act testing in a segregated monitoring zone. **Mandatory regardless (legal):** US 62+ never negatively scored; UK age only with justification; proxy detection (NY 296-a group-statistics ban, Equality Act s.19)
### Round 8: LLM & platform & outputs
- LB-F1/F2 LLM jobs: explain decisions (internal); draft customer letters (US adverse action / UK decline) from deterministic reasons with compliance-approved templates and human sign-off; credit memos & policy copilot; portfolio & risk chat (safe actions only)
- LB-F3/F4 LLM infra: **plug into the bank's own approved LLM platform** and/or on-prem GPU servers. Risk note: US regulators reportedly question China-origin AI and the DOJ data rule applies → recommend US/EU-origin open models when we supply the model. Template fallback kept (decisions never depend on the LLM)
- LB-G2/H1 Platform: **air-gapped option + any connectivity mode** (API, batch, streaming, SFTP)
- LB-G5 Key outputs: champion vs challenger report; risk-vs-opportunity frontier; regulator packs (SR 26-2/SS1/23, fair-lending, Consumer Duty MI, DPIA); board & CRO dashboard
### Round 9: Platform basics, notices, retention, governance packs
- LB-G2b Platform: enterprise SSO + roles (Entra ID/Okta/Ping, maker-checker, audit); Kubernetes/OpenShift (Helm), Docker for smaller banks; bank HSM/vault for keys; US/EU-origin LLM option as the US default when the bank has no own model
- LB-I4/I5 Notices: **we generate the content (US Reg B/FCRA adverse action, UK decline + Art 22C rights) with deadlines; the bank's systems send them**
- LB-I8 Retention: per-market config: US default ≥25 months (Reg B), configurable to 7+ years; UK term + 6 years with litigation hold (s.140A/FOS)
- LB-I1/I9 Packs: model documentation (SR 26-2 + SS1/23, incl. LLM control pack); third-party/security (US TPRM, UK SS2/21, SOC 2/ISO 27001 evidence, SBOM, pen test, escrow); data protection (UK DPIA + Art 22C, US GLBA/Part 500, CO/CA ADMT); accountability mapping (SM&CR owner; US model owner/validator)
### Round 10: Mortgages, commercial, other consumer, collections
- LB-B3 Mortgages: US conforming & jumbo (ATR/QM, HMDA, FHA disparate impact); UK residential (MCOB 11.6, LTI ≥4.5x); UK buy-to-let (ICR stress); home equity / second charge (US HELOC; UK second-charge stresses the first mortgage)
- LB-B7/B8 Commercial: SME loans/lines/cards (1071 data 2028; UK Bank Referral Scheme); mid & large corporate (5-dimension rating, stressed cash flow, large exposures/SCCL/legal lending limit); CRE (US 100/300% review, UK slotting attributes); leveraged/sponsor finance (debt/EBITDA flags, sponsor aggregation)
- LB-B4–B6 Other consumer: auto finance, UK overdrafts, UK BNPL selected AND "none beyond the first four" (resolved as phasing in round 11). User addition: **Gen Z facilities across loans, cards and other banking products**
- LB-B13 Collections v1: cure prediction; forbearance recommender (UK CONC 7 / persistent debt; US hardship); UK persistent-debt engine (18/27/36); contact strategy (drafts reviewed by humans)
### Round 11: Phasing, Gen Z features, releases, team
- LB-B4b Auto finance, UK overdrafts and UK BNPL: **in v1 but a later release**
- LB-GZ Gen Z features: credit-builder products (starter card, credit-builder loan, rent reporting 18+); student/graduate offers (UK graduate overdraft; US 18–20 cards under CARD Act income/cosigner rules); loyalty & rewards (non-credit for under-18s; credit only from 18); smart limits & nudges (spending controls, reminders, persistent-debt prevention)
- LB-J1/J5 Releases: **4 releases**: R1 Challenger MVP (cards + loans/advance, both markets, back-test); R2 Pilot (mortgages, SME/corporate, integrations, notices, packs); R3 Growth & macro (inclusion, Gen Z, product designer, stress, frontier); R4 Ops (collections, auto/overdraft/BNPL, doc AI, policy copilot)
- LB-J1b Team: **6–9 developers** → long timeline; plan will show a realistic estimate and where to cut scope
### Round 12: Automation, pilot win criteria, pilot data, pricing
- LB-AUTO Automation: **bank configures per product/amount** (automated vs human). Safeguards built in: UK Art 22C (information, representations, human intervention, contest); meaningful-review evidence when human; US/CO human review on request. Deviation from the UAE "humans always decide" principle → principle becomes "AI recommends; the bank chooses where automation is allowed and staff stay accountable"
- LB-K2 Pilot win criteria: accuracy (Gini/AUC out-of-time vs champion); more approvals at the same expected loss; fairness (AIR / Equality Act outcomes) equal or better; stability & explainability
- LB-K1 Pilot data: 3–5 years of history incl. rejects; 6-month shadow beside the champion
- LB-A7 Pricing: **per decision / per account** (volume-based)
### Round 13: Salary advance, starter card, UK & US affordability
- LB-SA Salary advance (demo policy): salary credited to the bank ≥ 3 months; up to **50% of net monthly pay**, repaid from next salary; **one advance at a time** (cooling-off); affordability check + blocked if in persistent debt or financial difficulty
- LB-SC Starter card (demo): **UK £250–£1,000 / US $300–$1,500**, reviews at 6 and 12 months of on-time payment, fresh affordability check at each increase
- LB-AF UK spending estimate: Open Banking actual spend; ONS/bureau expenditure norms; declared + verified mix; stress for foreseeable change (rate rises, end of fixed term, redundancy risk)
- LB-DTI US defaults: CARD Act ability-to-pay (under-21 independent income or cosigner); bank-set DTI/residual-income caps; MLA 36% / SCRA 6% / usury gates by charter & state; values configurable (demo uses typical values)
### Round 14: Opportunity, product designer, NBO, fraud
- LB-FR Opportunity measures: approvals & balances; risk-adjusted profit (income − funding − expected loss − opex, RAROC-style); customer lifetime value; inclusion impact (thin-file, blue-collar, young customers newly served)
- LB-PD Product designer may propose: limit ladders; pricing & fees (within usury/MLA/HCSTC caps and UK fair value); eligibility rules; product features (controls, rewards, payment holidays). All simulated on the book; proposals go through maker-checker
- LB-NBO Offer rules: affordability first; no offers to vulnerable customers or those in difficulty/collections/persistent debt; marketing consent & FCRA prescreen firm-offer rules; no credit promotions to minors; fair value (UK) / not deceptive (US UDAAP)
- LB-FD Fraud consistency: declared vs verified income; synthetic identity signals; first-party fraud / bust-out; **flags handed to the bank's fraud systems** (we don't decide fraud)
### Round 15: Scenarios, PIT refresh, validator, document AI
- LB-MS Default scenario set: regulator scenarios (Fed supervisory, BoE stress test); event shocks (war/sanctions, pandemic, oil shock, regional natural disaster, sector layoffs); NGFS climate paths + physical risk by ZIP/postcode; custom scenario builder for the CRO
- LB-MS2 Point-in-time score refresh: **daily** (with the nightly re-score; macro inputs update when released)
- LB-VB Validator in a box for the bank's models: scores & outcomes only; model files loaded on-prem (PMML/ONNX/pickle); side-by-side challenger; SR 26-2 and SS1/23 report formats
- LB-DOC Document AI: financial statements (incl. UK statutory accounts); US business tax returns (1120, 1065, K-1); loan agreements & covenants; bank statements (SME cash flow)
### Round 16: Roles, language, demo, principle
- LB-G1 Roles: underwriters & credit officers (retail + commercial); risk strategy & policy teams; model risk & validation; collections, fraud, CRO/board
- LB-G6/F6 Language & accessibility: English UI; Spanish customer letters (US, on request); Welsh letters (UK, on request); **WCAG 2.2 AA**
- LB-G7 Demo: synthetic Demo US Bank + Demo UK Bank; a synthetic "bank champion" scorecard to beat; benchmarks on public credit datasets
- LB-PR Principle: **"AI recommends; the bank sets where automation is allowed; people stay accountable."**
### Round 17: Certifications, contracts, support, licensing
- LB-H3 Certifications: SOC 2 Type II; ISO 27001; yearly independent pen test (+ SBOM, secure SDLC); cyber & PI insurance
- LB-K3 Contracts: source-code escrow; liability cap & indemnities; exit & transition plan. **Mandatory regardless:** regulator audit/access rights (US 12 USC 1867(c) examination of service providers; UK SS2/21 access)
- LB-K5 Support: US-person support for US installs; UK-based support for UK installs; 24/7 for the real-time API. Remote sessions not selected → support access mode per bank (on-site or bank-controlled)
- LB-H8 Licensing: signed licence file (bank ID, modules, volume tier, expiry, offline check). **Needed for per-decision pricing:** monthly usage-count export (no customer data)
### Round 18: Stack, scale, testing, R1 done
- LB-J3 Stack: **BMAD architect decides** (proposal in architecture.md)
- LB-J4 Scale: real-time **p95 < 300 ms**; nightly **50M+ accounts** (re-score + PIT update); feature store (online = offline); horizontal autoscaling, stateless scoring
- LB-J6 Testing: executable regulatory test suites per rule; fair-lending test suite on every model build; load & chaos tests; adversarial / LLM red-team
- LB-J7 R1 done: cards & loans scored in US + UK (rules, UK affordability, US ability-to-pay, PD/LGD/EAD, reasons); champion vs challenger report (synthetic bank + public data); risk-vs-opportunity frontier v1; Demo US & UK banks
### Round 19: Grades, early warning, corporate rating, Consumer Duty
- LB-E1b Grades: map to the **bank's master scale** (configurable grades & PD bands); demo uses a 20-grade scale typical of large banks
- LB-EW Retail early-warning signals: income shocks (salary stop/drop, job change, benefits income, sector redundancy); credit stress (utilisation, minimum-only payments, cash advances, BNPL/credit stacking, inquiries); spending behaviour (gambling, payday lenders, luxury spikes, spend > income); external exposure (home in flood/wildfire zone after an event; employer hit by sanctions/war/supply shock)
- LB-CORP Corporate rating: five dimensions (35/20/15/10/20, configurable); sector-specific templates (CRE, leveraged, SME, large corporate); market signals for listed names (optional feed); covenant & cash monitoring
- LB-UKCD UK Consumer Duty: outcome MI by cohort; vulnerability flags → human specialist (never auto-decline on a flag); fair-value checks; Art 22C contest workflow with SLA
### Round 20: US features, irregular income, Gen Z loyalty, deliverables
- LB-USR US v1: Reg B/FCRA notice content (≤4 deterministic reasons, bureau key factors, 30/90-day timers); HMDA fields & denial codes now + 1071 fields ready for 2028; state AI laws (CO SB 26-189 and CA ADMT, 2027: notices, 30-day explanation, human review on request, deployer docs); FCRA prescreen firm offers
- LB-INC Irregular income: smoothed from 6–12 months of verified cash flow with a volatility penalty; gig & multiple employers combined; seasonality-aware. (Conservative floor not selected, but UK CONC 5.2A requires accounting for foreseeable income falls → volatility penalty + stress retained)
- LB-LOY Gen Z loyalty (non-credit under 18): savings boosts; education & goals rewards; partner perks (student discounts via debit/prepaid); graduation path to a pre-assessed starter card / credit-builder at 18 (if affordable)
- LB-DEL Deliverables: brief, PRD, architecture, epics; BMAD build prompt; banker PDF (US + UK); visual walkthrough page with a New York and a London customer
### Round 21: Model lifecycle, children's data, consent, PII
- LB-ML Lifecycle: bank MRM approval before any model is used; auto-retrain on drift, activation needs approval; auto-suspend → fallback to the bank's champion or our scorecard + alert; overrides and outcomes feed retraining (carefully)
- LB-CH Under-18 data: **readiness scoring for ages 16+ only** (no profiling under 16; avoids COPPA); **no marketing profiling of minors** (education + compliant 18th-birthday offer only). **Mandatory regardless:** children's DPIA (UK high-risk processing); data minimisation
- LB-CON Consent: consent record per source (data, purpose, expiry, revocation); purpose limitation; integrate with the bank's consent platform. **Mandatory regardless:** revocation stops use (scores recomputed without the data)
- LB-PII PII: tokenise on ingestion (keys in the bank vault); field-level encryption; role-based reveal + audit. **Mandatory regardless:** protected attributes in a separate fairness-testing zone (UK DPA Sch 1 para 8; US BISG proxies)
### Round 22: Collections, policy copilot, board KPIs, climate
- LB-COL Collections contact: frequency caps (US 7-in-7 call presumption as a safe default; UK proportionate); vulnerability & hardship first (forbearance before escalation); channel & time rules incl. opt-outs; tone guardrails on AI drafts (no threats or misleading statements; human approval)
- LB-PC Policy copilot: read policy documents (draft rules with page citations, maker-checker); find conflicts & gaps (vs each other, vs regulator pack, uncovered cases); regulatory change alerts when pack values change (e.g. yearly QM thresholds); simulate before approval (frontier + fairness)
- LB-BD Board & CRO KPIs: champion vs challenger gains; opportunity captured (inclusion, Gen Z, product designer); macro & climate exposure; early warning & collections
- LB-CL Climate: physical risk on collateral (flood, wildfire, storm, subsidence, heat); transition risk for corporates (NGFS); insurance-gap flag; 1/5/30-year horizons
### Round 23: Automation defaults, trade-off view, synthetic banks, project risks
- LB-AUTO2 Demo automation defaults: auto-approve small starter cards / salary advances (low-risk grades only); auto-approve credit-limit increases for good accounts after a fresh affordability check; **never auto-decline** (every decline reviewed by a person); mortgages & commercial always human
- LB-RISKOPP Trade-off presentation: efficient-frontier chart (current policy marked); opportunity-loss segments (e.g. gig workers, graduates); risk-budget view; AI-recommended policy point within risk appetite (human approves)
- LB-SYN Synthetic demo banks: millions of accounts (e.g. 2M US + 1M UK); bureau, Open Banking & transactions; known ground truth; simulated recession + regional disaster in history
- LB-RISKS Risks to manage: long GSIB sales cycle; regulatory change; scope vs team; model validation hurdles. **User direction: compress the scope to 2–3 months and increase developers (frontend and backend)**. User also asked to wrap up discovery
### Round 24 (final): Timeline & team
- FINAL 1 Target: **everything in v1 within 2–3 months** (product-owner decision). Recorded as HIGH RISK; the plan runs squads in parallel and fixes a strict priority order (R1 Challenger MVP first) so the most valuable scope is done if time runs short
- FINAL 2 Team: **14–18 people**: ~5 backend, 4 frontend, 3 ML/data science, 2 data engineers, 1 platform/DevOps, 1 QA, + PM/architect

## Discovery complete: 24 rounds, 94 on-screen questions covering ~140 questionnaire items (2026-11-07)

## Agreed worked examples (used across PRD, PDF, walkthrough)
- **Maria (New York), 24**: warehouse shift worker + weekend delivery gig, thin file (FICO 640, 2 tradelines). Smoothed net income $3,400/mo; rent $1,450; car loan $310 + student loan $180; essential spend $900. Applies for a $5,000 card. Bank champion scorecard: decline (thin-file cut-off). Challenger: PD 3.1% → demo master-scale grade 13. CARD Act ability-to-pay: residual $560 vs minimum payment at full $5,000 limit ≈ $150 → passes. Bank starter-card cap (thin file) $1,500 → **recommend $1,500 starter card**, reviews at 6/12 months. Above the $1,000 auto-approval line → human review. Reg B reasons if counter-offer: limited credit history; income variability.
- **Tom (London), 19**: apprentice electrician; readiness record since 17 from junior account. Net income £1,650/mo (Open Banking verified); rent share £500; essentials £620 (Open Banking actual, checked against ONS norms); phone contract £35 → disposable ≈ £495. Requests £1,000 starter card. Affordability: repay £1,000 over 36 months at 29.9% APR ≈ £42/mo → PASS. PD 2.2% → grade 12. Within bank automation rule (starter card ≤ £1,000, grade ≤ 12, all rules pass) → **auto-approved**, with Art 22C information and the right to human review.
- Demo 20-grade master scale upper PD bounds (%): 0.03, 0.05, 0.08, 0.12, 0.18, 0.26, 0.38, 0.55, 0.8, 1.15, 1.65, 2.4, 3.4, 4.9, 7, 10, 14, 20, 30, 100.
