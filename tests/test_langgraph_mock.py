from ruleoak_py.integrations.langgraph import ruleoak_guarded_node
def test_langgraph_mock():
    def node(state): return {"ok": state["x"]}
    assert ruleoak_guarded_node(node)({"x":1})["ok"] == 1
