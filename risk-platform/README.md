# risk-platform: the skeleton

The working skeleton of the AI Risk Platform. The blueprint is `_bmad-output/planning-artifacts/blueprint/platform-blueprint-v1.md`.
Every limb exists and works end to end on a **fictional bank** (Demo Group: UAE, UK and US entities; retail, SME and corporate loans).
Organs (real models, full rulebooks, real data, LLM, UI) are added later **without changing the shape**.

## Run it
```bash
pip install pyyaml               # only dependency of the skeleton
python synth/generate.py         # build the fictional bank + hidden answer sheet
python run_demo.py               # run every engine, write outputs/report.md, results.json, audit.jsonl
python tests/test_answer_sheet.py   # or: python -m pytest tests
```
Optional UI shell: `pip install streamlit && streamlit run app/streamlit_app.py`.

## What runs today

| Capability | Module | What it does now |
|---|---|---|
| Decide | `core/policy.py`, `core/grading.py`, `services/assess.py` | Regulator → bank → credit rules (safe expressions, tighten-only check), grade 1–10 from an *illustrative* scorecard. Policy always wins; declines are recommendations |
| Monitor | `core/quality.py`, `core/limits.py`, `services/portfolio.py` | Duplicates, reconciliation, group (connected-borrower) limits, sector caps, approval authority, IFRS 9 staging backstops |
| Stress | `core/stress.py`, `services/stress.py` | Expected loss under baseline, credit deterioration, sector shock, FX shock, combined (explicit order, no double counting) |
| Benchmark | `services/benchmark.py` | Our policy vs regulator and peers, using `master-rulebook/data/compare_*.csv` |
| Explain | `services/explain.py`, `ports/llm.py` | Evidence-linked answers; refuses without evidence; the LLM can only rephrase (guarded) |
| Govern | `audit/log.py`, `config/risk_register.yaml` | Hash-chained audit log; register of risks not yet implemented |

**Planted problems:** 9, all detected. The answer sheet is in `data/answer_sheet.json`, and the tests fail if any problem is missed.

## Labels (read before showing anyone)
- **Data:** SYNTHETIC.
- **Limits and scenarios:** ASSUMED, except where a pack rule cites a regulator.
- **Grade:** an ILLUSTRATIVE scorecard. It proves the pipeline works, not that it predicts defaults.

## Where the organs go

| Organ | Plugs into | Notes |
|---|---|---|
| Real default model | `core/grading.py` (same `grade()` interface) | US mortgages on Freddie Mac / Fannie Mae loan-level data; SME/corporate rating models |
| Full regulator packs | `packs/{uae,uk,us}/regulator.yaml` | From `master-rulebook/` and the BMAD research runs |
| Bank data | `adapters/` | Replace `csv_store.py` with the bank's warehouse / LOS adapter |
| External data | new adapters behind allow-listed egress | Bureau, business credit, market, sanctions, adverse media |
| LLM | `ports/llm.py` | Bank-approved or local model. Rephrasing only, with the number guard kept |
| UI | `app/` | Streamlit shell now; React later |
| Market, liquidity, operational, vendor engines | `services/`, listed in the risk register | Not implemented yet |
