from ruleoak_py import create_action_envelope, evaluate_action
a=create_action_envelope("filesystem","delete",{"path":"/protected"}, risk="high")
print(evaluate_action(a,{"blockedActions":["filesystem.delete"]}))
