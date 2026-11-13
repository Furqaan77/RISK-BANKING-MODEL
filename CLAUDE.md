# CLAUDE.md: read this first (project context for Claude on any machine)

New machine? Say "implement the shift prompt md" (see `SHIFT-PROMPT.md` and `context/`).

This repo is the **AI Risk Score Card** project ("Risk Banking Model"). Read `HANDOFF.md` next for the full concept, decisions, status and open items. Read `README.md` for the folder map.

## One-paragraph concept
An **on-prem, per-bank AI credit risk model**. Each bank runs it privately on its own machines. It scores retail customers (grades 1–10) and applies rules in three layers: **central-bank rules → bank policy → credit policy**. Lower layers can only tighten, never loosen ("tighten-only"). The **policy always wins** over the model. Grade ≥ 7 goes to a human (Refer), grades 9–10 are declined. Changes to rules use maker-checker. Rules are written as plain-comparison config (YAML), not code.

## Standing preferences from the user
- Build happens on a **separate machine**. Never assume this PC's specs in prompts or plans.
- Write in **simple language** for new risk staff and interns. Avoid jargon, or explain it.
- Use **visuals** (graphs and pie charts). Give **PDFs the user can open directly**. Open them for the user once built.
- Positioning is **"competitive but safe"**: easy to qualify, mid-market price, never looser than the regulator.
- Bankers read plans **factually, not technically**.
- Ask the user questions when unsure. Don't invent regulatory values. Mark them "verify" and give the source and confidence.

## Conventions
- BMAD Method v6.12.4 is installed (`_bmad/`, outputs in `_bmad-output/`).
- Policy packs follow one numbered pattern: `00-decisions`, `01-benchmark`, `03-parameter-sheet`, `04-benchmark-gap-report`, `05-retail-credit-policy`, `config/`.
- Sign-off markers in policy docs: **[A]** adjusted from the user's criteria, **[P]** proposal, **[R]** required by regulation.
- Chart palette, in fixed order: blue #2a78d6, orange #eb6834, aqua #1baf7a, yellow #eda100, magenta #e87ba4, green #008300. Brand: navy #14213D, teal #0F7B7B.
- Do not draw bank group retail figures as market shares. They are group or segment books and are not additive.
- PDFs are made from HTML with headless Chrome. Scripts are in `tools/`. See `HANDOFF.md` §8.
