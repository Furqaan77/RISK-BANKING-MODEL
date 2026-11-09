"""Validate the demo_finance_company (pilot UAE finance company) retail credit policy config.

Checks:
  1. All three YAML files parse.
  2. Structure: required keys, unique ids, valid severity / direction / layer / scope, id prefix matches
     layer, every condition is safe DSL (whitelisted syntax only, no inline lookup tables), applies_to
     products exist, split rules (card tiers, card caps, salary-advance fee bands) match the config.
  3. Tighten-only: Layer 1 baseline matches the known CBUAE / FCR values; Layer 2 (company) and
     Layer 3 (products) are never looser than Layer 1; Layer 3 never looser than Layer 2.
  4. Pricing grid, approval matrix, decision bands and portfolio limits are consistent across files.
  5. Conventional vocabulary; FC restrictions (no deposits, no overdraft, no Islamic window, phase 2 off).
  6. Worked examples evaluated THROUGH the rules (safe evaluator) with asserted outcomes.
Run:  python credit-policy-uae-finance-company/config/validate_config.py
Exit code 1 if any check FAILS. FLAG = intentional, explained in README.md.
"""
import ast
import math
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
RULE_KEYS = {"id", "layer", "applies_to", "condition", "severity", "message", "source", "confidence"}
SEVERITIES = {"knockout", "refer", "warn"}
LAYERS = {"regulatory", "company_policy", "credit_policy"}
SCOPES = {"pre_approval", "portfolio_daily", "portfolio_monthly"}
PREFIX_LAYER = [("REG.", "regulatory"), ("PRU.FCR.", "regulatory"), ("PRU.CO.", "company_policy"),
                ("PORT.", "company_policy"), ("CO.RET.", "company_policy"), ("CRED.", "credit_policy")]
ISLAMIC_ONLY_TERMS = ["murabaha", "tawarruq", "ijarah", "profit_rate", "charity", "ibra", "takaful"]
SCANNED_FILES = ["bank_policy.yaml", "credit_policy.yaml", "rules.yaml", "README.md"]

# Known Layer 1 values (independent copy: guards against someone loosening regulatory_baseline)
KNOWN_CBUAE = {"personal_loan_income_multiple_max": 20, "personal_loan_tenor_months_max": 48, "dbr_max_pct": 50,
               "dbr_retiree_max_pct": 30, "auto_ltv_max_pct": 80, "auto_tenor_months_max": 60,
               "top_up_clean_repayment_months_min": 12, "credit_card_min_annual_income_aed": 60000,
               "deferment_fee_max_aed": 100, "rescheduling_fee_max_aed": 250, "security_cheque_max_pct_of_loan": 120,
               "cooling_off_business_days_min": 5, "disbursement_business_days_max": 10}
KNOWN_FCR = {"capital_min_aed": 150000000, "leverage_max_pct_of_capital_funds_years_0_2": 100,
             "liquid_assets_min_pct_of_liabilities": 10, "single_borrower_max_pct": 10, "connected_group_max_pct": 15,
             "large_exposure_threshold_pct": 7, "principal_shareholder_single_max_pct": 10,
             "principal_shareholder_aggregate_max_pct": 20, "board_member_lending_allowed": False,
             "individual_deposits_allowed": False, "islamic_window_allowed": False}
KNOWN_STC = {"max_amount_aed": 20000, "max_multiple_of_net_monthly_income": 3, "max_tenor_months": 12,
             "interest_allowed": False, "total_fees_max_pct": 30, "bureau_check_required_from_aed": 5000}

results = []  # (check, status, detail)


def record(check, ok, detail="", status=None):
    results.append((check, status or ("PASS" if ok else "FAIL"), detail))


# ------------------------------------------------------------------ 1. parse
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

co = docs["bank_policy.yaml"]
cred = docs["credit_policy.yaml"]
rdoc = docs["rules.yaml"]
rules = rdoc["rules"]
prud = rdoc["prudential_rules"]
base = rdoc["regulatory_baseline"]
products = cred["products"]
all_rules = prud + rules
by_id = {r["id"]: r for r in all_rules}

# ------------------------------------------------------------------ safe DSL
ALLOWED_NODES = (ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.BinOp, ast.Add,
                 ast.Sub, ast.Mult, ast.Div, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In,
                 ast.NotIn, ast.Call, ast.Name, ast.Load, ast.Constant, ast.List, ast.Tuple, ast.IfExp)
SAFE_FUNCS = {"min": min, "max": max}


def parse_dsl(expr):
    tree = ast.parse(expr, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"disallowed syntax {type(node).__name__}")
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCS):
            raise ValueError("only min() and max() may be called")
        if isinstance(node, ast.Compare):
            for op, comp in zip(node.ops, node.comparators):
                if isinstance(op, (ast.In, ast.NotIn)) and not isinstance(comp, (ast.List, ast.Tuple)):
                    raise ValueError("`in` needs a literal list")
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} - set(SAFE_FUNCS)
    return tree, names


def evaluate(expr, ctx):
    tree, names = parse_dsl(expr)
    missing = names - set(ctx)
    if missing:
        raise KeyError(f"missing variables {sorted(missing)}")
    return bool(eval(compile(tree, "<rule>", "eval"), {"__builtins__": {}, **SAFE_FUNCS}, dict(ctx)))  # noqa: S307


# ------------------------------------------------------------------ 2. structure
ids = [r.get("id") for r in all_rules]
missing = [(r.get("id"), sorted(RULE_KEYS - set(r))) for r in all_rules if RULE_KEYS - set(r)]
record("rules: required keys", not missing, f"{len(prud)} prudential + {len(rules)} customer rules" + (f"; missing {missing}" if missing else ""))
record("rules: unique ids", len(ids) == len(set(ids)), f"{len(set(ids))} unique")
bad = [r["id"] for r in all_rules if r["severity"] not in SEVERITIES]
record("rules: valid severity", not bad, str(bad) if bad else "")
bad = [r["id"] for r in all_rules if "direction" in r and r["direction"] not in ("max", "min")]
record("rules: valid direction", not bad, str(bad) if bad else "")
bad = [r["id"] for r in all_rules if r["layer"] not in LAYERS]
record("rules: valid layer", not bad, str(bad) if bad else "")
bad = [r["id"] for r in prud if r.get("scope") not in SCOPES]
bad += [r["id"] for r in rules if "scope" in r]
record("prudential rules have a scope; customer rules do not", not bad, str(bad) if bad else "")
bad = []
for r in all_rules:
    want = next((lay for pre, lay in PREFIX_LAYER if r["id"].startswith(pre)), None)
    if want != r["layer"]:
        bad.append((r["id"], r["layer"], want))
record("rules: id prefix matches layer", not bad, str(bad) if bad else "REG/PRU.FCR=L1, CO.RET/PRU.CO/PORT=L2, CRED=L3")
bad = [r["id"] for r in prud if not r["id"].startswith(("PRU.", "PORT."))] + [r["id"] for r in rules if r["id"].startswith(("PRU.", "PORT."))]
record("prudential rules kept separate from customer rules", not bad, str(bad) if bad else "")

lookup = [r["id"] for r in all_rules if "{" in r["condition"] or re.search(r"[\w\)\]\}]\[", r["condition"])]
record("rules: no inline lookup tables", not lookup, str(lookup) if lookup else "all conditions are plain expressions")
dsl_bad = []
for r in all_rules:
    try:
        parse_dsl(r["condition"])
    except Exception as exc:  # noqa: BLE001
        dsl_bad.append((r["id"], str(exc)))
record("rules: safe DSL (whitelisted syntax only)", not dsl_bad, str(dsl_bad) if dsl_bad else "ast whitelist; min/max only")

known_products = set(products) | {"all"}
bad = []
for r in all_rules:
    p = r["applies_to"].get("products")
    for nm in ([p] if isinstance(p, str) else (p or [])):
        if nm not in known_products:
            bad.append((r["id"], nm))
record("rules: applies_to products exist in credit_policy", not bad, str(bad) if bad else "")

tiers = products["credit_card"]["tiers"]
cc_bad = []
for suffix, tier in (("a", "classic"), ("b", "gold"), ("c", "platinum")):
    r1, r3 = by_id.get(f"CRED.CC.001{suffix}"), by_id.get(f"CRED.CC.003{suffix}")
    if not r1 or r1["limit"] != tiers[tier]["min_monthly_gross_income_aed"] or r1["applies_to"].get("card_tier") != tier:
        cc_bad.append(f"CRED.CC.001{suffix}")
    if not r3 or r3["limit"] != tiers[tier]["limit_cap_aed"] or r3["applies_to"].get("card_tier") != tier:
        cc_bad.append(f"CRED.CC.003{suffix}")
record("split card rules match tiers (income, caps)", not cc_bad, str(cc_bad) if cc_bad else "CRED.CC.001a-c, 003a-c")
sa = products["salary_advance"]
sa_bad = [i for i, band in (("CRED.SA.005a", "up_to_1000"), ("CRED.SA.005b", "from_1001_to_2500"), ("CRED.SA.005c", "from_2501_to_5000"))
          if i not in by_id or by_id[i]["limit"] != sa["fee_bands_aed"][band] or by_id[i]["applies_to"].get("advance_band") != band]
record("split salary-advance fee rules match fee bands", not sa_bad, str(sa_bad) if sa_bad else "CRED.SA.005a-c")

# ------------------------------------------------------------------ 3. tighten-only
cb, fcr, stc = base["cbuae"], base["fcr"], base["fcr"]["short_term_credit"]
bad = [k for k, v in KNOWN_CBUAE.items() if cb.get(k) != v] + [k for k, v in KNOWN_FCR.items() if fcr.get(k) != v] \
    + [k for k, v in KNOWN_STC.items() if stc.get(k) != v]
record("L1 baseline = known CBUAE / FCR values", not bad, str(bad) if bad else "regulatory_baseline unchanged")

aff = co["affordability"]
record("L2 DBR <= L1 (50% / retirees 30%)", aff["dbr_max_pct"] <= cb["dbr_max_pct"] and aff["dbr_max_pct_retiree"] <= cb["dbr_retiree_max_pct"],
       f"{aff['dbr_max_pct']} / {aff['dbr_max_pct_retiree']}")
record("L2 BNPL counted in DBR (FCR)", aff["bnpl_instalments_counted_in_full"] is True)

pr = co["prudential"]
record("L2 capital funds >= FCR minimum", pr["capital_funds_aed"] >= fcr["capital_min_aed"], f"{pr['capital_funds_aed']:,}")
record("L2 leverage <= FCR 100%", pr["leverage"]["max_liabilities_pct_of_capital_funds"] <= fcr["leverage_max_pct_of_capital_funds_years_0_2"],
       f"{pr['leverage']['max_liabilities_pct_of_capital_funds']}%")
liq = pr["liquidity"]
record("L2 liquidity >= FCR 10%, trigger above minimum", liq["min_liquid_assets_pct_of_liabilities"] >= fcr["liquid_assets_min_pct_of_liabilities"]
       and liq["internal_trigger_pct"] > liq["min_liquid_assets_pct_of_liabilities"], f"{liq['min_liquid_assets_pct_of_liabilities']}% / trigger {liq['internal_trigger_pct']}%")
le = pr["large_exposures"]
ok = (le["single_borrower_max_pct"] <= fcr["single_borrower_max_pct"] and le["connected_group_max_pct"] <= fcr["connected_group_max_pct"]
      and le["principal_shareholder_affiliate_single_max_pct"] <= fcr["principal_shareholder_single_max_pct"]
      and le["principal_shareholder_affiliate_aggregate_max_pct"] <= fcr["principal_shareholder_aggregate_max_pct"])
record("L2 large-exposure limits <= FCR", ok, f"single {le['single_borrower_max_pct']}%, group {le['connected_group_max_pct']}%")
single_cap = pr["capital_funds_aed"] * le["single_borrower_max_pct"] / 100
record("L2 per-individual cap within single-borrower limit", pr["internal_cap_per_individual_all_products_aed"] <= single_cap,
       f"AED {pr['internal_cap_per_individual_all_products_aed']:,} <= AED {single_cap:,.0f}")
max_assets = pr["capital_funds_aed"] * (1 + pr["leverage"]["max_liabilities_pct_of_capital_funds"] / 100)
record("L2 pilot book cap fits capital + allowed liabilities", pr["pilot_book_cap_gross_retail_loans_aed"] < max_assets,
       f"AED {pr['pilot_book_cap_gross_retail_loans_aed']:,} < AED {max_assets:,.0f}")
ls = co["licence_scope"]
record("L2 FCR prohibitions (board lending, deposits, overdraft, Islamic window)",
       not pr["board_member_lending_allowed"] and not ls["individual_deposits_allowed"] and not ls["overdrafts_allowed"]
       and not ls["islamic_window_allowed"] and ls["cbuae_no_objection_letter_per_product_line"])

pea, pna = products["personal_loan_employer_assigned"], products["personal_loan_non_assigned"]
record("L3 employer-assigned: 20x / 48 m (CBUAE)", pea["max_loan_amount"]["income_multiple"] <= cb["personal_loan_income_multiple_max"]
       and pea["max_tenor_months"] <= cb["personal_loan_tenor_months_max"], f"{pea['max_loan_amount']['income_multiple']}x / {pea['max_tenor_months']} m")
m = pna["max_loan_amount"]
record("L3 non-assigned: multiples <= 20x, 48 m (CBUAE)", max(m["uae_national"]["income_multiple"], m["expat"]["income_multiple"]) <= 20
       and pna["max_tenor_months"] <= 48, f"{m['uae_national']['income_multiple']}x / {m['expat']['income_multiple']}x")
for pname in ("buyout", "eosb_backed"):
    lim = products[pname].get("combined_limits") or products[pname].get("overall_limits")
    record(f"L3 {pname}: within 20x / 48 m (CBUAE)", lim["income_multiple_max"] <= 20 and lim["tenor_months_max"] <= 48, str(lim))
record("L3 top-up: >= 12 months clean (CBUAE)", products["top_up"]["min_clean_repayment_months"] >= cb["top_up_clean_repayment_months_min"])
auto = products["auto_loan"]
record("L3 auto: down >= 20%, tenor <= 60 (CBUAE)", auto["min_down_payment_pct"] >= 100 - cb["auto_ltv_max_pct"]
       and auto["max_tenor_months"] <= cb["auto_tenor_months_max"], f"{auto['min_down_payment_pct']}% / {auto['max_tenor_months']} m")
bad = [t for t, v in tiers.items() if 12 * v["min_monthly_gross_income_aed"] < cb["credit_card_min_annual_income_aed"]]
record("L3 card tiers >= AED 60,000 a year (CBUAE)", not bad, str(bad) if bad else "classic 5,000 x 12 = 60,000")

# fees
fee_bad = []
for pname, p in products.items():
    f = p.get("fees") or {}
    es, pf, lp = f.get("early_settlement"), f.get("processing"), f.get("late_payment")
    if es and (es["pct"] > cb["early_settlement_fee"]["pct"] or es["max_aed"] > cb["early_settlement_fee"]["max_aed"]):
        fee_bad.append((pname, "early settlement"))
    if pf and (pf["pct"] > 1.0 or pf["max_aed"] > cb["processing_fee"]["max_aed"] or pf["min_aed"] > cb["processing_fee"]["min_aed"]):
        fee_bad.append((pname, "processing"))
    if lp:
        cap = cb["late_fee_max_aed"]["auto" if pname == "auto_loan" else "personal"]
        if lp["max_aed"] > cap:
            fee_bad.append((pname, "late fee"))
fd = cred["fee_definitions"]
if products["credit_card"]["pricing"]["late_payment_fee_aed"] > cb["late_fee_max_aed"]["card"]:
    fee_bad.append(("credit_card", "late fee"))
if fd["deferment_aed"] > cb["deferment_fee_max_aed"] or fd["rescheduling_aed"] > cb["rescheduling_fee_max_aed"]:
    fee_bad.append(("fee_definitions", "deferment / rescheduling"))
record("L3 fees within CBUAE caps (all products)", not fee_bad, str(fee_bad) if fee_bad else "ES 1%/10k, processing 1% 500-2,500, late 200/500/230, deferment 100, rescheduling 250")
record("L3 auto late fee tighter than CBUAE (200 vs 500)", auto["fees"]["late_payment"]["max_aed"] < cb["late_fee_max_aed"]["auto"],
       f"{auto['fees']['late_payment']['max_aed']}")
record("L3 security cheque <= 120% (CBUAE)", pea["security"]["security_cheque"]["max_pct_of_loan"] <= cb["security_cheque_max_pct_of_loan"]
       and pna["repayment"]["security_cheque"]["max_pct_of_loan"] <= cb["security_cheque_max_pct_of_loan"]
       and not pea["security"]["security_cheque"]["blank_allowed"])

# short-term credit (salary advance, BNPL) vs FCR caps
ok = (sa["max_amount_aed"] <= stc["max_amount_aed"] and sa["max_pct_of_net_monthly_salary"] / 100 <= stc["max_multiple_of_net_monthly_income"]
      and sa["max_term_days"] <= 30.5 * stc["max_tenor_months"] and sa["interest"] == "none" and sa["total_fees_max_pct_of_advance"] <= stc["total_fees_max_pct"])
record("L3 salary advance within FCR short-term caps", ok, f"max {sa['max_amount_aed']:,}, {sa['max_pct_of_net_monthly_salary']}% of net, {sa['max_term_days']} days, no interest")
bands = {"from_1001_to_2500": 1001, "from_2501_to_5000": 2501}
worst = max((sa["fee_bands_aed"][b] + sa["late_fee_aed_once"]) / lo for b, lo in bands.items())
record("L3 salary advance fees <= 30% in bands 2-3 (incl. late fee)", worst <= stc["total_fees_max_pct"] / 100, f"worst {worst:.1%}")
min_ok = (sa["fee_bands_aed"]["up_to_1000"] + sa["late_fee_aed_once"]) / (stc["total_fees_max_pct"] / 100)
record("L3 salary advance band 1: no minimum advance amount", True,
       f"fee 30 + late fee 50 exceeds 30% below AED {min_ok:,.0f}; REG.STC.004 caps total fees per case; propose a minimum advance [P]",
       status="FLAG")
bn = products["bnpl"]
ok = (bn["max_amount_aed"] <= stc["max_amount_aed"] and bn["max_multiple_of_net_monthly_income"] <= stc["max_multiple_of_net_monthly_income"]
      and bn["max_tenor_months"] <= stc["max_tenor_months"] and bn["interest"] == "none" and bn["total_fees_max_pct"] <= stc["total_fees_max_pct"])
record("L3 BNPL (phase 2) within FCR short-term caps", ok, f"{bn['max_amount_aed']:,} / {bn['max_multiple_of_net_monthly_income']}x / {bn['max_tenor_months']} m / fees {bn['total_fees_max_pct']}%")

# Layer 3 vs Layer 2
cap1m = pr["internal_cap_per_individual_all_products_aed"]
amounts = {"personal_loan_employer_assigned": pea["max_loan_amount"]["cap_aed"],
           "personal_loan_non_assigned": max(m["uae_national"]["cap_aed"], m["expat"]["cap_aed"]),
           "auto_loan": auto["max_loan_amount_aed"], "gold_backed": products["gold_backed"]["max_loan_amount_aed"],
           "salary_advance": sa["max_amount_aed"], "bnpl": bn["max_amount_aed"],
           "credit_card": max(t["limit_cap_aed"] for t in tiers.values())}
bad = [k for k, v in amounts.items() if v > cap1m]
record("L3 product caps <= L2 per-individual cap (AED 1m)", not bad, str(bad) if bad else ", ".join(f"{k} {v:,}" for k, v in amounts.items()))
home_max = products["home_loan"]["phase_2_reference"]["max_loan_amount_aed"]
record("L3 home finance (phase 2, disabled) vs per-individual cap", True,
       f"AED {home_max:,} > AED {cap1m:,}: needs Board Credit Committee exception or a cap change before phase 2", status="FLAG")
se = co["self_employed"]
record("L3 self-employed caps = L2 (PL 250k, card 50k balance)", pna["max_loan_amount"]["self_employed_cap_aed"] <= se["personal_loan_max_aed"]
       and products["credit_card"]["self_employed"]["min_avg_balance_3m_aed"] >= se["min_average_monthly_balance_aed"]["credit_card_3m_average"])
aecb = co["aecb"]["min_score"]
record("L3 non-assigned AECB floors >= L2", pna["min_aecb_score"] >= aecb["non_assigned_pl"]
       and pna["compensating_controls_at_5000"]["min_aecb_score"] >= aecb["non_assigned_pl_aed_5000_entry"],
       f"{pna['min_aecb_score']} / {pna['compensating_controls_at_5000']['min_aecb_score']}")
el = co["eligibility"]
record("L3 minimum incomes >= L2 defaults", pea["min_monthly_gross_income_aed"] >= el["minimum_monthly_gross_income_aed"]["default"]
       and sa["min_net_monthly_salary_aed"] >= el["minimum_monthly_gross_income_aed"]["salary_advance_net_wps"]
       and pna["min_monthly_gross_income_aed_otherwise"] == co["employer_categories"]["D"]["non_assigned_min_income_aed"])
record("L3 service months >= L2", pea["min_service_months"] >= el["minimum_service_months"]["employer_assigned"]
       and pna["min_service_months"] >= el["minimum_service_months"]["non_assigned"]
       and sa["min_service_months"] >= el["minimum_service_months"]["salary_advance"])
record("L3 Cat D employer-assigned cap = L2", pea["max_loan_amount"]["cap_aed_employer_cat_d"] == co["employer_categories"]["D"]["employer_assigned_max_aed"])

# ------------------------------------------------------------------ 4. pricing, matrix, bands, portfolio
grid = co["pricing_grid"]
g_bad = []
for gname in ("personal_loan_employer_assigned_pct", "personal_loan_non_assigned_pct", "auto_new_flat_pct", "auto_used_flat_pct"):
    vals = [grid[gname][g] for g in range(1, 9)]
    if any(b < a for a, b in zip(vals, vals[1:])) or grid[gname][9] is not None or grid[gname][10] is not None:
        g_bad.append(gname)
record("pricing grid: rises with grade; grades 9-10 unpriced", not g_bad, str(g_bad) if g_bad else "4 grids")
ea, na = grid["personal_loan_employer_assigned_pct"], grid["personal_loan_non_assigned_pct"]
record("pricing grid: non-assigned above employer-assigned at every grade", all(na[g] > ea[g] for g in range(1, 9)))
record("pricing grid: used auto above new at every grade", all(grid["auto_used_flat_pct"][g] > grid["auto_new_flat_pct"][g] for g in range(1, 9)))
ok = (pea["pricing"]["interest_rate_floor_pct"] == ea[1] and pea["pricing"]["interest_rate_ceiling_pct"] == ea[8]
      and pna["pricing"]["interest_rate_floor_pct"] == na[1] and pna["pricing"]["interest_rate_ceiling_pct"] == na[8]
      and auto["pricing"]["new_vehicle_flat_pct"] == {"floor": grid["auto_new_flat_pct"][1], "ceiling": grid["auto_new_flat_pct"][8]}
      and auto["pricing"]["used_vehicle_flat_pct"] == {"floor": grid["auto_used_flat_pct"][1], "ceiling": grid["auto_used_flat_pct"][8]})
record("product floors / ceilings = grid grade 1 / grade 8", ok, f"PL-EA {ea[1]}-{ea[8]}, PL-NA {na[1]}-{na[8]}")
ok = products["credit_card"]["pricing"]["monthly_interest_rate_pct"] == grid["credit_card_monthly_pct"] \
    and products["gold_backed"]["pricing"]["interest_rate_pct"] == grid["gold_backed_pct"]
record("card and gold prices = grid", ok)

doa = co["delegation_of_authority"]
uns = [d["unsecured_total_max_aed"] for d in doa[:4]]
sec = [d["secured_max_aed"] for d in doa[:4]]
ok = all(b > a for a, b in zip(uns, uns[1:])) and all(b >= a for a, b in zip(sec, sec[1:])) and uns[-1] == cap1m \
    and doa[0]["max_grade"] == 6 and doa[3]["max_grade"] == 8 and doa[4]["authority"] == "board_credit_committee"
record("approval matrix: rising limits; CRO = AED 1m cap; BCC above", ok, " / ".join(f"{d['authority']} {d['unsecured_total_max_aed']}" for d in doa))
db, gd = co["decision_bands"], cred["grades"]["decision"]
record("decision bands identical (company vs credit policy)", db["approve_grades"] == gd["approve"] and db["refer_grades"] == gd["refer"]
       and db["decline_grades"] == gd["decline"] and db["policy_always_wins"], "approve 1-6, refer 7-8, decline 9-10")
pl = co["portfolio_limits"]
pmap = {"PORT.001": "non_assigned_share_of_pl_book_max_pct", "PORT.002": "category_d_share_of_pl_book_max_pct",
        "PORT.003": "single_employer_share_of_assigned_book_max_pct", "PORT.004": "gold_backed_share_of_retail_book_max_pct",
        "PORT.005": "salary_advance_plus_bnpl_share_of_retail_book_max_pct", "PORT.006": "aecb_541_599_share_of_monthly_approvals_max_pct",
        "PORT.007": "deviation_share_of_monthly_approvals_max_pct"}
bad = [i for i, k in pmap.items() if by_id[i]["limit"] != pl[k]]
record("portfolio rules PORT.001-007 = company portfolio limits", not bad, str(bad) if bad else "7 limits")
ok = (by_id["PRU.CO.001"]["limit"] == pr["pilot_book_cap_gross_retail_loans_aed"] and by_id["PRU.CO.003"]["limit"] == liq["internal_trigger_pct"]
      and by_id["PRU.CO.004"]["limit"] == cap1m and by_id["PRU.CO.002"]["limit"] == pr["leverage"]["early_warning_pct_of_limit"]
      and by_id["PRU.FCR.004"]["limit"] == le["single_borrower_max_pct"] and by_id["PRU.FCR.005"]["limit"] == le["connected_group_max_pct"])
record("prudential rules = company prudential values", ok)

# ------------------------------------------------------------------ 5. scope and vocabulary
off = {k: v["offered_in_pilot"] for k, v in products.items()}
ok = (not off["bnpl"] and not off["home_loan"] and not off["deposit_backed"]
      and all(off[p] for p in ls["phase_1_products"]) and set(ls["phase_2_products"]) == {"bnpl", "home_loan"})
record("product scope: phase 1 on; BNPL / home (phase 2) and deposit-backed off", ok)
pending = [k for k, v in products.items() if v["offered_in_pilot"] and not v["cbuae_nol_received"]]
record("CBUAE no-objection letters on file", True, f"pending for {len(pending)} phase-1 lines: REG.FCR.002 declines them until received (launch gate)",
       status="FLAG")
vp = [n for n, d in docs.items() if d["meta"].get("vocabulary_profile") != "conventional"]
record("vocabulary_profile: conventional in all files", not vp, str(vp) if vp else "")
hits = []
for fname in SCANNED_FILES:
    p = HERE / fname
    if p.exists():
        text = p.read_text(encoding="utf-8").lower()
        hits += [(fname, t) for t in ISLAMIC_ONLY_TERMS if re.search(rf"\b{re.escape(t)}\b", text)]
record("no Islamic-only terms", not hits, str(hits) if hits else f"scanned {', '.join(SCANNED_FILES)}")


# ------------------------------------------------------------------ 6. worked examples through the rules
def pmt(principal, rate_pct, months):
    r = rate_pct / 100 / 12
    return principal * r / (1 - (1 + r) ** -months)


def flat_instalment(principal, flat_pct, months):
    return principal * (1 + flat_pct / 100 * months / 12) / months


DEFAULTS = dict(nationality_group="expat", residency_status="resident", employment_type="salaried", is_retiree=False,
                sanctions_hit=False, age_at_application=35, age_at_maturity=39, service_months=24, income_verified=True,
                current_dpd=0, dpd90_last_24m=False, writeoff_or_settlement_last_24m=False, court_or_police_case_unpaid_debt=False,
                aecb_enquiries_30d=1, aecb_report_pulled=True, aecb_thin_file=False, employer_sector_watch_listed=False,
                essential_expenses_reviewed=True, statements_months=6, uaefts_consent=False, trade_licence_years=0,
                avg_monthly_balance=0, avg_balance_3m=0, kfs_signed_before_contract=True, cooling_off_business_days=5,
                cooling_off_waived_in_writing=False, affordability_summary_signed=True, facility_type="term_loan",
                secured_by_customer_deposit=False, contract_structure="conventional", security_cheque_blank=False,
                security_cheque_pct_of_loan=100, security_cheque_received=True, assignment_letter_received=True,
                eos_undertaking_received=True, uaedds_mandate_signed=True, credit_life_insurance=True, first_instalment_grace_days=0,
                salary_credit_months=6, transaction="new", uses_eosb_security=False, wps_salary=True, wps_credit_months=6,
                is_board_member=False, is_principal_shareholder_or_affiliate=False, is_related_party=False, existing_obligations=0,
                employer_category="B", track="employer_assigned", grade=3, tenor_months=48)
SNAPSHOT = dict(capital_funds=150_000_000, total_liabilities=90_000_000, liquid_assets=13_000_000, gross_retail_loans=180_000_000,
                individual_deposit_accounts=0, borrower_total_exposure=0, connected_group_exposure=0, customer_total_exposure=0,
                related_party_single_exposure=0, related_party_aggregate_exposure=0, share_non_assigned_of_pl_book_pct=28,
                share_category_d_of_pl_book_pct=18, share_max_single_employer_of_assigned_book_pct=3, share_gold_of_retail_book_pct=2.5,
                share_salary_advance_bnpl_of_retail_book_pct=0.8, share_aecb_541_599_of_monthly_approvals_pct=20,
                share_deviations_of_monthly_approvals_pct=3)


def build_case(launched=True, **kw):
    c = {**DEFAULTS, **kw}
    p = products[c["product"]]
    c["product_offered_in_pilot"] = p["offered_in_pilot"]
    c["product_cbuae_nol_received"] = p["cbuae_nol_received"] or (launched and p["offered_in_pilot"])
    loan, g, prod = c["loan_amount"], c["grade"], c["product"]
    inst = 0.0
    if prod in ("personal_loan_employer_assigned", "personal_loan_non_assigned"):
        gname = "personal_loan_employer_assigned_pct" if prod.endswith("employer_assigned") else "personal_loan_non_assigned_pct"
        c.setdefault("interest_rate_pct", grid[gname][g])
        inst = pmt(loan, c["interest_rate_pct"], c["tenor_months"])
    elif prod == "auto_loan":
        c.setdefault("auto_flat_rate_pct", grid["auto_new_flat_pct" if c["vehicle_condition"] == "new" else "auto_used_flat_pct"][g])
        inst = flat_instalment(loan, c["auto_flat_rate_pct"], c["tenor_months"])
    elif prod == "gold_backed":
        c.setdefault("interest_rate_pct", grid["gold_backed_pct"])
        inst = pmt(loan, c["interest_rate_pct"], c["tenor_months"])
    elif prod in ("salary_advance", "bnpl"):
        c.setdefault("interest_rate_pct", 0)
        inst = loan if prod == "salary_advance" else loan / c["tenor_months"]
    if prod == "salary_advance":
        band = "up_to_1000" if loan <= 1000 else ("from_1001_to_2500" if loan <= 2500 else "from_2501_to_5000")
        c.update(advance_band=band, advance_fee_aed=sa["fee_bands_aed"][band], late_payment_fee_aed=sa["late_fee_aed_once"])
        c["total_fees_aed"] = c["advance_fee_aed"] + c["late_payment_fee_aed"]
    else:
        c.setdefault("late_payment_fee_aed", min(max(0.02 * inst, 50), 200))
    c["instalment"] = inst
    c.setdefault("overdue_instalment", inst)
    pure = c.get("pure_buyout", False)
    c.setdefault("processing_fee_aed", 0 if pure else min(max(0.01 * loan, 500), 2500))
    c.setdefault("early_settlement_fee_aed", min(0.01 * loan, 10000))
    c.setdefault("amount_settled", loan)
    c["dbr_after"] = round((c["existing_obligations"] + inst) / c["monthly_gross_income"] * 100, 2)
    return c


def decide(case, snapshot=None):
    ctx = {**(snapshot or SNAPSHOT), **case}
    fails = []
    for r in prud + rules:
        if "scope" in r and r["scope"] != "pre_approval" and r["severity"] != "knockout":
            continue  # portfolio management actions do not change individual decisions
        at, ok = r["applies_to"], True
        for k, v in at.items():
            cv = ctx.get("product") if k == "products" else ctx.get(k)
            if k == "products" and v == "all":
                continue
            if (cv not in v) if isinstance(v, list) else (cv != v):
                ok = False
                break
        if ok and not evaluate(r["condition"], ctx):
            fails.append(r)
    sev = {r["severity"] for r in fails}
    decision = "Decline" if "knockout" in sev else ("Refer" if "refer" in sev else "Approve")
    return decision, [r["id"] for r in fails if r["severity"] != "warn"]


def example(label, ok, detail):
    record(f"Example: {label}", ok, detail)


try:
    # 1. Mariam - expat staff nurse, category C, AED 6,500, AECB 585, card AED 10k limit (AED 500 a month)
    mar = dict(product="personal_loan_employer_assigned", track="employer_assigned", employer_category="C", monthly_gross_income=6500,
               service_months=8, aecb_score=585, existing_obligations=500, loan_amount=60000, tenor_months=48, grade=5, statements_months=3)
    c = build_case(**mar)
    d, f = decide(c)
    max_amt = min(20 * 6500, pea["max_loan_amount"]["cap_aed"])
    example("Mariam, employer-assigned AED 60k / 48 m, grade 5", d == "Approve" and c["interest_rate_pct"] == 17.99
            and abs(c["instalment"] - 1762) < 1 and abs(c["dbr_after"] - 34.8) < 0.1 and max_amt == 130000,
            f"{d}; 17.99%; AED {c['instalment']:,.0f}/month; DBR {c['dbr_after']}%; max AED {max_amt:,}")
    c2 = build_case(**{**mar, "product": "personal_loan_non_assigned", "track": "non_assigned", "statements_months": 6, "salary_credit_months": 8})
    d2, f2 = decide(c2)
    example("Mariam, same customer on the non-assigned track", d2 == "Decline" and f2 == ["CRED.PNA.001"],
            f"{d2} by {f2} (AECB 585 < 600 needs AED 7,000 salary)")
    d3, f3 = decide(build_case(launched=False, **mar))
    example("Mariam before the CBUAE no-objection letter", d3 == "Decline" and "REG.FCR.002" in f3, f"{d3} by {f3}")

    # 2. Ravi - WPS worker, category D, AED 3,500, AECB 610, asks AED 1,500 salary advance
    c = build_case(product="salary_advance", employer_category="D", monthly_gross_income=3500, net_monthly_income=3500,
                   aecb_score=610, loan_amount=1500, term_days=30, advances_last_12m=0, advances_outstanding=0, grade=4, wps_credit_months=24)
    d, f = decide(c)
    example("Ravi, WPS salary advance AED 1,500", d == "Approve" and c["advance_fee_aed"] == 60 and abs(c["dbr_after"] - 42.86) < 0.01,
            f"{d}; fee AED {c['advance_fee_aed']} + VAT = AED {c['advance_fee_aed'] * 1.05:.0f}; max AED {min(0.5 * 3500, 5000):,.0f}; DBR {c['dbr_after']}%")
    d4, f4 = decide(build_case(product="salary_advance", employer_category="D", monthly_gross_income=3500, net_monthly_income=3500,
                               aecb_score=610, loan_amount=1500, term_days=30, advances_last_12m=0, advances_outstanding=1, grade=4))
    example("Ravi, second advance while one is outstanding", d4 == "Decline" and f4 == ["CRED.SA.004"], f"{d4} by {f4}")

    # 3. Khalid - national, government (A), AED 18,000, AECB 690; buys out AED 120k at 28%, 36 months left
    k_old = pmt(120000, 28, 36)
    k_loan = 120000 + 1200 * 1.05
    c = build_case(product="personal_loan_employer_assigned", transaction="buyout", pure_buyout=True, nationality_group="uae_national",
                   employer_category="A", monthly_gross_income=18000, aecb_score=690, loan_amount=k_loan, tenor_months=36, grade=2,
                   liability_letter_age_days=5, pays_other_lender_directly=True, residual_release_requested=False,
                   clearance_letter_received=False, cost_comparison_signed=True, statements_months=3)
    d, f = decide(c)
    save_m, save_t = k_old - c["instalment"], (k_old - c["instalment"]) * 36
    example("Khalid, buyout AED 121,260 / 36 m, grade 2", d == "Approve" and c["interest_rate_pct"] == 13.99 and c["processing_fee_aed"] == 0
            and abs(save_m - 820) < 5 and abs(save_t - 29514) / 29514 < 0.01,
            f"{d}; 13.99%; AED {c['instalment']:,.0f}/month vs AED {k_old:,.0f}; saves AED {save_m:,.0f}/month, AED {save_t:,.0f} total")
    d5, f5 = decide({**c, "cost_comparison_signed": False})
    example("Khalid without a signed cost comparison", d5 == "Decline" and f5 == ["CRED.BO.004"], f"{d5} by {f5}")

    # 4. Fatima - self-employed, licence 4 yrs, AED 25,000 a month, pledges gold worth AED 100,000 (AECB 620 assumed)
    c = build_case(product="gold_backed", employment_type="self_employed", monthly_gross_income=25000, statements_months=12,
                   trade_licence_years=4, aecb_score=620, loan_amount=70000, gold_ltv=70000 / 100000 * 100, tenor_months=24,
                   gold_assayed_in_company_custody=True, grade=3)
    d, f = decide(c)
    example("Fatima, gold-backed AED 70k / 24 m at 70% LTV", d == "Approve" and abs(c["instalment"] - 3394) < 1 and c["dbr_after"] < 14,
            f"{d}; 14.99%; AED {c['instalment']:,.0f}/month; DBR {c['dbr_after']}%; top-up call if gold falls {1 - 70 / 80:.1%}")
    d6, f6 = decide({**c, "gold_ltv": 75.0})
    example("Fatima at 75% LTV (peer level)", d6 == "Decline" and f6 == ["CRED.GOLD.001"], f"{d6} by {f6}")

    # 5. Arjun - expat, category C, AED 5,000, AECB 620; used car AED 45,000, 20% down, 48 m
    c = build_case(product="auto_loan", track="non_assigned", employer_category="C", monthly_gross_income=5000, service_months=14,
                   aecb_score=620, loan_amount=36000, down_payment_pct=20, tenor_months=48, vehicle_condition="used",
                   vehicle_age_at_maturity=9, seller_type="dealer", approved_valuation=False, rta_mortgage_registered=True,
                   comprehensive_motor_insurance=True, company_first_beneficiary=True, grade=2, statements_months=3)
    d, f = decide(c)
    example("Arjun, used-car loan AED 36,000 / 48 m", d == "Approve" and c["auto_flat_rate_pct"] == 4.49 and abs(c["instalment"] - 885) < 1
            and abs(c["dbr_after"] - 17.7) < 0.1, f"{d}; 4.49% flat; AED {c['instalment']:,.0f}/month; DBR {c['dbr_after']}%")

    # 6. Sara - expat, AED 9,000; PL AED 3,200 + cards AED 1,000 + BNPL AED 600 a month; asks AED 10,000
    sara = dict(product="personal_loan_non_assigned", track="non_assigned", monthly_gross_income=9000, aecb_score=600,
                employer_category="B", loan_amount=10000, tenor_months=48, grade=4, statements_months=6)
    c = build_case(existing_obligations=3200 + 1000 + 600, **sara)
    d, f = decide(c)
    dbr_before = (3200 + 1000 + 600) / 9000 * 100
    example("Sara, BNPL counted in DBR", d == "Decline" and f == ["REG.CB.001"] and abs(dbr_before - 53.3) < 0.1,
            f"{d} by {f}; DBR {dbr_before:.1f}% before the new loan, {c['dbr_after']}% after")
    head = 0.5 * 9000 - 4200
    r5 = grid["personal_loan_non_assigned_pct"][5] / 1200
    s_loan = math.floor(head * (1 - (1 + r5) ** -48) / r5)
    c7 = build_case(existing_obligations=4200, **{**sara, "loan_amount": s_loan, "grade": 5})
    d7, f7 = decide(c7)
    example("Sara if BNPL were ignored (the risk the rule stops)", d7 == "Approve" and c7["dbr_after"] <= 50,
            f"{d7}: a lender blind to BNPL would lend AED {s_loan:,} (DBR {c7['dbr_after']}%)")

    # 7. Extra controls
    d8, f8 = decide(build_case(product="bnpl", monthly_gross_income=9000, net_monthly_income=8000, aecb_score=650, loan_amount=2000,
                               tenor_months=4, term_days=120, late_fee_per_instalment_aed=50, total_fees_aed=0, bnpl_active_plans=0, grade=3))
    example("BNPL plan during the pilot (phase 2)", d8 == "Decline" and "CO.RET.000" in f8 and "REG.FCR.002" in f8, f"{d8} by {f8}")
    d9, f9 = decide(build_case(is_board_member=True, **mar))
    example("Board member applies (FCR)", d9 == "Decline" and f9 == ["PRU.FCR.007"], f"{d9} by {f9}")
    stress = {**SNAPSHOT, "liquid_assets": 0.11 * SNAPSHOT["total_liabilities"]}
    d10, f10 = decide(build_case(**mar), stress)
    example("Liquidity at 11% of liabilities (internal trigger 12%)", d10 == "Decline" and f10 == ["PRU.CO.003"], f"{d10} (held) by {f10}")
    d11, f11 = decide(build_case(**{**mar, "grade": 7}))
    example("Mariam at AI grade 7 (model escalation)", d11 == "Refer" and f11 == ["CRED.GRD.001"], f"{d11} by {f11}")
except Exception as exc:  # noqa: BLE001
    record("Examples ran", False, f"{type(exc).__name__}: {exc}")

# ------------------------------------------------------------------ print
counts = {}
for r in all_rules:
    key = ("prudential" if "scope" in r else "customer", r["layer"])
    counts[key] = counts.get(key, 0) + 1
w = max(len(c) for c, _, _ in results)
print(f"{'CHECK'.ljust(w)}  STATUS  DETAIL")
print("-" * (w + 40))
for c, s, dtl in results:
    print(f"{c.ljust(w)}  {s:<6}  {dtl}")
fails = [r for r in results if r[1] == "FAIL"]
flags = [r for r in results if r[1] == "FLAG"]
print("-" * (w + 40))
print("Rule counts: " + "; ".join(f"{blk} {lay} {n}" for (blk, lay), n in sorted(counts.items())) + f"; total {len(all_rules)}")
print(f"{len(results)} checks: {len(results) - len(fails) - len(flags)} pass, {len(flags)} flagged, {len(fails)} fail")
sys.exit(1 if fails else 0)
