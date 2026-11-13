"""End-to-end skeleton run on the fictional Demo Group bank.

  python run_demo.py            # generate data if missing, run all engines, write outputs/
Outputs: outputs/results.json, outputs/report.md, outputs/audit.jsonl
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import yaml
from riskplatform.adapters.csv_store import Store
from riskplatform.audit.log import AuditLog, verify
from riskplatform.core.policy import tighten_only_violations
from riskplatform.services import assess, portfolio, stress, benchmark, explain, acceptance

DEMO_QUESTIONS = ["Which limits were breached?", "Why was application {p2} declined?",
                  "What do the stress scenarios show?", "Which issues require management attention?",
                  "Is our policy too rigid versus peers?", "Which services depend on this vendor?",
                  "What changed since the previous reporting date?", "What is the CEO's favourite colour?"]


def run(cfg_path=ROOT / "config/run.yaml", write=True):
    if not (ROOT / "data/facilities.csv").exists():
        from synth import generate
        generate.main(cfg_path)
    store = Store(ROOT, cfg_path)
    cfg = store.cfg
    audit = AuditLog(ROOT / "outputs/audit.jsonl")
    audit.record("system", "run_start", cfg["run"])

    rules = store.rules()
    tighten = tighten_only_violations(rules)
    audit.record("policy_engine", "tighten_only_check", tighten)

    apps = store.applications()
    assessments = [assess.assess(a, rules, cfg) for a in apps]
    audit.record("assess", "applications_assessed", [(a["application_id"], a["decision"]) for a in assessments])

    mon = portfolio.monitor(store)
    audit.record("monitor", "findings", [(f["finding_id"], f["type"]) for f in mon["findings"]])

    st = stress.run_all(mon["book"], store.entities(), cfg)
    audit.record("stress", "scenarios_run", {k: v["total"] for k, v in st["results"].items()})

    master = ROOT.parent / "master-rulebook/data"
    bench = benchmark.position(rules, master)
    register = yaml.safe_load(open(ROOT / "config/risk_register.yaml", encoding="utf-8"))["risks"]

    ev = explain.build_evidence(mon["findings"], assessments, st, bench)
    ex = explain.Explainer(mon["findings"], assessments, st, bench, register)
    answer = json.load(open(ROOT / "data/answer_sheet.json"))
    p2 = next(p["application_id"] for p in answer["planted"] if p["id"] == "P2")
    qa = [{"question": q.format(p2=p2), **ex.ask(q.format(p2=p2))} for q in DEMO_QUESTIONS]

    acc = acceptance.check(answer, mon["findings"], assessments, tighten)
    audit.record("acceptance", "answer_sheet_check", acc)

    results = {"run": cfg["run"], "tighten_only_violations": tighten,
               "decisions": {d: sum(1 for a in assessments if a["decision"] == d)
                             for d in ("approve", "refer_to_underwriter", "decline_recommended")},
               "findings": mon["findings"], "dq": mon["dq"], "exposure_summary": mon["summary"],
               "stress": {k: {"total": v["total"], "change_vs_baseline": v["change_vs_baseline"], "by_entity": v["by_entity"]}
                          for k, v in st["results"].items()},
               "benchmark": bench, "qa": qa, "acceptance": acc, "risk_register": register}
    canon = json.dumps({k: results[k] for k in ("tighten_only_violations", "decisions", "findings", "stress", "acceptance")},
                       sort_keys=True, default=str)
    results["results_hash"] = hashlib.sha256(canon.encode()).hexdigest()
    audit.record("system", "run_end", results["results_hash"])
    results["audit_chain_valid"] = verify(ROOT / "outputs/audit.jsonl")
    results["evidence_count"] = len(ev.items)
    if write:
        (ROOT / "outputs").mkdir(exist_ok=True)
        json.dump(results, open(ROOT / "outputs/results.json", "w"), indent=1, default=str)
        (ROOT / "outputs/report.md").write_text(report(results), encoding="utf-8")
    return results


def report(r):
    L = [f"# Demo Group: skeleton run ({r['run']['reporting_date']}, {r['run']['reporting_currency']})",
         "", "All data is SYNTHETIC and all limits/scenarios are ASSUMED. The grade is an illustrative scorecard, not a validated model.", "",
         "## 1. Answer sheet (planted problems)", "| ID | Problem | Detected | Detail |", "|---|---|---|---|"]
    L += [f"| {a['id']} | {a['type']} | {'YES' if a['detected'] else 'NO'} | {a['detail'][:90]} |" for a in r["acceptance"]]
    L += ["", "## 2. Decisions on new applications", "| Decision | Count |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in r["decisions"].items()]
    L += ["", "## 3. Findings (monitor)", "| ID | Type | Entity | Owner | Evidence |", "|---|---|---|---|---|"]
    L += [f"| {f['finding_id']} | {f['type']} | {f.get('entity_id', '')} | {f['owner']} | {f.get('evidence_id', '')} |" for f in r["findings"]]
    L += ["", "## 4. Stress (expected loss, USD)", "| Scenario | Expected loss | Change vs baseline |", "|---|---|---|"]
    L += [f"| {k} | {v['total']['expected_loss']:,.0f} | {v['change_vs_baseline']:,.0f} |" for k, v in r["stress"].items()]
    L += ["", "## 5. Benchmark vs peers", "| Market | Measure | Ours | Peer median | Label |", "|---|---|---|---|---|"]
    L += [f"| {b['market']} | {b['measure']} | {b['ours']} | {b['peer_median']} | {b['label']} |" for b in r["benchmark"]]
    L += ["", "## 6. Questions to the assistant (evidence-linked)"]
    for q in r["qa"]:
        L += [f"**Q: {q['question']}**", f"A ({q['statement_type']}; evidence {', '.join(q['evidence_ids'][:6]) or 'none'}): {q['answer'][:600]}", ""]
    L += ["## 7. Not implemented (risk register)", "| ID | Category | Owner | Status |", "|---|---|---|---|"]
    L += [f"| {x['risk_id']} | {x['category']} | {x['owner']} | {x['status']} |" for x in r["risk_register"]]
    L += ["", f"Results hash: `{r['results_hash']}` | Audit chain valid: {r['audit_chain_valid']} | Evidence records: {r['evidence_count']}"]
    return "\n".join(L)


if __name__ == "__main__":
    r = run()
    print(json.dumps({"decisions": r["decisions"], "findings": len(r["findings"]),
                      "planted_detected": f"{sum(a['detected'] for a in r['acceptance'])}/{len(r['acceptance'])}",
                      "hash": r["results_hash"][:16], "audit_ok": r["audit_chain_valid"]}, indent=1))
