---
title: AI Risk Score Card
created: 2026-11-07
updated: 2026-11-07
status: final
inputDocuments:
  - _bmad-output/planning-artifacts/product-brief.md
  - _bmad-output/planning-artifacts/discovery-answers.md
  - research/research.txt
  - research/Bank's Credit Assessment Framework for Corporate Lending.pdf
  - archive/PROMPT_v1_2026-11-06.md (Appendix A: CBUAE rules)
---

# PRD: AI Risk Score Card

## 0. Document Purpose

This PRD is for the development team (6+ developers in squads), the architect, and the BMAD downstream
workflows (`bmad-architecture`, `bmad-create-epics-and-stories`, `bmad-sprint-planning`, `bmad-build`). It turns
104 discovery answers (`discovery-answers.md`) into numbered, testable requirements. Vocabulary is fixed by the
Glossary (§3). Features (§4) carry globally numbered FRs, each tagged with its release **[R1] / [R2] / [R3]**.
System-wide NFRs are in §5. CBUAE rule values live in `docs/regulatory/cbuae-rules.md` (copied from
Appendix A of `archive/PROMPT_v1_2026-11-06.md`). Assumptions are tagged inline and indexed in §12.

## 1. Vision

AI Risk Score Card is an on-premise AI credit-risk engine for **Islamic banks in the UAE**, and the first module
of a risk-AI platform for the bank's risk function. It sits inside the bank, connects to Temenos T24/Transact
and the bank's data warehouse, and assesses every **Finance Application** in real time and the whole **Book**
nightly. It checks three **Policy Layers** (CBUAE regulation, Bank Policy, Credit Policy), scores the **Customer**
with an expert **Scorecard** refined by a locally trained **Learning Model**, and returns a **Risk Grade** (1–10),
**PD**, **Recommendation**, **Recommended Limit** and an **Explanation** in English and Arabic.

It is built to deliver fewer defaults, more approvals at the same risk, faster decisions and a measurable ROI uplift
in AED. It serves the low-salary segment safely and shows the bank where its own policy turns away good
business.

**Product principle (binding on every feature):** *AI recommends, scores, drafts and flags; bank staff decide
and are accountable.*

## 2. Target User

### 2.1 Jobs To Be Done
- **Credit Officer:** "Give me a consistent, explained recommendation and a draft memo so I spend my time on judgement, not arithmetic."
- **Approver (authority levels up to Credit Committee):** "Show me only the cases I must sign, with the deviation and its risk."
- **Relationship Manager:** "Tell me instantly whether my customer qualifies, for how much, and which existing customers I can offer more to."
- **Risk Manager / CRO:** "Keep the book inside appetite. See deterioration early, test policy changes before making them, prove the models are sound."
- **Management / CEO:** "Show me approvals, defaults, missed opportunity and income uplift in AED."
- **Model Validator / Auditor / Sharia reviewer:** "Prove every decision followed the rules, reproduce any past decision, and show the models are fair and stable."
- **Bank IT / Security:** "Install it inside our network, connect it to T24 and AD, and prove no data leaves."

### 2.2 Non-Users (v1)
- Customers (no customer-facing screens or AI text).
- Conventional (non-Islamic) banks (vocabulary is Islamic-only in v1).
- AML/KYC, fraud and collections teams (separate future modules).

### 2.3 Key User Journeys

- **UJ-1. Sara, a credit officer, decides a Tawarruq personal finance application in minutes.**
  Sara is logged in through Active Directory. An RM submits an application in T24. The system receives it by API and returns a
  Recommendation within seconds. Sara opens the **Decision Screen**: Grade 4, PD 1.6%, Recommendation *Approve at AED 212,000
  (requested 400,000)*. Binding rule: DBR on basic + housing of AED 18,000 (instalment AED 4,979, DBR 49.9%). She clicks into the drill-down to see the DBR arithmetic and every rule result, reads the
  English/Arabic Explanation, edits the drafted **Credit Memo**, and submits. The case goes to the branch-manager queue because
  the amount is within that authority. **Edge case:** if Sara overrides to a higher amount within CBUAE limits, she must record a reason, the
  **Deviation** is allowed only because Grade 4 permits it, and the case routes to a higher **Approval Authority**.

- **UJ-2. Omar, an approver, clears his queue.**
  Omar opens the **Approval Queue** and sees only cases at his authority level, sorted by risk, each flagged with any
  Deviation. He approves one, returns one with a comment, and escalates one. Every action is recorded in the **Decision Record**.

- **UJ-3. Huda, the CRO, reads the morning risk pack.**
  After the **Nightly Run**, Huda opens the **Portfolio Dashboard**. 37 customers newly on the **Watch-list**. 12 **Lifestyle
  Mismatch** alerts, for example a customer whose monthly spend has exceeded salary credits for 4 months and who just bought a luxury car.
  A **De-risking Recommendation** to reduce unused card limits for 58 customers. Employer concentration over threshold for one
  semi-government employer. She asks the **Portfolio Assistant** "which employers drove the increase in grade 8–10 this
  month?" and gets an answer with a table.

- **UJ-4. Huda tests a policy change before proposing it.**
  In the **What-if Simulator** she lowers the DBR limit from 50% to 45% for expats in the private sector and sees approval rate −6%,
  expected loss −AED 2.1m, income −AED 3.4m. She saves the scenario and submits it as a **Policy Change Request**. A second
  risk manager (checker) approves it, and it takes effect with a new **Policy Version**.

- **UJ-5. The bank onboards its credit policy.**
  An admin uploads the bank's Credit Policy manual (PDF) and parameter sheet (Excel). The system extracts **Draft Rules** with the
  LLM, each linked to its page and section. The credit team reviews, edits and approves them (maker-checker). The tighten-only
  check rejects one rule that is looser than CBUAE. The system then publishes the **Data Field Template** that bank IT must supply.

- **UJ-6. A corporate analyst rates an SME.**
  The analyst opens an SME **Obligor** whose latest statements arrived as PDF. **Document AI** extracts the financials for review.
  The five-dimension rating gives Grade 6. Stressed DSCR (EBITDA −30%) sizes the limit. Group exposure is checked against 25% of Tier 1.
  A drafted credit paper is ready for committee.

- **UJ-7. Management sees the money.**
  The CEO opens the **KPI & ROI Dashboard**: approval rate, defaults by vintage, opportunity value blocked by each restriction (AED),
  and estimated income uplift, using the bank's funding cost, profit rates and LGD.

- **UJ-8. A salesperson demos to a new bank.**
  The **Demo Tenant** "Demo Islamic Bank", with synthetic T24-like data, shows UJ-1 to UJ-7 without any real data.

## 3. Glossary

- **Bank (Tenant)**: One client institution. All data, policies, models and users are isolated per Tenant. One installation may host several Tenants.
- **Policy Layer**: One of three ordered rule sets: **CBUAE Layer** (regulation), **Bank Policy**, **Credit Policy**. A lower layer may tighten but never loosen a higher one.
- **Rule**: A declarative condition with id, layer, applicability, severity (`knockout` / `refer` / `warn`), source reference and confidence.
- **Policy Version**: An immutable, approved snapshot of a Tenant's Bank Policy and Credit Policy.
- **Draft Rule**: A Rule extracted from a policy document (by LLM or parser) awaiting maker-checker approval.
- **Policy Change Request**: A proposed change to Rules or parameters, requiring maker-checker approval.
- **Customer**: An individual retail finance customer. **Obligor**: a corporate or SME counterparty. **Group**: connected Obligors (and connected Customers) aggregated for exposure.
- **Finance Application**: A request for a Product, amount and tenor by a Customer or Obligor.
- **Product**: Tawarruq/Murabaha Personal Finance, Islamic Credit Card, Auto/Goods Murabaha, Ijara Home Finance, SME Finance, Corporate Finance (term, working capital, overdraft facility).
- **Profit Rate**: The annual rate used in Islamic finance instalment maths (never "interest").
- **Finance Amount**: The principal financed (never "loan amount").
- **DBR (Debt Burden Ratio)**: Total monthly obligations to all lenders ÷ **DBR Income**. **DBR Income** = basic salary + housing allowance by default (bank-configurable).
- **EOSB**: End-of-service benefit accrued under UAE Labour Law, computed from basic salary and service years.
- **Total Unsecured Cap**: Total unsecured financing across all Products ≤ 20 × monthly income.
- **Scorecard**: Points-based expert model producing a **Score** on the Tenant's scale.
- **Learning Model**: Gradient-boosting model trained locally on the Tenant's history, producing a PD.
- **PD**: 12-month probability of default. **Default** = 90+ days past due within 12 months.
- **Risk Grade**: 1 (lowest risk) to 10 (highest), from PD bands set per Tenant.
- **Recommendation**: Approve / Refer / Decline, produced by the Policy Layers, with model escalation only (FR-31).
- **Deviation**: Approval of a case that failed a non-CBUAE Rule. Permitted only within grade limits and approved at the authority the grade requires.
- **Approval Authority**: A level in the Tenant's delegation matrix (e.g. Branch Manager → Head of Credit → Credit Committee).
- **Recommended Limit**: The maximum safe Finance Amount, with its **Binding Constraint**.
- **Explanation**: Plain-language reason text (English and Arabic). **Credit Memo**: a drafted credit paper. Both are drafts until a user approves them.
- **Decision Record**: Immutable record of inputs, Policy Version, model version, outputs, user actions and timestamps for one assessment.
- **Book**: All existing Customers and Obligors of a Tenant. **Nightly Run**: the scheduled re-scoring of the Book.
- **Watch-list**: Existing accounts flagged for deterioration before delinquency.
- **Lifestyle Mismatch**: Spending or purchases inconsistent with verified income or peers.
- **De-risking Recommendation**: Reduce limits (retail) or tighten collateral/covenants (corporate) for high-risk existing accounts.
- **Pre-approved Offer**: A proactive Recommended Limit for an existing Customer who is not currently applying.
- **Opportunity Finder**: Analysis of Customers declined or restricted by policy whose PD is within appetite, valued in AED.
- **What-if Simulator**: Re-runs the Book or past applications under a changed Policy Version and reports impact.
- **Portfolio Assistant**: LLM chat over the Tenant's portfolio data. It acts directly only on **Safe Actions** (queries, reports, what-ifs, re-scores, filters).
- **Demo Tenant**: "Demo Islamic Bank", populated with synthetic T24-like data.
- **Document AI**: Extraction of financial-statement figures from PDF documents for human review.

## 4. Features

### 4.1 Tenancy, Policy Layers & Policy Lifecycle
**Description:** Each Tenant has isolated data, users, Policy Versions and models. The CBUAE Layer ships with the
product (sourced rules with confidence levels). Bank Policy and Credit Policy are read from the bank's own documents,
reviewed, and versioned under maker-checker. Realizes UJ-4, UJ-5.

#### FR-1: Tenant isolation [R1]
An admin can create Tenants. All data, configuration, models and audit records are isolated per Tenant.
- A user of Tenant A can never query or see Tenant B data (integration test).
- The Demo Tenant is a normal Tenant flagged `demo=true`, with a persistent "DEMO DATA" banner.

#### FR-2: CBUAE Layer [R1]
The system ships a versioned CBUAE rule pack (retail, Islamic home and auto finance, corporate large exposures, classification),
each Rule with source, section, URL and confidence (H/M/L/UNCONFIRMED).
- Rules with confidence below H show a "to verify" badge in the Policy Viewer.
- The pack has a version and a verification date. Updating it is a signed update (FR-63).

#### FR-3: Tighten-only validation [R1]
The system rejects any Bank Policy or Credit Policy value that is looser than the CBUAE Layer.
- Every numeric limit carries a direction (max/min). A looser value blocks publication with a message naming the Rule and both values.

#### FR-4: Policy import from parameter sheet [R1]
A policy admin can import an Excel parameter sheet mapped to Rules and parameters.
- Unmapped rows are listed for manual mapping. Nothing is silently dropped.

#### FR-5: Policy extraction from documents [R2]
A policy admin can upload a policy manual (PDF/Word). The LLM proposes Draft Rules, each citing the page and section.
- No Draft Rule becomes active without maker-checker approval (FR-6).
- Every Draft Rule shows its source excerpt next to the proposed condition.

#### FR-6: Maker-checker & Policy Versions [R1]
Any Rule or parameter change is a Policy Change Request that a different user with checker rights must approve. It then publishes a new immutable Policy Version.
- The maker cannot approve their own request.
- Every Decision Record references the Policy Version used.

#### FR-7: Data Field Template from policy [R2]
From the active Policy Version, the system generates the list of required and optional data fields (with definitions) for bank IT.
- Adding a Rule that uses a new field updates the template and flags the missing field in data-quality checks.

#### FR-8: Demo Bank Policy [R1]
The Demo Tenant ships a demo Bank Policy and Credit Policy that encode the discovery defaults, clearly labelled "demo":
- salary-transfer requirement
- employer categories (government, semi-government, defence/MOI/MOD, blue-chip, other private) with caps
- age minimum 21, maximum at maturity 65 (expat) / 70 (national)
- restricted-nationality list → Refer
- EOSB-backed finance after ≥ 5 years of service, up to 80% of accrued EOSB
- low-salary threshold and caps
- Total Unsecured Cap 20×
- card obligation 5% of limit
- Profit Rate stress add-on 0
- Grade-based deviation and authority matrix
- corporate thresholds left empty [ASSUMPTION A1]

#### FR-9: Employer classification [R1]
The system ships a starter UAE employer-category list. The Tenant can override it with its own lists.
- Tenant list entries take precedence. Unknown employers default to `private_other` and are flagged.

#### FR-10: Restricted lists [R1]
The Tenant maintains a restricted-nationality list (default severity Refer), restricted sectors, and **Sharia-prohibited sectors** (Decline).
- The Opportunity Finder (FR-46) reports the AED value each restriction blocks.

### 4.2 Data Integration & Protection
**Description:** Applications arrive in real time from T24. The Book and history arrive through a read-only database connection.
There is **no file upload of customer data**. The Demo Tenant uses a local database that mimics T24 and warehouse structures.

#### FR-11: Real-time application API [R2]
T24 (or any LOS) can POST a Finance Application and receive the assessment synchronously.
- The response contains Grade, PD, Recommendation, Recommended Limit, Binding Constraint, failed Rules and a reference to the Decision Record.
- Latency targets are in NFR-1. An Explanation is included when ready, or fetched later by reference.

#### FR-12: T24/Transact connector [R2]
The system provides a Temenos T24/Transact adapter (API mapping and field mapping) as the first named connector.
- Field mapping is configuration, not code. The mapping is validated against the Data Field Template.

#### FR-13: Database connector for Book & history [R2]
The system reads the Book, transactions, salary credits, CASA balances, history and rejected applications from the bank's database (SQL Server / Oracle / PostgreSQL) through configured read-only views.
- The connector uses read-only credentials. Any attempted write fails and is logged.

#### FR-14: Demo data source [R1]
The Demo Tenant reads from a bundled local database with synthetic T24-like schemas. The same connector code path is used as in production.
- The synthetic data has a known latent risk function and ~3–6% retail / 4–8% corporate default rates.
- It includes rejected applications, raw transactions with MCC, salary credits and CASA balances.

#### FR-15: Behavioural data ingestion [R2]
The system accepts raw card/account transactions (with MCC) and monthly aggregates, and derives the same features from either.
- If raw transactions exist, they take precedence. Feature lineage records which source was used.

#### FR-16: AECB data [R2]
The system reads the bank's stored AECB scores and reports. An optional direct AECB API connector is off by default [R3].
- Enabling the AECB API needs an admin action, is logged, and is the only outbound customer-data flow allowed.

#### FR-17: PII masking [R1]
Names, Emirates ID, passport and phone numbers are pseudonymised on load. Only roles with `reveal_pii` see clear values, and each reveal is logged.

#### FR-18: Data-quality checks [R1]
Every run validates required fields, ranges and freshness. Records failing a required field are scored "incomplete" with the missing fields listed, never silently defaulted.

### 4.3 Retail Assessment (Islamic)
**Description:** Assesses Customers for Tawarruq/Murabaha Personal Finance, Islamic Credit Card, Auto/Goods Murabaha and Ijara Home
Finance. Covers salaried, self-employed, retired, non-resident and low-salary Customers, and joint applicants and guarantors. Realizes UJ-1.

#### FR-19: Retail feature derivation [R1]
The system derives:
- age (now and at maturity) and years of service
- **EOSB** (UAE Labour Law: 21 days' basic per year for the first 5 years, 30 days after, capped at 2 years' wages; configurable)
- DBR before and after (on DBR Income, all lenders, cards at the configured % of limit)
- Profit Rate instalment (annuity, with the stress add-on)
- salary multiple, Total Unsecured exposure, salary-credit regularity and delays
- card utilisation and cash advances
- spend level, volatility and category mix (MCC), bonus-month behaviour, CASA depth
- Unit tests cover the EOSB, DBR and annuity maths with worked examples.

#### FR-20: Product rules [R1 personal finance & card; R2 auto & Ijara]
Product-specific CBUAE and policy rules apply:
- personal finance: ≤ 20× income, ≤ 48 months
- card: minimum income per CBUAE/bank
- auto Murabaha: ≤ 80% of value, ≤ 60 months
- Ijara home finance: LTV by national/expat, first/second home, value band and off-plan; ≤ 25 years; DBR ≤ 50%; EOSB is not a repayment source
- DBR ≤ 50%, retirees ≤ 30%
- Total Unsecured Cap 20×

#### FR-21: Customer types [R2]
Self-employed (income from verified business credits / financials), retirees (pension, 30% DBR), non-residents and low-salary Customers are assessed under the Tenant's segment-specific rules and caps.
- The low-salary threshold and caps are Tenant parameters. No separate model.

#### FR-22: Joint applicants & guarantors [R2]
A Finance Application may include co-applicants (combined income and obligations) and guarantors (guarantor strength as a factor and a Rule input).

#### FR-23: Islamic product-structure checks [R2]
- Tawarruq/Murabaha: the commodity/asset purchase step is recorded as a required field.
- Ijara: ownership and lease conditions are recorded.
- Late-payment amounts are never treated as income (they go to charity).
- Missing structure data → Refer.

### 4.4 Corporate & SME Assessment
**Description:** Rates Obligors on five dimensions, sizes facilities on stressed cash flow, and enforces CBUAE large-exposure limits with
Group aggregation. Realizes UJ-6.

#### FR-24: Corporate features & five-dimension rating [R2]
Dimension weights (default, configurable): financial capacity 35%, business & industry 20%, management & governance 15%, external exposure 10%, security & structure 20%.
- Financial features: Debt/EBITDA, gearing, profit cover, cash conversion (OCF/EBITDA), DSCR, liquidity runway, audit quality.
- Each dimension is scored 0–100, then combined onto the Tenant's scale.

#### FR-25: Corporate knockouts [R2]
- Weak financial capacity AND (weak governance OR unenforceable security) → Decline.
- Sharia-prohibited sector → Decline. Restricted sector → per Tenant severity.
- Thresholds come from the Tenant's corporate policy (empty until supplied [ASSUMPTION A1]).

#### FR-26: Stressed sizing [R2]
Facility capacity = cash flow under EBITDA −30% (configurable) at the policy minimum DSCR. It is combined with collateral capacity (value × haircut by collateral type).

#### FR-27: Group & large-exposure limits [R2]
Exposures aggregate across connected Obligors/Customers (Group).
- The system checks CBUAE limits as % of Tier 1: 25% single/group; 20%/50% shareholders; 10%/25% affiliates; 5%/25% board members; GRE 25%/100%; federal government exempt.
- The Tenant's Tier 1 is a parameter.

#### FR-28: Document AI for financial statements [R2]
An analyst can upload a PDF financial statement for an Obligor. The system extracts line items into a spread for review.
- Each figure links to its page. Nothing is used in a rating until a user confirms the spread.

#### FR-29: Sole proprietors on owner salary [R2]
These are assessed with retail rules (20×, 48 months, 50% DBR) per CBUAE Reg 29/2011 Art 2(e).

### 4.5 Scoring & Grading
#### FR-30: Scorecard [R1]
A points-based Scorecard per segment. Bins and points come from config, with expert defaults documented in `docs/methodology/scorecard.md`.
- Score mapped to PD by a configurable calibration. Weights are replaceable by the bank's own scorecard (import) and refined from data (WoE/logistic calibration) [R2].

#### FR-31: Learning Model [R2]
A gradient-boosting model per segment, trained locally on the Tenant's history (1–2 years, including rejected applications with reject inference), predicts 12-month PD.
- Monotonic constraints apply where the risk direction is known.
- **Excluded features:** nationality, gender, marital status, religion. **Age is allowed.**
- Per-case feature contributions are stored for Explanations.
- Final PD = blend of Learning Model and Scorecard PDs (weight configurable; 0 when no active model).

#### FR-32: Risk Grades [R1]
PD maps to Grades 1–10 by Tenant bands, shown on the Tenant's score scale.
- Default bands: 1 < 0.25%, 2 0.25–0.5%, 3 0.5–1%, 4 1–2%, 5 2–3.5%, 6 3.5–5%, 7 5–8%, 8 8–12%, 9 12–20%, 10 ≥ 20% [ASSUMPTION A2].

### 4.6 Recommendation, Deviations & Limits
#### FR-33: Policy-first Recommendation [R1]
The Recommendation comes from the Policy Layers:
- a failed knockout Rule → Decline
- a failed refer Rule → Refer
- all Rules passed → Approve, subject to the **model escalation**: if the Grade is at or worse than the Tenant's escalation grade (default 7), Approve becomes Refer.
- The model never turns a policy Decline or Refer into Approve.

#### FR-34: Grade-based Deviations [R2]
The Tenant's Deviation matrix sets, per Grade, whether a non-CBUAE Rule failure can be approved as a Deviation and at which Approval Authority.
- CBUAE Rules can never be deviated.
- Every Deviation records the Rule, reason, approver and Grade.

#### FR-35: Recommended Limit [R1]
Retail limit = min(CBUAE cap, Bank cap by employer category and nationality group, Product cap, Total Unsecured headroom, DBR-headroom Finance Amount at the stressed Profit Rate, EOSB cap where applicable, requested amount).
- The Binding Constraint is always named, with a what-would-change hint (e.g. the maximum amount that passes DBR).
- Corporate limit: see FR-26/FR-27.

#### FR-36: Risk-based Profit Rate [R3]
The system suggests a Profit Rate per Grade and Product from the Tenant's pricing grid, with expected-loss cover shown. It is advisory only.

### 4.7 Approval Workflow & Access
#### FR-37: Approval Authority routing [R2]
The Tenant's delegation matrix (amount × Grade × Deviation × Product) routes each Referred or Deviation case to a queue.
- Approvers see only cases within their authority.
- Escalate, return-with-comment and approve actions are recorded in the Decision Record.

#### FR-38: Overrides [R2]
Any user override of a Recommendation or limit requires a reason code and free text.
- Override reports by officer, branch, Grade and outcome are available.
- Override outcomes are available as a Learning Model feature/label source [R3].

#### FR-39: Authentication & roles [R1 local accounts for demo; R2 AD/SSO]
Users authenticate via Active Directory / SSO (SAML or OIDC) [R2]. The standard roles are:
- RM, Credit Officer, Approver levels 1–n
- Risk Manager, CRO, Policy Admin, Model Validator, Auditor, Sys Admin
- Roles and permissions are configurable per Tenant.

### 4.8 Explanations & Language AI
#### FR-40: Explanations [R2; template-only in R1]
Each assessment has an Explanation in English and Arabic: decision, Grade, top drivers, failed Rules, Binding Constraint, and what would change the outcome.
- R1 uses deterministic templates. R2 adds the local LLM (Qwen/Llama) with templates as fallback.

#### FR-41: Number & rule guardrail [R2]
Every number and Rule id in LLM output must match the computed facts, or the text is discarded and the template is used.
- A unit test with a fake LLM that invents a number proves the fallback.

#### FR-42: Credit Memo drafting [R2]
The system drafts a Credit Memo (retail) or credit paper (corporate) from computed facts.
- The memo is a draft until a Credit Officer edits and signs it. The signed version is stored in the Decision Record.

#### FR-43: Internal-only AI text [R1]
No LLM output is exposed through customer-facing channels or APIs. The API returns Explanation text only to authenticated internal clients.

### 4.9 Portfolio Intelligence (Nightly)
**Description:** The Nightly Run re-scores the whole Book and produces the morning risk pack. Realizes UJ-3.

#### FR-44: Nightly Run [R2 basic re-score; R3 full pack]
A scheduled job re-scores all Customers and Obligors, stores Grade migration, and refreshes all portfolio outputs.
- Completion time is in NFR-2. A failed run alerts and keeps the previous results visible, labelled with their date.

#### FR-45: Risk ranking [R1]
Users can view the Book ranked from highest to lowest PD, filterable by segment, Product, employer category, sector and Grade. Each row shows its top-3 drivers.

#### FR-46: Opportunity Finder [R3]
Shows Customers declined or restricted by policy whose PD is within appetite, grouped by the Rule responsible, with count and AED value.
- Each restriction's "cost" is the AED value it blocks. Results feed the What-if Simulator.

#### FR-47: Early-warning Watch-list [R3]
Flags existing accounts with deterioration signals before delinquency:
- Grade migration ≥ 2 notches
- salary delays or irregularity
- utilisation and cash-advance spikes
- spending-habit change
- declining-profession or declining-industry flags
- Each flag lists its triggering signals. Thresholds are configurable.

#### FR-48: Lifestyle Mismatch [R3]
Detects:
- spending above salary credits for N months
- sudden large purchases (e.g. car, luxury, jewellery MCCs) relative to the customer's own history
- spending far above peers (same salary band and profession)
- spending funded by unexplained inflows (flagged "refer to compliance"; AML investigation itself is out of scope)

#### FR-49: Profession & industry decline [R3]
A Tenant-maintained table of declining professions and industries with risk adjustments, plus learned signals of rising default rates by profession or sector in the Tenant's own Book. Both feed FR-47 and stress tests.

#### FR-50: De-risking Recommendations [R3]
- Retail: for high-risk existing accounts, recommend reducing unused card or overdraft limits.
- Corporate: recommend tightening collateral or covenants.
- Recommendations go to a queue for human action. The system never changes limits in T24 itself.

#### FR-51: Pre-approved Offers & card limit increases [R3]
For eligible existing Customers, the system computes Pre-approved Offers and safe card-limit increases (express-consent requirement noted).
- Customers with a recent Watch-list flag or a Lifestyle Mismatch are excluded.

#### FR-52: Concentrations & hidden links [R3]
Exposure concentration by employer, sector, Product and Grade, against Tenant thresholds. Clustering finds hidden links (shared employer, owner, supplier, landlord or address) across Obligors and Customers.

#### FR-53: Stress tests [R3]
Portfolio and segment scenarios:
- income cut (e.g. −20%)
- job loss / sector layoffs
- Profit Rate rise (e.g. +2%)
- oil/macro shock
- declining professions and industries
- spending-habit shifts
Each reports DBR breaches, Grade migration, PD and expected-loss change. Nationality-based scenarios are excluded.

### 4.10 What-if Simulator & KPI/ROI
#### FR-54: What-if Simulator [R3]
Risk Managers and the CRO only. Clone the active Policy Version, change Rules or parameters, and re-run on the Book and past applications.
- Reports change in approval rate, expected loss (PD × Tenant LGD × exposure) and income/ROI.
- A scenario can be submitted as a Policy Change Request (FR-6).

#### FR-55: KPI & ROI Dashboard [R3]
Management view:
- approval rate, Grade mix, defaults by vintage, override rate
- Opportunity Finder value
- estimated income uplift, using the Tenant's funding cost, Profit Rates and LGD per Product (defaults until supplied)
- Late-payment charity amounts are excluded from income.

### 4.11 Portfolio Assistant
#### FR-56: Portfolio Assistant [R3]
Risk Managers and the CRO can ask questions in English or Arabic about the Tenant's portfolio and get answers with tables and the queries used.
- It acts directly only on Safe Actions: queries, reports, filters, what-if runs, re-scores.
- Any request to change a Rule, decision or model becomes a Policy Change Request or model request for maker-checker.
- Every action is logged.

### 4.12 Model Lifecycle & Governance
#### FR-57: Training & activation gate [R2]
Model Validators can train on the Tenant's history and view a model card:
- data window, default rate, AUC/Gini/KS, calibration, PSI, top features
- A model activates only if it passes the gate (≥ 1,000 rows, ≥ 50 defaults, out-of-time Gini ≥ 0.30 [ASSUMPTION A3]) **and** a user with the Model Validator role approves.

#### FR-58: Drift monitoring, auto-retrain, auto-suspend [R2]
The system monitors PSI and performance on every run.
- On drift (PSI > 0.25 or a configurable performance drop), it auto-retrains a challenger. Activation still needs approval.
- If the live model breaches suspension limits, it is **automatically suspended**, the Scorecard takes over, and Risk is alerted.

#### FR-59: Validation & documentation packs [R2]
Per model version, the system generates:
- a validation pack (performance, stability, calibration, backtesting, sensitivity)
- development documentation aligned to CBUAE Model Management Standards
- an export bundle for external validators

#### FR-60: Fairness report [R2]
Per model version, outcome and approval-rate monitoring by gender, nationality group and age band, for monitoring only (these attributes are never inputs except age).

### 4.13 Audit, Replay & Retention
#### FR-61: Decision Record & replay [R1]
Every assessment writes an immutable Decision Record: input hash and snapshot, Policy Version, model version, outputs, Explanation version, user actions and timestamps.
- An Auditor can replay any past Decision Record and get identical outputs.

#### FR-62: Retention [R1]
Records are kept per Tenant retention settings (default: keep everything; the bank controls purging).

### 4.14 Deployment, Licensing & Updates
#### FR-63: Installation & updates [R1 Docker; R2 Windows installer]
- Docker Compose deployment (primary) and a Windows Server installer (fallback).
- Updates are signed packages, applied offline (air-gapped) or via an outbound-only update channel. The Tenant chooses.

#### FR-64: Licence [R2]
A signed licence file per bank (bank id, Tenant list, modules, expiry), verified offline. On expiry, the system becomes read-only for audit; it never deletes data.

#### FR-65: Agentic annual review [R3 basic]
For corporate Obligors due for annual review, the system:
- assembles the latest financials (confirmed spreads)
- re-rates the Obligor
- flags changes since the last review
- drafts the review paper for analyst approval

### 4.15 Demo Mode
#### FR-66: Demo Tenant [R1]
"Demo Islamic Bank" with synthetic retail Book (~20,000 Customers) and corporate Book (~1,000 Obligors, R2), demo Policy Versions, demo users per role, and a guided scenario list covering UJ-1 to UJ-8 as features become available.

## 5. Cross-Cutting NFRs

- **NFR-1 Performance (real-time):** Finance Application assessment without LLM text: p95 ≤ 2 s and p99 ≤ 5 s at 20 concurrent requests on the reference server. LLM Explanation ≤ 20 s, asynchronous.
- **NFR-2 Performance (batch):** Nightly Run of 100k Customers + 5k Obligors in ≤ 2 h, including portfolio outputs (excluding LLM narratives).
- **NFR-3 Data residency:** No customer data leaves the Tenant's infrastructure at runtime. The only exception is the optional AECB API (FR-16). Outbound connections are deny-by-default and listed in config.
- **NFR-4 Security:** Encryption at rest (database and files) and TLS in transit. PII masked (FR-17). RBAC on every API endpoint. Secrets in a vault or OS keystore. OWASP ASVS L2 targets. Security tests in CI.
- **NFR-5 Auditability:** Every write action and every decision is audit-logged with user, time and before/after. Audit records are append-only.
- **NFR-6 Determinism:** Given the same inputs, Policy Version and model version, outputs are identical (seeded models; no LLM in decision paths).
- **NFR-7 Availability:** Real-time API ≥ 99.5% in bank business hours. Graceful degradation: Learning Model down → Scorecard; LLM down → templates; nightly failure → last results with date.
- **NFR-8 Localisation:** UI in English. Explanations, memos and assistant answers in English and Arabic (Arabic text right-to-left in documents).
- **NFR-9 Portability of regulation:** The regulator layer is a pluggable pack (CBUAE first; QCB, SAMA, other GCC later) with no code changes for new rule values.
- **NFR-10 Accessibility:** WCAG 2.1 AA for the web UI.
- **NFR-11 Hardware:** Reference server = Linux or Windows Server, 16+ cores, 64 GB RAM, NVIDIA GPU ≥ 24 GB for the LLM [ASSUMPTION A4]. CPU-only mode works without LLM features.
- **NFR-12 Observability:** Health endpoints, structured logs, job metrics. No external telemetry.

## 6. Constraints and Guardrails

- **Regulatory:** CBUAE Rules cannot be loosened or deviated. Values with confidence below H must be verified before production (Appendix A, A.6 list).
- **Sharia:** Islamic vocabulary only. No compounding late charges counted as income. Sharia-prohibited sectors declined. A Sharia compliance note is delivered for the bank's Sharia board.
- **AI safety:** LLM never in the decision path. Guardrail on numbers. Drafts need human sign-off. Assistant restricted to Safe Actions.
- **Fairness:** Protected attributes excluded from the Learning Model (age allowed). Fairness monitoring per model.
- **Accountability:** Decision-support disclaimer in the UI and every report: *AI recommends, scores, drafts and flags; bank staff decide and are accountable.*

## 7. Integration and Dependencies

Temenos T24/Transact (API and DB views); bank data warehouse (SQL Server / Oracle / PostgreSQL); Active Directory / SSO; AECB (stored data; optional API);
local LLM runtime (Ollama or vLLM serving Qwen/Llama); bank SMTP for notifications (optional).

## 8. Rollout and Change Management

- **R1 Demo MVP:** FR-1–4, 6, 8–10, 14, 17–20 (personal finance + card), 30, 32, 33, 35, 39 (local accounts), 40 (templates), 43, 45, 61–63 (Docker), 66.
- **R2 Pilot-ready:** FR-5, 7, 11–13, 15, 16, 20 (auto + Ijara), 21–29, 31, 34, 37–42, 44 (basic), 57–60, 63 (Windows), 64.
- **R3 Full v1:** FR-16 (AECB API), 36, 38 (learning from overrides), 44 (full), 46–56, 65.
- **Pilot:** parallel run at the Islamic bank on historical and live applications. Compare with actual decisions and outcomes, then go live by segment.
- **Commercial readiness deliverables (non-code):** NDA/DPA templates, support SLA definition, training materials (user guide, role-based training, admin guide), and onboarding packs (security, UAE PDPL, CBUAE outsourcing/third-party, Sharia note).

## 9. Non-Goals (Explicit)

- No customer-facing AI text or customer channels.
- No upload of customer data files (CSV/Excel). Integration only. Policy documents and corporate PDFs are the only uploads.
- No AML/KYC investigation, fraud detection or collections module (future platform modules).
- No lifetime PD, per-customer expected loss output or IFRS 9 ECL engine. 12-month PD only (expected loss appears only in the simulator, stress tests and ROI, at portfolio level).
- No conventional (non-Islamic) vocabulary in v1.
- No automatic changes to limits or accounts in T24. All actions go through humans.
- No nationality-based scenarios or scoring.

## 10. Success Metrics

**Primary**
- **SM-1:** Default rate of model-approved cases vs. the bank's historical approvals at equal approval rate: **≥ 15% fewer defaults** in parallel-run back-testing [ASSUMPTION A5]. Validates FR-30–33.
- **SM-2:** Additional approvals at equal expected loss (from the Opportunity Finder / What-if): **≥ 5% more approvals** [ASSUMPTION A5]. Validates FR-46, FR-54.
- **SM-3:** Median time from application to Recommendation: **< 1 minute** (vs days). Validates FR-11, FR-37.
- **SM-4:** Estimated annual income uplift in AED, reported on the bank's own assumptions. Validates FR-55.

**Secondary**
- **SM-5:** Low-salary segment served: approval rate and default rate within appetite set by the Tenant. Validates FR-21.
- **SM-6:** Learning Model out-of-time Gini ≥ 0.30 and ≥ Scorecard Gini + 0.05. Validates FR-31, FR-57.
- **SM-7:** Zero CBUAE-rule breaches in Recommendations (audit sample). Validates FR-2, FR-3, FR-33.
- **SM-8:** 100% of past decisions replay identically. Validates FR-61.

**Counter-metrics (do not optimize)**
- **SM-C1:** Raw approval rate. Must not rise at the expense of SM-1.
- **SM-C2:** Override rate. Should not be pushed to zero; overrides are legitimate judgement.
- **SM-C3:** LLM verbosity / memo length.

## 11. Open Questions

1. Pilot bank identity, its T24 version and integration method (API vs. message queue).
2. The bank's Credit Policy and corporate thresholds (C16), and its deviation/authority matrix.
3. The bank's score scale and PD bands (default bands in FR-32 until supplied).
4. LGD, funding cost and Profit Rate grids for ROI (defaults until supplied).
5. Pricing model for the product (undecided; out of PRD).
6. CBUAE items to verify manually (Appendix A, A.6), including the card minimum income after Nov 2025.
7. Reference GPU size at the pilot bank.
8. Whether an anonymised real sample can be obtained before the pilot.

## 12. Assumptions Index

- **A1** (FR-8, FR-25): Corporate hard thresholds are empty until the bank supplies them. The demo shows corporate ratings without threshold knockouts except the combination rule and Sharia sectors.
- **A2** (FR-32): Default 1–10 PD bands as listed.
- **A3** (FR-57): Activation gate values (1,000 rows / 50 defaults / Gini 0.30).
- **A4** (NFR-11): Reference GPU ≥ 24 GB for a 14B-class model. 8–16 GB supports 7–8B models.
- **A5** (SM-1, SM-2): Target uplift percentages are proposals to confirm with the pilot bank.
- **A6** (FR-33): Model escalation grade default = 7.
