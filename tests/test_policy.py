from ruleoak_py import create_action_envelope, evaluate_action
def test_policy_deny():
    a=create_action_envelope("filesystem","delete",{}, risk="high")
    assert evaluate_action(a,{"blockedActions":["filesystem.delete"]})["decision"] == "deny"
