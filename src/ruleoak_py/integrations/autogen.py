from __future__ import annotations
from typing import Any, Callable, Dict
from ruleoak_py.integrations.generic import wrap_tool as _wrap
def wrap_tool(tool: Callable[..., Any], recorder=None, tool_name: str | None = None, dry_run: bool = False, policy: Dict[str, Any] | None = None, approval_callback=None):
    if dry_run:
        policy = policy or {"defaultAction": "approval", "approvalRequired": [f"{tool_name or getattr(tool, '__name__', 'tool')}.call"]}
    guarded = _wrap(tool, recorder=recorder, tool_name=tool_name, operation="call", policy=policy or {"defaultAction":"allow"}, approval_callback=approval_callback)
    def wrapped(*args: Any, **kwargs: Any):
        result = guarded(*args, **kwargs)
        return result["result"] if isinstance(result, dict) and result.get("executed") else result
    wrapped.ruleoak_recorder = guarded.ruleoak_recorder
    return wrapped
