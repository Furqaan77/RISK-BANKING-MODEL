---
title: AI Risk Score Card Global
created: 2026-11-07
updated: 2026-11-07
status: final
inputDocuments:
  - _bmad-output/large-bank/planning-artifacts/product-brief.md
  - _bmad-output/large-bank/planning-artifacts/discovery-answers.md
  - _bmad-output/large-bank/planning-artifacts/jurisdiction-comparison.md
  - docs/regulatory/large-bank/us-federal-and-new-york.md
  - docs/regulatory/large-bank/uk-prudential-and-conduct.md
---

# PRD: AI Risk Score Card Global

## 0. Document Purpose
For the development team (14–18 people in parallel squads), the architect, and BMAD downstream skills. It turns the large-bank
discovery (`discovery-answers.md`) into numbered, testable requirements. FRs are numbered globally and tagged **[R1]–[R4]**.
Regulatory values live in the two pack references under `docs/regulatory/large-bank/`. This product is **separate** from the
UAE Islamic edition (own repo, own docs). Its vocabulary is conventional (loan, interest, APR).

## 1. Vision
AI Risk Score Card Global is an on-premise AI credit-risk platform for large US and UK banks. It proves on the bank's own data that
it is **better than the bank's champion model** (more accurate, more approvals at the same loss, fairer, more stable and explainable),
then serves as a challenger, a scoring add-on to the bank's decision engine, or a full decision engine. It covers consumer and
commercial lending in both markets. It adds inclusion for blue-collar, thin-file and Gen Z customers, macro and climate early warning,
and a risk-vs-opportunity view so credit committees see what they gain as well as what they risk.

**Principle (binding):** *AI recommends; the bank sets where automation is allowed; people stay accountable.*

## 2. Target Users

### 2.1 Jobs To Be Done
- **Underwriter / credit officer:** "Give me a sound, explained recommendation; let me act fast on clear cases and spend time on hard ones."
- **Risk strategy / policy:** "Show me which policy gives the best approvals and profit for the loss we accept, and who we are missing."
- **Model risk / validation:** "Prove the model is sound, stable and fair, quickly, and help me validate our own models too."
- **Collections & fraud:** "Tell me who will cure, who needs help, and which applications look inconsistent."
- **CRO / board:** "Show me exposure to recession, war, disaster and climate, and how much better the challenger is."
- **Compliance / DPO / TPRM / InfoSec:** "Show me the notices, the safeguards, the data controls and the evidence."

### 2.2 Non-Users (v1)
Customers directly (the bank sends all communications). Under-18s as borrowers. Fraud investigators as decision-makers (flags only).

### 2.3 Key User Journeys
- **UJ-1. Maria (New York), thin-file, gets a starter card the champion would decline.** Maria, 24, warehouse shift worker with
  weekend delivery gig income, applies for a $5,000 card. The bank's decision engine calls the real-time API (p95 < 300 ms). The
  champion scorecard would decline (thin-file cut-off). The challenger smooths 12 months of cash-flow income ($3,400 net), checks CARD
  Act ability-to-pay (residual $560 vs $150 minimum payment at $5,000) and scores PD 3.1% (master grade 13). Bank starter policy
  caps thin-file at $1,500, so the recommendation is a **$1,500 starter card** with 6/12-month reviews. Above the $1,000 automation line,
  it goes to an underwriter, who approves. If it had been a counteroffer, the notice content (≤4 deterministic reasons, e.g. limited
  credit history, income variability) is generated for the bank's letter system in English or Spanish within the Reg B timer.
- **UJ-2. Tom (London), 19, auto-approved within the bank's rules.** Tom has a readiness record since 17 (junior account habits, no
  credit). At 19, as an apprentice electrician, he applies for a £1,000 starter card. Open Banking verifies £1,650 net income;
  expenditure from actual spend checked against ONS norms leaves £495; repaying £1,000 over 36 months at 29.9% APR ≈ £42/month →
  **affordability PASS**; PD 2.2% (grade 12). The bank allows automation for starter cards ≤ £1,000 at grade ≤ 12, so it is
  auto-approved. Tom receives Art 22C information and can ask for human review.
- **UJ-3. Priya, risk strategy, finds the opportunity.** She opens the **Risk-vs-Opportunity Frontier** for cards: the current policy
  sits inside the frontier. Moving to the recommended point adds 7% approvals (mostly gig workers and graduates) for +0.3% expected loss
  and +£/$ X risk-adjusted profit. She submits it through the **Policy Copilot**, which runs fairness tests, then a checker approves.
- **UJ-4. Daniel, model validation, validates in weeks not months.** He loads the bank's champion scores and outcomes (and the model
  file on-prem). The **Validator in a Box** produces an SR 26-2 / SS1/23 report comparing champion and challenger on accuracy, stability,
  calibration and fairness (AIR, LDA search; UK Equality Act tests in a segregated zone).
- **UJ-5. The CRO sees the hurricane and the recession together.** In the **Board & CRO dashboard**, the scenario "regional hurricane
  + mild recession" shows mortgage collateral in flood and wind zones, an uninsurable-home flag, PD uplift by sector, and loss under
  scenario. The early-warning list shows employers in sanctioned or disrupted sectors.
- **UJ-6. A collections agent helps instead of chasing.** The **cure model** ranks delinquent customers. For a UK card customer at month
  27 of persistent debt, the forbearance recommender proposes a repayment plan within 3–4 years. AI drafts the letter with tone guardrails,
  and the agent approves.
- **UJ-7. A commercial analyst rates a sponsor-backed company.** Document AI reads statements, tax returns and the loan agreement
  (covenants). The sector template rates it, flags debt/EBITDA > 6x for heightened review (Fed SR 13-3), aggregates sponsor and group
  exposure against SCCL / large exposures, and drafts a credit memo.
- **UJ-8. Sales demo.** Demo US Bank (2M accounts) and Demo UK Bank (1M), each with a synthetic champion scorecard to beat and a
  simulated recession and regional disaster in history.

## 3. Glossary
- **Bank / Install**: one client; **separate US and UK installs** (no cross-border data). **Market pack**: the US or UK regulator rule set.
- **Policy Layers**: Regulator pack → Bank policy → Credit policy (tighten-only, as in the UAE edition).
- **Champion**: the bank's current model or score. **Challenger**: our model(s) run beside it.
- **Mode**: *challenger* (shadow only) · *add-on* (bank engine calls our API) · *engine* (full decision engine).
- **Automation rule**: bank-configured condition under which a decision may be made without a person (never for declines, mortgages or commercial in the demo).
- **Assessment**: for consumer credit: **credit-risk outcome** + (UK) **affordability verdict** + (US) **ability-to-pay** result.
- **PD / LGD / EAD / EL**: 12-month probability of default, loss given default, exposure at default, expected loss. **TTC score**: through-the-cycle (decisions). **PIT PD**: point-in-time, macro-adjusted, refreshed daily.
- **Master scale**: the bank's grade scale (demo: 20 grades, upper PD bounds 0.03 … 100%).
- **Reason codes**: deterministic, ranked reasons from the model or rules; the LLM may only paraphrase them.
- **Notice content**: US adverse action / FCRA / risk-based pricing, UK decline + Art 22C information; generated by us, sent by the bank.
- **Frontier**: approvals/balances/profit/inclusion vs expected loss across policy options. **Opportunity-loss segment**: profitable group the current policy declines.
- **Readiness record**: non-credit financial-habit profile for ages 16–17 (no credit, no marketing profiling).
- **Starter card / salary advance / credit-builder**: inclusion products with demo defaults in §4.6.
- **Scenario**: regulator, event, climate (NGFS) or custom macro path.
- **Validator in a Box**: validation evidence generator for our and the bank's models.
- **Income segment (S0–S5)**: band of verified annual gross income that sets eligible products, caps and residual-income floors. **Overlay tag**: attribute (Gen Z, thin file, gig/self-employed, retiree, new to country, under-18 readiness) that changes how a customer is assessed, not the segment. **Residual income**: money left each month after essentials, existing obligations and the new repayment.

## 4. Features

### 4.1 Platform, installs, packs & policy
- **FR-1 [R1]** Separate US and UK installs; multi-entity within an install (bank, card issuer, ring-fenced bank, affiliates) with entity-aware rules.
- **FR-2 [R1]** US pack and UK pack as versioned, effective-dated rule sets with sources and confidence (from the regulatory references); yearly-changing values (e.g. QM thresholds) are dated tables.
- **FR-3 [R1]** Tighten-only validation of bank and credit policy against the pack.
- **FR-4 [R1]** Policy-as-config with maker-checker, immutable versions and back-testing of any version on history.
- **FR-5 [R1]** Three modes (challenger, add-on, engine) selectable per product.
- **FR-6 [R1]** Automation rules per product/amount/grade (demo: auto-approve starter cards and salary advances ≤ $/£1,000 at grade ≤ 12; auto CLI for good accounts after fresh affordability check; **never auto-decline**; mortgages and commercial always human).
- **FR-7 [R1]** Decision record (inputs, pack/policy/model versions, outputs, reasons, user actions), replayable exactly; retention per market (US ≥ 25 months default, configurable to 7+ years; UK term + 6 years with litigation hold).

### 4.2 Data & integration
- **FR-8 [R1]** Real-time scoring API for decision engines (FICO, Experian PowerCurve, SAS, Pega, in-house); p95 < 300 ms (NFR-1).
- **FR-9 [R1]** SFTP/file drop for back-tests and pilots.
- **FR-10 [R2]** Batch read from the bank data platform (Snowflake, Databricks, Teradata, Oracle) for nightly 50M+ accounts (NFR-2).
- **FR-11 [R2]** Kafka event streaming (transactions, payments, account events) for early warning.
- **FR-12 [R2]** Bureau adapters: Equifax, Experian, TransUnion; FICO and VantageScore (US); UK CRA files; purpose code per pull (FCRA permissible purpose); CRA used recorded (UK CCA s.157).
- **FR-13 [R2]** Open Banking / cash-flow adapters (UK consented Open Banking; US aggregators), income/employment verification, rent/utility/telecom data.
- **FR-14 [R1]** Consent records per source (data, purpose, expiry, revocation) via the bank's consent platform; purpose limitation; revocation stops use and triggers recomputation.
- **FR-15 [R1]** PII tokenised on ingestion (bank vault keys), field-level encryption, role-based reveal with audit; protected attributes only in a segregated fairness-testing zone.
- **FR-16 [R3]** Macro, climate and event data import: Fed/BoE scenarios, NGFS, flood/wildfire/storm/subsidence/heat maps by ZIP/postcode, BLS/ONS labour data, sanctions/geopolitical events (offline import or optional feed).
- **FR-17 [R1]** Feature store: identical feature definitions online and offline; lineage per feature.

### 4.3 Consumer assessment (both markets)
- **FR-18 [R1]** Cards and personal loans: regulator + bank rules, PD/LGD/EAD/EL, master-scale grade, reason codes.
- **FR-19 [R1] UK** Two-limb CONC 5.2A: separate credit-risk outcome and **affordability verdict**; verified income (Open Banking / CRA / document; self-declared alone not sufficient); expenditure from Open Banking actuals, ONS/bureau norms and declared-vs-verified; foreseeable-change stress; proportionality tiers; cumulative-increase tracking; "obvious affordability" use logged with justification. A good score never overrides a failed affordability verdict.
- **FR-20 [R1] US** CARD Act ability-to-pay (minimum-payment test on verified income/assets and obligations); under-21 independent income or cosigner 21+; bank DTI/residual-income policy; MLA 36% MAPR, SCRA 6%, usury caps by charter/state/size (NY 16%/25%).
- **FR-21 [R2]** Mortgages: US ATR (8 factors) + QM classifier with dated APR-APOR and points-and-fees tables, DTI/residual income considered and verified, HMDA fields and denial codes; UK MCOB 11.6 (capital and interest, stress = max(forward-curve rate, current +1pp) over 5 years, fixed ≥ 5 years exempt), LTI ≥ 4.5x tag, buy-to-let ICR stress, second charge stresses first mortgage; US HELOC.
- **FR-22 [R4]** Auto finance (US direct/indirect; UK motor with commission disclosure capture, no discretionary commission), UK overdrafts (CONC 5D repeat use), UK BNPL (CONC 5.2A unmodified).
- **FR-23 [R1]** Age rules: US 62+ never scored negatively; UK age only with documented justification. Prohibited bases and proxies blocked (feature allow-list; NY 296-a group-statistics ban; Equality Act).
- **FR-24 [R1]** Income & fraud consistency: declared vs verified income (UK CONC 5.2A.36), synthetic-identity signals, first-party/bust-out signals → **flags handed to the bank's fraud systems**.

### 4.4 Commercial assessment
- **FR-25 [R2]** SME loans/lines/cards: rating, cash-flow (bank statements), UK Bank Referral Scheme offer on decline, LSB standards decline reasons, US 1071 data fields ready (2028).
- **FR-26 [R2]** Mid/large corporate: five dimensions (35/20/15/10/20, configurable), sector templates (CRE, leveraged, SME, large corporate), stressed cash flow, market signals for listed names (optional feed), covenant and cash monitoring.
- **FR-27 [R2]** Exposure limits: US SCCL (25% / 15% Tier 1), legal lending limit (15% + 10%), Reg O, Reg W; UK large exposures (25% / 15% G-SII); connected-counterparty and sponsor aggregation.
- **FR-28 [R2]** CRE concentration review (US 100%/300%), UK slotting and Basel 3.1 attributes (data only); leveraged heightened-review flag (debt/EBITDA > 6x, configurable).

### 4.5 Models & scoring
- **FR-29 [R1]** Three model families: constrained GBM, explainable boosting/GAM, logistic scorecard; champion-challenger selection on accuracy AND fairness.
- **FR-30 [R1]** Two scores: TTC for decisions; PIT PD macro-adjusted, refreshed daily (R3 macro inputs; R1 baseline).
- **FR-31 [R1]** Deterministic reason codes (≤ 4 for US notices; bureau key factors kept separate) from model attribution and rules; versioned reason library.
- **FR-32 [R1]** Master-scale mapping (configurable; demo 20 grades).
- **FR-33 [R2]** Model lifecycle: bank MRM approval before use; auto-retrain challenger on drift (approval to activate); auto-suspend on breach with fallback to the bank champion or our scorecard; overrides and outcomes feed retraining.
- **FR-34 [R1]** Reject inference using the bank's through-the-door data.

### 4.6 Inclusion & Gen Z (growth)
- **FR-35 [R3]** Inclusion engine: smoothed 6–12-month cash-flow income with volatility penalty, gig/multiple employers, seasonality; rent/utility/telecom history; thin-file scoring.
- **FR-36 [R1]** Starter card (demo UK £250–£1,000 / US $300–$1,500; reviews at 6 and 12 months with fresh affordability; customer spending controls; persistent-debt protection).
- **FR-37 [R1]** One-month salary advance (demo: salary credited ≥ 3 months; ≤ 50% of net pay; one at a time; affordability + not in persistent debt/difficulty; pricing from bank policy, gated by UK HCSTC caps / US MLA and state small-dollar rules if crossed).
- **FR-38 [R3]** Credit-builder products (credit-builder loan, rent reporting 18+), student/graduate offers (UK graduate overdraft; US 18–20 cards under CARD Act rules).
- **FR-39 [R3]** Readiness record for ages **16–17 only** (junior-account habits, education/goal signals; no profiling under 16; no marketing profiling of minors; children's DPIA); compliant pre-assessed offer at 18 after full affordability; US authorised-user path where the bank allows.
- **FR-40 [R3]** Gen Z loyalty (non-credit for under-18s): savings boosts, education rewards, partner perks, graduation path. No credit promotion to minors (UK CCA s.50; US CARD Act campus rules).

### 4.7 Risk vs opportunity, product design, offers
- **FR-41 [R1]** Frontier v1 (cards, loans): approvals, balances, expected loss, risk-adjusted profit (income − funding − EL − opex), inclusion impact; current policy marked. **[R3]** adds CLV, risk-budget view and **recommended policy** within appetite (human approves).
- **FR-42 [R3]** Opportunity-loss segments (e.g. gig workers, graduates) with value and risk.
- **FR-43 [R3]** Product designer: proposes limit ladders, pricing and fees (within caps and UK fair value), eligibility and features; simulates loss and profit; maker-checker.
- **FR-44 [R3]** Next-best-offer and CLV: affordability first; excludes vulnerable customers, those in difficulty, collections or persistent debt; marketing consent; FCRA prescreen firm-offer rules; no credit promotions to minors; fair value / UDAAP checks.
- **FR-45 [R2]** Card limit increases with fresh affordability (UK) / ability-to-pay (US); blocked in persistent debt.

### 4.8 Macro, climate & early warning
- **FR-46 [R3]** Scenario engine: Fed and BoE scenarios; event shocks (war/sanctions, pandemic, oil, regional disaster, sector layoffs); NGFS climate paths; custom builder. Outputs PD/EL uplift by segment, sector and region.
- **FR-47 [R3]** Physical climate risk on collateral (flood, wildfire, storm, subsidence, heat), insurance-gap flag, transition risk for corporates; 1/5/30-year horizons.
- **FR-48 [R2]** Early warning (retail): income shocks, credit stress, spending behaviour (gambling, payday, luxury, spend > income), external exposure (hazard event near home, employer in sanctioned/disrupted sector).
- **FR-49 [R3]** Sector and job-loss warning: borrowers whose employer or sector faces layoffs, sanctions or supply shocks.

### 4.9 Fairness, validation & governance
- **FR-50 [R3] US** Fair-lending suite: AIR, marginal effects, proxy detection, LDA search; BISG for testing only; disparate-impact testing on by default (FHA, state law, 5-year look-back).
- **FR-51 [R3] UK** Equality Act testing (indirect discrimination) in the segregated monitoring zone (DPA 2018 Sch 1 para 8); Consumer Duty outcome MI by cohort; fair-value checks.
- **FR-52 [R3]** Validator in a Box: champion vs challenger on scores/outcomes, model files on-prem (PMML/ONNX/pickle), stability, calibration, backtests, fairness; SR 26-2 and SS1/23 report formats.
- **FR-53 [R1]** Champion-vs-challenger report (accuracy, approvals at equal EL, fairness, stability).
- **FR-54 [R2]** Governance packs: SR 26-2 + SS1/23 model docs (incl. LLM control pack), TPRM/SS2/21, DPIA + Art 22C design, GLBA/Part 500 mapping, CO/CA ADMT deployer docs, SM&CR / model-owner mapping.

### 4.10 Notices, safeguards & UK servicing
- **FR-55 [R2]** Notice content generator (bank sends): US Reg B adverse action (30/90-day timers), FCRA (score, ≤ 4/5 key factors, CRA details), risk-based pricing; UK decline explanation and Art 22C rights; English, Spanish (US) and Welsh (UK) templates; compliance-approved, human sign-off.
- **FR-56 [R2] UK** Art 22C workflow: information, representations, human intervention and contest, tracked to SLA; meaningful-review evidence (time on case, override rate, authority) when human-in-loop.
- **FR-57 [R2] US** State AI laws: Colorado SB 26-189 and California ADMT (2027): notices, 30-day explanation, human review on request, deployer documentation.
- **FR-58 [R2] UK** Vulnerability flags route to specialists; never auto-decline on a flag.
- **FR-59 [R4] UK** Persistent-debt engine (monthly test; 18/27/36 months; £200 exemption; repayment within ~3–4 years; suspend/cancel), overdraft repeat-use, CONC 7 forbearance.

### 4.11 Collections
- **FR-60 [R4]** Cure prediction (self-cure / needs help / likely loss).
- **FR-61 [R4]** Forbearance recommender (UK CONC 7 / persistent debt; US hardship programmes).
- **FR-62 [R4]** Contact strategy with frequency caps (US 7-in-7 call presumption default), channel/time rules, opt-outs, vulnerability first; AI drafts with tone guardrails and human approval.

### 4.12 AI language model
- **FR-63 [R2]** Plug into the bank's approved LLM platform or an on-prem GPU model; US/EU-origin model option as the US default; template fallback (decisions never depend on the LLM).
- **FR-64 [R2]** Internal explanations grounded in reason codes; number/reason guardrail.
- **FR-65 [R2]** Customer letter drafts from deterministic reasons and approved templates; human sign-off.
- **FR-66 [R4]** Credit memos (commercial) and Policy Copilot: read policies (citations), find conflicts/gaps, regulatory change alerts, simulate before approval (frontier + fairness).
- **FR-67 [R3]** Portfolio & risk chat (safe actions only; changes become maker-checker requests).
- **FR-68 [R4]** Document AI: financial statements (incl. UK statutory accounts), US tax returns (1120, 1065, K-1), loan agreements and covenants, bank statements; human-confirmed extraction.

### 4.13 UX
- **FR-69 [R1]** Underwriter workspace: decision with drill-down (rules, affordability/ability-to-pay maths, reasons, PD/LGD/EAD).
- **FR-70 [R2]** Queues and workflow (if engine mode or when the bank uses ours); overrides with reason.
- **FR-71 [R1]** Strategy workspace: frontier, champion vs challenger. **[R3]** opportunity segments, product designer, what-if.
- **FR-72 [R3]** Board & CRO dashboard: champion-vs-challenger gains, opportunity captured, macro & climate exposure, early warning & collections.
- **FR-73 [R2]** Enterprise SSO (Entra ID / Okta / Ping), roles: underwriter, credit officer, strategy/policy, model risk/validator, collections, fraud liaison, CRO/board, compliance, admin, auditor.
- **FR-74 [R1]** Demo US Bank (2M accounts) and Demo UK Bank (1M accounts): bureau, Open Banking and transactions, ground truth, a simulated recession and regional disaster, a synthetic champion scorecard; plus benchmarks on public credit datasets.

### 4.14 Deployment, licence, operations
- **FR-75 [R1]** Kubernetes/OpenShift (Helm) and Docker; air-gapped mode with signed offline updates; any connectivity mode.
- **FR-76 [R1]** Bank HSM/vault for keys; encryption at rest and in transit.
- **FR-77 [R2]** Signed licence file (bank ID, modules, volume tier, expiry, offline check); read-only on expiry; **monthly usage-count export** for per-decision billing (no customer data).
- **FR-78 [R2]** Incident hooks: US service-provider notice when disruption ≥ 4 hours (bank notifies its regulator within 36 hours); UK incident reporting from Mar 2027; NY Part 500 support.

### 4.15 Income-based customer segmentation (spec: `income-segmentation-spec.md`)
- **FR-79 [R1]** Segment assignment S0–S5 from **verified annual gross income** using fixed, configurable, effective-dated bands per market (US: <$30k, $30–60k, $60–120k, $120–250k, $250k+; UK: <£20k, £20–35k, £35–60k, £60–100k, £100k+; S0 = no verified income). Irregular income uses the smoothed 12-month verified average; joint applications combine incomes; self-declared income alone never sets the segment.
- **FR-80 [R1]** Overlay tags: `GENZ`, `THIN_FILE`, `GIG_SELF_EMPLOYED`, `RETIREE`, `NEW_TO_COUNTRY`, `UNDER_18_READINESS`, with the assessment effects in the spec. No immigration-status feature without legal review.
- **FR-81 [R1]** Segment policy matrix as policy data: eligible products, card limit ranges, loan caps, max DTI (US), minimum residual income for loans and mortgages, card/advance residual floor ($300 / £100), salary-advance caps, UK mortgage LTI, automation rule per segment, limit-growth review cadence. Maker-checker, tighten-only against the packs.
- **FR-82 [R1]** Decision order: verify income → segment + tags → regulator pack → segment policy → affordability / ability-to-pay with segment residual floors → risk score → limit = lowest cap with binding constraint named → automation check (never auto-decline). Golden tests: Maria (S2, $1,500, residual $515 ≥ $300, human review), Tom (S2, £1,000, residual £453 ≥ £100, auto-approved), US S3 loan ($30k/60m/12% → ~$667; DTI 34%; residual $1,233 ≥ $1,200; binding = minimum residual).
- **FR-83 [R2]** Nightly re-segmentation: up after 2 consecutive verified months, down after 3 (immediate on verified job loss); logged; limit decreases follow change-in-terms / CONC notice rules.
- **FR-84 [R1]** Segment-level calibration and monitoring: PD accuracy, approval rate, average limit, APR and losses by segment. Income band is not a scoring penalty by itself.
- **FR-85 [R3]** Fairness by segment: fairness suites report outcomes by segment × protected-group proxy, with a business-justification record. Consumer Duty fair-value check per segment. No income-only knockouts except S0 product eligibility and regulatory minimums; S0 gets a secured-card / credit-builder path.
- **FR-86 [R3]** Segment views: dashboards and reports of customers and balances by segment (pie/donut), default rate, approval rate champion vs challenger, limit ranges, and stress-scenario EL uplift by segment; segment-aware stress scenarios and early-warning emphasis.

## 5. Cross-Cutting NFRs
- **NFR-1** Real-time scoring p95 < 300 ms, p99 < 800 ms at bank peak load (sized per install); horizontally scalable, stateless scoring.
- **NFR-2** Nightly 50M+ accounts re-score + PIT update within the bank's batch window (target ≤ 4 h).
- **NFR-3** No customer data leaves the install; deny-by-default egress; separate US/UK installs; US-person / UK-based support.
- **NFR-4** Security: SOC 2 Type II and ISO 27001 aligned controls, yearly independent pen test, SBOM, secure SDLC, OWASP ASVS L2, MFA.
- **NFR-5** Determinism and replay of every decision; effective-dated packs and policies.
- **NFR-6** Availability 99.9% for the real-time API; 24/7 support; graceful degradation (LLM → templates; challenger → champion/scorecard).
- **NFR-7** Accessibility WCAG 2.2 AA.
- **NFR-8** Regulatory, fair-lending, load/chaos and LLM red-team test suites in CI.
- **NFR-9** Explainability: every recommendation has ranked reasons; reason stability tested.

## 6. Constraints and Guardrails
- No credit to minors; readiness from 16 only; no credit promotion or marketing profiling of minors.
- LLM never selects reasons or decides; letters from approved templates with human sign-off.
- Never auto-decline; automation only where the bank configures it, with UK Art 22C safeguards.
- Fraud: flags only. Notices: content only (the bank sends).
- Regulatory values effective-dated; anything below H confidence flagged for verification.

## 7. Rollout, Team & Timeline
- **Product-owner target:** everything in v1 in **2–3 months** with **14–18 people** (≈5 backend, 4 frontend, 3 ML/data science, 2 data engineers, 1 platform/DevOps, 1 QA, PM/architect).
- **Risk statement:** this target is **high risk**. Two markets, 78 FRs and the governance packs normally take 9–12 months at this team size. The plan therefore (a) runs releases in parallel squads, (b) fixes the priority order R1 → R2 → R3 → R4, and (c) treats R1 as the must-ship. Bank vendor onboarding (12–24 months) runs in parallel and is not shortened by build speed.
- **Release contents:** R1 = FR-1–9, 14, 15, 17–20, 23, 24, 29–32, 34, 36, 37, 41 (v1), 53, 69, 71 (v1), 74–76, 79–82, 84. R2 = FR-10–13, 21, 25–28, 33, 45, 48, 54–58, 63–65, 70, 73, 77, 78, 83. R3 = FR-16, 35, 38–44, 46, 47, 49–52, 67, 71–72, 85, 86. R4 = FR-22, 59–62, 66, 68.
- **Pilot:** back-test on 3–5 years incl. rejects → 6-month shadow beside champion → limited live on one segment.
- **Commercial:** per-decision / per-account pricing; contracts with escrow, liability cap and indemnities, exit plan, regulator access rights; SOC 2 Type II, ISO 27001, pen test, cyber & PI insurance.

## 8. Non-Goals
Credit to minors; sending customer communications; fraud decisions; lifetime PD / provisioning engines; IRB capital calculations; Islamic products; cross-border data sharing between installs.

## 9. Success Metrics
- **SM-1** Out-of-time Gini ≥ champion + 3 points on the bank's history.
- **SM-2** ≥ 5% more approvals at equal expected loss (higher in thin-file/blue-collar/Gen Z).
- **SM-3** Fairness: AIR ≥ champion (US); Equality Act outcome gaps ≤ champion (UK).
- **SM-4** Reason stability and validator sign-off within the pilot period.
- **SM-5** p95 < 300 ms; nightly 50M+ within window.
- **SM-6** Zero regulator-pack breaches in recommendations; 100% replayable decisions.
- **Counter-metrics:** raw approval rate (not at the expense of SM-1/SM-3); automation rate (not a goal in itself).

## 10. Open Questions
1. Pilot bank and its champion models/engine. 2. Bank master scale and default definitions per product. 3. Bank LGD, funding cost and pricing grids for profit. 4. Which LLM platform the bank has approved. 5. Bureau and Open Banking contracts held by the bank. 6. US charter (national vs state) for usury and Part 500 scope. 7. Spanish/Welsh template approval. 8. Items marked unconfirmed in the regulatory references.

## 11. Assumptions
- A1 Demo master scale (20 grades) and automation defaults as in discovery round 23.
- A2 SM-1/SM-2 targets are proposals to confirm with the pilot bank.
- A3 Starter card, salary advance and readiness defaults as in discovery rounds 13 and 21.
- A4 The 2–3 month target is a product-owner decision recorded with a high-risk flag.
