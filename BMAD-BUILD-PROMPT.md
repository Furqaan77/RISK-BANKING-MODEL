# BMAD BUILD PROMPT: AI Risk Score Card

> **What this is:** the single entry point for building **AI Risk Score Card** with the **BMAD Method (v6)** on a separate
> build machine. It tells the development team (6+ developers in squads, each working with Claude Code or another coding
> agent) exactly how to go from the finished plan to working, tested software, release by release.
>
> **Planning is complete.** Discovery (104 questions), product brief, PRD, architecture and epics & stories are done. **Do not
> re-plan.** Validate the plan, then build.
>
> **How to start (any team member, in Claude Code at the repo root):**
> `Read BMAD-BUILD-PROMPT.md and run Phase 0.` Then work through the phases in order. Each phase lists its BMAD skill calls.

---

## 1. What is in this folder (read in this order)

| # | File | Role | Authority |
|---|---|---|---|
| 1 | `_bmad-output/planning-artifacts/prd.md` | Requirements FR-1..FR-66, NFR-1..NFR-12, Glossary, release mapping | **Source of truth for WHAT** |
| 2 | `_bmad-output/planning-artifacts/architecture.md` | Paradigm, invariants AD-1..AD-16, conventions, stack, structure | **Source of truth for HOW** |
| 3 | `_bmad-output/planning-artifacts/epics.md` | Epics & stories by release, with acceptance criteria and FR coverage | **Source of truth for WORK ORDER** |
| 4 | `_bmad-output/planning-artifacts/product-brief.md` | Why, who, differentiation, vision | Context |
| 5 | `_bmad-output/planning-artifacts/discovery-answers.md` | Every product-owner decision, with reasons | Tie-breaker for intent |
| 6 | `docs/regulatory/cbuae-rules.md` | CBUAE rules with sources and confidence levels | Source for the CBUAE Layer |
| 7 | `research/` | Call transcript, whiteboard, corporate credit framework, AI-in-risk research | Background only |
| 8 | `AI Risk Score Card - Plan for Bank Leadership.pdf` | Banker-facing explanation (non-technical) | Must stay consistent with the build |
| 9 | `archive/` | Superseded v1 prompt and PDF | **Do not build from these** |

**Conflict rule:** PRD > architecture > epics > brief > discovery answers > research. If two sources conflict, stop and raise it
with the product owner (§7). Never silently pick one.

## 2. The product in one paragraph

An on-premise AI credit-risk engine for **Islamic banks in the UAE**. It assesses every **Finance Application** in real time (via a
Temenos T24/Transact API) and the whole **Book** nightly (via read-only database views). Every case is checked against three **Policy Layers**:
**CBUAE** → **Bank Policy** → **Credit Policy**. The output is a **Risk Grade 1–10**, a 12-month **PD**, a **Recommendation** (Approve /
Refer / Decline: policy always wins, and the model can only escalate a pass to Refer), a **Recommended Limit** with its Binding Constraint, and
English/Arabic **Explanations**. Around this sit an approval workflow, a nightly early-warning and opportunity analysis, a
what-if simulator, a KPI/ROI dashboard and a local-LLM Portfolio Assistant. Multi-tenant (one schema per bank), air-gapped capable,
licensed per bank.
**Principle:** *AI recommends, scores, drafts and flags; bank staff decide and are accountable.*

## 3. Non-negotiables (every story, every PR)

1. **Data never leaves the bank.** Egress is denied by default (AD-11). No CDNs or telemetry at runtime. Optional AECB API only when switched on by an admin.
2. **Deterministic decision core** (AD-1): `assess(snapshot, policy_version, model_version, params)` is pure. **No LLM, I/O or clock in `app/core`.** Every Decision Record replays identically (AD-9).
3. **CBUAE is tighten-only** (AD-3). Bank or credit policy can never loosen a CBUAE Rule, and CBUAE Rules can never be deviated.
4. **Policy is data**, evaluated by the allow-listed expression evaluator. **Never `eval`.**
5. **Maker-checker** for policy, deviation matrix, model activation, regulator pack and assistant change actions (AD-7). Checker ≠ maker, enforced in code and in the DB.
6. **LLM is advisory only** (AD-6). It sees only facts JSON. The number/Rule guardrail is mandatory, with template fallback. Drafts need human sign-off. AI text is internal only.
7. **Tenant isolation**: schema per Tenant (AD-2). Cross-tenant access is a release-blocking bug.
8. **PII is pseudonymised at ingestion** (AD-10). Never write PII to logs or LLM prompts.
9. **Islamic vocabulary only** (AD-12): finance amount, profit rate, finance application, obligor. "loan" and "interest" are lint errors.
10. **Fairness**: nationality, gender, marital status and religion are never Learning Model features. Age is allowed.
11. **Money in integer fils, never floats.** UTC storage. UUIDv7 ids. Error envelope per AD-14.
12. **No customer-data file upload.** Data comes via the T24 API, read-only DB views, or the demo DB. The only uploads are policy documents and corporate PDF statements.

## 4. Agreed defaults (configurable per Tenant; the demo uses these)

| Item | Default |
|---|---|
| Risk Grades (PD bands, 12-month) | 1 <0.25% · 2 0.25–0.5% · 3 0.5–1% · 4 1–2% · 5 2–3.5% · 6 3.5–5% · 7 5–8% · 8 8–12% · 9 12–20% · 10 ≥20% |
| Model escalation | Policy pass and Grade ≥ 7 → Refer |
| Default definition | 90+ DPD within 12 months |
| DBR Income | Basic salary + housing allowance. Card obligation = 5% of limit. Profit-rate stress add-on 0 |
| CBUAE retail | Personal finance ≤ 20× income, ≤ 48 months. DBR ≤ 50% (retirees 30%). Auto ≤ 80% / 60 months. Ijara LTV per `cbuae-rules.md` A.7, ≤ 25 yrs |
| Bank caps | Total Unsecured Cap 20× income. Ages 21 min; 65 (expat) / 70 (national) at maturity. EOSB finance after ≥ 5 yrs, ≤ 80% of EOSB. Restricted nationality → Refer |
| Corporate | Weights 35/20/15/10/20. EBITDA −30% stress. Large exposure ≤ 25% of Tier 1 (other limits per A.3). Thresholds empty until the bank supplies them |
| Learning Model | LightGBM. Gate: ≥ 1,000 rows, ≥ 50 defaults, out-of-time Gini ≥ 0.30, plus validator approval. Drift PSI > 0.25 → auto-retrain challenger. Breach → auto-suspend → Scorecard |
| Performance | Real-time p95 ≤ 2 s (no LLM). Nightly 100k Customers + 5k Obligors ≤ 2 h |
| Golden test | Expat govt employee, basic+housing AED 18,000; obligations AED 3,000 + card 20,000 (5% = 1,000); Tawarruq AED 400,000 / 48 m / 6% → **DBR binds → Approve AED 212,000** (instalment ≈ AED 4,979, DBR ≈ 49.9%) |

## 5. Build-machine setup (Phase 0)

**Prerequisites:** Git, Node.js ≥ 20 (for the BMAD installer), Python 3.12, `uv`, Docker + Docker Compose, Claude Code. An NVIDIA GPU is
optional for LLM work (CPU-only works with template explanations).

1. Create the private GitHub repo `ai-risk-score-card`. Copy this whole folder in, including `_bmad/`, `.claude/skills/` and `_bmad-output/`. Commit on `main`, then branch.
2. If `_bmad/` is missing or broken, reinstall BMAD:
   `npx bmad-method@6.12.4 install --directory . --modules bmm --tools claude-code --set core.project_name="AI Risk Score Card" -y`
   (it keeps `_bmad-output/`). Set your name: `--user-name "<name>"`.
3. Run the skill **`bmad-help`** to confirm BMAD sees the planning artifacts and recommends the next step.
4. Record the machine environment (OS, Python, Node, Docker, GPU/VRAM) in `docs/environment.md`. **Do not assume hardware.** Choose the LLM size from the detected VRAM (≥ 24 GB → 14B-class Qwen; 8–16 GB → 7–8B Qwen/Llama; none → templates only).

## 6. BMAD phases

### Phase 1: Validate the plan (one person, ~1 day)
- **`bmad-prd`** → *validate* `prd.md`. Fix gaps in place. Do not change product decisions without the product owner.
- **`bmad-architecture`** → *validate* `architecture.md`. **Verify and pin current stable versions** of every stack item, and update the Stack table.
- **`bmad-sprint-planning`** → *"check implementation readiness"*. All FRs must be covered by stories and no story may depend forward. Resolve findings.
- ⛔ **Checkpoint:** product owner reviews the validation findings.

### Phase 2: Agent context (one person, ~½ day)
- **`bmad-project-context`** → create `AGENTS.md` (and the Claude Code project instructions) containing: §3 non-negotiables, the Glossary vocabulary
  rule, AD-1..AD-16 one-liners, conventions, test commands, and "PRD > architecture > epics" precedence. Every agent reads this first.

### Phase 3: Sprint planning
- **`bmad-sprint-planning`** → *generate* `_bmad-output/implementation-artifacts/sprint-status.yaml` from `epics.md`.
- Assign epics to squads by the squad focus noted on each epic (Platform, Decision Core, Data & Integrations, ML & Analytics, Frontend, AI/LLM).
  Respect epic dependencies. Use 2-week sprints.

### Phase 4: Build loop (every developer, per story)
For each story taken from `sprint-status.yaml`:
1. **`bmad-build`** with the story id (e.g. `story 3.2`). It clarifies, plans, implements test-first, self-reviews and updates sprint status.
2. **`bmad-code-review`** on the branch (parallel reviewers). Fix findings.
3. Open a PR. CI must pass: ruff, mypy, pytest (unit, property, contract), front-end lint and tests, Bandit, dependency audit, the "no loan/interest" lint, and the tenant-isolation scan.
4. A second developer approves the PR (human review). Merge.
- After each feature area: **`bmad-qa-generate-e2e-tests`** for its user journeys (UJ-1..UJ-8) → Playwright suite.
- End of each epic: **`bmad-retrospective`**.
- Any scope or requirement change: **`bmad-correct-course`** (updates PRD, architecture and epics consistently). Never patch requirements ad hoc.
- Unattended overnight runs (optional): **`bmad-build-auto`**, one iteration per story, only for stories marked low-risk, with human review the next day.

### Phase 5: Release gates
| Release | Gate (all must pass) |
|---|---|
| **R1 Demo MVP** | A retail applicant scored end-to-end on the Demo Islamic Bank (CBUAE + demo policy + Scorecard → Grade, PD, Recommendation, limit, template Explanation). Decision screen with drill-down. Risk ranking of the book. Golden test passes. Tighten-only, evaluator-safety, replay and tenant-isolation tests pass. `docker compose up` on a clean machine works with networking disabled |
| **R2 Pilot-ready** | Corporate & SME + Document AI. Approval workflow with AD/SSO and the deviation matrix. T24 adapter + read-only DB connector (against a T24-like test harness). Learning Model with gate, drift, auto-suspend and validation pack. LLM Explanations/memos (EN+AR) with guardrail. Policy extraction from documents. Windows installer. Licence. NFR-1 met in k6. Security tests clean |
| **R3 Full v1** | Nightly Run with Watch-list, Lifestyle Mismatch, De-risking, Pre-approved Offers, card limit increases, Opportunity Finder, concentrations & hidden links, stress tests. What-if Simulator. KPI/ROI dashboard. Portfolio Assistant (safe actions only). Risk-based profit rate. Agentic annual review (basic). NFR-2 met. Onboarding packs, guides and templates delivered |

⛔ **Checkpoint at every release:** demo to the product owner. Update the banker PDF if anything it states has changed.

### Phase 6: Pilot preparation (after R2)
Parallel run at the pilot Islamic bank. Install on the bank's server and connect T24/DWH read-only. Load the bank's real Credit Policy through
FR-4/FR-5 with credit-team maker-checker. Train the Learning Model on the bank's 1–2 years of history (including rejected applications). Score
historical and live applications alongside the existing process. Report against SM-1..SM-8.

## 7. Stop and ask the product owner when…
- Two artifacts conflict, or a story needs a decision not covered by the PRD or discovery answers.
- A CBUAE value marked below **H** confidence affects a gate (see `cbuae-rules.md` A.6). Verify it manually in a browser on rulebook.centralbank.ae.
- Anything would send data outside the bank, put the LLM in a decision path, loosen a CBUAE Rule, or add non-Islamic wording.
- Any change to grades, PD bands, the escalation grade, or the default definition.

## 8. Still pending from the client (do not invent; use demo defaults until received)
1. Pilot bank identity, T24 version and integration method.
2. The bank's Credit Policy manual + parameter sheet, deviation/authority matrix, and corporate thresholds.
3. The bank's score scale and PD bands. LGD, funding cost and profit-rate grids for ROI.
4. Approved-employer / blue-chip lists and the restricted-nationality list.
5. Tier 1 capital (large exposures). GPU size of the pilot server.
6. An anonymised real data sample (if obtainable) to validate the Data Field Template.
7. Pricing model (commercial, outside the build).

## 9. Definition of Done (every story)
Acceptance criteria met and demonstrated. Tests written first and passing (unit/property for maths and rules, contract for ports, E2E where a
journey changes). Glossary vocabulary used. No PII in logs. Audit events written for every write action. OpenAPI updated and the client
regenerated. Docs updated (`docs/`). The CHANGELOG entry references the FR/NFR/AD ids. Code-reviewed by `bmad-code-review` + one human. Merged
with green CI.
