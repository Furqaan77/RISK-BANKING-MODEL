# SHIFT PROMPT: move the whole project context to this machine

> **How to use:** on the new machine, clone the repo, open it in Claude Code and say:
> **"implement the shift prompt md"**
> Claude then follows the steps below and comes back knowing the business, the model, what is built and what comes next.

---

## Instructions for Claude (follow in order)

You are picking up an existing project on a new machine, possibly with a new account. The original chat history is **not** available. Everything you need is in this repo. Do these steps:

### Step 1: Read the context pack, in this order
1. `CLAUDE.md`: the project rules (short).
2. `context/01-business-idea.md`: what we sell, to whom, why, and the problem statement.
3. `context/02-the-model.md`: how the AI Risk Platform works (rules layers, grading, six capabilities, architecture rules).
4. `context/03-status.md`: everything built so far, with folder locations and results.
5. `context/04-people-and-direction.md`: who is involved and the direction from the mentor.
6. `context/05-working-rules.md`: how the user wants you to work (language, visuals, PDFs, honesty rules).
7. `context/06-next-steps.md`: open items and the agreed next steps.
8. `context/07-glossary.md`: banking and project terms.
9. Then skim `HANDOFF.md` (full detail), `README.md` (folder map), `risk-platform/README.md` and `master-rulebook/README.md`.

Do **not** read every research digest or policy file now. Open them only when a task needs them.

### Step 2: Install the memory
The files in `context/memory/` are the long-term memory from the original machine. Copy them into your persistent memory directory for this project (the `memory/` folder Claude Code uses for this working directory), including `MEMORY.md` as the index. If a memory file with the same name already exists, merge it; don't duplicate it. Treat them as background facts, and check any file or path they name before relying on it.

### Step 3: Check the machine (read-only, quick)
- `python --version`. Then `pip install pyyaml` and run `python risk-platform/synth/generate.py`, `python risk-platform/run_demo.py` and `python risk-platform/tests/test_answer_sheet.py` (from inside `risk-platform/`). Expect **6/6 tests pass and 9/9 planted problems detected**.
- Check whether Chrome is installed (needed for PDFs) and whether `openpyxl`, `markdown` and `pypdfium2` are available. Report what is missing; don't install heavy things without asking.
- Paths in `tools/` scripts were written on Windows and some are hard-coded. Note this; don't fix them unless a task needs it.

### Step 4: Confirm to the user
Reply in **simple language** (no jargon) with:
1. The business idea in 3 lines.
2. How the model decides, in 5 bullets.
3. What is built (a short list with folder names).
4. The test result from Step 3.
5. The top 3 next steps from `context/06-next-steps.md`, and a question asking which one to start.

Keep it under one screen. Then wait for the user.

---

## Rules that always apply (short version; detail in `context/05-working-rules.md`)
- **Simple language**, visuals (charts), and PDFs the user can open. Open PDFs for the user after building them.
- **Never invent regulatory numbers.** Mark them "verify" and give the source and confidence.
- **Bank internal policies are supplied by the user later.** Don't research or make them up.
- **Policy always wins over the AI. Lower rule layers can only tighten. Declines are recommendations; a human decides.**
- **Push to GitHub only when the user asks.** The repo is https://github.com/Furqaan77/RISK-BANKING-MODEL (public).
- Ask the user when unsure.
