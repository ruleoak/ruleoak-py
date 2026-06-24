from __future__ import annotations
from typing import Any, Callable, Dict
from ruleoak_py.agentic import FlightRecorder
from ruleoak_py.action_envelope import create_action_envelope
from ruleoak_py.policy import evaluate_action
from ruleoak_py.redaction import redact
def wrap_tool(tool: Callable[..., Any], recorder: FlightRecorder | None = None, tool_name: str | None = None, operation: str = "call", policy: Dict[str, Any] | None = None, approval_callback: Callable[[Dict[str, Any]], Dict[str, Any]] | None = None):
    recorder = recorder or FlightRecorder(actor="generic-python-agent")
    name = tool_name or getattr(tool, "__name__", "tool")
    def wrapped(*args: Any, **kwargs: Any):
        action = create_action_envelope(name, operation, {"args": list(args), "kwargs": redact(kwargs)})
        recorder.record("action_requested", action)
        decision = evaluate_action(action, policy or {"defaultAction": "allow"})
        if decision["decision"] == "needs_approval" and approval_callback:
            approval = approval_callback({"action": action, "decision": decision})
            decision = {**decision, "decision": "allow" if approval.get("decision") == "allow" else "deny", "approval": approval}
        recorder.record("policy_decision", decision)
        if decision["decision"] != "allow":
            return {"executed": False, "decision": decision}
        result = tool(*args, **kwargs)
        recorder.record("action_executed", {"toolName": name, "result": result})
        return {"executed": True, "decision": decision, "result": result}
    wrapped.ruleoak_recorder = recorder
    return wrapped
