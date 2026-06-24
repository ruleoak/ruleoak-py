from ruleoak_py import redact
def test_redaction():
    assert redact({"apiKey":"x"})["apiKey"] == "[REDACTED]"
