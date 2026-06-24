import os, subprocess, sys
def _env():
    e=os.environ.copy(); e["PYTHONPATH"] = "src" + os.pathsep + e.get("PYTHONPATH", ""); return e
def test_cli_demo():
    r=subprocess.run([sys.executable,"-m","ruleoak_py.cli","demo","approval-required"], capture_output=True, text=True, env=_env())
    assert r.returncode == 0, r.stderr
    assert "needs_approval" in r.stdout
