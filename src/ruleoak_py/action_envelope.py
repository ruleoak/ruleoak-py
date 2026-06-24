from __future__ import annotations
from typing import Any, Dict
def create_action_envelope(tool_name: str = "unknown", operation: str = "unknown", input: Dict[str, Any] | None = None, target: Any = None, risk: str | None = None, metadata: Dict[str, Any] | None = None) -> Dict[str, Any]:
    text = f"{tool_name}.{operation} {input or {}}".lower()
    inferred = "high" if any(x in text for x in ["delete", "drop", "rm -rf", "secret", "token", "password", "send", "mutate", "write", "install"]) else "low"
    return {"schemaVersion": "ruleoak.action_envelope.v1", "toolName": tool_name, "operation": operation, "input": input or {}, "target": target, "risk": risk or inferred, "metadata": {"adapter": "ruleoak-py", **(metadata or {})}}
