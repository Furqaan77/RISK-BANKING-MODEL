import json, sys, pathlib, statistics, csv
S = pathlib.Path(sys.argv[1]); MP = pathlib.Path(sys.argv[2])
d = json.load(open(S/"data.json", encoding="utf-8"))
banks = d["banks"]; measures = d["measures"]
# fix non-STL personal-loan availability per research notes
FIX = {"HSBC Bank Middle East (UAE)":"N","Standard Chartered UAE":"N","Arab Bank UAE":"N","Citibank N.A. UAE":"P",
       "Habib Bank AG Zurich UAE":"P","Bank of Baroda UAE":"?","United Bank Limited UAE":"P","Banque Misr UAE":"P",
       "Al Ahli Bank of Kuwait UAE":"P","National Bank of Kuwait UAE":"?"}
for b in banks:
    if b["bank"] in FIX: b["nonstl_pl"] = FIX[b["bank"]]
    if b["segment"] == "Policy": b["nonstl_pl"] = "Y"
def num(v):
    try: return float(v)
    except: return None
PRICE = {"pl_rate_min","card_rate_month","home_fixed_rate","auto_rate_flat"}
for m in measures:
    m["group"] = "price" if m["key"] in PRICE else "access"
    ents = [(b["short"], num(b[m["key"]])) for b in banks if num(b[m["key"]]) is not None]
    n = len(ents)
    for b in banks:
        v = num(b[m["key"]])
        if v is None: continue
        worse = sum(1 for _, x in ents if (x > v if m["better"]=="low" else x < v))
        ties = sum(1 for _, x in ents if x == v) - 1
        b.setdefault("pct", {})[m["key"]] = round(100*(worse + 0.5*ties)/(n-1), 1)
    # verdict for policy using mid-rank percentile
    pol = next(b for b in banks if b["segment"]=="Policy")
    p = pol["pct"][m["key"]]; m["policy_pct"] = p
    m["verdict"] = "Ahead of most" if p >= 65 else ("Market middle" if p >= 40 else "Behind most")
    m["joint_best"] = m["friendlier"] == 0
league = []
for b in banks:
    pc = b.get("pct", {})
    acc = [v for k, v in pc.items() if k not in PRICE]; pr = [v for k, v in pc.items() if k in PRICE]
    b["access_n"], b["price_n"] = len(acc), len(pr)
    if len(acc) >= 5 and len(pr) >= 2:
        a = statistics.mean(acc); p = statistics.mean(pr)
        league.append(dict(short=b["short"], segment=b["segment"], access=round(a,1), price=round(p,1), overall=round((a+p)/2,1), access_n=len(acc), price_n=len(pr)))
league.sort(key=lambda r: -r["overall"])
for i, r in enumerate(league, 1): r["rank"] = i
for r in league: print(r)
from collections import Counter
print(Counter(m["verdict"] for m in measures), [m["key"] for m in measures if m["joint_best"]])
for m in measures: print(m["key"], m["policy_pct"], m["verdict"])
print(Counter(b["nonstl_pl"] for b in banks if b["segment"]!="Policy"))
d["league"] = league
json.dump(d, open(S/"data.json","w",encoding="utf-8"), indent=1)
with open(MP/"position_table.csv","w",newline="",encoding="utf-8") as fh:
    keys = ["measure","unit","better","policy","n","friendlier","same","less_friendly","rank","median","policy_pct","verdict","joint_best","group","key"]
    w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(measures)
with open(MP/"all_banks.csv", encoding="utf-8") as fh: rows = list(csv.DictReader(fh))
fixmap = {b["bank"]: b["nonstl_pl"] for b in banks}
for r in rows: r["nonstl_pl"] = fixmap.get(r["bank"], r["nonstl_pl"])
with open(MP/"all_banks.csv","w",newline="",encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
