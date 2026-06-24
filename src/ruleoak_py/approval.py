from __future__ import annotations
from typing import Any, Dict, Callable
def auto_deny(request: Dict[str, Any]) -> Dict[str, Any]:
    return {"decision": "deny", "reason": "auto_deny", "request": request}
def auto_allow(request: Dict[str, Any]) -> Dict[str, Any]:
    return {"decision": "allow", "reason": "auto_allow", "request": request}
def create_static_approval(decision: str = "deny") -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    return auto_allow if decision == "allow" else auto_deny
