# AI Risk Score Card Global: Step-by-Step Build Plan

Written for **anyone joining the project**, including new risk-department staff and interns. You do not need to be a developer to follow it.
The technical instructions for the team are in `BMAD-BUILD-PROMPT-GLOBAL.md`. This page explains the same plan in plain steps.

---

## Part 0. Read this first (5 minutes)

**What are we building?** Software that a large US or UK bank installs on its own servers. When a customer applies for a credit card,
loan, mortgage or business loan, the software:
1. checks the law (US or UK rules),
2. checks the bank's own lending policy,
3. checks whether the customer can afford the repayments,
4. estimates the chance the customer will not pay back,
5. recommends approve / refer to a person / a lower amount, with reasons,
6. and proves to the bank that it does this **better than the bank's current model** (the "champion").

**What is BMAD?** A step-by-step method for building software with AI coding assistants. It splits the work into:
- **Epics**: big chunks of work (we have **29**).
- **Stories**: small tasks inside an epic, each about 1–3 days of work (we have **146**).
- **Sprints**: two-week work periods. At the end of each one, the team shows what it finished.

**Who builds it?** 14–18 people in 8 squads (small teams), all working at the same time.

**Target:** everything in about **2–3 months (6 sprints)**. This is ambitious and **high risk**, so we always build the most important things first
(Release 1 → 2 → 3 → 4).

| Word | Plain meaning |
|---|---|
| Release (R1–R4) | A bundle of finished features we can demonstrate |
| Gate | A checklist that must pass before a release counts as done |
| Squad | A small team that owns some epics |
| PR (pull request) | A proposed code change that another person reviews before it is accepted |
| CI | Automatic tests that run on every change |
| Must-ship | The stories in each epic that we protect first if time runs short |

---

## Part 1. The four releases in plain words

| Release | What the bank can see when it is done | Epics | Stories |
|---|---|---|---|
| **R1 Challenger MVP** | Cards, personal loans and salary advances scored in **both** the US and the UK; **customers placed in income segments S0–S5** with matching products and limits; affordability (UK) and ability-to-pay (US); risk numbers and reasons; a report showing we beat the bank's model; demo US and UK banks | 1–10 + 29 (must-ship) | 55 + 5 |
| **R2 Pilot-ready** | Mortgages, business and corporate loans, connection to the bank's systems, letters content, logins and approval queues, the AI writer, model governance, compliance documents | 11–19 | 46 |
| **R3 Growth & macro** | Help for thin-file, blue-collar and Gen Z customers; product designer and offers; war/disaster/recession/climate scenarios; fairness tests; checking the bank's own models; board dashboard | 20–24 | 22 |
| **R4 Operations** | Collections help, UK persistent-debt rules, auto loans, UK overdrafts and BNPL, reading documents, policy copilot | 25–28 | 15 |

---

## Part 2. Who does what (the 8 squads)

| Squad | What they own | Epics |
|---|---|---|
| **Platform/DevOps** | Servers, security, separate US/UK installs, logins, speed, licence | 1, 8, 16, 18 |
| **US Pack** | US laws turned into rules: Reg B letters, CARD Act, mortgages (ATR/QM), interest caps, state AI laws | 2, 6, 12, 15, 27 |
| **UK Pack** | UK rules: affordability (CONC 5.2A), Consumer Duty, mortgage stress, right to human review, persistent debt | 2, 7, 12, 15, 25, 27 |
| **Models & ML** | Risk models, reasons, champion vs challenger, frontier, inclusion, scenarios, fairness | 5, 9, 13, 14, 20–23, 26 |
| **Data Engineering** | Data pipes from the bank, feature store, consent, privacy tokens, demo banks | 3, 4, 11, 18, 20, 22 |
| **Frontend** | The screens people use | 10, 16, 21, 24 |
| **AI/LLM** | The AI writer: explanations, letter drafts, memos, policy copilot, chat | 17, 24, 26, 28 |
| **QA** | Testing everything: rules, fairness, speed, security | 8, 19, 23 (+ all) |

---

## Part 3. Before any code: setup (Week 1, days 1–3)

| Step | What happens | Who | Done when |
|---|---|---|---|
| 1 | Create the private code repository `ai-risk-score-card-global` | Platform lead | Repo exists, team has access |
| 2 | Copy the planning documents into it (list in `BMAD-BUILD-PROMPT-GLOBAL.md` §1) | PM | Files in `_bmad-output/planning-artifacts/` |
| 3 | Install BMAD (one command in the build prompt) | Platform lead | `.claude/skills` and `_bmad/` folders present |
| 4 | Run `bmad-help` to check BMAD can see the plan | PM | It recommends "validate PRD" |
| 5 | **Validate the plan**: `bmad-prd` (requirements), `bmad-architecture` (design and versions) | PM + architect | Findings list written |
| 6 | Product owner reviews the findings | Product owner | Signed off ⛔ |
| 7 | Create the rules file every AI assistant must follow (`bmad-project-context` → `AGENTS.md`) | Architect | `AGENTS.md` committed |
| 8 | Generate the task tracker (`bmad-sprint-planning` → `sprint-status.yaml`) | PM | 138 stories listed with status |
| 9 | Assign epics to squads (table in Part 2); each squad picks its first stories | Squad leads | Sprint 1 board ready |

---

## Part 4. How ONE task gets done (example: Tom's affordability check, Story 7.2)

Tom, 19, in London, applies for a £1,000 starter card. Story 7.2 builds the UK affordability check.

1. **Pick the story.** A UK Pack developer moves Story 7.2 to "in progress" in `sprint-status.yaml`.
2. **Read the story.** It says what to build and how we know it works (acceptance criteria):
   income £1,650 − rent £500 − essentials £620 − phone £35 = **£495** left over; repaying £1,000 over 36 months at 29.9% APR ≈ **£42.40**
   a month → **PASS**.
3. **Start the BMAD build.** The developer runs `bmad-build story 7.2` in Claude Code.
4. **Write the tests first.** Before any feature code, write tests that check exactly those numbers, plus a "fail" case (for example,
   essentials of £1,200 leave too little money) and the rule that a good risk score can **never** override a failed affordability check.
5. **Write the code** until the tests pass.
6. **Self-check.** BMAD reviews its own work against the story and the rules.
7. **Code review.** Run `bmad-code-review` (several AI reviewers), then fix what they find.
8. **Open a PR.** Automatic tests (CI) run: all tests, the UK rule tests, security scans.
9. **Human review.** Another developer reads the change and approves it.
10. **Merge.** The change joins the main code, and the story is marked "done".

Every one of the 138 stories goes through these same 10 steps.

---

## Part 5. Week-by-week plan (target: 6 sprints, about 12 weeks)

> If the team falls behind, **R4 moves out first, then parts of R3**. R1 is never cut.

### Sprint 1 (weeks 1–2): Foundations
| Squad | Works on | Goal by end of sprint |
|---|---|---|
| Platform/DevOps | Epic 1 (platform, separate US and UK installs, replay of decisions) | Empty US and UK installs running; can't talk to each other |
| US + UK Pack | Epic 2 (rule packs, "can't be looser than the law" check, never-auto-decline) | Rule engine runs on sample rules |
| Data Eng | Epic 3 (feature store, consent, privacy tokens) + Epic 4 (demo banks) | Demo US (2M) and UK (1M) customers generated |
| Models & ML | Epic 4 (synthetic champion model, public datasets) | A "champion" model to beat exists |
| Frontend | Screen designs for Epic 10 | Clickable mock-ups |
| QA | Test framework, rule-test template | CI runs on every change |
| **End of sprint** | **Demo:** installs, rule engine, demo data | |

### Sprint 2 (weeks 3–4): Scoring core
| Squad | Works on |
|---|---|
| Models & ML | Epic 5 (three model types, risk numbers, reasons, grades) |
| US Pack | Epic 6 starts (US cards, loans, starter card, salary advance, CARD Act, interest caps) |
| US + UK Pack | **Epic 29** (income segments S0–S5, overlay tags, segment policy matrix: stories 29.1–29.4) |
| UK Pack | Epic 7 starts (UK affordability, starter card, salary advance) |
| Data Eng | Finish Epic 3; start Epic 11 (connect to bank data platforms) |
| Platform | Epic 8 starts (real-time API) |
| QA + all | Epic 19 starts early (compliance documents take longest at banks) |
| **End of sprint** | **Demo + honest re-forecast** using real speed. Tell the product owner what will and won't fit ⛔ |

### Sprint 3 (weeks 5–6): Finish Release 1
| Squad | Works on |
|---|---|
| US + UK Pack | Finish Epics 6 and 7: **Maria and Tom golden tests must pass** |
| Platform + QA | Finish Epic 8: speed test **p95 < 300 ms** |
| Models & ML | Epic 9 (champion vs challenger report, frontier v1) |
| Frontend | Epic 10 (underwriter and strategy screens) |
| **End of sprint** | **R1 gate** (checklist in Part 6) + demo to product owner ⛔ |

### Sprint 4 (weeks 7–8): Release 2, part 1
| Squad | Works on |
|---|---|
| US + UK Pack | Epic 12 (mortgages) and Epic 15 (letter content, UK right to human review, US state AI laws) |
| Models & ML | Epic 13 (business and corporate loans, exposure limits) and Epic 14 (model approval, drift, safety switch) |
| Data Eng | Finish Epic 11 (batch 50M accounts, Kafka, bureaus, Open Banking) |
| Platform + Frontend | Epic 16 (logins, roles, approval queues, limit increases) |
| AI/LLM | Epic 17 (AI writer with number check) |
| Platform + Data | Epic 18 (licence, incident alerts, early warning) |

### Sprint 5 (weeks 9–10): Finish Release 2, start Release 3
| Squad | Works on |
|---|---|
| All R2 squads | Finish Epics 12–18; finish Epic 19 documents |
| Models & ML + Data | Epic 20 (inclusion engine, Gen Z readiness from 16, loyalty) and Epic 22 (war, disaster, recession, climate scenarios) |
| Models & ML + Frontend | Epic 21 (opportunity segments, product designer, offers) |
| **End of sprint** | **R2 gate** + demo ⛔ |

### Sprint 6 (weeks 11–12): Release 3 and Release 4
| Squad | Works on |
|---|---|
| Models & ML + QA | Epic 23 (fair-lending tests, validator for the bank's own models) |
| Frontend + AI/LLM | Epic 24 (board dashboard, portfolio chat) |
| UK Pack | Epic 25 (persistent debt, overdrafts, forbearance) |
| Models & ML + AI/LLM | Epic 26 (collections cure and contact strategy) |
| US + UK Pack | Epic 27 (auto loans, UK overdraft and BNPL) |
| AI/LLM | Epic 28 (document reading, credit memos, policy copilot) |
| **End of sprint** | **R3 and R4 gates** + demo ⛔. Week 13 (if available): fixes and hardening |

---

## Part 6. Release gate checklists (tick every box)

**R1 Challenger MVP**
- [ ] US and UK installs run separately and cannot reach each other
- [ ] Cards, loans and salary advance scored in both markets
- [ ] Every customer gets an income segment (S0–S5) and overlay tags; segment limits apply; **US S3 loan example:** $667/month, DTI 34%, $1,233 left over → passes
- [ ] **Maria (New York):** $560 left over; $150 minimum payment; grade 13; $1,500 starter card; sent to a person
- [ ] **Tom (London):** £495 left over; £42.40 a month; affordability PASS; grade 12; auto-approved with UK rights information
- [ ] The system never automatically declines anyone
- [ ] No bank setting can be looser than the law
- [ ] Every decision can be replayed exactly
- [ ] p95 speed under 300 ms
- [ ] Champion vs challenger report and frontier v1 on the demo banks

**R2 Pilot-ready**
- [ ] Mortgages (US ATR/QM, UK stress test), business and corporate loans with exposure limits
- [ ] Connected to the bank's data (batch, streaming, bureaus, Open Banking)
- [ ] Letter content (English, Spanish, Welsh), UK human-review workflow, US state AI laws
- [ ] Logins, roles, approval queues; AI writer with number check; model approval and safety switch
- [ ] Compliance documents ready (model docs, third-party, data protection, security)

**R3 Growth & macro**
- [ ] Inclusion engine, Gen Z readiness (16–17 only, no credit, no marketing to minors), loyalty
- [ ] Product designer, offers, recommended policy on the frontier
- [ ] War / disaster / recession / climate scenarios and climate risk on homes
- [ ] Fairness tests (US and UK) and validator for the bank's own models
- [ ] Board & CRO dashboard and portfolio chat

**R4 Operations**
- [ ] Collections cure, forbearance and contact rules
- [ ] UK persistent debt (18/27/36 months), overdrafts, BNPL; auto loans
- [ ] Document reading, credit memos, policy copilot

---

## Part 7. The team's weekly rhythm

| When | What | Who |
|---|---|---|
| Every day, 15 minutes | Stand-up: what I finished, what I'm doing, what blocks me | Each squad |
| Every day | Pick next story → 10 steps in Part 4 | Developers |
| Weekly | Cross-squad sync on shared pieces (rule engine, API, data model) | Squad leads + architect |
| End of each sprint | Demo to the product owner; update `sprint-status.yaml` | Everyone |
| End of each epic | Retrospective (`bmad-retrospective`): what went well, what to fix | The squad |
| Any change of scope | `bmad-correct-course`, never ad hoc | PM |

---

## Part 8. After the build: the pilot at a bank

| Step | What happens | Typical length |
|---|---|---|
| 1 | Bank security, legal and third-party checks (in parallel from the start) | 12–24 months at a large bank |
| 2 | Install inside the bank (US or UK) | 2–4 weeks |
| 3 | **Back-test:** run the challenger on 3–5 years of the bank's past applications, including rejected ones | 4–8 weeks |
| 4 | Bank's model-risk team validates our models | 2–4 months |
| 5 | **Shadow run:** score live applications beside the champion; no customer is affected | 6 months |
| 6 | Compare: accuracy, approvals at equal loss, fairness, stability | End of shadow |
| 7 | **Limited live** on one product or segment | Bank decides |

---

## Part 9. Stop and ask the product owner when…
- Two documents disagree.
- A legal value marked "to verify" affects a release gate.
- Anything would mix US and UK data, let the AI choose reasons or decide, automatically decline, market credit to under-18s, or loosen a legal rule.
- The sprint-2 re-forecast shows the 2–3 month target won't be met.

---

## Where everything is
| Document | Path |
|---|---|
| Discovery answers (every decision + Maria & Tom) | `_bmad-output/large-bank/planning-artifacts/discovery-answers.md` |
| US vs UK comparison | `_bmad-output/large-bank/planning-artifacts/jurisdiction-comparison.md` |
| Product brief | `_bmad-output/large-bank/planning-artifacts/product-brief.md` |
| PRD (78 requirements) | `_bmad-output/large-bank/planning-artifacts/prd.md` |
| Architecture (16 design rules) | `_bmad-output/large-bank/planning-artifacts/architecture.md` |
| Epics & stories (29 / 146) | `_bmad-output/large-bank/planning-artifacts/epics.md` |
| Income segmentation spec (S0–S5) | `_bmad-output/large-bank/planning-artifacts/income-segmentation-spec.md` |
| US and UK rule references | `docs/regulatory/large-bank/` |
| Build prompt for the team | `BMAD-BUILD-PROMPT-GLOBAL.md` |
| Banker PDF | `AI Risk Score Card Global - Plan for Bank Leadership.pdf` |
