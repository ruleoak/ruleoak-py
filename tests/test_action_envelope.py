from ruleoak_py import create_action_envelope
def test_action_envelope():
    a=create_action_envelope("x","y",{})
    assert a["schemaVersion"] == "ruleoak.action_envelope.v1"
