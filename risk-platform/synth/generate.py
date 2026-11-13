"""Generate the fictional Demo Group bank (label: synthetic) with PLANTED problems and a hidden answer sheet (AD-18).

Usage: python synth/generate.py [config/run.yaml]
Writes data/{customers,facilities,applications}.csv, data/ledger_control_totals.json, data/answer_sheet.json
"""
import csv, json, random, sys
from datetime import date, timedelta
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTORS = ["real_estate", "construction", "trade", "manufacturing", "logistics", "hospitality", "healthcare", "technology"]
SECTOR_RISK = {"real_estate": 3, "construction": 4, "trade": 2, "manufacturing": 2, "logistics": 2,
               "hospitality": 3, "healthcare": 1, "technology": 2}
TARGET_SHARE = {  # non-retail exposure share by sector; UAE real estate deliberately high (P5)
    "UAE01": {"real_estate": 0.30, "construction": 0.06, "trade": 0.16, "manufacturing": 0.14, "logistics": 0.10,
              "hospitality": 0.10, "healthcare": 0.08, "technology": 0.06},
    "default": {"real_estate": 0.12, "construction": 0.08, "trade": 0.16, "manufacturing": 0.18, "logistics": 0.12,
                "hospitality": 0.10, "healthcare": 0.12, "technology": 0.12},
}
CORP_SIZE = {"UAE01": (50e6, 400e6), "UK01": (10e6, 80e6), "US01": (20e6, 150e6)}   # local currency
SME_SIZE = {"UAE01": (0.3e6, 6e6), "UK01": (0.05e6, 1.5e6), "US01": (0.1e6, 2e6)}
RETAIL_PRODUCTS = ["personal_loan", "credit_card", "mortgage", "auto_loan"]


def approver_for(amount_rep, auth):
    for level, cap in sorted(auth.items(), key=lambda kv: kv[1]):
        if amount_rep <= cap:
            return level
    return "credit_committee"


def main(cfg_path=ROOT / "config/run.yaml"):
    cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))
    rnd = random.Random(cfg["run"]["seed"])
    rep_date = date.fromisoformat(cfg["run"]["reporting_date"])
    fx = cfg["fx_to_reporting"]
    auth = cfg["limits"]["approval_authority"]
    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    customers, facilities, applications = [], [], []
    answer = {"label": "HIDDEN ANSWER SHEET - do not feed to the engines", "planted": []}
    n = cfg["sizes"]
    fid = 0

    def new_fac(ent, cust, segment, product, sector, amount, secured, coll, dpd=0, stage=None, approved_by=None, pd=None):
        nonlocal fid
        fid += 1
        cur = ent["currency"]
        stage = stage if stage is not None else (3 if dpd > 90 else 2 if dpd > 30 else 1)
        orig = rep_date - timedelta(days=rnd.randint(60, 1800))
        fac = {"facility_id": f"F{fid:06d}", "customer_id": cust["customer_id"], "customer_name": cust["name"],
               "entity_id": ent["entity_id"], "segment": segment, "product": product, "sector": sector,
               "currency": cur, "balance": round(amount, 2), "limit": round(amount * (1.0 if segment == "retail" else 1.1), 2),
               "rate": round(rnd.uniform(3.5, 12.0) if segment != "retail" else rnd.uniform(4.0, 24.0), 2),
               "origination": orig.isoformat(), "maturity": (orig + timedelta(days=rnd.randint(365, 3650))).isoformat(),
               "secured": int(secured), "collateral_value": round(coll, 2), "dpd": dpd, "stage": stage,
               "approved_by": approved_by or approver_for(amount * 1.1 * fx[cur], auth),
               "pd": pd if pd is not None else round(min(0.5, rnd.lognormvariate(-4.2, 0.7)), 5),
               "ultimate_owner_id": cust["ultimate_owner_id"], "data_label": "synthetic"}
        facilities.append(fac)
        return fac

    for ent in cfg["entities"]:
        e = ent["entity_id"]
        # ---- retail
        for i in range(n["retail_facilities_per_entity"]):
            c = {"customer_id": f"{e}-R{i:05d}", "name": f"Retail customer {e}-{i:05d}", "entity_id": e,
                 "segment": "retail", "sector": "household", "ultimate_owner_id": f"{e}-R{i:05d}"}
            customers.append(c)
            prod = rnd.choice(RETAIL_PRODUCTS)
            amt = {"personal_loan": rnd.uniform(5e3, 60e3), "credit_card": rnd.uniform(1e3, 15e3),
                   "mortgage": rnd.uniform(150e3, 900e3), "auto_loan": rnd.uniform(15e3, 70e3)}[prod]
            amt *= {"UAE01": 3.67, "UK01": 0.79, "US01": 1.0}[e]
            sec = prod in ("mortgage", "auto_loan")
            dpd = rnd.choices([0, 15, 45, 120], weights=[92, 4, 2.5, 1.5])[0]
            new_fac(ent, c, "retail", prod, "household", amt, sec, amt * 1.3 if sec else 0, dpd=dpd)
        # ---- SME + corporate exposures first, sectors assigned to hit target shares
        pending = []
        for i in range(n["sme_facilities_per_entity"]):
            pending.append(("sme", f"{e}-S{i:04d}", rnd.uniform(*SME_SIZE[e])))
        for i in range(n["corporate_customers_per_entity"]):
            pending.append(("corporate", f"{e}-C{i:04d}", rnd.uniform(*CORP_SIZE[e])))
        planted_falcon = []
        if e == "UAE01":   # P1: three differently named borrowers, one ultimate owner -> group over limit
            for cid, name, sector, amt in [("UAE01-C9001", "Falcon Trading LLC", "trade", 650e6),
                                           ("UAE01-C9002", "Al Saqr General Contracting", "construction", 520e6),
                                           ("UAE01-C9003", "Peregrine Logistics FZE", "logistics", 630e6)]:
                planted_falcon.append((cid, name, sector, amt))
        total = sum(a for _, _, a in pending) + sum(p[3] for p in planted_falcon)
        targets = TARGET_SHARE.get(e, TARGET_SHARE["default"])
        filled = {s: 0.0 for s in SECTORS}
        for _, _, sector, amt in planted_falcon:
            filled[sector] += amt
        rnd.shuffle(pending)
        for seg, cid, amt in sorted(pending, key=lambda p: -p[2]):
            gap = {s: targets[s] * total - filled[s] for s in SECTORS}
            sector = max(gap, key=gap.get)
            filled[sector] += amt
            c = {"customer_id": cid, "name": f"{'SME' if seg == 'sme' else 'Corporate'} {cid}", "entity_id": e,
                 "segment": seg, "sector": sector, "ultimate_owner_id": f"OWN-{cid}"}
            customers.append(c)
            new_fac(ent, c, seg, "term_loan" if seg == "corporate" else rnd.choice(["term_loan", "pos_loan", "overdraft"]),
                    sector, amt, rnd.random() < 0.6, amt * rnd.uniform(0.5, 1.5))
        for cid, name, sector, amt in planted_falcon:
            c = {"customer_id": cid, "name": name, "entity_id": e, "segment": "corporate", "sector": sector,
                 "ultimate_owner_id": "OWN-FALCON-HOLDINGS"}
            customers.append(c)
            new_fac(ent, c, "corporate", "term_loan", sector, amt, True, amt * 0.8, approved_by="credit_committee")

    # ---- P4: approval above authority (US corporate, credit officer approved USD 4m limit)
    us_corp = next(f for f in facilities if f["entity_id"] == "US01" and f["segment"] == "corporate")
    us_corp.update({"balance": 3_600_000.0, "limit": 4_000_000.0, "approved_by": "credit_officer"})
    # ---- P8: corporate 95 dpd still Stage 1 (UK)
    uk_corp = next(f for f in facilities if f["entity_id"] == "UK01" and f["segment"] == "corporate")
    uk_corp.update({"dpd": 95, "stage": 1})
    # control totals are the "ledger": computed BEFORE planting duplicates
    control = {}
    for f in facilities:
        control[f["entity_id"]] = round(control.get(f["entity_id"], 0) + f["balance"], 2)
    # ---- P3: duplicate rows in the source file (UK retail)
    dups = [f for f in facilities if f["entity_id"] == "UK01" and f["segment"] == "retail"][:2]
    facilities.extend(dict(d) for d in dups)

    # ---- answer sheet expected values (computed from ground truth, independently of the engines)
    eq_rep = {en["entity_id"]: en["equity"] * fx[en["currency"]] for en in cfg["entities"]}
    falcon = [f for f in facilities if f["ultimate_owner_id"] == "OWN-FALCON-HOLDINGS"]
    falcon_exp = round(sum(f["balance"] * fx[f["currency"]] for f in falcon), 2)
    lim = eq_rep["UAE01"] * cfg["limits"]["single_borrower_group_pct_of_equity"] / 100
    seen, uniq = set(), []
    for f in facilities:
        if f["facility_id"] not in seen:
            seen.add(f["facility_id"]); uniq.append(f)
    uae_nr = [f for f in uniq if f["entity_id"] == "UAE01" and f["segment"] != "retail"]
    re_share = 100 * sum(f["balance"] for f in uae_nr if f["sector"] == "real_estate") / sum(f["balance"] for f in uae_nr)
    answer["planted"] += [
        {"id": "P1", "type": "group_limit_breach", "entity_id": "UAE01", "group_id": "OWN-FALCON-HOLDINGS",
         "expected_exposure": falcon_exp, "expected_limit": round(lim, 2), "expected_excess": round(falcon_exp - lim, 2),
         "borrowers": sorted(f["customer_name"] for f in falcon)},
        {"id": "P3", "type": "duplicate_facility", "facility_ids": sorted(d["facility_id"] for d in dups)},
        {"id": "P4", "type": "approval_authority_breach", "facility_id": us_corp["facility_id"]},
        {"id": "P5", "type": "sector_limit_breach", "entity_id": "UAE01", "sector": "real_estate",
         "expected_share_pct": round(re_share, 2)},
        {"id": "P8", "type": "staging_error", "facility_id": uk_corp["facility_id"], "expected_min_stage": 3},
        {"id": "P9", "type": "tighten_only_violation", "rule_id": "BANK.UAE.DBR.900", "looser_than": "REG.UAE.DBR.001"},
    ]

    # ---- applications (new business to decide)
    def app(i, ent_id, seg, prod, **kw):
        base = {"application_id": f"A{i:05d}", "entity_id": ent_id, "segment": seg, "product": prod,
                "bureau_checked": 1, "bureau_date": (rep_date - timedelta(days=rnd.randint(1, 60))).isoformat(),
                "max_dpd_12m": rnd.choice([0, 0, 0, 0, 15, 30]), "data_label": "synthetic"}
        base.update(kw)
        applications.append(base)
        return base

    ents = [x["entity_id"] for x in cfg["entities"]]
    for i in range(n["new_applications"]):
        e = ents[i % 3]
        if rnd.random() < 0.75:
            prod = rnd.choice(["personal_loan", "mortgage", "credit_card"])
            inc = rnd.uniform(4000, 30000)
            kw = dict(monthly_income=round(inc, 2), age=rnd.randint(19, 64), bureau_score=rnd.randint(480, 820),
                      dbr_pct=round(rnd.uniform(10, 48), 1), income_verified=1, affordability_assessed=1,
                      nationality=rnd.choice(["national", "expat"]))
            if prod == "personal_loan":
                kw.update(amount=round(inc * rnd.uniform(2, 15), 2), term_months=rnd.choice([24, 36, 48]))
            elif prod == "mortgage":
                kw.update(amount=round(inc * 12 * rnd.uniform(2.5, 5.0), 2), term_months=rnd.choice([240, 300, 360]),
                          ltv_pct=round(rnd.uniform(50, 80), 1), lti=round(rnd.uniform(2.5, 5.0), 2),
                          dti_pct=round(rnd.uniform(20, 44), 1), stress_rate_add_pp=1)
            else:
                kw.update(amount=round(inc * rnd.uniform(0.5, 3), 2), term_months=0)
            app(i, e, "retail", prod, **kw)
        else:
            seg = rnd.choice(["sme", "corporate"])
            app(i, e, seg, "term_loan", amount=round(rnd.uniform(*(SME_SIZE if seg == "sme" else CORP_SIZE)[e]), 2),
                dscr=round(rnd.uniform(0.9, 2.6), 2), debt_to_ebitda=round(rnd.uniform(1.0, 5.5), 2),
                years_trading=rnd.randint(1, 30), sector_risk=rnd.randint(1, 4), bureau_score=rnd.randint(500, 800))
    k = n["new_applications"]
    p2 = app(k, "UAE01", "retail", "personal_loan", monthly_income=15000, age=34, bureau_score=700, dbr_pct=62.0,
             amount=150000, term_months=48, income_verified=1, affordability_assessed=1, nationality="expat")
    p6 = app(k + 1, "UK01", "retail", "mortgage", monthly_income=5000, age=31, bureau_score=760, dbr_pct=30.0,
             amount=372000, term_months=300, ltv_pct=75.0, lti=6.2, dti_pct=33.0, stress_rate_add_pp=1,
             income_verified=1, affordability_assessed=1, nationality="expat")
    p7 = app(k + 2, "US01", "retail", "personal_loan", monthly_income=7000, age=45, bureau_score=720, dbr_pct=25.0,
             amount=20000, term_months=36, income_verified=1, affordability_assessed=1, nationality="national",
             bureau_date=(rep_date - timedelta(days=140)).isoformat())
    answer["planted"] += [
        {"id": "P2", "type": "policy_fail", "application_id": p2["application_id"], "rule_id": "REG.UAE.DBR.001",
         "expected_verdict": "decline_recommended"},
        {"id": "P6", "type": "policy_fail", "application_id": p6["application_id"], "rule_id": "BANK.UK.LTI.001",
         "expected_verdict": "decline_recommended"},
        {"id": "P7", "type": "policy_fail", "application_id": p7["application_id"], "rule_id": "CRED.ALL.BUR.001",
         "expected_verdict": "decline_recommended"},
    ]
    answer["planted"].sort(key=lambda p: int(p["id"][1:]))

    def write(name, rows):
        keys = sorted({k for r in rows for k in r})
        with open(out / name, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader(); w.writerows(rows)
    write("customers.csv", customers)
    write("facilities.csv", facilities)
    write("applications.csv", applications)
    json.dump(control, open(out / "ledger_control_totals.json", "w"), indent=1)
    json.dump(answer, open(out / "answer_sheet.json", "w"), indent=1)
    print(f"customers={len(customers)} facilities_rows={len(facilities)} applications={len(applications)} planted={len(answer['planted'])}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "config/run.yaml")
