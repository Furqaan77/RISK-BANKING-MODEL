"""Compare engine outputs with the hidden answer sheet (AD-18). Used by run_demo and the tests."""


def check(answer: dict, findings: list, assessments: list, tighten: list, tol=0.01) -> list:
    res = []
    by_app = {a["application_id"]: a for a in assessments}
    for p in answer["planted"]:
        ok, detail = False, ""
        if p["type"] == "group_limit_breach":
            hit = [f for f in findings if f["type"] == p["type"] and f["group_id"] == p["group_id"]]
            if hit:
                f = hit[0]
                ok = abs(f["exposure"] - p["expected_exposure"]) <= tol and abs(f["excess"] - p["expected_excess"]) <= tol
                detail = f"exposure {f['exposure']} vs expected {p['expected_exposure']}"
        elif p["type"] == "duplicate_facility":
            got = sorted(f["facility_id"] for f in findings if f["type"] == "duplicate_facility")
            ok, detail = got == p["facility_ids"], f"found {got}"
        elif p["type"] in ("approval_authority_breach", "staging_error"):
            ok = any(f["type"] == p["type"] and f["facility_id"] == p["facility_id"] for f in findings)
            detail = p["facility_id"]
        elif p["type"] == "sector_limit_breach":
            hit = [f for f in findings if f["type"] == p["type"] and f["entity_id"] == p["entity_id"] and f["sector"] == p["sector"]]
            ok = bool(hit) and abs(hit[0]["share_pct"] - p["expected_share_pct"]) <= tol
            detail = f"share {hit[0]['share_pct'] if hit else None} vs expected {p['expected_share_pct']}"
        elif p["type"] == "policy_fail":
            a = by_app.get(p["application_id"])
            ok = bool(a) and a["decision"] == p["expected_verdict"] and any(r["rule_id"] == p["rule_id"] for r in a["policy_fails"])
            detail = f"decision {a['decision'] if a else None}; fails {[r['rule_id'] for r in a['policy_fails']] if a else None}"
        elif p["type"] == "tighten_only_violation":
            ok = any(t["rule_id"] == p["rule_id"] and t["looser_than"] == p["looser_than"] for t in tighten)
            detail = str([t for t in tighten if t["rule_id"] == p["rule_id"]])
        res.append({"id": p["id"], "type": p["type"], "detected": ok, "detail": detail})
    return res
