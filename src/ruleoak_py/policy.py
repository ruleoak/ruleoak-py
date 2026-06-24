from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import re

def action_key(action: Dict[str, Any]) -> str:
    if action.get("actionType"):
        return str(action["actionType"])
    if action.get("action_type"):
        return str(action["action_type"])
    if action.get("category"):
        return str(action["category"])
    metadata = action.get("metadata") or {}
    if metadata.get("actionType"):
        return str(metadata["actionType"])
    if metadata.get("action_type"):
        return str(metadata["action_type"])
    if metadata.get("category"):
        return str(metadata["category"])
    return f"{action.get('toolName','unknown')}.{action.get('operation','unknown')}"

def load_policy(path_or_policy: str | Path | Dict[str, Any] | None = None) -> Dict[str, Any]:
    if path_or_policy is None:
        return {"defaultAction": "deny", "allowedActions": [], "approvalRequired": [], "blockedActions": []}
    if isinstance(path_or_policy, dict):
        return path_or_policy
    text = Path(path_or_policy).read_text(encoding="utf-8")
    return json.loads(text)

def normalize_policy_decision(decision: str | None = "needs_approval") -> str:
    raw = str(decision or "needs_approval")
    return {"approval": "needs_approval", "ask": "needs_approval", "block": "deny"}.get(raw, raw)

def pattern_specificity(pattern: str = "") -> int:
    p = str(pattern or "").strip()
    if not p:
        return -1
    if p == "*":
        return 0
    if "*" not in p:
        return 1000 + len([x for x in p.split(".") if x]) * 10 + len(p)
    if p.endswith(".*"):
        return 500 + len([x for x in p[:-2].split(".") if x]) * 10 + len(p)
    return 100 + len(p.replace("*", ""))

def pattern_matches_action(pattern: str = "", key: str = "") -> bool:
    p = str(pattern or "").strip()
    k = str(key or "").strip()
    if not p or not k:
        return False
    if p == "*" or p == k:
        return True
    if p.endswith(".*"):
        return k == p[:-2] or k.startswith(p[:-1])
    if "*" in p:
        return re.match("^" + re.escape(p).replace(r"\*", ".*") + "$", k) is not None
    return False

def matching_patterns(patterns: List[str] | None, key: str) -> List[Dict[str, Any]]:
    matches = [
        {"pattern": p, "specificity": pattern_specificity(p)}
        for p in (patterns or [])
        if pattern_matches_action(p, key)
    ]
    return sorted(matches, key=lambda x: (-x["specificity"], str(x["pattern"])))

def evaluate_action(action: Dict[str, Any], policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
    policy = load_policy(policy)
    key = action_key(action)
    blocked = next(iter(matching_patterns(policy.get("blockedActions", []), key)), None)
    if blocked:
        return {"decision": "deny", "action": key, "matched": blocked["pattern"], "source": "blockedActions", "specificity": blocked["specificity"], "reason": "explicit_deny_wins"}
    allowed = next(iter(matching_patterns(policy.get("allowedActions", []), key)), None)
    approval = next(iter(matching_patterns(policy.get("approvalRequired", []), key)), None)
    if allowed and approval:
        if allowed["specificity"] > approval["specificity"]:
            return {"decision": "allow", "action": key, "matched": allowed["pattern"], "source": "allowedActions", "specificity": allowed["specificity"], "reason": "most_specific_allow"}
        if approval["specificity"] > allowed["specificity"]:
            return {"decision": "needs_approval", "action": key, "matched": approval["pattern"], "source": "approvalRequired", "specificity": approval["specificity"], "reason": "most_specific_approval"}
        return {"decision": "needs_approval", "action": key, "matched": approval["pattern"], "source": "approvalRequired", "specificity": approval["specificity"], "reason": "same_specificity_conflict_needs_approval"}
    if allowed:
        return {"decision": "allow", "action": key, "matched": allowed["pattern"], "source": "allowedActions", "specificity": allowed["specificity"], "reason": "allowed_by_policy"}
    if approval:
        return {"decision": "needs_approval", "action": key, "matched": approval["pattern"], "source": "approvalRequired", "specificity": approval["specificity"], "reason": "approval_required"}
    default = normalize_policy_decision(policy.get("defaultAction") or ("allow" if action.get("risk") == "low" else "deny"))
    if default not in {"allow", "deny", "needs_approval", "dry_run_only"}:
        default = "deny"
    return {"decision": default, "action": key, "matched": "defaultAction", "source": "defaultAction", "reason": f"default_{default}"}
