"""Benchmark (Faisal's comparison): place this bank's own policy values next to the regulator and peers, using the
master-rulebook comparison data. Same labelling logic as master-rulebook (5% band around the peer median)."""
import csv, statistics
from pathlib import Path

# which master-rulebook row each of OUR policy values corresponds to (param_id -> rule id in packs)
MAPPING = {"UAE": {"UAE-PL-05": "CRED.PL.001", "UAE-HL-02": "CRED.HL.001"},
           "UK": {"UK-HL-02": "BANK.UK.LTI.001"},
           "US": {}}


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def label(v, peers, cap, direction, kind, t=0.05):
    if v is None or kind == "info":
        return ""
    if cap is not None:
        if (v > cap) if direction == "higher" else (v < cap):
            return "Above rule limit"
        if v == cap:
            return "At rule limit"
    nums = [p for p in peers if p is not None]
    if len(nums) < 2:
        return "No peer data"
    m = statistics.median(nums)
    if (v > m * (1 + t)) if direction == "higher" else (v < m * (1 - t)):
        return {"risk": "Higher risk", "price": "Cheaper", "outcome": "Worse"}[kind]
    if (v < m * (1 - t)) if direction == "higher" else (v > m * (1 + t)):
        return {"risk": "Too rigid", "price": "More expensive", "outcome": "Better"}[kind]
    return "In line"


def position(rules: list, master_dir: Path) -> list:
    by_id = {r["id"]: r for r in rules}
    out = []
    for market, mp in MAPPING.items():
        f = master_dir / f"compare_{market.lower()}.csv"
        if not f.exists() or not mp:
            continue
        rows = list(csv.reader(open(f, encoding="utf-8")))
        head, data = rows[0], rows[1:]
        banks = head[7:11]
        for row in data:
            r = dict(zip(head, row))
            if r["param_id"] not in mp:
                continue
            ours = by_id[mp[r["param_id"]]]["limit"]
            peers = [_num(r[b]) for b in banks]
            out.append({"market": market, "param_id": r["param_id"], "measure": r["parameter"], "ours": ours,
                        "peers": dict(zip(banks, peers)), "peer_median": statistics.median([p for p in peers if p is not None]),
                        "regulator_rule": r["reg_rule"],
                        "label": label(ours, peers, _num(r["reg_cap"]), r["direction"], r["kind"]),
                        "evidence": f"master-rulebook/data/{f.name}#{r['param_id']}; rule {mp[r['param_id']]}"})
    return out
