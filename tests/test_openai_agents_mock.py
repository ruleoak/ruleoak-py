from ruleoak_py.integrations.openai_agents import wrap_tool
def test_openai_agents_mock():
    def tool(): return 42
    assert wrap_tool(tool)() == 42
