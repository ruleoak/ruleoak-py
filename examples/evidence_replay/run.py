from ruleoak_py import FlightRecorder, replay_jsonl_text
r=FlightRecorder(run_id="demo"); r.record("policy_decision", {"decision":"allow"}); print(replay_jsonl_text(r.to_jsonl()))
