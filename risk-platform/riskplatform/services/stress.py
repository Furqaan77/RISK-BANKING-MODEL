"""Stress: run every configured scenario on the clean book; report change vs baseline. Assumptions kept separate."""
from riskplatform.core.stress import run_scenario


def run_all(book, entities, cfg) -> dict:
    res = {s["id"]: run_scenario(book, entities, s, cfg) for s in cfg["scenarios"]}
    base = res["S0_baseline"]["total"]["expected_loss"]
    for r in res.values():
        r["change_vs_baseline"] = round(r["total"]["expected_loss"] - base, 2)
    return {"assumptions": cfg["scenarios"], "results": res}
