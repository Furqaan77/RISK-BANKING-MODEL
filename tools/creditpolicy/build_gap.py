# Builds the Benchmark & Gap Report (Markdown + HTML for PDF) for the UAE retail credit policy.
import html, pathlib, sys

OUT_MD = pathlib.Path(sys.argv[1])
OUT_HTML = pathlib.Path(sys.argv[2])

def pv(pay, rate, n):
    r = rate / 12
    return pay * (1 - (1 + r) ** -n) / r

# ---------- worked examples (computed) ----------
HOME_PAY_5K = 5000 * 0.5
HOME_FIN_5K_STRESS = pv(HOME_PAY_5K, 0.06, 300)
HOME_FIN_5K_TEASER = pv(HOME_PAY_5K, 0.0424, 300)
HOME_PROP_80 = HOME_FIN_5K_STRESS / 0.80
HOME_PROP_85 = HOME_FIN_5K_STRESS / 0.85
HOME_FIN_10K = pv(5000, 0.06, 300)
HOME_FIN_15K = pv(7500, 0.06, 300)
PF_NSTL_DBR = pv(2500, 0.0999, 48)
EOS_DAILY = 12000 * 12 / 365
EOS = 135 * EOS_DAILY
GOLD_CALL_DROP = (1 - 0.70 / 0.80) * 100
GOLD_SALE_DROP = (1 - 0.70 / 0.85) * 100

def aed(x):
    return "AED {:,.0f}".format(x)

# ---------- items (from 03-parameter-sheet.md) ----------
# (group, id, item, user, benchmark, rating, recommended, tag)
N, S, F, NA = "Near", "Slightly off", "Far", "n/a"
ITEMS = [
 ("General (all products)", "P-01", "Eligible customers", "UAE nationals and expats", "All five lend to both", N, "Nationals and UAE-resident expats; non-residents out of scope for v1", "[U] [P]"),
 ("General (all products)", "P-02", "Minimum age", "\"CBUAE limit\" (CBUAE sets none for personal finance)", "18 (ADCB, DIB home) / 21 / 21", S, "21 for all products", "[M]"),
 ("General (all products)", "P-03", "Maximum age at maturity", "\"CBUAE limit\" (none; mortgage age cap abolished 2019)", "PF 70 / 65 nationals, 60 expats / 60. Home 70 all / 70 nationals & self-employed, 65 salaried expats / 60", S, "PF, cards, auto: 65 nationals / 60 expats. Home: 70 nationals & self-employed / 65 salaried expats. Retirees: pension-based to 70 (nationals)", "[M]"),
 ("General (all products)", "P-04", "Minimum length of service", "3 months", "None (ENBD) / 6 months (FAB, Mashreq) / 18 months (FAB Islamic no-STL)", "Near (STL) / Slightly off (no STL, home)", "Salary-assigned 3 months; no-STL 6 months; home 6 months + probation completed", "[U] [A]"),
 ("General (all products)", "P-05", "Salary transfer", "Not required; STL version secured, no-STL version unsecured", "Headline terms need STL; no-STL needs higher salary, higher rate, lower limits", N, "Two tracks: salary-assigned (STL + EOS undertaking) and unsecured no-STL with tighter terms", "[U]"),
 ("General (all products)", "P-06", "Employer categories", "All accepted", "Listed / approved vs non-listed tiers (FAB non-listed 10k, max 500k)", S, "All accepted but tiered: Cat A government / semi-gov / MoD / AF; Cat B listed large private; Cat C other listed; Cat D non-listed", "[U] [A]"),
 ("General (all products)", "P-07", "Debt burden ratio (DBR)", "CBUAE limit", "50% of gross + regular income; retirees 30% (all five)", N, "50% of gross + regular income; retirees 30%; government housing 60%. Basic + housing DBR reported by the model as a risk indicator", "[C] [P]"),
 ("General (all products)", "P-08", "AECB credit score", "Not specified", "Only RAKBANK publishes floors: 541 expats / no-STL, 300 nationals STL", F, "Salary-assigned >= 541 (nationals >= 500); no-STL >= 600; cards, home, auto >= 541; deposit-backed no floor (refer < 541); knock-outs for DPD >= 30, 90+ DPD or write-off in 24 months; > 6 enquiries in 30 days refer", "[P]"),
 ("General (all products)", "P-09", "Restricted nationalities / sectors", "Not specified", "No published nationality bans; EI tightened some employer sectors (2026)", S, "No nationality exclusion (sanctions screening only); sector watch-list with lower caps; Sharia Board guidance", "[P]"),
 ("General (all products)", "P-10", "Bank statements / verification", "Last 12 months + financials if possible", "3 months (salaried STL), 6 months (self-employed, DIB), 2 yrs audited (self-employed home)", N, "Salary-assigned 3 months or UAEFTS consent; no-STL and self-employed 12 months; self-employed home 2 yrs audited", "[A] [U] [M]"),
 ("General (all products)", "P-11", "Self-employed", "Statements + financials", "PF 1-yr business + AED 20k avg balance (ENBD); home 2-3 yrs + 2 yrs audited", S, "Trade licence >= 2 yrs (PF, auto) / >= 3 yrs (home); avg balance >= AED 20k (PF), >= 15k (auto); PF max AED 500k", "[M] [P]"),
 ("Personal finance: salary-assigned", "P-12", "Minimum salary", "AED 5,000", "3,000 (DIB) / 5,000 / 7,000 (FAB)", N, "AED 5,000 nationals and expats", "[U]"),
 ("Personal finance: salary-assigned", "P-13", "Maximum amount", "Not given (CBUAE)", "20x salary; nationals 5m / 4m / 3m; expats 3m / 2m / 1.5m", N, "Lower of 20x gross monthly income or AED 4m nationals / 2m expats; Cat D max AED 500k", "[C] [M]"),
 ("Personal finance: salary-assigned", "P-14", "Maximum tenor", "Not given (CBUAE)", "48 months (60 MoD / AF)", N, "48 months; 60 for MoD / AF where the CBUAE exemption applies", "[C]"),
 ("Personal finance: salary-assigned", "P-15", "Profit rate", "Mid-market", "Floor 4.75 / ~5.24-5.99 / 12.75; ceiling 13.99 / 19.99-21.99 / 31.99", N, "Nationals from 5.49%, expats from 5.99%, up to 19.99% by grade", "[M]"),
 ("Personal finance: salary-assigned", "P-16", "Processing fee", "Mid-market", "1% (min 500, max 2,500) + VAT at all five", N, "1% (min AED 500, max 2,500) + VAT", "[C] [M]"),
 ("Personal finance: salary-assigned", "P-17", "Early settlement", "Mid-market", "1% of outstanding, max AED 10,000 + VAT", N, "1%, max AED 10,000 + VAT, by rebate of unearned profit (Ibra)", "[C] [M]"),
 ("Personal finance: salary-assigned", "P-18", "Late payment", "Mid-market", "Charity AED 100 (ADIB) / 175-210 / 210", N, "Undertaking to donate AED 175 per late instalment", "[M]"),
 ("Personal finance: salary-assigned", "P-19", "Salary assignment & security", "STL confirmation + EOS undertaking", "DIB, RAKBANK, ADCB: salary + EOSB assignment; ENBD security cheque; Mashreq PDCs", N, "Employer STL + irrevocable EOS undertaking; WPS check; +2% p.a. if salary not credited 3 months; security cheque per legal advice", "[U] [P] [M]"),
 ("Personal finance: salary-assigned", "P-20", "First-instalment grace (nationals)", "Not given", "365 (FAB) / 120-210 / 60 days", S, "Up to 120 days for nationals", "[M]"),
 ("Personal finance: unsecured (no STL)", "P-21", "Minimum salary", "AED 5,000", "5,000 + AECB 541 (RAKBANK ref.) / 10,000 (FAB, ENBD) / 15,000 + 18 months (FAB Islamic)", F, "AED 5,000 only with AECB >= 600, Cat A-C employer, >= 6 months' service, 12 months' statements; Cat D or AECB 541-599: AED 10,000", "[A] [M]"),
 ("Personal finance: unsecured (no STL)", "P-22", "Maximum amount", "Not given (CBUAE)", "RAKBANK no-STL: nationals 20x max 500k, expats 10x max 200k; FAB non-listed 500k", S, "Nationals 20x max AED 500k; expats 10x max AED 200k", "[M]"),
 ("Personal finance: unsecured (no STL)", "P-23", "Pricing & repayment", "Mid-market", "FAB non-listed 8.99-11.99%; Mashreq NEO 10.49-17.49%; RAKBANK 12.99-22.49%", N, "9.99%-21.99% by grade; repayment by UAE direct debit; 48 months", "[M] [C]"),
 ("Buyout and top-up", "P-24", "Buyout", "STL confirmation + EOS undertaking", "Liability letter; settle in 30-90 days (ADIB); residual after clearance (Mashreq)", S, "Liability letter <= 15 days old; pay other bank within 30 days; residual after clearance letter; total <= 20x / 48 months; no fee on pure buyout", "[U] [P] [M] [C]"),
 ("Buyout and top-up", "P-25", "Top-up", "Not given (CBUAE)", "Only after >= 12 months clean repayment (CBUAE); top-up Murabaha at ADIB, DIB", N, ">= 12 months clean, fresh DBR and AECB, max one per 12 months, fee on increment only", "[C] [M]"),
 ("Buyout and top-up", "P-26", "Rescheduling", "Not given (CBUAE)", "Beyond 48 months only when DBR > 50%, no new money", N, "As CBUAE (collections policy)", "[C]"),
 ("Islamic credit cards", "P-27", "Minimum salary", "AED 5,000", "5,000 entry at all five; premium 15-35k", N, "Entry AED 5,000; Gold 12,000; Platinum 20,000", "[M]"),
 ("Islamic credit cards", "P-28", "Card limit", "Not given", "Not published by any bank", F, "Lower of 3x gross monthly income (salary-assigned) / 2x (no STL), tier caps, DBR headroom (5% of limit)", "[P]"),
 ("Islamic credit cards", "P-29", "Profit rate & fees", "Mid-market", "Monthly 2.99 / 3.49-3.75% / 3.99%; min payment 5% or AED 100; entry fee free", N, "3.59% per month standard, 3.25% premium; min 5% or AED 100; late donation AED 200; entry card free", "[M]"),
 ("Islamic credit cards", "P-30", "Self-employed card", "Statements + financials", "Avg balance 50k / 3 months (ENBD); 75k avg or 150k turnover (RAKBANK)", S, "Avg balance >= AED 50,000 over 3 months, or deposit-backed card", "[M]"),
 ("Home finance", "P-31", "Minimum salary", "AED 5,000", "Nationals 8k / 10k / 15k; expats 10k / 15k / 20k", F, "AED 10,000 nationals (8,000 under government housing schemes) / AED 15,000 expats", "[A]"),
 ("Home finance", "P-32", "Finance-to-value", "CBUAE", "85/80 at 7 of 8 banks", N, "First home <= 5m 85% nationals / 80% expats; > 5m 75/70; second home 65/60; off-plan 50%", "[C]"),
 ("Home finance", "P-33", "Maximum tenor", "CBUAE", "25 yrs (30 under national rate relief)", N, "25 years (30 only under CBUAE rate-relief exception)", "[C]"),
 ("Home finance", "P-34", "Maximum finance amount", "Not given", "30m (ADIB) / 20-25m / 13m (RAKBANK)", S, "AED 20m", "[M]"),
 ("Home finance", "P-35", "Profit rate", "Mid-market", "3-yr fixed 3.85 / ~4.0-4.3 / 4.69; variable EIBOR + 1.25 / 1.49-1.69; floor 1.99 / 2.5-3.1 / 3.99", N, "3-yr fixed 4.24% (STL) / 4.49%; 5-yr 4.44% / 4.69%; variable 3M EIBOR + 1.59%; reversion + 1.79%; floor 2.99%; self-employed + 0.25%", "[M]"),
 ("Home finance", "P-36", "Fees", "Mid-market", "Processing 1% + VAT (caps 30k-105k or none); valuation 2,500-3,150; free prepayment 0 / 20-30% / 0", N, "Processing 1% + VAT (min 5k, max 50k); valuation AED 2,500 + VAT; 25% free prepayment; ES 1% max 10k + VAT; buyout no fee + valuation refund", "[M]"),
 ("Home finance", "P-37", "DBR & stress", "CBUAE", "50%; no bank publishes a stress rate", S, "DBR 50% assessed at the higher of the initial rate and the reversion rate", "[C] [P]"),
 ("Home finance", "P-38", "Off-plan", "CBUAE", "50%; project >= 35% complete, customer >= 50% paid (DIB, ADIB, Mashreq)", N, "50%; >= 35% complete; customer paid >= 50%; approved developers", "[C] [M]"),
 ("Home finance", "P-39", "Age / service / self-employed", "Not given", "70/65; ENBD expats 3 yrs UAE + 1 yr job; self-employed 2 yrs audited", S, "Age per P-03; salaried 6 months + probation; self-employed >= 3 yrs + 2 yrs audited", "[A] [M]"),
 ("Home finance", "P-40", "Takaful", "Not given", "Life ~0.011-0.025%/month; property ~0.03-0.06% p.a.", S, "Mandatory life and property takaful, bank as beneficiary", "[M]"),
 ("Home finance", "P-41", "Government schemes", "Not given", "SZHP, MBRHE, ADHA top-up, Sharjah housing", S, "Participate subject to Board decision; government housing DBR up to 60%", "[C] [P]"),
 ("Home finance", "P-42", "Non-resident", "Not in scope", "50-65% LTV", NA, "Excluded in v1", "[P]"),
 ("Auto finance", "P-43", "Minimum salary", "AED 5,000", "3k (DIB) / 5k / 7k (ENBD, FAB)", N, "AED 5,000", "[U]"),
 ("Auto finance", "P-44", "Down payment / tenor", "Mid-market", "20% / 60 months everywhere", N, "20% minimum / 60 months maximum", "[C]"),
 ("Auto finance", "P-45", "Maximum amount", "Mid-market", "2m (ENBD) / 1.5m (EI, FAB, ADCB) / 1m (DIB, ADIB)", N, "AED 1.5m", "[M]"),
 ("Auto finance", "P-46", "Profit rate", "Mid-market", "New car flat 1.75-1.89 / 2.15-2.90% / 3.19%+", N, "New 2.49% flat nationals / 2.69% expats; used 3.19%; EV 1.99%; APR in KFS", "[M]"),
 ("Auto finance", "P-47", "Vehicle age", "Mid-market", "12 yrs at maturity (ADCB, ENBD) / 10 yrs (DIB, RAKBANK)", N, "<= 10 years at end of finance", "[M]"),
 ("Auto finance", "P-48", "Seller / valuation", "Mid-market", "Private sale with approved-dealer valuation (ENBD, EI, DIB); dealer only (Mashreq)", N, "Dealer or private sale with bank-approved valuation", "[M]"),
 ("Auto finance", "P-49", "Self-employed", "Statements", "Avg balance 10k (EI) / 20k (ENBD) / 25k (FAB)", S, "Trade licence >= 2 yrs; avg balance >= AED 15,000", "[M]"),
 ("Auto finance", "P-50", "Security, takaful, settlement", "Mid-market", "Car mortgaged; comprehensive takaful; ES lower of 1% or unearned profit + Ibra; charity 100-210", N, "Vehicle mortgaged with RTA; comprehensive motor takaful; ES lower of 1% (max 10k) or unearned profit; late donation AED 175", "[M]"),
 ("Other secured", "P-51", "Deposit-backed", "90% of security", "90% (ENBD, ADCB, Mashreq); 95% (FAB, ADIB)", N, "90%; max AED 10m; 48 months; deposit profit rate + 2%; no minimum salary", "[U] [M]"),
 ("Other secured", "P-52", "Gold-backed", "90%", "Only EI lends: 50% of gold certificates (Priority)", F, "70% maximum; top-up call at 80%, sale at 85%; daily revaluation; <= 24 months; Sharia Board approval", "[A] [P]"),
 ("Other secured", "P-53", "EOSB-backed", "90% of accrued EOSB", "No top-five bank lends against EOSB alone; used as additional security", F, "Only inside salary-assigned finance; <= 80% of accrued EOSB; >= 3 years' service; employer undertaking; yearly recalculation; total <= 20x / 48 months", "[A] [C] [P]"),
 ("Other secured", "P-54", "Salary advance", "(product group)", "DIB FlexiSalary min 2k up to 13k; ADIB Yusr 50% of net salary max 50k <= 51 days", S, "Salary-assigned; min AED 5,000; up to 50% of net salary, max AED 25,000; repaid from next salary; fixed profit AED 100-250; max 6 per year", "[U] [M] [P]"),
]

GROUPS = ["General (all products)", "Personal finance: salary-assigned", "Personal finance: unsecured (no STL)",
          "Buyout and top-up", "Islamic credit cards", "Home finance", "Auto finance", "Other secured"]
GROUP_SHORT = {"General (all products)": "General", "Personal finance: salary-assigned": "PF salary-assigned",
               "Personal finance: unsecured (no STL)": "PF unsecured", "Buyout and top-up": "Buyout / top-up",
               "Islamic credit cards": "Cards", "Home finance": "Home", "Auto finance": "Auto", "Other secured": "Other secured"}

def counts_for(group):
    n = s = f = 0
    for g, i, *_rest in ITEMS:
        if g != group:
            continue
        r = _rest[3]
        if r.startswith("Near (STL)"):
            n += 1; s += 1
        elif r == N: n += 1
        elif r == S: s += 1
        elif r == F: f += 1
    return n, s, f

TOT = [sum(counts_for(g)[k] for g in GROUPS) for k in range(3)]
assert TOT == [31, 17, 6], TOT

FAR = [
 ("P-08", "AECB credit score floor is missing",
  "Only RAKBANK publishes floors (541 for expats and no-STL; 300 for nationals with STL). ENBD uses the score to waive salary-transfer, listing and service requirements. The other banks apply the score internally but do not publish a number.",
  "Without a floor, applicants with poor repayment records at other lenders can qualify on salary alone. Unsecured approvals would carry losses the top five avoid, and decisions would be inconsistent between officers.",
  "Adopt score floors by product: salary-assigned >= 541 (nationals >= 500); unsecured no-STL >= 600; cards, home and auto >= 541; deposit-backed no floor (refer below 541). Add knock-outs: current DPD >= 30; any 90+ DPD, write-off or settlement in 24 months. More than 6 AECB enquiries in 30 days goes to referral.",
  "A small share of thin- or poor-record applicants is declined or referred. In return, unsecured losses stay in line with peers. The AI model's grade still decides inside the floor, so good customers above it are not penalised.",
  "On the ADCB band scale, 300-540 is Poor, 541-650 Fair, 651-710 Good, 711-745 Very good, 746-900 Excellent. The proposed floors keep Poor out of unsecured lending and send Fair applicants without salary transfer to the 600 floor."),
 ("P-21", "Unsecured (no salary transfer) minimum salary of AED 5,000 is the most lenient in the market",
  "The top five ask about AED 10,000 for no-STL or non-listed employers (FAB non-listed 10,000; ENBD no-STL 10,000 per comparison sites). FAB Islamic asks AED 15,000 plus 18 months' service. Only RAKBANK and Mashreq NEO lend at AED 5,000, and RAKBANK requires AECB >= 541 and caps expats at 10x salary / AED 200k.",
  "No-STL finance has no salary assignment, so repayment depends on the customer keeping the direct debit funded. At AED 5,000 with no further controls the bank would be the easiest no-STL lender among peers and would attract applicants other banks decline.",
  "Keep AED 5,000 (the user's criterion) but only with compensating controls: AECB >= 600, employer Cat A-C, >= 6 months' service, 12 months' statements showing a regular salary, repayment by UAE direct debit. For Cat D (non-listed) employers or AECB 541-599, require AED 10,000 (the market median). Caps: nationals 20x salary max AED 500k; expats 10x max AED 200k.",
  "This keeps the bank competitive for good low-income customers with clean records and a stable employer, the inclusion goal. It removes the riskiest combination (low income, no salary transfer, weak score, unlisted employer).",
  "A AED 5,000 salary at 50% DBR supports up to AED 2,500 a month. Over 48 months at 9.99% that is about " + aed(PF_NSTL_DBR) + ", but the expat cap (10x salary) limits it to AED 50,000 and the national cap (20x) to AED 100,000."),
 ("P-28", "Credit card limit rule is missing",
  "No top-five bank publishes a limit multiple. Card limits count in the DBR (market practice: 5% of the limit as a monthly obligation).",
  "Without a rule, limits depend on officer judgement, DBR headroom is consumed unevenly, and the AI model has no ceiling to test against.",
  "Limit = lower of 3x gross monthly income (salary-assigned) or 2x (no STL), the tier cap (entry / Gold / Platinum), and the DBR headroom with 5% of the limit counted as a monthly obligation.",
  "These multiples sit within typical UAE practice and leave room for growth reviews (6 and 12 months of good use).",
  "A AED 5,000 salary: salary-assigned limit AED 15,000 (5% = AED 750 a month counted in DBR); no-STL limit AED 10,000 (AED 500 a month)."),
 ("P-31", "Home finance minimum salary of AED 5,000 is far below the market",
  "Top-five minimums: nationals AED 8,000 (EI, ADCB) to 15,000 (ADIB without STL), median 10,000; expats AED 10,000 (DIB) to 20,000 (EI), median 15,000.",
  "Home finance is a 25-year commitment that has to survive rate rises. At AED 5,000 the affordable finance is small, documentation and valuation costs are high relative to the loan, and the customer has little buffer after rent-free ownership costs (service charges, maintenance, takaful).",
  "AED 10,000 for nationals (AED 8,000 under government housing schemes such as SZHP, MBRHE and ADHA top-up) and AED 15,000 for expats, the top-five medians.",
  "Fewer low-income home finance applications. Those customers remain eligible for personal and auto finance, and nationals keep access through government schemes.",
  "A AED 5,000 salary at 50% DBR supports AED 2,500 a month. Over 25 years at a ~6% stressed rate that funds about " + aed(HOME_FIN_5K_STRESS) + " (about " + aed(HOME_FIN_5K_TEASER) + " at the 4.24% teaser rate). At 80% finance-to-value the property would be about " + aed(HOME_PROP_80) + " (about " + aed(HOME_PROP_85) + " for a national at 85%). At AED 10,000 the stressed finance is about " + aed(HOME_FIN_10K) + "; at AED 15,000 about " + aed(HOME_FIN_15K) + "."),
 ("P-52", "Gold-backed finance at 90% of value has no market precedent",
  "Only Emirates Islamic lends against gold, at 50% of gold certificates and only for Priority customers. No other top-five bank offers it.",
  "Gold prices can fall more than 10% within days (for example April 2013). At 90%, a 10% fall leaves no cover at all, and the bank must sell the collateral in a falling market.",
  "Maximum 70% of gold value; top-up call at 80% and sale at 85% finance-to-value; daily revaluation; tenor up to 24 months; allocated gold or gold certificates held by the bank; Sharia Board approval of the structure.",
  "A lower advance than the user wanted, but still more generous than the only market reference (50%). It gives the customer room to respond to a call before any sale.",
  "At 70%, gold can fall {:.1f}% before the top-up call and {:.1f}% before a sale. At 90% there is no room for a call at all.".format(GOLD_CALL_DROP, GOLD_SALE_DROP)),
 ("P-53", "EOSB-backed finance at 90% of accrued EOSB has no market precedent",
  "No top-five bank lends against end-of-service benefits on their own. DIB, ADCB, RAKBANK, Mashreq and ADIB (auto) take an assignment of EOSB as additional security alongside the salary. CBUAE allows personal finance to be repaid from salary and EOSB, within the 20x and 48-month limits.",
  "EOSB is only paid when employment ends. It can be reduced by amounts the employee owes the employer, depends on the employer's ability to pay, and may sit in an approved savings fund under the voluntary alternative scheme. A 90% advance leaves no margin for these risks.",
  "Offer EOSB backing only inside salary-assigned finance, as additional security: finance against EOSB up to 80% of accrued EOSB; >= 3 years' service; irrevocable employer undertaking; EOSB recalculated every year; total finance still within 20x salary and 48 months.",
  "Slightly smaller advances than requested. In return it is the only structure that matches how the market already treats EOSB, and it gives long-service customers more without creating an untested product.",
  "Basic salary AED 12,000 and 6 years' service: accrued EOSB = 21 days x 5 years + 30 days x 1 year = 135 days x AED {:,.2f} = about {}. At 90% the advance would be {}; at 80% it is {}.".format(EOS_DAILY, aed(EOS), aed(EOS * 0.9), aed(EOS * 0.8))),
]

SIGNOFF = [
 ("P-04", "Minimum service", "3 months for all", "3 months salary-assigned; 6 months no-STL; home 6 months + probation"),
 ("P-06", "Employer categories", "All accepted, no distinction", "All accepted, tiered A-D for caps and pricing"),
 ("P-10", "Bank statements", "12 months for everyone", "3 months (or UAEFTS consent) for salary-assigned; 12 months for no-STL and self-employed"),
 ("P-21", "No-STL minimum salary", "AED 5,000", "AED 5,000 with controls; AED 10,000 for Cat D employers or AECB 541-599"),
 ("P-31", "Home finance minimum salary", "AED 5,000", "AED 10,000 nationals (8,000 government schemes) / AED 15,000 expats"),
 ("P-39", "Home finance service", "3 months", "6 months + probation completed"),
 ("P-52", "Gold-backed advance", "90%", "70% with top-up call at 80% and sale at 85%"),
 ("P-53", "EOSB-backed advance", "90% of accrued EOSB", "80% of accrued EOSB, only inside salary-assigned finance, >= 3 years' service"),
]

SLIGHT_ADD = [
 ("P-02", "Minimum age", "Set 21 for all products (CBUAE sets no limit)."),
 ("P-03", "Maximum age at maturity", "Set 65 nationals / 60 expats for PF, cards, auto; 70 / 65 for home; retirees to 70."),
 ("P-04", "Service (no-STL, home)", "Add 6 months for no-STL and home finance."),
 ("P-06", "Employer categories", "Add tiers A-D that drive caps and pricing."),
 ("P-09", "Restricted lists", "Sanctions screening only; sector watch-list with lower caps."),
 ("P-11", "Self-employed", "Add trade-licence vintage and average-balance minimums."),
 ("P-20", "First-instalment grace", "Add up to 120 days for nationals."),
 ("P-22", "No-STL maximum amount", "Add 20x / AED 500k nationals and 10x / AED 200k expats."),
 ("P-24", "Buyout process", "Add liability-letter age, 30-day settlement, residual after clearance."),
 ("P-30", "Self-employed card", "Add average balance >= AED 50,000 or deposit-backed card."),
 ("P-34", "Home maximum amount", "Add AED 20m."),
 ("P-37", "Home DBR stress", "Assess DBR at the higher of initial and reversion rate."),
 ("P-39", "Home age / service / self-employed", "Add 6 months + probation; self-employed 3 yrs + 2 yrs audited."),
 ("P-40", "Takaful", "Make life and property takaful mandatory."),
 ("P-41", "Government schemes", "Decide participation; DBR 60% where CBUAE allows."),
 ("P-49", "Auto self-employed", "Add licence >= 2 yrs and average balance >= AED 15,000."),
 ("P-54", "Salary advance", "Add 50% of net salary, max AED 25,000, max 6 per year."),
]

RANKING = [
 ("1", "Emirates NBD (incl. Emirates Islamic)", "AED 184bn retail banking & wealth gross loans (Dec-25; incl. KSA and Egypt)", "ENBD Q4-25 investor presentation [R1/H]"),
 ("2", "ADIB", "AED 94.6bn retail financing FY25; AED 109.2bn at 3Q26 (+21%)", "ADIB Q3-26 earnings presentation [R3/H]"),
 ("3", "FAB (incl. FAB Islamic)", "about AED 94bn personal / retail loans (Dec-25, group-wide)", "FAB Sep-26 investor presentation [R4/M, chart labels]"),
 ("4", "DIB", "AED 77bn net / about AED 79bn gross consumer financing (FY25)", "DIB FY25 earnings presentation [R6/H]"),
 ("5", "ADCB (incl. ADCB Islamic)", "about AED 75bn (personal = 18% of AED 414bn gross loans)", "ADCB FY25 investor presentation [R7/H]"),
]

# Range charts: (title, unit_fmt, dmin, dmax, lenient(v,label) or None, conservative(v,label) or None,
#                median (v or (a,b)) + label, user value or None, recs [(v,label)], note)
CHARTS = [
 ("Personal finance, salary-assigned: minimum salary", "aed", 2000, 8000, (3000, "DIB"), (7000, "FAB"), (5000, "median"), 5000, [(5000, "Rec.")], ""),
 ("Personal finance, no salary transfer: minimum salary", "aed", 4000, 16000, (5000, "RAKBANK (ref.)"), (15000, "FAB Islamic"), (10000, "median"), 5000, [(5000, "Rec. with controls"), (10000, "Rec. Cat D / AECB 541-599")], "AED 5,000 kept only with AECB >= 600, Cat A-C employer and 6 months' service."),
 ("Home finance, nationals: minimum salary", "aed", 4000, 16000, (8000, "EI, ADCB"), (15000, "ADIB (no STL)"), (10000, "median"), 5000, [(10000, "Rec.")], "AED 8,000 under government housing schemes."),
 ("Home finance, expats: minimum salary", "aed", 4000, 21000, (10000, "DIB"), (20000, "EI"), (15000, "median"), 5000, [(15000, "Rec.")], ""),
 ("Minimum length of service (months)", "num", -1, 19, (0, "ENBD"), (18, "FAB Islamic (no STL)"), (6, "median"), 3, [(3, "Rec. salary-assigned"), (6, "Rec. no STL / home")], ""),
 ("Personal finance profit rate floor (% reducing)", "pct", 4.0, 13.5, (4.75, "RAKBANK (ref.)"), (12.75, "FAB new-to-country"), ((5.24, 5.99), "median 5.24-5.99"), None, [(5.49, "Rec. nationals"), (5.99, "Rec. expats")], "User criterion: mid-market (no figure)."),
 ("Deposit-backed finance-to-value (%)", "pct0", 85, 97, (95, "FAB, ADIB"), (90, "ENBD, ADCB, Mashreq"), (90, "median"), 90, [(90, "Rec.")], "Here the higher number is the more lenient."),
 ("Gold-backed finance-to-value (%)", "pct0", 40, 100, None, None, (50, "EI, only bank (median)"), 90, [(70, "Rec.")], "Top-up call at 80%, sale at 85%."),
 ("EOSB-backed advance (% of accrued EOSB)", "pct0", 60, 100, None, None, None, 90, [(80, "Rec. (inside salary-assigned only)")], "No top-five bank lends against EOSB alone."),
 ("Auto finance maximum amount (AED million)", "m", 0.3, 2.2, (0.5, "Mashreq; ADIB expats"), (2.0, "ENBD"), (1.5, "median EI, FAB, ADCB"), None, [(1.5, "Rec.")], "Higher is more lenient. User criterion: mid-market (no figure)."),
 ("Home finance 3-year fixed rate (%)", "pct", 3.7, 4.85, (3.85, "ADCB package"), (4.69, "RAKBANK (ref.)"), ((4.0, 4.3), "median 4.0-4.3"), None, [(4.24, "Rec. salary-assigned"), (4.49, "Rec. no STL")], "User criterion: mid-market (no figure)."),
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

S1, S2, TEAL, NAVY, MUTED, BAND = "#2a78d6", "#eb6834", "#0F7B7B", "#14213D", "#5B6475", "#cfe6e4"

def range_svg(c):
    title, kind, dmin, dmax, len_, con, med, user, recs, note = c
    W, H, L, R = 680, 104, 24, 24
    def x(v):
        return L + (v - dmin) / (dmax - dmin) * (W - L - R)
    out = ['<svg viewBox="0 0 {} {}" class="rng" role="img" aria-label="{}">'.format(W, H, html.escape(title))]
    y0 = 52
    out.append('<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="#d5dae1" stroke-width="2"/>'.format(L, y0 + 5, W - R, y0 + 5))
    bottom = []
    if len_ and con:
        a, b = sorted([len_[0], con[0]])
        out.append('<rect x="{:.1f}" y="{}" width="{:.1f}" height="10" rx="3" fill="{}"/>'.format(x(a), y0, max(x(b) - x(a), 3), BAND))
        for v, lab in (len_, con):
            bottom.append((x(v), "{} {}".format(fmt(v, kind), lab), "#5B6475"))
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
    # bottom labels: endpoints row 1, median row 2
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
    # top markers & labels
    tops = []
    merged_user = False
    for rv, rlab in recs:
        if user is not None and abs(rv - user) < 1e-9:
            merged_user = True
    if user is not None:
        ux = x(user)
        out.append('<circle cx="{:.1f}" cy="{}" r="7" fill="{}" stroke="#fff" stroke-width="2"/>'.format(ux, y0 - 8, S2))
        if not merged_user:
            tops.append((ux, "You: {}".format(fmt(user, kind)), S2))
    for rv, rlab in recs:
        rx = x(rv)
        s = 5
        out.append('<polygon points="{:.1f},{} {:.1f},{} {:.1f},{} {:.1f},{}" fill="{}" stroke="#fff" stroke-width="1.5"/>'.format(rx, y0 - 8 - s, rx + s, y0 - 8, rx, y0 - 8 + s, rx - s, y0 - 8, S1))
        if user is not None and abs(rv - user) < 1e-9:
            tops.append((rx, "You = {}: {}".format(rlab, fmt(rv, kind)), NAVY))
        else:
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
    svg = svg.replace('viewBox="0 0 {} {}"'.format(W, H),
                      'viewBox="0 {} {} {}"'.format(-top_extra, W, H + top_extra + bot_extra), 1)
    return svg

def stacked_bar_svg():
    W = 680
    total = sum(TOT)
    cols = [("#0ca30c", "Near", "#ffffff"), ("#fab219", "Slightly off", "#3b2a00"), ("#d03b3b", "Far", "#ffffff")]
    out = ['<svg viewBox="0 0 {} 62" class="stack" role="img" aria-label="31 near, 17 slightly off, 6 far">'.format(W)]
    xpos = 0
    for (col, lab, tcol), v in zip(cols, TOT):
        w = v / total * W
        out.append('<rect x="{:.1f}" y="6" width="{:.1f}" height="30" fill="{}"/>'.format(xpos, max(w - 2, 1), col))
        out.append('<text x="{:.1f}" y="26" font-size="12" font-weight="700" fill="{}" text-anchor="middle">{} {}</text>'.format(xpos + w / 2, tcol, v, lab))
        xpos += w
    out.append('<text x="0" y="56" font-size="10" fill="#5B6475">Ratings across 54 policy items (P-04 counted once in Near and once in Slightly off; P-42 out of scope).</text>')
    out.append('</svg>')
    return "".join(out)

def chip(r):
    if r.startswith("Near (STL)"):
        return '<span class="chip near">&#10003; Near (STL)</span> <span class="chip slight">! Slightly off (no STL, home)</span>'
    cls = {N: ("near", "&#10003;"), S: ("slight", "!"), F: ("far", "&#10005;"), NA: ("na", "&ndash;")}[r]
    return '<span class="chip {}">{} {}</span>'.format(cls[0], cls[1], html.escape(r))

E = html.escape

# ---------- peer annex ----------
PEERS = [
 ("Emirates NBD (conventional)", [
   ("Personal loan", "Min salary AED 5,000 with STL (listed and non-listed employers); no minimum service; max AED 4m nationals / 3m expats; 48 months (60 MoD); fixed 4.99-19.99% reducing, variable from 5.24%; processing 1.05% (525-2,625); early settlement 1.05% / max 10,500; late AED 52.50; DBR 50% (retirees 30%); higher AECB score can waive STL / listing / service. KFS 08/2025"),
   ("Cards", "Entry about AED 5,000; 3.25-3.49% per month; minimum 5% or AED 100; late AED 241.50; self-employed avg balance >= AED 50k over 3 months"),
   ("Home", "Min salary 10k nationals / 15k expats; expats >= 3 yrs in UAE + 1 yr in job; max age 65 salaried / 70 self-employed; max AED 25m; 85/80; 25 yrs; 2-yr fixed 4.19% STL (Oct-26, broker); reversion 1M EIBOR + 1.99%; processing up to 1.05%; 20% free prepayment. KFS 02/2026"),
   ("Auto", "Min salary 7k; age 21-60; max AED 2m; 20% / 60 months; KFS 3.75-9.00% reducing, Emiratis 1.89% flat; vehicle up to 12 yrs. KFS 07/2025"),
   ("Other secured", "Loan against fixed deposit up to 90%, max AED 20m, 5.99-7.29%. KFS 08/2026")]),
 ("Emirates Islamic (ENBD group)", [
   ("Personal finance", "Min salary AED 7,500 (product page) vs 5,000 (apply page), a conflict on the bank's own site; 1 month's service; age 21 / 65 nationals, 60 expats; max AED 4m / 3m; Murabaha 2.59% flat nationals / 2.99% flat expats; processing 0.7875%; late AED 210 to charity. KFS undated"),
   ("Cards", "Flex AED 5,000; 3.69% per month; late donation AED 131.25"),
   ("Home", "IMBT; min salary 8k nationals / 20k expats; max AED 25m; 85/80 (expats 70% for some employer sectors Apr-Jun 26, broker); 25 yrs (30 under EIBOR Relief); 30% free prepayment. KFS Apr-26"),
   ("Auto", "Murabaha; min salary 4k; age 21-60; max AED 1.5m; new 2.49% flat nationals / 2.65% expats; used 3.19%. KFS Oct-25"),
   ("Other secured", "Finance against gold certificates at 50% (Priority), 48 months")]),
 ("ADIB", [
   ("Personal finance", "Min salary AED 5,000; age 21 / 65 nationals, 60 expats; max AED 3m / 2m; 20x salary (15x MoD / AF); 48 months (60 MoD / AF); debt settlement 5.99-12%, other 7.25-20% (rate basis to confirm); processing 1% (500-2,500) + VAT; late AED 100 to charity; Yusr salary advance (50% of net salary, max 50k). KFS V11 Sep-2025"),
   ("Cards", "Dana AED 5,000; 3.75% per month; late AED 100 to charity"),
   ("Home", "Ijara; min salary 10k with STL / 15k without; age 21 / 70 nationals, 65 salaried expats; max AED 30m; 85% (no split stated); variable 1M EIBOR + 1.25% (min 3.99%); 2-yr fixed 4.14%; ARP up to 2%, max 30k; valuation 2,500; 30% free prepayment; ADIB pays property takaful. KFS Aug-25"),
   ("Auto", "Murabaha / Musawama; min salary 5k; age 21 / 65 nationals, 60 expats; max AED 1m nationals / 500k expats; 2.75-4.49% flat; EOSB assignment as security. KFS Apr-25"),
   ("Other secured", "Murabaha against lien on deposits / Sukuk / shares, 95% or up to AED 25m, 4.99-9.99%. KFS Jul-25")]),
 ("FAB and FAB Islamic", [
   ("Personal finance", "Min salary AED 7,000 (government / semi-gov / reputable private); non-listed AED 10,000 or acceptable AECB + 6 months; FAB Islamic no-STL AED 15,000 + 18 months; age 21+; 6 months' service; max AED 5m / 2m; nationals 4.79-13.99%, expats 5.74-13.99%; processing 1.05%"),
   ("Cards", "Cashback Islamic AED 5,000; 3.99% per month (KFS Sep-2026)"),
   ("Home", "Min salary not published; 85/80; max AED 20m; 1-3 yr fixed 3.99%, 5-yr 4.19% (STL + card); variable 3M EIBOR + 1.50%, floor 1.99%; 25% free prepayment (variable period). KFS Sep-26"),
   ("Auto", "Min salary 7k; max AED 1.5m; 2.15% flat nationals / 2.29% expats (STL + card). KFS May-26"),
   ("Other secured", "Loan against fixed deposit up to 95% or AED 5m, deposit rate + 2%")]),
 ("DIB", [
   ("Personal finance", "From AED 3,000; salary transfer not mandatory; max AED 5m / 3m; 48 months; 5.99-21.99% reducing; processing 1.05% (520-2,620); early settlement 1% max 10k (waived MoD / AF); late up to AED 175 donation; salary + EOSB transfer letter; FlexiSalary advance from AED 2,000. KFS Apr-2026, SOC Jun-2025"),
   ("Cards", "Platinum AED 15,000; up to 3.69% per month; late donation AED 236.25. SOC Oct-2026"),
   ("Home", "IMBT; min salary 10k; age 18 to 70; 85/80; off-plan 50% (>= 35% complete, >= 50% paid); 3-yr fixed 3.95% STL (broker); processing 1.05% (min 5,250, max 105,000); valuation 2,500; no free prepayment. KFS May-26"),
   ("Auto", "Murabaha; min salary 3k; 1 month's service; max AED 1m (EV 1.5m); 2.25-6.15% flat; vehicle up to 10 yrs. KFS Sep-26"),
   ("Other secured", "Finance against investment / Wakala deposits")]),
 ("ADCB and ADCB Islamic", [
   ("Personal finance", "Min salary AED 5,000 (employer listed or eligible) [M]; age 21 / 65 nationals, 60 expats [M]; max AED 4m / 1.5m (FAQ about 4 years old) [M]; 6-48 months; nationals from 5.24%, expats from 6.49% (conventional) / 5.99% (Islamic); processing 1.05%; salary + EOSB assignment; mandatory life takaful (Islamic)"),
   ("Cards", "Entry AED 5,000; about 3.25% per month [M]"),
   ("Home", "Min salary 8k nationals / 15k expats; age 18 / 65 salaried, 70 self-employed, 60 non-resident; AED 250k-24m; 85/80; from 3.99%, 3.85% 3-yr package; processing 0.525-0.7875% incl. VAT, cap AED 52,500; valuation 3,150; 30% free prepayment. KFS Feb-26"),
   ("Auto", "Min salary 5k; age 18 / 70 nationals, 65 expats; max AED 1.5m; 1.75-4.99% flat; vehicle up to 12 yrs at maturity. KFS Jan / Feb-25"),
   ("Other secured", "Overdraft against fixed deposit 90%; Islamic finance against deposits (Commodity Murabaha + Wakala), nil fee")]),
]

SOURCES = [
 ("Ranking", "R1", "ENBD Q4-25 investor presentation", "https://www.emiratesnbd.com/-/media/enbd/files/investor-relations/financial-information/presentations/emiratesnbd_investor_presentation_2025_q4.pdf", "H"),
 ("Ranking", "R3", "ADIB Q3-26 earnings presentation", "https://www.adib.ae/-/media/Project/ADIB/ADIBSite/docs/Investor-Relations/Quarterly-results/Earning-presentation/2026/ADIB-EP-Q3.pdf", "H"),
 ("Ranking", "R4", "FAB Sep-26 investor presentation", "https://www.bankfab.com/-/media/fab-uds/about-fab/investor-relations/reports-and-presentations/presentations/pdfs/2026/september-2026-investor-presentation.pdf", "M"),
 ("Ranking", "R6", "DIB FY25 earnings presentation", "https://www.dib.ae/docs/default-source/financial-reports/dib-ye-earnings-presentation-2025.pdf", "H"),
 ("Ranking", "R7", "ADCB FY25 investor presentation", "https://www.adcb.com/en/multimedia/pdfs/2026/february/investor-presentation-FY-2025.pdf", "H"),
 ("Ranking", "R8", "Emirates Islamic FY25 financial statements", "https://www.emiratesislamic.ae/-/media/ei/pdfs/financial-information/annual-report-pdf/2025/financial_statements_2025_eng.pdf", "H"),
 ("Regulation", "R15", "CBUAE eases mortgage requirements (age cap removed; ES cap)", "https://www.centralbank.ae/media/z31oq5zw/the-central-bank-of-the-uae-eases-mortgage-loan-requirements-for-bank-customers.pdf", "H"),
 ("Regulation", "P1", "Gulf News: UAE scraps minimum salary rule (Nov-2025)", "https://gulfnews.com/business/banking/uae-scraps-minimum-salary-rule-for-loans-what-does-this-really-mean-for-residents-1.500352440", "L"),
 ("Regulation", "P3", "Khaleej Times: banks' minimum salary for personal loans (Dec-2025)", "https://www.khaleejtimes.com/uae/these-banks-set-minimum-salary-dh5000-personal-loans", "L"),
 ("Regulation", "R16", "CBUAE base rate raised to 3.90% (Sep-2026)", "https://gulfbusiness.com/en/2026/uae/uae-central-bank-raises-base-rate-to-3-9-after-fed-hike/", "L"),
 ("ENBD", "E1", "Personal loan KFS 08/2025", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_personal_loan_fixed_interest_rate.pdf", "H"),
 ("ENBD", "E2", "Salary-transfer loans for expats", "https://www.emiratesnbd.com/en/loans/personal-loans/salary-transfer-loans-for-expats", "H"),
 ("ENBD", "E5", "Debt burden ratio help page", "https://www.emiratesnbd.com/en/help-and-support/your-debt-burden-ratio", "H"),
 ("ENBD", "E6", "Credit card KFS", "https://www.emiratesnbd.com/en/KFS/credit-card", "H"),
 ("ENBD", "E3h", "Home loan KFS 02/2026", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_home_loan_fixed_and_variable_interest_rate.pdf", "H"),
 ("ENBD", "E16", "Auto loan KFS 07/2025", "https://cdn.emiratesnbd.com/enbd/files/pdf/kfs_auto_loan_fixed_interest_rate.pdf", "H"),
 ("ENBD", "E22", "Loan against fixed deposit KFS 08/2026", "https://www.emiratesnbd.com/-/media/enbd/files/others/form-center/retail-banking/loan-forms/loan_against_fd_for_individuals.pdf", "H"),
 ("Emirates Islamic", "I1", "Personal finance", "https://www.emiratesislamic.ae/en/personal-banking/finance/personal-finance", "H"),
 ("Emirates Islamic", "I3", "Personal finance KFS", "https://www.emiratesislamic.ae/en/key-information/kfs-personal-finance", "H"),
 ("Emirates Islamic", "I4", "Credit card KFS", "https://www.emiratesislamic.ae/en/key-information/kfs-credit-cards", "H"),
 ("Emirates Islamic", "E43", "Home finance KFS Apr-26", "https://www.emiratesislamic.ae/-/media/ei/pdfs/key-information/kfs_homefinance_ea.pdf", "H"),
 ("Emirates Islamic", "E52", "Auto finance KFS Oct-25", "https://www.emiratesislamic.ae/-/media/ei/pdfs/key-information/kfs_autofinance_ea.pdf", "H"),
 ("Emirates Islamic", "E55", "Finance against gold certificates", "https://www.emiratesislamic.ae/en/priority-banking/wealth-solutions/finance-against-gold-certificates", "H"),
 ("ADIB", "B1", "Personal finance", "https://www.adib.ae/en/personal/finance/personal-finance", "H"),
 ("ADIB", "B2", "Personal finance KFS V11 Sep-2025", "https://www.adib.ae/-/media/project/adib/adibsite/docs/kfs/adib-personal-finance_kfs.pdf", "H"),
 ("ADIB", "B3", "Yusr salary advance KFS", "https://www.adib.com/en/SiteAssets/kfs/ADIB-Salary-Advance_Yusr_KFS.pdf", "H"),
 ("ADIB", "D42", "Home finance KFS Aug-25", "https://www.adib.ae/-/media/Project/ADIB/ADIBSite/docs/kfs/adib-home-finance_KFS.pdf", "H"),
 ("ADIB", "D48", "Auto finance KFS Apr-25", "https://www.adib.ae/-/media/Project/ADIB/ADIBSite/docs/kfs/adib-auto-finance_kfs.pdf", "H"),
 ("ADIB", "D50", "Secured finance KFS Jul-25", "https://www.adib.ae/-/media/project/adib/adibsite/docs/kfs/adib-secured-finance_kfs.pdf", "H"),
 ("FAB", "F2", "Personal loan", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/personal-loan", "H"),
 ("FAB", "F3", "Non-listed company personal loan", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/non-listed-company-personal-loan", "H"),
 ("FAB", "F6", "Islamic non-salary-transfer personal finance", "https://www.bankfab.com/en-ae/personal/fab-islamic/personal-islamic-banking/islamic-finances/non-salary-transfer-personal-finance", "H/M"),
 ("FAB", "F8", "Consolidated credit card KFS Sep-2026", "https://apply.bankfab.com/-/media/fab-uds/personal/key-facts-statements/credit-cards/fab-consolidated-credit-cards-en.pdf", "H"),
 ("FAB", "F28", "Mortgage KFS Sep-26", "https://www.bankfab.com/-/media/fab-uds/personal/key-facts-statements/loans/mortgage-loan-en.pdf", "H"),
 ("FAB", "F43", "Car loan KFS (salaried) May-26", "https://www.bankfab.com/-/media/fab-uds/personal/key-facts-statements/loans/car-loans-for-salaried-individuals-en.pdf", "H"),
 ("FAB", "F48", "Secured loan against fixed deposit", "https://www.bankfab.com/en-ae/personal/loans/personal-loans/secured-loans", "H"),
 ("DIB", "D1", "Personal finance", "https://www.dib.ae/personal/personal-finance/personal-finance", "H"),
 ("DIB", "D4", "Personal finance KFS Apr-2026", "https://dib.ae/docs/default-source/cpr/kfs/Personal-Finance-KFS-PF-Goods-Murabaha-POST-Sanc.pdf", "H"),
 ("DIB", "D5", "Personal finance schedule of charges Jun-2025", "https://www.dib.ae/docs/default-source/cpr/soc/cpr-soc-pf.pdf", "H"),
 ("DIB", "D7", "Cards schedule of charges Oct-2026", "https://www.dib.ae/docs/default-source/cpr/soc/cpr-soc-cards.pdf", "H"),
 ("DIB", "D11", "Home finance KFS May-26", "https://www.dib.ae/docs/default-source/cpr/kfs/home-finance-kfs-interim-pre-product-static.pdf", "H"),
 ("DIB", "D20", "Auto finance KFS Sep-26", "https://www.dib.ae/docs/default-source/cpr/kfs/auto-finance-kfs-auto-finance-post-ls-fb.pdf", "H"),
 ("ADCB", "A3", "Personal loan FAQ", "https://www.adcb.com/en/get-in-touch/faqs/loans/personal-loan", "M"),
 ("ADCB", "A4", "Islamic personal finance FAQ", "https://www.adcb.com/en/islamic/get-in-touch/faqs/finances/personal-finance", "M"),
 ("ADCB", "F6a", "Mortgage KFS Feb-26", "https://www.adcb.com/en/multimedia/kfs/mortgage-kfs.pdf", "H"),
 ("ADCB", "F7", "Schedule of fees Sep-26", "https://www.adcb.com/en/multimedia/sof/cb-sof-current-charges-fees.pdf", "H"),
 ("ADCB", "F22", "Islamic car finance KFS Feb-25", "https://www.adcb.com/en/multimedia/kfs/auto-finance-islamic-kfs.pdf", "H"),
 ("ADCB", "F24", "Islamic finance against deposits KFS Mar-24", "https://www.adcb.com/en/multimedia/kfs/ib-finance-against-deposits-kfs.pdf", "H"),
 ("Reference", "R1k", "RAKBANK expat personal loan KFS V08/2026 (AECB floors)", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs088-personal-loan-expat.pdf", "H"),
 ("Reference", "R3k", "RAKBANK non-STL personal finance KFS V01/2026", "https://www.rakbank.ae/globalassets/rakbank/all-pdfs/001---key-fact-statements/bilingual/kfs091-personal-finance-nstl-expat.pdf", "H"),
 ("Reference", "M3", "Mashreq personal loan KFS rev. 12-Jan-2026", "https://www.mashreq.com/-/jssmedia/pdfs/neo/loans/kfs-tnc/Mashreq-personal-loans-KFS-english.ashx", "H"),
 ("Reference", "M4", "Mashreq mortgage KFS 19-Jun-26", "https://www.mashreq.com/-/jssmedia/pdfs/neo/loans/kfs-tnc/Mortgage-KFS-English.ashx", "H"),
]

CAVEATS = [
 "ADCB personal-finance and card figures are search-engine extracts (M) because the bank's site blocked automated reading; one ADCB FAQ is about 4 years old.",
 "FAB's retail book (~AED 94bn) was read from chart labels (M) and includes international books; ADIB and FAB are effectively tied at FY25, with ADIB clearly ahead on UAE-only retail and 2026 growth.",
 "Emirates Islamic's own pages conflict on the personal-finance minimum salary (AED 7,500 vs 5,000).",
 "ADIB labels its 7.25-20% personal-finance rates as fixed but its KFS formula is flat-rate; confirm the basis before comparing directly.",
 "Non-STL minimum salary of AED 10,000 at ENBD comes from a comparison site (L).",
 "Card limit multiples, most AECB floors, stress rates, and LTVs above AED 5m or for second homes are not published by the top five; recommended values there are proposals [P].",
 "Several rate grids come from broker market briefs (L) and move with EIBOR (3M EIBOR 4.39% on 1-Oct-26; CBUAE base rate 3.90% from 17-Sep-26).",
 "The CBUAE LTV caps and auto limits match all bank documents; the age-cap removal and the early-settlement cap were verified against the CBUAE Oct-2019 release.",
]

# ---------- Markdown ----------
md = []
md.append("# Benchmark & Gap Report: UAE Islamic Bank Retail Credit Policy v0.1\n")
md.append("Prepared 2026-11-09 for the bank's management and credit team. It compares the bank's basic credit criteria with the published criteria of the **top five UAE retail banks** and their Islamic arms, rates each item, and recommends changes. Source of truth: `03-parameter-sheet.md`. Benchmark data: `01-benchmark-unsecured.md`, `02-benchmark-secured.md`.\n")
md.append("## 1. Executive summary\n")
md.append("**The top five UAE retail banks** (by retail financing book):\n")
md.append("| # | Bank | Retail financing | Source |\n|---|---|---|---|")
for r in RANKING:
    md.append("| {} | {} | {} | {} |".format(*r))
md.append("\nIslamic peers: ADIB, DIB, Emirates Islamic, ADCB Islamic (with Al Hilal Bank) and FAB Islamic. Mashreq and RAKBANK are extra reference points.\n")
md.append("**Verdict:** of the 54 policy items, **{} are near** the top five, **{} slightly off** and **{} far**. The basic criteria are close to the market on pricing, fees, DBR, finance-to-value, tenors and salary-assigned finance.\n".format(*TOT))
md.append("**The six far gaps:**\n")
for fid, ftitle, *_r in FAR:
    md.append("- **{}**: {}".format(fid, ftitle))
md.append("\n**Headline:** after the recommended changes, every item sits inside the top-five range.\n")
md.append("## 2. Scorecard\n")
md.append("| Product | Near | Slightly off | Far |\n|---|---|---|---|")
for g in GROUPS:
    n, s, f = counts_for(g)
    md.append("| {} | {} | {} | {} |".format(GROUP_SHORT[g], n, s, f))
md.append("| **Total** | **{}** | **{}** | **{}** |\n".format(*TOT))
md.append("P-04 is counted once as Near (salary-assigned) and once as Slightly off (no STL, home). P-42 (non-resident) is out of scope.\n")
md.append("## 3. Where you stand on key numbers\n")
md.append("| Item | Most lenient | Median | Most conservative | Your criterion | Recommended |\n|---|---|---|---|---|---|")
for c in CHARTS:
    title, kind, dmin, dmax, len_, con, med, user, recs, note = c
    lt = "{} ({})".format(fmt(len_[0], kind), len_[1]) if len_ else "-"
    ct = "{} ({})".format(fmt(con[0], kind), con[1]) if con else "-"
    if med:
        mt = med[1] if isinstance(med[0], tuple) else "{} ({})".format(fmt(med[0], kind), med[1])
    else:
        mt = "no market precedent"
    ut = fmt(user, kind) if user is not None else "mid-market (no figure)"
    rt = "; ".join("{}: {}".format(l, fmt(v, kind)) for v, l in recs)
    md.append("| {} | {} | {} | {} | {} | {} |".format(title, lt, mt, ct, ut, rt))
md.append("")
md.append("## 4. Item-by-item comparison\n")
md.append("Tags: [U] user criterion kept; [C] CBUAE rule; [M] top-five median; [P] proposed (no clear market figure); [A] adjusted from the user criterion (needs sign-off).\n")
for g in GROUPS:
    md.append("### " + g + "\n")
    md.append("| ID | Item | Your criterion | Top-five benchmark | Rating | Recommended | Tag |\n|---|---|---|---|---|---|---|")
    for it in ITEMS:
        if it[0] == g:
            md.append("| {} | {} | {} | {} | {} | {} | {} |".format(*it[1:]))
    md.append("")
md.append("## 5. How to close the six far gaps\n")
for fid, ftitle, peers, risk, change, trade, example in FAR:
    md.append("### {}: {}\n".format(fid, ftitle))
    md.append("- **What the top five do:** " + peers)
    md.append("- **Risk if unchanged:** " + risk)
    md.append("- **Recommended change:** " + change)
    md.append("- **Trade-off:** " + trade)
    md.append("- **Worked example:** " + example + "\n")
md.append("## 6. Slightly-off items: what to add\n")
md.append("| ID | Item | What to add |\n|---|---|---|")
for r in SLIGHT_ADD:
    md.append("| {} | {} | {} |".format(*r))
md.append("\n## 7. Items needing your sign-off\n")
md.append("These recommendations differ from your basic criteria ([A]). Approve or reject each one; the policy and model configuration will follow your decision.\n")
md.append("| ID | Item | Your basic criterion | Recommended | Decision |\n|---|---|---|---|---|")
for r in SIGNOFF:
    md.append("| {} | {} | {} | {} | Approve / Reject |".format(*r))
md.append("\n## 8. Annex A: peer profiles\n")
for bank, rows in PEERS:
    md.append("### " + bank + "\n")
    md.append("| Product | Published criteria |\n|---|---|")
    for p, t in rows:
        md.append("| {} | {} |".format(p, t))
    md.append("")
md.append("**Data caveats**\n")
for c in CAVEATS:
    md.append("- " + c)
md.append("\n## 9. Annex B: sources\n")
md.append("Confidence: H = bank page, KFS or schedule of charges; M = search extract or chart reading; L = broker, aggregator or press. All checked 2026-11-09. Full lists: `01-benchmark-unsecured.md` §C and `02-benchmark-secured.md` §D.\n")
md.append("| Group | Tag | Source | URL | Conf. |\n|---|---|---|---|---|")
for s in SOURCES:
    md.append("| {} | {} | {} | {} | {} |".format(*s))
OUT_MD.write_text(("\n".join(md) + "\n").replace(">=", "≥").replace("<=", "≤"), encoding="utf-8")

# ---------- HTML ----------
CSS = """
@page { size: A4; margin: 15mm 13mm 16mm 13mm; @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 8pt "IBM Plex Sans", "Segoe UI", sans-serif; color: #5B6475; } @bottom-left { content: "Benchmark & Gap Report  |  UAE Islamic bank retail credit policy v0.1"; font: 8pt "IBM Plex Sans", "Segoe UI", sans-serif; color: #5B6475; } }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; box-sizing: border-box; }
body { font: 9.6pt/1.5 "IBM Plex Sans", "Segoe UI", sans-serif; color: #14213D; margin: 0; }
h1, h2, h3 { font-family: "Plus Jakarta Sans", "Segoe UI", sans-serif; color: #14213D; break-after: avoid; }
h2 { font-size: 15pt; margin: 22px 0 8px; padding-bottom: 4px; border-bottom: 2px solid #0F7B7B; }
h3 { font-size: 11.5pt; margin: 16px 0 6px; color: #0F7B7B; }
p { margin: 0 0 8px; }
.cover { background: #14213D; color: #fff; padding: 22px 24px 20px; border-radius: 8px; margin-bottom: 14px; }
.cover small { color: #7FC4C4; font-weight: 600; letter-spacing: .1em; font-size: 8pt; }
.cover h1 { color: #fff; font-size: 22pt; margin: 6px 0 4px; line-height: 1.15; }
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
.chip.slight { background: #FFF3D1; border-color: #fab219; color: #5a3d00; }
.chip.far { background: #FBE4E4; border-color: #d03b3b; color: #8a1f1f; }
.chip.na { background: #EEF0F3; border-color: #9AA6BA; color: #44506a; }
.heat td.c { text-align: center; font-weight: 700; }
.heat td.n1 { background: #DDF3DD !important; color: #0a5c0a; }
.heat td.s1 { background: #FFF0C7 !important; color: #5a3d00; }
.heat td.f1 { background: #F8D7D7 !important; color: #8a1f1f; }
.heat td.z { color: #9AA6BA; }
.legend { display: flex; gap: 18px; font-size: 8.5pt; color: #5B6475; margin: 4px 0 8px; flex-wrap: wrap; align-items: center; }
.legend i { display: inline-block; vertical-align: middle; margin-right: 5px; }
.rngbox { break-inside: avoid; border: 1px solid #D5DAE1; border-radius: 6px; padding: 8px 10px 4px; margin: 0 0 8px; }
.rngbox h4 { margin: 0 0 2px; font: 600 9.6pt "Plus Jakarta Sans", "Segoe UI", sans-serif; }
.rngbox .note { font-size: 8pt; color: #5B6475; margin: 0 0 2px; }
svg.rng { width: 100%; height: auto; display: block; font-family: "IBM Plex Sans", "Segoe UI", sans-serif; }
svg.stack { width: 100%; height: auto; display: block; font-family: "IBM Plex Sans", "Segoe UI", sans-serif; }
.gap { break-inside: avoid; border: 1px solid #D5DAE1; border-left: 5px solid #d03b3b; border-radius: 6px; padding: 10px 14px; margin: 0 0 10px; }
.gap h3 { margin-top: 0; color: #14213D; }
.gap dl { display: grid; grid-template-columns: 150px 1fr; gap: 4px 12px; margin: 0; font-size: 8.9pt; }
.gap dt { font-weight: 700; color: #0F7B7B; }
.gap dd { margin: 0; }
.ex { background: #F4F6F9; border-radius: 4px; padding: 6px 8px; }
.pb { break-before: page; }
.small { font-size: 8pt; color: #5B6475; }
.url { word-break: break-all; font-size: 7.4pt; }
.peer { break-inside: avoid; }
.peer td:first-child { width: 95px; font-weight: 600; }
.tags { font-size: 8.3pt; color: #44506a; }
.far1 td:first-child, .heat td:first-child { white-space: nowrap; }
"""

h = []
h.append('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Benchmark &amp; Gap Report</title>')
h.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap">')
h.append('<style>' + CSS + '</style></head><body>')
h.append('<div class="cover"><small>BENCHMARK &amp; GAP REPORT &middot; 9 NOVEMBER 2026</small><h1>UAE Islamic bank retail credit policy v0.1 vs the top five UAE retail banks</h1>'
         '<p>Basic criteria compared with published criteria of Emirates NBD (with Emirates Islamic), ADIB, FAB, DIB and ADCB. For management and the credit team.</p></div>')
# 1 exec summary
h.append('<h2>1. Executive summary</h2>')
h.append('<p><b>The top five UAE retail banks</b>, ranked by retail financing book:</p>')
h.append('<table><thead><tr><th>#</th><th>Bank</th><th>Retail financing</th><th>Source</th></tr></thead><tbody>')
for r in RANKING:
    h.append('<tr><td>{}</td><td><b>{}</b></td><td>{}</td><td class="small">{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
h.append('<p class="small">Islamic peers: ADIB, DIB, Emirates Islamic, ADCB Islamic (with Al Hilal Bank) and FAB Islamic. Mashreq and RAKBANK are extra reference points. ADIB and FAB are effectively tied at FY25; ADIB leads on UAE-only retail and 2026 growth.</p>')
h.append('<p><b>Verdict.</b> Of the 54 policy items, <span class="chip near">&#10003; {} Near</span> <span class="chip slight">! {} Slightly off</span> <span class="chip far">&#10005; {} Far</span>. '
         'The basic criteria are close to the market on pricing, fees, DBR, finance-to-value, tenors and salary-assigned finance. '
         'They are more lenient than every top-five bank on unsecured (no salary transfer) entry, home-finance minimum salary, and gold- and EOSB-backed advances, and silent on credit-score floors and card limits.</p>'.format(*TOT))
h.append('<p><b>The six far gaps</b></p><table class="far1"><thead><tr><th>ID</th><th>Gap</th><th>Recommended</th></tr></thead><tbody>')
recmap = {it[1]: it[6] for it in ITEMS}
for fid, ftitle, *_r in FAR:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td></tr>'.format(fid, E(ftitle), E(recmap[fid])))
h.append('</tbody></table>')
h.append('<div class="headline">After the recommended changes, every item sits inside the top-five range.</div>')
# 2 scorecard
h.append('<h2>2. Scorecard</h2>')
h.append(stacked_bar_svg())
h.append('<table class="heat"><thead><tr><th>Product</th><th style="text-align:center">&#10003; Near</th><th style="text-align:center">! Slightly off</th><th style="text-align:center">&#10005; Far</th></tr></thead><tbody>')
for g in GROUPS:
    n, s, f = counts_for(g)
    h.append('<tr><td><b>{}</b></td><td class="c {}">{}</td><td class="c {}">{}</td><td class="c {}">{}</td></tr>'.format(
        E(GROUP_SHORT[g]), "n1" if n else "z", n, "s1" if s else "z", s, "f1" if f else "z", f))
h.append('<tr><td><b>Total</b></td><td class="c n1">{}</td><td class="c s1">{}</td><td class="c f1">{}</td></tr>'.format(*TOT))
h.append('</tbody></table><p class="small">P-04 (minimum service) is Near for salary-assigned and Slightly off for no-STL and home, so it is counted once in each. P-42 (non-resident) is out of scope.</p>')
# 3 range charts
h.append('<h2 class="pb">3. Where you stand on key numbers</h2>')
h.append('<p>Each strip runs from the most lenient to the most conservative top-five value. The darker mark is the top-five median. Values are as published (checked 9 Nov 2026).</p>')
h.append('<div class="legend"><span><i style="width:22px;height:9px;background:{};border-radius:2px"></i>Top-five range</span>'
         '<span><i style="width:4px;height:14px;background:{}"></i>Median</span>'
         '<span><i style="width:12px;height:12px;border-radius:50%;background:{}"></i>Your criterion</span>'
         '<span><i style="width:10px;height:10px;background:{};transform:rotate(45deg)"></i>Recommended</span></div>'.format(BAND, TEAL, S2, S1))
for c in CHARTS:
    note = c[9]
    h.append('<div class="rngbox"><h4>{}</h4>{}{}</div>'.format(E(c[0]), '<p class="note">' + E(note) + '</p>' if note else '', range_svg(c)))
# 4 full table
h.append('<h2 class="pb">4. Item-by-item comparison</h2>')
h.append('<p class="tags">Tags: [U] your criterion kept &middot; [C] CBUAE rule &middot; [M] top-five median &middot; [P] proposed (no clear market figure) &middot; [A] adjusted from your criterion, needs sign-off.</p>')
for g in GROUPS:
    h.append('<h3>{}</h3>'.format(E(g)))
    h.append('<table class="cmp"><thead><tr><th style="width:5%">ID</th><th style="width:13%">Item</th><th style="width:15%">Your criterion</th><th style="width:22%">Top-five benchmark</th><th style="width:11%">Rating</th><th style="width:28%">Recommended</th><th style="width:6%">Tag</th></tr></thead><tbody>')
    for it in ITEMS:
        if it[0] == g:
            h.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                it[1], E(it[2]), E(it[3]), E(it[4]), chip(it[5]), E(it[6]), E(it[7])))
    h.append('</tbody></table>')
# 5 far gaps
h.append('<h2 class="pb">5. How to close the six far gaps</h2>')
for fid, ftitle, peers, risk, change, trade, example in FAR:
    h.append('<div class="gap"><h3>{}: {}</h3><dl>'.format(fid, E(ftitle)))
    h.append('<dt>What the top five do</dt><dd>{}</dd>'.format(E(peers)))
    h.append('<dt>Risk if unchanged</dt><dd>{}</dd>'.format(E(risk)))
    h.append('<dt>Recommended change</dt><dd><b>{}</b></dd>'.format(E(change)))
    h.append('<dt>Trade-off</dt><dd>{}</dd>'.format(E(trade)))
    h.append('<dt>Worked example</dt><dd class="ex">{}</dd>'.format(E(example)))
    h.append('</dl></div>')
# 6 slightly off
h.append('<h2>6. Slightly-off items: what to add</h2>')
h.append('<table><thead><tr><th style="width:8%">ID</th><th style="width:30%">Item</th><th>What to add</th></tr></thead><tbody>')
for r in SLIGHT_ADD:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
# 7 sign-off
h.append('<h2>7. Items needing your sign-off</h2>')
h.append('<p>These recommendations differ from your basic criteria (tag [A]). Approve or reject each one; the policy document and the model configuration will follow your decision.</p>')
h.append('<table><thead><tr><th style="width:7%">ID</th><th style="width:18%">Item</th><th style="width:22%">Your basic criterion</th><th>Recommended</th><th style="width:13%">Decision</th></tr></thead><tbody>')
for r in SIGNOFF:
    h.append('<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>&#9744; Approve<br>&#9744; Reject</td></tr>'.format(*[E(x) for x in r]))
h.append('</tbody></table>')
# 8 peers
h.append('<h2 class="pb">8. Annex A: peer profiles</h2>')
h.append('<p class="small">Published criteria as read on 9 Nov 2026. KFS = key facts statement; SOC = schedule of charges. [M] = search extract.</p>')
for bank, rows in PEERS:
    h.append('<div class="peer"><h3>{}</h3><table><tbody>'.format(E(bank)))
    for p, t in rows:
        h.append('<tr><td>{}</td><td>{}</td></tr>'.format(E(p), E(t)))
    h.append('</tbody></table></div>')
h.append('<h3>Data caveats</h3><ul>')
for c in CAVEATS:
    h.append('<li>{}</li>'.format(E(c)))
h.append('</ul>')
# 9 sources
h.append('<h2 class="pb">9. Annex B: sources</h2>')
h.append('<p class="small">Confidence: H = bank page, KFS or schedule of charges; M = search extract or chart reading; L = broker, aggregator or press. All checked 9 Nov 2026. Full lists are in 01-benchmark-unsecured.md and 02-benchmark-secured.md.</p>')
h.append('<table><thead><tr><th style="width:12%">Group</th><th style="width:6%">Tag</th><th style="width:28%">Source</th><th>URL</th><th style="width:6%">Conf.</th></tr></thead><tbody>')
for s in SOURCES:
    h.append('<tr><td>{}</td><td>{}</td><td>{}</td><td class="url">{}</td><td>{}</td></tr>'.format(*[E(x) for x in s]))
h.append('</tbody></table>')
h.append('</body></html>')
OUT_HTML.write_text("".join(h).replace("&gt;=", "≥").replace("&lt;=", "≤"), encoding="utf-8")
print("ok", TOT)
