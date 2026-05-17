from pathlib import Path

from agent.workflow import LangGraphWorkflow


def test_workflow_runs(tmp_path: Path):
    code_file = tmp_path / "sample.py"
    code_file.write_text("""
import math

def square(n):
    return n * n
""")
    workflow = LangGraphWorkflow()
    result = workflow.run_full_analysis(code_file)
    assert "summary" in result
    summary = result["summary"]
    assert summary["file"] == str(code_file)
    assert isinstance(summary["bugs"], list)
    assert summary["complexity"]["estimate"] == "O(1)"
