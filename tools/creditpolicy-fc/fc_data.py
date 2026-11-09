# Single data source for the pilot finance-company parameter sheet and gap report.
# Each item: (group, id, item, policy criterion, finance-company market, top-five banks, rating, tags)
# Tags: B = bank criterion carried over unchanged; C = CBUAE consumer rule (Reg 29/2011, CP Standards);
#       R = Finance Companies Regulation (FCR) rule; A = adjusted for the finance-company market or rules (sign-off);
#       P = proposal (no published market figure).

N = "Near"
T = "Tighter"
E = "Competitive edge"
X = "No FC peer"
R = "Required (FCR)"
O = "Not offered"
RATINGS = [N, T, E, X, R, O]
RATING_TEXT = {
    N: "inside the finance-company range, at or close to the typical value",
    T: "stricter criterion or higher price than the finance-company typical (deliberate)",
    E: "better for the customer than the finance-company typical, still inside the market range",
    X: "no finance company publishes this product or figure; ours is a proposal",
    R: "required by the Finance Companies Regulation; not a market choice",
    O: "not offered in the pilot (not permitted, or deferred to phase 2)",
}

G1 = "1. Licence and prudential rules (finance-company only)"
G2 = "2. General criteria (all products)"
G3 = "3. Personal loan: employer-assigned"
G4 = "4. Personal loan: non-assigned"
G5 = "5. Buyout, top-up, rescheduling"
G6 = "6. Credit cards"
G7 = "7. Auto loans"
G8 = "8. Other secured and short-term credit"
G9 = "9. Pricing, decisions, limits, conduct"
GROUPS = [G1, G2, G3, G4, G5, G6, G7, G8, G9]
GROUP_SHORT = {G1: "Licence & prudential", G2: "General criteria", G3: "PL employer-assigned", G4: "PL non-assigned",
               G5: "Buyout / top-up", G6: "Credit cards", G7: "Auto loans", G8: "Other secured / short-term",
               G9: "Pricing, decisions, conduct"}

ITEMS = [
    # ---- 1. Licence and prudential
    (G1, "F-01", "Licence and product scope",
     "FCR Part I full finance company, conventional only (no Islamic window). Retail finance: personal loans, cards, auto, short-term credit. Mortgage finance not in the pilot. CBUAE no-objection letter before each new product line",
     "Finance House, Deem, Al Ain: conventional full FCs; Tamara: restricted (Part II) BNPL licence; Al Futtaim: captive auto",
     "Bank licence (not comparable)", R, "R"),
    (G1, "F-02", "Capital and leverage",
     "Capital funds AED 150m; liabilities ≤ 100% of capital funds in years 0–2; internal pilot cap: gross retail loans ≤ AED 250m; early warning at 85% of the leverage limit",
     "Sector capital / assets 57.1% (FSR 2025)", "Basel III capital", R, "R/P"),
    (G1, "F-03", "Single borrower and group",
     "≤ 10% (AED 15m) single borrower, ≤ 15% (AED 22.5m) connected group of capital funds; internal cap per individual, all products: AED 1m",
     "Same FCR limits for all FCs", "Large exposure ≤ 25% of Tier 1", R, "R/P"),
    (G1, "F-04", "Board members and related parties",
     "No lending to board members; principal shareholders and affiliates within 10% single / 20% aggregate; related-party screening at onboarding",
     "Same FCR rule for all FCs", "Bank related-party rules", R, "R"),
    (G1, "F-05", "Funding and deposits",
     "No deposits or accounts for individuals, so no deposit-backed loans and no overdrafts. Funding: capital, bank lines, legal-entity deposits (≥ 30 days), securitisation",
     "Deem USD 400m ABS; botim USD 500m bank facility", "Retail deposits", R, "R"),
    (G1, "F-06", "Liquidity",
     "Liquid assets ≥ 10% of total liabilities (internal trigger 12%); disbursement pipeline tied to the treasury buffer",
     "Same FCR rule for all FCs", "Basel liquidity ratios", R, "R/P"),
    (G1, "F-07", "Governance",
     "Board credit committee (≥ 3 members); Board approves the credit approval matrix and creditworthiness procedures and reviews them at least every 2 years; policy reviewed annually",
     "Same FCR rule for all FCs", "Board Risk Committee", R, "R"),
    (G1, "F-08", "Credit bureau",
     "AECB report before every retail credit, any amount; monthly data submission; BNPL obligations counted in DBR",
     "Bureau required; Al Ain prices by AECB score", "Same", R, "R"),

    # ---- 2. General
    (G2, "F-09", "Eligible customers",
     "UAE nationals and UAE-resident expats; non-residents out of scope",
     "Both at all active FCs (Sulfah: nationals only)", "All five lend to both", N, "B"),
    (G2, "F-10", "Minimum age", "21", "18 (digital) / 21 / 23 (Al Ain)", "21", N, "B"),
    (G2, "F-11", "Maximum age at maturity",
     "65 nationals / 60 expats; pension-based lending to 70 (nationals)",
     "70 (Sulfah, gold) / 60–65 / 60", "65 / 60 (ADCB) to 70 (Mashreq)", N, "B"),
    (G2, "F-12", "Length of service",
     "Employer-assigned 3 months; non-assigned 6 months",
     "None (digital) / 6 m expats, 3 m nationals (Al Ain); 6 m (Finance House)", "None to 6 months", N, "B"),
    (G2, "F-13", "Two repayment tracks",
     "Employer-assigned: salary-assignment letter + irrevocable EOS undertaking + UAEDDS on the salary account. Non-assigned: UAEDDS + security cheque",
     "Most FCs take no salary transfer; security cheque or direct debit instead", "Salary transfer (STL) vs no STL", N, "A"),
    (G2, "F-14", "Employer categories",
     "A–D, all accepted; caps for category D", "None published", "Listed / non-listed tiers", X, "B"),
    (G2, "F-15", "DBR and affordability",
     "≤ 50% of gross income (retirees 30%), counting cards at 5% of limit and BNPL; rate-rise stress test; signed affordability summary",
     "50% (regulatory); none stricter published", "Same", N, "C/R"),
    (G2, "F-16", "AECB score floor",
     "Employer-assigned ≥ 541 (nationals 500); non-assigned ≥ 560 (≥ 600 for the AED 5,000 entry); knock-outs: current 30+ DPD, 90+ DPD / write-off / partial settlement in 24 months, court case",
     "No published floors; 'good standing'; Al Ain prices by score", "Only RAKBANK publishes (541)", T, "A"),
    (G2, "F-17", "Bank statements",
     "Employer-assigned 3 months or UAEFTS; non-assigned 6 months (12 where available); self-employed 12 months",
     "3–6 months typical", "3 months (STL)", N, "A"),
    (G2, "F-18", "Self-employed",
     "Licence ≥ 2 years; average balance ≥ AED 20,000 (personal) / 15,000 (auto); personal-loan cap AED 250,000; SME CP Regulation C 2/2026 applies",
     "Mawarid lends to self-employed; Aafaq cards from AED 50k turnover", "ENBD 1 yr + AED 20k", N, "A"),
    (G2, "F-19", "Nationality and sector",
     "No nationality exclusion; sector watch-list lowers caps", "None published", "None published", N, "B"),

    # ---- 3. PL employer-assigned
    (G3, "F-20", "Minimum salary", "AED 5,000", "1,000 (payday WPS) / 5,000 / 8,000–10,000", "5,000 (median)", N, "B"),
    (G3, "F-21", "Maximum amount",
     "Lower of 20× salary and AED 300,000; category D AED 150,000",
     "500k (Sulfah) / 100–250k / 30k (digital); buyouts 320–400k", "2m–4m", N, "A"),
    (G3, "F-22", "Tenor", "48 months", "48 (60 MoD)", "48", N, "C"),
    (G3, "F-23", "Interest rate (reducing)",
     "12.99%–24.99% by AI grade",
     "~14% (Al Ain) / 20–28% / 36–40%", "Medians 5.24% (floor) – 19.99% (ceiling)", E, "A"),
    (G3, "F-24", "Processing fee", "1% (min 500, max 2,500) + VAT", "1% typical; digital 2–4%", "1.05% incl. VAT", N, "C"),
    (G3, "F-25", "Early settlement", "1% of outstanding, max AED 10,000 + VAT", "Same", "Same", N, "C"),
    (G3, "F-26", "Late payment fee", "2% of overdue instalment, min AED 50, max AED 200 + VAT", "2% (50–200) at Finance House and Deem", "Same", N, "C/B"),
    (G3, "F-27", "Security",
     "Salary-assignment letter + EOS undertaking + UAEDDS; security cheque ≤ 120% of the loan, never blank; if the salary account is moved without clearance and no new mandate within 30 days, repriced as non-assigned",
     "Security cheque or direct debit", "Salary transfer + EOSB assignment", N, "A/R"),
    (G3, "F-28", "Credit life insurance", "Mandatory, company as beneficiary, premium in the APR", "Sulfah life cover 2.5%", "ENBD free; RAK 1.05% upfront", N, "B"),
    (G3, "F-29", "First-instalment grace (nationals)", "Up to 60 days", "None published", "120–365 days", X, "A"),

    # ---- 4. PL non-assigned
    (G4, "F-30", "Minimum salary",
     "AED 5,000 with AECB ≥ 600, employer A–C and 6 months of salary credits; otherwise AED 7,000",
     "None (digital) / 5,000 / 8,000 (Al Ain)", "5,000 (RAK) / 8,000–10,000", N, "A"),
    (G4, "F-31", "Maximum amount",
     "Nationals 20× up to AED 250,000; expats 10× up to AED 150,000",
     "250k (Finance House) / 150k (Aafaq) / 100k (Mawarid) / 30k (botim)", "150k–500k", N, "A"),
    (G4, "F-32", "Interest rate (reducing)", "15.99%–29.99% by AI grade",
     "14–24% (Al Ain); 15.99–39.99% (Deem); from 20% (Finance House); 24–28% (Sulfah)", "~9%–22%", N, "A"),
    (G4, "F-33", "Repayment", "UAEDDS mandate + security cheque ≤ 120% of the loan", "Security cheque or direct debit", "UAEDDS", N, "R"),

    # ---- 5. Buyout / top-up
    (G5, "F-34", "Buyout",
     "Employer-assigned track for buyouts over AED 100,000; liability letter ≤ 15 days; pay the other lender directly; written cost comparison; no processing fee",
     "Finance House to 320k; Al Ain to 400k", "ENBD, Mashreq, RAK buyouts", N, "B/C"),
    (G5, "F-35", "Top-up", "Only after ≥ 12 months of clean repayment; fresh DBR and AECB; one per 12 months", "Same CBUAE rule", "Same", N, "C/B"),
    (G5, "F-36", "Rescheduling and deferral",
     "Beyond 48 months only when DBR > 50% and no new money; ≤ 2 deferrals a year (AED 100); rescheduling AED 250",
     "Same caps", "Same", N, "C"),

    # ---- 6. Cards
    (G6, "F-37", "Minimum income", "Entry AED 5,000 (= AED 60,000 a year, the CBUAE card minimum); Gold 12,000; Platinum 20,000",
     "5,000 / 5,000–8,000 / 15,000", "5,000", N, "B/C"),
    (G6, "F-38", "Card limit", "Lower of 3× salary (assigned) / 2× (non-assigned), tier cap (Classic 25k, Gold 60k, Platinum 100k), DBR headroom", "Finance House ≤ 2× salary", "Not published", N, "B/P"),
    (G6, "F-39", "Rate and fees", "3.59% per month (premium 3.25%); minimum payment 5% or AED 100; late fee AED 230 + VAT; entry card free",
     "2.9% (Al Ain) / 3.65–3.99% / 3.99%", "3.25%–3.99%", E, "B"),
    (G6, "F-40", "Self-employed", "Average balance ≥ AED 50,000 over 3 months (no deposit-backed card)", "Aafaq: AED 50k turnover", "ENBD AED 50k", N, "A/R"),

    # ---- 7. Auto
    (G7, "F-41", "Minimum salary", "AED 5,000", "5,000 (Aafaq)", "5,000–7,000", N, "B"),
    (G7, "F-42", "Down payment and tenor", "≥ 20% / ≤ 60 months", "Same", "Same", N, "C"),
    (G7, "F-43", "Maximum amount", "AED 500,000", "1m (Aafaq)", "0.5m–2m", N, "A"),
    (G7, "F-44", "Interest rate (flat)", "New 3.49%, used 4.49%, up to 5.99% by grade (about 6.5%–10.8% reducing)",
     "From 2.5% (Aafaq); 3% (Al Futtaim, captive)", "1.75%–3.19%", T, "A"),
    (G7, "F-45", "Vehicle age", "≤ 10 years at end of loan", "None published", "10–12 years", N, "B"),
    (G7, "F-46", "Seller", "Dealer, or private sale with an approved valuation", "Dealer (captive)", "Dealer or private", N, "B"),
    (G7, "F-47", "Self-employed", "Licence ≥ 2 years; average balance ≥ AED 15,000", "Mawarid lends to self-employed", "AED 20k–25k", N, "B"),
    (G7, "F-48", "Security, insurance, fees",
     "RTA vehicle mortgage; comprehensive insurance; early settlement 1% max 10,000; late fee 2% (50–200) + VAT, below the AED 500 auto cap",
     "Late-fee cap AED 500", "Late fees 52.5–525", N, "B"),

    # ---- 8. Other secured / short-term
    (G8, "F-49", "Gold-backed: LTV and margin", "70% LTV; top-up call at 80%; sale at 85%; ≤ 24 months",
     "Finance House 75% LTV", "None of the five", T, "A"),
    (G8, "F-50", "Gold-backed: price and size", "14.99% reducing; AED 5,000–250,000", "Finance House 16%; AED 5k–500k", "None of the five", E, "A"),
    (G8, "F-51", "EOSB-backed", "Only inside employer-assigned loans; ≤ 80% of accrued EOSB; ≥ 3 years' service", "No FC offers it", "None (EOSB as added security)", X, "B"),
    (G8, "F-52", "Salary advance",
     "Net salary ≥ AED 3,000 via WPS; ≤ 50% of net salary, max AED 5,000; ≤ 35 days; flat fee AED 30 / 60 / 120 + VAT; no interest; ≤ 6 a year",
     "Deem ≤ 50%, cap 1,500, fee 30–75; e& 100–1,500, fee 8%; botim 300–8,000", "No conventional product", N, "A/R"),
    (G8, "F-53", "BNPL (phase 2)",
     "≤ lower of AED 10,000 or 1× net monthly income; ≤ 6 months; no interest; late fee ≤ AED 50 per instalment; total fees ≤ 10%",
     "Tamara ≤ 20,000, 0–1% fee; legal cap 20,000 / 3× income / fees 30%", "Card instalment plans", T, "A/R"),
    (G8, "F-54", "Deposit-backed", "Not offered: finance companies cannot take deposits from individuals", "No FC offers it", "90% at banks", O, "R"),
    (G8, "F-55", "Home finance", "Not in the pilot. Phase 2 only with a mortgage-finance licence and CBUAE no-objection; bank criteria then apply, max AED 3m",
     "Siraj 200k–5m; Amlak exiting", "13m–25m", O, "A"),

    # ---- 9. Pricing, decisions, conduct
    (G9, "F-56", "Risk-based pricing and decisions", "AI grades 1–6 approve, 7–8 refer, 9–10 decline; price by grade within floor and ceiling; floors must cover funding, operating cost, expected loss and return on capital; policy always wins",
     "Al Ain prices by AECB; Deem 15.99–39.99%", "Same structure", N, "B/P"),
    (G9, "F-57", "Delegation of authority", "Scaled to capital: Credit Officer ≤ 100k; Senior ≤ 300k; Head of Credit ≤ 750k; CRO ≤ 1m; Board Credit Committee above and for exceptions",
     "None published", "Bank matrix to AED 4m+", X, "A/R"),
    (G9, "F-58", "Portfolio limits", "Non-assigned ≤ 35% of the personal-loan book; category D ≤ 25%; single employer ≤ 5%; gold ≤ 5%; short-term credit ≤ 2%; AECB 541–599 ≤ 25% of approvals; deviations ≤ 5%",
     "None published", "Bank limits", X, "P"),
    (G9, "F-59", "Consumer protection", "KFS and APR first; 5-business-day cooling-off; cheques ≤ 120%, never blank; disbursement ≤ 10 business days; telemarketing 9am–6pm with consent",
     "Same rules", "Same rules", N, "C"),
    (G9, "F-60", "Provisioning and write-off", "IFRS 9: Stage 2 > 30 DPD; Stage 3 > 90 DPD; write-off ≤ 180 DPD until the CBUAE maximum is confirmed",
     "Sector net NPL 7.1%; Finance House ECL ~21%", "NPL 3.3%, net 1.6%", N, "C/R"),
]

# ---------------- market data for charts ----------------
FC_STATUS = [  # 20 entities on the CB Register Aug-2026 (classification from 01-regulation-and-benchmark.md)
    ("Active retail lenders", 9, "Finance House, Aafaq, Deem, Mawarid, Siraj, Al Ain Finance, botim / CashNow, e&, AMEX (Middle East)"),
    ("Run-off or exiting", 4, "Amlak, Tamweel, Mashreq Al Islami Finance, BMW Albatha"),
    ("No published retail lending", 4, "Gulf Finance Corp, Samaa Finance, FAB Islamic Finance, Emirates Money"),
    ("BNPL (restricted licence)", 1, "Tamara"),
    ("Captive auto", 1, "Al Futtaim Finance"),
    ("SME only (consumer coming)", 1, "Comera Finance"),
]
FC_LOAN_MIX = [  # FSR 2025, finance-company loans by type (shares of ~AED 11.2bn)
    ("Business loans and cards", 71.1),
    ("Real estate", 14.7),
    ("Personal loans", 12.7),
    ("Vehicle loans", 1.5),
]

# (label, group, min, max, note)  group: us | fc | bank | digital
PL_RATES = [
    ("Our FC: employer-assigned", "us", 12.99, 24.99, ""),
    ("Our FC: non-assigned", "us", 15.99, 29.99, ""),
    ("Al Ain Finance", "fc", 14.0, 24.0, ""),
    ("Aafaq (8% flat)", "fc", 14.5, None, "from"),
    ("Deem", "fc", 15.99, 39.99, ""),
    ("Finance House Easy", "fc", 20.0, None, "from"),
    ("Finance House Sulfah", "fc", 24.0, 28.0, ""),
    ("Finance House Payday", "fc", 36.0, None, "flat rate"),
    ("botim Professional (APR)", "digital", 16.0, None, "from"),
    ("Top-5 banks: STL (medians)", "bank", 5.24, 19.99, ""),
    ("Top-5 banks: no STL", "bank", 8.99, 22.49, ""),
]
CARD_RATES = [
    ("Our FC", "us", 3.25, 3.59, ""),
    ("Al Ain Finance", "fc", 2.90, None, ""),
    ("Mawarid", "fc", 3.10, None, ""),
    ("AMEX (Middle East)", "fc", 3.25, None, "approx."),
    ("Finance House", "fc", 3.65, None, ""),
    ("Deem", "fc", 3.75, 3.99, ""),
    ("Aafaq", "fc", 3.99, None, ""),
    ("Top-5 banks", "bank", 3.25, 3.99, ""),
]
# (label, group, value AED, note)
PL_MIN_SALARY = [
    ("Our FC: employer-assigned", "us", 5000, ""),
    ("Our FC: non-assigned (AECB ≥ 600)", "us", 5000, ""),
    ("Our FC: non-assigned (other)", "us", 7000, ""),
    ("Finance House Payday (WPS)", "fc", 1000, ""),
    ("Finance House Easy", "fc", 5000, ""),
    ("Deem", "fc", 5000, ""),
    ("Aafaq", "fc", 5000, ""),
    ("Al Ain Finance", "fc", 8000, ""),
    ("Finance House Sulfah (nationals)", "fc", 10000, ""),
    ("botim Standard", "digital", 0, "none"),
    ("Top-5 banks: STL (median)", "bank", 5000, ""),
    ("Top-5 banks: no STL (typical)", "bank", 10000, "8,000–10,000"),
]
PL_MAX_AMOUNT = [
    ("Our FC: employer-assigned", "us", 300000, ""),
    ("Our FC: non-assigned, nationals", "us", 250000, ""),
    ("Our FC: non-assigned, expats", "us", 150000, ""),
    ("Finance House Sulfah", "fc", 500000, ""),
    ("Al Ain Finance (incl. buyout)", "fc", 400000, ""),
    ("Finance House Easy", "fc", 250000, ""),
    ("Aafaq", "fc", 150000, ""),
    ("Mawarid", "fc", 100000, ""),
    ("botim Professional", "digital", 30000, ""),
    ("RAKBANK no-STL (nationals)", "bank", 500000, ""),
    ("Mashreq NEO (no STL)", "bank", 150000, ""),
]
