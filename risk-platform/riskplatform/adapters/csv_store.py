"""Data adapter: loads CSV/YAML, standardises types and converts to reporting currency (FX documented in config).
Swap this adapter for a bank data-warehouse / LOS adapter later; the services do not change."""
import csv, json
from datetime import date
from pathlib import Path
import yaml

NUM = {"balance", "limit", "rate", "collateral_value", "pd", "amount", "monthly_income", "dbr_pct", "ltv_pct", "lti",
       "dti_pct", "dscr", "debt_to_ebitda", "stress_rate_add_pp"}
INT = {"dpd", "stage", "secured", "term_months", "age", "bureau_score", "bureau_checked", "income_verified",
       "affordability_assessed", "max_dpd_12m", "years_trading", "sector_risk"}


def _typed(row):
    out = {}
    for k, v in row.items():
        if v in ("", None):
            out[k] = None
        elif k in NUM:
            out[k] = float(v)
        elif k in INT:
            out[k] = int(float(v))
        else:
            out[k] = v
    return out


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return [_typed(r) for r in csv.DictReader(f)]


class Store:
    def __init__(self, root: Path, cfg_path: Path):
        self.root = root
        self.cfg = yaml.safe_load(open(cfg_path, encoding="utf-8"))
        self.fx = self.cfg["fx_to_reporting"]
        self.rep_date = date.fromisoformat(self.cfg["run"]["reporting_date"])

    def entities(self):
        return {e["entity_id"]: {**e, "equity_rep": e["equity"] * self.fx[e["currency"]]} for e in self.cfg["entities"]}

    def facilities_raw(self):
        return load_csv(self.root / "data/facilities.csv")

    def to_reporting(self, facilities):
        for f in facilities:
            r = self.fx[f["currency"]]
            f["exposure_rep"] = f["balance"] * r
            f["limit_rep"] = f["limit"] * r
            f["collateral_value_rep"] = (f.get("collateral_value") or 0) * r
            f["group_id"] = f.get("ultimate_owner_id")       # connected group = common ultimate owner
        return facilities

    def applications(self):
        apps = load_csv(self.root / "data/applications.csv")
        for a in apps:
            if a.get("bureau_date"):
                a["bureau_age_days"] = (self.rep_date - date.fromisoformat(a["bureau_date"])).days
        return apps

    def control_totals(self):
        return json.load(open(self.root / "data/ledger_control_totals.json"))

    def rules(self):
        rules = []
        for e in self.cfg["entities"]:
            for r in yaml.safe_load(open(self.root / f"packs/{e['pack']}/regulator.yaml", encoding="utf-8"))["rules"]:
                rules.append({**r, "entity": e["entity_id"]})      # regulator pack applies to its entity
        for layer in ("bank_policy", "credit_policy"):
            rules += yaml.safe_load(open(self.root / f"packs/demo_group/{layer}.yaml", encoding="utf-8"))["rules"]
        return rules
