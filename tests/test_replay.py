from ruleoak_py import FlightRecorder, replay_jsonl_text
def test_replay():
    r=FlightRecorder(run_id="x"); r.record("policy_decision", {"decision":"allow"}); assert replay_jsonl_text(r.to_jsonl())[0]["type"] == "policy_decision"
