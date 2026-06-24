from ruleoak_py import create_action_envelope, evaluate_action
a=create_action_envelope("email","send",{"to":"outside@example.com"}, risk="high")
print(evaluate_action(a,{"approvalRequired":["email.send"]}))
