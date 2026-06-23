# ruleoak-py v1.0.0

Python adapters and bridge utilities for adding RuleOak permission, approval, evidence, and replay to Python agentic workflows.

## Use this repo when you need

- Evidence JSONL v1 helpers
- local flight recording in Python
- LangGraph-style integration helpers
- OpenAI Agents Python-style integration helpers
- CrewAI / AutoGen / LlamaIndex / Semantic Kernel-style adapter patterns
- local, mockable tests with no live LLM calls

## Public repository

- GitHub: https://github.com/ruleoak/ruleoak-py
- Version: `1.0.0`
- License: `Apache-2.0`

## Relationship to RuleOak Core

`ruleoak-py` is an adapter/bridge package. RuleOak Core remains the full Agent Firewall + Flight Recorder runtime and is licensed under `AGPL-3.0-or-later` with commercial licensing available.

## Install locally

```bash
pip install -e .
python -m pytest
```

## Quickstart

```bash
python -m ruleoak_py.cli quickstart
```

## License

Apache-2.0. See `LICENSE`.
