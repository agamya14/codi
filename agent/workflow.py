from pathlib import Path
from typing import Dict, Any

from .bug_detector import detect_bugs
from .complexity import analyze_complexity
from .file_loader import read_python_file
from .fix_suggester import suggest_fixes
from .parser import parse_source
from .runner import execute_tests, run_python_file
from .test_generator import generate_edge_tests, write_test_module
from .flashapi_client import GeminiFlashClient


class LangGraphWorkflow:
    def __init__(self, use_flashapi: bool = False):
        self.use_flashapi = use_flashapi
        self.flash = GeminiFlashClient() if use_flashapi else None

    def run_full_analysis(self, path: Path) -> Dict[str, Any]:
        source = read_python_file(path)
        tree = parse_source(source)
        bug_reports = detect_bugs(tree, source)
        complexity = analyze_complexity(tree)
        tests = generate_edge_tests(tree)

        test_module = path.parent / f"test_{path.stem}_generated.py"
        if tests:
            write_test_module(tests, str(test_module))
            test_results = execute_tests(str(test_module))
        else:
            test_results = {"exit_code": 0, "stdout": "No generated tests.", "stderr": ""}

        fix_suggestions = suggest_fixes(source, bug_reports)
        summary = {
            "file": str(path),
            "bugs": [vars(report) for report in bug_reports],
            "complexity": {
                "function": complexity.function_name,
                "estimate": complexity.complexity,
                "details": complexity.details,
            },
            "generated_tests": [test for test in tests],
            "test_results": test_results,
            "fix_suggestions": fix_suggestions,
        }

        if self.use_flashapi and self.flash and self.flash.is_configured():
            summary["gemini_explanation"] = self.flash.explain_issue(
                "Review the code analysis and provide improvements.", source
            )

        return {"summary": summary}
