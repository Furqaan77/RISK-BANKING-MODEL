"""Append-only, hash-chained audit log (AD-11). Each line: seq, actor, action, payload_hash, prev_hash, hash."""
import hashlib, json
from pathlib import Path


def _h(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


class AuditLog:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("")          # one log per run in the skeleton; production = append-only store
        self.prev, self.seq = "GENESIS", 0

    def record(self, actor: str, action: str, payload) -> str:
        self.seq += 1
        ph = _h(json.dumps(payload, sort_keys=True, default=str))
        entry = {"seq": self.seq, "actor": actor, "action": action, "payload_hash": ph, "prev_hash": self.prev}
        entry["hash"] = _h(json.dumps(entry, sort_keys=True))
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        self.prev = entry["hash"]
        return entry["hash"]


def verify(path: Path) -> bool:
    prev = "GENESIS"
    for line in open(path, encoding="utf-8"):
        e = json.loads(line)
        h = e.pop("hash")
        if e["prev_hash"] != prev or _h(json.dumps(e, sort_keys=True)) != h:
            return False
        prev = h
    return True
