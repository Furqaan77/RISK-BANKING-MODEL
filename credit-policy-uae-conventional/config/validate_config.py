"""Validate the demo_conventional_bank retail credit policy config.

Checks:
  1. All three YAML files parse.
  2. Every rule has the required AD-3 keys; no inline lookup tables; split rules match products.
  3. Tighten-only against CBUAE values.
  4. Conventional conversion: fee definitions; no Islamic-only terms left in the conventional files.
  5. Worked examples (max loan / minimum income).
Run:  python credit-policy-uae-conventional/config/validate_config.py
"""
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
REQUIRED_RULE_KEYS = {"id", "layer", "applies_to", "condition", "severity", "message", "source", "confidence"}
SEVERITIES = {"knockout", "refer", "warn"}
ISLAMIC_ONLY_TERMS = ["murabaha", "tawarruq", "ijarah", "profit_rate", "charity", "ibra", "takaful"]
SCANNED_FILES = ["bank_policy.yaml", "credit_policy.yaml", "rules.yaml", "README.md"]

results = []  # (check, status, detail)


def record(check, ok, detail="", status=None):
    results.append((check, status or ("PASS" if ok else "FAIL"), detail))


# 1. Parse
docs = {}
for name in ("bank_policy.yaml", "credit_policy.yaml", "rules.yaml"):
    try:
        docs[name] = yaml.safe_load((HERE / name).read_text(encoding="utf-8"))
        record(f"parse {name}", True)
    except Exception as exc:  # noqa: BLE001
        record(f"parse {name}", False, str(exc))
if len(docs) < 3:
    for r in results:
        print(r)
    sys.exit(1)

bank = docs["bank_policy.yaml"]
cred = docs["credit_policy.yaml"]
rules = docs["rules.yaml"]["rules"]
products = cred["products"]

# 2. Rule keys
ids = [r.get("id") for r in rules]
missing = [(r.get("id"), sorted(REQUIRED_RULE_KEYS - set(r))) for r in rules if REQUIRED_RULE_KEYS - set(r)]
record("rules: required keys", not missing, f"{len(rules)} rules" + (f"; missing {missing}" if missing else ""))
record("rules: unique ids", len(ids) == len(set(ids)), f"{len(set(ids))} unique")
bad_sev = [r["id"] for r in rules if r.get("severity") not in SEVERITIES]
record("rules: valid severity", not bad_sev, str(bad_sev) if bad_sev else "")
bad_dir = [r["id"] for r in rules if "direction" in r and r["direction"] not in ("max", "min")]
record("rules: valid direction", not bad_dir, str(bad_dir) if bad_dir else "")

lookup = [r["id"] for r in rules if "{" in r["condition"] or re.search(r"[\w\)\]\}]\[", r["condition"])]
record("rules: no inline lookup tables", not lookup, str(lookup) if lookup else "all conditions are plain expressions")

known_products = set(products) | {"all"}
bad_prod = []
for r in rules:
    p = r["applies_to"].get("products")
    for name in ([p] if isinstance(p, str) else (p or [])):
        if name not in known_products:
            bad_prod.append((r["id"], name))
record("rules: applies_to products exist in credit_policy", not bad_prod, str(bad_prod) if bad_prod else "")

by_id = {r["id"]: r for r in rules}
tiers = products["credit_card"]["tiers"]
cc_map = {"CRED.CC.001a": "classic_entry", "CRED.CC.001b": "gold", "CRED.CC.001c": "platinum"}
cc_bad = [i for i, t in cc_map.items()
          if i not in by_id or by_id[i]["limit"] != tiers[t]["min_monthly_gross_income_aed"]
          or by_id[i]["applies_to"].get("card_tier") != t]
record("split card-tier rules match credit_policy", not cc_bad, str(cc_bad) if cc_bad else "CRED.CC.001a-c")
ltv_cfg = products["home_loan"]["ltv_max_pct"]
hl_map = {
    "CRED.HL.002a": ("first_home_value_le_5m", "uae_national"), "CRED.HL.002b": ("first_home_value_le_5m", "expat"),
    "CRED.HL.002c": ("first_home_value_gt_5m", "uae_national"), "CRED.HL.002d": ("first_home_value_gt_5m", "expat"),
    "CRED.HL.002e": ("second_or_more_home", "uae_national"), "CRED.HL.002f": ("second_or_more_home", "expat"),
}
hl_bad = [i for i, (band, grp) in hl_map.items()
          if i not in by_id or by_id[i]["limit"] != ltv_cfg[band][grp]
          or by_id[i]["applies_to"].get("property") != band or by_id[i]["applies_to"].get("nationality_group") != grp]
record("split home LTV rules match credit_policy", not hl_bad, str(hl_bad) if hl_bad else "CRED.HL.002a-f")

# 3. Tighten-only vs CBUAE
aff = bank["affordability"]
record("DBR <= 50% (CBUAE)", aff["dbr_max_pct"] <= 50, f"{aff['dbr_max_pct']}")
record("DBR retirees <= 30% (CBUAE)", aff["dbr_max_pct_retiree"] <= 30, f"{aff['dbr_max_pct_retiree']}")
record("DBR govt housing <= 60% (CBUAE)", aff["dbr_max_pct_government_housing_programme"] <= 60,
       f"{aff['dbr_max_pct_government_housing_programme']}")

for pname in ("personal_loan_salary_assigned", "personal_loan_unsecured"):
    p = products[pname]
    record(f"{pname}: tenor <= 48 (CBUAE)", p["max_tenor_months"] <= 48, f"{p['max_tenor_months']}")
    if "max_tenor_months_mod_af" in p:
        record(f"{pname}: MoD/AF tenor 60 (CBUAE exemption)", True, f"{p['max_tenor_months_mod_af']} - VERIFY exemption",
               status="FLAG")
pls = products["personal_loan_salary_assigned"]["max_loan_amount"]
record("PL salary-assigned multiple <= 20 (CBUAE)", pls["income_multiple"] <= 20, f"{pls['income_multiple']}")
plu = products["personal_loan_unsecured"]["max_loan_amount"]
mults = [plu["uae_national"]["income_multiple"], plu["expat"]["income_multiple"]]
record("PL unsecured multiples <= 20 (CBUAE)", max(mults) <= 20, f"{mults}")
eos = products["eosb_backed"]["overall_limits"]
record("EOSB-backed within 20x / 48m (CBUAE)", eos["income_multiple_max"] <= 20 and eos["tenor_months_max"] <= 48, f"{eos}")
bo = products["buyout"]["combined_limits"]
record("Buyout within 20x / 48m (CBUAE)", bo["income_multiple_max"] <= 20 and bo["tenor_months_max"] <= 48, f"{bo}")

auto = products["auto_loan"]
record("Auto down payment >= 20% (CBUAE)", auto["min_down_payment_pct"] >= 20, f"{auto['min_down_payment_pct']}")
record("Auto tenor <= 60 (CBUAE)", auto["max_tenor_months"] <= 60, f"{auto['max_tenor_months']}")

hl = products["home_loan"]
ltv = hl["ltv_max_pct"]
cbuae_ltv = {
    "first_home_value_le_5m": {"uae_national": 85, "expat": 80},
    "first_home_value_gt_5m": {"uae_national": 75, "expat": 70},
    "second_or_more_home": {"uae_national": 65, "expat": 60},
}
for band, caps in cbuae_ltv.items():
    for grp, cap in caps.items():
        v = ltv[band][grp]
        record(f"Home LTV {band} {grp} <= {cap} (CBUAE)", v <= cap, f"{v}")
record("Home LTV off-plan <= 50 (CBUAE)", ltv["off_plan"] <= 50, f"{ltv['off_plan']}")
record("Home tenor <= 25 yrs (CBUAE)", hl["max_tenor_years"] <= 25, f"{hl['max_tenor_years']}")
record("Home tenor 30 yrs rate-relief exception", True,
       f"{hl['max_tenor_years_cbuae_rate_relief_exception']} - CBUAE exception only", status="FLAG")
record("Home DBR <= 50% (CBUAE)", hl["affordability"]["dbr_max_pct"] <= 50, f"{hl['affordability']['dbr_max_pct']}")

for pname, p in products.items():
    es = (p.get("fees") or {}).get("early_settlement")
    if isinstance(es, dict) and "pct" in es:
        ok = es["pct"] <= 1.0 and es["max_aed"] <= 10000
        record(f"{pname}: early settlement <= 1% / AED 10,000 (CBUAE)", ok, f"{es['pct']}% / {es['max_aed']}")

# 4. Conventional conversion
for pname in ("personal_loan_salary_assigned", "personal_loan_unsecured", "auto_loan"):
    lp = products[pname]["fees"]["late_payment"]
    ok = lp["pct_of_overdue_instalment"] == 2.0 and lp["min_aed"] == 50 and lp["max_aed"] == 200 and lp["retained_as_income"]
    record(f"{pname}: late fee 2% (min 50, max 200) + VAT", ok, f"{lp['pct_of_overdue_instalment']}% / {lp['min_aed']}-{lp['max_aed']}")
card_fee = products["credit_card"]["pricing"]["late_payment_fee_aed"]
record("credit_card: late fee AED 230 + VAT", card_fee == 230, f"{card_fee}")
for pname in ("personal_loan_salary_assigned", "personal_loan_unsecured"):
    record(f"{pname}: credit life insurance mandatory (P-20a)", products[pname]["insurance"]["credit_life_insurance"] == "mandatory")
record("home_loan: life + property insurance mandatory",
       hl["insurance"]["life_insurance"] == "mandatory" and hl["insurance"]["property_insurance"] == "mandatory")
record("auto_loan: comprehensive motor insurance required", auto["security"]["comprehensive_motor_insurance"] == "required")
dep = products["deposit_backed"]
record("deposit_backed: loan or overdraft, 90%, overdraft 12 months renewable",
       set(dep["facility_types"]) == {"term_loan", "overdraft"} and dep["max_advance_pct_of_deposit"] == 90
       and dep["overdraft_tenor_months"] == 12 and dep["overdraft_renewable"])

term_hits = []
for fname in SCANNED_FILES:
    text = (HERE / fname).read_text(encoding="utf-8").lower()
    for term in ISLAMIC_ONLY_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", text):
            term_hits.append((fname, term))
record("no Islamic-only terms in conventional files", not term_hits,
       str(term_hits) if term_hits else f"scanned {', '.join(SCANNED_FILES)} for {', '.join(ISLAMIC_ONLY_TERMS)}")


# 5. Worked examples
def pl_salary_assigned_max(income, group, employer_cat="B"):
    p = products["personal_loan_salary_assigned"]["max_loan_amount"]
    caps = [p["income_multiple"] * income, p["cap_aed"][group]]
    if employer_cat == "D":
        caps.append(p["cap_aed_employer_cat_d"])
    return min(caps)


def pl_unsecured_max(income, group):
    p = products["personal_loan_unsecured"]["max_loan_amount"][group]
    return min(p["income_multiple"] * income, p["cap_aed"])


def pl_unsecured_eligible(income, employer_cat, aecb):
    p = products["personal_loan_unsecured"]
    c = p["compensating_controls_at_5000"]
    low = income >= p["min_monthly_gross_income_aed"] and aecb >= c["min_aecb_score"] and employer_cat in c["employer_categories_allowed"]
    high = income >= p["min_monthly_gross_income_aed_cat_d_or_aecb_541_599"] and aecb >= 541
    return low or high


def home_min_income_ok(income, group, govt_scheme=False):
    m = products["home_loan"]["min_monthly_gross_income_aed"]
    need = m["expat"] if group == "expat" else (m["uae_national_government_housing_scheme"] if govt_scheme else m["uae_national"])
    return income >= need, need


a = pl_salary_assigned_max(5000, "uae_national")
record("Example (a) salary-assigned PL, national, AED 5,000 -> max 100,000", a == 100000, f"max = {a:,}")
elig_b = pl_unsecured_eligible(12000, "B", 640)
b = pl_unsecured_max(12000, "expat")
record("Example (b) non-STL expat AED 12,000, Cat B, AECB 640 -> eligible, max 120,000", elig_b and b == 120000,
       f"eligible = {elig_b}, max = {b:,}")
ok_c, need_c = home_min_income_ok(12000, "expat")
record("Example (c) home loan expat AED 12,000 -> fails minimum 15,000", (not ok_c) and need_c == 15000,
       f"meets minimum = {ok_c}, required = {need_c:,}")

# Print table
w = max(len(c) for c, _, _ in results)
print(f"{'CHECK'.ljust(w)}  STATUS  DETAIL")
print("-" * (w + 40))
for c, s, d in results:
    print(f"{c.ljust(w)}  {s:<6}  {d}")
fails = [r for r in results if r[1] == "FAIL"]
flags = [r for r in results if r[1] == "FLAG"]
print("-" * (w + 40))
print(f"{len(results)} checks: {len(results) - len(fails) - len(flags)} pass, {len(flags)} flagged, {len(fails)} fail")
sys.exit(1 if fails else 0)
