# Jurisdiction Comparison: New York (Fed/OCC/CFPB) vs London (Bank of England PRA/FCA)

For: **AI Risk Score Card Global**, an on-premise AI credit decision-support product for a large (GSIB) bank.
Research date: 2026-11-07. Based on two sourced research reports (US federal + New York; UK). Not legal advice.

## Bottom line

**Recommendation: London (UK: PRA + FCA, with the Bank of England) as the first market.**

The US is *lighter on paper* right now because of 2025–26 deregulation. The UK is *easier to execute and safer to build for*: one national
rulebook, a technology-neutral regulator with a supervised AI testing route, mature Open Banking for thin-file and blue-collar
customers, and no 50-state patchwork or class-action exposure. The UK's extra duties (affordability, Consumer Duty, persistent
debt) are features this product already wants to have, and building them first makes a later US launch straightforward.

## Side-by-side

| Factor | US (New York GSIB) | UK (London GSIB) | Easier |
|---|---|---|---|
| Number of regulators/enforcers | ~12+: Fed, OCC or NYDFS, FDIC, CFPB, NYDFS (Part 500), DOJ, HUD, FTC, NY AG, other state AGs (MA, NJ, CA, CO) | ~8–11: PRA, FCA, BoE FPC, ICO, FOS, CMA, HMT, EHRC, LSB | **UK** |
| Rulebook shape | Federal + 50-state patchwork (usury by charter/state, state AI laws CO 2027 / CA 2027, NJ, NY bills) | One national regime (FCA Handbook, PRA Rulebook, UK GDPR) | **UK** |
| Policy stability | Volatile: Reg B disparate-impact removal (in litigation), SR 11-7 → SR 26-2, Basel endgame re-proposed, leveraged guidance split Fed vs OCC/FDIC, 5-yr ECOA look-back | Active but orderly: Basel 3.1 1 Jan 2027, DUAA ADM in force Feb 2026, CCA reform via FSM Bill | **UK** |
| AI-specific law | None federal. State laws (CO SB 26-189 from 2027, CA ADMT 2027). Preemption push not law | None. FCA Mills Review (Jul 2026): no new AI rules. **FCA AI Live Testing** supervised route | **UK** |
| Automated decisions | No general ADM law federally; CO human-review-on-request (2027) | UK GDPR Art 22A–D (Feb 2026): ADM now allowed with safeguards (info, representations, human intervention, contest) | Even |
| Adverse-action / reasons | **Prescriptive**: Reg B specific principal reasons (≤4), 30/90-day timers; FCRA key factors; risk-based pricing notices; HMDA denial reasons | No statutory reasons notice; CCA s.157 CRA disclosure; Art 22C info rights; FOS expects clear reasons | **UK** |
| Affordability duty | None general (CARD Act ability-to-pay for cards; ATR/QM for mortgages, no DTI cap) | **CONC 5.2A two-limb** (credit risk + affordability), verified income, MCOB 11.6 stress (+1pp min, 5 yrs) | **US** |
| Outcomes regulation | Fair lending (disparate treatment; disparate impact via FHA/state law) | **Consumer Duty** outcomes + cohort monitoring + fair value; Equality Act indirect discrimination | **US** |
| Prescriptive servicing rules | URCCP charge-off 120/180 days | Persistent-debt 18/27/36-month interventions, overdraft repeat-use, CONC 7 forbearance | **US** |
| Model risk guidance | SR 26-2 (Apr 2026): principles-based, explicitly non-enforceable, GenAI out of scope | PRA SS1/23: prescriptive, all decision models incl. vendor & AI/ML, SMF owner | **US** |
| Litigation / redress | Class actions (FCRA $100–1,000 per violation, ECOA punitive), state AGs (MA v. Earnest $2.5M AI case) | FOS up to £455k per complaint; s.140A unfair relationships; s.404 redress schemes (motor finance £9.1bn) | Even (different shapes) |
| Thin-file / blue-collar data | Section 1033 open-banking rule in flux; cash-flow underwriting via aggregators | **Mature Open Banking** (CMA Order 2017) widely used for affordability | **UK** |
| Bias testing data | Reg B limits collecting race data outside mortgages; BISG proxies for testing | **DPA 2018 Sch 1 para 8** allows equality monitoring with safeguards | **UK** |
| Vendor onboarding (GSIB) | 12–24 months; TPRM 2023 guidance; examiner access to vendor; DOJ bulk-data rule; China-origin AI questions | 12–24 months; SS2/21 material outsourcing; register from Mar 2027; SM&CR owner | Even |
| Under-18s / juniors | No credit to minors; CARD Act under-21 needs income or cosigner 21+ | No credit to minors (contract capacity); authorised users from parent accounts | UK slightly |
| Salary advance for blue-collar | Small-dollar rules, MLA 36%, state payday laws | If priced as high-cost short-term credit: price cap 0.8%/day, total cost cap 100% (HCSTC); bank-priced advance fine | Even |

**Score:** UK easier on 8 factors, US easier on 4, 4 even. The US advantages are *substantive and temporary* (deregulation that can swing back,
with a 5-year look-back). The UK advantages are *structural* (one regime, predictable supervision, Open Banking).

## What the UK choice means for the product

- **Two separate outputs:** a credit-risk score **and** an affordability verdict (CONC 5.2A). A good score never overrides failed affordability.
- **Verified income** for every product (Open Banking / CRA / documents). Self-declared income alone is not enough.
- **Meaningful human review** evidenced (time on case, override rate, authority) or full Art 22C safeguards.
- **Consumer Duty outcome monitoring** by customer cohort, including vulnerable customers.
- **Persistent-debt, overdraft repeat-use and forbearance** logic for cards and overdrafts.
- **MCOB 11.6 mortgage stress** (forward curve, +1pp floor, 5 years) and LTI ≥4.5x tagging.
- **PRA SS1/23 model documentation**, including the LLM explainer as an inventoried model.
- **Large exposures** ≤25% Tier 1 (15% G-SII to G-SII); Basel 3.1 attributes from 1 Jan 2027 (data only, not capital).
- **Retail default** definition: 90 DPD, £0 / 0% materiality (stricter than many assume).
- **Decision records kept for 10–20 years** (s.140A and FOS back-book exposure).

## US later (phase 2 market)

The same core plus a US pack: Reg B reason codes (deterministic, ≤4), FCRA notices, CARD Act ability-to-pay, ATR/QM thresholds,
MLA/SCRA rate gates, usury by charter/state, SCCL/legal lending limit/Reg O/Reg W, URCCP, state AI laws (CO, CA), and disparate-impact
testing kept on by default.

## Source reports
The full sourced research for both jurisdictions is in `docs/regulatory/large-bank/` (added after the jurisdiction decision).
