"""Monitor: data quality -> clean book -> exposures and findings. Read-only (AD-20)."""
from riskplatform.core import quality, limits
from riskplatform.core.limits import aggregate


def monitor(store) -> dict:
    raw = store.facilities_raw()
    dq = quality.check_facilities(raw)
    book = store.to_reporting(dq["clean"])
    ents = store.entities()
    rec = quality.reconcile(dq["clean"], store.control_totals())
    findings = (limits.group_limit_breaches(book, ents, store.cfg) + limits.sector_limit_breaches(book, store.cfg)
                + limits.approval_authority_breaches(book, store.cfg) + limits.staging_errors(book, store.cfg)
                + dq["issues"] + rec)
    owners = {"group_limit_breach": "Head of Credit Risk", "sector_limit_breach": "Head of Credit Risk",
              "approval_authority_breach": "Head of Credit Administration", "staging_error": "Finance - IFRS 9 team",
              "duplicate_facility": "Data Owner - Lending", "missing_field": "Data Owner - Lending",
              "impossible_value": "Data Owner - Lending", "reconciliation_difference": "Finance - Reconciliation"}
    for i, f in enumerate(findings, 1):
        f["finding_id"] = f"FND-{i:04d}"
        f["owner"] = owners.get(f["type"], "Chief Risk Officer")
        f["status"] = "open"
    summary = {k: {g: round(v["exposure"], 2) for g, v in sorted(aggregate(book, k).items())}
               for k in ("entity_id", "segment", "sector")}
    return {"book": book, "findings": findings, "summary": summary,
            "dq": {"rows_in": dq["rows_in"], "rows_out": dq["rows_out"], "reconciliation": rec}}
