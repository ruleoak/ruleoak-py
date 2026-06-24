# ruleoak-py

Python bridge for RuleOak-compatible Evidence JSONL, local flight recording, policy decisions, approval callbacks, redaction, replay, and framework-shaped agent examples.

## Install

```bash
pip install ruleoak-py
```

## Quickstart

```bash
ruleoak-py quickstart
ruleoak-py demo approval-required
```

## Code

```python
from ruleoak_py import FlightRecorder, create_action_envelope, evaluate_action
rec = FlightRecorder(run_id="demo")
action = create_action_envelope("filesystem", "delete", {"path": "/protected"}, risk="high")
print(evaluate_action(action, {"blockedActions": ["filesystem.delete"]}))
```

Framework-shaped examples are mock-friendly and offline. They do not claim production integration with optional frameworks unless you add those dependencies.

Apache-2.0. Copyright 2026 Sun Shaobin and RuleOak contributors. Contact: hello@ruleoak.com.
