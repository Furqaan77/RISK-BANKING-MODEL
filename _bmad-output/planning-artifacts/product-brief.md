---
title: AI Risk Score Card
type: product-brief
created: 2026-11-07
status: final
sources:
  - _bmad-output/planning-artifacts/discovery-answers.md (104 discovery questions, 26 rounds)
  - research/Untitled document (10).pdf (planning-call transcript)
  - research/WhatsApp Image 2026-11-06 at 1.03.52 PM.jpeg (whiteboard)
  - research/Bank's Credit Assessment Framework for Corporate Lending.pdf
  - research/research.txt (AI in the bank's risk function, 13 departments)
  - archive/PROMPT_v1_2026-11-06.md, Appendix A (CBUAE rules research)
---

# Product Brief: AI Risk Score Card

## Executive Summary

**AI Risk Score Card** is an on-premise AI credit-risk engine for **Islamic banks in the UAE**. It runs inside the
bank's own data centre and connects to the core banking system (Temenos T24/Transact first). Every
finance application, and every night the whole existing book, is assessed against three layers of
policy: **CBUAE regulation**, the **bank's own policy**, and the bank's **credit policy**. The result is a
risk grade (1–10), a 12-month probability of default, a decision recommendation (Approve / Refer / Decline),
a recommended finance limit, and a plain-language explanation in English and Arabic.

The problem it solves is commercial as much as it is about risk. UAE banks hold far more deposits than they lend
(e.g. ~AED 60 bn of deposits against ~AED 34 bn of financing). Credit policies with 60–80 parameters are
applied by hand, so good customers are declined by blanket rules, risky customers slip through, and decisions
take days. AI Risk Score Card applies the bank's own rules consistently and adds behavioural intelligence:
salary stability, spending patterns, and lifestyle that doesn't match income. It also shows the bank
**where its policy is costing it good business**. The aim is fewer defaults, more approvals at the same
risk, faster decisions, and a measurable ROI uplift in AED. It is designed to serve the **low-salary
segment** too, now that CBUAE has removed the AED 5,000 minimum.

It is the first module of a broader risk-AI platform for the bank's risk function. Its governing
principle: **AI recommends, scores, drafts and flags; bank staff decide and are accountable.**

## The Problem

- **Idle balance sheet.** Deposits (liabilities) far exceed financing (assets). The bank pays for funds it
  does not deploy, because it cannot measure and contain the risk of lending more.
- **Manual, inconsistent policy application.** Officers apply long credit policies by hand. Two officers
  reach different answers on the same file, and nobody can easily say *why* a past decision was made.
- **Blanket rules turn away good customers.** Whole groups (restricted nationalities, non-listed
  employers, low earners) are declined regardless of individual strength. Long-service salary-transfer
  customers with large end-of-service benefits are rarely offered finance, even though CBUAE allows
  personal finance to be repaid from salary and EOSB.
- **Behaviour data is unused.** Banks hold salary credits, card transactions and account conduct that
  reveal risk early (salary delays, rising card utilisation, lifestyle out of line with income), but
  decisions rarely use it, and the existing book is reviewed too late.
- **Data cannot leave the bank.** Cloud scoring services are not acceptable to UAE banks for customer data.

## The Solution

- **Three-layer policy engine.** CBUAE rules (researched and sourced) are hard gates the bank can tighten
  but never loosen. The bank's policy and credit policy are read from its own documents (PDF/Word manual
  and Excel parameter sheet), converted with LLM help into a reviewed, versioned rule set under
  maker-checker control.
- **Risk scoring.** An expert scorecard that works from day one, refined by a gradient-boosting model
  trained locally on the bank's own 1–2 years of history (including rejected applications). The model is
  monitored for drift, retrains automatically, and is suspended automatically (scorecard fallback) if quality
  drops.
- **Decision support.** Policy always wins. The model can only escalate a policy pass to Refer. The
  risk grade decides whether a deviation is possible and who must approve it. The approval workflow
  routes each case to the right authority.
- **Limits.** The largest safe finance amount under the CBUAE caps, the bank's caps, DBR (basic + housing
  income) and the 20× total unsecured cap, with the binding rule named.
- **Portfolio intelligence (nightly).** Early-warning watch-list, lifestyle-vs-income mismatch alerts,
  de-risking actions (reduce limits, tighten collateral/covenants), pre-approved offers, card limit
  increases, opportunity finder (good business blocked by policy, in AED), concentrations including hidden links,
  stress tests, and a policy what-if simulator with approval / expected-loss / ROI impact.
- **Local AI language model (Qwen/Llama).** Explains decisions, drafts credit memos (human-approved),
  answers "ask-the-portfolio" questions (acts only on safe actions), and reads policy PDFs into draft rules.
  It never invents numbers (strict guardrail), and its output is internal only.
- **Islamic-native.** Tawarruq/Murabaha personal finance, Islamic cards, auto/goods Murabaha and
  Ijara/home finance. Profit-rate maths and wording, no compounding late charges (charity), Sharia-prohibited
  sectors, product-structure checks.
- **Corporate & SME.** Five-dimension rating (financial capacity 35%, business 20%, governance 15%,
  external 10%, security 20%), EBITDA −30% stressed cash-flow sizing, CBUAE large-exposure limits with group
  aggregation, and document AI for PDF financial statements.

## What Makes This Different

1. **Runs entirely on-premise.** No customer data leaves the bank. Works fully air-gapped.
2. **Built on the bank's own policy plus CBUAE**, not a generic bureau score. Every decision traces to a rule and a source.
3. **Finds missed opportunities.** It quantifies good customers the policy turns away, and what each restriction costs.
4. **Islamic-finance native** from day one.

These are execution and positioning advantages, not technical moats. Speed to a credible pilot matters.

## Who This Serves

- **CRO / Head of Risk** (buyer, policy owner): risk appetite, what-if simulation, model governance, de-risking.
- **Credit officers / analysts** (daily users): consistent, explained recommendations, drafted memos, fewer days per file.
- **Relationship managers**: instant eligibility, pre-approved offers, card limit increases.
- **Management / CEO**: KPI and ROI dashboard. Approvals, defaults, opportunity value, income uplift.
- Secondary: model validators, auditors, the bank's Sharia board, bank IT/security.

## Success Criteria

- Pilot (parallel run at an Islamic bank, < 100k retail customers) demonstrates on the bank's own data:
  fewer defaults among approvals, more approvals at equal risk, faster decision time, and ROI uplift in AED.
- Low-salary customers are served under bank-set thresholds and caps, with risk held within appetite.
- Learning-model quality passes the activation gate and independent validation. Zero CBUAE-rule breaches in recommendations.
- Bank onboarding packs (security, PDPL, CBUAE outsourcing, Sharia note) accepted by the pilot bank.

## Scope

Delivered in three releases (detail in the PRD):
- **R1: Demo MVP.** Retail Islamic scoring end-to-end (CBUAE + demo bank policy + scorecard → grade,
  decision, limit, reasons), decision screen with drill-down, risk ranking of the book, "Demo Islamic Bank" tenant on
  synthetic T24-like data.
- **R2: Pilot.** Corporate & SME, approval workflow & roles (AD/SSO), T24 API + DB connectors, ML with
  monitoring, LLM explanations/memos/policy-reading, document AI for PDF financials, Arabic outputs.
- **R3: Full v1.** Nightly early warning, lifestyle mismatch, de-risking, opportunity finder, pre-approved
  offers, card limit increases, what-if simulator, stress tests, concentrations & hidden links, portfolio
  chat, ROI dashboard, compliance packs, agentic annual review (basic).

**Explicitly out:** customer-facing AI text, CSV/Excel customer uploads, AML/KYC, lifetime PD / IFRS 9 ECL engine,
collections priority (roadmap), nationality-based scenarios, conventional (non-Islamic) wording.

## Vision

In 2–3 years, AI Risk Score Card becomes the risk-AI platform for GCC Islamic and conventional banks
(Qatar, Saudi Arabia, other GCC next, with a pluggable regulator layer per country). The next modules are retail
collections & recoveries, credit administration (document AI, covenant tracking), continuous model
validation, then operational risk & fraud. Each runs on-premise under the same principle: AI changes the
workload of risk, never the ownership of it.
