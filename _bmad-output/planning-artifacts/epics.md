---
status: final
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/product-brief.md
  - _bmad-output/planning-artifacts/discovery-answers.md
  - docs/regulatory/cbuae-rules.md
---

# AI Risk Score Card - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for AI Risk Score Card, decomposing the requirements from the PRD
(FR-1..FR-66, NFR-1..NFR-12), the derived UX requirements and the Architecture spine (AD-1..AD-16) into implementable stories.

- Epics are ordered by release: **R1 Demo MVP** (Epics 1–5), **R2 Pilot** (Epics 6–14), **R3 Full v1** (Epics 15–20).
- Every epic names its **squad focus** (Platform, Decision Core, Data & Integrations, ML & Analytics, Frontend, AI/LLM, or Delivery & Compliance) and depends only on **earlier** epics.
- Each story is sized for one developer within a 2-week sprint. Acceptance criteria cite FR / NFR / AD ids and are testable.
- Vocabulary follows the PRD Glossary exactly (finance application, finance amount, profit rate, obligor, risk grade, recommendation, deviation). The words "loan" and "interest" are never used in code or UI (AD-12).
- **Agreed defaults** used in the ACs (all Tenant-configurable):
  - Grades 1–10 with PD bands: 1 <0.25%, 2 0.25–0.5%, 3 0.5–1%, 4 1–2%, 5 2–3.5%, 6 3.5–5%, 7 5–8%, 8 8–12%, 9 12–20%, 10 ≥20%. Model escalation to Refer at grade ≥7.
  - DBR Income = basic + housing. Card obligation = 5% of limit. Profit-rate stress add-on = 0.
  - Demo age limits: minimum 21; maximum at maturity 65 (expat) / 70 (UAE national).
  - EOSB-backed finance: ≥5 years' service, up to 80% of accrued EOSB. Total Unsecured Cap = 20× monthly income.
  - Corporate dimension weights 35/20/15/10/20, with an EBITDA −30% stress.
  - ML activation gate: ≥1,000 rows, ≥50 defaults, out-of-time Gini ≥0.30. Drift threshold: PSI >0.25.
  - Performance: NFR-1 p95 ≤2 s; NFR-2 nightly run of 100k + 5k ≤2 h.

**Golden worked example (acceptance anchor, used in Stories 4.9 and 5.7):**

| Input | Value |
|---|---|
| Customer | Expat government employee |
| Gross monthly income | AED 25,000 |
| DBR Income (basic + housing) | AED 18,000 |
| Existing obligations | AED 3,000/month auto Murabaha + card limit AED 20,000 (5% = AED 1,000) |
| Request | Tawarruq personal finance, AED 400,000, 48 months, 6% profit rate |

| Expected result | Value |
|---|---|
| Instalment at the requested amount | ≈ AED 9,394 |
| DBR at the requested amount | ≈ 74.4% → fails the 50% cap |
| CBUAE 20× cap | AED 500,000 → passes |
| Total Unsecured headroom | AED 480,000 |
| DBR-headroom finance amount | ≈ AED 212,902 |
| **Recommended Limit** | **AED 212,000**, Binding Constraint = DBR |
| Instalment at the Recommended Limit | ≈ AED 4,979 |
| DBR at the Recommended Limit | ≈ 49.9% |

## Requirements Inventory

### Functional Requirements

- FR-1: Tenant isolation [R1]
- FR-2: CBUAE Layer (sourced, versioned regulator pack with confidence levels) [R1]
- FR-3: Tighten-only validation against CBUAE [R1]
- FR-4: Policy import from Excel parameter sheet [R1]
- FR-5: Policy extraction from PDF/Word manuals into Draft Rules (LLM) [R2]
- FR-6: Maker-checker & immutable Policy Versions [R1]
- FR-7: Data Field Template generated from the active policy [R2]
- FR-8: Demo Bank Policy & Credit Policy with discovery defaults [R1]
- FR-9: Employer classification (starter UAE list + Tenant override) [R1]
- FR-10: Restricted lists (nationality → Refer, restricted sectors, Sharia-prohibited sectors → Decline) [R1]
- FR-11: Real-time finance application API [R2]
- FR-12: Temenos T24/Transact connector [R2]
- FR-13: Read-only database connector for Book & history [R2]
- FR-14: Demo data source (synthetic T24-like DB) [R1]
- FR-15: Behavioural data ingestion (raw transactions with MCC or monthly aggregates) [R2]
- FR-16: AECB data (stored data R2; optional direct API R3) [R2/R3]
- FR-17: PII masking (pseudonymisation, audited reveal) [R1]
- FR-18: Data-quality checks [R1]
- FR-19: Retail feature derivation (age, service, EOSB, DBR, annuity, behaviour) [R1]
- FR-20: Product rules (personal finance & card R1; auto Murabaha & Ijara home finance R2) [R1/R2]
- FR-21: Customer types (self-employed, retirees, non-residents, low-salary) [R2]
- FR-22: Joint applicants & guarantors [R2]
- FR-23: Islamic product-structure checks & charity treatment of late amounts [R2]
- FR-24: Corporate features & five-dimension rating [R2]
- FR-25: Corporate knockouts (combination rule, Sharia-prohibited, restricted sectors) [R2]
- FR-26: Stressed facility sizing + collateral capacity [R2]
- FR-27: Group aggregation & CBUAE large-exposure limits [R2]
- FR-28: Document AI for PDF financial statements [R2]
- FR-29: Sole proprietors assessed under retail rules [R2]
- FR-30: Scorecard (expert defaults R1; bank scorecard import & data refinement R2) [R1/R2]
- FR-31: Learning Model (gradient boosting, exclusions, contributions, blend) [R2]
- FR-32: Risk Grades 1–10 on the Tenant scale [R1]
- FR-33: Policy-first Recommendation with model escalation [R1]
- FR-34: Grade-based Deviations [R2]
- FR-35: Recommended Limit with Binding Constraint [R1]
- FR-36: Risk-based Profit Rate suggestion [R3]
- FR-37: Approval Authority routing & queues [R2]
- FR-38: Overrides with reasons, reports (R2); learning from overrides (R3) [R2/R3]
- FR-39: Authentication & roles (local accounts R1; AD/SSO R2) [R1/R2]
- FR-40: Explanations EN/AR (templates R1; LLM R2) [R1/R2]
- FR-41: Number & rule guardrail on LLM output [R2]
- FR-42: Credit Memo / credit paper drafting with sign-off [R2]
- FR-43: Internal-only AI text [R1]
- FR-44: Nightly Run (basic re-score R2; full pack R3) [R2/R3]
- FR-45: Risk ranking of the Book [R1]
- FR-46: Opportunity Finder [R3]
- FR-47: Early-warning Watch-list [R3]
- FR-48: Lifestyle Mismatch detection [R3]
- FR-49: Profession & industry decline signals [R3]
- FR-50: De-risking Recommendations [R3]
- FR-51: Pre-approved Offers & card limit increases [R3]
- FR-52: Concentrations & hidden links [R3]
- FR-53: Stress tests [R3]
- FR-54: What-if Simulator [R3]
- FR-55: KPI & ROI Dashboard [R3]
- FR-56: Portfolio Assistant (Safe Actions only) [R3]
- FR-57: Model training & activation gate [R2]
- FR-58: Drift monitoring, auto-retrain, auto-suspend [R2]
- FR-59: Validation & model documentation packs [R2]
- FR-60: Fairness report [R2]
- FR-61: Decision Record & exact replay [R1]
- FR-62: Retention [R1]
- FR-63: Installation & signed updates (Docker R1; Windows installer R2) [R1/R2]
- FR-64: Offline licence [R2]
- FR-65: Agentic annual review (basic) [R3]
- FR-66: Demo Tenant "Demo Islamic Bank" [R1]

### NonFunctional Requirements

- NFR-1: Real-time assessment p95 ≤ 2 s, p99 ≤ 5 s at 20 concurrent requests (no LLM text); LLM Explanation ≤ 20 s async.
- NFR-2: Nightly Run of 100k Customers + 5k Obligors ≤ 2 h (excluding LLM narratives).
- NFR-3: No customer data leaves the Tenant infrastructure at runtime (only the optional AECB API); egress deny-by-default.
- NFR-4: Encryption at rest + TLS, PII masking, RBAC on every endpoint, secrets in a vault/keystore, OWASP ASVS L2, security tests in CI.
- NFR-5: Every write action and decision audit-logged (append-only).
- NFR-6: Determinism: same inputs + Policy Version + model version → identical outputs.
- NFR-7: Availability ≥ 99.5% in business hours; graceful degradation (model → Scorecard, LLM → templates, nightly failure → last results).
- NFR-8: Localisation: UI English; Explanations, memos and assistant answers English + Arabic (RTL documents).
- NFR-9: Pluggable regulator packs (CBUAE first; QCB, SAMA later) without code changes.
- NFR-10: WCAG 2.1 AA web UI.
- NFR-11: Reference hardware (16+ cores, 64 GB RAM, GPU ≥ 24 GB for LLM); CPU-only mode without LLM features.
- NFR-12: Observability (health endpoints, structured logs, job metrics), no external telemetry.

### Additional Requirements

From the architecture spine:
- AD-1: Pure, deterministic decision core: `assess(snapshot, policy_version, model_version, params)`, with no I/O, clock, network or LLM.
- AD-2: Tenant isolation through one DB schema per Tenant (`t_<tenant_code>`) plus a shared `platform` schema.
- AD-3: Policy as data. JSON/YAML Rules are evaluated by an allow-listed AST evaluator; Policy Versions are immutable; tighten-only runs on publish; the regulator pack is a signed artifact.
- AD-4: One feature pipeline from the Canonical Data Model (CDM) for training, real-time and nightly.
- AD-5: Ports for every external system. Source adapters are read-only; the demo adapter implements the same ports.
- AD-6: The LLM is an advisory side-channel: facts JSON only, guardrail, async, drafts only.
- AD-7: One generic ChangeRequest (maker-checker). Checker ≠ maker is enforced in the service layer and by a DB constraint.
- AD-8: Model registry (hash, model card, data hash); one active model per Tenant and segment; suspension falls back to the Scorecard.
- AD-9: Append-only, hash-chained `decision_record` and `audit_event`. The app role has no UPDATE/DELETE.
- AD-10: PII pseudonymised at ingestion into `pii_vault`. No PII in logs or LLM prompts.
- AD-11: Deny-by-default egress allow-list. No CDNs at runtime.
- AD-12: Glossary-exact Islamic vocabulary. "loan" and "interest" are banned in identifiers and UI strings (lint).
- AD-13: SQLAlchemy 2 + Alembic. PostgreSQL by default, SQL Server supported (Oracle in R3). No vendor SQL outside dialect modules.
- AD-14: REST `/api/v1`, committed OpenAPI, generated TS client, standard error envelope, declared permissions per endpoint.
- AD-15: Async work through Celery + Redis. Idempotent tasks keyed by `(tenant, job_type, input_hash)`.
- AD-16: Signed release bundles (Ed25519) and an offline signed licence. An expired licence switches to read-only mode.

Starter and source structure come from the architecture "Structural Seed": `backend/app/{shared,core,ports,adapters,services,api,worker}`, plus `regulatory/`, `tenants/`, `synth/`, `migrations/`, `frontend/`, `deploy/`, `docs/`, `e2e/` and `perf/`.

Compliance and commercial deliverables (from PRD §8 and discovery):
- Onboarding packs: security, UAE PDPL, CBUAE outsourcing/third-party, Sharia compliance note.
- Model documentation and validation templates.
- NDA/DPA templates, support SLA definition, training materials, user and admin guides.
- Pilot parallel-run playbook.

### UX Design Requirements

- UX-DR1: **Decision Screen** (UJ-1): summary card with Grade (1–10 on the Tenant scale), PD, Recommendation, Recommended Limit and Binding Constraint, top-3 drivers and the Explanation (EN/AR toggle).
- UX-DR2: **Drill-down** on the Decision Screen: DBR arithmetic, every Rule result with layer, severity, source and confidence badge, and a limit waterfall showing each cap and the binding one.
- UX-DR3: **Approval Queue** (UJ-2): cases filtered to the user's authority, sorted by risk, Deviation flags, and approve / return-with-comment / escalate actions.
- UX-DR4: **Portfolio & Early-warning Dashboard** (UJ-3): risk ranking, Watch-list, Lifestyle Mismatch alerts, De-risking queue, concentrations, data "as of" date.
- UX-DR5: **KPI & ROI Dashboard** (UJ-7): approval rate, grade mix, defaults by vintage, override rate, opportunity value, income uplift in AED.
- UX-DR6: **Policy Viewer** (UJ-5): the three Policy Layers side by side, sources, "to verify" badges for confidence below H, tighten-only status, Policy Version history, ChangeRequest inbox.
- UX-DR7: **Model Lab**: model cards, gate results, drift and PSI charts, activate/suspend through a ChangeRequest.
- UX-DR8: **Demo banner**: a persistent "DEMO DATA" banner on Demo Tenant screens and reports.
- UX-DR9: **Bilingual outputs**: Explanations, memos and assistant answers rendered in English and Arabic (RTL) in the UI and in PDF.
- UX-DR10: **Decision-support disclaimer** on every decision screen and report: "AI recommends, scores, drafts and flags; bank staff decide and are accountable."
- UX-DR11: **What-if Simulator** (UJ-4): clone a policy, edit parameters, view deltas (approvals, expected loss, income), submit as a ChangeRequest.
- UX-DR12: **Accessibility**: WCAG 2.1 AA across all screens (NFR-10).

### FR Coverage Map

| FR | Epic.Story |
|---|---|
| FR-1 | 1.3, 1.7 |
| FR-2 | 2.3 |
| FR-3 | 2.4 |
| FR-4 | 2.6 |
| FR-5 | 10.4, 10.5 |
| FR-6 | 2.5, 2.10 |
| FR-7 | 7.6 |
| FR-8 | 2.7 |
| FR-9 | 2.8 |
| FR-10 | 2.9 |
| FR-11 | 7.1, 7.7 |
| FR-12 | 7.2 |
| FR-13 | 7.3 |
| FR-14 | 3.1, 3.2, 3.3 |
| FR-15 | 7.4 |
| FR-16 | 7.5 (stored), 20.3 (API) |
| FR-17 | 3.4 |
| FR-18 | 3.5 |
| FR-19 | 4.1, 4.2, 4.3, 4.4 |
| FR-20 | 4.5 (personal finance, card), 8.1 (auto), 8.2 (Ijara) |
| FR-21 | 8.3, 8.4 |
| FR-22 | 8.5 |
| FR-23 | 8.6 |
| FR-24 | 9.1, 9.2 |
| FR-25 | 9.3 |
| FR-26 | 9.4 |
| FR-27 | 9.5 |
| FR-28 | 10.2, 10.3 |
| FR-29 | 9.6 |
| FR-30 | 4.6, 11.8 |
| FR-31 | 11.1, 11.2, 11.4 |
| FR-32 | 4.7 |
| FR-33 | 4.8 |
| FR-34 | 6.4 |
| FR-35 | 4.9 |
| FR-36 | 16.4 |
| FR-37 | 6.3, 6.5, 6.7 |
| FR-38 | 6.6 (record, report), 20.2 (learning) |
| FR-39 | 1.4 (local), 6.1, 6.2 (AD/SSO, roles) |
| FR-40 | 5.2 (templates), 12.2 (LLM) |
| FR-41 | 12.1 |
| FR-42 | 12.3, 12.4 |
| FR-43 | 5.1, 12.2 |
| FR-44 | 13.1, 13.2 (basic), 15.1 (full pack) |
| FR-45 | 5.5 |
| FR-46 | 16.1, 16.2 |
| FR-47 | 15.2 |
| FR-48 | 15.3 |
| FR-49 | 15.4 |
| FR-50 | 15.5 |
| FR-51 | 16.3 |
| FR-52 | 17.1, 17.2 |
| FR-53 | 17.3, 17.4 |
| FR-54 | 18.1, 18.2 |
| FR-55 | 18.3, 18.4 |
| FR-56 | 19.1, 19.2, 19.3 |
| FR-57 | 11.3, 11.9 |
| FR-58 | 11.5 |
| FR-59 | 11.6, 14.5 |
| FR-60 | 11.7 |
| FR-61 | 1.5, 4.10 |
| FR-62 | 1.5 |
| FR-63 | 1.2 (Docker), 13.3, 13.4 (signed updates, Windows) |
| FR-64 | 13.5 |
| FR-65 | 20.1 |
| FR-66 | 1.7, 3.6, 3.7, 9.7 |

Coverage check: FR-1..FR-66 are all mapped, with no orphans.

## Epics List

| # | Epic | Release | Squad focus | Depends on |
|---|---|---|---|---|
| 1 | Platform Foundation & Demo Tenant Shell | R1 | Platform | — |
| 2 | Policy Engine & CBUAE Layer | R1 | Decision Core | 1 |
| 3 | Synthetic Data & Demo Data Source | R1 | Data & Integrations | 1 |
| 4 | Retail Assessment & Recommendation Core | R1 | Decision Core | 1, 2, 3 |
| 5 | Officer Decision Screen & Risk Ranking | R1 | Frontend | 1–4 |
| 6 | Enterprise Access & Approval Workflow | R2 | Platform + Frontend | 1, 2, 4, 5 |
| 7 | Bank Integration: T24 & Data Warehouse | R2 | Data & Integrations | 1, 2, 3, 4 |
| 8 | Islamic Product Coverage & Retail Customer Types | R2 | Decision Core | 2, 4 |
| 9 | Corporate & SME Assessment | R2 | Decision Core | 2, 3, 4 |
| 10 | Document AI & Policy Extraction | R2 | AI/LLM | 2, 9 |
| 11 | Learning Model & Model Governance | R2 | ML & Analytics | 2, 3, 4 |
| 12 | AI Explanations & Credit Memos | R2 | AI/LLM | 4, 5, 10 |
| 13 | Pilot Operations: Nightly Run, Packaging, Licensing & Security | R2 | Platform | 1–4, 7 |
| 14 | Bank Onboarding & Commercial Readiness Pack | R2 | Delivery & Compliance | 1–13 (documents describe built features) |
| 15 | Early Warning & Behavioural Risk Signals | R3 | ML & Analytics | 4, 7, 11, 13 |
| 16 | Growth: Opportunity Finder, Pre-approved Offers & Pricing | R3 | ML & Analytics + Frontend | 4, 11, 13, 15 |
| 17 | Portfolio Concentrations & Stress Tests | R3 | ML & Analytics | 4, 9, 13, 15 |
| 18 | What-if Simulator & KPI/ROI Dashboard | R3 | Decision Core + Frontend | 2, 4, 13, 16 |
| 19 | Portfolio Assistant | R3 | AI/LLM | 12, 15–18 |
| 20 | Agentic Annual Review & Advanced Integrations | R3 | AI/LLM + Data & Integrations | 6, 7, 9, 10, 11, 12 |

---

## Epic 1: Platform Foundation & Demo Tenant Shell [R1]

**Squad:** Platform. **Depends on:** none.
Goal: a running, secured, multi-tenant application shell (API, worker, DB, web) that can be deployed with Docker Compose and shows a "Demo Islamic Bank" tenant to a logged-in user, with audit and the CDM in place for all later epics.

### Story 1.1: Repository skeleton and CI pipeline

As a developer,
I want the repository structured per the architecture seed with CI running lint, types, tests and security scans,
So that every squad builds on the same conventions from day one.

**Acceptance Criteria:**

**Given** a fresh clone
**When** CI runs on a pull request
**Then** ruff, mypy, pytest (backend), ESLint/TypeScript checks and unit tests (frontend), Bandit and dependency audit all run, and the PR is blocked on failure
**And** the tree matches the architecture seed (`backend/app/{shared,core,ports,adapters,services,api,worker}`, `frontend/`, `deploy/`, `docs/`, `e2e/`, `perf/`)
**And** a vocabulary lint fails the build if "loan" or "interest" appear in identifiers or UI strings (AD-12)
**And** an import-boundary check fails the build if `app/core` imports from `adapters`, `services`, `api` or any I/O library (AD-1)

### Story 1.2: Docker Compose stack

As a platform engineer,
I want a Docker Compose deployment of api, worker, PostgreSQL, Redis and nginx-served web,
So that the product can be installed on one server inside a bank (FR-63 R1).

**Acceptance Criteria:**

**Given** a host with Docker
**When** `docker compose up` is run with the sample env file
**Then** all services become healthy and `/api/v1/health` returns 200 (NFR-12)
**And** no container pulls assets from the internet at runtime; front-end assets are bundled (AD-11)
**And** secrets are read from env/secret files, never committed (NFR-4)

### Story 1.3: Schema-per-tenant tenancy

As a sys admin,
I want to create Tenants that each get their own database schema,
So that bank data is strictly isolated (FR-1, AD-2).

**Acceptance Criteria:**

**Given** two Tenants A and B created through the admin API
**When** a user bound to Tenant A queries any endpoint
**Then** only rows from schema `t_a` are returned. An integration test proves Tenant B data is unreachable
**And** Alembic migrations apply to `platform` and to every tenant schema
**And** a test scans the code for schema-qualified SQL outside the tenancy module and fails if found

### Story 1.4: Local accounts and RBAC framework

As a sys admin,
I want local user accounts with roles and `resource:action` permissions on every endpoint,
So that the demo can be used safely before AD/SSO is available (FR-39 R1, AD-14).

**Acceptance Criteria:**

**Given** the standard role set (RM, Credit Officer, Approver L1–Ln, Risk Manager, CRO, Policy Admin, Model Validator, Auditor, Sys Admin)
**When** a user calls an endpoint without the declared permission
**Then** the API returns 403 with the standard error envelope
**And** an automated test asserts that every registered route declares a permission
**And** passwords are stored with a modern hash (argon2/bcrypt)

### Story 1.5: Append-only, hash-chained audit and retention settings

As an auditor,
I want every write action recorded in an append-only, hash-chained log,
So that history cannot be silently altered (NFR-5, AD-9, FR-61 foundation, FR-62).

**Acceptance Criteria:**

**Given** any create/update/delete through the services layer
**When** it completes
**Then** an `audit_event` row stores user, tenant, time, action, before/after, `prev_hash` and `row_hash`
**And** the application DB role has no UPDATE/DELETE privilege on `audit_event` and `decision_record` (test attempts and fails)
**And** a chain-verification command detects a tampered row
**And** the Tenant retention setting defaults to "keep everything", and no purge job exists unless the Tenant configures one (FR-62)

### Story 1.6: Canonical Data Model and shared kernel

As a developer,
I want a CDM and shared value types (money in fils, UUIDv7 ids, UTC dates, typed errors),
So that adapters and features exchange data consistently (AD-4, conventions).

**Acceptance Criteria:**

**Given** the CDM Pydantic models (Customer, Obligor, FinanceApplication, Obligation, SalaryCredit, Transaction, CasaBalance, BureauRecord, Collateral, FinancialStatement)
**When** they are serialised and parsed
**Then** round-trips are lossless, and money is integer minor units with an ISO currency (unit tests)
**And** field names use Glossary terms (`finance_amount`, `profit_rate`, `obligor`)

### Story 1.7: Web app shell with tenant context and demo banner

As a bank user,
I want to log in and land in my Tenant's workspace, with a clear banner when it is the demo,
So that I always know whose data I am looking at (FR-1, FR-66, UX-DR8, UX-DR10).

**Acceptance Criteria:**

**Given** a user of the Demo Tenant (flag `demo=true`)
**When** they log in
**Then** every page shows a persistent "DEMO DATA" banner and the decision-support disclaimer footer
**And** the navigation shows only the features the user's role permits
**And** the shell passes automated WCAG 2.1 AA checks (axe) on the login and home pages (NFR-10)

## Epic 2: Policy Engine & CBUAE Layer [R1]

**Squad:** Decision Core. **Depends on:** Epic 1.
Goal: the three Policy Layers exist as safe, versioned, maker-checker-controlled data. The CBUAE pack is loaded with sources and confidence, and the demo bank policies are publishable and viewable.

### Story 2.1: Safe expression evaluator

As a policy admin,
I want rule conditions evaluated by a restricted evaluator,
So that policies can be edited as data without code-injection risk (AD-3).

**Acceptance Criteria:**

**Given** conditions using comparisons, arithmetic, `and/or/not`, `in` and whitelisted functions (`min`, `max`, `abs`, `round`)
**When** they are evaluated against a feature dict
**Then** results match the expected values in a table-driven unit test suite
**And** malicious inputs (`__import__('os')`, attribute access `x.__class__`, lambdas, comprehensions, subscripts on dunder names, very long or deeply nested expressions) are rejected with `UnsafeExpression` without execution
**And** an unknown feature name raises `UnknownFeature` naming the field

### Story 2.2: Rule schema and rule engine

As the decision core,
I want to evaluate every applicable Rule for a case and return structured results,
So that Recommendations can cite exactly which rules passed or failed (AD-3, FR-33 foundation).

**Acceptance Criteria:**

**Given** Rules validated against `policy-rule.schema.json` (id `LAYER.SEGMENT.NNN`, layer, applies_to, condition, severity, source, confidence, direction?)
**When** the engine runs for a case
**Then** it returns `{rule_id, layer, passed, severity, message, source, confidence}` for every Rule whose `applies_to` matches the segment, product, nationality group and employment type
**And** Rules not applicable are listed as `skipped` with the reason
**And** the engine is pure: no I/O, no clock (import-boundary test, AD-1)

### Story 2.3: CBUAE regulator pack v1

As a risk manager,
I want the CBUAE Layer delivered as a sourced, versioned pack,
So that regulatory limits are applied consistently and transparently (FR-2, NFR-9).

**Acceptance Criteria:**

**Given** `regulatory/cbuae/` built from `docs/regulatory/cbuae-rules.md`
**When** the pack loads
**Then** it contains at least:
- personal finance ≤ 20× monthly income and ≤ 48 months
- DBR ≤ 50%, retirees ≤ 30%
- card minimum income (confidence M, flagged "to verify")
- auto Murabaha ≤ 80% LTV / 60 months
- the Ijara LTV table, 25-year tenor, no EOSB as a repayment source
- large-exposure limits as % of Tier 1
- each Rule with source, section, URL and confidence H/M/L/UNCONFIRMED
**And** the pack has a version and verification date and is loaded by a generic loader (adding another regulator is data only)
**And** Rules with confidence below H carry `needs_verification=true`

### Story 2.4: Tighten-only validator

As a policy admin,
I want publication blocked when a bank value is looser than CBUAE,
So that the bank can never breach regulation through configuration (FR-3).

**Acceptance Criteria:**

**Given** a Bank Policy setting DBR max = 55% while CBUAE max = 50% (direction `max`)
**When** publication is attempted
**Then** it is blocked with a message naming the Rule id, the bank value and the CBUAE value
**And** unit tests cover `max` and `min` directions, equal values (allowed) and stricter values (allowed)
**And** CBUAE Rules can never be marked deviable

### Story 2.5: ChangeRequest (maker-checker) and Policy Versions

As a CRO,
I want every policy change to need a second person's approval and to create an immutable version,
So that policy changes are controlled and every decision is traceable to a version (FR-6, AD-7).

**Acceptance Criteria:**

**Given** a maker submits a ChangeRequest of type `policy` with a diff
**When** the same user tries to approve it
**Then** the service rejects it, and a DB check constraint (`checker_id <> maker_id`) also rejects a direct insert (test)
**And** on approval by another user with checker rights, a new immutable Policy Version is published (tighten-only must pass)
**And** previous Policy Versions remain readable, and any attempt to modify a published version fails

### Story 2.6: Excel parameter-sheet import

As a policy admin,
I want to import the bank's Excel parameter sheet into Rules and parameters,
So that the bank's policy is loaded directly, not retyped (FR-4).

**Acceptance Criteria:**

**Given** an .xlsx sheet with columns parameter, segment, product, value, unit, source
**When** it is imported
**Then** mapped rows become a draft ChangeRequest, and unmapped rows are listed for manual mapping with nothing silently dropped
**And** invalid values (type or unit errors) are reported per row

### Story 2.7: Demo Islamic Bank policy versions

As a salesperson,
I want the Demo Tenant to have a realistic, clearly labelled demo Bank Policy and Credit Policy,
So that the demo shows real-looking decisions (FR-8).

**Acceptance Criteria:**

**Given** the demo policy files under `tenants/demo_islamic_bank/`
**When** they are published through a ChangeRequest
**Then** they encode:
- salary-transfer requirement
- employer categories with caps
- age minimum 21; maximum at maturity 65 (expat) / 70 (national)
- restricted-nationality → Refer
- EOSB-backed finance ≥ 5 years' service, up to 80% of accrued EOSB
- low-salary threshold and caps
- Total Unsecured Cap 20×
- card obligation 5% of limit
- profit-rate stress add-on 0
- grade bands 1–10 and escalation grade 7
- an empty corporate threshold section
**And** every rule carries `demo=true` and the source "Demo policy (discovery defaults)"
**And** tighten-only passes

### Story 2.8: Employer classification

As a credit officer,
I want each employer mapped to a category from the bank's list or the starter list,
So that the right caps apply (FR-9).

**Acceptance Criteria:**

**Given** a starter UAE employer list and a Tenant override list
**When** an employer is classified
**Then** the Tenant entry wins, the starter list is used otherwise, and unknown employers default to `private_other` with a flag
**And** the lists are editable only through a ChangeRequest

### Story 2.9: Restricted and Sharia-prohibited lists

As a risk manager,
I want restricted nationalities, restricted sectors and Sharia-prohibited sectors maintained per Tenant,
So that restrictions are explicit and auditable (FR-10).

**Acceptance Criteria:**

**Given** a Customer on the restricted-nationality list
**When** assessed
**Then** the result includes a failed `refer` Rule (never a model feature)
**And** an obligor in a Sharia-prohibited sector gets a failed `knockout` Rule (Decline)
**And** each restriction is stored with an id, so later opportunity analysis can attribute blocked value to it

### Story 2.10: Policy Viewer screen

As a policy admin,
I want to see the three layers side by side with sources, confidence and validation status,
So that I can review and govern the policy (UX-DR6, FR-6).

**Acceptance Criteria:**

**Given** a Tenant with a published Policy Version
**When** the Policy Viewer opens
**Then** CBUAE, Bank Policy and Credit Policy Rules are shown with id, condition, severity, source and a "to verify" badge for confidence below H
**And** the tighten-only status and the Policy Version history are shown, and pending ChangeRequests appear in an inbox with approve/reject for checkers

## Epic 3: Synthetic Data & Demo Data Source [R1]

**Squad:** Data & Integrations. **Depends on:** Epic 1.
Goal: a realistic synthetic Islamic-bank dataset behind a T24-like demo database, read through the same ports as production, with PII protection and data-quality checks.

### Story 3.1: Synthetic retail data generator

As a data scientist,
I want a generator for a realistic UAE retail Book with a known latent risk function,
So that scoring quality can be measured against the truth (FR-14).

**Acceptance Criteria:**

**Given** `python -m synth retail --n 20000 --seed 42`
**When** it runs
**Then** it produces Customers (nationals and expats, employer categories, AED salaries split into basic, housing and other), obligations, card limits, salary credits, raw transactions with MCC, CASA balances, bureau scores (300–900), DPD history, finance applications including rejected ones, and a 12-month default flag at a 3–6% rate
**And** the same seed gives identical output (determinism test)
**And** the latent risk function is saved so ranking AUC can be computed later

### Story 3.2: Demo T24-like database and loader

As a platform engineer,
I want the synthetic data loaded into a bundled database with T24-like tables and warehouse views,
So that the demo exercises the same integration path as production (FR-14).

**Acceptance Criteria:**

**Given** the generator output
**When** the loader runs
**Then** a `demo_source` database contains T24-like customer, account, arrangement, transaction and application tables, plus read-only views mirroring the production view contract
**And** loading 20k Customers completes in under 5 minutes on the reference server

### Story 3.3: Demo source adapter

As the services layer,
I want `ApplicationSource` and `BookSource` ports implemented for the demo database,
So that later T24/SQL adapters plug in without changing core code (AD-5).

**Acceptance Criteria:**

**Given** the port interfaces in `app/ports`
**When** the demo adapter fetches an application or the Book
**Then** it returns CDM objects only (contract tests shared with future adapters)
**And** it uses a read-only connection; any write method is absent, and an attempted write via a raw connection fails (test)

### Story 3.4: PII pseudonymisation and audited reveal

As a compliance officer,
I want direct identifiers pseudonymised at ingestion,
So that names and Emirates IDs never spread across the system (FR-17, AD-10).

**Acceptance Criteria:**

**Given** source records with name, Emirates ID, passport and phone
**When** ingested
**Then** they are stored encrypted in `pii_vault`, and only `customer_key` flows onwards. A test asserts no clear PII appears in any other table or in logs
**And** the reveal endpoint requires `pii:reveal` and writes an audit event per reveal

### Story 3.5: Data-quality checks

As a credit officer,
I want incomplete records flagged rather than silently defaulted,
So that no decision rests on invented data (FR-18).

**Acceptance Criteria:**

**Given** a finance application missing a required field (e.g. housing allowance)
**When** it is assessed
**Then** the result status is `incomplete`, with the missing fields listed and no Recommendation of Approve
**And** range checks (negative salary, future dates) and freshness checks produce a data-quality report per run

### Story 3.6: Retail golden set

As a QA engineer,
I want a hand-crafted golden set, including the worked example and edge cases,
So that acceptance tests anchor on known answers (FR-66).

**Acceptance Criteria:**

**Given** `synth/golden/retail.json`
**When** loaded
**Then** it contains ≥ 20 cases: the golden worked example, an obvious best and worst case, age-at-maturity at the limit, DBR exactly 50%, a restricted nationality, a retiree, missing optional fields, and an EOSB-backed case
**And** each case carries its expected Grade range, Recommendation, Recommended Limit and Binding Constraint

### Story 3.7: Demo users and guided scenarios

As a salesperson,
I want demo users for every role and a guided scenario list,
So that I can present the product end to end (FR-66).

**Acceptance Criteria:**

**Given** a fresh Demo Tenant
**When** the seed command runs
**Then** demo users exist for each standard role, and a "Guided scenarios" page lists the scenarios available in the current release (UJ-1 and the risk ranking in R1)
**And** a reset command restores the Demo Tenant to its initial state

## Epic 4: Retail Assessment & Recommendation Core [R1]

**Squad:** Decision Core. **Depends on:** Epics 1, 2, 3.
Goal: a pure, deterministic `assess` that takes a retail finance application to a Grade, PD, Recommendation and Recommended Limit with Binding Constraint, and records a replayable Decision Record.

### Story 4.1: Retail demographic and employment features

As the decision core,
I want age now and at maturity, years of service, salary multiple and employer category as features,
So that eligibility and scoring rules can use them (FR-19).

**Acceptance Criteria:**

**Given** a Customer born 1992-03-01, joined 2020-11-07, applying on 2026-11-07 for 48 months
**When** features are derived
**Then** age now = 34, age at maturity = 38, years of service = 6.0 (unit tests including leap-year and month-end cases)
**And** the requested-amount salary multiple = finance amount ÷ gross monthly income

### Story 4.2: EOSB calculator

As the decision core,
I want accrued end-of-service benefit computed under UAE Labour Law,
So that EOSB-backed finance and caps are correct (FR-19).

**Acceptance Criteria:**

**Given** basic salary AED 12,000 and 6 years of service, with daily wage = basic × 12 / 365
**When** EOSB is computed
**Then** it equals 21 days × 5 years + 30 days × 1 year of daily wage ≈ AED 53,260 (± AED 1)
**And** the total is capped at 24 × basic (2 years' wages), and part years are pro-rated (unit tests)
**And** service under 1 year → EOSB 0. The formula parameters are configurable per Tenant
**And** EOSB-backed cap = 80% × EOSB (≈ AED 42,608 in this example) only when service ≥ 5 years

### Story 4.3: DBR and profit-rate annuity

As the decision core,
I want DBR before and after the new finance on DBR Income (basic + housing) with the profit-rate annuity,
So that affordability is computed exactly as the policy defines (FR-19, FR-20).

**Acceptance Criteria:**

**Given** DBR Income AED 18,000, existing obligation AED 3,000/month and a card limit of AED 20,000 at 5%
**When** existing DBR is computed
**Then** obligations = AED 4,000 and DBR before = 22.2%
**And** for AED 400,000 over 48 months at a 6% profit rate (monthly r = 0.5%), instalment ≈ AED 9,394 and DBR after ≈ 74.4% (unit test, tolerance ±1 AED / ±0.1 pp)
**And** the stress add-on (default 0) is applied to the profit rate when configured, e.g. +2% → instalment computed at 8% (test)
**And** zero profit rate gives instalment = amount ÷ tenor (edge test)

### Story 4.4: Behavioural features

As the decision core,
I want behaviour features from salary credits, cards, transactions and CASA,
So that the scorecard can use conduct signals (FR-19, E15).

**Acceptance Criteria:**

**Given** 12 months of salary credits, card statements and transactions with MCC
**When** features are derived
**Then** the output includes:
- salary-credit regularity and count of late salary credits
- average card utilisation (6 months) and cash-advance count
- monthly spend average and volatility, and spend-to-income
- category shares (essentials, travel, luxury, high-risk MCC)
- bonus-month spend ratio
- average CASA balance (6 months)
**And** each feature has a unit test on a fixed fixture, and missing sources yield `null` with a reason (never a silent zero)

### Story 4.5: Retail product rules for personal finance and card

As a risk manager,
I want CBUAE and demo-bank product rules applied to Tawarruq/Murabaha personal finance and Islamic cards,
So that every Recommendation respects the caps (FR-20 R1).

**Acceptance Criteria:**

**Given** the CBUAE pack and the demo Policy Version
**When** a personal finance application is assessed
**Then** these Rules are evaluated:
- ≤ 20× gross monthly income
- ≤ 48 months
- DBR ≤ 50%
- Total Unsecured Cap: existing unsecured limits + new amount ≤ 20× monthly income
- age at maturity
- salary transfer
**And** a unit test covers total unsecured: income AED 25,000 with an existing card limit AED 20,000 gives headroom AED 480,000
**And** card applications evaluate the CBUAE minimum income rule (flagged "to verify") and the demo card-limit matrix

### Story 4.6: Retail Scorecard and PD calibration

As a risk manager,
I want an expert points-based Scorecard mapped to PD,
So that every Customer gets a risk estimate from day one (FR-30 R1).

**Acceptance Criteria:**

**Given** bins and points from the Credit Policy for the factors:
- AECB band
- DBR-after band
- max DPD 12m and 90+ DPD 24m
- years of service and employer category
- salary regularity
- utilisation and cash advances
- spend volatility
- bureau enquiries
**When** a case is scored
**Then** the Score is on the Tenant scale, and PD = 1/(1+exp((score−a)/b)) with documented defaults
**And** on the synthetic Book the Scorecard achieves AUC ≥ 0.65 against the true default flag (test)
**And** the methodology is written to `docs/methodology/scorecard.md`

### Story 4.7: Risk Grades 1–10

As a credit officer,
I want PD shown as a Grade 1–10 on the bank's scale,
So that risk is communicated in the bank's own terms (FR-32).

**Acceptance Criteria:**

**Given** the default bands (1 <0.25%, 2 0.25–0.5%, 3 0.5–1%, 4 1–2%, 5 2–3.5%, 6 3.5–5%, 7 5–8%, 8 8–12%, 9 12–20%, 10 ≥20%)
**When** PD = 0.25% exactly, 1.6%, 5.0% and 20%
**Then** the Grades are 2, 4, 7 and 10 (lower bound inclusive; boundary unit tests)
**And** a Tenant can replace the bands and the score scale via ChangeRequest

### Story 4.8: Policy-first Recommendation with model escalation

As a CRO,
I want the policy to decide, with the model only able to escalate to Refer,
So that policy always wins (FR-33).

**Acceptance Criteria:**

**Given** rule results and a Grade
**When** the Recommendation is computed
**Then** any failed knockout → Decline. Otherwise any failed refer Rule → Refer. Otherwise Grade ≥ escalation grade (default 7) → Refer. Otherwise → Approve
**And** a property test proves the model can never turn a policy Decline or Refer into Approve
**And** an incomplete data status never yields Approve

### Story 4.9: Recommended Limit with Binding Constraint

As a credit officer,
I want the largest safe finance amount and the rule that sets it,
So that I can make a counter-offer confidently (FR-35).

**Acceptance Criteria:**

**Given** the golden worked example (expat government employee, gross AED 25,000, DBR Income AED 18,000, obligations AED 4,000, request AED 400,000 / 48 months / 6%)
**When** the limit is computed
**Then** candidates are:
- CBUAE 20× = 500,000
- Total Unsecured headroom = 480,000
- bank employer cap (per demo policy)
- DBR-headroom ≈ 212,902
- requested = 400,000
**And** the Recommended Limit = AED 212,000 (rounded down to the Tenant rounding unit of 1,000), with Binding Constraint = `DBR`
**And** the instalment ≈ AED 4,979 and DBR ≈ 49.9% at the Recommended Limit
**And** the output includes a what-would-change hint: "Maximum finance amount that passes DBR: AED 212,000"
**And** an EOSB-backed product adds the EOSB cap (unit test), and a tie between caps reports all binding constraints

### Story 4.10: Assess service and replayable Decision Record

As an auditor,
I want every assessment stored immutably and replayable to identical outputs,
So that any past decision can be explained exactly (FR-61, AD-1, AD-9, NFR-6).

**Acceptance Criteria:**

**Given** an assessment produced by `assess(snapshot, policy_version, model_version, params)`
**When** it is stored
**Then** the Decision Record contains the snapshot hash and content, Policy Version id, model version (or `scorecard-only`), outputs, rule results and timestamps, and is hash-chained
**And** the replay command re-runs `assess` from the record and asserts identical output hashes for 1,000 random synthetic cases
**And** running the same case twice yields byte-identical outputs (determinism test)

## Epic 5: Officer Decision Screen & Risk Ranking [R1]

**Squad:** Frontend (with Decision Core support). **Depends on:** Epics 1–4.
Goal: the R1 demo is complete. A credit officer submits a demo finance application, sees the decision with drill-down and bilingual template Explanation, and a risk manager sees the whole Book ranked (PRD J9 "done").

### Story 5.1: Internal assessment API v1

As a frontend developer,
I want documented internal endpoints to submit a demo finance application and fetch assessments,
So that the UI and later integrations share one contract (AD-14, FR-43).

**Acceptance Criteria:**

**Given** the OpenAPI spec committed under `backend/openapi.json`
**When** `POST /api/v1/assessments` is called with a demo application reference by an authenticated internal user
**Then** it returns Grade, PD, Recommendation, Recommended Limit, Binding Constraint, failed Rules and the Decision Record id
**And** the TypeScript client is generated from the spec in CI, and drift fails the build
**And** no endpoint serves Explanation text to unauthenticated or external clients (FR-43)

### Story 5.2: Template Explanations in English and Arabic

As a credit officer,
I want a plain-language Explanation in English and Arabic for each assessment,
So that I can understand and record the reasons (FR-40 R1, NFR-8).

**Acceptance Criteria:**

**Given** an assessment's facts (decision, Grade, top drivers, failed Rules, Binding Constraint, what-if hint)
**When** the template engine renders
**Then** an English and an Arabic text are produced that contain only values from the facts (test compares numbers)
**And** Arabic renders right-to-left in the UI. Templates are reviewed strings, no LLM

### Story 5.3: Decision Screen summary

As a credit officer,
I want one screen with the decision essentials,
So that I can decide in under a minute (UX-DR1, UX-DR10, UJ-1).

**Acceptance Criteria:**

**Given** a completed assessment
**When** the Decision Screen opens
**Then** it shows:
- Grade on the Tenant scale and PD
- Recommendation, Recommended Limit vs requested, and Binding Constraint
- top-3 drivers
- the Explanation with an EN/AR toggle
- the disclaimer
**And** the page passes axe WCAG 2.1 AA checks and renders within 1 s after the API response

### Story 5.4: Decision Screen drill-down

As a credit officer,
I want to expand the full calculation,
So that I can verify the maths and every rule (UX-DR2).

**Acceptance Criteria:**

**Given** the golden worked example
**When** the drill-down opens
**Then** it shows:
- the DBR arithmetic (DBR Income 18,000; obligations 4,000; instalment 9,394 → 74.4%)
- each Rule with layer, severity, pass/fail, source and confidence badge
- a limit waterfall listing each cap with DBR highlighted as binding at AED 212,000

### Story 5.5: Risk ranking of the Book

As a risk manager,
I want the whole Book scored and ranked from highest to lowest PD,
So that I can see where risk sits (FR-45, UX-DR4 partial).

**Acceptance Criteria:**

**Given** the demo Book of 20,000 Customers
**When** a risk manager triggers "Score Book" (a worker job)
**Then** all Customers are scored and listed by PD descending, with Grade, Recommendation, product, employer category and top-3 drivers
**And** filters (segment, product, employer category, Grade) and pagination work, and the "as of" date is shown
**And** the job completes in ≤ 10 minutes for 20k Customers on the reference server

### Story 5.6: R1 performance baseline for assess

As a platform engineer,
I want a performance test for single assessments,
So that NFR-1 is tracked from R1 (NFR-1).

**Acceptance Criteria:**

**Given** a k6 script in `perf/` hitting `POST /api/v1/assessments` with 20 concurrent virtual users
**When** run against the Docker Compose stack on reference hardware
**Then** p95 ≤ 2 s and p99 ≤ 5 s without LLM text, and results are stored as a CI artifact

### Story 5.7: R1 end-to-end demo acceptance

As a product owner,
I want an automated E2E test of the R1 demo flow,
So that "R1 done" is objectively verifiable (PRD J9).

**Acceptance Criteria:**

**Given** a fresh Docker Compose install with the Demo Tenant seeded
**When** the Playwright suite runs
**Then** a credit officer logs in, submits the golden worked example, and sees Recommendation "Approve at AED 212,000" with the DBR binding, the drill-down and the EN/AR Explanation
**And** a risk manager runs "Score Book" and sees the ranked list with the golden worst case in Grade 9–10 and the best case in Grade 1–2
**And** the "DEMO DATA" banner and disclaimer are visible on every page visited

## Epic 6: Enterprise Access & Approval Workflow [R2]

**Squad:** Platform + Frontend. **Depends on:** Epics 1, 2, 4, 5.
Goal: bank users log in with Active Directory. Referred and deviation cases route to the right Approval Authority queue, and every override is recorded and reported.

### Story 6.1: Active Directory / SSO login

As a bank user,
I want to sign in with my bank Windows account,
So that access follows the bank's identity controls (FR-39 R2).

**Acceptance Criteria:**

**Given** an OIDC or SAML IdP (and LDAP group lookup) configured per Tenant
**When** a user signs in
**Then** their AD groups map to product roles via Tenant configuration, and local accounts can be disabled for that Tenant
**And** session timeout and logout are enforced. Integration tests run against a test IdP container

### Story 6.2: Tenant-configurable roles and permissions

As a sys admin,
I want to define custom roles from permission strings,
So that each bank's organisation is reflected (FR-39).

**Acceptance Criteria:**

**Given** the standard role set as a template
**When** an admin creates or edits a role (through a ChangeRequest)
**Then** permissions take effect on the next request, and a role-permission report is exportable for audit

### Story 6.3: Delegation-of-authority matrix

As a CRO,
I want to configure who can approve what (amount × Grade × Deviation × product),
So that cases reach the correct authority (FR-37).

**Acceptance Criteria:**

**Given** a matrix, e.g. Branch Manager ≤ AED 100k for Grades 1–6, Head of Credit ≤ AED 1m, Credit Committee above that or any Deviation at Grade ≥ 6
**When** a case is evaluated
**Then** the required Approval Authority is computed deterministically (table-driven unit tests, including boundaries)
**And** matrix changes require a ChangeRequest

### Story 6.4: Grade-based Deviation matrix

As a CRO,
I want the Grade to decide whether a rule failure can be approved as a Deviation and by whom,
So that exceptions follow risk (FR-34).

**Acceptance Criteria:**

**Given** a Deviation matrix (e.g. Grades 1–4 deviable at Head of Credit, 5–6 at Credit Committee, 7–10 not deviable)
**When** a Credit Officer requests a Deviation on a failed Bank or Credit Policy Rule
**Then** it is allowed only within the matrix and routed to the required authority
**And** a Deviation on any CBUAE Rule is always refused (test)
**And** the Decision Record stores the Rule, reason, approver and Grade

### Story 6.5: Approval queues and actions

As an approver,
I want a queue of cases within my authority with approve, return and escalate actions,
So that I can clear my work efficiently (FR-37, UX-DR3, UJ-2).

**Acceptance Criteria:**

**Given** Referred and Deviation cases routed by the matrix
**When** an approver opens the queue
**Then** they see only cases within their authority, sorted by risk, with Deviation flags
**And** approve, return-with-comment and escalate actions update the case and write to the Decision Record
**And** a user can never approve a case they originated (checker ≠ maker, test)

### Story 6.6: Overrides and override reporting

As a CRO,
I want every override captured with a reason and reported,
So that judgement is visible and governable (FR-38 R2).

**Acceptance Criteria:**

**Given** a Credit Officer changing a Recommendation or limit
**When** they submit
**Then** a reason code and free text are mandatory and stored in the Decision Record
**And** an override report by officer, branch, Grade and later outcome is available and exportable to Excel

### Story 6.7: Approval queue UI

As an approver,
I want the queue and case view in the web app,
So that the workflow is usable day to day (UX-DR3).

**Acceptance Criteria:**

**Given** the queue API
**When** an approver works a case in the UI
**Then** the Decision Screen opens with the approval panel (required authority, Deviation details, comment box)
**And** E2E tests cover approve, return and escalate, and the screens pass WCAG 2.1 AA checks

## Epic 7: Bank Integration: T24 & Data Warehouse [R2]

**Squad:** Data & Integrations. **Depends on:** Epics 1, 2, 3, 4.
Goal: real finance applications arrive from T24 in real time, and the Book, history and behaviour data are read from the bank's warehouse through read-only connectors.

### Story 7.1: Real-time finance application API for LOS

As bank IT,
I want T24 or the LOS to submit a finance application and receive the assessment synchronously,
So that decisions happen inside the origination flow (FR-11).

**Acceptance Criteria:**

**Given** a service client authenticated with mTLS or client credentials
**When** it POSTs to `/api/v1/finance-applications`
**Then** the response contains Grade, PD, Recommendation, Recommended Limit, Binding Constraint, failed Rules and the Decision Record reference
**And** the Explanation is fetched later by reference (async), and requests are idempotent on the source application id

### Story 7.2: Temenos T24/Transact adapter

As bank IT,
I want a T24/Transact adapter with configurable field mapping,
So that integration needs configuration rather than code (FR-12).

**Acceptance Criteria:**

**Given** a mapping file from T24 fields to the CDM
**When** a T24 payload arrives
**Then** it is mapped to CDM objects, and mapping errors list the offending fields
**And** the mapping is validated against the Data Field Template (Story 7.6) at load time
**And** contract tests use recorded T24-style fixtures

### Story 7.3: Read-only SQL source connector

As bank IT,
I want the Book, history and rejected applications read from warehouse views over a read-only connection,
So that no bank system can be modified (FR-13, AD-5, AD-13).

**Acceptance Criteria:**

**Given** configured views on PostgreSQL or SQL Server
**When** the connector reads
**Then** CDM objects are produced in pages
**And** any write attempt fails and is logged (test with a write-capable account is rejected at configuration time)
**And** CI runs the connector tests on PostgreSQL and SQL Server containers

### Story 7.4: Behavioural data from raw transactions or aggregates

As a data engineer,
I want the same behaviour features from raw transactions or monthly aggregates,
So that banks with either data shape are supported (FR-15).

**Acceptance Criteria:**

**Given** a Customer with both raw transactions and aggregates
**When** features are derived
**Then** raw transactions take precedence, and feature lineage records the source used
**And** features computed from aggregates match those from raw data within documented tolerances on the synthetic set (test)

### Story 7.5: Stored AECB data reader

As a credit officer,
I want the bank's stored AECB score and report fields used in assessment,
So that bureau information informs decisions without outbound calls (FR-16 R2).

**Acceptance Criteria:**

**Given** AECB fields in the warehouse (score 300–900, enquiries, external obligations, delinquency records)
**When** a case is assessed
**Then** the fields feed the features and Rules, and a missing AECB report triggers the CBUAE "report required" Rule → Refer
**And** no outbound connection is opened (egress test)

### Story 7.6: Data Field Template from policy

As bank IT,
I want a generated list of required and optional fields derived from the active policy,
So that I know exactly what to supply (FR-7).

**Acceptance Criteria:**

**Given** the active Policy Version
**When** the template is generated
**Then** it lists every field referenced by Rules and Scorecard factors with type, definition and required/optional, exportable to Excel
**And** publishing a Rule that uses a new field updates the template and flags the field as missing in data-quality checks

### Story 7.7: Real-time API performance and resilience

As a platform engineer,
I want load and failure tests for the LOS API,
So that NFR-1 and NFR-7 hold in pilot conditions (NFR-1, NFR-7).

**Acceptance Criteria:**

**Given** k6 at 20 concurrent clients
**When** run against the API with the T24 adapter
**Then** p95 ≤ 2 s and p99 ≤ 5 s
**And** with the Learning Model unavailable, responses still succeed using the Scorecard (degradation test)

## Epic 8: Islamic Product Coverage & Retail Customer Types [R2]

**Squad:** Decision Core. **Depends on:** Epics 2, 4.
Goal: all v1 Islamic retail products and Customer types are assessable with correct CBUAE limits and Sharia-specific checks.

### Story 8.1: Auto Murabaha rules

As a credit officer,
I want auto Murabaha applications assessed against CBUAE limits,
So that vehicle finance is compliant (FR-20 R2).

**Acceptance Criteria:**

**Given** a vehicle value of AED 150,000 and a request of AED 130,000 over 72 months
**When** assessed
**Then** the LTV Rule fails (max 80% = AED 120,000) and the tenor Rule fails (max 60 months). Unit tests also cover exactly 80% and exactly 60 months (pass)
**And** a down payment funded by personal finance or a card fails the "own funds" Rule
**And** the Recommended Limit includes the LTV cap as a candidate constraint

### Story 8.2: Ijara home finance rules

As a credit officer,
I want Ijara home finance assessed against the CBUAE LTV table,
So that home finance is compliant (FR-20 R2).

**Acceptance Criteria:**

**Given** the LTV table
**When** unit tests run
**Then** they assert:
- national first home ≤ AED 5m → 85%; expat → 80%
- > AED 5m → 75% / 70%
- second home → 65% / 60%
- off-plan → 50% for any buyer
- the AED 5m boundary is included in the ≤ band
**And** tenor > 25 years fails, DBR uses the 50% cap, and EOSB is excluded as a repayment source
**And** maximum age at maturity comes from the Tenant policy (CBUAE sets none)

### Story 8.3: Self-employed and retired Customers

As a credit officer,
I want self-employed and retired Customers assessed under their segment rules,
So that these segments can be served (FR-21).

**Acceptance Criteria:**

**Given** a retiree with a pension of AED 15,000
**When** assessed
**Then** the DBR cap is 30% (CBUAE) and the limit reflects it (unit test)
**And** a self-employed Customer's income is derived from verified business credits per Tenant rules, with income source shown in the drill-down

### Story 8.4: Non-resident and low-salary segments

As a risk manager,
I want non-residents and low-salary Customers handled by Tenant-defined thresholds and caps,
So that financial inclusion is supported within appetite (FR-21).

**Acceptance Criteria:**

**Given** the Tenant's low-salary threshold (e.g. gross < AED 5,000) and caps
**When** such a Customer is assessed
**Then** the segment-specific caps apply and are named in the Binding Constraint, with no separate model
**And** non-resident rules apply per Tenant policy, and the segment appears in the ranking filters

### Story 8.5: Joint applicants and guarantors

As a credit officer,
I want co-applicants and guarantors included,
So that combined capacity and support are assessed (FR-22).

**Acceptance Criteria:**

**Given** a finance application with one co-applicant
**When** assessed
**Then** combined DBR Income and obligations are used for DBR (unit test), and each applicant's individual eligibility Rules are evaluated
**And** guarantor strength is a Scorecard factor and a Rule input, shown in the drill-down

### Story 8.6: Islamic product-structure checks and charity treatment

As a Sharia reviewer,
I want product-structure data checked and late-payment amounts never counted as income,
So that assessments respect Sharia requirements (FR-23).

**Acceptance Criteria:**

**Given** a Tawarruq application without the commodity purchase step recorded
**When** assessed
**Then** a `refer` Rule fails with "structure data missing"
**And** Ijara applications require the ownership/lease fields
**And** late-payment amounts are tagged `charity` and excluded from every income or ROI computation (test asserts exclusion)

## Epic 9: Corporate & SME Assessment [R2]

**Squad:** Decision Core. **Depends on:** Epics 2, 3, 4.
Goal: corporate and SME obligors get a five-dimension rating, Grade, Recommendation and stressed-capacity limit within CBUAE large-exposure limits.

### Story 9.1: Corporate financial features

As a corporate analyst,
I want standard ratios computed from confirmed financial spreads,
So that financial capacity is measured consistently (FR-24).

**Acceptance Criteria:**

**Given** a spread with revenue, EBITDA, total debt, profit expense, OCF, cash, undrawn facilities and debt service
**When** features are derived
**Then** Debt/EBITDA, gearing, profit cover, cash conversion (OCF/EBITDA), DSCR and liquidity runway are computed (unit tests with fixtures, including EBITDA ≤ 0 handled as "not meaningful")
**And** audit quality (audited flag, auditor tier, qualified opinion, years of statements) is captured

### Story 9.2: Five-dimension rating

As a corporate analyst,
I want each dimension scored 0–100 and weighted into a Score, PD and Grade,
So that obligors are rated on the research framework (FR-24).

**Acceptance Criteria:**

**Given** default weights 35/20/15/10/20 (financial, business, governance, external, security)
**When** an obligor is rated
**Then** the Score is the weighted sum on the Tenant scale, mapped to PD and Grade 1–10. Weights are configurable via ChangeRequest
**And** each dimension's sub-factor contributions are stored for the drill-down

### Story 9.3: Corporate knockouts

As a CRO,
I want automatic declines for fatal combinations and prohibited sectors,
So that obvious bad credit never progresses (FR-25).

**Acceptance Criteria:**

**Given** a financial dimension score below the "weak" threshold and governance below "weak"
**When** assessed
**Then** the combination knockout fails → Decline. The same applies with unenforceable security
**And** a Sharia-prohibited sector → Decline, and a restricted sector → the Tenant's severity
**And** with empty Tenant thresholds (demo), only the combination rule (using demo "weak" thresholds) and the sector rules apply

### Story 9.4: Stressed sizing and collateral capacity

As a corporate analyst,
I want facility capacity sized on stressed cash flow plus collateral,
So that limits survive a downturn (FR-26).

**Acceptance Criteria:**

**Given** EBITDA AED 14m, existing debt service and a policy minimum DSCR of 1.25
**When** sized with the default stress (EBITDA −30%)
**Then** capacity = the maximum new debt service that keeps stressed DSCR ≥ 1.25, converted to a facility amount at the profit rate and tenor (unit test with worked numbers)
**And** collateral capacity = value × (1 − haircut by type) using the Tenant's haircut table (CBUAE indicative defaults), and the Recommended Limit names the binding one

### Story 9.5: Group aggregation and large-exposure limits

As a CRO,
I want exposure aggregated across connected obligors and checked against CBUAE limits,
So that concentration rules are never breached (FR-27).

**Acceptance Criteria:**

**Given** Tenant Tier 1 = AED 5bn and a group with existing exposure of AED 1.1bn
**When** a new AED 300m facility is assessed
**Then** the 25% single/group limit (AED 1.25bn) fails with headroom AED 150m reported
**And** unit tests cover shareholder (20%/50%), affiliate (10%/25%), board member (5%/25%), GRE (25%/100%) and federal government exempt
**And** groups are defined by configured links (ownership, guarantees), shown in the drill-down

### Story 9.6: Sole proprietors on owner salary

As a credit officer,
I want sole proprietors financed on the owner's salary assessed with retail rules,
So that CBUAE Reg 29/2011 Art 2(e) is respected (FR-29).

**Acceptance Criteria:**

**Given** a sole proprietorship application secured by the owner's salary
**When** assessed
**Then** the retail rules apply (20× income, 48 months, DBR 50%), and the segment is labelled in the Decision Record

### Story 9.7: Synthetic corporate Book and golden set

As a data scientist,
I want a synthetic corporate and SME Book with known risk and a golden set,
So that the corporate model is testable and demoable (FR-66).

**Acceptance Criteria:**

**Given** `python -m synth corporate --n 1000 --seed 42`
**When** it runs
**Then** consistent financials, governance, collateral, groups and a 4–8% default rate are produced and loaded into the demo source
**And** a corporate golden set (≥ 15 cases) includes a Sharia-prohibited sector, a large-exposure breach, a combination knockout and the "weak cash conversion" illustrative case at Grade 7 → Refer

### Story 9.8: Obligor assessment screen

As a corporate analyst,
I want an obligor view with the five dimensions, sizing and exposure checks,
So that I can review a corporate case end to end (UJ-6, UX-DR1/2).

**Acceptance Criteria:**

**Given** an assessed obligor
**When** the screen opens
**Then** it shows the Grade and PD, the dimension scores with drivers, stressed DSCR and capacity, collateral capacity, group exposure vs limit, Recommendation and Binding Constraint
**And** it passes WCAG 2.1 AA checks

## Epic 10: Document AI & Policy Extraction [R2]

**Squad:** AI/LLM. **Depends on:** Epics 2, 9.
Goal: a local LLM runtime is integrated. PDF financial statements become reviewable spreads, and policy manuals become reviewable Draft Rules.

### Story 10.1: LLM runtime port and adapter

As a platform engineer,
I want an `LLMClient` port with Ollama and vLLM adapters and hardware-based model selection,
So that language features run locally on any bank's hardware (AD-6, NFR-11).

**Acceptance Criteria:**

**Given** the installer's hardware detection
**When** the GPU is ≥ 24 GB / 8–16 GB / absent
**Then** the config selects a 14B-class Qwen, an 8B-class Llama/Qwen, or "no LLM" respectively
**And** the adapter enforces timeouts, runs only in the worker, and logs prompts without PII (test asserts no `pii_vault` values reach prompts)
**And** a fake LLM adapter exists for tests

### Story 10.2: PDF financial-statement extraction

As a corporate analyst,
I want figures extracted from PDF statements into a draft spread,
So that I don't retype financials (FR-28).

**Acceptance Criteria:**

**Given** text-based and scanned PDF statements (fixtures)
**When** extraction runs (pdfplumber, Tesseract OCR for scans, LLM table mapping)
**Then** a draft spread is created where every figure links to its page and bounding text
**And** on the fixture set, ≥ 95% of key line items match the expected values. Mismatches are reported, not hidden

### Story 10.3: Spread review and confirmation

As a corporate analyst,
I want to review, correct and confirm a draft spread,
So that only verified numbers are used in ratings (FR-28).

**Acceptance Criteria:**

**Given** a draft spread
**When** the analyst edits and confirms it
**Then** the confirmed spread is versioned with user and time, and only confirmed spreads feed Story 9.1 features (test)

### Story 10.4: Policy manual to Draft Rules

As a policy admin,
I want the LLM to propose Draft Rules from the bank's policy manual,
So that onboarding a new bank's policy is fast (FR-5, UJ-5).

**Acceptance Criteria:**

**Given** a PDF/Word credit policy
**When** extraction runs
**Then** each Draft Rule has a proposed condition, severity, applicability, and the source page/section with an excerpt
**And** Draft Rules are validated by the schema and the safe evaluator. Invalid proposals are flagged, never published

### Story 10.5: Draft Rule review into ChangeRequest

As a policy admin,
I want to review Draft Rules side by side with their source and submit approved ones,
So that nothing becomes active without maker-checker (FR-5, FR-6).

**Acceptance Criteria:**

**Given** a set of Draft Rules
**When** the admin accepts, edits or rejects each one and submits
**Then** a ChangeRequest is created. On checker approval, tighten-only runs, and any Rule looser than CBUAE blocks publication with its name

## Epic 11: Learning Model & Model Governance [R2]

**Squad:** ML & Analytics. **Depends on:** Epics 2, 3, 4.
Goal: a governed gradient-boosting Learning Model trained on the bank's history refines the Scorecard, with activation gates, drift handling, auto-suspension, validation packs and fairness reporting.

### Story 11.1: Training dataset builder with reject inference

As a model developer,
I want a reproducible training dataset from history, including rejected applications,
So that the model learns from the full through-the-door population (FR-31).

**Acceptance Criteria:**

**Given** 1–2 years of applications, outcomes (default = 90+ DPD within 12 months) and rejects
**When** the builder runs
**Then** it produces a feature matrix via the shared feature pipeline (AD-4), the labels, a reject-inference augmentation (documented method), and a data snapshot hash
**And** an out-of-time split uses the latest 20% by date when dates exist

### Story 11.2: Gradient-boosting training with constraints and exclusions

As a model developer,
I want a LightGBM model with monotonic constraints and protected attributes excluded,
So that the model is accurate, sensible and fair (FR-31).

**Acceptance Criteria:**

**Given** the training dataset
**When** training runs in the worker with a fixed seed
**Then** nationality, gender, marital status and religion are excluded (a test fails if they appear), and age is allowed
**And** monotonic constraints apply to configured features (e.g. DPD ↑ → risk ↑)
**And** on the synthetic Book, out-of-time AUC ≥ 0.75 retail / ≥ 0.70 corporate
**And** per-case contributions (`pred_contrib`) are produced

### Story 11.3: Model registry and activation gate

As a model validator,
I want models registered with cards and activated only through approval after passing the gate,
So that no unvalidated model reaches decisions (FR-57, AD-8, AD-7).

**Acceptance Criteria:**

**Given** a trained model
**When** registered
**Then** the artifact hash, model card (data window, default rate, AUC, Gini, KS, calibration, PSI, top features) and data hash are stored
**And** activation requires ≥ 1,000 rows, ≥ 50 defaults, out-of-time Gini ≥ 0.30 **and** an approved ChangeRequest by a Model Validator. Failing any condition blocks activation (tests)

### Story 11.4: PD blend and serving with fallback

As the decision core,
I want the final PD to blend the active model and the Scorecard, with automatic fallback,
So that scoring always works (FR-31, NFR-7).

**Acceptance Criteria:**

**Given** an active model and weight w (default 0.6)
**When** a case is assessed
**Then** PD_final = w·PD_model + (1−w)·PD_scorecard, and the Decision Record stores both and the model version
**And** with no active or a suspended model, w = 0 and the record says `scorecard-only` (test)
**And** replay with the stored model version reproduces the PD exactly

### Story 11.5: Drift monitoring, auto-retrain and auto-suspend

As a CRO,
I want drift detected, challengers retrained automatically, and failing models suspended,
So that model risk is controlled continuously (FR-58).

**Acceptance Criteria:**

**Given** PSI and performance computed on each run
**When** PSI > 0.25 or performance drops beyond the configured limit
**Then** a challenger is retrained automatically and queued for activation approval (never auto-activated)
**And** if suspension limits are breached, the live model is set to `suspended`, the Scorecard takes over within the same run, and Risk is alerted (test with injected drift)

### Story 11.6: Validation pack and CBUAE model documentation

As a model validator,
I want generated validation and development documentation per model version,
So that internal and external validation is efficient (FR-59).

**Acceptance Criteria:**

**Given** a registered model
**When** the pack is generated
**Then** it contains performance, stability, calibration, backtesting and sensitivity sections, and development documentation following the CBUAE Model Management Standards outline
**And** an export bundle (PDF + data tables, no PII) is downloadable for external validators

### Story 11.7: Fairness report

As a compliance officer,
I want outcome and approval-rate monitoring by gender, nationality group and age band,
So that unfair patterns are detected (FR-60).

**Acceptance Criteria:**

**Given** a model version and its scored population
**When** the fairness report runs
**Then** it shows approval rate, average PD and default rate per group, with disparity ratios, and flags groups beyond the configured threshold
**And** the report states that these attributes are not model inputs (except age)

### Story 11.8: Bank scorecard import and data-refined weights

As a risk manager,
I want to import the bank's existing scorecard and refine weights from data,
So that defaults are replaced by the bank's own methodology (FR-30 R2).

**Acceptance Criteria:**

**Given** an exported scorecard (bins, points) in the documented Excel format
**When** imported via ChangeRequest
**Then** it replaces the expert defaults for that segment
**And** a WoE/logistic recalibration proposal can be generated from history and submitted as a ChangeRequest, with before/after AUC shown

### Story 11.9: Model Lab screen

As a model validator,
I want a Model Lab to train, compare, activate and suspend models,
So that model governance is operable without code (UX-DR7, FR-57).

**Acceptance Criteria:**

**Given** registered models
**When** the Model Lab opens
**Then** model cards, gate results, champion vs challenger, and PSI/performance trend charts are shown, and activate/suspend actions create ChangeRequests
**And** the screens pass WCAG 2.1 AA checks

## Epic 12: AI Explanations & Credit Memos [R2]

**Squad:** AI/LLM. **Depends on:** Epics 4, 5, 10.
Goal: LLM-written bilingual Explanations and drafted credit memos, protected by a strict guardrail and human sign-off.

### Story 12.1: Facts JSON and number/rule guardrail

As a CRO,
I want any LLM text containing numbers or Rule ids not present in the facts to be discarded,
So that credit files never contain invented figures (FR-41, AD-6).

**Acceptance Criteria:**

**Given** a facts JSON produced after `assess`
**When** a fake LLM returns text with an invented number (e.g. "AED 250,000" when the limit is 212,000) or an unknown Rule id
**Then** the guardrail rejects it and the template Explanation is used (unit test)
**And** numbers are normalised (thousand separators, AED prefix, %, Arabic-Indic digits) before comparison

### Story 12.2: LLM Explanations in English and Arabic

As a credit officer,
I want richer bilingual Explanations from the local LLM, with automatic fallback,
So that I get clear reasons even when the LLM is unavailable (FR-40 R2, FR-43, NFR-8).

**Acceptance Criteria:**

**Given** an assessment
**When** the worker generates the Explanation (temperature 0) within 20 s
**Then** English and Arabic texts are stored as a versioned Explanation linked to the Decision Record
**And** with the LLM stopped, the template is used and the UI shows "standard explanation" (test)
**And** Explanations are served only to authenticated internal users

### Story 12.3: Credit memo and credit paper drafting

As a credit officer,
I want a drafted credit memo (retail) or credit paper (corporate) that I edit and sign,
So that documentation takes minutes (FR-42, UJ-1, UJ-6).

**Acceptance Criteria:**

**Given** an assessment
**When** a memo is requested
**Then** a draft with standard sections is generated from facts (guardrailed): applicant, request, policy results, risk, limit, recommendation, conditions
**And** the memo remains `draft` until a Credit Officer edits and signs it. The signed version is stored in the Decision Record

### Story 12.4: Bilingual PDF rendering

As a credit officer,
I want signed memos and Explanations exported as PDF in English and Arabic,
So that they can go into the credit file (FR-42, UX-DR9).

**Acceptance Criteria:**

**Given** a signed memo
**When** exported
**Then** a PDF renders with correct Arabic shaping and RTL layout, the Tenant's white-label logo, the disclaimer and, for the Demo Tenant, a "DEMO DATA" watermark
**And** a visual regression test checks the rendered fixtures

## Epic 13: Pilot Operations: Nightly Run, Packaging, Licensing & Security [R2]

**Squad:** Platform. **Depends on:** Epics 1–4, 7.
Goal: the product is operable at a pilot bank. The Book is re-scored nightly within budget, installable on Docker or Windows, updatable offline, licensed, egress-locked and encrypted.

### Story 13.1: Nightly Run scheduler and re-score

As a risk manager,
I want the whole Book re-scored every night,
So that every morning I see current risk (FR-44 basic).

**Acceptance Criteria:**

**Given** a Tenant schedule (default 01:00 Asia/Dubai)
**When** the Nightly Run executes
**Then** all Customers and obligors are re-scored via the shared pipeline, and Grade migrations are stored
**And** a failed run alerts and leaves the previous results visible with their "as of" date (NFR-7)
**And** the job is idempotent per `(tenant, date)`

### Story 13.2: Nightly performance test

As a platform engineer,
I want the nightly run tested at pilot scale,
So that NFR-2 is met.

**Acceptance Criteria:**

**Given** a synthetic Book of 100k Customers + 5k obligors on reference hardware
**When** the Nightly Run executes
**Then** it completes in ≤ 2 h (excluding LLM narratives), with timings per stage recorded as CI artifacts

### Story 13.3: Signed release bundles and offline updates

As bank IT,
I want signed update packages applicable offline or via an outbound-only channel,
So that updates are safe in air-gapped environments (FR-63, AD-16).

**Acceptance Criteria:**

**Given** a release bundle (images, migrations, regulator pack) signed with Ed25519
**When** applied
**Then** the signature is verified first, and a tampered bundle is rejected (test)
**And** the update supports both USB/offline import and the outbound-only update mode, chosen per Tenant

### Story 13.4: Windows Server installer

As bank IT,
I want a Windows Server installer for banks that do not allow containers,
So that installation is possible everywhere (FR-63 R2).

**Acceptance Criteria:**

**Given** a clean Windows Server
**When** the installer runs
**Then** API, worker, web, database (or connection to the bank's SQL Server) and Redis-compatible queue are installed as services, health checks pass, and uninstall leaves data intact

### Story 13.5: Offline licence and read-only mode

As the vendor,
I want a signed licence per bank verified offline,
So that use is controlled without phoning home (FR-64, AD-16).

**Acceptance Criteria:**

**Given** a licence JSON (bank id, tenants, modules, expiry) signed with the vendor key
**When** verified at start-up and daily
**Then** an invalid signature blocks start, an expired licence switches to read-only mode (audit access only), and no data is deleted (tests)

### Story 13.6: Egress deny-by-default

As a CISO,
I want all outbound connections blocked unless allow-listed,
So that no customer data can leave (NFR-3, AD-11).

**Acceptance Criteria:**

**Given** the default configuration
**When** any component attempts an outbound connection
**Then** it is blocked and logged. Allow-list entries can only be added via ChangeRequest
**And** an automated test runs the full stack in a network namespace and asserts zero outbound attempts during assessment and the Nightly Run

### Story 13.7: Encryption at rest and secret management

As a CISO,
I want database and file encryption and secrets in a vault or keystore,
So that data at rest is protected (NFR-4).

**Acceptance Criteria:**

**Given** a production install
**When** inspected
**Then** DB storage/TDE or column encryption and blob-store encryption are enabled, TLS is enforced, and secrets come from the configured vault/keystore
**And** the security pack documents key rotation steps

### Story 13.8: SQL Server compatibility and security testing in CI

As a platform engineer,
I want migrations and repositories tested on PostgreSQL and SQL Server, plus dynamic security scans,
So that bank database choice and security are assured (AD-13, NFR-4).

**Acceptance Criteria:**

**Given** the CI matrix
**When** a PR runs
**Then** Alembic migrations and repository tests pass on PostgreSQL and SQL Server containers
**And** OWASP ZAP baseline runs against the stack, and high findings fail the build

## Epic 14: Bank Onboarding & Commercial Readiness Pack [R2]

**Squad:** Delivery & Compliance (with Platform and ML input). **Depends on:** Epics 1–13 (documents describe built features).
Goal: the documents a UAE Islamic bank needs to approve, contract, install, validate and use the product in a pilot.

### Story 14.1: Security pack

As a bank CISO,
I want a security pack,
So that I can approve installation (NFR-4, AD-10, AD-11).

**Acceptance Criteria:**

**Given** the R2 build
**When** the pack is produced in `docs/packs/security/`
**Then** it covers architecture and data-flow diagrams, the egress policy, encryption, RBAC/SSO, the audit chain, the hardening guide, the vulnerability-management process and a pen-test readiness checklist, and is reviewed by the platform lead

### Story 14.2: UAE PDPL data-protection pack

As a bank DPO,
I want a data-protection description,
So that processing complies with UAE PDPL.

**Acceptance Criteria:**

**Given** the data inventory
**When** the pack is produced
**Then** it lists data categories, purposes, lawful basis notes, the pseudonymisation and retention controls (FR-17, FR-62), data-subject request support and the on-premise residency statement

### Story 14.3: CBUAE outsourcing / third-party due-diligence pack

As a bank vendor-risk officer,
I want standard due-diligence answers,
So that the bank can onboard us under CBUAE outsourcing rules.

**Acceptance Criteria:**

**Given** the CBUAE outsourcing and third-party expectations
**When** the pack is produced
**Then** it answers company, BCP, support access (remote by invitation / on-site), sub-processors (none at runtime), incident notification, exit and data-return questions

### Story 14.4: Sharia compliance note

As a Sharia board member,
I want a note explaining terminology and product logic,
So that the board can review the tool.

**Acceptance Criteria:**

**Given** the Islamic product rules (FR-20, FR-23)
**When** the note is produced
**Then** it explains the profit-rate usage, the Tawarruq/Murabaha/Ijara structure checks, charity treatment of late amounts, Sharia-prohibited sector handling, and the statement that the tool does not approve products (the bank's Sharia board does)

### Story 14.5: Model documentation and validation templates

As a model validator,
I want templates aligned to CBUAE Model Management Standards,
So that generated packs (Story 11.6) slot into the bank's governance (FR-59).

**Acceptance Criteria:**

**Given** the validation pack generator
**When** templates are finalised
**Then** development, validation and annual-review templates exist with section guidance, and an example filled from the synthetic model is included

### Story 14.6: NDA and DPA templates

As a salesperson,
I want NDA and data-processing agreement templates,
So that pilot contracting can start quickly.

**Acceptance Criteria:**

**Given** the on-premise model
**When** the templates are drafted
**Then** they reflect no vendor access to customer data by default, remote support only by invitation, and the licence terms. They are marked "for legal review"

### Story 14.7: Support SLA definition

As a bank operations manager,
I want a support SLA,
So that I know response times.

**Acceptance Criteria:**

**Given** the support model (remote by invitation and on-site)
**When** the SLA is drafted
**Then** it defines severity levels, response and resolution targets, the escalation path, the update cadence and the bank's responsibilities

### Story 14.8: User, admin and training materials

As a bank trainer,
I want role-based guides and training,
So that staff can use the product correctly.

**Acceptance Criteria:**

**Given** the R2 features
**When** materials are produced
**Then** there are a user guide per role (RM, Credit Officer, Approver, Risk Manager/CRO, Model Validator, Auditor), an admin/installation guide and a training deck with exercises on the Demo Tenant

### Story 14.9: Pilot parallel-run playbook

As a pilot lead,
I want a parallel-run playbook,
So that the pilot proves value objectively (PRD §8, SM-1..SM-4).

**Acceptance Criteria:**

**Given** the success metrics
**When** the playbook is written
**Then** it defines data needed, back-test method on historical applications, live parallel scoring, comparison metrics (defaults, approvals at equal risk, decision time, ROI), sign-off criteria and the go-live-by-segment steps

## Epic 15: Early Warning & Behavioural Risk Signals [R3]

**Squad:** ML & Analytics. **Depends on:** Epics 4, 7, 11, 13.
Goal: the Nightly Run produces the morning risk pack with Watch-list, Lifestyle Mismatch, profession/industry decline and De-risking Recommendations.

### Story 15.1: Morning risk pack and portfolio dashboard

As a CRO,
I want the Nightly Run to publish a morning risk pack on a dashboard,
So that I see what changed overnight (FR-44 full, UX-DR4, UJ-3).

**Acceptance Criteria:**

**Given** a completed Nightly Run
**When** the Portfolio Dashboard opens
**Then** it shows new Watch-list entries, Lifestyle Mismatch alerts, the De-risking queue, Grade migration summary and the "as of" date
**And** each item links to the Customer or obligor view with triggering signals

### Story 15.2: Early-warning Watch-list

As a risk manager,
I want accounts flagged before delinquency,
So that I can act early (FR-47).

**Acceptance Criteria:**

**Given** configurable thresholds
**When** the Nightly Run evaluates signals
**Then** accounts are flagged for:
- Grade migration ≥ 2 notches
- salary delays or irregularity
- utilisation or cash-advance spikes
- spending-habit change
- declining profession or industry
**And** each flag lists its signals, and backtesting on synthetic data shows flagged accounts default at ≥ 2× the Book rate (test)

### Story 15.3: Lifestyle Mismatch detection

As a risk manager,
I want spending inconsistent with income detected,
So that hidden over-indebtedness is caught (FR-48).

**Acceptance Criteria:**

**Given** 12 months of salary credits and transactions
**When** detection runs
**Then** it flags:
- spending above salary credits for N consecutive months (default 3)
- sudden large purchases vs the customer's own history (e.g. car or luxury MCC > 3× personal median)
- spend far above peers in the same salary band and profession
- spending funded by unexplained inflows, tagged "refer to compliance" (no AML investigation)
**And** unit tests cover each rule on fixtures

### Story 15.4: Profession and industry decline signals

As a risk manager,
I want declining professions and industries maintained and learned,
So that structural decline feeds early warning and stress (FR-49).

**Acceptance Criteria:**

**Given** a Tenant table of declining professions/industries with risk adjustments (editable via ChangeRequest)
**When** the Nightly Run executes
**Then** table adjustments apply, and learned signals of rising default rates by profession or sector in the Book are reported with statistical significance

### Story 15.5: De-risking Recommendations

As a risk manager,
I want recommended actions for high-risk existing accounts,
So that exposure is reduced deliberately (FR-50).

**Acceptance Criteria:**

**Given** high-risk accounts (Grade ≥ configured threshold or Watch-list)
**When** recommendations are generated
**Then** retail accounts get "reduce unused card/overdraft limit to X", and corporate obligors get "tighten collateral/covenants", in a queue for human action
**And** the system never changes limits in T24 (no write path exists, test)

## Epic 16: Growth: Opportunity Finder, Pre-approved Offers & Pricing [R3]

**Squad:** ML & Analytics + Frontend. **Depends on:** Epics 4, 11, 13, 15.
Goal: the bank sees good business its policy blocks, proactive offers for safe customers, and risk-based profit-rate guidance.

### Story 16.1: Opportunity Finder analysis

As a CRO,
I want customers declined or restricted by policy but with PD within appetite identified,
So that I know what good business the policy blocks (FR-46).

**Acceptance Criteria:**

**Given** past rejected applications and the current Book
**When** the analysis runs
**Then** cases are grouped by the responsible Rule or restriction, with count, total AED value and average PD
**And** each restriction (e.g. restricted nationality list) shows its "cost" in AED

### Story 16.2: Opportunity Finder screen

As management,
I want the opportunity results visualised and exportable,
So that policy discussions are evidence-based (FR-46, UX-DR5).

**Acceptance Criteria:**

**Given** analysis results
**When** the screen opens
**Then** restrictions are ranked by blocked AED value with drill-down to anonymised cases, and "send to What-if" pre-fills a scenario

### Story 16.3: Pre-approved Offers and card limit increases

As a relationship manager,
I want safe proactive offers for existing customers,
So that I can grow the relationship (FR-51).

**Acceptance Criteria:**

**Given** eligible existing Customers
**When** offers are computed nightly
**Then** each offer has a Recommended Limit via the standard limit logic, and card-limit increases carry the "express customer consent required" flag
**And** customers with a recent Watch-list flag or Lifestyle Mismatch are excluded (test)

### Story 16.4: Risk-based profit-rate suggestion

As a pricing manager,
I want a suggested profit rate per Grade and product,
So that pricing reflects risk (FR-36).

**Acceptance Criteria:**

**Given** the Tenant pricing grid and LGD assumptions
**When** an assessment is made
**Then** the advisory profit rate and the expected-loss cover it provides are shown, labelled advisory, with no effect on the Recommendation

## Epic 17: Portfolio Concentrations & Stress Tests [R3]

**Squad:** ML & Analytics. **Depends on:** Epics 4, 9, 13, 15.
Goal: concentrations (including hidden links) and stress scenarios are visible to the CRO.

### Story 17.1: Concentration views

As a CRO,
I want exposure by employer, sector, product and Grade against thresholds,
So that concentrations are controlled (FR-52).

**Acceptance Criteria:**

**Given** Tenant concentration thresholds
**When** the Nightly Run completes
**Then** concentration tables and charts show exposure and share, with breaches highlighted and listed on the dashboard

### Story 17.2: Hidden-link clustering

As a CRO,
I want hidden links between borrowers found,
So that disguised concentration is revealed (FR-52).

**Acceptance Criteria:**

**Given** shared attributes (employer, owner, supplier, landlord, address, guarantor)
**When** clustering runs
**Then** clusters above a configurable size or exposure are listed with their linking attributes
**And** a synthetic planted cluster is detected (test)

### Story 17.3: Stress-test engine

As a risk manager,
I want portfolio stress scenarios run on the Book,
So that I know how risk moves under shocks (FR-53).

**Acceptance Criteria:**

**Given** scenarios:
- income −20%
- job loss / sector layoffs
- profit rate +2%
- oil/macro shock
- declining professions/industries
- spending-habit shift
**When** a scenario runs (worker job)
**Then** the results report DBR breaches, Grade migration, PD and portfolio expected-loss change (using Tenant LGD)
**And** nationality-based scenarios are not available (test asserts no nationality parameter)

### Story 17.4: Stress-test screen

As a CRO,
I want to configure and compare scenarios,
So that I can brief management (FR-53).

**Acceptance Criteria:**

**Given** stress results
**When** the screen opens
**Then** scenarios can be parameterised, run and compared side by side, and exported to Excel/PDF

## Epic 18: What-if Simulator & KPI/ROI Dashboard [R3]

**Squad:** Decision Core + Frontend. **Depends on:** Epics 2, 4, 13, 16.
Goal: the CRO tests policy changes before adopting them, and management sees approvals, risk and income in AED.

### Story 18.1: What-if engine

As a CRO,
I want to re-run past applications and the Book under a modified policy,
So that I know the impact before changing policy (FR-54).

**Acceptance Criteria:**

**Given** a cloned Policy Version with changed parameters (e.g. DBR 45% for private-sector expats)
**When** the simulation runs
**Then** it reports the change in approval rate, expected loss (PD × Tenant LGD × exposure) and income/ROI vs the active version
**And** it is restricted to Risk Manager and CRO roles (permission test)

### Story 18.2: What-if screen and submission

As a CRO,
I want to edit, compare and submit a scenario as a ChangeRequest,
So that simulation flows into governance (FR-54, UX-DR11, UJ-4).

**Acceptance Criteria:**

**Given** a completed simulation
**When** the CRO clicks "Propose change"
**Then** a policy ChangeRequest is created with the diff and the simulation results attached, requiring a different checker

### Story 18.3: ROI assumptions configuration

As a finance manager,
I want to enter funding cost, profit-rate grids and LGD per product,
So that ROI figures use the bank's numbers (FR-55, K1/K2).

**Acceptance Criteria:**

**Given** default assumptions shipped with the product
**When** the bank enters its own values (via ChangeRequest)
**Then** all ROI, expected-loss and simulator figures use them, and the dashboard shows whether defaults or bank values are in use

### Story 18.4: KPI & ROI Dashboard

As the CEO,
I want approvals, risk and income uplift in one view,
So that I see the business value in AED (FR-55, UX-DR5, UJ-7).

**Acceptance Criteria:**

**Given** decision and outcome history
**When** the dashboard opens
**Then** it shows approval rate, Grade mix, defaults by vintage, override rate, Opportunity Finder value and estimated income uplift in AED
**And** late-payment charity amounts are excluded from income (test)

## Epic 19: Portfolio Assistant [R3]

**Squad:** AI/LLM. **Depends on:** Epics 12, 15–18.
Goal: risk managers ask questions about the portfolio in English or Arabic. The assistant acts only on Safe Actions and routes anything else to maker-checker.

### Story 19.1: Assistant query tools over portfolio data

As a risk manager,
I want to ask questions in plain English or Arabic and get answers with tables,
So that analysis takes seconds (FR-56, UJ-3).

**Acceptance Criteria:**

**Given** a tool set of read-only, Tenant-scoped, parameterised queries (no free SQL)
**When** a user asks "which employers drove the increase in Grades 8–10 this month?"
**Then** the answer cites the tool calls and data used, with numbers guardrailed against the tool results (FR-41 reuse)

### Story 19.2: Safe Actions and ChangeRequest routing

As a CRO,
I want the assistant to act directly only on Safe Actions,
So that it can never change policy, decisions or models by itself (FR-56, AD-7).

**Acceptance Criteria:**

**Given** a request to run a report, what-if, re-score or filter
**When** the assistant handles it
**Then** it executes directly and logs the action
**And** a request to change a Rule, decision or model creates a ChangeRequest draft and does not apply it (test for each forbidden type)

### Story 19.3: Assistant UI and audit

As an auditor,
I want every assistant conversation and action recorded,
So that its use is accountable (FR-56, NFR-5).

**Acceptance Criteria:**

**Given** the assistant panel in the web app (Risk Manager and CRO roles only)
**When** a user converses
**Then** prompts, tool calls, answers and actions are stored in the audit log, with PII excluded from prompts

## Epic 20: Agentic Annual Review & Advanced Integrations [R3]

**Squad:** AI/LLM + Data & Integrations. **Depends on:** Epics 6, 7, 9, 10, 11, 12.
Goal: basic agentic annual reviews for corporate obligors, learning from overrides, the optional AECB API, and Oracle support.

### Story 20.1: Agentic annual review (basic)

As a corporate analyst,
I want obligors due for review prepared automatically,
So that annual reviews take days, not weeks (FR-65).

**Acceptance Criteria:**

**Given** obligors with a review due date within 30 days
**When** the review agent runs (worker)
**Then** it assembles the latest confirmed spreads, re-rates the obligor, flags changes since the last review, and drafts the review paper (guardrailed)
**And** the paper stays in draft until an analyst approves it, and missing financials are flagged rather than estimated

### Story 20.2: Learning from overrides

As a model developer,
I want override outcomes available as features or labels,
So that officer judgement improves the model (FR-38 R3).

**Acceptance Criteria:**

**Given** overrides with recorded outcomes
**When** the training dataset is built
**Then** override indicators and outcomes are included as documented features or labels, and their effect is reported in the model card

### Story 20.3: Optional AECB API connector

As bank IT,
I want an optional direct AECB API connector, off by default,
So that bureau data can be pulled in real time where the bank permits (FR-16 R3, NFR-3).

**Acceptance Criteria:**

**Given** the connector disabled by default
**When** an admin enables it via ChangeRequest and adds the AECB endpoint to the egress allow-list
**Then** bureau pulls require recorded customer consent, are logged, and are the only outbound customer-data flow (egress test)

### Story 20.4: Oracle database support

As bank IT,
I want Oracle supported as the application and source database,
So that Oracle-standard banks can deploy (AD-13).

**Acceptance Criteria:**

**Given** the CI matrix extended with an Oracle container
**When** migrations, repository and source-connector tests run
**Then** they pass on Oracle 19c+ as on PostgreSQL and SQL Server
