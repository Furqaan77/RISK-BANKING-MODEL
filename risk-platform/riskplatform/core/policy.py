"""Policy engine (pure). Layers: regulator -> bank_policy -> credit_policy. Policy always wins over the model.

Conditions use a SAFE expression subset (comparisons, arithmetic, and/or/not, `in`, min/max, if-else). No calls
other than min/max, no attribute access, no imports: rule files are data, never code.
"""
import ast

LAYER_ORDER = ["regulator", "bank_policy", "credit_policy"]
_ALLOWED = (ast.Expression, ast.BoolOp, ast.And, ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.Compare, ast.Eq, ast.NotEq,
            ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div,
            ast.Name, ast.Load, ast.Constant, ast.IfExp, ast.Call, ast.List, ast.Tuple)
_FUNCS = {"min": min, "max": max}


def _check(node):
    for n in ast.walk(node):
        if not isinstance(n, _ALLOWED):
            raise ValueError(f"disallowed syntax in rule: {type(n).__name__}")
        if isinstance(n, ast.Call) and not (isinstance(n.func, ast.Name) and n.func.id in _FUNCS):
            raise ValueError("only min()/max() calls allowed")


def compile_condition(expr: str):
    tree = ast.parse(expr, mode="eval")
    _check(tree)
    return compile(tree, "<rule>", "eval")


def evaluate(rule: dict, facts: dict) -> dict:
    """Return a rule result. Missing facts -> 'not_evaluable' (never silently pass)."""
    code = rule.get("_code") or compile_condition(rule["condition"])
    names = {n.id for n in ast.walk(ast.parse(rule["condition"], mode="eval")) if isinstance(n, ast.Name)} - set(_FUNCS)
    missing = sorted(n for n in names if facts.get(n) is None)
    base = {"rule_id": rule["id"], "layer": rule["layer"], "severity": rule["severity"],
            "message": rule["message"], "source": rule.get("source"), "confidence": rule.get("confidence")}
    if missing:
        return {**base, "outcome": "not_evaluable", "missing": missing}
    ok = bool(eval(code, {"__builtins__": {}}, {**_FUNCS, **facts}))  # safe: AST whitelisted above
    return {**base, "outcome": "pass" if ok else "fail",
            "observed": {k: facts.get(k) for k in names}}


def applicable(rule: dict, facts: dict) -> bool:
    scope = set(rule.get("applies_to", []))
    tags = {facts.get("segment"), facts.get("product")}
    if rule.get("entity") and rule["entity"] != facts.get("entity_id"):
        return False
    return bool(scope & tags)


def run_policy(rules: list, facts: dict) -> dict:
    results = [evaluate(r, facts) for r in rules if applicable(r, facts)]
    fails = [r for r in results if r["outcome"] == "fail"]
    unknown = [r for r in results if r["outcome"] == "not_evaluable"]
    if any(r["severity"] == "knockout" for r in fails):
        verdict = "decline_recommended"
    elif any(r["severity"] == "refer" for r in fails) or unknown:
        verdict = "refer"
    else:
        verdict = "pass"
    return {"verdict": verdict, "results": results, "fails": fails, "not_evaluable": unknown}


def tighten_only_violations(rules: list) -> list:
    """A lower layer may not be looser than a higher layer on the same measure/scope (AD-2, P9)."""
    out = []
    for lo in rules:
        for hi in rules:
            if LAYER_ORDER.index(lo["layer"]) <= LAYER_ORDER.index(hi["layer"]):
                continue
            if lo.get("measure") != hi.get("measure") or lo.get("direction") != hi.get("direction"):
                continue
            if not (set(lo.get("applies_to", [])) & set(hi.get("applies_to", []))):
                continue
            if hi.get("entity") and lo.get("entity") and hi["entity"] != lo["entity"]:
                continue
            looser = lo["limit"] > hi["limit"] if lo["direction"] == "max" else lo["limit"] < hi["limit"]
            if looser:
                out.append({"rule_id": lo["id"], "looser_than": hi["id"], "measure": lo["measure"],
                            "limit": lo["limit"], "higher_limit": hi["limit"]})
    return out
