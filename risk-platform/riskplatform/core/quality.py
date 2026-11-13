"""Data quality checks (pure): duplicates, missing identifiers, impossible values, reconciliation."""
from collections import Counter

REQUIRED = ["facility_id", "customer_id", "entity_id", "currency", "balance"]


def check_facilities(rows: list) -> dict:
    issues = []
    counts = Counter(r["facility_id"] for r in rows)
    dups = sorted(k for k, n in counts.items() if n > 1)
    for d in dups:
        issues.append({"type": "duplicate_facility", "facility_id": d, "rows": counts[d], "rule": "DQ.DUP.001"})
    for r in rows:
        miss = [k for k in REQUIRED if r.get(k) in (None, "")]
        if miss:
            issues.append({"type": "missing_field", "facility_id": r.get("facility_id"), "fields": miss, "rule": "DQ.MISS.001"})
        if r.get("balance") is not None and float(r["balance"]) < 0:
            issues.append({"type": "impossible_value", "facility_id": r["facility_id"], "field": "balance", "rule": "DQ.VAL.001"})
    seen, clean = set(), []
    for r in rows:                      # keep first occurrence; duplicates are reported, never double counted
        if r["facility_id"] in seen:
            continue
        seen.add(r["facility_id"])
        clean.append(r)
    return {"issues": issues, "clean": clean, "rows_in": len(rows), "rows_out": len(clean)}


def reconcile(clean: list, control_totals: dict) -> list:
    out = []
    for ent, expected in control_totals.items():
        actual = round(sum(float(r["balance"]) for r in clean if r["entity_id"] == ent), 2)
        if abs(actual - expected) > 0.01:
            out.append({"type": "reconciliation_difference", "entity_id": ent, "ledger": expected,
                        "loaded": actual, "difference": round(actual - expected, 2), "rule": "DQ.REC.001"})
    return out
