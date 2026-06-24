from ruleoak_py.policy import evaluate_action, pattern_specificity, pattern_matches_action

def test_policy_specificity_and_catch_all():
    assert pattern_matches_action("filesystem.*", "filesystem.read")
    assert pattern_specificity("filesystem.read") > pattern_specificity("filesystem.*") > pattern_specificity("*")
    p1={"defaultAction":"deny","allowedActions":["filesystem.read"],"approvalRequired":["filesystem.*"],"blockedActions":[]}
    assert evaluate_action({"toolName":"filesystem","operation":"read"},p1)["decision"] == "allow"
    assert evaluate_action({"toolName":"filesystem","operation":"write"},p1)["decision"] == "needs_approval"
    p2={"defaultAction":"deny","allowedActions":["*"],"approvalRequired":["database.*"],"blockedActions":[]}
    assert evaluate_action({"toolName":"search","operation":"read"},p2)["decision"] == "allow"
    assert evaluate_action({"toolName":"database","operation":"query"},p2)["decision"] == "needs_approval"
    p3={"defaultAction":"allow","allowedActions":["filesystem.delete"],"approvalRequired":["filesystem.delete"],"blockedActions":["filesystem.delete"]}
    assert evaluate_action({"toolName":"filesystem","operation":"delete"},p3)["decision"] == "deny"
    p4={"defaultAction":"deny","allowedActions":["mcp.*"],"approvalRequired":["mcp.*"],"blockedActions":[]}
    assert evaluate_action({"toolName":"mcp","operation":"tool_call"},p4)["decision"] == "needs_approval"
