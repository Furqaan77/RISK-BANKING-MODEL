"""Acceptance tests (AD-18, AD-19, AD-22). Run: python -m pytest tests  (or: python tests/test_answer_sheet.py)"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import run_demo
from riskplatform.core.policy import compile_condition


def test_all_planted_problems_detected():
    r = run_demo.run(write=False)
    missed = [a for a in r["acceptance"] if not a["detected"]]
    assert not missed, missed


def test_reproducible():
    assert run_demo.run(write=False)["results_hash"] == run_demo.run(write=False)["results_hash"]


def test_no_double_counting_of_duplicates():
    r = run_demo.run(write=False)
    assert r["dq"]["rows_in"] - r["dq"]["rows_out"] == 2
    assert not r["dq"]["reconciliation"], r["dq"]["reconciliation"]


def test_assistant_refuses_without_evidence():
    r = run_demo.run(write=False)
    off = [q for q in r["qa"] if "favourite colour" in q["question"]][0]
    assert off["evidence_ids"] == [] and "cannot answer" in off["answer"]
    vendor = [q for q in r["qa"] if "vendor" in q["question"]][0]
    assert vendor["statement_type"] == "missing"


def test_rules_are_data_not_code():
    for bad in ["__import__('os').system('x')", "open('f')", "a.b > 1"]:
        try:
            compile_condition(bad)
            assert False, bad
        except ValueError:
            pass


def test_audit_chain():
    assert run_demo.run(write=False)["audit_chain_valid"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("PASS", name)
