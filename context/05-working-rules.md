# 05. How to work with this user

## Style
- **Simple language.** Readers are bankers, new risk staff and interns. Avoid jargon or explain it. Bankers read plans **factually, not technically**.
- **Visuals:** graphs and pie charts. Use the chart palette in this order: blue #2a78d6, orange #eb6834, aqua #1baf7a, yellow #eda100, magenta #e87ba4, green #008300. Brand colours: navy #14213D, teal #0F7B7B.
- **PDFs** the user can open directly. **Open them for the user** after building. They are made from HTML with headless Chrome (see `HANDOFF.md` §8), using a separate `--user-data-dir` per build.
- Keep answers short. When asked to be critical, be really critical.
- When asked to "stitch" or merge text, don't drop content unless told to reduce it.

## Honesty rules
- **Never invent regulatory values.** Mark them **"verify"** and give the source, date and confidence (H/M/L).
- **Research facts need a source retrieved now**, not memory. Training knowledge can suggest where to look, but it is not evidence.
- **Don't draw bank group retail figures as market shares.** They are group or segment books and can't be added up.
- **Don't research or invent banks' internal policies.** The user will paste them in.
- Ask the user when unsure.

## Product rules (never break)
- **Tighten-only:** lower rule layers can't loosen.
- **Policy beats AI.** Grade ≥ 7 is referred to a human; grades 9–10 get a decline recommendation. A human decides declines.
- **Maker-checker** for rule changes. **Audit everything.**
- **"Competitive but safe":** never looser than the regulator.

## Process
- **Build machine:** builds happen on a **separate machine**. Never assume this PC's specs. Prompt files must run directly elsewhere.
- **BMAD Method v6.12.4** is installed (`_bmad/`). Outputs go in `_bmad-output/`. The user lets Claude choose which BMAD agent or skill to use (analyst, architect, PM, dev, deep-recon). Deep-recon research runs live in `_bmad-output/planning-artifacts/research/<run>/` with `digests/`, `imports/`, `research.md` and `.memlog.md`.
- **Policy packs:** follow one numbered pattern: `00-decisions`, `01-benchmark`, `03-parameter-sheet`, `04-benchmark-gap-report`, `05-retail-credit-policy`, `config/`. Sign-off markers: **[A]** adjusted from the user's criteria, **[P]** proposal, **[R]** required by regulation. When a value changes, update the parameter sheet, policy, config and gap report together.
- **Git:** commit and push **only when the user asks**. The repo is public; keep private material (meeting transcripts, real bank policies) out unless the user confirms.
- **Token-heavy research:** each researcher costs about 160–240k tokens. Say the cost before starting large runs.
