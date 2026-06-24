from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
import json
def action_key(action: Dict[str, Any]) -> str:
    return f"{action.get('toolName','unknown')}.{action.get('operation','unknown')}"
def load_policy(path_or_policy: str | Path | Dict[str, Any] | None = None) -> Dict[str, Any]:
    if path_or_policy is None:
        return {"defaultAction": "deny", "allowedActions": [], "approvalRequired": [], "blockedActions": []}
    if isinstance(path_or_policy, dict):
        return path_or_policy
    text = Path(path_or_policy).read_text(encoding="utf-8")
    return json.loads(text)
def evaluate_action(action: Dict[str, Any], policy: Dict[str, Any] | None = None) -> Dict[str, Any]:
    policy = load_policy(policy)
    key = action_key(action)
    if key in policy.get("blockedActions", []):
        return {"decision": "deny", "action": key, "reason": "blocked_by_policy"}
    if key in policy.get("approvalRequired", []):
        return {"decision": "needs_approval", "action": key, "reason": "approval_required"}
    if key in policy.get("allowedActions", []):
        return {"decision": "allow", "action": key, "reason": "allowed_by_policy"}
    if policy.get("defaultAction") == "allow":
        return {"decision": "allow", "action": key, "reason": "default_allow"}
    if policy.get("defaultAction") == "approval":
        return {"decision": "needs_approval", "action": key, "reason": "default_approval"}
    if action.get("risk") == "low":
        return {"decision": "allow", "action": key, "reason": "low_risk_default"}
    return {"decision": "deny", "action": key, "reason": "default_deny"}
