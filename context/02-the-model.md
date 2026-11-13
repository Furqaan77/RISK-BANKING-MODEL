# 02. The model: how the platform works

Full blueprint: `_bmad-output/planning-artifacts/blueprint/platform-blueprint-v1.md` (with a PDF next to it). Earlier architecture rules AD-1..AD-16: `_bmad-output/large-bank/planning-artifacts/architecture.md` (Global) and `_bmad-output/planning-artifacts/architecture.md` (UAE).

## How one decision is made
1. **Data in.** The applicant's details plus the bank's own records. Outside data (bureau and so on) comes through allow-listed connections only.
2. **Three rule layers**, run in order:
   1. **Regulator** (`REG.*`)
   2. **Bank policy** (`CO.*`, `PORT.*`)
   3. **Credit policy** (`CRED.*`, per product)

   A lower layer may only be **tighter** than the one above ("tighten-only"). The system checks this automatically and flags any looser rule.
3. **Rules are configuration, not code.** They are YAML files with plain comparisons (for example `dbr <= 50`). Tiered limits are split into separate rules (CRED.CC.001a/b/c). A safe expression checker allows only simple comparisons.
4. **Grade 1–10** from the model (lower is safer):
   - grade **≥ 7 → refer** to a human underwriter;
   - grades **9–10 → decline recommended**.
5. **Policy always wins.** If a rule says no, the AI cannot say yes. A missing piece of data means "not evaluable", and the case goes to a human.
6. **Declines are recommendations.** A human makes the final call on declines and exceptions.
7. **Every step is written to an audit log** (hash-chained, so tampering shows). Rule changes need **maker-checker** (one person proposes, another approves).

## Six capabilities

| | Capability | Question it answers |
|---|---|---|
| A | **Decide** | Should we lend to this applicant, and why? |
| B | **Monitor** | Where are our exposures, and which limits are breached (group, sector, approval authority, staging)? |
| C | **Stress** | What happens if things get worse (bad loans double, a sector shock, a currency fall)? |
| D | **Benchmark** | Is this bank too rigid or too risky compared with its regulator and peers? (uses `master-rulebook/`) |
| E | **Explain** | Why did this happen? It answers only with evidence and refuses otherwise. |
| F | **Govern** | Who changed what, what is not yet covered (risk register), what is overdue? |

**Segments:** retail, SME, corporate and finance houses (gold and cash finance).
**Markets:** UAE (Islamic and conventional), UK, US.

## Architecture rules (the important ones)
- **Pure core:** the decision logic has no network, no database calls and no AI calls inside it, so it is testable and repeatable.
- **The AI language model (LLM) is advisory only.** It may rephrase evidence; a "number guard" stops it from changing figures. It runs on a bank-approved or local model.
- **No outbound internet** except allow-listed data providers ("egress deny").
- **AD-17:** every dataset is labelled real, de-identified, synthetic or assumed.
- **AD-18:** acceptance is measured against a hidden answer sheet of planted problems.
- **AD-19:** evidence or silence. No claim without evidence.
- **AD-20:** the portfolio engines are read-only.
- **AD-21:** honest coverage. Anything not built is listed in the risk register.
- **AD-22:** every run can be reproduced from its config (fixed seed, results hash).

## Code layout (`risk-platform/`)
```
config/          run.yaml (entities, FX, limits, grading bands, scenarios), risk_register.yaml
packs/           uae|uk|us/regulator.yaml, demo_group/bank_policy.yaml, credit_policy.yaml
riskplatform/
  core/          policy.py, grading.py, limits.py, quality.py, stress.py   (pure logic)
  services/      assess, portfolio, stress, benchmark, explain, acceptance
  ports/llm.py   NullLLM + number guard
  adapters/      csv_store.py (swap for the bank's warehouse later)
  audit/log.py   hash-chained audit log
synth/generate.py  builds the fictional "Demo Group" bank + hidden answer sheet
run_demo.py      runs everything -> outputs/report.md, results.json, audit.jsonl
tests/           answer-sheet acceptance tests
app/             Streamlit UI shell (optional)
```

## Roadmap (body metaphor the user likes)
**0 Skeleton** (done) → **1 Muscles** (full rule packs, policy intake) → **2 Organs** (real default models, real bank data) → **3 Nerves** (external data connectors, LLM) → **4 Skin** (proper UI) → **5 Blood supply** (operations, monitoring, deployment at a bank).

**Real default model, planned:** US mortgages trained on Freddie Mac / Fannie Mae loan-level data; SME and corporate rating models later. The current scorecard is **illustrative only**.
