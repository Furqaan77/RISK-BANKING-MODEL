# BMAD BUILD PROMPT: AI Risk Score Card Global (large US + UK banks)

> **What this is:** the entry point for building **AI Risk Score Card Global** with the **BMAD Method (v6)**. It is a **separate
> product** from the UAE Islamic edition (`BMAD-BUILD-PROMPT.md`). Build it in its **own repository**.
>
> **Planning is complete** (24 discovery rounds, product brief, PRD, architecture, epics). **Do not re-plan.** Validate, then build.
>
> **Start:** in Claude Code at the new repo root, say `Read BMAD-BUILD-PROMPT-GLOBAL.md and run Phase 0.`

---

## 1. Files to copy into the new repo and how BMAD finds them

| Source in this folder | Put in the new repo at | Role |
|---|---|---|
| `_bmad-output/large-bank/planning-artifacts/prd.md` | `_bmad-output/planning-artifacts/prd.md` | **WHAT**: FR-1..86, NFR-1..9 |
| `_bmad-output/large-bank/planning-artifacts/income-segmentation-spec.md` | `_bmad-output/planning-artifacts/income-segmentation-spec.md` | Income segments S0–S5, overlay tags, segment policy matrix (FR-79..86) |
| `_bmad-output/large-bank/planning-artifacts/architecture.md` | `_bmad-output/planning-artifacts/architecture.md` | **HOW**: AD-1..16, stack, structure |
| `_bmad-output/large-bank/planning-artifacts/epics.md` | `_bmad-output/planning-artifacts/epics.md` | **WORK ORDER**: epics & stories R1–R4 |
| `_bmad-output/large-bank/planning-artifacts/product-brief.md` | `_bmad-output/planning-artifacts/product-brief.md` | Context |
| `_bmad-output/large-bank/planning-artifacts/discovery-answers.md` | `_bmad-output/planning-artifacts/discovery-answers.md` | Intent tie-breaker, worked examples |
| `_bmad-output/large-bank/planning-artifacts/jurisdiction-comparison.md` | `docs/regulatory/jurisdiction-comparison.md` | US vs UK rationale |
| `docs/regulatory/large-bank/us-federal-and-new-york.md` | `docs/regulatory/us-pack.md` | **US pack source** |
| `docs/regulatory/large-bank/uk-prudential-and-conduct.md` | `docs/regulatory/uk-pack.md` | **UK pack source** |
| `research/` | `research/` | Background |
| `AI Risk Score Card Global - Plan for Bank Leadership.pdf` | `docs/` | Banker view (keep consistent) |

Precedence: **PRD > architecture > epics > brief > discovery > research.** Raise conflicts with the product owner; never pick silently.

## 2. Product in one paragraph
On-premise AI credit-risk platform for large US and UK banks, deployed as **separate US and UK installs**. Headline: **"Better than your
champion model"**. It runs as challenger, as a scoring add-on to the bank's decision engine, or as a full engine. It assesses cards,
loans, salary advances, mortgages, SME and corporate lending (auto, UK overdrafts and UK BNPL in R4). Every case gets:
- regulator-pack + bank-policy rules
- UK two-limb affordability / US ability-to-pay
- PD/LGD/EAD/EL on the bank master scale
- deterministic reason codes
- TTC and daily PIT scores

Twelve value-added services surround this: inclusion, Gen Z readiness and loyalty, product designer, next-best-offer, frontier,
macro/climate stress, early warning, fairness/LDA, validator in a box, collections cure, document AI, fraud consistency, notices, and
policy copilot.

**Principle:** *AI recommends; the bank sets where automation is allowed; people stay accountable.*

## 3. Non-negotiables (every story, every PR)
1. **Separate US and UK installs.** No shared DB, registry, or cross-install calls (AD-3). Deny-by-default egress; air-gap capable (AD-14).
2. **Pure deterministic core and exact replay** (AD-1, AD-11). No LLM, I/O or clock in `core`.
3. **Packs are signed, effective-dated, tighten-only** (AD-2). Values below H confidence are flagged for verification.
4. **Two-limb assessment.** No score overrides a failed affordability or ability-to-pay result (AD-5).
5. **Reasons are deterministic** (≤ 4 for US notices; bureau key factors kept separate). **The LLM never chooses reasons or decides** (AD-6).
6. **Never auto-decline.** Automation is bank-configured. Mortgages and commercial are human in the demo. UK Art 22C safeguards apply (AD-7).
7. **Protected data only in the fairness zone.** Models can't read it (AD-9). US 62+ never scored negatively; UK age only with justification; proxies blocked.
8. **Tokenise PII at ingestion.** Keys stay in the bank HSM/vault. Consent revocation stops use (AD-10).
9. **No credit to minors.** Readiness only for ages 16–17. No marketing profiling or credit promotion to minors.
10. **Bank MRM approval before any model serves.** Drift → challenger retrain only. Breach → auto-suspend with fallback (AD-8).
11. **Online/batch feature parity.** Single feature definition, with a parity test in CI (AD-4).
12. **Latency budget.** p95 < 300 ms on the real-time path (AD-12). Nightly 50M+ within the window.
13. **Fraud:** flags only. **Notices:** content only (the bank sends).
14. **Money in minor units; Decimal rates; UUIDv7; error envelope** (conventions table in architecture).

## 4. Agreed defaults (demo; configurable per bank)
| Item | Default |
|---|---|
| Master scale | 20 grades; upper PD bounds % 0.03, 0.05, 0.08, 0.12, 0.18, 0.26, 0.38, 0.55, 0.8, 1.15, 1.65, 2.4, 3.4, 4.9, 7, 10, 14, 20, 30, 100 |
| Automation | Auto-approve starter cards and salary advances ≤ $/£1,000 at grade ≤ 12; auto CLI after fresh affordability; never auto-decline; mortgages & commercial human |
| Starter card | UK £250–£1,000 / US $300–$1,500; reviews at 6 and 12 months with fresh affordability |
| Salary advance | Salary credited ≥ 3 months; ≤ 50% of net pay; one at a time; blocked in persistent debt/difficulty; pricing from bank (HCSTC/MLA/state gates) |
| Readiness | Ages 16–17 only; habits + education signals; offer at 18 after affordability; US authorised-user path if the bank allows |
| Corporate | 5 dimensions 35/20/15/10/20; leveraged review flag at debt/EBITDA > 6x |
| Income segments | Verified gross income → S0 none · S1 <$30k/<£20k · S2 $30–60k/£20–35k · S3 $60–120k/£35–60k · S4 $120–250k/£60–100k · S5 $250k+/£100k+; overlay tags GENZ, THIN_FILE, GIG_SELF_EMPLOYED, RETIREE, NEW_TO_COUNTRY, UNDER_18_READINESS; card residual floor $300/£100; loan/mortgage residual floors and caps per `income-segmentation-spec.md` §2; re-segment up after 2 months, down after 3 |
| Packs | Values from `docs/regulatory/us-pack.md` and `uk-pack.md` (QM 2026 tables, MLA 36%, SCRA 6%, NY 16%/25%, SCCL 25/15, LLL 15+10, CONC 5.2A, MCOB +1pp/5y, persistent debt 18/27/36 £200, LE 25/15, UK retail default £0/0%) |
| Golden tests | **Maria (NY):** residual $560; min payment $150 at $5,000 → ATP pass; PD 3.1% grade 13; recommend $1,500 starter; human review. **Tom (London):** disposable £495; £1,000/36m @ 29.9% ≈ £42/m → PASS; PD 2.2% grade 12; auto-approved with Art 22C info |
| Performance | Real-time p95 < 300 ms; nightly 50M+ ≤ 4 h |

## 5. Team, timeline and priority (read carefully)
- **Team:** 14–18 people in squads: Platform/DevOps, US Pack, UK Pack, Models & ML, Data Engineering, Frontend, AI/LLM, QA (+ PM/architect).
- **Product-owner target:** all of v1 in **2–3 months** (6 two-week sprints). This is **high risk**. Rules:
  - Build in priority order **R1 → R2 → R3 → R4**. Squads may start later-release epics only when no R1 story is blocked.
  - Each epic marks a **must-ship** subset. Protect it first.
  - Re-forecast at the end of sprint 2 using real velocity from `sprint-status.yaml`. Report the forecast to the product owner honestly, including what will not fit.
- Bank vendor onboarding (12–24 months) runs in parallel. Fast building does not shorten it, so start the compliance packs early (epic for governance documents).

## 6. Setup (Phase 0)
Prerequisites: Git, Node.js ≥ 20, Python 3.12, `uv`, Docker, kind/minikube or a dev Kubernetes, Java 17 (Spark), Claude Code. GPU optional.
1. Create a private GitHub repo `ai-risk-score-card-global`. Copy the files per §1.
2. Install BMAD: `npx bmad-method@6.12.4 install --directory . --modules bmm --tools claude-code --set core.project_name="AI Risk Score Card Global" -y`
3. Run **`bmad-help`** to confirm BMAD sees the planning artifacts.
4. Record the environment in `docs/environment.md`. Do not assume hardware.

## 7. BMAD phases
**Phase 1: Validate (~2 days, PM + architect)**
- `bmad-prd` → validate `prd.md`. `bmad-architecture` → validate and **pin current versions**. `bmad-sprint-planning` → "check implementation readiness".
- ⛔ The product owner reviews the findings.

**Phase 2: Agent context**
- `bmad-project-context` → `AGENTS.md` containing §3 non-negotiables, AD one-liners, conventions, test commands and the precedence rule.

**Phase 3: Sprint planning**
- `bmad-sprint-planning` → generate `sprint-status.yaml`. Assign epics to squads by the squad tag on each epic. Use 2-week sprints.

**Phase 4: Build loop (per story)**
1. `bmad-build <story>` (test-first).
2. `bmad-code-review`.
3. PR with CI green. CI runs: unit/property, the regulatory suite for each rule id touched, fairness suite (model stories), online/batch parity, security scans and SBOM, and k6 smoke for API stories.
4. One human approval. Merge.
- Per feature area: `bmad-qa-generate-e2e-tests` for the UJ-1..8 journeys.
- Per epic: `bmad-retrospective`.
- Scope or requirement changes go through `bmad-correct-course` only.

**Phase 5: Release gates**
| Release | Gate |
|---|---|
| **R1 Challenger MVP** | Cards + loans/advance scored in US and UK installs; income segments S0–S5 + overlay tags + segment policy applied (Epic 29 must-ship); UK affordability + US ability-to-pay; PD/LGD/EAD/EL; reasons; Maria & Tom & US S3 loan golden tests pass; champion-vs-challenger report on Demo US (2M) / UK (1M) banks + public datasets; frontier v1; never-auto-decline, tighten-only, replay, parity tests pass; p95 < 300 ms in k6 |
| **R2 Pilot-ready** | Mortgages (ATR/QM + HMDA; MCOB 11.6 + LTI); SME & corporate with exposure limits; batch 50M+ (scaled test); Kafka early warning; bureau/Open Banking adapters; notices (EN/ES/CY); Art 22C workflow; CO/CA ADMT; SSO + workflow; model lifecycle; LLM explanations/letters with guardrail; governance packs; licence + usage export |
| **R3 Growth & macro** | Inclusion engine; Gen Z readiness & loyalty; credit-builder & student offers; product designer; NBO/CLV; frontier with recommended policy; scenario & climate engine; sector/job-loss warning; fairness/LDA (US) and Equality Act (UK) suites; validator in a box; portfolio chat; board & CRO dashboard |
| **R4 Operations** | Collections cure, forbearance, contact strategy; UK persistent-debt, overdraft, BNPL; auto finance; document AI; credit memos & policy copilot |

⛔ Demo to the product owner at each gate. Update the banker PDF if anything it states changed.

**Phase 6: Pilot**
- Back-test on 3–5 years including rejects.
- 6-month shadow beside the champion.
- Limited live on one segment.
- Report against SM-1..SM-6.

## 8. Stop and ask the product owner when…
- Artifacts conflict, or a decision isn't covered.
- A regulatory value below H confidence affects a gate.
- Anything would: cross installs, send data out, let the LLM decide or pick reasons, auto-decline, profile or market credit to minors, or loosen a pack rule.
- The sprint-2 forecast shows the 2–3 month target won't be met (state what will fit).

## 9. Pending from the client
Pilot bank and its champion and decision engine; master scale and default definitions; LGD/funding/pricing grids; approved LLM platform; bureau and Open Banking contracts; US charter (usury, Part 500 scope); Spanish/Welsh template approval; the unconfirmed items in the pack references.

## 10. Definition of Done (every story)
- Acceptance criteria met.
- Tests first: unit/property, plus regulatory tests by rule id, fairness (models), parity (features), E2E (journeys).
- No PII in logs. Audit events written.
- OpenAPI/gRPC contracts updated.
- Docs updated. CHANGELOG lists FR/NFR/AD ids.
- `bmad-code-review` + one human. CI green.
