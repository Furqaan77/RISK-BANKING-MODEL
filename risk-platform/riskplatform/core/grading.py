"""Grading 1-10 (pure). v1 = ILLUSTRATIVE expert scorecard (label: assumed). It is NOT a validated predictive model.

Organ to add later: trained models behind the same interface (e.g. US mortgage PD on Freddie Mac loan-level data),
registered and approved via maker-checker (AD-8). The interface stays: grade(facts, cfg) -> dict.
"""
import math

# points: (feature, weight, transform). Higher score = lower risk.
RETAIL = [
    ("bureau_score", 0.012, lambda v: v - 600),
    ("dbr_pct", -0.035, lambda v: v - 35),
    ("ltv_pct", -0.015, lambda v: (v or 0) - 70),
    ("max_dpd_12m", -0.04, lambda v: v),
]
BUSINESS = [
    ("dscr", 1.1, lambda v: v - 1.4),
    ("debt_to_ebitda", -0.35, lambda v: v - 3.0),
    ("years_trading", 0.08, lambda v: min(v, 15) - 5),
    ("sector_risk", -0.45, lambda v: v - 2),   # 1 low .. 4 high (assumed sector map)
    ("max_dpd_12m", -0.04, lambda v: v),
]
BASE_LOGODDS = {"retail": -4.3, "sme": -3.6, "corporate": -4.0}


def _card(segment):
    return RETAIL if segment == "retail" else BUSINESS


def grade(facts: dict, cfg: dict) -> dict:
    seg = facts["segment"]
    contributions, z = [], -BASE_LOGODDS[seg]
    for feat, w, f in _card(seg):
        v = facts.get(feat)
        if v is None:
            continue
        c = w * f(v)
        z += c
        contributions.append({"feature": feat, "value": v, "points": round(c, 3)})
    pd = 1 / (1 + math.exp(z))
    bands = cfg["grading"]["pd_band_upper"]
    g = next(i + 1 for i, ub in enumerate(bands) if pd <= ub)
    reasons = sorted([c for c in contributions if c["points"] < 0], key=lambda c: c["points"])[:4]
    return {"grade": g, "pd": round(pd, 5), "label": "assumed (illustrative scorecard)",
            "reason_codes": [f"RC.{r['feature'].upper()}" for r in reasons], "contributions": contributions}


def grade_band_action(g: int, cfg: dict) -> str:
    if g >= cfg["grading"]["decline_recommended_from_grade"]:
        return "decline_recommended"
    if g >= cfg["grading"]["refer_from_grade"]:
        return "refer"
    return "pass"
