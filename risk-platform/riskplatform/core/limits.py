"""Exposure aggregation and limit checks (pure). Works on de-duplicated facilities in reporting currency."""
from collections import defaultdict


def aggregate(facilities: list, key: str) -> dict:
    agg = defaultdict(lambda: {"exposure": 0.0, "facility_ids": []})
    for f in facilities:
        k = f.get(key) or "UNKNOWN"
        agg[k]["exposure"] += f["exposure_rep"]
        agg[k]["facility_ids"].append(f["facility_id"])
    return dict(agg)


def group_limit_breaches(facilities, entities, cfg):
    """Single borrower / connected group limit: % of entity equity (Basel / CBUAE C 1/2023: 25% of Tier 1)."""
    out = []
    pct = cfg["limits"]["single_borrower_group_pct_of_equity"]
    by_ent = defaultdict(list)
    for f in facilities:
        if f.get("group_id"):
            by_ent[f["entity_id"]].append(f)
    for ent_id, fs in by_ent.items():
        eq = entities[ent_id]["equity_rep"]
        for gid, a in aggregate(fs, "group_id").items():
            if a["exposure"] > eq * pct / 100:
                names = sorted({f["customer_name"] for f in fs if f["group_id"] == gid})
                out.append({"type": "group_limit_breach", "entity_id": ent_id, "group_id": gid,
                            "exposure": round(a["exposure"], 2), "limit": round(eq * pct / 100, 2),
                            "excess": round(a["exposure"] - eq * pct / 100, 2), "borrowers": names,
                            "facility_ids": a["facility_ids"], "rule": f"LIM.GROUP.{pct}PCT"})
    return out


def sector_limit_breaches(facilities, cfg):
    out = []
    caps = cfg["limits"]["sector_cap_pct_of_entity_loans"]
    by_ent = defaultdict(list)
    for f in facilities:
        by_ent[f["entity_id"]].append(f)
    for ent_id, fs in by_ent.items():
        total = sum(f["exposure_rep"] for f in fs if f["segment"] != "retail")
        for sector, a in aggregate([f for f in fs if f["segment"] != "retail"], "sector").items():
            cap = caps.get(sector, caps["default"])
            share = 100 * a["exposure"] / total if total else 0
            if share > cap:
                out.append({"type": "sector_limit_breach", "entity_id": ent_id, "sector": sector,
                            "share_pct": round(share, 2), "cap_pct": cap, "exposure": round(a["exposure"], 2),
                            "rule": f"LIM.SECTOR.{sector.upper()}"})
    return out


def approval_authority_breaches(facilities, cfg):
    auth = cfg["limits"]["approval_authority"]
    return [{"type": "approval_authority_breach", "facility_id": f["facility_id"], "entity_id": f["entity_id"],
             "approved_by": f["approved_by"], "amount": round(f["limit_rep"], 2), "authority": auth[f["approved_by"]],
             "rule": "GOV.APPROVAL.001"}
            for f in facilities if f.get("approved_by") in auth and f["limit_rep"] > auth[f["approved_by"]]]


def staging_errors(facilities, cfg):
    s2, s3 = cfg["staging"]["stage2_dpd"], cfg["staging"]["stage3_dpd"]
    out = []
    for f in facilities:
        expected = 3 if f["dpd"] > s3 else 2 if f["dpd"] > s2 else 1
        if f["stage"] < expected:
            out.append({"type": "staging_error", "facility_id": f["facility_id"], "entity_id": f["entity_id"],
                        "dpd": f["dpd"], "stage": f["stage"], "expected_min_stage": expected, "rule": "IFRS9.BACKSTOP"})
    return out
