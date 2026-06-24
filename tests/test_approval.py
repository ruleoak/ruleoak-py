from ruleoak_py.approval import auto_allow, auto_deny
def test_approval_callbacks():
    assert auto_allow({})["decision"] == "allow"
    assert auto_deny({})["decision"] == "deny"
