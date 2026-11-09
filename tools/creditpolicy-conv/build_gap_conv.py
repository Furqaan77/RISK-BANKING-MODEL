# Builds the Benchmark & Gap Report (Markdown + HTML for PDF) for the UAE CONVENTIONAL BANK retail credit policy.
# Source of truth: credit-policy-uae-conventional/03-parameter-sheet.md (ratings final: Near 46, Lenient edge 4, No peer 5, n/a 1).
import html, pathlib, sys

OUT_MD = pathlib.Path(sys.argv[1])
OUT_HTML = pathlib.Path(sys.argv[2])

def pv(pay, rate, n):
    r = rate / 12
    return pay * (1 - (1 + r) ** -n) / r

def aed(x):
    return "AED {:,.0f}".format(x)

# ---------- worked examples (computed) ----------
HOME_FIN_10K = pv(5000, 0.06, 300)      # 10k salary, 50% DBR, ~6% stressed, 25 yrs
HOME_FIN_125K = pv(6250, 0.06, 300)
HOME_FIN_15K = pv(7500, 0.06, 300)
AUTO_INST = (100000 + 100000 * 0.0249 * 5) / 60   # AED 100k, 2.49% flat, 60 months
AUTO_MONTHS_15 = 15000 / AUTO_INST
AUTO_MONTHS_20 = 20000 / AUTO_INST
AUTO_5K_DBR = 2500                                  # 50% DBR headroom at 5k with no other debts
GOLD_CALL_DROP = (1 - 0.70 / 0.80) * 100
GOLD_SALE_DROP = (1 - 0.70 / 0.85) * 100
EOS_DAILY = 12000 * 12 / 365
EOS = 135 * EOS_DAILY

# ---------- items (from 03-parameter-sheet.md) ----------
# (group, id, item, policy criterion, conventional top five, rating, tag)
N, L, P, NA = "Near", "Lenient edge", "No peer product", "n/a"
SPLIT31 = "Lenient edge (nationals) / Near (expats)"
G1, G2, G3, G4, G5, G6, G7, G8 = ("General (all products)", "Personal loan: salary-assigned", "Personal loan: unsecured (no STL)",
                                  "Buyout, top-up, rescheduling", "Credit cards", "Home loans (conventional mortgage)", "Auto loans", "Other secured")
ITEMS = [
 (G1, "P-01", "Eligible customers", "UAE nationals and UAE-resident expats; non-residents out of scope", "All five lend to both", N, "[I]"),
 (G1, "P-02", "Minimum age", "21 for all products", "18y 6m with guarantor (RAK nationals) / 21 / 21", N, "[I]"),
 (G1, "P-03", "Maximum age at maturity", "PF, cards, auto 65 nationals / 60 expats; home 70 nationals & self-employed / 65 salaried expats; retirees to 70", "PF 70 (Mashreq Emiratis) / 65 / 60 (ADCB); home 70 all (Mashreq) / 65 salaried, 70 SE (ENBD, ADCB) / 60 NR", N, "[I]"),
 (G1, "P-04", "Length of service", "Salary-assigned 3 months; no-STL 6 months; home 6 months + probation", "None (ENBD STL) / 6 months (FAB, Mashreq) / 6; RAK nationals 3", N, "[I]"),
 (G1, "P-05", "Two tracks", "Salary-assigned (STL + EOS undertaking) vs unsecured no-STL", "All five run STL and no-STL variants (ENBD, FAB non-listed, Mashreq NEO, RAK no-STL)", N, "[I]"),
 (G1, "P-06", "Employer categories", "All accepted, tiered A-D for caps and pricing", "Listed / approved vs non-listed tiers at FAB, Mashreq, RAK", N, "[I]"),
 (G1, "P-07", "Debt burden ratio (DBR)", "50% of gross + regular income; retirees 30%; government housing 60%", "Same at all five", N, "[C]"),
 (G1, "P-08", "AECB credit score", ">= 541 (nationals >= 500); no-STL >= 600; knock-outs for arrears, write-offs, enquiry spikes", "Only RAK publishes floors (541 / 300); ENBD uses the score qualitatively", N, "[I]"),
 (G1, "P-09", "Nationality / sector", "No nationality exclusion; sector watch-list with lower caps", "No published nationality bans", N, "[I]"),
 (G1, "P-10", "Bank statements", "3 months or UAEFTS consent (STL); 12 months (no-STL, self-employed)", "3 months (ENBD, FAB, Mashreq / UAEFTS)", N, "[I]"),
 (G1, "P-11", "Self-employed", "Licence >= 2 yrs (PF, auto) / >= 3 yrs (home); avg balance >= 20k (PF), >= 15k (auto); PF max 500k", "ENBD PF 1 yr + 20k (L); home 2-3 yrs + 2 yrs audited", N, "[I]"),
 (G2, "P-12", "Minimum salary", "AED 5,000", "3,000 (RAK nationals) / 5,000 (ENBD, ADCB, Mashreq, RAK) / 7,000 (FAB)", N, "[I]"),
 (G2, "P-13", "Maximum amount", "Lower of 20x income or AED 4m nationals / 2m expats; Cat D max 500k", "Nationals 5m (FAB) / 4m / ~2.25m (RAK); expats 3m (ENBD) / 2m / 1.5m (ADCB)", N, "[I]"),
 (G2, "P-14", "Tenor", "48 months (60 MoD / AF where exempt: verify)", "48 (60 MoD / AF)", N, "[C]"),
 (G2, "P-15", "Interest rate", "Nationals from 5.49%, expats from 5.99%, max 19.99% by AI grade", "Floors: nationals 4.79-5.99% (median 5.24%), expats 4.75-6.49% (median 5.74%); ceilings median 19.99%", "Near (floor ~0.25% above median)", "[I]"),
 (G2, "P-16", "Processing fee", "1% (min 500, max 2,500) + VAT", "1.05% incl. VAT at all five", N, "[C]"),
 (G2, "P-17", "Early settlement", "1% of outstanding, max AED 10,000 + VAT", "1.05% max 10,500 incl. VAT", N, "[C] [CV]"),
 (G2, "P-18", "Late payment fee", "2% of overdue instalment, min AED 50, max AED 200 + VAT", "52.50 (ENBD) / 2%, 52.5-210 incl. VAT (Mashreq, FAB) / 210 + rate step-up (RAK)", N, "[CV] [M]"),
 (G2, "P-19", "Security", "Employer STL on bank format + irrevocable EOS undertaking; WPS verified; +2% p.a. if salary diverted 3 months; security cheque per legal advice", "RAK salary + EOSB transfer + step-up; ADCB salary + EOSB assignment; ENBD security cheque; Mashreq PDCs", N, "[I]"),
 (G2, "P-20", "First-instalment grace (nationals)", "Up to 120 days", "365 (FAB) / 120-180 / 120 (ENBD, Mashreq)", N, "[I]"),
 (G2, "P-20a", "Credit life insurance", "Mandatory credit life cover, premium per tariff (or bank-paid)", "ENBD free; FAB 0.0169% per month; RAK 1.05% upfront; Mashreq free (Emiratis)", N, "[CV]"),
 (G3, "P-21", "Minimum salary", "AED 5,000 with AECB >= 600, employer A-C, 6 months' service, 12 months' salary credits; otherwise AED 10,000", "5,000 + AECB 541 (RAK); Mashreq NEO 5,000 / 8,000-10,000 (Mashreq unapproved, FAB non-listed, ENBD) / 10,000", N, "[I]"),
 (G3, "P-22", "Maximum amount", "Nationals 20x max AED 500k; expats 10x max AED 200k", "RAK identical; FAB non-listed max 500k; Mashreq NEO max 150k", N, "[I]"),
 (G3, "P-23", "Rate & repayment", "9.99-21.99% by grade; UAE direct debit", "FAB non-listed 8.99-11.99%; Mashreq NEO 10.49-17.49%; RAK 12.99-22.49%", N, "[I]"),
 (G4, "P-24", "Buyout", "STL + EOS undertaking; liability letter <= 15 days; pay other bank directly within 30 days; residual after clearance; no fee on pure buyout", "ENBD liability letter, first payment up to 90 days; Mashreq residual after clearance + STL; RAK takeover; FAB liability / clearance letter", N, "[I]"),
 (G4, "P-25", "Top-up", ">= 12 months clean (CBUAE), fresh DBR / AECB, max one per 12 months, fee on increment", "ENBD top-ups (zero fee for nationals); Mashreq fee on increment", N, "[C] [I]"),
 (G4, "P-26", "Rescheduling", "Beyond 48 months only with DBR > 50% and no new money", "Same CBUAE rule at all five", N, "[C]"),
 (G5, "P-27", "Minimum salary", "Entry 5,000; Gold 12,000; Platinum 20,000", "5,000 entry at all five", N, "[I]"),
 (G5, "P-28", "Card limit", "Lower of 3x income (STL) / 2x (no-STL), tier cap, DBR headroom (5% of limit)", "Not published by any of the five", P, "[P]"),
 (G5, "P-29", "Rate & fees", "3.59% per month (premium 3.25%); min payment 5% or AED 100; late fee AED 230 + VAT; entry card free", "3.25% (ENBD, ADCB) / 3.49-3.85% / 3.99% (FAB); min payment 4-5%; late fee 241.50 incl. VAT at four of five", N, "[CV] [M]"),
 (G5, "P-30", "Self-employed", "Avg balance >= 50k over 3 months or deposit-backed card", "ENBD 50k / 3 months; RAK 75k quarterly or 150k turnover", N, "[I]"),
 (G6, "P-31", "Minimum salary", "AED 10,000 nationals (8,000 under government schemes) / 15,000 expats", "Nationals 8k (ADCB) / 10-15k (ENBD 10, Mashreq 15, RAK 15; FAB 15 L) / 15k; expats 15k at all five", SPLIT31, "[I]"),
 (G6, "P-32", "Loan-to-value", "85/80; 75/70 above 5m; 65/60 second home; 50% off-plan", "85/80 at four; RAK 80% for all", N, "[C]"),
 (G6, "P-33", "Tenor", "25 yrs (30 only under the rate-relief exception)", "25 yrs", N, "[C]"),
 (G6, "P-34", "Maximum amount", "AED 20m", "25m (ENBD) / 20m (FAB) / 13m (RAK)", N, "[I]"),
 (G6, "P-35", "Interest rate", "3-yr fixed 4.24% STL / 4.49% no-STL; 5-yr 4.44 / 4.69%; variable 3M EIBOR + 1.59%; reversion + 1.79%; floor 2.99%; SE + 0.25%", "Fixed 3.85-4.69% (median ~4.19%); variable + 1.49-1.69%; floors 1.99-3.99%", N, "[I]"),
 (G6, "P-36", "Fees", "Processing 1% + VAT (min 5,000, max 50,000); valuation 2,500 + VAT; 25% free prepayment; early settlement 1% max 10,000 + VAT; buyout no fee + valuation refund", "Processing 1.05% (ADCB 0.525%, cap 52.5k); valuation 3,150 incl. VAT; prepayment 0-30% (median 20%)", "Near (valuation & prepayment slightly customer-friendly)", "[I]"),
 (G6, "P-37", "DBR stress", "DBR 50% at the higher of initial and reversion rate", "No bank publishes a stress rate (ADCB KFS illustrates +2%)", P, "[P]"),
 (G6, "P-38", "Off-plan", "50%; >= 35% complete; >= 50% paid; approved developers", "Mashreq identical; ENBD via DLD developers; RAK Dubai only", N, "[C] [I]"),
 (G6, "P-39", "Service / self-employed", "Salaried 6 months + probation; SE >= 3 yrs + 2 yrs audited", "ENBD expats >= 3 yrs in UAE + >= 1 yr in job (stricter); SE 2-3 yrs + audited", L, "[I]"),
 (G6, "P-40", "Insurance", "Mandatory life and property insurance, bank beneficiary", "ENBD life 0.0171% per month + property; FAB life 0.0112-0.0132% per month; ADCB via bank", N, "[CV]"),
 (G6, "P-41", "Government schemes", "SZHP, MBRHE, ADHA top-up, Sharjah housing subject to Board; DBR up to 60%", "ENBD SZHP; FAB ADHA / SZHP; Mashreq 85% nationals", N, "[C] [I]"),
 (G6, "P-42", "Non-resident", "Excluded in v1", "50-65% LTV offered", NA, "[I]"),
 (G7, "P-43", "Minimum salary", "AED 5,000", "5k (ADCB, RAK) / 7k (ENBD, FAB, Mashreq) / 7k + STL", L, "[I]"),
 (G7, "P-44", "Down payment / tenor", "20% / 60 months", "20% / 60", N, "[C]"),
 (G7, "P-45", "Maximum amount", "AED 1.5m", "2m (ENBD) / 1.5m (FAB, ADCB) / 0.5m (Mashreq)", N, "[I]"),
 (G7, "P-46", "Rate (flat)", "New 2.49% nationals / 2.69% expats; used 3.19%; EV 1.99%; APR in KFS", "1.75-1.89% (ADCB min, ENBD Emiratis) / 2.15-2.90% / 3.19%+ (Mashreq)", N, "[I]"),
 (G7, "P-47", "Vehicle age", "<= 10 yrs at maturity", "12 yrs (ENBD, ADCB) / 10-12 / 10 (RAK)", "Near (conservative side)", "[I]"),
 (G7, "P-48", "Seller", "Dealer or private sale with approved valuation", "ENBD private sale; ADCB dealer quotation; Mashreq dealer only; RAK dealer or third party", N, "[I]"),
 (G7, "P-49", "Self-employed", "Licence >= 2 yrs; avg balance >= 15k", "ENBD 20k; FAB 25k; RAK >= 1 yr business", L, "[I]"),
 (G7, "P-50", "Security, insurance, settlement", "Vehicle mortgaged with RTA; comprehensive motor insurance (bank first beneficiary, financeable); early settlement 1% max 10,000 + VAT; late fee 2% min 50 max 200 + VAT", "ENBD first-degree mortgage + salary assignment; Mashreq chattel mortgage + EOSB routing; late fees 52.5-525", N, "[CV] [M]"),
 (G8, "P-51", "Deposit-backed", "Loan or overdraft against fixed deposit at 90%; max 10m; 48 months (overdraft 12 months renewable); deposit rate + 2%", "90% (ENBD loan & overdraft, ADCB overdraft, Mashreq Quick Cash) / 95% (FAB)", N, "[I] [CV]"),
 (G8, "P-52", "Gold-backed", "70% max; top-up call 80%; sale 85%; <= 24 months", "None of the five offers it", P, "[I]"),
 (G8, "P-53", "EOSB-backed", "<= 80% of accrued EOSB, only inside salary-assigned, >= 3 yrs' service", "None lends against EOSB; ADCB, Mashreq, RAK take EOSB as added security", "No peer product (in line with how they use EOSB)", "[I]"),
 (G8, "P-54", "Salary advance", "Salary-assigned; <= 50% net salary, max 25,000; <= 35 days; fixed fee 100-250; <= 6 per year", "No published conventional product (DIB, ADIB Islamic only)", P, "[I]"),
]

GROUPS = [G1, G2, G3, G4, G5, G6, G7, G8]
GROUP_SHORT = {G1: "General", G2: "PL salary-assigned", G3: "PL unsecured", G4: "Buyout / top-up", G5: "Cards",
               G6: "Home loans", G7: "Auto loans", G8: "Other secured"}

def classify(r):
    if r == SPLIT31:
        return ["N", "L"]
    if r.startswith("Near"):
        return ["N"]
    if r.startswith("Lenient"):
        return ["L"]
    if r.startswith("No peer"):
        return ["P"]
    return ["NA"]

def counts_for(group):
    c = {"N": 0, "L": 0, "P": 0, "NA": 0}
    for it in ITEMS:
        if it[0] == group:
            for k in classify(it[5]):
                c[k] += 1
    return c

TOTC = {k: sum(counts_for(g)[k] for g in GROUPS) for k in ("N", "L", "P", "NA")}
assert (TOTC["N"], TOTC["L"], TOTC["P"], TOTC["NA"]) == (46, 4, 5, 1), TOTC
assert len(ITEMS) == 55

RANKING = [
 ("1", "Emirates NBD (conventional)", "Group retail & wealth gross loans AED 184bn (Dec-25), incl. Emirates Islamic (retail segment assets ~AED 53bn) → conventional ≈ AED 130bn (approximation)", "ENBD Q4-25 investor presentation; EI FY25 statements [H / approx.]"),
 ("2", "FAB", "≈ AED 94bn personal / retail loans (Dec-25), incl. international books and the small FAB Islamic window", "FAB Sep-26 investor presentation [M, chart labels]"),
 ("3", "ADCB", "≈ AED 75bn \"Personal\" (18% of AED 414bn gross loans), incl. ADCB Islamic; 2.2m+ UAE retail customers", "ADCB FY25 investor presentation [H]"),
 ("4", "Mashreq", "AED 36bn retail banking segment assets (FY25)", "Mashreq FY25 investor presentation [H]"),
 ("5", "RAKBANK", "AED 23.1bn personal banking loans (Q1-25)", "Gulfbase / Zawya [L]"),
]

LENIENT = [
 ("P-31", "Home loan minimum salary for UAE nationals: AED 10,000",
  "ADCB 8k; ENBD 10k; Mashreq 15k; RAKBANK 15k; FAB not published (15k per aggregator). Expats: 15k at all five, which matches the policy.",
  "A 25-year mortgage has to survive rate resets. At AED 10,000 the customer has a thinner buffer for service charges, maintenance and insurance than at the 15k used by Mashreq and RAKBANK.",
  "Keep AED 10,000 (in line with ENBD), or tighten to AED 12,500-15,000 for nationals outside government schemes. Keep AED 8,000 under SZHP / MBRHE / ADHA top-up.",
  "Tightening removes some lower-income national borrowers outside the schemes; the government-scheme channel keeps access for them.",
  "At 50% DBR and a ~6% stressed rate over 25 years: AED 10,000 salary funds about {}; AED 12,500 about {}; AED 15,000 about {}.".format(aed(HOME_FIN_10K), aed(HOME_FIN_125K), aed(HOME_FIN_15K))),
 ("P-39", "Home loan service for salaried expats: 6 months + probation",
  "ENBD requires expats to have >= 3 years in the UAE and >= 1 year in the current job. The other four do not publish a figure.",
  "Recently arrived expats have shorter local credit history and higher job and residence mobility, which raises early-default and repatriation risk on long mortgages.",
  "Option to tighten: 12 months in the current job and >= 3 years' UAE residence (ENBD standard), or keep 6 months but cap LTV at 70% for expats with < 2 years in the UAE.",
  "Tightening excludes new arrivals who can afford a home; the LTV-cap alternative keeps them eligible with more equity at risk.",
  "An expat earning AED 25,000 who arrived 8 months ago passes the current policy at 80% LTV; under the ENBD-style rule they would wait until month 36, or (alternative) borrow at 70% LTV."),
 ("P-43", "Auto loan minimum salary: AED 5,000",
  "ADCB and RAKBANK accept AED 5,000; ENBD, FAB and Mashreq require AED 7,000 (Mashreq also requires salary transfer).",
  "Lower-income car buyers are more exposed to insurance, fuel and maintenance costs on top of the instalment; repossession recoveries on used cars are uncertain.",
  "Keep AED 5,000 (ADCB, RAKBANK level) with salary transfer mandatory below AED 7,000 and a maximum of 10x monthly salary; or tighten to the AED 7,000 median.",
  "Tightening loses the 5-7k segment that two of the five still serve; the STL-plus-cap option keeps them with a stronger repayment source.",
  "At AED 5,000 with no other debts, 50% DBR leaves AED {:,} a month; a AED 50,000 new-car loan at 2.49% flat over 60 months costs about AED {:,.0f} a month.".format(AUTO_5K_DBR, (50000 + 50000 * 0.0249 * 5) / 60)),
 ("P-49", "Self-employed auto loans: average balance AED 15,000",
  "ENBD requires an average balance of AED 20,000; FAB AED 25,000; RAKBANK >= 1 year in business; ADCB eligible without a published figure.",
  "Self-employed income is volatile; the average balance is the main buffer when business receipts fall.",
  "Tighten to AED 20,000 (ENBD level), or keep 15,000 with a 6-month bank-statement turnover test (credits >= 3x the instalment).",
  "Tightening excludes smaller traders; the turnover test keeps them where cash flow is proven.",
  "A AED 100,000 loan at 2.49% flat over 60 months costs about AED {:,.0f} a month: AED 15,000 covers about {:.1f} months of instalments, AED 20,000 about {:.1f} months.".format(AUTO_INST, AUTO_MONTHS_15, AUTO_MONTHS_20)),
]

NOPEER = [
 ("P-28", "Card limit rule (3x income with STL / 2x without)",
  "No conventional top-five bank publishes a limit multiple; limits still count in DBR (5% of the limit).",
  "Gives a consistent, testable ceiling for officers and the AI Risk Score Card; keeps DBR headroom predictable.",
  "Credit Risk to calibrate against the bank's own card book after 6-12 months; growth reviews at 6 and 12 months.",
  "Credit policy approval (Board Risk Committee)."),
 ("P-37", "Home loan DBR at the higher of the initial and reversion rate",
  "No bank publishes a stress rate; ADCB's KFS illustrates a +2% EIBOR shock.",
  "Most fixed teaser rates (3.85-4.69%) sit below the reversion rate (EIBOR + margin ≈ 5.5-6.4% at 3M EIBOR 4.39%), so affordability at the teaser overstates capacity.",
  "Recalculate the stress input monthly from 3M EIBOR; review if EIBOR moves by more than 0.5%.",
  "Credit policy approval; ALCO note on rate assumptions."),
 ("P-52", "Gold-backed lending at 70% (top-up call 80%, sale 85%)",
  "None of the five conventional banks offers it (only Emirates Islamic, at 50%, in the Islamic market).",
  "Serves customers holding gold without selling it; 70% leaves room for price moves: gold can fall {:.1f}% before the call and {:.1f}% before a sale.".format(GOLD_CALL_DROP, GOLD_SALE_DROP),
  "Daily revaluation; custody in the bank's vault or approved certificates; tenor <= 24 months; concentration limit <= 2% of the retail book.",
  "New-product approval (Board), market-risk sign-off for collateral valuation, Legal (pledge enforceability), Operations (custody)."),
 ("P-53", "EOSB-backed advance (<= 80% of accrued EOSB, inside salary-assigned finance only)",
  "No bank lends against EOSB alone; ADCB, Mashreq and RAKBANK take EOSB as additional security, which is how the policy uses it too.",
  "Rewards long-service employees with higher limits secured by an employer undertaking.",
  ">= 3 years' service; irrevocable employer undertaking; yearly recalculation; total within 20x and 48 months.",
  "Legal opinion on the employer undertaking and on employees under the alternative end-of-service savings scheme; product approval."),
 ("P-54", "Salary advance (<= 50% of net salary, max AED 25,000)",
  "No published conventional product among the five (Islamic peers DIB and ADIB offer one).",
  "Low-cost short-term liquidity for salary-assigned customers; competitive against payday-type alternatives.",
  "Fixed fee AED 100-250 disclosed as APR; max 6 per year; blocked with any arrears; repaid from the next salary.",
  "Product approval; Compliance check against CBUAE fee rules and consumer-protection disclosure."),
]

CONVERSIONS = [
 ("Late payment fee (personal and auto loans)", "Islamic: undertaking to donate AED 175 to charity", "Conventional: 2% of the overdue instalment, min AED 50, max AED 200 + VAT, retained as income (market median)"),
 ("Credit card late fee", "Islamic: donation undertaking AED 200", "Conventional: AED 230 + VAT (241.50 incl. VAT), the standard at four of the five"),
 ("Insurance", "Islamic: family takaful, property takaful, motor takaful", "Conventional: credit life insurance (personal loans), life and property insurance (mortgages), comprehensive motor insurance (auto)"),
 ("Deposit-backed lending", "Islamic: Murabaha against a lien on a Wakala deposit", "Conventional: loan or overdraft against a fixed deposit at 90% (overdraft 12 months renewable)"),
 ("Early settlement", "Islamic: 1% max AED 10,000 + VAT via rebate of unearned profit (Ibra)", "Conventional: 1% of outstanding, max AED 10,000 + VAT; no Ibra (interest stops accruing at settlement)"),
 ("Structures and terms", "Murabaha / Tawarruq, IMBT, Istisna'a, profit rate, Sharia committee", "Personal loan, conventional mortgage, auto loan, interest rate; governance by the Board Risk Committee"),
]

# Range charts: (title, unit_fmt, dmin, dmax, lenient(v,label) or None, conservative(v,label) or None, median, recs [(v,label)], note)
CHARTS = [
 ("Personal loan, salary-assigned: minimum salary (AED)", "aed", 2000, 8000, (3000, "RAK nationals"), (7000, "FAB"), (5000, "median"), [(5000, "Policy")], ""),
 ("Personal loan, no salary transfer: minimum salary (AED)", "aed", 4000, 11000, (5000, "RAK, Mashreq NEO"), (10000, "FAB non-listed, ENBD"), ((8000, 10000), "median 8-10k"), [(5000, "Policy with controls"), (10000, "Policy Cat D / AECB 541-599")], "AED 5,000 only with AECB >= 600, Cat A-C employer and 6 months' service."),
 ("Personal loan interest-rate floor, nationals (% reducing)", "pct", 4.5, 6.3, (4.79, "FAB"), (5.99, "Mashreq"), (5.24, "median ADCB"), [(5.49, "Policy")], ""),
 ("Personal loan interest-rate floor, expats (% reducing)", "pct", 4.5, 6.8, (4.75, "RAK"), (6.49, "ADCB"), (5.74, "median FAB"), [(5.99, "Policy")], ""),
 ("Home loan, nationals: minimum salary (AED)", "aed", 6000, 16500, (8000, "ADCB"), (15000, "Mashreq, RAK"), ((10000, 15000), "median 10-15k"), [(10000, "Policy")], "AED 8,000 under government housing schemes."),
 ("Home loan, expats: minimum salary (AED)", "aed", 10000, 20000, None, None, (15000, "all five banks"), [(15000, "Policy")], "All five publish or are reported at AED 15,000 (FAB per aggregator)."),
 ("Auto loan: minimum salary (AED)", "aed", 4000, 8000, (5000, "ADCB, RAK"), (7000, "ENBD, FAB, Mashreq"), (7000, "median"), [(5000, "Policy")], ""),
 ("Auto loan maximum amount (AED million)", "m", 0.3, 2.2, (2.0, "ENBD"), (0.5, "Mashreq"), (1.5, "median FAB, ADCB"), [(1.5, "Policy")], "Higher is more lenient."),
 ("Home loan 3-year fixed rate (%)", "pct", 3.7, 4.85, (3.85, "ADCB package"), (4.69, "RAK"), (4.19, "median (ENBD 2-yr STL)"), [(4.24, "Policy STL"), (4.49, "Policy no-STL")], ""),
 ("Home loan variable margin over EIBOR (%)", "pct", 1.40, 1.78, (1.49, "ENBD, Mashreq"), (1.69, "RAK"), (1.50, "median FAB"), [(1.59, "Policy")], "Margin over 3M EIBOR."),
 ("Credit card interest rate (% per month)", "pct", 3.1, 4.1, (3.25, "ENBD, ADCB"), (3.99, "FAB"), ((3.49, 3.85), "median 3.49-3.85"), [(3.59, "Policy")], ""),
 ("Deposit-backed loan-to-value (%)", "pct0", 85, 97, (95, "FAB"), (90, "ENBD, ADCB, Mashreq"), (90, "median"), [(90, "Policy")], "Higher is more lenient."),
]

def fmt(v, kind):
    if kind == "aed":
        return "{:,.0f}".format(v)
    if kind == "pct":
        return "{:.2f}%".format(v)
    if kind == "pct0":
        return "{:.0f}%".format(v)
    if kind == "m":
        return "{:.1f}m".format(v)
    return "{:g}".format(v)

S1, TEAL, NAVY, MUTED, BAND = "#2a78d6", "#0F7B7B", "#14213D", "#5B6475", "#cfe6e4"

def range_svg(c):
    title, kind, dmin, dmax, len_, con, med, recs, note = c
    W, H, Lm, Rm = 680, 104, 24, 24
    def x(v):
        return Lm + (v - dmin) / (dmax - dmin) * (W - Lm - Rm)
    out = ['<svg viewBox="0 0 {} {}" class="rng" role="img" aria-label="{}">'.format(W, H, html.escape(title))]
    y0 = 52
    out.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#d5dae1" stroke-width="2"/>'.format(Lm, y0 + 5, W - Rm, y0 + 5))
    bottom = []
    if len_ and con:
        a, b = sorted([len_[0], con[0]])
        out.append('<rect x="{:.1f}" y="{}" width="{:.1f}" height="10" rx="3" fill="{}"/>'.format(x(a), y0, max(x(b) - x(a), 3), BAND))
        for v, lab in (len_, con):
            bottom.append((x(v), "{} {}".format(fmt(v, kind), lab), MUTED))
    if med:
        mv, mlab = med
        if isinstance(mv, tuple):
            out.append('<rect x="{:.1f}" y="{}" width="{:.1f}" height="10" rx="2" fill="{}"/>'.format(x(mv[0]), y0, x(mv[1]) - x(mv[0]), TEAL))
            mx = (x(mv[0]) + x(mv[1])) / 2
        else:
            mx = x(mv)
            out.append('<line x1="{:.1f}" y1="{}" x2="{:.1f}" y2="{}" stroke="{}" stroke-width="4"/>'.format(mx, y0 - 4, mx, y0 + 14, TEAL))
            mlab = "{} {}".format(fmt(mv, kind), mlab)
        bottom.append((mx, mlab, TEAL))
    rows_b = []
    for bx, text, col in bottom:
        row = 0
        wtxt = len(text) * 5.6
        while any(abs(bx - ox) < (wtxt + ow) / 2 + 6 for ox, ow, orow in rows_b if orow == row):
            row += 1
        rows_b.append((bx, wtxt, row))
        anchor = "middle"
        if bx - wtxt / 2 < 2: anchor = "start"
        if bx + wtxt / 2 > W - 2: anchor = "end"
        out.append('<text x="{:.1f}" y="{}" font-size="10" fill="{}" text-anchor="{}">{}</text>'.format(bx, 80 + row * 14, col, anchor, html.escape(text)))
    tops = []
    for rv, rlab in recs:
        rx = x(rv)
        s = 6
        out.append('<polygon points="{:.1f},{} {:.1f},{} {:.1f},{} {:.1f},{}" fill="{}" stroke="#fff" stroke-width="1.5"/>'.format(rx, y0 - 8 - s, rx + s, y0 - 8, rx, y0 - 8 + s, rx - s, y0 - 8, S1))
        tops.append((rx, "{}: {}".format(rlab, fmt(rv, kind)), S1))
    rows_t = []
    tops.sort(key=lambda t: t[0])
    for tx, text, col in tops:
        row = 0
        wtxt = len(text) * 5.7
        while any(abs(tx - ox) < (wtxt + ow) / 2 + 6 for ox, ow, orow in rows_t if orow == row):
            row += 1
        rows_t.append((tx, wtxt, row))
        anchor = "middle"
        if tx - wtxt / 2 < 2: anchor = "start"
        if tx + wtxt / 2 > W - 2: anchor = "end"
        out.append('<text x="{:.1f}" y="{}" font-size="10.5" font-weight="600" fill="{}" text-anchor="{}">{}</text>'.format(tx, 28 - row * 14, col, anchor, html.escape(text)))
    out.append('</svg>')
    top_extra = 14 * max([r[2] for r in rows_t] + [0])
    bot_extra = 14 * max([r[2] - 1 for r in rows_b] + [0])
    svg = "".join(out)
    svg = svg.replace('viewBox="0 0 {} {}"'.format(W, H), 'viewBox="0 {} {} {}"'.format(-top_extra, W, H + top_extra + bot_extra), 1)
    return svg

COLS = [("N", "#0ca30c", "Near", "#ffffff"), ("L", "#fab219", "Lenient edge", "#3b2a00"),
        ("P", "#8da2b8", "No peer product", "#ffffff"), ("NA", "#cfd6df", "n/a", "#3b4a5e")]

def stacked_bar_svg():
    W = 680
    total = sum(TOTC.values())
    out = ['<svg viewBox="0 0 {} 62" class="stack" role="img" aria-label="46 near, 4 lenient edge, 5 no peer product, 1 not applicable">'.format(W)]
    xpos = 0
    for k, col, lab, tcol in COLS:
        v = TOTC[k]
        w = v / total * W
        out.append('<rect x="{:.1f}" y="6" width="{:.1f}" height="30" fill="{}"/>'.format(xpos, max(w - 2, 1), col))
        txt = "{} {}".format(v, lab) if w > 70 else str(v)
        out.append('<text x="{:.1f}" y="26" font-size="12" font-weight="700" fill="{}" text-anchor="middle">{}</text>'.format(xpos + w / 2, tcol, txt))
        xpos += w
    out.append('<text x="0" y="56" font-size="10" fill="#5B6475">55 policy items (54 + P-20a); P-31 counted once as Near (expats) and once as Lenient edge (nationals). Small segments: 5 no peer product, 1 n/a.</text>')
    out.append('</svg>')
    return "".join(out)

def chip(r):
    if r == SPLIT31:
        return '<span class="chip lenient">! Lenient edge (nationals)</span> <span class="chip near">&#10003; Near (expats)</span>'
    k = classify(r)[0]
    cls = {"N": ("near", "&#10003;", "Near"), "L": ("lenient", "!", "Lenient edge"), "P": ("nopeer", "&#9675;", "No peer product"), "NA": ("na", "&ndash;", "n/a")}[k]
    note = ""
    if "(" in r:
        note = '<div class="cnote">{}</div>'.format(html.escape(r[r.index("(") + 1:r.rindex(")")]))
    return '<span class="chip {}">{} {}</span>{}'.format(cls[0], cls[1], cls[2], note)

E = html.escape

PEERS = [
 ("Emirates NBD (conventional)", [
   ("Personal loan", "Min salary AED 5,000 with STL (listed and non-listed employers); no minimum service; max AED 4m nationals / 3m expats; 48 months (60 MoD); fixed 4.99-19.99% reducing, variable from 5.24% (EIBOR + margin); processing 1.05% (525-2,625); early settlement 1.05% / max 10,500; late AED 52.50; security cheque; credit life free; DBR 50% (retirees 30%); a higher AECB score can waive STL / listing / service. KFS 08/2025"),
   ("Cards", "Entry about AED 5,000; 3.25% (nationals, premium) / 3.49% per month; minimum 5% or AED 100; late AED 241.50; self-employed average balance >= AED 50k over 3 months. KFS (undated)"),
   ("Home", "Min salary 10k nationals / 15k expats; expats >= 3 yrs in UAE + 1 yr in job; SE company >= 3 yrs + 2 yrs audited; max age 65 salaried / 70 SE; max AED 25m; 85/80; 25 yrs; 2-yr fixed 4.19% STL / 4.59% (Oct-26, broker); variable 1M/3M EIBOR + 1.49%; reversion 1M + 1.99%; processing up to 1.05%; valuation 3,150; 20% free prepayment. KFS 02/2026"),
   ("Auto", "Min salary 7k; self-employed avg balance 20k; age 21-60; max AED 2m; 20% / 60 months; KFS 3.75-9.00% reducing, Emiratis 1.89% flat; vehicle up to 12 yrs; private sale with dealer valuation; late AED 52.5. KFS 07/2025"),
   ("Other secured", "Loan against fixed deposit up to 90%, max AED 20m, 5.99-7.29% (KFS 08/2026); overdraft against FD 90%, 4.75-18% (KFS 09/2025); loan against property nationals 70-85%, expats 80%, 1M EIBOR + 1.99%")]),
 ("FAB", [
   ("Personal loan", "Min salary AED 7,000 (government / semi-government / reputable private employer); non-listed AED 10,000 or acceptable AECB + 6 months' service, max 500k; new-to-country AED 10,000, from 12.75%; age 21+; 6 months' service; max AED 5m nationals / 2m expats; 48 months (60 MoD nationals); nationals 4.79-13.99%, expats 5.74-13.99%, non-listed 8.99% / 11.99%; processing 1.05%; life cover 0.0169% per month; first-instalment grace up to 365 days (nationals)"),
   ("Cards", "Entry AED 5,000; 3.99% per month (all cards), +1% when past due; minimum 5% or AED 100; late AED 241.50. Consolidated KFS Sep-2026"),
   ("Home", "Min salary not published (aggregator 15k); 85/80; max AED 20m; 1-3 yr fixed 3.99%, 5-yr 4.19% (STL + card); variable 3M EIBOR + 1.50% / 1.89%, floor 1.99%; processing 1.05% (min 5,250, waived for salaried to Dec-26); valuation 3,150; 25% free prepayment (variable period). KFS Sep-26; fees Jul-26"),
   ("Auto", "Min salary 7k; self-employed avg balance 25k; max AED 1.5m; 20% / 60 months; 2.15% flat nationals / 2.29% expats with STL + card, 3.19-3.44% otherwise. KFS May-26"),
   ("Other secured", "Loan against fixed deposit up to 95% or AED 5m, 48 months, deposit rate + 2%")]),
 ("ADCB", [
   ("Personal loan", "Min salary AED 5,000, employer listed or eligible for listing [M]; age 21 / 65 nationals, 60 expats [M]; max AED 4m / 1.5m (FAQ about 4 years old) [M]; 6-48 months; nationals from 5.24%, expats from 6.49% (L); processing 1.05%; assignment of salary and EOSB"),
   ("Cards", "Entry AED 5,000 (Lulu Titanium); about 3.25% per month (some cards 3.69%) [M]; minimum 5% or AED 100; late AED 241.50"),
   ("Home", "Min salary 8k nationals / 15k expats; SE average credits AED 75k/month, audited if > 2.5m; age 18 / 65 salaried, 70 SE, 60 non-resident; AED 250k-24m; 85/80; from 3.99%, 3.85% 3-yr package; EIBOR + 1.50-3.50%; processing 0.525-0.7875% incl. VAT, cap AED 52,500; valuation 3,150; 30% free prepayment. KFS Feb-26; schedule of fees Sep-26"),
   ("Auto", "Min salary 5k; self-employed eligible; age 18 / 70 nationals, 65 expats; max AED 1.5m; 1.75-4.99% flat; vehicle <= 12 yrs at maturity; dealer quotation required; late 2.1% (52.5-525). KFS Jan-25"),
   ("Other secured", "Overdraft against fixed deposit 90% (75% cross-currency), deposit rate + 1.5-2%, no fees. KFS Apr-25")]),
 ("Mashreq", [
   ("Personal loan", "Min salary AED 5,000 approved company (STL a requisite); unapproved company AED 8,000 (other pages 10,000); Emiratis AED 10,000, approved employer only; NEO Credit (no STL) AED 5,000, max 150k, 10.49-17.49%; 6 months' service; max AED 3m Emiratis / 2m expats, 20x; 6-48 months (60 MoD); Emiratis 5.99-12.99%, expats 5.99-31.99% reducing; processing 1.05%; early settlement 1.05% / max 10,500; late 2% of overdue (52.5-210); PDCs; EOSB assignment on exit; DBR 50%. KFS rev. 12-Jan-2026"),
   ("Cards", "Cashback AED 5,000; 3.85% per month; minimum 5% of balance; cards KFS effective 13-Jun-2026"),
   ("Home", "Min salary 15k nationals and expats; SE 15k + 2 yrs audited; max age 70 for all (KFS Jun-26); max AED 15m; 85/80; off-plan <= 50% at >= 35% complete; 2-yr fixed 4.49% salaried (Q4-26, broker); variable 3M EIBOR + 1.49%; processing 1.05% uncapped; valuation 2,625; no free prepayment per KFS. KFS 19-Jun-26"),
   ("Auto", "Min salary 7k + mandatory STL; self-employed not offered; max AED 500k; 60 months; from 3.19% flat (5.99-9.99% reducing); dealer only; chattel mortgage; late 2% (52.5-210). KFS Dec-25"),
   ("Other secured", "Quick Cash overdraft against deposit 90%, 4.25-12%. KFS Sep-26")]),
 ("RAKBANK", [
   ("Personal loan", "Expats AED 5,000, approved employer, salary and EOSB transfer, AECB >= 541 (KFS V08/2026); nationals AED 3,000, AECB >= 300, 3 months' service, from 18y 6m with guarantor (KFS V10/2026); no-STL AED 5,000, AECB >= 541, direct debit, nationals 20x max 500k, expats 10x max 200k, 12.99-22.49% (KFS V01/2026); expats 4.75-19.99%, nationals 5.29-19.99%; 48 months (60 AF); processing 1.05%; late AED 210; mandatory insurance 1.05% upfront; +2% p.a. if salary credited < 75% for 3 months"),
   ("Cards", "RED AED 5,000, security cheque equal to the limit; 3.65% per month (+0.5% if minimum missed); minimum 4% or AED 100; late AED 241.50; free for life; self-employed average quarterly balance 75k or turnover 150k. KFS V01/11-2025"),
   ("Home", "Min salary 15k, AECB >= 541; max AED 13m; 80% LTV for all (20% down), 70% above 5m; 3-yr fixed 4.69% salaried; 3M EIBOR + 1.69%, floor 2.49-3.99%; processing 1.05% uncapped; valuation 3,150; no free prepayment. KFS Oct-26"),
   ("Auto", "Min salary 5k; self-employed >= 1 yr in business; max AED 1m; 20% / 60 months; new 2.80-2.90% flat, used 3.00-3.20%; vehicle 10 yrs (legacy rule); dealer or third party; late AED 525. KFS Oct-26"),
   ("Other secured", "Not published")]),
]

SOURCES = [
 ("Ranking", "R1", "ENBD Q4-25 investor presentation", "https://www.emiratesnbd.com/-/media/enbd/files/investor-relations/financial-information/presentations/emiratesnbd_investor_presentation_2025_q4.pdf", "H"),
 ("Ranking", "R8", "Emirates Islamic FY25 financial statements (segment note, for the ENBD-conventional approximation)", "https://www.emiratesislamic.ae/-/media/ei/pdfs/financial-information/annual-report-pdf/2025/financial_statements_2025_eng.pdf", "H"),
 ("Ranking", "R4", "FAB Sep-26 investor presentation", "https://www.bankfab.com/-/media/fab-uds/about-fab/investor-relations/reports-and-presentations/presentations/pdfs/2026/september-2026-investor-presentation.pdf", "M"),
 ("Ranking", "R7", "ADCB FY25 investor presentation", "https://www.adcb.com/en/multimedia/pdfs/2026/february/investor-presentation-FY-2025.pdf", "H"),
 ("Ranking", "R9", "Mashreq FY25 investor presentation", "https://www.mashreq.com/-/jssmedia/pdfs/aboutus/investors/2025/mashreq-investor-presentation-fy2025.ashx", "H"),
 ("Ranking", "R10", "RAKBANK Q1-25 results (Gulfbase)", "https://gulfbase.com/news/rakbank-profits-rise-22-7-in-first-quarter-of-2025/207579", "L"),
 ("Ranking", "R11", "Commercial Bank of Dubai FY25 (not ranked)", "https://focus.hidubai.com/commercial-bank-of-dubai-posts-record-fy2025-profit-as-net-loans-exceed-aed-100b", "L"),
 ("Regulation", "R15", "CBUAE eases mortgage requirements (age cap removed; ES cap)", "https://www.centralbank.ae/media/z31oq5zw/the-central-bank-of-the-uae-eases-mortgage-loan-requirements-for-bank-customers.pdf", "H"),
 ("Regulation", "P1", "Gulf News: UAE scraps minimum salary rule (Nov-2025)", "https://gulfnews.com/business/banking/uae-scraps-minimum-salary-rule-for-loans-what-does-this-really-mean-for-residents-1.500352440", "L"),
 ("Regulation", "R16", "CBUAE base rate raised to 3.90% (Sep-2026)", "https://gulfbusiness.com/en/2026/uae/uae-central-bank-raises-base-rate-to-3-9-after-fed-hike/", "L"),
 ("ENBD", "U-E1", "Personal loan KFS 08/2025", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_personal_loan_fixed_interest_rate.pdf", "H"),
 ("ENBD", "U-E2", "Salary-transfer loans for expats", "https://www.emiratesnbd.com/en/loans/personal-loans/salary-transfer-loans-for-expats", "H"),
 ("ENBD", "U-E3", "Salary-transfer loans for UAE nationals", "https://www.emiratesnbd.com/en/loans/personal-loans/salary-transfer-loans-for-uae-nationals", "H"),
 ("ENBD", "U-E4", "Personal loans hub (AECB waiver, co-applicant)", "https://www.emiratesnbd.com/en/loans/personal-loans", "H"),
 ("ENBD", "U-E5", "Debt burden ratio help page", "https://www.emiratesnbd.com/en/help-and-support/your-debt-burden-ratio", "H"),
 ("ENBD", "U-E6", "Credit card KFS", "https://www.emiratesnbd.com/en/KFS/credit-card", "H"),
 ("ENBD", "U-E8", "yallacompare: ENBD self-employed and non-STL loans", "https://yallacompare.com/uae/en/personal-loans/emirates-nbd-personal-loan-self-employed/", "L"),
 ("ENBD", "S-E1", "Home loans for expatriates", "https://www.emiratesnbd.com/en/loans/home-loans/home-loans-for-expatriates", "H"),
 ("ENBD", "S-E3", "Home loan KFS 02/2026", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_home_loan_fixed_and_variable_interest_rate.pdf", "H"),
 ("ENBD", "S-E5", "Apply for a home loan (eligibility)", "https://www.emiratesnbd.com/en/help-and-support/apply-for-a-home-loan", "H"),
 ("ENBD", "S-E16", "Auto loan KFS 07/2025", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_auto_loan_fixed_interest_rate.pdf", "H"),
 ("ENBD", "S-E18", "Apply for an auto loan", "https://www.emiratesnbd.com/en/help-and-support/apply-for-an-auto-loan", "H"),
 ("ENBD", "S-E22", "Loan against fixed deposit KFS 08/2026", "https://www.emiratesnbd.com/-/media/enbd/files/others/form-center/retail-banking/loan-forms/loan_against_fd_for_individuals.pdf", "H"),
 ("ENBD", "S-E23", "Overdraft KFS 09/2025", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_overdrafts.pdf", "H"),
 ("ENBD", "S-E29", "Mortgease: ENBD Oct-26 pricing", "https://mortgease.ae/market-brief/2026-10-03-emirates-nbd-october-pricing/", "L"),
 ("FAB", "U-F2", "Personal loan", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/personal-loan", "H"),
 ("FAB", "U-F3", "Non-listed company personal loan", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/non-listed-company-personal-loan", "H"),
 ("FAB", "U-F4", "New-to-country / new-to-employment loans", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/new-to-country-employment-loans", "H"),
 ("FAB", "U-F8", "Consolidated credit card KFS Sep-2026", "https://apply.bankfab.com/-/media/fab-uds/personal/key-facts-statements/credit-cards/fab-consolidated-credit-cards-en.pdf", "H"),
 ("FAB", "S-F27", "Home loan", "https://www.bankfab.com/en-ae/personal/mortgages/mortgage-loan-for-residences-investment-in-uae", "H"),
 ("FAB", "S-F28", "Mortgage KFS Sep-26", "https://www.bankfab.com/-/media/fab-uds/personal/key-facts-statements/loans/mortgage-loan-en.pdf", "H"),
 ("FAB", "S-F29", "Fees and charges Jul-26", "https://www.bankfab.com/-/media/fab-uds/personal/charges-and-fees/fees-and-charges-first-abu-dhabi-bank.pdf", "H"),
 ("FAB", "S-F43", "Car loan KFS (salaried) May-26", "https://www.bankfab.com/-/media/fab-uds/personal/key-facts-statements/loans/car-loans-for-salaried-individuals-en.pdf", "H"),
 ("FAB", "S-F44", "Car loan KFS (self-employed) May-26", "https://www.bankfab.com/-/media/fab-uds/personal/key-facts-statements/loans/car-loans-for-self-employed-individuals-en.pdf", "H"),
 ("FAB", "S-F48", "Secured loan against fixed deposit", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/secured-loans", "H"),
 ("FAB", "S-F54", "Paisabazaar: FAB home loan eligibility", "https://www.paisabazaar.ae/mortgage-loan/articles/fab-home-loan-eligibility-in-uae/", "L"),
 ("ADCB", "U-A1", "Personal loan, UAE nationals", "https://www.adcb.com/en/personal/loans/personal-loans/personal-loan-uae-nationals", "M"),
 ("ADCB", "U-A2", "Personal loan, expats", "https://www.adcb.com/en/personal/loans/personal-loans/personal-loan-expats", "M"),
 ("ADCB", "U-A3", "Personal loan FAQ", "https://www.adcb.com/en/get-in-touch/faqs/loans/personal-loan", "M"),
 ("ADCB", "U-A6", "Knowing your credit card details", "https://www.adcb.com/en/consumer-education-awareness/equality-financial-inclusion/knowing-your-credit-card-details", "M"),
 ("ADCB", "S-F1", "Mortgage FAQ (incl. EIBOR table)", "https://www.adcb.com/en/get-in-touch/faqs/loans/mortgage-services.aspx", "H"),
 ("ADCB", "S-F2", "Standard mortgage", "https://www.adcb.com/en/personal/loans/home-loans/standard-mortgage-loan.aspx", "H"),
 ("ADCB", "S-F6", "Mortgage KFS Feb-26", "https://www.adcb.com/en/multimedia/kfs/mortgage-kfs.pdf", "H"),
 ("ADCB", "S-F7", "Schedule of fees Sep-26", "https://www.adcb.com/en/multimedia/sof/cb-sof-current-charges-fees.pdf", "H"),
 ("ADCB", "S-F17", "Car loans", "https://www.adcb.com/en/personal/loans/car-loans/car-loan", "H"),
 ("ADCB", "S-F19", "Car loan KFS Jan-25", "https://www.adcb.com/en/multimedia/kfs/car-loan-kfs.pdf", "H"),
 ("ADCB", "S-F23", "Overdraft against fixed deposits KFS Apr-25", "https://www.adcb.com/en/multimedia/kfs/overdraft-against-fixed-term-deposits-kfs.pdf", "H"),
 ("Mashreq", "U-M1", "Personal loan, new customers", "https://www.mashreq.com/uae/neo/loans/personal-loans/pl-new-customers", "H"),
 ("Mashreq", "U-M2", "Personal loans for Emiratis", "https://www.mashreq.com/uae/emirati-banking/personal-loans-for-emiratis", "H"),
 ("Mashreq", "U-M3", "Personal loan KFS rev. 12-Jan-2026", "https://www.mashreq.com/-/jssmedia/pdfs/neo/loans/kfs-tnc/Mashreq-personal-loans-KFS-english.ashx", "H"),
 ("Mashreq", "U-M4", "NEO Credit", "https://www.mashreq.com/uae/neo/loans/personal-loans/neo-credit-instant-loans", "H"),
 ("Mashreq", "U-M6", "Cashback credit card", "https://www.mashreq.com/uae/neo/cards/credit-cards/cashback-credit-card/", "H/M"),
 ("Mashreq", "S-M1", "Home loans", "https://www.mashreq.com/en/uae/neo/loans/mortage-loans/mashreq-home-loans/", "H"),
 ("Mashreq", "S-M4", "Mortgage KFS 19-Jun-26", "https://www.mashreq.com/-/jssmedia/pdfs/neo/loans/kfs-tnc/Mortgage-KFS-English.ashx", "H"),
 ("Mashreq", "S-M14", "CashIn car loan", "https://www.mashreq.com/uae/neo/loans/car-loans/cashin-car-loan/", "H"),
 ("Mashreq", "S-M15", "Car loan KFS Dec-25", "https://www.mashreq.com/-/jssmedia/pdfs/neo/loans/kfs-tnc/Mashreq-Car-Loan-KFS-EN.ashx", "H"),
 ("Mashreq", "S-M19", "Quick Cash facility KFS Sep-26", "https://www.mashreq.com/-/jssmedia/pdfs/neo/loans/kfs-tnc/quick-cash-facility-kfs-en-ar.ashx", "H"),
 ("Mashreq", "S-M21", "Mortgease: Mashreq Q4 pricing", "https://mortgease.ae/market-brief/2026-10-01-mashreq-q4-pricing-premium-withdrawn/", "L"),
 ("RAKBANK", "U-R1", "Expat personal loan KFS V08/2026", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs088-personal-loan-expat.pdf", "H"),
 ("RAKBANK", "U-R2", "UAE national personal loan KFS V10/2026", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs034-personal-loan-uae-national.pdf", "H"),
 ("RAKBANK", "U-R3", "Non-STL personal finance KFS V01/2026", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs091-personal-finance-nstl-expat.pdf", "H"),
 ("RAKBANK", "U-R6", "RED credit card KFS V01/11-2025", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs012-red-credit-card.pdf", "H"),
 ("RAKBANK", "S-M24", "Home loan", "https://www.rakbank.ae/en/loans/home-loans/home-loan", "H"),
 ("RAKBANK", "S-M25", "Mortgage KFS Oct-26", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs033-term-loan-mortgage-loan1.pdf", "H"),
 ("RAKBANK", "S-M33", "RAKauto loan", "https://www.rakbank.ae/en/loans/auto-loans/rakauto-loan", "H"),
 ("RAKBANK", "S-M34", "Auto loan KFS Oct-26", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs002-auto-loan.pdf", "H"),
 ("RAKBANK", "S-M35", "Auto finance price guide", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---service-and-price-guides/bilingual/006-j00183-sp-vat-autofinance.pdf", "H"),
]

CAVEATS = [
 "Emirates NBD's conventional retail book is an approximation: group retail & wealth gross loans (AED 184bn) less Emirates Islamic's retail segment assets (~AED 53bn, which include some SME). It is still clearly the largest.",
 "FAB's retail book (~AED 94bn) was read from chart labels in the investor presentation (M) and includes international books and the small FAB Islamic window.",
 "ADCB personal-loan and card figures are search-engine extracts (M) because the bank's site blocked automated reading; one ADCB FAQ is about 4 years old. ADCB's book includes ADCB Islamic.",
 "Commercial Bank of Dubai is not ranked: it does not disclose a retail split (AED 105bn gross loans, corporate-led).",
 "ENBD's AED 10,000 non-STL minimum salary and FAB's home-loan minimum salary (15k) come from comparison sites (L). Mashreq's own pages show AED 8,000 and AED 10,000 for unapproved employers.",
 "Card limit multiples, most AECB floors and home-loan stress rates are not published by any of the five; the policy values there are proposals.",
 "Several mortgage rate grids come from broker market briefs (L) and move with EIBOR (3M EIBOR 4.39% on 1-Oct-26; CBUAE base rate 3.90% from 17-Sep-26).",
 "All figures were read on 9 Nov 2026 from the research in ../credit-policy-uae/01-benchmark-unsecured.md and 02-benchmark-secured.md (conventional products only).",
]

TITLE = "UAE conventional bank retail credit policy v0.1 vs the top five conventional UAE retail banks"

# ---------- Markdown ----------
md = []
md.append("# Benchmark & Gap Report: UAE Conventional Bank Retail Credit Policy v0.1\n")
md.append("Prepared 2026-11-09 for the bank's management and credit team. It tests the recommended retail credit criteria (carried over unchanged from the Islamic policy work and converted to conventional structures) against the published criteria of the **top five conventional UAE retail banks**. Source of truth: `03-parameter-sheet.md`. Benchmark data: `01-benchmark-conventional.md`.\n")
md.append("## 1. Executive summary\n")
md.append("**The top five conventional UAE retail lenders** (by retail lending):\n")
md.append("| # | Bank | Retail lending | Source |\n|---|---|---|---|")
for r in RANKING:
    md.append("| {} | {} | {} | {} |".format(*r))
md.append("\nIslamic arms (Emirates Islamic, FAB Islamic, ADCB Islamic) are excluded from the product benchmark. Commercial Bank of Dubai is not ranked (retail split not disclosed).\n")
md.append("**Verdict:** of 55 policy items, **{N} are near** the conventional top five, **{L} sit at the lenient edge** of their range, **{P} have no peer product** among the five, and **{NA} is out of scope**.\n".format(**TOTC))
md.append("**Headline:** every published item sits within the conventional top-five range and nothing is looser than the CBUAE. Four items are at the customer-friendly end and can be tightened; five are proposals or differentiators that need product approval.\n")
md.append("**Lenient-edge items:** " + "; ".join("{} {}".format(a, b) for a, b, *_ in LENIENT) + ".\n")
md.append("**No-peer items:** " + "; ".join("{} {}".format(a, b) for a, b, *_ in NOPEER) + ".\n")
md.append("## 2. Scorecard\n")
md.append("| Product | Near | Lenient edge | No peer product | n/a |\n|---|---|---|---|---|")
for g in GROUPS:
    c = counts_for(g)
    md.append("| {} | {} | {} | {} | {} |".format(GROUP_SHORT[g], c["N"], c["L"], c["P"], c["NA"]))
md.append("| **Total** | **{N}** | **{L}** | **{P}** | **{NA}** |\n".format(**TOTC))
md.append("55 items (54 + P-20a credit life insurance). P-31 is counted once as Near (expats) and once as Lenient edge (nationals).\n")
md.append("## 3. Where the policy stands on key numbers\n")
md.append("| Item | Most lenient | Median | Most conservative | Policy |\n|---|---|---|---|---|")
for c in CHARTS:
    title, kind, dmin, dmax, len_, con, med, recs, note = c
    lt = "{} ({})".format(fmt(len_[0], kind), len_[1]) if len_ else "-"
    ct = "{} ({})".format(fmt(con[0], kind), con[1]) if con else "-"
    mt = med[1] if isinstance(med[0], tuple) else "{} ({})".format(fmt(med[0], kind), med[1])
    rt = "; ".join("{}: {}".format(l, fmt(v, kind)) for v, l in recs)
    md.append("| {} | {} | {} | {} | {} |".format(title, lt, mt, ct, rt))
md.append("")
md.append("## 4. Lenient-edge items: tighten or keep?\n")
for fid, ftitle, peers, risk, opt, trade, example in LENIENT:
    md.append("### {}: {}\n".format(fid, ftitle))
    md.append("- **What the five do:** " + peers)
    md.append("- **Risk:** " + risk)
    md.append("- **Option:** " + opt)
    md.append("- **Trade-off:** " + trade)
    md.append("- **Worked example:** " + example + "\n")
md.append("## 5. No-peer products\n")
md.append("| ID | Product / rule | Market position | Why proposed | Controls | Approvals needed |\n|---|---|---|---|---|---|")
for r in NOPEER:
    md.append("| {} | {} | {} | {} | {} | {} |".format(*r))
md.append("\n## 6. Conventional conversions to confirm\n")
md.append("The credit criteria are unchanged from the recommended Islamic policy. These structure and pricing items were converted to conventional practice and should be confirmed by management.\n")
md.append("| Item | Islamic policy | Conventional policy | Decision |\n|---|---|---|---|")
for r in CONVERSIONS:
    md.append("| {} | {} | {} | Confirm / Change |".format(*r))
md.append("\n## 7. Item-by-item comparison\n")
md.append("Tags: [I] carried over from the recommended Islamic policy; [C] CBUAE rule; [M] conventional top-five median; [P] proposal (no market figure); [CV] converted to conventional practice.\n")
for g in GROUPS:
    md.append("### " + g + "\n")
    md.append("| ID | Item | Policy criterion | Conventional top five | Rating | Tag |\n|---|---|---|---|---|---|")
    for it in ITEMS:
        if it[0] == g:
            md.append("| {} | {} | {} | {} | {} | {} |".format(*it[1:]))
    md.append("")
md.append("## 8. Annex A: peer profiles\n")
for bank, rows in PEERS:
    md.append("### " + bank + "\n")
    md.append("| Product | Published criteria |\n|---|---|")
    for p_, t in rows:
        md.append("| {} | {} |".format(p_, t))
    md.append("")
md.append("**Data caveats**\n")
for c in CAVEATS:
    md.append("- " + c)
md.append("\n## 9. Annex B: sources\n")
md.append("Confidence: H = bank page, KFS or schedule of charges; M = search extract or chart reading; L = broker, aggregator or press. All checked 2026-11-09. Tag prefix U- = `../credit-policy-uae/01-benchmark-unsecured.md`; S- = `../credit-policy-uae/02-benchmark-secured.md`.\n")
md.append("| Group | Tag | Source | URL | Conf. |\n|---|---|---|---|---|")
for s in SOURCES:
    md.append("| {} | {} | {} | {} | {} |".format(*s))
OUT_MD.write_text(("\n".join(md) + "\n").replace(">=", "≥").replace("<=", "≤"), encoding="utf-8")

# ---------- HTML ----------
CSS = """
@page { size: A4; margin: 15mm 13mm 16mm 13mm; @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 8pt "IBM Plex Sans", "Segoe UI", sans-serif; color: #5B6475; } @bottom-left { content: "Benchmark & Gap Report  |  UAE conventional bank retail credit policy v0.1"; font: 8pt "IBM Plex Sans", "Segoe UI", sans-serif; color: #5B6475; } }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }
body { font: 9.6pt/1.5 "IBM Plex Sans", "Segoe UI", sans-serif; color: #14213D; margin: 0; }
h1, h2, h3 { font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif; color: #14213D; break-after: avoid; }
h2 { font-size: 15pt; margin: 22px 0 8px; padding-bottom: 4px; border-bottom: 2px solid #0F7B7B; }
h3 { font-size: 11.5pt; margin: 16px 0 6px; color: #0F7B7B; }
p { margin: 0 0 8px; }
.cover { background: #14213D; color: #fff; padding: 22px 24px 20px; border-radius: 8px; margin-bottom: 14px; }
.cover small { color: #7FC4C4; font-weight: 600; letter-spacing: .1em; font-size: 8pt; }
.cover h1 { color: #fff; font-size: 21pt; margin: 6px 0 4px; line-height: 1.15; }
.cover p { color: #C9D2E0; margin: 0; }
.headline { background: #E3F1F1; border-left: 4px solid #0F7B7B; padding: 10px 14px; margin: 10px 0; font-weight: 600; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 12px; font-size: 8.4pt; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
th { background: #14213D; color: #fff; text-align: left; padding: 5px 6px; font-weight: 600; vertical-align: bottom; }
td { padding: 5px 6px; border-bottom: 1px solid #D5DAE1; vertical-align: top; }
tbody tr:nth-child(even) td { background: #F4F6F9; }
.cmp td:nth-child(1) { white-space: nowrap; font-weight: 600; }
.chip { display: inline-block; border-radius: 10px; padding: 1px 7px; font-size: 7.6pt; font-weight: 700; border: 1px solid; white-space: nowrap; margin: 1px 0; }
.chip.near { background: #E5F6E5; border-color: #0ca30c; color: #0a5c0a; }
.chip.lenient { background: #FFF3D1; border-color: #fab219; color: #5a3d00; }
.chip.nopeer { background: #E8EDF3; border-color: #8da2b8; color: #34465c; }
.chip.na { background: #EEF0F3; border-color: #9AA6BA; color: #44506a; }
.heat td.c { text-align: center; font-weight: 700; }
.heat td.n1 { background: #DDF3DD !important; color: #0a5c0a; }
.heat td.l1 { background: #FFF0C7 !important; color: #5a3d00; }
.heat td.p1 { background: #E1E8F0 !important; color: #34465c; }
.heat td.a1 { background: #EEF0F3 !important; color: #44506a; }
.heat td.z { color: #9AA6BA; }
.legend { display: flex; gap: 18px; font-size: 8.5pt; color: #5B6475; margin: 4px 0 8px; flex-wrap: wrap; align-items: center; }
.legend i { display: inline-block; vertical-align: middle; margin-right: 5px; }
.rngbox { break-inside: avoid; border: 1px solid #D5DAE1; border-radius: 6px; padding: 8px 10px 4px; margin: 0 0 8px; }
.rngbox h4 { margin: 0 0 2px; font: 600 9.6pt "Plus Jakarta Sans", "Segoe UI", sans-serif; }
.rngbox .note { font-size: 8pt; color: #5B6475; margin: 0 0 2px; }
svg.rng { width: 100%; height: auto; display: block; font-family: "IBM Plex Sans", "Segoe UI", sans-serif; }
svg.stack { width: 100%; height: auto; display: block; font-family: "IBM Plex Sans", "Segoe UI", sans-serif; }
.gap { break-inside: avoid; border: 1px solid #D5DAE1; border-left: 5px solid #fab219; border-radius: 6px; padding: 10px 14px; margin: 0 0 10px; }
.gap h3 { margin-top: 0; color: #14213D; }
.gap dl { display: grid; grid-template-columns: 140px 1fr; gap: 4px 12px; margin: 0; font-size: 8.9pt; }
.gap dt { font-weight: 700; color: #0F7B7B; }
.gap dd { margin: 0; }
.ex { background: #F4F6F9; border-radius: 4px; padding: 6px 8px; }
.pb { break-before: page; }
.small { font-size: 8pt; color: #5B6475; }
.url { word-break: break-all; font-size: 7.4pt; }
.peer { break-inside: avoid; }
.peer td:first-child { width: 95px; font-weight: 600; }
.tags { font-size: 8.3pt; color: #44506a; }
.heat td:first-child, .np td:first-child { white-space: nowrap; }
.cnote { font-size: 7.4pt; color: #5B6475; margin-top: 2px; line-height: 1.3; }
.keep { break-inside: avoid; }
"""

h = []
h.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Benchmark &amp; Gap Report: UAE Conventional Bank Retail Credit Policy</title>')
h.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">')
h.append('<style>' + CSS + '</style></head><body>')
h.append('<div class="cover"><small>BENCHMARK &amp; GAP REPORT &middot; 9 NOVEMBER 2026</small><h1>{}</h1>'.format(E(TITLE)) +
         '<p>The recommended retail credit criteria, converted to conventional structures, compared with the published criteria of Emirates NBD (conventional), FAB, ADCB, Mashreq and RAKBANK. For management and the credit team.</p></div>')
h.append('<h2>1. Executive summary</h2>')
h.append('<p><b>The top five conventional UAE retail lenders</b>, ranked by retail lending:</p>')
h.append('<table><thead><tr><th>#</th><th>Bank</th><th>Retail lending</th><th>Source</th></tr></thead><tbody>')
for r in RANKING:
    h.append('<tr><td>{}</td><td><b>{}</b></td><td>{}</td><td class="small">{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
h.append('<p class="small">Islamic arms (Emirates Islamic, FAB Islamic, ADCB Islamic) are excluded from the product benchmark. Commercial Bank of Dubai is not ranked because it does not disclose a retail split. The Emirates NBD conventional figure is an approximation (group retail book less Emirates Islamic\'s retail segment).</p>')
h.append('<p><b>Verdict.</b> Of 55 policy items, <span class="chip near">&#10003; {N} Near</span> <span class="chip lenient">! {L} Lenient edge</span> <span class="chip nopeer">&#9675; {P} No peer product</span> <span class="chip na">&ndash; {NA} n/a</span>. '.format(**TOTC) +
         'The recommended criteria match the conventional market on eligibility, DBR, tenors, loan-to-value, salary-assigned and unsecured personal loans, cards, pricing and fees. '
         'Four items sit at the customer-friendly end of the range; five are products or rules that none of the five publishes.</p>')
h.append('<div class="keep"><p><b>Lenient-edge items</b> (inside the range, at the lenient end)</p><table class="np"><thead><tr><th>ID</th><th>Item</th><th>Option to tighten</th></tr></thead><tbody>')
for fid, ftitle, peers, risk, opt, trade, example in LENIENT:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td></tr>'.format(fid, E(ftitle), E(opt)))
h.append('</tbody></table></div>')
h.append('<div class="keep"><p><b>No-peer items</b> (proposals or differentiators)</p><table class="np"><thead><tr><th>ID</th><th>Item</th><th>Approval needed</th></tr></thead><tbody>')
for r in NOPEER:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td></tr>'.format(r[0], E(r[1]), E(r[5])))
h.append('</tbody></table></div>')
h.append('<div class="headline">Every published item sits within the conventional top-five range, and nothing is looser than the CBUAE.</div>')
h.append('<h2>2. Scorecard</h2>')
h.append(stacked_bar_svg())
h.append('<table class="heat"><thead><tr><th>Product</th><th style="text-align:center">&#10003; Near</th><th style="text-align:center">! Lenient edge</th><th style="text-align:center">&#9675; No peer product</th><th style="text-align:center">&ndash; n/a</th></tr></thead><tbody>')
for g in GROUPS:
    c = counts_for(g)
    h.append('<tr><td><b>{}</b></td><td class="c {}">{}</td><td class="c {}">{}</td><td class="c {}">{}</td><td class="c {}">{}</td></tr>'.format(
        E(GROUP_SHORT[g]), "n1" if c["N"] else "z", c["N"], "l1" if c["L"] else "z", c["L"], "p1" if c["P"] else "z", c["P"], "a1" if c["NA"] else "z", c["NA"]))
h.append('<tr><td><b>Total</b></td><td class="c n1">{N}</td><td class="c l1">{L}</td><td class="c p1">{P}</td><td class="c a1">{NA}</td></tr>'.format(**TOTC))
h.append('</tbody></table><p class="small">55 items (54 + P-20a credit life insurance). P-31 (home-loan minimum salary) is Near for expats and Lenient edge for nationals, so it is counted once in each. P-42 (non-resident) is out of scope.</p>')
h.append('<h2 class="pb">3. Where the policy stands on key numbers</h2>')
h.append('<p>Each strip runs between the most lenient and most conservative of the five conventional banks. The teal mark is the median. Values are as published (checked 9 Nov 2026).</p>')
h.append('<div class="legend"><span><i style="width:22px;height:9px;background:{};border-radius:2px"></i>Top-five range</span>'
         '<span><i style="width:4px;height:14px;background:{}"></i>Median (bar = median band)</span>'
         '<span><i style="width:10px;height:10px;background:{};transform:rotate(45deg)"></i>Policy value</span></div>'.format(BAND, TEAL, S1))
for c in CHARTS:
    note = c[8]
    h.append('<div class="rngbox"><h4>{}</h4>{}{}</div>'.format(E(c[0]), '<p class="note">' + E(note) + '</p>' if note else '', range_svg(c)))
h.append('<h2 class="pb">4. Lenient-edge items: tighten or keep?</h2>')
h.append('<p>These four items are inside the conventional range but at the customer-friendly end. Keeping them supports growth and inclusion; tightening brings them to the median for a more conservative appetite.</p>')
for fid, ftitle, peers, risk, opt, trade, example in LENIENT:
    h.append('<div class="gap"><h3>{}: {}</h3><dl>'.format(fid, E(ftitle)))
    h.append('<dt>What the five do</dt><dd>{}</dd>'.format(E(peers)))
    h.append('<dt>Risk</dt><dd>{}</dd>'.format(E(risk)))
    h.append('<dt>Option</dt><dd><b>{}</b></dd>'.format(E(opt)))
    h.append('<dt>Trade-off</dt><dd>{}</dd>'.format(E(trade)))
    h.append('<dt>Worked example</dt><dd class="ex">{}</dd>'.format(E(example)))
    h.append('</dl></div>')
h.append('<h2>5. No-peer products</h2>')
h.append('<p>None of the five conventional banks publishes these products or figures. They are proposals carried over from the recommended policy and need product approval before launch.</p>')
h.append('<table class="np"><thead><tr><th style="width:6%">ID</th><th style="width:16%">Product / rule</th><th style="width:20%">Market position</th><th style="width:21%">Why proposed</th><th style="width:20%">Controls</th><th>Approvals needed</th></tr></thead><tbody>')
for r in NOPEER:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
h.append('<h2>6. Conventional conversions to confirm</h2>')
h.append('<p>The credit criteria are unchanged from the recommended Islamic policy. These structure and pricing items were converted to conventional practice and should be confirmed by management.</p>')
h.append('<table><thead><tr><th style="width:18%">Item</th><th style="width:30%">Islamic policy</th><th>Conventional policy</th><th style="width:13%">Decision</th></tr></thead><tbody>')
for r in CONVERSIONS:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>&#9744; Confirm<br>&#9744; Change</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
h.append('<h2 class="pb">7. Item-by-item comparison</h2>')
h.append('<p class="tags">Tags: [I] carried over from the recommended Islamic policy &middot; [C] CBUAE rule &middot; [M] conventional top-five median &middot; [P] proposal (no market figure) &middot; [CV] converted to conventional practice.</p>')
for g in GROUPS:
    h.append('<h3>{}</h3>'.format(E(g)))
    h.append('<table class="cmp"><thead><tr><th style="width:6%">ID</th><th style="width:14%">Item</th><th style="width:30%">Policy criterion</th><th style="width:30%">Conventional top five</th><th style="width:13%">Rating</th><th style="width:7%">Tag</th></tr></thead><tbody>')
    for it in ITEMS:
        if it[0] == g:
            h.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                it[1], E(it[2]), E(it[3]), E(it[4]), chip(it[5]), E(it[6])))
    h.append('</tbody></table>')
h.append('<h2 class="pb">8. Annex A: peer profiles</h2>')
h.append('<p class="small">Published conventional criteria as read on 9 Nov 2026. KFS = key facts statement. [M] = search extract; (L) = aggregator or broker.</p>')
for bank, rows in PEERS:
    h.append('<div class="peer"><h3>{}</h3><table><tbody>'.format(E(bank)))
    for p_, t in rows:
        h.append('<tr><td>{}</td><td>{}</td></tr>'.format(E(p_), E(t)))
    h.append('</tbody></table></div>')
h.append('<h3>Data caveats</h3><ul>')
for c in CAVEATS:
    h.append('<li>{}</li>'.format(E(c)))
h.append('</ul>')
h.append('<h2 class="pb">9. Annex B: sources</h2>')
h.append('<p class="small">Confidence: H = bank page, KFS or schedule of charges; M = search extract or chart reading; L = broker, aggregator or press. All checked 9 Nov 2026. Tag prefix U- = 01-benchmark-unsecured.md; S- = 02-benchmark-secured.md (in ../credit-policy-uae/).</p>')
h.append('<table><thead><tr><th style="width:11%">Group</th><th style="width:7%">Tag</th><th style="width:28%">Source</th><th>URL</th><th style="width:6%">Conf.</th></tr></thead><tbody>')
for s in SOURCES:
    h.append('<tr><td>{}</td><td>{}</td><td>{}</td><td class="url">{}</td><td>{}</td></tr>'.format(*[E(x) for x in s]))
h.append('</tbody></table>')
h.append('</body></html>')
OUT_HTML.write_text("".join(h).replace("&gt;=", "≥").replace("&lt;=", "≤"), encoding="utf-8")
print("ok", TOTC)
