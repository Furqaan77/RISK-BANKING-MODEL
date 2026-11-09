# Customer scenarios for the finance-company gap report.
# Every number is computed here from the policy values (03-parameter-sheet.md / 05 policy); nothing is hardcoded.

VAT = 0.05
DBR_MAX = 0.50
CARD_FACTOR = 0.05            # cards counted at 5% of limit in DBR (F-15)
ES_FEE = 0.01                 # early settlement 1% (F-25)
CAP_ASSIGNED = 300000         # F-21
ASSIGNED = {1: .1299, 2: .1399, 3: .1499, 4: .1649, 5: .1799, 6: .1999, 7: .2249, 8: .2499}      # F-23
NONASSIGNED = {1: .1599, 2: .1699, 3: .1799, 4: .1949, 5: .2149, 6: .2399, 7: .2699, 8: .2999}   # F-32
SA_SHARE, SA_CAP = 0.50, 5000                       # F-52
SA_FEE_BANDS = [(1000, 30), (2500, 60), (5000, 120)]  # F-52 flat fee + VAT
GOLD_LTV, GOLD_CALL, GOLD_SALE, GOLD_RATE = .70, .80, .85, .1499   # F-49, F-50
AUTO_DOWN, AUTO_USED_FLAT_G13 = .20, .0449           # F-42, F-44


def pmt(p, rate, n):
    i = rate / 12
    return p * i / (1 - (1 + i) ** -n)


def flat_inst(p, fr, n):
    return p * (1 + fr * n / 12) / n


def flat_to_reducing(fr, n):
    p, inst, lo, hi = 1000.0, flat_inst(1000.0, fr, n), 1e-6, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if pmt(p, mid, n) > inst:
            hi = mid
        else:
            lo = mid
    return mid


def annuity_pv(inst, rate, n):
    i = rate / 12
    return inst * (1 - (1 + i) ** -n) / i


def aed(x):
    return "AED {:,.0f}".format(x)


def n0(x):
    return "{:,.0f}".format(x)


def pc(x, k=1):
    return "{:.{}%}".format(x, k)


# ---------- 1. Mariam: employer-assigned loan without moving salary ----------
M_SAL, M_CARD, M_AMT, M_N, M_GRADE = 6500, 10000, 60000, 48, 5
M_RATE = ASSIGNED[M_GRADE]
M_MAX = min(20 * M_SAL, CAP_ASSIGNED)
M_CARDPAY = M_CARD * CARD_FACTOR
M_INST = pmt(M_AMT, M_RATE, M_N)
M_DBR = (M_INST + M_CARDPAY) / M_SAL
assert M_AMT <= M_MAX and M_DBR <= DBR_MAX
M_INT = M_INST * M_N - M_AMT
M_20_INT = pmt(M_AMT, .20, M_N) * M_N - M_AMT
M_24_INT = pmt(M_AMT, .24, M_N) * M_N - M_AMT
M_40_INT = pmt(M_AMT, .3999, M_N) * M_N - M_AMT

# ---------- 2. Ravi: WPS worker, salary advance ----------
R_NET, R_AMT = 3500, 1500
R_MAX = min(SA_SHARE * R_NET, SA_CAP)
R_FEE = next(f for cap, f in SA_FEE_BANDS if R_AMT <= cap)
R_FEE_VAT = R_FEE * (1 + VAT)
R_REPAY = R_AMT + R_FEE_VAT
R_SHARE = R_REPAY / R_NET
R_COST = R_FEE_VAT / R_AMT
R_APR = R_FEE / R_AMT * 12
R_EAND = R_AMT * 0.08 * (1 + VAT)
assert R_AMT <= R_MAX and R_SHARE <= DBR_MAX

# ---------- 3. Khalid: buyout of a 28% finance-company loan ----------
K_SAL, K_BAL, K_OLD_RATE, K_N, K_GRADE = 18000, 120000, .28, 36, 2
K_OLD = pmt(K_BAL, K_OLD_RATE, K_N)
K_ES = K_BAL * ES_FEE * (1 + VAT)
K_P = K_BAL + K_ES
K_RATE = ASSIGNED[K_GRADE]
K_NEW = pmt(K_P, K_RATE, K_N)
K_DBR = K_NEW / K_SAL
K_BANK = pmt(K_P, .0549, K_N)
K_OLD_TOT, K_NEW_TOT, K_BANK_TOT = K_OLD * K_N, K_NEW * K_N, K_BANK * K_N
assert K_P <= min(20 * K_SAL, CAP_ASSIGNED) and K_DBR <= DBR_MAX

# ---------- 4. Fatima: gold-backed loan ----------
F_GOLD, F_INC, F_N = 100000, 25000, 24
F_AMT = F_GOLD * GOLD_LTV
F_INST = pmt(F_AMT, GOLD_RATE, F_N)
F_DBR = F_INST / F_INC
F_INT = F_INST * F_N - F_AMT
F_16_INT = pmt(F_AMT, .16, F_N) * F_N - F_AMT
F_CALL_DROP = 1 - GOLD_LTV / GOLD_CALL
F_SALE_DROP = 1 - GOLD_LTV / GOLD_SALE
assert F_DBR <= DBR_MAX

# ---------- 5. Arjun: used car at AED 5,000 salary ----------
A_PRICE, A_SAL, A_N, A_MODEL, A_START = 45000, 5000, 48, 2021, 2026
A_DOWN = A_PRICE * AUTO_DOWN
A_AMT = A_PRICE - A_DOWN
A_INST = flat_inst(A_AMT, AUTO_USED_FLAT_G13, A_N)
A_DBR = A_INST / A_SAL
A_INT = A_INST * A_N - A_AMT
A_RED = flat_to_reducing(AUTO_USED_FLAT_G13, A_N)
A_AGE_END = A_START + A_N // 12 - A_MODEL
A_BANK_INT = flat_inst(A_AMT, .0215, A_N) * A_N - A_AMT
assert A_DBR <= DBR_MAX and A_AGE_END <= 10

# ---------- 6. Sara: declined because BNPL is counted ----------
S_INC, S_PL, S_CARDLIM, S_BNPL, S_ASK, S_GRADE = 9000, 3200, 20000, 600, 10000, 5
S_RATE = NONASSIGNED[S_GRADE]
S_CARD = S_CARDLIM * CARD_FACTOR
S_DBR_BNPL = (S_PL + S_CARD + S_BNPL) / S_INC
S_DBR_NO = (S_PL + S_CARD) / S_INC
S_NEW = pmt(S_ASK, S_RATE, 48)
S_DBR_AFTER = (S_PL + S_CARD + S_BNPL + S_NEW) / S_INC
S_HEAD = DBR_MAX * S_INC - (S_PL + S_CARD)
S_LOAN = annuity_pv(S_HEAD, S_RATE, 48)
assert S_DBR_BNPL > DBR_MAX

SCENARIOS = [
    {
        "title": "Mariam, staff nurse: a loan without moving her salary",
        "who": "Expat staff nurse at a private hospital (employer category C). Gross salary AED {}; 8 months in the job; AECB score 585; one credit card with an AED {} limit.".format(n0(M_SAL), n0(M_CARD)),
        "ask": "AED {} over {} months. She does not want to move her salary account.".format(n0(M_AMT), M_N),
        "banks": "Most banks need AED 8,000–10,000 without a salary transfer: decline. RAKBANK's no-transfer loan (AED 5,000, AECB 541, 12.99–22.49%) is the one bank route.",
        "market": "Finance companies approve at about 20–28% (Finance House from 20%; Deem 15.99–39.99%).",
        "ours": "Employer-assigned track: the hospital signs a salary-assignment letter and EOS undertaking; she repays by direct debit from her current account. AI grade {} → **{}**. (The non-assigned track would need AED 7,000 salary at her score, so the assigned route is the right one.)".format(M_GRADE, pc(M_RATE, 2)),
        "result": "Approved at {} a month. She pays {} interest instead of {} at a typical 24%: a saving of **{}**.".format(aed(M_INST), aed(M_INT), aed(M_24_INT), aed(M_24_INT - M_INT)),
        "maths": [
            ("Maximum loan", "lower of 20 × {} and AED 300,000".format(n0(M_SAL)), aed(M_MAX)),
            ("Card counted in DBR", "5% × AED {} limit".format(n0(M_CARD)), aed(M_CARDPAY)),
            ("Monthly instalment", "AED {}, {} months, {} reducing".format(n0(M_AMT), M_N, pc(M_RATE, 2)), aed(M_INST)),
            ("DBR", "({} + {}) ÷ {}".format(n0(M_INST), n0(M_CARDPAY), n0(M_SAL)), pc(M_DBR) + " (limit 50%)"),
            ("Total interest", "{} instalments − AED {} borrowed (exact, before rounding)".format(M_N, n0(M_AMT)), aed(M_INT)),
            ("Same loan at 24%", "typical finance company", aed(M_24_INT)),
        ],
    },
    {
        "title": "Ravi, construction worker: AED {} before payday".format(n0(R_AMT)),
        "who": "Construction worker paid through WPS into a bank account (employer category D). Net salary AED {}; 2 years in the job; AECB 610; no other debts.".format(n0(R_NET)),
        "ask": "AED {} mid-month for a family emergency.".format(n0(R_AMT)),
        "banks": "Below every bank's minimum salary: no product.",
        "market": "e& easyCredit (fee 8% + VAT = {}); Deem salary advance (≤ AED 1,500, flat fee AED 30–75, needs a Deem WPS card); botim small loans.".format(aed(R_EAND)),
        "ours": "Salary advance: flat fee **{} incl. VAT**, no interest, repaid from the next salary by direct debit. The KFS shows the annual rate (about {} a year, because the fee covers one month). At most 6 advances a year, never two at once.".format(aed(R_FEE_VAT), pc(R_APR, 0)),
        "result": "Approved. Costs {} against {} at e& easyCredit; in line with Deem, without needing a payroll card.".format(aed(R_FEE_VAT), aed(R_EAND)),
        "maths": [
            ("Maximum advance", "lower of 50% × {} and AED 5,000".format(n0(R_NET)), aed(R_MAX)),
            ("Fee band", "AED 1,001–2,500 → AED {} + 5% VAT".format(R_FEE), aed(R_FEE_VAT)),
            ("Repaid on payday", "{} + {}".format(n0(R_AMT), n0(R_FEE_VAT)), aed(R_REPAY)),
            ("Share of salary", "{} ÷ {}".format(n0(R_REPAY), n0(R_NET)), pc(R_SHARE) + " (limit 50%)"),
            ("Cost of the advance", "{} ÷ {}".format(n0(R_FEE_VAT), n0(R_AMT)), pc(R_COST)),
            ("e& easyCredit, same amount", "8% + VAT", aed(R_EAND)),
        ],
    },
    {
        "title": "Khalid, government employee: buying out a 28% loan",
        "who": "UAE national, government (category A). Gross salary AED {}; AECB 690. Has a finance-company loan: AED {} outstanding at 28%, {} months left, instalment {}.".format(n0(K_SAL), n0(K_BAL), K_N, aed(K_OLD)),
        "ask": "A cheaper loan for the same amount and term.",
        "banks": "A bank salary-transfer loan from about 5.49% would be cheapest, but only if he moves his salary to that bank.",
        "market": "Finance-company buyouts to AED 320–400k at 14–28%.",
        "ours": "Buyout on the employer-assigned track, AI grade {} → **{}**. No processing fee; we pay the old lender directly and give him a written cost comparison.".format(K_GRADE, pc(K_RATE, 2)),
        "result": "Saves **{}** a month and **{}** over {} months. A bank would save him {} if he moves his salary; the cost comparison says so.".format(aed(K_OLD - K_NEW), aed(K_OLD_TOT - K_NEW_TOT), K_N, aed(K_OLD_TOT - K_BANK_TOT)),
        "maths": [
            ("Old lender's settlement fee", "1% × {} + VAT".format(n0(K_BAL)), aed(K_ES)),
            ("New loan", "{} + {}".format(n0(K_BAL), n0(K_ES)), aed(K_P)),
            ("New instalment", "{} months at {}".format(K_N, pc(K_RATE, 2)), aed(K_NEW)),
            ("DBR", "{} ÷ {}".format(n0(K_NEW), n0(K_SAL)), pc(K_DBR) + " (limit 50%)"),
            ("Monthly saving", "{} − {}".format(n0(K_OLD), n0(K_NEW)), aed(K_OLD - K_NEW)),
            ("Saving over {} months".format(K_N), "{} × monthly saving (exact, before rounding)".format(K_N), aed(K_OLD_TOT - K_NEW_TOT)),
        ],
    },
    {
        "title": "Fatima, boutique owner: a gold-backed loan",
        "who": "Self-employed, trade licence 4 years; average business income AED {} a month (12 months of statements). Pledges gold worth AED {}.".format(n0(F_INC), n0(F_GOLD)),
        "ask": "Cash for stock, repaid over 2 years.",
        "banks": "None of the top five banks offers gold-backed loans.",
        "market": "Finance House: 75% of the gold value at 16%.",
        "ours": "70% loan-to-value at **{}** over {} months. Top-up call only if gold falls {}; sale only after a {} fall and written notice.".format(pc(GOLD_RATE, 2), F_N, pc(F_CALL_DROP), pc(F_SALE_DROP)),
        "result": "Approved at {} a month. Interest {} against {} for the same loan at 16%. The lower starting loan-to-value (70% vs 75%) leaves more room before any margin call.".format(aed(F_INST), aed(F_INT), aed(F_16_INT)),
        "maths": [
            ("Loan", "70% × {}".format(n0(F_GOLD)), aed(F_AMT)),
            ("Monthly instalment", "{} months at {}".format(F_N, pc(GOLD_RATE, 2)), aed(F_INST)),
            ("DBR", "{} ÷ {}".format(n0(F_INST), n0(F_INC)), pc(F_DBR) + " (limit 50%)"),
            ("Top-up call", "gold value falls to {} (LTV 80%)".format(aed(F_AMT / GOLD_CALL)), "−" + pc(F_CALL_DROP)),
            ("Sale", "gold value falls to {} (LTV 85%)".format(aed(F_AMT / GOLD_SALE)), "−" + pc(F_SALE_DROP)),
            ("Total interest", "ours vs Finance House 16%", "{} vs {}".format(aed(F_INT), aed(F_16_INT))),
        ],
    },
    {
        "title": "Arjun, sales executive: a used car at AED {} salary".format(n0(A_SAL)),
        "who": "Expat, employer category C. Gross salary AED {}; 14 months in the job; AECB 620. Buying a {} car for AED {} from a dealer.".format(n0(A_SAL), A_MODEL, n0(A_PRICE)),
        "ask": "Auto loan over {} months.".format(A_N),
        "banks": "Emirates NBD, FAB and Mashreq need AED 7,000: decline. ADCB and RAKBANK lend at AED 5,000 at about 2.15–2.90% flat, cheaper than us.",
        "market": "Aafaq (Islamic) from 2.5% flat at AED 5,000.",
        "ours": "Used car, AI grade 1–3 → **{} flat** (about {} reducing). The car is {} years old at the end of the loan (limit 10).".format(pc(AUTO_USED_FLAT_G13, 2), pc(A_RED), A_AGE_END),
        "result": "Approved at {} a month where three of the five big banks decline. On auto we are an access lender, not the cheapest: the price reflects finance-company funding costs.".format(aed(A_INST)),
        "maths": [
            ("Down payment", "20% × {}".format(n0(A_PRICE)), aed(A_DOWN)),
            ("Loan", "{} − {}".format(n0(A_PRICE), n0(A_DOWN)), aed(A_AMT)),
            ("Monthly instalment", "{} × (1 + 4.49% × {}) ÷ {}".format(n0(A_AMT), A_N // 12, A_N), aed(A_INST)),
            ("DBR", "{} ÷ {}".format(n0(A_INST), n0(A_SAL)), pc(A_DBR) + " (limit 50%)"),
            ("Total interest", "ours vs a bank at 2.15% flat", "{} vs {}".format(aed(A_INT), aed(A_BANK_INT))),
        ],
    },
    {
        "title": "Sara, marketing coordinator: the 'no' that protects",
        "who": "Expat, gross salary AED {}. Personal-loan instalment AED {}; cards with AED {} of limits; three BNPL plans totalling AED {} a month.".format(n0(S_INC), n0(S_PL), n0(S_CARDLIM), n0(S_BNPL)),
        "ask": "Another AED {} (non-assigned, AI grade {}).".format(n0(S_ASK), S_GRADE),
        "banks": "Banks count BNPL from the AECB report: decline.",
        "market": "A lender that ignores BNPL sees DBR {} and could lend about {}.".format(pc(S_DBR_NO), aed(S_LOAN)),
        "ours": "BNPL has been in AECB reports since July 2026 and the policy counts it: DBR is already **{}**, above the 50% legal maximum. **Decline**, and offer a consolidation review with a written cost comparison.".format(pc(S_DBR_BNPL)),
        "result": "Declined. Responsible lending is a legal duty, and it keeps the sector's 7.1% net NPL from repeating in our book.",
        "maths": [
            ("Cards counted in DBR", "5% × {}".format(n0(S_CARDLIM)), aed(S_CARD)),
            ("DBR before the new loan, with BNPL", "({} + {} + {}) ÷ {}".format(n0(S_PL), n0(S_CARD), n0(S_BNPL), n0(S_INC)), pc(S_DBR_BNPL) + " (limit 50%)"),
            ("New instalment asked for", "AED {}, 48 months at {}".format(n0(S_ASK), pc(S_RATE, 2)), aed(S_NEW)),
            ("DBR after the new loan", "all debts ÷ {}".format(n0(S_INC)), pc(S_DBR_AFTER)),
            ("DBR if BNPL were ignored", "({} + {}) ÷ {}".format(n0(S_PL), n0(S_CARD), n0(S_INC)), pc(S_DBR_NO)),
        ],
    },
]

SUMMARY = [  # (name, product, outcome, key number)
    ("Mariam", "Personal loan, employer-assigned", "Approved", "{} a month; saves {}".format(aed(M_INST), aed(M_24_INT - M_INT))),
    ("Ravi", "Salary advance", "Approved", "fee {} vs {} at e&".format(aed(R_FEE_VAT), aed(R_EAND))),
    ("Khalid", "Buyout", "Approved", "saves {} a month / {} total".format(aed(K_OLD - K_NEW), aed(K_OLD_TOT - K_NEW_TOT))),
    ("Fatima", "Gold-backed loan", "Approved", "{} a month".format(aed(F_INST))),
    ("Arjun", "Used-car loan", "Approved", "{} a month at 4.49% flat".format(aed(A_INST))),
    ("Sara", "Personal loan", "Declined", "DBR {} with BNPL".format(pc(S_DBR_BNPL))),
]

if __name__ == "__main__":
    for s in SUMMARY:
        print(s)
