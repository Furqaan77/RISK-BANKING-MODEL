# AI Risk Score Card: Risk Banking Model

An on-prem, per-bank AI credit risk model built on central-bank rules, bank policy and credit policy. This repo holds the plans, build prompts, regulatory research, and three complete retail credit policy packs.

New here? Read `CLAUDE.md`, then `HANDOFF.md`.

## Folder map

| Path | What it is |
|---|---|
| `BMAD-BUILD-PROMPT.md`, `BUILD-PLAN.md` | UAE Islamic edition: build prompt (run on a separate machine) and build plan |
| `BMAD-BUILD-PROMPT-GLOBAL.md`, `BUILD-PLAN-GLOBAL.md` | Global edition (US + UK, large global bank): build prompt and plan |
| `AI Risk Score Card - Plan for Bank Leadership.pdf` | Banker-facing plan, UAE (non-technical) |
| `AI Risk Score Card Global - Plan for Bank Leadership.pdf` | Banker-facing plan, Global |
| `AI Risk Score Card Global - Complete Pack.pdf` | 81 pages, titled "AI Risk Score Modelling for Banks" (walkthrough + banker plan + income-segmentation spec) |
| `credit-policy-uae/` | Retail credit policy, **UAE Islamic bank** |
| `credit-policy-uae-conventional/` | Retail credit policy, **UAE conventional bank**, plus `market-position/` (comparison with 33 UAE banks) |
| `credit-policy-uae-finance-company/` | Retail credit policy, **UAE finance company** (pilot) |
| `docs/regulatory/` | Regulatory research (CBUAE, UK, US/NY) |
| `research/` | Source research documents supplied by the user |
| `_bmad/`, `_bmad-output/` | BMAD Method install and planning artifacts (PRD, architecture, epics, discovery answers) |
| `archive/` | Superseded v1 files |
| `tools/` | Scripts used to build the PDFs and charts |

## Each credit-policy pack contains
`00-decisions.md` (user decisions and open sign-offs), `01-benchmark*.md` (research on peers), `03-parameter-sheet.md` (every parameter, rated vs the market), `04-benchmark-gap-report.md` + PDF (where we stand, with charts), `05-retail-credit-policy.md` + PDF/DOCX (the policy itself), and `config/` (YAML rules + `validate_config.py` + README).

To check a pack's rules: `python config/validate_config.py` (needs PyYAML).
