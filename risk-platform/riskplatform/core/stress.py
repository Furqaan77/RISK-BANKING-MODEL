"""Stress engine (pure). Expected loss = PD x LGD x EAD per facility, summed by entity. Scenarios are ASSUMED.

Order of events is explicit (AD-22): 1) FX translation, 2) collateral haircut (raises LGD on secured),
3) PD multipliers. Each facility's loss is computed once per scenario - no double counting.
"""


def _lgd(f, cfg, haircut):
    lgd = cfg["grading"]["lgd"]
    base = lgd["retail_secured"] if f["segment"] == "retail" and f.get("secured") else \
        lgd["retail_unsecured"] if f["segment"] == "retail" else lgd[f["segment"]]
    if haircut and f.get("secured") and f.get("collateral_value_rep"):
        cover = max(0.0, min(1.0, f["collateral_value_rep"] * (1 - haircut) / max(f["exposure_rep"], 1)))
        base = min(1.0, max(base, 1 - cover * 0.9))
    return base


def run_scenario(facilities, entities, scen, cfg):
    sh = scen.get("shocks", {})
    fxc = sh.get("fx_change", {})
    pdm = sh.get("pd_multiplier", {})
    pds = sh.get("pd_multiplier_by_sector", {})
    hc = sh.get("collateral_haircut", 0)
    by_ent = {e: {"ead": 0.0, "el": 0.0} for e in entities}
    for f in facilities:
        if f["stage"] == 3:
            pd = 1.0
        else:
            pd = f["pd"] * pdm.get(f["segment"], 1.0) * pds.get(f.get("sector"), 1.0)
            pd = min(pd, 1.0)
        ead = f["exposure_rep"] * (1 + fxc.get(f["currency"], 0))
        el = pd * _lgd(f, cfg, hc) * ead
        by_ent[f["entity_id"]]["ead"] += ead
        by_ent[f["entity_id"]]["el"] += el
    out = {}
    for e, v in by_ent.items():
        eq = entities[e]["equity_rep"] * (1 + fxc.get(entities[e]["currency"], 0))
        out[e] = {"ead": round(v["ead"], 2), "expected_loss": round(v["el"], 2),
                  "equity": round(eq, 2), "loss_pct_equity": round(100 * v["el"] / eq, 2) if eq else None}
    total = {"ead": round(sum(v["ead"] for v in out.values()), 2),
             "expected_loss": round(sum(v["expected_loss"] for v in out.values()), 2)}
    return {"scenario": scen["id"], "description": scen["description"], "label": "assumed scenario",
            "by_entity": out, "total": total}
