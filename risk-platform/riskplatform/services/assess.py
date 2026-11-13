"""Decide: assess one application. Policy first; grade second; POLICY ALWAYS WINS. Declines are recommendations
that a human confirms (AD-7)."""
from riskplatform.core import policy, grading

RANK = {"pass": 0, "refer": 1, "decline_recommended": 2}


def assess(app: dict, rules: list, cfg: dict) -> dict:
    pol = policy.run_policy(rules, app)
    g = grading.grade(app, cfg)
    model_action = grading.grade_band_action(g["grade"], cfg)
    verdict = max(pol["verdict"], model_action, key=RANK.get)
    decision = {"pass": "approve", "refer": "refer_to_underwriter", "decline_recommended": "decline_recommended"}[verdict]
    driver = "policy" if RANK[pol["verdict"]] >= RANK[model_action] and pol["verdict"] != "pass" else \
        ("model_grade" if model_action != "pass" else "none")
    return {"application_id": app["application_id"], "entity_id": app["entity_id"], "segment": app["segment"],
            "product": app["product"], "decision": decision, "driver": driver, "grade": g["grade"], "pd": g["pd"],
            "grade_label": g["label"], "reason_codes": g["reason_codes"],
            "policy_fails": [{"rule_id": r["rule_id"], "layer": r["layer"], "severity": r["severity"],
                              "message": r["message"], "observed": r["observed"], "source": r["source"]}
                             for r in pol["fails"]],
            "not_evaluable": [{"rule_id": r["rule_id"], "missing": r["missing"]} for r in pol["not_evaluable"]]}
