from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List
import json
def replay_jsonl_text(text: str) -> List[Dict[str, Any]]:
    out=[]
    for idx,line in enumerate([ln for ln in text.splitlines() if ln.strip()], start=1):
        ev=json.loads(line)
        out.append({"index": idx, "type": ev.get("type"), "decision": ev.get("payload", {}).get("decision"), "actor": ev.get("actor")})
    return out
def replay_jsonl(path) -> List[Dict[str, Any]]:
    return replay_jsonl_text(Path(path).read_text(encoding="utf-8"))
