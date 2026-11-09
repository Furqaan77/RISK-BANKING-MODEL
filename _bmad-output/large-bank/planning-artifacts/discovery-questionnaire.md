# AI Risk Score Card Global: BMAD Discovery Questionnaire (large US/UK bank)

Same method as the UAE track. Answers are logged in `discovery-answers.md`. Rounds 1–3 already covered A1–A4 and the jurisdiction decision (US + UK).

## A. Business & positioning
A5 Who buys at a GSIB (CRO, Chief Credit Officer, Head of Retail/Cards, Model Risk, CDO/AI office)? · A6 How do we beat incumbents (FICO, Experian, Zest AI, Upstart, Moody's, in-house teams)? · A7 Pricing (licence per segment, per decision, enterprise) · A8 Pilot structure (shadow/challenger first?) · A9 What must the pilot prove (Gini uplift, approval uplift at same loss, fair-lending, time-to-decision, cost)? · A10 Proof data: public datasets, synthetic, or bank data? · A11 Brand/IP: company entity in US and UK? · A12 Sales path: direct, via consultancies (Big 4), or via core-banking partners?

## B. Scope by segment
B1 Cards: new accounts, CLI/CLD, pre-approved, balance transfer? · B2 Personal loans: unsecured, debt consolidation? · B3 Mortgages: US agency/non-agency/jumbo; UK residential, BTL, second charge? · B4 Auto: direct/indirect (dealer), lease? · B5 Overdrafts (UK arranged/unarranged)? · B6 BNPL (UK regulated from Jul 2026)? · B7 SME: unsecured loans, lines, cards, asset finance, invoice finance? · B8 Corporate: mid-market, large corporate, CRE, leveraged, sponsor-backed? · B9 Salary advance product · B10 Starter card & credit-builder products · B11 Junior/teen readiness · B12 Wealth/private-bank lending (Lombard)? · B13 Collections & forbearance decision support in v1?

## C. Policy & rules
C1 Format of large-bank credit policies (thousands of pages, parameter systems)? · C2 Integrate with existing decision engines (FICO Blaze/Decision Manager, Experian PowerCurve, SAS, Pega) or replace? · C3 Who owns policy changes (1st line) vs approvals (2nd line)? · C4 Delegated authority matrix import · C5 Exceptions/overrides capture · C6 Effective-dated rules and back-testing · C7 Multi-entity (bank, card issuer, non-bank affiliates, ring-fenced bank) · C8 State-by-state US rules (usury, licensing) handled how? · C9 Affordability methodology UK (ONS / bureau expenditure / Open Banking)? · C10 US DTI/residual income policy thresholds · C11 Concentration and risk-appetite limits by segment

## D. Data & integration
D1 Data platforms (Snowflake/Databricks/Teradata/Hadoop/Oracle)? · D2 Real-time channels (APIs from origination platforms) · D3 Bureau integrations (Equifax/Experian/TransUnion; FICO/VantageScore; UK CRA data) · D4 Open Banking / cash-flow data (UK aggregators; US 1033 / aggregators) · D5 Rent & utility data · D6 Transaction/MCC data · D7 Employer/payroll data (income verification, e.g. US The Work Number; UK HMRC/RTI via providers) · D8 Rejected/through-the-door data for reject inference · D9 Volumes (millions of decisions/day?) · D10 History length & default definitions per segment · D11 PII handling, tokenisation · D12 Data residency (US data in US, UK data in UK) · D13 Corporate financial spreading systems (Moody's CreditLens, S&P) · D14 Macro & climate data sources (BoE/Fed scenarios, NGFS, flood/wildfire maps)

## E. Scoring, models & outputs
E1 Score scale & grades (bank master scale?) · E2 PD horizon (12m + lifetime for IFRS 9/CECL?) · E3 LGD/EAD/expected loss outputs? · E4 Model types allowed by bank MRM (GBM with constraints, explainable boosting, logistic) · E5 Challenger mode outputs (side-by-side vs bank champion) · E6 Reason codes (US Reg B ≤4; UK) · E7 Affordability verdict (UK) · E8 Point-in-time vs through-the-cycle PD · E9 Macro overlay mechanics (scenario-conditioned PD) · E10 Fair-lending tests (US AIR/LDA; UK Equality Act) · E11 Retraining cadence & approval · E12 Monitoring & auto-suspension

## F. AI / LLM
F1 LLM jobs (explanations, adverse-action letters?, memos, policy extraction, portfolio chat) · F2 Customer-facing text allowed? (US notices, UK understanding testing) · F3 Model provenance constraints (no China-origin models in US) · F4 GPU availability on-prem at GSIBs · F5 LLM governance pack (SR 26-2 excludes GenAI; SS1/23 includes) · F6 Languages (English; Spanish for US; Welsh for UK?)

## G. UX & operations
G1 Users and roles · G2 SSO (Entra ID/Okta/Ping) · G3 Screens priority · G4 Approval workflows vs bank's own case management · G5 Reporting (MI, board packs, regulator packs) · G6 Accessibility standards · G7 Demo mode

## H. Deployment & security
H1 On-prem vs bank private cloud (Kubernetes/OpenShift) · H2 Two regions (US, UK) separate installs · H3 Certifications (SOC 2 Type II, ISO 27001, pen tests) · H4 SBOM & secure SDLC · H5 Escrow · H6 Incident SLAs (US 4h trigger; UK 2027 reporting) · H7 Support model (US persons / UK-only) · H8 Licensing & IP protection

## I. Governance & compliance
I1 SR 26-2 + SS1/23 documentation packs · I2 TPRM / SS2/21 packs · I3 Consumer Duty outcome MI · I4 Art 22C safeguards workflow · I5 Reg B/FCRA notice generation (who sends?) · I6 HMDA/1071 data support · I7 Fairness reports · I8 Record retention (US 25 months+; UK 10–20 years) · I9 SM&CR owner mapping

## J. Build (BMAD)
J1 Team size and squads · J2 Separate repo from UAE product · J3 Stack (reuse FastAPI + React?) · J4 Cloud-native packaging (Kubernetes) · J5 Releases and phasing with two markets · J6 Testing incl. fair-lending test suites · J7 Definition of done for MVP

## K. Commercial & pilot
K1 Pilot design (back-test, shadow, challenger, limited live) · K2 Success metrics · K3 Contracts (MSA, DPA, indemnities, liability caps) · K4 Insurance (PI/cyber) · K5 Support SLAs · K6 Training
