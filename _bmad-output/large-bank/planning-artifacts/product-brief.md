---
title: AI Risk Score Card Global
type: product-brief
created: 2026-11-07
status: final
sources:
  - _bmad-output/large-bank/planning-artifacts/discovery-answers.md (24 rounds, 94 on-screen questions)
  - _bmad-output/large-bank/planning-artifacts/jurisdiction-comparison.md
  - docs/regulatory/large-bank/us-federal-and-new-york.md
  - docs/regulatory/large-bank/uk-prudential-and-conduct.md
  - research/ (transcript, corporate credit framework, AI-in-risk research)
---

# Product Brief: AI Risk Score Card Global

## Executive Summary

**AI Risk Score Card Global** is an on-premise AI credit-risk platform for **large US and UK banks** (GSIB scale; New York and
London). It is a separate product from the UAE Islamic edition. The pitch is direct: **"Better than your champion model."**
It runs beside the bank's existing scorecards and decision engines (FICO, Experian PowerCurve, SAS, Pega, in-house) and
proves, on the bank's own history, that it is more accurate, approves more good customers at the same loss, is fairer, and is
easier to explain and validate. It can then act as a challenger, an add-on scoring service, or a full decision engine.

It covers cards, personal loans and salary advances, mortgages, SME and corporate lending (plus auto, UK overdrafts and UK BNPL in
a later release). It encodes two regulator packs from day one: **US** (Fed/OCC/CFPB rules, New York law, state AI laws) and **UK**
(PRA, FCA, Consumer Duty, UK GDPR). Around the core it adds twelve value-added services: an **inclusion engine** for blue-collar,
thin-file and Gen Z customers, a **macro and climate stress engine** (war, disasters, recession, redundancy), **fair-lending and
less-discriminatory-alternative search**, a **validator in a box** for the bank's own models, a **risk-vs-opportunity frontier**, a
product designer, next-best-offer, collections cure, document AI, fraud consistency checks, a notice generator and a policy copilot.

**Principle:** *AI recommends; the bank sets where automation is allowed; people stay accountable.*

## The Problem

- **Champion models leave money and customers behind.** Bureau-centric scorecards decline thin-file, gig, blue-collar and young
  customers who repay well, and miss early stress in the existing book.
- **Risk is shown without opportunity.** Credit committees see loss forecasts but rarely the profit and inclusion they give up.
- **Regulation is heavy and moving.** US: Reg B reasons, FCRA, CARD Act, ATR/QM, state AI laws, Reg B litigation. UK: CONC 5.2A
  affordability, Consumer Duty, UK GDPR automated-decision safeguards, SS1/23 model risk. Models must be explainable and fair, and
  validation queues are long.
- **External shocks arrive faster than annual reviews.** War, sanctions, natural disasters, recessions and sector layoffs hit
  borrowers before delinquency shows.
- **Data cannot leave the bank.** Cloud scoring of customer data meets residency, third-party and security objections.

## The Solution

- **Challenger first:** back-test on 3–5 years of bank history (including rejects), then a 6-month shadow run beside the
  champion, then limited live use. The champion-vs-challenger report is the sales proof.
- **Decision core per market:** policy and regulator rules; UK two-limb assessment (credit risk + affordability); US CARD Act
  ability-to-pay and ATR/QM; PD, LGD, EAD and expected loss; mapping to the bank's master scale; deterministic reason codes; two
  scores (through-the-cycle for decisions, point-in-time macro-adjusted, refreshed daily).
- **Model choice under the bank's model-risk rules:** constrained gradient boosting, explainable boosting/GAM and a logistic
  scorecard. The best on accuracy and fairness wins, and nothing runs without the bank's model-risk approval.
- **Growth with control:** inclusion scoring (cash flow, rent, utilities, Open Banking, smoothed and seasonal income), Gen Z
  readiness from 16 (no credit before 18; non-credit loyalty), a starter card (UK £250–£1,000 / US $300–$1,500), a one-month salary
  advance (up to 50% of net pay), a product designer and next-best-offer, all inside affordability and fair-value rules.
- **See the next crisis first:** a regulator, event, climate and custom scenario engine; physical climate risk on collateral; a
  sector and job-loss early warning; collections cure and forbearance.
- **Regulator-ready:** notice content (US adverse action in English/Spanish; UK decline and Art 22C rights in English/Welsh)
  generated for the bank to send, fairness reports, SR 26-2 and SS1/23 documentation, DPIA, TPRM/SS2/21 packs.
- **Fits any GSIB stack:** real-time API (p95 < 300 ms), nightly batch (50M+ accounts), Kafka streaming, SFTP for pilots;
  Kubernetes/OpenShift; SSO; bank HSM; separate US and UK installs; air-gap capable.

## What Makes This Different

1. **Beats the champion on four measures at once:** accuracy, approvals at equal loss, fairness, and stability/explainability.
2. **Shows opportunity, not only risk:** the efficient frontier, opportunity-loss segments and a recommended policy within appetite.
3. **Inclusion that is safe and legal:** blue-collar, gig, thin-file and Gen Z customers, with affordability first.
4. **Macro, climate and event early warning** on the whole book, on-premise.
5. **Validator in a box:** shortens the bank's model validation for our models and theirs.

## Who This Serves

Underwriters and credit officers (retail and commercial); risk strategy and policy teams; model risk and validation; collections and
fraud; the CRO and the board. Secondary: compliance, data protection, procurement/TPRM, information security, regulators.

## Success Criteria

- Pilot: on the bank's own history, the challenger beats the champion out-of-time on Gini, gives more approvals at equal expected
  loss, has equal or better fairness metrics, and passes the bank's model-risk validation.
- More blue-collar, thin-file and Gen Z customers approved within affordability and risk appetite.
- Real-time p95 < 300 ms; nightly 50M+ accounts.
- Security and compliance packs accepted (SOC 2 Type II, ISO 27001, pen test, TPRM/SS2/21, DPIA).

## Scope

**Product-owner target: everything in v1 within 2–3 months with 14–18 people** (high risk; see the PRD). Delivered in four releases,
built by parallel squads, in strict priority order:
- **R1 Challenger MVP:** cards + personal loans/salary advance, US + UK; rules, affordability/ability-to-pay, PD/LGD/EAD, reasons;
  champion-vs-challenger report; frontier v1; Demo US and UK banks.
- **R2 Pilot-ready:** mortgages; SME and corporate; integrations (API, batch, Kafka, SFTP, bureaus, Open Banking); notices; SSO,
  workflow; governance packs.
- **R3 Growth & macro:** inclusion engine, Gen Z readiness and loyalty, product designer, next-best-offer, stress and climate engine,
  fair-lending/LDA, validator in a box.
- **R4 Operations:** collections cure and forbearance, UK persistent-debt engine, auto/overdraft/BNPL, document AI, fraud
  consistency, policy copilot.

**Out:** credit to minors; marketing credit to minors; fraud decisions (flags only, handed to the bank); lifetime PD; sending notices
ourselves; capital (IRB) calculations; Islamic products (UAE edition).

## Vision

The reference challenger platform for Western banks, then other jurisdictions (EU, Canada, Australia) through new regulator packs,
and further risk-function modules (collections at scale, credit administration, model risk, operational risk). Each runs inside the
bank, where AI changes the workload of risk but never its ownership.
