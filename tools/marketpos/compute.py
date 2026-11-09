import csv, json, statistics, pathlib, sys
MP = pathlib.Path(sys.argv[1])
rows = []
for f in ["banks_core.csv", "banks_national_rest.csv", "banks_foreign.csv"]:
    with open(MP / f, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append(r)
EXCLUDE = {"Doha Bank UAE"}  # legacy fees only, no active retail lending
TOP5 = {"Emirates NBD", "Abu Dhabi Islamic Bank", "FAB", "Dubai Islamic Bank", "ADCB"}
ISLAMIC = {"Emirates Islamic", "Sharjah Islamic Bank", "Ajman Bank", "Al Hilal Bank"}
DIGITAL = {"Wio Bank", "Ruya", "Al Maryah Community Bank (Mbank)", "Reem Community Bank"}
SHORT = {"Emirates NBD": "Emirates NBD", "Emirates Islamic": "Emirates Islamic", "FAB": "FAB", "ADCB": "ADCB",
 "Dubai Islamic Bank": "DIB", "Abu Dhabi Islamic Bank": "ADIB", "Mashreq": "Mashreq", "RAKBANK": "RAKBANK",
 "Commercial Bank of Dubai": "CBD", "Sharjah Islamic Bank": "Sharjah Islamic", "Ajman Bank": "Ajman Bank",
 "Al Hilal Bank": "Al Hilal", "National Bank of Fujairah": "NBF", "National Bank of Umm Al Qaiwain": "NBQ",
 "Bank of Sharjah": "Bank of Sharjah", "United Arab Bank": "UAB", "Invest Bank": "Invest Bank",
 "Commercial Bank International": "CBI", "Al Masraf": "Al Masraf", "Wio Bank": "Wio", "Ruya": "Ruya",
 "Al Maryah Community Bank (Mbank)": "Mbank", "Reem Community Bank": "Reem Bank",
 "HSBC Bank Middle East (UAE)": "HSBC", "Standard Chartered UAE": "Standard Chartered", "Citibank N.A. UAE": "Citibank",
 "Arab Bank UAE": "Arab Bank", "Habib Bank AG Zurich UAE": "Habib Bank AG Zurich", "Bank of Baroda UAE": "Bank of Baroda",
 "United Bank Limited UAE": "UBL", "Banque Misr UAE": "Banque Misr", "Al Ahli Bank of Kuwait UAE": "ABK",
 "National Bank of Kuwait UAE": "NBK", "OUR POLICY (bank)": "Our policy"}
FOREIGN_PL_NONSTL = {"HSBC Bank Middle East (UAE)": "N", "Standard Chartered UAE": "N"}  # other foreign: only other products
merged = []
for r in rows:
    b = r["bank"]
    if b in EXCLUDE: continue
    if b.startswith("OUR POLICY"): seg = "Policy"
    elif b in TOP5: seg = "Top-5"
    elif b in ISLAMIC: seg = "Islamic"
    elif b in DIGITAL: seg = "Digital"
    elif r["type"].startswith("foreign"): seg = "Foreign"
    else: seg = "Other national"
    ns = (r.get("nonstl_offered") or "").strip().upper()
    if seg == "Foreign":
        ns = FOREIGN_PL_NONSTL.get(b, "P")
    elif ns in ("YES",): ns = "Y"
    elif ns == "": ns = "?"
    r2 = dict(r); r2["segment"] = seg; r2["short"] = SHORT.get(b, b); r2["nonstl_pl"] = ns
    merged.append(r2)
cols = list(rows[0].keys())
cols = [c for c in cols if c != "notes"] + ["segment", "short", "nonstl_pl"]
with open(MP / "all_banks.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(merged)

policy = next(r for r in merged if r["segment"] == "Policy")
banks = [r for r in merged if r["segment"] != "Policy"]
def num(v):
    try: return float(v)
    except: return None
MEASURES = [
 ("pl_min_salary_stl", "Personal loan: minimum salary (with salary transfer)", "AED", "low"),
 ("pl_min_salary_nonstl", "Personal loan without salary transfer: minimum salary", "AED", "low"),
 ("pl_max_nat_aed", "Personal loan: maximum amount for UAE nationals", "AED", "high"),
 ("pl_max_exp_aed", "Personal loan: maximum amount for expats", "AED", "high"),
 ("pl_rate_min", "Personal loan: lowest rate (reducing)", "%", "low"),
 ("card_min_salary", "Credit card: entry minimum salary", "AED", "low"),
 ("card_rate_month", "Credit card: monthly rate", "%", "low"),
 ("home_min_salary_nat", "Home loan: minimum salary for UAE nationals", "AED", "low"),
 ("home_min_salary_exp", "Home loan: minimum salary for expats", "AED", "low"),
 ("home_ltv_nat", "Home loan: max loan-to-value, first home (nationals)", "%", "high"),
 ("home_ltv_exp", "Home loan: max loan-to-value, first home (expats)", "%", "high"),
 ("home_fixed_rate", "Home loan: headline fixed rate", "%", "low"),
 ("auto_min_salary", "Auto loan: minimum salary", "AED", "low"),
 ("auto_max_aed", "Auto loan: maximum amount", "AED", "high"),
 ("auto_rate_flat", "Auto loan: headline flat rate (new car)", "%", "low"),
 ("deposit_advance_pct", "Lending against deposits: advance %", "%", "high"),
]
out = []
for key, label, unit, better in MEASURES:
    pv = num(policy[key]); vals = [(r["short"], num(r[key]), r["segment"]) for r in banks if num(r[key]) is not None]
    n = len(vals)
    if better == "low":
        friendlier = sum(1 for _, v, _ in vals if v < pv); tie = sum(1 for _, v, _ in vals if v == pv); worse = sum(1 for _, v, _ in vals if v > pv)
    else:
        friendlier = sum(1 for _, v, _ in vals if v > pv); tie = sum(1 for _, v, _ in vals if v == pv); worse = sum(1 for _, v, _ in vals if v < pv)
    med = statistics.median([v for _, v, _ in vals])
    rank = friendlier + 1
    share_fr = friendlier / n
    if share_fr <= 1/3: verdict = "Customer-friendly"
    elif share_fr <= 2/3: verdict = "Market middle"
    else: verdict = "Careful"
    # tie-aware nuance: if many ties and not many friendlier, mark middle when policy == median
    out.append(dict(key=key, measure=label, unit=unit, better=better, policy=pv, n=n, friendlier=friendlier, same=tie,
                    less_friendly=worse, rank=rank, median=med, verdict=verdict))
with open(MP / "position_table.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
json.dump({"measures": out, "banks": merged}, open(pathlib.Path(sys.argv[2]) / "data.json", "w", encoding="utf-8"), indent=1)
for o in out:
    print(f"{o['key']:22} pol={o['policy']:>10} n={o['n']:2} friendlier={o['friendlier']:2} same={o['same']:2} worse={o['less_friendly']:2} rank={o['rank']:2} median={o['median']:>10} {o['verdict']}")
from collections import Counter
print("segments", Counter(r["segment"] for r in banks), "total", len(banks))
print("nonstl", Counter(r["nonstl_pl"] for r in banks))
bands = Counter()
for r in banks:
    v = num(r["pl_min_salary_stl"])
    if v is None: continue
    b = "Up to AED 4k" if v <= 4000 else "AED 5k" if v <= 5000 else "AED 6–8k" if v <= 8000 else "AED 10–12.5k" if v <= 12500 else "AED 15k+"
    bands[b] += 1
print("bands", bands)
print("nonstl salary", [(r["short"], r["pl_min_salary_nonstl"]) for r in banks if r["pl_min_salary_nonstl"]])
