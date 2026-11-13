"""Explain (AD-19 evidence or silence). Answers only from approved outputs; every figure cites an evidence ID.
Questions it cannot ground are refused. Text inside data/documents is never treated as an instruction.
v1 = deterministic templates; the LLM port may only rephrase (guarded)."""
import re
from riskplatform.ports.llm import NullLLM, guarded


class Evidence:
    def __init__(self):
        self.items = {}

    def add(self, kind, ref, values):
        eid = f"E-{len(self.items) + 1:05d}"
        self.items[eid] = {"evidence_id": eid, "kind": kind, "ref": ref, "values": values}
        return eid


def build_evidence(findings, assessments, stress, bench):
    ev = Evidence()
    for f in findings:
        f["evidence_id"] = ev.add("finding", f.get("rule"), f)
    for a in assessments:
        a["evidence_id"] = ev.add("assessment", a["application_id"], a)
    for sid, r in stress["results"].items():
        r["evidence_id"] = ev.add("stress", sid, r)
    for b in bench:
        b["evidence_id"] = ev.add("benchmark", b["param_id"], b)
    return ev


def _money(x):
    return f"USD {x:,.0f}"


class Explainer:
    def __init__(self, findings, assessments, stress, bench, register, llm=None):
        self.f, self.a, self.s, self.b, self.reg = findings, {a["application_id"]: a for a in assessments}, stress, bench, register
        self.llm = llm or NullLLM()

    def ask(self, q: str) -> dict:
        ql = q.lower()
        m = re.search(r"\bA\d{5}\b", q)
        if m and m.group(0) in self.a:
            return self._why_app(self.a[m.group(0)])
        if "limit" in ql or "breach" in ql:
            return self._breaches()
        if "stress" in ql or "scenario" in ql or "shortfall" in ql or "loss" in ql:
            return self._stress()
        if "attention" in ql or "management" in ql or "action" in ql:
            return self._attention()
        if "rigid" in ql or "peer" in ql or "benchmark" in ql:
            return self._bench()
        if "vendor" in ql or "liquidity" in ql or "market risk" in ql or "cyber" in ql:
            return self._not_implemented(ql)
        if "changed" in ql or "previous" in ql:
            return self._out("Not available: this is the first run, so there is no previous reporting date to compare.", [], kind="missing")
        return self._out("I cannot answer that from the approved evidence for this run. No answer is given rather than a guess.", [], kind="refused")

    def _out(self, text, eids, kind="fact"):
        return {"answer": guarded(self.llm, text, {}), "evidence_ids": eids, "statement_type": kind}

    def _why_app(self, a):
        parts = [f"Application {a['application_id']} ({a['entity_id']}, {a['product']}): decision {a['decision']}, driven by {a['driver']}."]
        for r in a["policy_fails"]:
            parts.append(f"Rule {r['rule_id']} ({r['layer']}, {r['severity']}) failed: {r['message']}; observed {r['observed']}; source {r['source']}.")
        parts.append(f"Grade {a['grade']} (PD {a['pd']}; {a['grade_label']}); main negative factors: {', '.join(a['reason_codes']) or 'none'}.")
        if a["not_evaluable"]:
            parts.append(f"Missing information: {a['not_evaluable']}.")
        return self._out(" ".join(parts), [a["evidence_id"]])

    def _breaches(self):
        lim = [f for f in self.f if f["type"] in ("group_limit_breach", "sector_limit_breach", "approval_authority_breach")]
        lines = []
        for f in lim:
            if f["type"] == "group_limit_breach":
                lines.append(f"[{f['evidence_id']}] Group {f['group_id']} in {f['entity_id']}: exposure {_money(f['exposure'])} vs limit {_money(f['limit'])} (excess {_money(f['excess'])}); borrowers: {', '.join(f['borrowers'])}.")
            elif f["type"] == "sector_limit_breach":
                lines.append(f"[{f['evidence_id']}] Sector {f['sector']} in {f['entity_id']}: {f['share_pct']}% of business loans vs cap {f['cap_pct']}%.")
            else:
                lines.append(f"[{f['evidence_id']}] Facility {f['facility_id']} approved by {f['approved_by']} for {_money(f['amount'])}, above authority {_money(f['authority'])}.")
        return self._out(f"{len(lim)} limit breaches. " + " ".join(lines), [f["evidence_id"] for f in lim])

    def _stress(self):
        r = self.s["results"]
        lines = [f"[{v['evidence_id']}] {k}: expected loss {_money(v['total']['expected_loss'])} (change vs baseline {_money(v['change_vs_baseline'])})." for k, v in r.items()]
        return self._out("Stress results (scenarios are ASSUMED, not calibrated forecasts). " + " ".join(lines),
                         [v["evidence_id"] for v in r.values()], kind="estimate")

    def _attention(self):
        top = [f for f in self.f if f["type"] in ("group_limit_breach", "approval_authority_breach", "staging_error", "sector_limit_breach")]
        lines = [f"[{f['evidence_id']}] {f['type']} -> owner {f['owner']} (status {f['status']})." for f in top]
        return self._out(f"{len(top)} items need management attention. " + " ".join(lines), [f["evidence_id"] for f in top])

    def _bench(self):
        lines = [f"[{b['evidence_id']}] {b['market']} {b['measure']}: ours {b['ours']} vs peer median {b['peer_median']} -> {b['label']}." for b in self.b]
        return self._out("Position vs regulator and peers (public peer data). " + " ".join(lines), [b["evidence_id"] for b in self.b], kind="interpretation")

    def _not_implemented(self, ql):
        hits = [r for r in self.reg if any(w in ql for w in r["category"].lower().split())]
        names = ", ".join(f"{r['risk_id']} ({r['category']}: {r['status']})" for r in hits) or "the requested area"
        return self._out(f"Not implemented in this version: {names}. No figures are available, so none are given.", [], kind="missing")
