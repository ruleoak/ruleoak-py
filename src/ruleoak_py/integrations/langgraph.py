from __future__ import annotations
from typing import Any, Callable, Dict
from ruleoak_py.agentic import FlightRecorder
from ruleoak_py.integrations.generic import wrap_tool
def ruleoak_guarded_node(node: Callable[..., Any], recorder: FlightRecorder | None = None, node_name: str = "langgraph_node", policy: Dict[str, Any] | None = None, approval_callback=None):
    guarded = wrap_tool(lambda state, *a, **kw: node(state, *a, **kw), recorder=recorder or FlightRecorder(actor="langgraph"), tool_name=node_name, operation="node", policy=policy or {"defaultAction":"allow"}, approval_callback=approval_callback)
    def wrapped(state: Dict[str, Any], *args: Any, **kwargs: Any):
        result = guarded(state, *args, **kwargs)
        return result["result"] if isinstance(result, dict) and result.get("executed") else result
    wrapped.ruleoak_recorder = guarded.ruleoak_recorder
    return wrapped
def ruleoak_tool_wrapper(tool: Callable[..., Any], recorder: FlightRecorder | None = None, tool_name: str | None = None, policy: Dict[str, Any] | None = None, approval_callback=None):
    return wrap_tool(tool, recorder=recorder or FlightRecorder(actor="langgraph"), tool_name=tool_name, operation="call", policy=policy or {"defaultAction":"allow"}, approval_callback=approval_callback)
def ruleoak_checkpoint_evidence(recorder: FlightRecorder, path):
    recorder.write_jsonl(path)
    return path
