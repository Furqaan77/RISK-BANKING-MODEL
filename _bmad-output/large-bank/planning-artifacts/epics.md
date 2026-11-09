---
status: final
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/large-bank/planning-artifacts/prd.md
  - _bmad-output/large-bank/planning-artifacts/architecture.md
  - _bmad-output/large-bank/planning-artifacts/product-brief.md
  - _bmad-output/large-bank/planning-artifacts/discovery-answers.md
  - docs/regulatory/large-bank/us-federal-and-new-york.md
  - docs/regulatory/large-bank/uk-prudential-and-conduct.md
---

# AI Risk Score Card Global - Epics & Stories

## Overview

This document breaks AI Risk Score Card Global into epics and stories. It draws on the PRD (FR-1..FR-86, NFR-1..NFR-9), the
architecture spine (AD-1..AD-16), the two regulatory references (US and UK packs) and the discovery answers. It is organised by
release **R1 → R4**. The team is **14–18 people** in parallel squads: **Platform/DevOps, US Pack, UK Pack, Models & ML, Data
Engineering, Frontend, AI/LLM, QA**.

**Product-owner target:** all of v1 in **2–3 months**. This is **high risk**, so:
- Stories are sized at ≤ ~3 developer-days.
- Each epic names a **must-ship** subset.
- If time runs short, delivery follows R1 → R2 → R3 → R4 priority, and R1 must-ship comes first.
- Epics within a release depend only on earlier epics, so squads can work in parallel.

**Vocabulary:** conventional (loan, interest, APR, affordability, ability-to-pay). No real bank names.

**Golden worked examples** (executable acceptance tests, used in Epics 6, 7, 8 and 10):

| | Maria (New York, 24) | Tom (London, 19) |
|---|---|---|
| Income | Smoothed net $3,400/mo | Net £1,650/mo (Open Banking) |
| Outgoings | Rent $1,450; existing debt $310 + $180; essentials $900 | Rent share £500; essentials £620; phone £35 |
| Spare money | Residual **$560** | Disposable **£495** |
| Repayment tested | Minimum payment at a $5,000 limit = 1% principal + 24%/12 interest = **$150** → ability-to-pay PASS | £1,000 over 36 months at 29.9% nominal ≈ **£42/mo** → affordability PASS |
| Risk | PD **3.1%** → demo master-scale **grade 13** | PD **2.2%** → **grade 12** |
| Policy outcome | Thin-file starter cap $1,500 → **recommend $1,500 starter card** | Within the automation rule (starter card ≤ £1,000, grade ≤ 12, all rules pass) |
| Who decides | Routed to a human, because $1,500 > $1,000 automation line | **Auto-approved**, with Art 22C information and a human-review request path |
| Reasons | ≤ 4 deterministic reason codes | — |

**Demo 20-grade master scale (upper PD bounds, %):** 0.03, 0.05, 0.08, 0.12, 0.18, 0.26, 0.38, 0.55, 0.8, 1.15, 1.65, 2.4, 3.4, 4.9, 7, 10, 14, 20, 30, 100.

## Requirements Inventory

### Functional Requirements

**Platform, packs, policy**
- FR-1 [R1] Separate US and UK installs; multi-entity partitions with entity-aware rules.
- FR-2 [R1] Versioned, effective-dated US/UK market packs with sources and confidence; dated tables.
- FR-3 [R1] Tighten-only validation of bank/credit policy against the pack.
- FR-4 [R1] Policy-as-config, maker-checker, immutable versions, back-testing on history.
- FR-5 [R1] Three modes (challenger, add-on, engine) per product.
- FR-6 [R1] Automation rules per product/amount/grade; never auto-decline; mortgages and commercial always human (demo).
- FR-7 [R1] Replayable decision record; per-market retention.

**Data and integration**
- FR-8 [R1] Real-time scoring API for decision engines; p95 < 300 ms.
- FR-9 [R1] SFTP/file drop for back-tests and pilots.
- FR-10 [R2] Batch from the bank data platform; nightly 50M+.
- FR-11 [R2] Kafka event streaming for early warning.
- FR-12 [R2] Bureau adapters (Equifax, Experian, TransUnion; FICO/VantageScore; UK CRA); purpose codes; CRA used recorded.
- FR-13 [R2] Open Banking / cash-flow, income/employment verification, rent/utility/telecom adapters.
- FR-14 [R1] Consent records; purpose limitation; revocation stops use and recomputes.
- FR-15 [R1] Tokenisation, field-level encryption, role-based reveal; protected data only in the fairness zone.
- FR-16 [R3] Macro, climate and event data import.
- FR-17 [R1] Feature store with online/offline parity and lineage.

**Consumer and commercial assessment**
- FR-18 [R1] Cards and personal loans: rules, PD/LGD/EAD/EL, grade, reasons.
- FR-19 [R1] UK two-limb CONC 5.2A affordability.
- FR-20 [R1] US CARD Act ability-to-pay, under-21, DTI/residual income, MLA/SCRA/usury gates.
- FR-21 [R2] Mortgages (US ATR/QM/HMDA/HELOC; UK MCOB 11.6, LTI, BTL ICR, second charge).
- FR-22 [R4] Auto finance, UK overdrafts, UK BNPL.
- FR-23 [R1] Age rules and prohibited bases/proxies blocked.
- FR-24 [R1] Income & fraud consistency flags handed to the bank's fraud systems.
- FR-25 [R2] SME loans/lines/cards (UK Bank Referral Scheme, LSB, US 1071 fields).
- FR-26 [R2] Mid/large corporate rating with sector templates, stressed cash flow, market signals, covenant monitoring.
- FR-27 [R2] Exposure limits (SCCL, legal lending limit, Reg O, Reg W; UK large exposures) with aggregation.
- FR-28 [R2] CRE concentration, UK slotting/Basel 3.1 attributes, leveraged review flag.

**Models and scoring**
- FR-29 [R1] Three model families; champion-challenger on accuracy and fairness.
- FR-30 [R1] TTC score + daily PIT PD.
- FR-31 [R1] Deterministic reason codes; versioned reason library.
- FR-32 [R1] Master-scale mapping.
- FR-33 [R2] Model lifecycle: MRM approval, drift retrain, auto-suspend with fallback, overrides feed learning.
- FR-34 [R1] Reject inference.

**Growth: inclusion, Gen Z, opportunity, offers**
- FR-35 [R3] Inclusion engine (smoothed/gig/seasonal income, alternative data).
- FR-36 [R1] Starter card (UK £250–£1,000 / US $300–$1,500; reviews at 6/12 months; controls; persistent-debt protection).
- FR-37 [R1] One-month salary advance (≥ 3 months salary, ≤ 50% net pay, one at a time, affordability; pricing gates).
- FR-38 [R3] Credit-builder, student/graduate offers.
- FR-39 [R3] Readiness record 16–17 only; offer at 18; US authorised-user path.
- FR-40 [R3] Gen Z non-credit loyalty; no credit promotion to minors.
- FR-41 [R1/R3] Risk-vs-opportunity frontier (v1 in R1; CLV, risk budget, recommended policy in R3).
- FR-42 [R3] Opportunity-loss segments.
- FR-43 [R3] Product designer with simulation and maker-checker.
- FR-44 [R3] Next-best-offer & CLV within affordability, consent, prescreen, minors and fair-value rules.
- FR-45 [R2] Card limit increases with fresh affordability / ability-to-pay.

**Macro, climate and early warning**
- FR-46 [R3] Scenario engine (regulator, event, NGFS, custom).
- FR-47 [R3] Physical climate risk on collateral, insurance gap, transition risk, 1/5/30-year horizons.
- FR-48 [R2] Retail early warning signals.
- FR-49 [R3] Sector and job-loss warning.

**Fairness, validation and governance**
- FR-50 [R3] US fair-lending suite (AIR, proxies, LDA, BISG testing only).
- FR-51 [R3] UK Equality Act testing, Consumer Duty outcome MI, fair value.
- FR-52 [R3] Validator in a Box.
- FR-53 [R1] Champion-vs-challenger report.
- FR-54 [R2] Governance packs.

**Notices, safeguards and servicing**
- FR-55 [R2] Notice content generator (bank sends), EN/ES/CY.
- FR-56 [R2] UK Art 22C workflow and meaningful-review evidence.
- FR-57 [R2] US state AI laws (CO SB 26-189, CA ADMT).
- FR-58 [R2] UK vulnerability flags route to specialists.
- FR-59 [R4] UK persistent debt, overdraft repeat use, CONC 7 forbearance.
- FR-60 [R4] Cure prediction.
- FR-61 [R4] Forbearance recommender.
- FR-62 [R4] Collections contact strategy with guardrails.

**AI language model**
- FR-63 [R2] LLM port (bank LLM / vLLM; US/EU-origin default in US); template fallback.
- FR-64 [R2] Internal explanations with guardrail.
- FR-65 [R2] Customer letter drafts from deterministic reasons; human sign-off.
- FR-66 [R4] Credit memos and Policy Copilot.
- FR-67 [R3] Portfolio & risk chat (safe actions only).
- FR-68 [R4] Document AI (statements, US tax returns, loan agreements, bank statements).

**UX, deployment and operations**
- FR-69 [R1] Underwriter workspace with drill-down.
- FR-70 [R2] Queues, workflow, overrides.
- FR-71 [R1/R3] Strategy workspace (frontier, champion vs challenger; later segments, designer, what-if).
- FR-72 [R3] Board & CRO dashboard.
- FR-73 [R2] Enterprise SSO and roles.
- FR-74 [R1] Demo US Bank (2M) and Demo UK Bank (1M), synthetic champion, public benchmarks.
- FR-75 [R1] Kubernetes/OpenShift (Helm), Docker; air-gap; signed offline updates.
- FR-76 [R1] Bank HSM/vault; encryption at rest and in transit.
- FR-77 [R2] Signed licence; read-only on expiry; usage-count export with no customer data.
- FR-78 [R2] Incident hooks (US 4-hour / 36-hour, UK 2027 reporting, NY Part 500).
- FR-79 [R1] Income segment S0–S5 from verified gross income, fixed configurable bands per market.
- FR-80 [R1] Overlay tags (Gen Z, thin file, gig/self-employed, retiree, new to country, under-18 readiness).
- FR-81 [R1] Segment policy matrix as policy data (products, caps, DTI, residual floors, salary advance, LTI, automation).
- FR-82 [R1] Segment-aware decision order and golden tests (Maria, Tom, US S3 loan).
- FR-83 [R2] Nightly re-segmentation (up after 2 months, down after 3; immediate on verified job loss).
- FR-84 [R1] Segment-level calibration and monitoring; income band is not a scoring penalty by itself.
- FR-85 [R3] Fairness and Consumer Duty fair value by segment; no income-only knockouts except S0 eligibility.
- FR-86 [R3] Segment views and segment-aware stress & early warning.

### NonFunctional Requirements
- NFR-1 Real-time p95 < 300 ms, p99 < 800 ms; stateless horizontal scaling.
- NFR-2 Nightly 50M+ accounts re-score + PIT update within the batch window (target ≤ 4 h).
- NFR-3 No customer data leaves the install; deny-by-default egress; separate US/UK installs; US-person / UK-based support.
- NFR-4 SOC 2 Type II and ISO 27001 aligned controls; yearly pen test; SBOM; secure SDLC; OWASP ASVS L2; MFA.
- NFR-5 Determinism and replay; effective-dated packs and policies.
- NFR-6 99.9% availability of the real-time API; 24/7 support; graceful degradation.
- NFR-7 WCAG 2.2 AA.
- NFR-8 Regulatory, fair-lending, load/chaos and LLM red-team suites in CI.
- NFR-9 Every recommendation has ranked reasons; reason stability tested.

### Additional Requirements
- **AD-1** Pure deterministic decision core; replay from stored inputs.
- **AD-2** Signed, effective-dated market packs; tighten-only on publish; new country = new pack.
- **AD-3** One install per market; `entity_id` on every row; no cross-install API.
- **AD-4** Single feature definition run online and in Spark; parity test gates release.
- **AD-5** Two-limb assessment is structural; a score never overrides a failed affordability or ability-to-pay result.
- **AD-6** Deterministic reasons; LLM advisory, async, behind a port, with guardrail.
- **AD-7** Mode-agnostic core; automation rules evaluated after `assess`; declines never automated.
- **AD-8** MLflow registry; serve only `bank_mrm_approved`; auto-suspend with fallback; champion models in a sandbox.
- **AD-9** Segregated fairness zone; feature pipelines and models cannot read it.
- **AD-10** Tokenisation at ingestion; reveal service; consent checked at feature build.
- **AD-11** Append-only, hash-chained records.
- **AD-12** Real-time latency budget of 300 ms p95.
- **AD-13** Generic maker-checker ChangeRequest.
- **AD-14** Egress deny-by-default; air-gap; signed updates.
- **AD-15** Scenario/climate overlays on PIT only.
- **AD-16** Conventional vocabulary; market terms live in pack text.

**Compliance and commercial deliverables (non-code):**
- SR 26-2 and SS1/23 model documentation, including the LLM control pack
- TPRM / SS2/21 pack
- DPIA and children's DPIA
- Art 22C design
- GLBA / NY Part 500 mapping
- CO / CA ADMT deployer documentation
- SM&CR / model-owner mapping
- SOC 2 Type II and ISO 27001 readiness; yearly pen test
- Source-code escrow and exit & transition plan
- Support SLA (24/7 real-time API; US-person / UK-based support)
- Contract positions (liability cap, indemnities, regulator access rights)
- Training materials

### UX Design Requirements
- **UX-1 (UJ-1, UJ-2)** Underwriter decision view:
  - recommendation, grade, PD/LGD/EAD/EL
  - separate credit-risk and affordability / ability-to-pay panels with drill-down maths
  - ranked reasons
  - automation status and route (auto / human)
- **UX-2 (UJ-2)** Art 22C information panel and human-review request tracking (UK).
- **UX-3 (UJ-3)** Strategy workspace: frontier chart with current and recommended policy, opportunity segments, product designer, submit as change request.
- **UX-4 (UJ-4)** Validation workspace: champion vs challenger, stability, calibration, fairness, report export.
- **UX-5 (UJ-5)** Board & CRO dashboard: scenarios, climate hazard exposure, early-warning trends.
- **UX-6 (UJ-6)** Collections workspace: cure ranking, forbearance options, letter drafts with approval.
- **UX-7 (UJ-7)** Commercial analyst view: document extraction confirmation, sector template rating, exposure aggregation, memo draft.
- **UX-8 (UJ-8)** Demo-bank banner and guided demo scenarios.
- **UX-9** WCAG 2.2 AA throughout; English UI; letters in English/Spanish/Welsh.

### FR Coverage Map

| FR | Epic.Story | FR | Epic.Story | FR | Epic.Story |
|---|---|---|---|---|---|
| FR-1 | 1.2, 1.3 | FR-27 | 13.4, 13.5 | FR-53 | 9.1, 9.2 |
| FR-2 | 2.1, 2.2 | FR-28 | 13.6 | FR-54 | 19.1–19.8 |
| FR-3 | 2.3 | FR-29 | 5.1, 5.2 | FR-55 | 15.1, 15.2, 15.3 |
| FR-4 | 2.4, 2.5 | FR-30 | 5.4 | FR-56 | 15.4 |
| FR-5 | 2.6 | FR-31 | 5.5 | FR-57 | 15.5 |
| FR-6 | 2.7 | FR-32 | 5.3 | FR-58 | 15.6 |
| FR-7 | 1.5, 1.6 | FR-33 | 14.1–14.5 | FR-59 | 25.1–25.4 |
| FR-8 | 8.1–8.4 | FR-34 | 5.6 | FR-60 | 26.1 |
| FR-9 | 3.5 | FR-35 | 20.1, 20.2 | FR-61 | 26.2 |
| FR-10 | 11.1, 11.2 | FR-36 | 6.5, 7.5 | FR-62 | 26.3, 26.4 |
| FR-11 | 11.3 | FR-37 | 6.6, 7.6 | FR-63 | 17.1 |
| FR-12 | 11.4 | FR-38 | 20.3 | FR-64 | 17.2, 17.3 |
| FR-13 | 11.5 | FR-39 | 20.4 | FR-65 | 17.4 |
| FR-14 | 3.3 | FR-40 | 20.5 | FR-66 | 28.3, 28.4 |
| FR-15 | 3.4, 3.6 | FR-41 | 9.3, 21.1 | FR-67 | 24.3 |
| FR-16 | 22.1 | FR-42 | 21.2 | FR-68 | 28.1, 28.2 |
| FR-17 | 3.1, 3.2 | FR-43 | 21.3 | FR-69 | 10.1, 10.2 |
| FR-18 | 6.1, 7.1 | FR-44 | 21.4 | FR-70 | 16.2 |
| FR-19 | 7.2, 7.3 | FR-45 | 16.4 | FR-71 | 10.3, 21.5 |
| FR-20 | 6.2, 6.3 | FR-46 | 22.2 | FR-72 | 24.1, 24.2 |
| FR-21 | 12.1–12.5 | FR-47 | 22.3 | FR-73 | 16.1 |
| FR-22 | 27.1–27.3 | FR-48 | 18.3 | FR-74 | 4.1–4.5 |
| FR-23 | 6.4, 7.4 | FR-49 | 22.4 | FR-75 | 1.7 |
| FR-24 | 6.7, 7.7 | FR-50 | 23.1, 23.2 | FR-76 | 1.4 |
| FR-25 | 13.1 | FR-51 | 23.3 | FR-77 | 18.1 |
| FR-26 | 13.2, 13.3 | FR-52 | 23.4, 23.5 | FR-78 | 18.2 |
| FR-79 | 29.1 | FR-82 | 29.4 | FR-85 | 29.7 |
| FR-80 | 29.2 | FR-83 | 29.5 | FR-86 | 29.8 |
| FR-81 | 29.3 | FR-84 | 29.6 | | |

## Epics List

| # | Title | Release | Squad | Depends on |
|---|---|---|---|---|
| 1 | Platform Foundation & Separate Installs | R1 | Platform/DevOps | — |
| 2 | Market Packs, Policy Engine & Modes | R1 | US Pack + UK Pack | 1 |
| 3 | Data Foundation: Feature Store, Consent & Tokenisation | R1 | Data Engineering | 1 |
| 4 | Demo US & UK Banks and Benchmarks | R1 | Data Engineering + Models & ML | 1 |
| 5 | Models, Scoring & Reason Codes | R1 | Models & ML | 3, 4 |
| 6 | US Consumer Assessment: Cards, Loans, Starter Card, Salary Advance | R1 | US Pack | 2, 3, 5 |
| 7 | UK Consumer Assessment: Cards, Loans, Starter Card, Salary Advance | R1 | UK Pack | 2, 3, 5 |
| 8 | Real-time Scoring API & Performance | R1 | Platform/DevOps + QA | 2, 5, 6, 7 |
| 9 | Champion vs Challenger & Frontier v1 | R1 | Models & ML | 4, 5, 6, 7 |
| 10 | Underwriter & Strategy Workspace v1 | R1 | Frontend | 8, 9 |
| 11 | Enterprise Data Integration | R2 | Data Engineering | 3 |
| 12 | Mortgages US & UK | R2 | US Pack + UK Pack | 2, 5 |
| 13 | Commercial Assessment & Exposure Limits | R2 | Models & ML + US/UK Pack | 2, 5 |
| 14 | Model Lifecycle & Model-Risk Governance | R2 | Models & ML | 5 |
| 15 | Notices, Safeguards & State AI Laws | R2 | US Pack + UK Pack | 5, 6, 7 |
| 16 | Enterprise Access, Workflow & Limit Increases | R2 | Platform/DevOps + Frontend | 1, 6, 7, 10 |
| 17 | AI Language Model Foundations | R2 | AI/LLM | 5, 8 |
| 18 | Pilot Operations: Licence, Incidents & Early Warning | R2 | Platform/DevOps + Data Engineering | 1, 3, 5 |
| 19 | Governance & Commercial Packs | R2 | QA + all squads | 1–10 |
| 20 | Inclusion Engine & Gen Z | R3 | Models & ML + Data Engineering | 3, 5, 6, 7, 11 |
| 21 | Opportunity, Product Designer & Offers | R3 | Models & ML + Frontend | 2, 9, 10 |
| 22 | Macro, Climate & Sector Early Warning | R3 | Models & ML + Data Engineering | 5, 11, 18 |
| 23 | Fair Lending & Validator in a Box | R3 | Models & ML + QA | 3, 5, 9, 14 |
| 24 | Board & CRO Dashboard and Portfolio Chat | R3 | Frontend + AI/LLM | 9, 17, 18 |
| 25 | UK Servicing: Persistent Debt, Overdrafts & Forbearance Rules | R4 | UK Pack | 7, 11 |
| 26 | Collections Cure & Contact Strategy | R4 | Models & ML + AI/LLM | 5, 17, 25 |
| 27 | Auto Finance, UK Overdraft & UK BNPL Products | R4 | US Pack + UK Pack | 6, 7 |
| 28 | Document AI, Credit Memos & Policy Copilot | R4 | AI/LLM | 2, 13, 17 |
| 29 | Income Segmentation & Segment Policy | R1 (29.5 R2; 29.7–29.8 R3) | US Pack + UK Pack + Models & ML | 2, 3, 5 |

---

## Epic 1: Platform Foundation & Separate Installs [R1]

**Squad:** Platform/DevOps. **Depends on:** none.
**Goal:** A running, secure skeleton deployable as separate US and UK installs, with entity partitions, audit chain, replayable decision records, keys in the bank vault, and air-gap packaging.
**Must-ship:** 1.1, 1.2, 1.3, 1.5, 1.6.

### Story 1.1: Repository skeleton and CI pipeline

As a developer,
I want the repo laid out per the architecture with CI running lint, types, tests, SBOM and security scans,
So that every squad starts on a consistent, gated base.

**Acceptance Criteria:**

**Given** the architecture source tree (core, services, ports, adapters, api, batch, stream, ui, packs, synth, deploy, tests)
**When** a PR is opened
**Then** CI runs ruff, mypy, pytest, front-end lint/tests, CycloneDX SBOM, SAST and dependency audit, and blocks merge on failure (NFR-4, NFR-8)
**And** an import-linter rule fails the build if `core` imports I/O, network, clock or LLM modules (AD-1)

### Story 1.2: Install profile and separate US/UK deployments

As a platform engineer,
I want an install profile (`market: US|UK`) that selects the pack, data stores and support settings,
So that US and UK run as separate installs with no shared data.

**Acceptance Criteria:**

**Given** two installs started from the same release with `market: US` and `market: UK`
**When** the install-isolation test runs
**Then** neither install can resolve or call the other's endpoints, databases, registries or queues (FR-1, AD-3, NFR-3)
**And** the market pack loaded matches the profile and is shown in the health endpoint

### Story 1.3: Entity partitions

As a bank administrator,
I want entities (bank, card issuer, ring-fenced bank, affiliates) as partitions inside an install,
So that rules and data are scoped per legal entity.

**Acceptance Criteria:**

**Given** two entities in one install
**When** a user scoped to entity A queries decisions
**Then** no entity B rows are returned (FR-1, AD-3)
**And** every table has a non-null `entity_id` (migration test)

### Story 1.4: Keys in bank HSM/vault and encryption

As an information-security officer,
I want encryption keys held in the bank's HSM or vault and all data encrypted at rest and in transit,
So that the vendor never holds key material.

**Acceptance Criteria:**

**Given** a PKCS#11 HSM or Vault configured
**When** the app encrypts a sensitive field or opens a DB connection
**Then** keys are fetched from the HSM/vault only and never written to disk or logs (FR-76, NFR-4)
**And** TLS is enforced on every internal and external connection (startup check fails otherwise)

### Story 1.5: Append-only hash-chained audit

As an auditor,
I want every write action and decision event stored append-only with a hash chain,
So that tampering is detectable.

**Acceptance Criteria:**

**Given** the app DB role
**When** an UPDATE or DELETE is attempted on `audit_event` or `decision_record`
**Then** it is denied by grants (AD-11)
**And** a chain-verification job detects any altered row in a test fixture

### Story 1.6: Decision record and exact replay

As a model validator,
I want each assessment stored with inputs, pack/policy/model versions, outputs and reasons, replayable exactly,
So that any decision can be explained later.

**Acceptance Criteria:**

**Given** 1,000 stored assessments
**When** the replay job re-runs `assess` with the stored snapshot and versions
**Then** outputs and reasons match byte-for-byte (FR-7, NFR-5, AD-1)
**And** retention defaults apply per market (US ≥ 25 months, UK term + 6 years with litigation hold), configurable

### Story 1.7: Helm, Compose and air-gap bundle

As a bank platform team,
I want Helm charts for Kubernetes/OpenShift, Docker Compose for demos, and a signed air-gap bundle,
So that the product installs inside any bank network.

**Acceptance Criteria:**

**Given** an air-gapped cluster
**When** the signed bundle is installed
**Then** all images, packs and assets load with egress blocked, and a tampered bundle fails Ed25519 verification (FR-75, AD-14)
**And** a deny-by-default egress policy is applied and listed in the health report (NFR-3)

## Epic 2: Market Packs, Policy Engine & Modes [R1]

**Squad:** US Pack + UK Pack (shared core). **Depends on:** Epic 1.
**Goal:**
- Signed, effective-dated US and UK packs.
- A safe rule DSL with tighten-only validation and maker-checker policy versions.
- Three operating modes, and automation rules that can never auto-decline.

**Must-ship:** 2.1, 2.2, 2.3, 2.4, 2.7.

### Story 2.1: Pack format and safe rule DSL

As a policy engineer,
I want rules expressed as signed pack data with an allow-listed expression evaluator,
So that rules are auditable and no code is executed from config.

**Acceptance Criteria:**

**Given** a rule with id, layer, applies_to, condition, severity, source, confidence and effective dates
**When** the evaluator runs malicious inputs (`__import__`, attribute access, lambdas, huge exponents)
**Then** they are rejected and nothing executes (FR-2, AD-2)
**And** each rule result carries its source citation

### Story 2.2: US and UK pack v1 with dated tables

As a compliance analyst,
I want the US and UK pack values from the regulatory references loaded with effective dates and confidence,
So that the product applies the right value on the right date.

**Acceptance Criteria:**

**Given** the US QM 2026 table (first lien ≥ $137,958: APR–APOR < 2.25 pp; $82,775–137,958 < 3.5 pp; < $82,775 < 6.5 pp; safe harbor 1.5 pp)
**When** an application dated 2026-03-01 is evaluated, and another dated 2025-12-31 with the 2025 table
**Then** each resolves to its own year's thresholds (FR-2, NFR-5)
**And** values below H confidence show a "verify" flag in the pack viewer

### Story 2.3: Tighten-only validation

As a CRO,
I want bank or credit policy values that are looser than the pack rejected,
So that the bank never configures below the law.

**Acceptance Criteria:**

**Given** a bank policy setting the UK mortgage stress minimum to +0.5 pp, or a US MAPR cap of 40% for covered borrowers
**When** the policy is published
**Then** publication fails naming the pack rule and both values (FR-3, AD-2)
**And** a stricter value (+1.5 pp, 30%) publishes successfully

### Story 2.4: Policy versions with maker-checker

As a policy owner,
I want changes submitted as change requests approved by a different user,
So that no single person can change credit policy.

**Acceptance Criteria:**

**Given** a change request created by user A
**When** user A tries to approve it
**Then** approval is refused by the service and by the DB constraint (FR-4, AD-13)
**And** user B's approval creates a new immutable policy version referenced by later decision records

### Story 2.5: Back-test any policy version on history

As a risk strategist,
I want to run any policy version over historical applications,
So that I see its impact before it goes live.

**Acceptance Criteria:**

**Given** the Demo US Bank history and two policy versions
**When** a back-test runs
**Then** it reports approvals, expected loss and the rule-level reasons for each version (FR-4)
**And** results are reproducible for the same inputs (NFR-5)

### Story 2.6: Challenger, add-on and engine modes

As a bank architect,
I want to choose challenger, add-on or engine mode per product,
So that the product fits beside or instead of our decision engine.

**Acceptance Criteria:**

**Given** the same application under the three modes
**When** it is assessed
**Then** `assess` output is identical. Challenger persists shadow results only, add-on returns score/reasons only, and engine returns a full decision (FR-5, AD-7)

### Story 2.7: Automation rules with the never-auto-decline invariant

As a CRO,
I want to configure where automation is allowed,
So that clear cases move fast and declines always reach a person.

**Acceptance Criteria:**

**Given** the demo automation rules (starter card / salary advance ≤ 1,000 at grade ≤ 12 auto-approve; CLI for good accounts after fresh affordability; mortgages and commercial always human)
**When** any assessment results in decline, under any rule configuration including a rule explicitly set to auto-decline
**Then** the route is always "human review" (FR-6, AD-7)
**And** a mortgage or commercial application is never auto-approved under the demo rules

## Epic 3: Data Foundation: Feature Store, Consent & Tokenisation [R1]

**Squad:** Data Engineering. **Depends on:** Epic 1.
**Goal:**
- A canonical data model and a feature store with online/offline parity.
- Consent-aware feature building and tokenised PII.
- A segregated fairness zone, and SFTP intake for pilots.

**Must-ship:** 3.1, 3.2, 3.4, 3.5.

### Story 3.1: Canonical data model

As a data engineer,
I want a canonical model for applicants, accounts, transactions, bureau, income, alternative data and collateral,
So that adapters map once and features never read source schemas.

**Acceptance Criteria:**

**Given** sample US and UK records
**When** they are validated against the CDM (Pydantic)
**Then** valid records pass, invalid ones fail with field-level errors, and money is in integer minor units with currency (FR-17, AD-4)

### Story 3.2: Feature store with online/batch parity

As an ML engineer,
I want features defined once and served online (Redis via Feast) and computed in Spark,
So that training and serving never diverge.

**Acceptance Criteria:**

**Given** 100,000 sample customers
**When** features are computed online and in Spark
**Then** every feature matches within tolerance (exact for categorical, ≤ 1e-9 for numeric), and CI blocks release on mismatch (FR-17, AD-4)
**And** feature lineage records source tables and version

### Story 3.3: Consent records and revocation recomputation

As a data-protection officer,
I want consent per data source with purpose and expiry, and revocation to stop use,
So that only consented data drives decisions.

**Acceptance Criteria:**

**Given** a customer with Open Banking consent for "credit assessment"
**When** consent is revoked
**Then** the next feature build excludes Open Banking data, and the customer's scores are recomputed and logged (FR-14, AD-10)
**And** the data is never used for marketing purposes (purpose limitation test)

### Story 3.4: Tokenisation at ingestion and role-based reveal

As an information-security officer,
I want names, SSN/NI numbers and addresses tokenised on ingestion with role-based reveal,
So that PII does not spread.

**Acceptance Criteria:**

**Given** an ingested record
**When** it is stored and logged
**Then** only tokens appear outside the vault, and logs contain no PII (log scanner test) (FR-15, AD-10)
**And** a reveal by a permitted role is audited, and a non-permitted role is refused

### Story 3.5: SFTP file drop for back-tests

As a pilot lead,
I want encrypted SFTP intake of history files into the CDM,
So that back-tests can start before integrations are built.

**Acceptance Criteria:**

**Given** a PGP-encrypted file in the agreed layout
**When** it lands in the drop folder
**Then** it is decrypted, validated, tokenised and loaded, with a per-file quality report (FR-9)

### Story 3.6: Segregated fairness zone

As a fair-lending analyst,
I want protected attributes and proxies stored in a separate zone,
So that models can never use them.

**Acceptance Criteria:**

**Given** the fairness zone schema
**When** feature pipelines or the model-training service attempt to read it
**Then** access is denied by DB grants, and the import-linter fails if code under core/features or core/scoring references it (FR-15, AD-9)
**And** fairness jobs inside the zone output aggregates only

## Epic 4: Demo US & UK Banks and Benchmarks [R1]

**Squad:** Data Engineering + Models & ML. **Depends on:** Epic 1.
**Goal:** Synthetic Demo US Bank (2M accounts) and Demo UK Bank (1M), with known ground truth, a synthetic champion scorecard to beat, simulated stress history, and public-dataset benchmarks.
**Must-ship:** 4.1, 4.2, 4.3.

### Story 4.1: Demo US Bank generator (2M)

As a sales engineer,
I want a synthetic US book with bureau, cash-flow and transaction data,
So that demos run at realistic scale.

**Acceptance Criteria:**

**Given** a seed
**When** the generator runs
**Then** it produces 2,000,000 accounts across cards, loans, mortgages and SME with bureau fields, MCC transactions and outcomes, with no real persons (FR-74)
**And** output is deterministic for the same seed

### Story 4.2: Demo UK Bank generator (1M)

As a sales engineer,
I want a synthetic UK book with CRA, Open Banking and transaction data,
So that UK demos run at realistic scale.

**Acceptance Criteria:**

**Given** a seed
**When** the generator runs
**Then** it produces 1,000,000 accounts, including thin-file, gig, blue-collar and 16–17 junior-account profiles (readiness only) (FR-74)

### Story 4.3: Known ground truth and synthetic champion

As a model validator,
I want built-in default risk and a synthetic champion scorecard,
So that the demo can prove whether the challenger wins.

**Acceptance Criteria:**

**Given** the demo banks
**When** the champion scorecard (bureau-centric logistic with a thin-file cut-off) is scored
**Then** the ground-truth default process is documented, and the champion declines Maria-like thin-file profiles (FR-74, FR-53)

### Story 4.4: Simulated recession and regional disaster in history

As a CRO,
I want history that contains a recession and a regional disaster,
So that stress and early warning can be demonstrated.

**Acceptance Criteria:**

**Given** the generated history
**When** default rates are plotted by month and region
**Then** a recession window and a regional disaster spike are visible and labelled (FR-74)

### Story 4.5: Public dataset benchmarks

As a model-risk lead,
I want benchmark runs on public credit datasets,
So that accuracy claims are credible outside our synthetic data.

**Acceptance Criteria:**

**Given** at least two public credit datasets with licences recorded
**When** the benchmark pipeline runs
**Then** it reports Gini/AUC for each model family with fixed seeds (FR-74, FR-29)

## Epic 5: Models, Scoring & Reason Codes [R1]

**Squad:** Models & ML. **Depends on:** Epics 3, 4.
**Goal:**
- Three model families with champion-challenger selection on accuracy and fairness.
- Master-scale mapping, TTC and baseline PIT scores.
- Deterministic reason codes and reject inference.

**Must-ship:** 5.1, 5.3, 5.5.

### Story 5.1: Train the three model families

As an ML engineer,
I want constrained LightGBM, EBM and a logistic scorecard trained per segment,
So that the bank's model-risk team can choose the right transparency.

**Acceptance Criteria:**

**Given** the Demo US and UK training data
**When** training runs
**Then** each family produces a registered artifact with monotonic constraints where directions are known, and with fixed seeds (FR-29)
**And** no feature comes from the fairness zone (AD-9)

### Story 5.2: Champion-challenger selection on accuracy and fairness

As a model-risk lead,
I want the best model selected on out-of-time accuracy AND fairness,
So that we never trade fairness for accuracy silently.

**Acceptance Criteria:**

**Given** three trained candidates
**When** selection runs
**Then** candidates failing the fairness threshold are excluded, and the remaining best Gini is proposed with a comparison table (FR-29)

### Story 5.3: Master-scale mapping

As a credit-risk manager,
I want PD mapped to the bank's master scale,
So that grades match our internal language.

**Acceptance Criteria:**

**Given** the demo 20-grade scale (upper bounds 0.03 … 100%)
**When** PD = 3.1% and PD = 2.2% are mapped
**Then** they return grade 13 and grade 12 respectively (FR-32)
**And** the scale is configurable per bank

### Story 5.4: TTC score and baseline PIT PD

As a portfolio manager,
I want a through-the-cycle score for decisions and a point-in-time PD,
So that decisions are stable while monitoring tracks the economy.

**Acceptance Criteria:**

**Given** a customer
**When** scored
**Then** both a TTC score and a PIT PD are returned. In R1 the PIT PD equals the TTC PD × 1.0 baseline overlay. Decisions use TTC unless policy references PIT (FR-30, AD-15)

### Story 5.5: Deterministic reason codes

As a compliance officer,
I want ranked reason codes from model attribution and rules through a versioned library,
So that reasons are accurate and stable.

**Acceptance Criteria:**

**Given** Maria's assessment
**When** reasons are produced
**Then** at most 4 ranked codes are returned (e.g. limited credit history, income variability), identical on replay (FR-31, NFR-9, AD-6)
**And** the reason-stability test (small input perturbations) passes the configured threshold

### Story 5.6: Reject inference

As an ML engineer,
I want reject inference using through-the-door data,
So that the model is not biased toward previously approved customers.

**Acceptance Criteria:**

**Given** a demo history with rejects
**When** training runs with reject inference on and off
**Then** both runs are recorded, and the method and its out-of-time impact are documented in the model card (FR-34)

## Epic 6: US Consumer Assessment: Cards, Loans, Starter Card, Salary Advance [R1]

**Squad:** US Pack. **Depends on:** Epics 2, 3, 5.
**Goal:**
- US cards and personal loans with CARD Act ability-to-pay, the under-21 rules, and DTI/residual income.
- MLA/SCRA/usury gates, age and proxy rules.
- The starter card and salary advance.
- Fraud consistency flags.

**Must-ship:** 6.1, 6.2, 6.3, 6.5.

### Story 6.1: US cards and loans assessment

As an underwriter,
I want a US card/loan assessment with PD/LGD/EAD/EL, grade and reasons,
So that I get a complete recommendation.

**Acceptance Criteria:**

**Given** a US application
**When** assessed
**Then** the output contains separate credit-risk and ability-to-pay sections, EL = PD × LGD × EAD, a master-scale grade and reasons (FR-18, AD-5)

### Story 6.2: CARD Act ability-to-pay with the Maria worked example

As a US compliance officer,
I want the minimum-payment ability-to-pay test on verified income and obligations,
So that card lines meet the CARD Act.

**Acceptance Criteria:**

**Given** Maria: smoothed net income $3,400, rent $1,450, obligations $490, essentials $900, requested limit $5,000 at 24% APR with 1% principal
**When** ability-to-pay is computed
**Then** residual = **$560**, minimum payment = **$150**, and the result is PASS (FR-20)
**And** with bank thin-file starter cap $1,500 the recommendation is a **$1,500 starter card**

### Story 6.3: Under-21 branch and DTI/residual policy

As a US compliance officer,
I want under-21 applicants to require independent income or a cosigner aged 21+, and the bank's DTI/residual-income rules applied,
So that young applicants are handled lawfully.

**Acceptance Criteria:**

**Given** a 20-year-old without independent ability to pay
**When** assessed
**Then** the result is refer/decline unless a cosigner aged 21+ is attached, and a credit-line increase on a cosigned account requires cosigner consent (FR-20)
**And** a bank DTI cap (demo 43%) is applied from bank policy, not the pack

### Story 6.4: MLA, SCRA, usury and age gates

As a US compliance officer,
I want rate and age gates applied by borrower status, charter, state and size,
So that pricing never breaks federal or state law.

**Acceptance Criteria:**

**Given** a covered servicemember, an SCRA pre-service loan, and a NY-law state-chartered personal loan of $50,000
**When** pricing at 38% MAPR, 9% and 18% respectively is proposed
**Then** each is blocked (MLA 36% cap, SCRA 6% cap, NY civil 16% cap) (FR-20)
**And** the same NY loan from a national bank exporting home-state rates is not capped by NY. A $3M commercial loan is outside NY usury. Any rate > 25% on NY-governed consumer credit is always blocked
**And** an applicant aged 62+ never receives a negative age contribution, and prohibited bases or declared proxies are absent from features (FR-23)

### Story 6.5: US starter card

As a product manager,
I want a US starter card ($300–$1,500) with 6/12-month reviews, spending controls and persistent-debt protection,
So that thin-file customers start safely.

**Acceptance Criteria:**

**Given** a thin-file applicant passing ability-to-pay
**When** assessed
**Then** the limit is within $300–$1,500 per bank policy, reviews are scheduled at 6 and 12 months with fresh ability-to-pay, and customer-chosen controls (e.g. block gambling MCC) are recorded (FR-36)

### Story 6.6: US one-month salary advance

As a product manager,
I want salary-advance eligibility and amount scored,
So that blue-collar customers get short-term help safely.

**Acceptance Criteria:**

**Given** salary credited ≥ 3 months, net pay $2,800, no open advance
**When** assessed
**Then** the maximum is $1,400 (50% of net) and one advance at a time is enforced (FR-37)
**And** pricing comes from bank policy, and any price breaching MLA 36% or state small-dollar caps is blocked

### Story 6.7: US income & fraud consistency flags

As a fraud liaison,
I want declared-vs-verified income gaps, synthetic-identity and bust-out signals flagged to the bank's fraud system,
So that we inform but never decide fraud.

**Acceptance Criteria:**

**Given** declared income 40% above verified income
**When** assessed
**Then** an inconsistency flag is emitted to the FraudSink port, and the credit decision path is unchanged except for routing to human review (FR-24)

## Epic 7: UK Consumer Assessment: Cards, Loans, Starter Card, Salary Advance [R1]

**Squad:** UK Pack. **Depends on:** Epics 2, 3, 5.
**Goal:**
- UK cards and personal loans with two-limb CONC 5.2A affordability, verified income, proportionality and cumulative-increase tracking.
- Equality Act/age rules.
- The starter card, salary advance and fraud consistency checks.

**Must-ship:** 7.1, 7.2, 7.3, 7.5.

### Story 7.1: UK cards and loans assessment

As an underwriter,
I want a UK assessment with separate credit-risk and affordability verdicts,
So that a good score never hides unaffordable lending.

**Acceptance Criteria:**

**Given** a UK application with PD in grade 3 and an affordability FAIL
**When** assessed
**Then** the recommendation cannot be approve without a human deviation (FR-18, FR-19, AD-5)

### Story 7.2: CONC 5.2A affordability with the Tom worked example

As a UK compliance officer,
I want affordability on verified income and expenditure,
So that lending meets CONC 5.2A.

**Acceptance Criteria:**

**Given** Tom: Open Banking net income £1,650, rent share £500, essentials £620 (checked against ONS norms), phone £35, requesting a £1,000 starter card
**When** affordability is computed with repayment over 36 months at 29.9% nominal APR
**Then** disposable = **£495**, repayment ≈ **£42/month**, and the verdict is **PASS** (FR-19)
**And** PD 2.2% maps to grade 12, and the automation rule (≤ £1,000, grade ≤ 12, all rules pass) gives **auto-approve** with Art 22C information attached

### Story 7.3: Verified income, proportionality and cumulative increases

As a UK compliance officer,
I want self-declared income alone rejected as sufficient, proportional depth by product tier, and cumulative small increases tracked,
So that CONC 5.2A.4–20 are met.

**Acceptance Criteria:**

**Given** an application with only declared income
**When** assessed
**Then** it is referred for verification (CONC 5.2A.16) (FR-19)
**And** three small limit increases that together exceed the "significant" threshold trigger a full assessment
**And** any use of the "obvious affordability" route is logged with justification

### Story 7.4: UK Equality Act and age handling

As a UK fair-lending analyst,
I want age used only with documented justification and protected characteristics/proxies blocked,
So that indirect discrimination risk is controlled.

**Acceptance Criteria:**

**Given** a model using age without a justification record
**When** the policy is published
**Then** publication fails, and postcode/name/language proxies flagged by the proxy audit are excluded or justified (FR-23)

### Story 7.5: UK starter card

As a product manager,
I want a UK starter card (£250–£1,000) with 6/12-month reviews, controls and persistent-debt protection,
So that thin-file and Gen Z customers start safely.

**Acceptance Criteria:**

**Given** a thin-file applicant passing affordability
**When** assessed
**Then** the limit is within £250–£1,000. Increases at 6/12 months require a fresh CONC 5.2A assessment and are blocked if the account shows persistent-debt signals (FR-36)

### Story 7.6: UK one-month salary advance

As a product manager,
I want salary-advance eligibility for UK customers,
So that blue-collar customers get short-term help safely.

**Acceptance Criteria:**

**Given** salary credited ≥ 3 months, net pay £1,800, no open advance, not in persistent debt or financial difficulty
**When** assessed
**Then** the maximum is £900 and one at a time is enforced (FR-37)
**And** if bank pricing would make it high-cost short-term credit (e.g. APR ≥ 100%), the HCSTC caps (0.8%/day, 100% total cost) are enforced as gates

### Story 7.7: UK income & fraud consistency flags

As a fraud liaison,
I want declared vs verified income inconsistency flagged (CONC 5.2A.36) along with synthetic-identity/bust-out signals,
So that the bank's fraud system can act.

**Acceptance Criteria:**

**Given** declared income inconsistent with Open Banking credits
**When** assessed
**Then** the application is referred, and a flag is sent to FraudSink with no fraud decision made by us (FR-24)

## Epic 8: Real-time Scoring API & Performance [R1]

**Squad:** Platform/DevOps + QA. **Depends on:** Epics 2, 5, 6, 7.
**Goal:** REST and gRPC scoring for bank decision engines within 300 ms p95, graceful degradation, and end-to-end golden tests.
**Must-ship:** 8.1, 8.2, 8.3.

### Story 8.1: REST and gRPC ScoreService

As a bank engine integrator,
I want REST `/api/v1/score` and gRPC `ScoreService`,
So that FICO-, PowerCurve-, SAS-, Pega- or in-house engines can call us.

**Acceptance Criteria:**

**Given** an OpenAPI/proto contract
**When** a valid request is sent
**Then** the response includes grade, PD/LGD/EAD/EL, affordability or ability-to-pay result, reasons, automation route and a decision-record id (FR-8, AD-7)
**And** errors use the standard envelope with trace_id

### Story 8.2: Latency budget and k6 load test

As a platform engineer,
I want the real-time path proven under load,
So that we fit inside the bank engine's SLA.

**Acceptance Criteria:**

**Given** the reference sizing and the Demo US Bank
**When** k6 runs at the agreed peak rate for 30 minutes
**Then** p95 < 300 ms and p99 < 800 ms with no errors (FR-8, NFR-1, AD-12)
**And** per-stage timings (features, rules, model, reasons) are reported

### Story 8.3: Golden end-to-end tests: Maria and Tom

As QA,
I want both worked examples as end-to-end API tests,
So that the core promise never regresses.

**Acceptance Criteria:**

**Given** the US install with Maria's data
**When** scored via the API
**Then** recommendation = $1,500 starter card, grade 13, route = human (above the $1,000 automation line), ≤ 4 reasons (FR-6, FR-8, FR-20)
**And** on the UK install Tom's application returns affordability PASS, grade 12, route = auto-approve, with Art 22C information in the response

### Story 8.4: Graceful degradation and chaos tests

As a platform engineer,
I want degraded modes tested,
So that the API stays available.

**Acceptance Criteria:**

**Given** the challenger model is unavailable or suspended
**When** requests arrive
**Then** responses fall back to the configured fallback (bank champion score or our scorecard) and mark degraded mode (NFR-6, AD-8)
**And** chaos tests (pod kill, adapter timeout) keep availability within target

## Epic 9: Champion vs Challenger & Frontier v1 [R1]

**Squad:** Models & ML. **Depends on:** Epics 4, 5, 6, 7.
**Goal:** Prove "better than your champion" with a report, and show the first risk-vs-opportunity frontier for cards and loans.
**Must-ship:** 9.1, 9.3.

### Story 9.1: Champion vs challenger computation

As a model-risk lead,
I want champion and challenger compared on the same population,
So that the claim is evidenced.

**Acceptance Criteria:**

**Given** the synthetic champion and our challenger on Demo US and UK out-of-time samples
**When** the comparison runs
**Then** it reports Gini/AUC, approvals at equal expected loss, AIR (US) / outcome gaps (UK), and stability (PSI) (FR-53)

### Story 9.2: Champion-vs-challenger report export

As a CRO,
I want an exportable report,
So that I can take it to the credit committee.

**Acceptance Criteria:**

**Given** a completed comparison
**When** exported
**Then** a PDF/Excel report with method, data window, results and limitations is produced, reproducible from stored inputs (FR-53, NFR-5)

### Story 9.3: Frontier v1 for cards and loans

As a risk strategist,
I want approvals, balances, expected loss, risk-adjusted profit and inclusion impact for each policy option,
So that I see opportunity as well as risk.

**Acceptance Criteria:**

**Given** at least 10 policy options (cut-off and limit variants) and bank profit inputs (demo defaults)
**When** the frontier runs
**Then** each option shows approvals, balances, EL, risk-adjusted profit (income − funding − EL − opex) and inclusion count, the efficient set is marked, and the current policy is marked (FR-41)

## Epic 10: Underwriter & Strategy Workspace v1 [R1]

**Squad:** Frontend. **Depends on:** Epics 8, 9.
**Goal:** The underwriter decision view with drill-down and the first strategy workspace (frontier, champion vs challenger), with a demo banner.
**Must-ship:** 10.1, 10.2.

### Story 10.1: Decision view

As an underwriter,
I want recommendation, grade, PD/LGD/EAD/EL, reasons and route on one screen,
So that I can act quickly.

**Acceptance Criteria:**

**Given** Maria's case
**When** opened
**Then** it shows a $1,500 starter card, grade 13, ≤ 4 reasons, "Human review: above automation line", and separate credit-risk and ability-to-pay panels (FR-69, UX-1)
**And** the page meets WCAG 2.2 AA checks (NFR-7)

### Story 10.2: Drill-down maths and rule results

As an underwriter,
I want to see the ability-to-pay or affordability arithmetic and every rule with its source,
So that I can explain the recommendation.

**Acceptance Criteria:**

**Given** Tom's case
**When** the affordability panel is expanded
**Then** income £1,650, rent £500, essentials £620, phone £35, disposable £495, repayment ≈ £42, PASS are shown, plus every rule with its pack citation and the Art 22C information panel (FR-69, UX-1, UX-2)

### Story 10.3: Strategy workspace v1

As a risk strategist,
I want the frontier chart and the champion-vs-challenger summary,
So that I can choose a policy option.

**Acceptance Criteria:**

**Given** frontier results
**When** viewed
**Then** an interactive chart shows options (EL vs approvals/profit) with the current policy marked, and hovering shows each option's numbers (FR-71, UX-3)
**And** demo installs show a persistent demo-bank banner (UX-8)

## Epic 11: Enterprise Data Integration [R2]

**Squad:** Data Engineering. **Depends on:** Epic 3.
**Goal:** Batch from bank data platforms for 50M+ nightly, Kafka streaming, bureau, Open Banking/cash-flow, income verification and alternative data adapters.
**Must-ship:** 11.1, 11.2, 11.4.

### Story 11.1: Batch connectors to the bank data platform

As a data engineer,
I want read-only connectors for Snowflake, Databricks, Teradata and Oracle,
So that the book can be scored nightly.

**Acceptance Criteria:**

**Given** read-only credentials
**When** a write is attempted
**Then** it fails and is logged, and reads map into the CDM through configurable views (FR-10)

### Story 11.2: Nightly 50M+ re-score at scale

As a platform engineer,
I want the nightly job sized for 50M+ accounts,
So that the morning views are fresh.

**Acceptance Criteria:**

**Given** a 5M-account scaled test on the reference Spark cluster
**When** the nightly job runs
**Then** measured throughput extrapolates linearly to ≤ 4 h for 50M (documented scaling factor and cluster size), and PIT PD is updated for all accounts (FR-10, NFR-2)

### Story 11.3: Kafka streaming consumers

As a data engineer,
I want transaction, payment and account events consumed from the bank's Kafka,
So that early-warning features update intraday.

**Acceptance Criteria:**

**Given** Avro events on `install.entity.accounts.events`
**When** consumed
**Then** online features update within the configured lag, and replaying the topic is idempotent (FR-11)

### Story 11.4: Bureau adapters

As a credit-risk manager,
I want Equifax, Experian and TransUnion adapters (FICO/VantageScore in the US; CRA files in the UK),
So that bureau data feeds features and notices.

**Acceptance Criteria:**

**Given** a US pull
**When** executed
**Then** a permissible-purpose code is recorded. In the UK, the CRA used is recorded for CCA s.157 disclosure. Bureau key factors are stored separately from bank reasons (FR-12)

### Story 11.5: Open Banking, income verification and alternative data

As an inclusion lead,
I want consented Open Banking/aggregator data, income/employment verification and rent/utility/telecom data,
So that thin-file customers can be scored fairly.

**Acceptance Criteria:**

**Given** consents recorded per source
**When** data is ingested
**Then** only consented purposes use it, and expired consent excludes the source on the next build (FR-13, FR-14)

## Epic 12: Mortgages US & UK [R2]

**Squad:** US Pack + UK Pack. **Depends on:** Epics 2, 5.
**Goal:** US ATR/QM with HMDA support and HELOC; UK MCOB 11.6 stress, LTI tagging, buy-to-let and second charge.
**Must-ship:** 12.1, 12.3.

### Story 12.1: US ATR and QM classifier

As a US mortgage underwriter,
I want ATR factors checked and QM status classified with dated thresholds,
So that mortgages meet Reg Z.

**Acceptance Criteria:**

**Given** a first-lien loan of $300,000 dated 2026-05-01 with APR–APOR 2.0 pp and points-and-fees 2.5%
**When** classified
**Then** the result is General QM (< 2.25 pp; ≤ 3%), safe harbor (< 1.5 pp is false → rebuttable presumption), and DTI/residual income is considered and verified with no pack DTI cap (FR-21)

### Story 12.2: HMDA fields and denial reasons

As a US compliance officer,
I want HMDA data points and up to 4 denial reasons mapped from reason codes,
So that reporting is consistent with decisions.

**Acceptance Criteria:**

**Given** a denied mortgage application
**When** exported
**Then** HMDA denial-reason codes (≤ 4) map from our reason codes, and demographic fields come only from the fairness zone, never from decision features (FR-21, AD-9)

### Story 12.3: UK MCOB 11.6 affordability and stress

As a UK mortgage underwriter,
I want affordability on capital and interest with the regulatory stress,
So that mortgages meet MCOB.

**Acceptance Criteria:**

**Given** a 2-year fix at 4.5% with a forward-curve reversion rate of 5.2% over 5 years
**When** stressed
**Then** stress rate = max(5.2%, 4.5% + 1pp) = 5.5% is applied, and a 5-year fix is exempt from the 5-year stress test (FR-21)
**And** LTI ≥ 4.5x is tagged, and the internal high-LTI share limit is configurable (no hard-coded 15%)

### Story 12.4: UK buy-to-let and second charge

As a UK mortgage underwriter,
I want buy-to-let ICR stress and second-charge assessment that stresses the first mortgage,
So that these products are covered.

**Acceptance Criteria:**

**Given** a second-charge application
**When** assessed
**Then** the first mortgage payment is also stressed per MCOB 11.6.18A, and buy-to-let uses bank ICR rules (FR-21)

### Story 12.5: US HELOC

As a US underwriter,
I want HELOC assessment with ability-to-repay on the drawn-down payment,
So that home equity lines are covered.

**Acceptance Criteria:**

**Given** a HELOC application
**When** assessed
**Then** payment is computed at the fully drawn amount under bank policy, and CLTV and collateral are recorded (FR-21)

## Epic 13: Commercial Assessment & Exposure Limits [R2]

**Squad:** Models & ML + US/UK Pack. **Depends on:** Epics 2, 5.
**Goal:**
- SME and corporate ratings with sector templates and stressed cash flow.
- Exposure limits with aggregation.
- CRE and leveraged flags.

**Must-ship:** 13.1, 13.2, 13.4.

### Story 13.1: SME assessment

As an SME credit officer,
I want SME loans/lines/cards rated from financials and bank statements,
So that small businesses get consistent decisions.

**Acceptance Criteria:**

**Given** a declined UK SME
**When** finalised
**Then** a Bank Referral Scheme offer event with a consent flag is emitted, and LSB-standard decline reasons are produced (FR-25)
**And** US applications store Section 1071 fields (ready for 2028) with demographics only in the fairness zone

### Story 13.2: Five-dimension corporate rating with sector templates

As a corporate analyst,
I want weighted dimensions (35/20/15/10/20) and sector templates (CRE, leveraged, SME, large corporate),
So that ratings fit the business.

**Acceptance Criteria:**

**Given** a company with dimension scores 48/55/78/60/80
**When** rated with default weights
**Then** the weighted total is 61.5, and a CRE template changes factors per template config (FR-26)

### Story 13.3: Stressed cash flow, market signals and covenants

As a corporate analyst,
I want facility sizing on EBITDA −30% stress, optional market signals and covenant/cash monitoring,
So that limits survive bad years.

**Acceptance Criteria:**

**Given** EBITDA of 10m and debt service of 6m
**When** stressed by 30%
**Then** stressed DSCR = 7/6 ≈ 1.17 is reported against the policy minimum, and covenant headroom is tracked when covenants are confirmed (FR-26)

### Story 13.4: US exposure limits

As a US credit-risk officer,
I want SCCL, legal lending limit, Reg O and Reg W checks before decision,
So that limits are never breached.

**Acceptance Criteria:**

**Given** Tier 1 of $100bn and existing group exposure of $24.5bn
**When** a $1bn facility to the same connected group is proposed
**Then** it is blocked/referred (SCCL 25%), and 15% applies for a major-to-major counterparty (FR-27)
**And** the 15% + 10% legal lending limit uses borrower combination, an insider triggers Reg O board approval, and an affiliate triggers the Reg W workflow

### Story 13.5: UK large exposures and sponsor aggregation

As a UK credit-risk officer,
I want connected-client and sponsor aggregation against 25% (15% G-SII to G-SII) of Tier 1,
So that large exposures are respected.

**Acceptance Criteria:**

**Given** a sponsor-backed group with five portfolio companies
**When** aggregated
**Then** the total is checked against the limit, and a breach routes to referral (FR-27)

### Story 13.6: CRE concentration, slotting attributes and leveraged flag

As a portfolio manager,
I want CRE concentration checks, UK slotting/Basel 3.1 attributes and a leveraged flag,
So that concentration and leverage are visible.

**Acceptance Criteria:**

**Given** total CRE of 320% of capital with 55% growth in 36 months
**When** the dashboard runs
**Then** a US review flag is raised. Debt/EBITDA of 6.5x raises the heightened-review flag (configurable, not a hard decline). UK exposures carry exposure class and Art 124E attributes as data only (FR-28)

## Epic 14: Model Lifecycle & Model-Risk Governance [R2]

**Squad:** Models & ML. **Depends on:** Epic 5.
**Goal:** Bank model-risk approval gating, drift-triggered retraining, auto-suspension with fallback, and override learning.
**Must-ship:** 14.1, 14.3.

### Story 14.1: MRM approval gate

As a model-risk manager,
I want models to serve only after bank model-risk approval via maker-checker,
So that nothing unvalidated decides.

**Acceptance Criteria:**

**Given** a registered model without `bank_mrm_approved`
**When** activation is attempted
**Then** it is refused. Approval by a different user with the validator role sets the status and activates it (FR-33, AD-8, AD-13)

### Story 14.2: Drift detection and challenger retrain

As a model-risk manager,
I want PSI/performance drift to trigger a challenger retrain,
So that models stay current without silent changes.

**Acceptance Criteria:**

**Given** PSI > 0.25 on a key feature
**When** monitoring runs
**Then** a challenger is retrained and registered but not activated (FR-33)

### Story 14.3: Auto-suspension with fallback

As a CRO,
I want a breaching model suspended automatically,
So that decisions fall back safely.

**Acceptance Criteria:**

**Given** a breach of the configured suspension limits
**When** detected
**Then** the model status becomes `suspended`, serving switches to the configured fallback within one request cycle, and alerts are sent (FR-33, AD-8)

### Story 14.4: Overrides captured and fed to learning

As an ML engineer,
I want underwriter overrides and their outcomes captured,
So that retraining can learn from them carefully.

**Acceptance Criteria:**

**Given** overrides with reasons and later outcomes
**When** the training dataset is built
**Then** override features and labels are available behind a configuration flag, with an override-bias report (FR-33)

### Story 14.5: Bank champion models in a sandbox

As a model validator,
I want the bank's champion model files loaded in an isolated sandbox,
So that we can compare without risk.

**Acceptance Criteria:**

**Given** PMML, ONNX and pickle artifacts
**When** loaded
**Then** they run in a sandbox without network or filesystem access outside its volume (FR-33, AD-8)

## Epic 15: Notices, Safeguards & State AI Laws [R2]

**Squad:** US Pack + UK Pack. **Depends on:** Epics 5, 6, 7.
**Goal:** Notice content the bank sends (US and UK), UK Art 22C workflow, US state AI-law support, and UK vulnerability routing.
**Must-ship:** 15.1, 15.2, 15.4.

### Story 15.1: Reg B adverse-action content and timers

As a US compliance officer,
I want adverse-action content with ≤ 4 specific reasons and deadline timers,
So that notices are compliant and on time.

**Acceptance Criteria:**

**Given** a completed application declined on day 0
**When** notice content is generated
**Then** it has ≤ 4 specific reasons from reason codes (never LLM-selected) and a due date of day 30. A counteroffer not accepted sets day 90. Escalation fires before the deadline (FR-55, AD-6)

### Story 15.2: FCRA and risk-based pricing content

As a US compliance officer,
I want FCRA disclosures with the score, range and key factors kept separate from bank reasons,
So that both duties are met.

**Acceptance Criteria:**

**Given** a decline based partly on a bureau score
**When** content is generated
**Then** it includes score, range, up to 4 key factors (5 if inquiries is a factor), CRA details and the 60-day free-report right, listed separately from bank reasons (FR-55)
**And** a risk-based pricing notice is triggered when terms are materially less favourable

### Story 15.3: UK decline content and letter templates in EN/ES/CY

As a compliance officer,
I want compliance-approved templates in English, Spanish (US) and Welsh (UK),
So that the bank's letter systems can send the right language.

**Acceptance Criteria:**

**Given** a UK decline and a requested Welsh template
**When** content is generated
**Then** the approved Welsh template is used with deterministic reasons and Art 22C rights, and content goes to NoticeSink. We do not send letters ourselves (FR-55)

### Story 15.4: UK Art 22C workflow and meaningful-review evidence

As a UK DPO,
I want information, representations, human intervention and contest tracked to SLA, plus evidence of meaningful human review,
So that automated and human decisions are lawful.

**Acceptance Criteria:**

**Given** Tom's auto-approved case and another automated outcome he contests
**When** he requests human review
**Then** a case opens in the review queue with SLA timers, and the outcome is recorded (FR-56)
**And** for human-in-loop decisions, time-on-case, override rate and reviewer authority are recorded

### Story 15.5: US state AI-law support (CO, CA)

As a US compliance officer,
I want Colorado and California ADMT support,
So that 2027 obligations can be met per state.

**Acceptance Criteria:**

**Given** a Colorado resident with an adverse outcome
**When** processed with the CO rule set active (effective 2027-01-01)
**Then** a notice and a plain-language explanation within 30 days are generated, human review on request is available, and deployer documentation is exportable (FR-57)

### Story 15.6: UK vulnerability routing

As a UK conduct lead,
I want vulnerability flags to route to specialists and never auto-decline,
So that vulnerable customers are treated fairly.

**Acceptance Criteria:**

**Given** a vulnerability flag on an application
**When** assessed under any automation rule
**Then** the route is a specialist human queue, and no automated outcome is produced (FR-58)

## Epic 16: Enterprise Access, Workflow & Limit Increases [R2]

**Squad:** Platform/DevOps + Frontend. **Depends on:** Epics 1, 6, 7, 10.
**Goal:** Enterprise SSO and roles, queues and workflow with overrides, and compliant card-limit increases.
**Must-ship:** 16.1, 16.2.

### Story 16.1: Enterprise SSO and roles

As a bank IAM admin,
I want SAML/OIDC with Entra ID, Okta or Ping and our role set,
So that access follows bank identity.

**Acceptance Criteria:**

**Given** the IdP groups mapped to roles (underwriter, credit officer, strategy/policy, validator, collections, fraud liaison, CRO/board, compliance, admin, auditor)
**When** users sign in with MFA
**Then** each sees only permitted features, and every endpoint enforces its permission (FR-73, NFR-4)

### Story 16.2: Queues, workflow and overrides

As a credit officer,
I want case queues by authority with override reasons,
So that engine-mode decisions are controlled.

**Acceptance Criteria:**

**Given** engine mode
**When** a case is routed to a human
**Then** it appears in the right queue, and approve/return/escalate/override actions require a reason code and are audited (FR-70)

### Story 16.3: Accessibility and UI hardening

As an accessibility lead,
I want automated WCAG 2.2 AA checks on all workflow screens,
So that the UI is usable by all staff.

**Acceptance Criteria:**

**Given** the workflow screens
**When** axe-core checks and keyboard-only tests run in CI
**Then** there are no AA violations (NFR-7)

### Story 16.4: Card limit increases

As a card risk manager,
I want CLI recommendations with a fresh affordability (UK) or ability-to-pay (US) check,
So that increases are safe and lawful.

**Acceptance Criteria:**

**Given** a good account in persistent-debt status (UK) or a cosigned under-21 account without cosigner consent (US)
**When** a CLI is evaluated
**Then** it is blocked. A clean account passing the fresh check can be auto-approved where the automation rule allows (FR-45, FR-6)

## Epic 17: AI Language Model Foundations [R2]

**Squad:** AI/LLM. **Depends on:** Epics 5, 8.
**Goal:** The LLM port (bank platform or vLLM), grounded internal explanations with guardrail, red-team tests, and customer-letter drafts from deterministic reasons.
**Must-ship:** 17.1, 17.2.

### Story 17.1: LLM port with bank platform and vLLM adapters

As an AI platform owner,
I want the LLM behind a port with adapters for the bank's approved platform and vLLM,
So that the bank chooses the model.

**Acceptance Criteria:**

**Given** a US install with no bank LLM
**When** the default is resolved
**Then** a US/EU-origin open model is selected, the model provenance is recorded, and with the LLM down every function uses templates (FR-63, AD-6)

### Story 17.2: Grounded explanations with guardrail

As a compliance officer,
I want explanations built only from facts JSON, with a number/reason guardrail,
So that no invented numbers reach staff.

**Acceptance Criteria:**

**Given** a fake LLM that inserts "DBR 45%" not present in the facts
**When** an explanation is generated
**Then** the text is discarded, the template is used, and the event is logged (FR-64, AD-6)

### Story 17.3: LLM red-team suite

As QA,
I want prompt-injection, hallucination and tone tests in CI,
So that LLM behaviour is monitored.

**Acceptance Criteria:**

**Given** the red-team corpus
**When** CI runs
**Then** injection attempts cannot change reasons or actions, and the hallucination rate is reported per model version (FR-64, NFR-8)

### Story 17.4: Customer letter drafts

As an operations lead,
I want letter drafts from approved templates and deterministic reasons, with human sign-off,
So that letters are accurate and approved.

**Acceptance Criteria:**

**Given** a decline with reasons
**When** a draft is created
**Then** it uses an approved template, cannot add or reorder reasons, and is marked draft until signed by an authorised user (FR-65)

## Epic 18: Pilot Operations: Licence, Incidents & Early Warning [R2]

**Squad:** Platform/DevOps + Data Engineering. **Depends on:** Epics 1, 3, 5.
**Goal:** Licence and usage metering, incident hooks, and the retail early-warning signals for pilots.
**Must-ship:** 18.1, 18.3.

### Story 18.1: Signed licence and usage-count export

As a commercial lead,
I want a signed licence and a monthly usage export for per-decision billing,
So that billing works without customer data.

**Acceptance Criteria:**

**Given** a licence with bank ID, modules, volume tier and expiry
**When** it expires
**Then** the system becomes read-only and never deletes data (FR-77)
**And** the monthly usage export contains only counts by product/mode/month, and a scanner confirms no tokens, IDs or customer fields

### Story 18.2: Incident hooks

As an operations manager,
I want incident detection and notification hooks,
So that the bank meets its reporting duties.

**Acceptance Criteria:**

**Given** a service disruption lasting ≥ 4 hours
**When** detected
**Then** a service-provider notice event is raised for the bank (supporting its 36-hour regulator notice). UK incident fields for 2027 reporting and Part 500 72-hour support data are included (FR-78)

### Story 18.3: Retail early-warning signals

As a portfolio manager,
I want income-shock, credit-stress, spending-behaviour and external-exposure signals,
So that deterioration is seen before delinquency.

**Acceptance Criteria:**

**Given** a customer with salary stopped, utilisation from 35% to 85%, gambling MCC spikes and spend > income for 3 months
**When** the nightly/stream job runs
**Then** each signal is raised with its triggering data, and the customer joins the watch-list (FR-48)

## Epic 19: Governance & Commercial Packs [R2]

**Squad:** QA + all squads (documents). **Depends on:** Epics 1–10.
**Goal:** The documents a GSIB needs to onboard, validate and contract with us.
**Must-ship:** 19.1, 19.2, 19.3.

### Story 19.1: Model documentation pack

As a model validator,
I want SR 26-2 and SS1/23-aligned documentation per model,
So that validation can start immediately.

**Acceptance Criteria:**

**Given** each model version
**When** the pack is generated
**Then** it covers purpose, data and lineage, methodology, assumptions, limitations, performance, stability, fairness, explainability and monitoring (FR-54)
**And** it includes a separate LLM control pack (grounding, hallucination tests, prompt/version control)

### Story 19.2: Third-party risk and security pack

As a TPRM analyst,
I want a TPRM/SS2/21 pack,
So that onboarding can proceed.

**Acceptance Criteria:**

**Given** the pack
**When** reviewed
**Then** it includes architecture/data flows, SBOM, secure SDLC, pen-test summary, BCP, sub-processor list, escrow terms, exit & transition plan, and regulator audit/access rights clauses (FR-54, NFR-4)

### Story 19.3: Data-protection packs

As a DPO,
I want DPIA, children's DPIA and Art 22C design documents (UK) plus GLBA/Part 500 mapping (US),
So that data protection is evidenced.

**Acceptance Criteria:**

**Given** the packs
**When** reviewed
**Then** they describe lawful bases, the fairness-zone segregation, the readiness-at-16–17-only design with no marketing profiling of minors, consent/revocation and retention per market (FR-54)

### Story 19.4: State ADMT deployer documentation

As a US compliance officer,
I want deployer documentation for Colorado and California,
So that the bank can meet ADMT duties.

**Acceptance Criteria:**

**Given** the export
**When** generated
**Then** it states intended use, training-data categories, limitations and human-review instructions (FR-54, FR-57)

### Story 19.5: Accountability mapping

As a UK SMF holder,
I want every model, pack and policy mapped to an accountable owner (SM&CR; US model owner/validator),
So that responsibility is clear.

**Acceptance Criteria:**

**Given** the inventory
**When** exported
**Then** each item lists owner, validator and approval history (FR-54)

### Story 19.6: SOC 2 Type II and ISO 27001 readiness

As a security lead,
I want control mapping and evidence collection for SOC 2 Type II and ISO 27001, plus a yearly independent pen test plan,
So that certifications can be obtained.

**Acceptance Criteria:**

**Given** the control matrix
**When** reviewed
**Then** each control has an owner, evidence source and test frequency (FR-54, NFR-4)

### Story 19.7: Commercial terms and SLA

As a commercial lead,
I want a support SLA and contract positions,
So that GSIB contracting is faster.

**Acceptance Criteria:**

**Given** the documents
**When** reviewed
**Then** they cover 24/7 real-time API support, US-person/UK-based support, liability cap and indemnities, escrow, the exit plan, regulator access, and cyber & PI insurance levels (FR-54)

### Story 19.8: Training materials

As a bank trainer,
I want role-based guides,
So that users adopt the product correctly.

**Acceptance Criteria:**

**Given** the guides
**When** used in training
**Then** there is one per role (underwriter, strategy, validator, collections, admin, auditor), covering the automation rules and the never-auto-decline principle (FR-54)

## Epic 20: Inclusion Engine & Gen Z [R3]

**Squad:** Models & ML + Data Engineering. **Depends on:** Epics 3, 5, 6, 7, 11.
**Goal:** Fair scoring of irregular income and thin files, credit-builder and student/graduate products, readiness for 16–17s, and non-credit Gen Z loyalty, all within the law on minors.
**Must-ship:** 20.1, 20.4.

### Story 20.1: Smoothed, gig and seasonal income

As an inclusion lead,
I want income smoothed over 6–12 months with a volatility penalty, gig/multiple employers combined and seasonality handled,
So that blue-collar income is measured fairly.

**Acceptance Criteria:**

**Given** 12 months of credits from a warehouse employer and a delivery platform
**When** income is computed
**Then** the smoothed income, volatility penalty and seasonal adjustment are shown, and foreseeable falls are stressed for UK affordability (FR-35)

### Story 20.2: Thin-file alternative-data scoring

As an inclusion lead,
I want rent, utility and telecom history in thin-file scoring,
So that customers without bureau depth can qualify.

**Acceptance Criteria:**

**Given** a no-bureau applicant with 24 months of on-time rent
**When** scored with consented alternative data
**Then** the PD reflects the history, and the source and consent are recorded (FR-35)

### Story 20.3: Credit-builder and student/graduate offers

As a product manager,
I want credit-builder loans, rent reporting (18+), the UK graduate overdraft and US 18–20 cards under CARD Act rules,
So that young adults can build credit safely.

**Acceptance Criteria:**

**Given** a 19-year-old US student without independent income and no cosigner
**When** a card is assessed
**Then** it is not approved, and a credit-builder alternative is suggested (FR-38)

### Story 20.4: Readiness record for ages 16–17 only

As a DPO,
I want readiness profiling only for ages 16–17, with no marketing profiling of minors,
So that we comply with children's data rules.

**Acceptance Criteria:**

**Given** a 15-year-old junior account and a 16-year-old junior account
**When** the readiness job runs
**Then** the 15-year-old is excluded, the 16-year-old gets an education-only readiness record, and no marketing segment or offer is created before 18 (FR-39)
**And** at 18, a pre-assessed offer is produced only after a full affordability/ability-to-pay check. The US authorised-user path is offered only where the bank enables it

### Story 20.5: Gen Z non-credit loyalty

As a marketing lead,
I want savings boosts, education rewards, partner perks and a graduation path for under-18s,
So that young customers grow with the bank.

**Acceptance Criteria:**

**Given** an under-18 customer
**When** loyalty rewards are generated
**Then** none promote credit (UK CCA s.50; US CARD Act campus rules), and a test asserts no credit product appears in any under-18 communication content (FR-40)

## Epic 21: Opportunity, Product Designer & Offers [R3]

**Squad:** Models & ML + Frontend. **Depends on:** Epics 2, 9, 10.
**Goal:** The full frontier with CLV and recommended policy, opportunity-loss segments, the product designer and compliant next-best-offers.
**Must-ship:** 21.1, 21.2.

### Story 21.1: Frontier with CLV, risk budget and recommended policy

As a CRO,
I want CLV, a risk-budget view and an AI-recommended policy point within appetite,
So that I can pick the best trade-off.

**Acceptance Criteria:**

**Given** the bank's risk appetite (max EL rate)
**When** the frontier runs
**Then** the recommended point is the highest risk-adjusted profit within appetite, shown with its trade-off versus current policy, and submitting it creates a change request (FR-41, AD-13)

### Story 21.2: Opportunity-loss segments

As a risk strategist,
I want segments the current policy declines that would be profitable,
So that missed business is visible.

**Acceptance Criteria:**

**Given** the Demo UK Bank
**When** the analysis runs
**Then** segments (e.g. gig workers, graduates, thin-file) are listed with count, value, expected loss and profit (FR-42)

### Story 21.3: Product designer

As a product manager,
I want AI-proposed limit ladders, pricing/fees, eligibility and features, simulated on the book,
So that new products are designed with evidence.

**Acceptance Criteria:**

**Given** a proposed starter-card ladder and APR
**When** simulated
**Then** loss and profit are reported. Any price breaching usury/MLA/HCSTC caps or failing the UK fair-value check is flagged, and approval is via maker-checker (FR-43)

### Story 21.4: Next-best-offer and CLV

As a relationship manager,
I want safe offers ranked by CLV,
So that cross-sell is responsible.

**Acceptance Criteria:**

**Given** customers who are vulnerable, in persistent debt, in collections or under 18
**When** offers are generated
**Then** none receive credit offers. FCRA prescreen offers meet firm-offer rules with criteria fixed before the pull, and marketing consent is required (FR-44)

### Story 21.5: Strategy workspace: segments, designer, what-if

As a risk strategist,
I want the segments, designer and what-if in the strategy workspace,
So that I can work end to end.

**Acceptance Criteria:**

**Given** the workspace
**When** I change a policy parameter
**Then** approvals, EL and profit update, and I can save a scenario and submit it as a change request (FR-71, UX-3)

## Epic 22: Macro, Climate & Sector Early Warning [R3]

**Squad:** Models & ML + Data Engineering. **Depends on:** Epics 5, 11, 18.
**Goal:** Scenario engine, climate hazards on collateral, and sector/job-loss warnings, feeding daily PIT PD.
**Must-ship:** 22.1, 22.2.

### Story 22.1: Macro, climate and event data import

As a data engineer,
I want regulator scenarios, NGFS paths, hazard maps, labour data and sanctions events importable offline or via optional feed,
So that the scenario engine has inputs.

**Acceptance Criteria:**

**Given** an air-gapped install
**When** a signed data bundle is imported
**Then** datasets load with version and date. Optional feeds are off by default and allow-listed when enabled (FR-16, AD-14)

### Story 22.2: Scenario engine

As a CRO,
I want regulator, event, climate and custom scenarios applied to the book,
So that I see PD and loss impacts.

**Acceptance Criteria:**

**Given** the Fed severely adverse scenario and a custom "regional hurricane + mild recession" scenario
**When** run on the Demo US Bank
**Then** PIT PD uplift and expected loss by segment, sector and region are reported, and TTC decisions are unchanged (FR-46, AD-15)

### Story 22.3: Physical climate risk on collateral

As a mortgage risk manager,
I want flood, wildfire, storm, subsidence and heat risk on collateral with an insurance-gap flag and 1/5/30-year horizons,
So that climate exposure is visible.

**Acceptance Criteria:**

**Given** properties geocoded to ZIP/postcode
**When** hazard overlays run
**Then** each gets hazard scores per horizon and an insurance-gap flag where risk exceeds the threshold. Corporates get transition-risk scores by sector (FR-47)

### Story 22.4: Sector and job-loss warning

As a portfolio manager,
I want borrowers whose employer or sector faces layoffs, sanctions or supply shocks flagged,
So that I can act early.

**Acceptance Criteria:**

**Given** a sanctions event affecting a sector and a layoff spike in BLS/ONS data
**When** the nightly job runs
**Then** affected borrowers are flagged with the event reference, and the flags feed the watch-list (FR-49, FR-48)

## Epic 23: Fair Lending & Validator in a Box [R3]

**Squad:** Models & ML + QA. **Depends on:** Epics 3, 5, 9, 14.
**Goal:** US and UK fairness suites, LDA search, and validation reports for our models and the bank's.
**Must-ship:** 23.1, 23.4.

### Story 23.1: US fairness suite (AIR, proxies)

As a fair-lending officer,
I want AIR, marginal effects and proxy detection on every model build, using BISG for testing only,
So that disparate impact is controlled.

**Acceptance Criteria:**

**Given** a model build
**When** CI runs the fairness suite inside the fairness zone
**Then** AIR by group is reported, and builds below the threshold are blocked. BISG never leaves the zone or enters features (FR-50, AD-9, NFR-8)

### Story 23.2: LDA search

As a fair-lending officer,
I want a search for less-discriminatory alternatives with comparable accuracy,
So that we document business necessity.

**Acceptance Criteria:**

**Given** a candidate model
**When** LDA search runs
**Then** alternative models with accuracy within tolerance and better AIR are listed with trade-offs (FR-50)

### Story 23.3: UK Equality Act and Consumer Duty MI

As a UK conduct lead,
I want indirect-discrimination tests, cohort outcome MI and fair-value checks,
So that Consumer Duty is evidenced.

**Acceptance Criteria:**

**Given** monitoring data in the fairness zone (DPA 2018 Sch 1 para 8)
**When** reports run
**Then** approval, pricing, arrears and complaint outcomes by cohort (including vulnerability) are reported, along with fair-value results per product (FR-51)

### Story 23.4: Validator in a Box: champion vs challenger

As a model validator,
I want accuracy, stability, calibration, backtests and fairness for the bank's models and ours,
So that validation takes weeks, not months.

**Acceptance Criteria:**

**Given** the bank champion's scores and outcomes, and optionally its model file in the sandbox
**When** validation runs
**Then** a comparison with our challenger on the same population is produced (FR-52)

### Story 23.5: SR 26-2 and SS1/23 report formats

As a model validator,
I want reports structured for each regime,
So that they go straight into our validation process.

**Acceptance Criteria:**

**Given** a completed validation
**When** exported
**Then** US (SR 26-2: conceptual soundness, outcomes analysis, monitoring) and UK (SS1/23 five principles, post-model adjustments) formats are available (FR-52)

## Epic 24: Board & CRO Dashboard and Portfolio Chat [R3]

**Squad:** Frontend + AI/LLM. **Depends on:** Epics 9, 17, 18.
**Goal:** Board and CRO KPIs, and a portfolio chat limited to safe actions.
**Must-ship:** 24.1.

### Story 24.1: Board & CRO dashboard

As a CRO,
I want champion-vs-challenger gains, opportunity captured, macro & climate exposure and early warning & collections on one dashboard,
So that the board sees value and risk.

**Acceptance Criteria:**

**Given** the demo data
**When** the dashboard loads
**Then** the four KPI areas show values with drill-down and the source of every number (FR-72, UX-5)

### Story 24.2: Scenario and climate views on the dashboard

As a board member,
I want scenario losses and hazard-zone exposure,
So that I understand the next crisis.

**Acceptance Criteria:**

**Given** the "regional hurricane + mild recession" scenario
**When** selected
**Then** loss under scenario, hazard exposure and insurance-gap counts are shown (FR-72)

### Story 24.3: Portfolio & risk chat with safe actions

As a risk manager,
I want to ask questions about the book and run safe actions,
So that analysis is quick.

**Acceptance Criteria:**

**Given** the request "lower the starter-card cut-off to grade 14"
**When** issued in chat
**Then** it creates a change request instead of acting, while "show watch-list growth by sector" runs directly with the query shown (FR-67, AD-13)

## Epic 25: UK Servicing: Persistent Debt, Overdrafts & Forbearance Rules [R4]

**Squad:** UK Pack. **Depends on:** Epics 7, 11.
**Goal:** CONC 6.7 persistent-debt engine, CONC 5D overdraft repeat use, and CONC 7 forbearance requirements.
**Must-ship:** 25.1, 25.2.

### Story 25.1: Persistent-debt monthly test

As a UK card risk manager,
I want the monthly 18-month test with the £200 exemption,
So that persistent debt is identified.

**Acceptance Criteria:**

**Given** an account where principal repaid < interest + fees over 18 months, and another whose balance fell below £200 in the period
**When** the monthly test runs
**Then** the first is flagged PD18 and the second is exempt (FR-59)

### Story 25.2: 27- and 36-month actions

As a UK card risk manager,
I want the PD27 review and PD36 repayment offer, with suspend/cancel if there is no response,
So that the rules are applied end to end.

**Acceptance Criteria:**

**Given** an account still in persistent debt at month 36
**When** processed
**Then** a repayment option within ~3–4 years is offered. With no response or refusal of sustainable options, a suspend/cancel action is recommended for human approval, and limit increases are blocked throughout (FR-59)

### Story 25.3: Overdraft repeat-use monitoring

As a UK overdraft manager,
I want repeat-use detection split into financial-difficulty and other categories, with communications cadence,
So that CONC 5D is met.

**Acceptance Criteria:**

**Given** repeat overdraft use
**When** monitored
**Then** the customer is classified and the communications schedule (first, second, then at least annual) is generated (FR-59)

### Story 25.4: CONC 7 forbearance requirements

As a UK collections lead,
I want forbearance options required for customers in or approaching arrears,
So that treatment is fair.

**Acceptance Criteria:**

**Given** a customer indicating they are approaching arrears
**When** assessed
**Then** forbearance options (interest freeze, deferral, token payment, arrangement) must be offered before escalation (FR-59)

## Epic 26: Collections Cure & Contact Strategy [R4]

**Squad:** Models & ML + AI/LLM. **Depends on:** Epics 5, 17, 25.
**Goal:** Cure prediction, forbearance recommendations, and contact strategy with guardrails.
**Must-ship:** 26.1, 26.2.

### Story 26.1: Cure prediction

As a collections manager,
I want delinquent customers ranked as self-cure, needs help or likely loss,
So that effort goes where it helps.

**Acceptance Criteria:**

**Given** the delinquent demo population
**When** scored
**Then** each customer gets a cure class with probability and reasons (FR-60)

### Story 26.2: Forbearance recommender

As a collections agent,
I want the best forbearance option per customer (UK CONC 7 and persistent debt; US hardship programmes),
So that recovery is sustainable.

**Acceptance Criteria:**

**Given** a UK card customer at PD27
**When** recommendations run
**Then** a plan repaying within ~3–4 years is proposed with an affordability check (FR-61)

### Story 26.3: Contact strategy with caps

As a collections manager,
I want channel, time and frequency rules,
So that contact is lawful and humane.

**Acceptance Criteria:**

**Given** the US default cap (7 calls in 7 days) and customer opt-outs
**When** the strategy is generated
**Then** no plan exceeds the cap, contacts outside allowed hours, or uses an opted-out channel. Vulnerable customers go to specialists first (FR-62)

### Story 26.4: AI contact drafts with tone guardrails

As a compliance officer,
I want AI-drafted messages checked for threats or misleading statements and approved by a human,
So that communications are safe.

**Acceptance Criteria:**

**Given** a draft containing threatening language from a fake LLM
**When** checked
**Then** it is rejected and the template is used, and every sent draft requires human approval (FR-62, AD-6)

## Epic 27: Auto Finance, UK Overdraft & UK BNPL Products [R4]

**Squad:** US Pack + UK Pack. **Depends on:** Epics 6, 7.
**Goal:** Auto finance in both markets, UK arranged/unarranged overdraft assessment and UK BNPL.
**Must-ship:** 27.1.

### Story 27.1: Auto finance

As an auto-finance underwriter,
I want US direct/indirect and UK motor assessments,
So that auto lending is covered.

**Acceptance Criteria:**

**Given** a UK motor application via a dealer
**When** assessed
**Then** the commission model, % of cost of credit and disclosure evidence are captured, discretionary commission arrangements are blocked, and high-commission flags (≥ 39% of cost of credit and ≥ 10% of loan) are raised (FR-22)

### Story 27.2: UK overdraft assessment

As a UK product manager,
I want overdraft limits assessed under CONC 5.2A, with the repeat-use link,
So that overdrafts are affordable.

**Acceptance Criteria:**

**Given** an arranged overdraft request
**When** assessed
**Then** two-limb affordability applies, and the account is enrolled in repeat-use monitoring (FR-22, FR-59)

### Story 27.3: UK BNPL

As a UK product manager,
I want BNPL (deferred payment credit) assessed with CONC 5.2A unmodified,
So that BNPL meets the July 2026 rules.

**Acceptance Criteria:**

**Given** a low-value BNPL purchase
**When** assessed
**Then** a proportionate but complete affordability assessment is recorded, and missed-payment information content is available (FR-22)

## Epic 28: Document AI, Credit Memos & Policy Copilot [R4]

**Squad:** AI/LLM. **Depends on:** Epics 2, 13, 17.
**Goal:** Document extraction for commercial credit, credit memo drafting, and a policy copilot that cites, checks and simulates.
**Must-ship:** 28.1, 28.3.

### Story 28.1: Financial statements and bank statements extraction

As a commercial analyst,
I want statements (including UK statutory accounts) and bank statements extracted with page links,
So that spreading is fast.

**Acceptance Criteria:**

**Given** a PDF set
**When** extracted
**Then** every figure links to its page, and nothing feeds a rating until a user confirms the spread (FR-68)

### Story 28.2: US tax returns and loan agreements

As a commercial analyst,
I want 1120/1065/K-1 extraction and covenant extraction from loan agreements,
So that small-business and covenant data is captured.

**Acceptance Criteria:**

**Given** a 1065 return and a loan agreement
**When** extracted
**Then** key lines and covenants (type, threshold, test date) are proposed for confirmation and then tracked (FR-68, FR-26)

### Story 28.3: Credit memo drafting

As a commercial analyst,
I want a credit memo drafted from confirmed data and computed results,
So that committee papers are faster.

**Acceptance Criteria:**

**Given** a rated company
**When** a memo is drafted
**Then** all numbers match computed facts (guardrail), and the memo is a draft until signed (FR-66, AD-6)

### Story 28.4: Policy copilot

As a policy owner,
I want policy documents read with citations, conflicts and gaps found, change alerts raised, and proposals simulated,
So that policy changes are safer.

**Acceptance Criteria:**

**Given** a policy manual and a pack update (e.g. a new year's QM thresholds)
**When** the copilot runs
**Then** draft rules cite pages, conflicts with the pack or other rules are listed, affected rules are alerted, and a proposed change runs through the frontier and fairness tests before becoming a change request (FR-66, AD-13)

## Epic 29: Income Segmentation & Segment Policy [R1]

**Squad:** US Pack + UK Pack (policy), Models & ML (calibration, views). **Depends on:** Epics 2, 3, 5.
**Goal:** Every customer is placed in an income segment (S0–S5) with overlay tags, and the segment's policy (products, caps, DTI, residual floors, automation) is applied in the decision. Spec: `income-segmentation-spec.md`.
**Must-ship:** 29.1, 29.3, 29.4. Stories 29.6–29.8 extend Epics 9, 22, 23 and 24 in later releases; 29.5 is R2; 29.7–29.8 are R3.

### Story 29.1: Segment assignment from verified income

As an underwriter,
I want each applicant placed in an income segment from verified gross income,
So that the right products and limits apply.

**Acceptance Criteria:**

**Given** US bands (<$30k, $30–60k, $60–120k, $120–250k, $250k+) and UK bands (<£20k, £20–35k, £35–60k, £60–100k, £100k+) as effective-dated policy data
**When** an applicant with verified income is assessed
**Then** the segment is S1–S5 by band, S0 if no verified income, irregular income uses the smoothed 12-month verified average, joint applicants combine income, and self-declared income alone never sets the segment (FR-79)
**And** boundary tests pass: $29,999 → S1, $30,000 → S2, £20,000 → S2, £100,000 → S5

### Story 29.2: Overlay tags

As a credit officer,
I want overlay tags shown on each case,
So that I understand why the assessment path differs.

**Acceptance Criteria:**

**Given** an applicant aged 19 with 1 tradeline and 40% platform income
**When** tags are computed
**Then** `GENZ`, `THIN_FILE` and `GIG_SELF_EMPLOYED` are set with their effects (starter caps, smoothed income with volatility penalty), and no immigration-status feature is used without legal review (FR-80)

### Story 29.3: Segment policy matrix as policy data

As a policy owner,
I want the segment matrix (products, card ranges, loan caps, max DTI, residual floors, salary-advance caps, UK LTI, automation rule, review cadence) as maker-checker policy data,
So that the bank can tune it safely.

**Acceptance Criteria:**

**Given** the demo matrix from the spec
**When** a policy admin edits a value
**Then** a change request is created, the checker must differ from the maker, tighten-only validation against the pack runs, and the new version is effective-dated (FR-81, AD-13, AD-2)

### Story 29.4: Segment-aware decision and golden tests

As a QA engineer,
I want the decision to apply the segment in the agreed order,
So that results are consistent and explainable.

**Acceptance Criteria:**

**Given** Maria (≈$48k → S2, `THIN_FILE`, `GIG_SELF_EMPLOYED`) applying for $5,000
**When** assessed
**Then** the limit is $1,500 (starter cap binds over the S2 range $1,500–5,000), card residual $560 − $45 = $515 ≥ $300 floor passes, and the case routes to a human because $1,500 > $1,000 (FR-82)
**And** Tom (≈£24k → S2, `GENZ`, `THIN_FILE`) for £1,000: residual £495 − £42.40 = £453 ≥ £100, grade 12, auto-approved with Art 22C information
**And** a US S3 applicant ($90k gross, $5,600 net, obligations $1,900, essentials $1,800) asking $30,000 over 60 months at 12%: instalment ≈ $667, DTI ≈ 34% ≤ 43%, residual $1,233 ≥ $1,200 → pass, binding constraint "minimum residual income"
**And** declines are never automated in any segment (AD-7)

### Story 29.5: Nightly re-segmentation

As a risk analyst,
I want segments rechecked nightly with stability rules,
So that one bad month doesn't drop a customer's segment.

**Acceptance Criteria:**

**Given** verified income history
**When** the nightly run executes
**Then** a customer moves up after 2 consecutive qualifying months and down after 3 (immediately on verified job loss), every change is logged, and limit decreases raise change-in-terms (US) / CONC notice tasks (UK) (FR-83)

### Story 29.6: Segment-level calibration and monitoring

As a model validator,
I want PD calibration, approvals, limits, APR and losses reported by segment,
So that the model is accurate within every band.

**Acceptance Criteria:**

**Given** a model build
**When** validation runs
**Then** calibration tables by segment are produced, a segment with predicted-vs-actual gap above tolerance fails the build, and income band alone carries no scoring penalty (FR-84)

### Story 29.7: Fairness and fair value by segment

As a fair-lending officer,
I want outcomes reported by segment × protected-group proxy,
So that income bands don't hide unfair treatment.

**Acceptance Criteria:**

**Given** the fairness zone and segment outcomes
**When** the fairness suite runs
**Then** approval rate, average limit, APR and decline reasons are reported by segment × proxy group with a business-justification record, the UK fair-value check runs per segment, and no income-only knockout exists other than S0 eligibility and regulatory minimums (FR-85, AD-9)

### Story 29.8: Segment views and segment-aware stress

As a CRO,
I want customers and balances by segment (pie/donut), default and approval rates, limit ranges, and stress EL uplift by segment,
So that I see where risk and opportunity sit.

**Acceptance Criteria:**

**Given** the demo banks
**When** the segment dashboard opens
**Then** pies show customers % and balances % by S0–S5 per market in fixed segment colours, bars show default rate and champion-vs-challenger approval rate, and the stress view shows EL uplift for recession, rate shock +3pp and market crash by segment (FR-86)
