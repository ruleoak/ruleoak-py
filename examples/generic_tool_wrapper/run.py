from ruleoak_py.integrations.generic import wrap_tool
def search(q): return {"q": q}
print(wrap_tool(search)("ruleoak"))
