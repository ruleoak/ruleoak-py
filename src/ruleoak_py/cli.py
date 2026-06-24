from __future__ import annotations
import argparse, json
from pathlib import Path
from .agentic import FlightRecorder, validate_evidence_jsonl_text, read_evidence_jsonl
from .policy import load_policy, evaluate_action
from .action_envelope import create_action_envelope
from .redaction import redact
from .replay import replay_jsonl
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="ruleoak-py")
    sub = parser.add_subparsers(dest="cmd", required=True)
    val = sub.add_parser("validate-evidence"); val.add_argument("path")
    sub.add_parser("quickstart")
    replay = sub.add_parser("replay"); replay.add_argument("path")
    evalp = sub.add_parser("evaluate-action"); evalp.add_argument("path"); evalp.add_argument("--policy")
    red = sub.add_parser("redact"); red.add_argument("path")
    demo = sub.add_parser("demo"); demo.add_argument("name", choices=["approval-required", "policy-deny"])
    args = parser.parse_args(argv)
    if args.cmd == "quickstart":
        rec = FlightRecorder(run_id="py-quickstart"); rec.start_run({"purpose":"quickstart"}); rec.record("action_requested", {"toolName":"search","operation":"read","apiKey":"SHOULD_REDACT"}); rec.record("policy_decision", {"decision":"allow","risk":"low"}); rec.finish_run({"ok": True}); print(rec.to_jsonl(), end=""); return 0
    if args.cmd == "validate-evidence":
        result = validate_evidence_jsonl_text(Path(args.path).read_text(encoding="utf-8")); print(json.dumps(result, indent=2)); return 0 if result["ok"] else 1
    if args.cmd == "replay":
        print(json.dumps(replay_jsonl(args.path), indent=2)); return 0
    if args.cmd == "evaluate-action":
        action = json.loads(Path(args.path).read_text(encoding="utf-8")); policy = load_policy(args.policy) if args.policy else {"defaultAction":"approval"}; print(json.dumps(evaluate_action(action, policy), indent=2)); return 0
    if args.cmd == "redact":
        print(json.dumps(redact(json.loads(Path(args.path).read_text(encoding="utf-8"))), indent=2)); return 0
    if args.cmd == "demo":
        action = create_action_envelope("email", "send", {"to":"outside@example.com"}, risk="high") if args.name == "approval-required" else create_action_envelope("filesystem", "delete", {"path":"/protected"}, risk="high")
        policy = {"defaultAction":"deny", "approvalRequired":["email.send"], "blockedActions":["filesystem.delete"]}
        print(json.dumps(evaluate_action(action, policy), indent=2)); return 0
    return 2
if __name__ == "__main__": raise SystemExit(main())
