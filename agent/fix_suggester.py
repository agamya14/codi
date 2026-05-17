from typing import List

from .bug_detector import BugReport
from .flashapi_client import GeminiFlashClient


def suggest_fixes(source: str, bug_reports: List[BugReport]) -> List[str]:
    suggestions: List[str] = []
    for bug in bug_reports:
        if bug.issue == "Mutable default argument":
            suggestions.append("Replace mutable default arguments with None and initialize inside the function.")
        elif bug.issue == "Bare except":
            suggestions.append("Specify the exception type instead of using a bare except. Use `except Exception:` or specific exception classes.")
        elif bug.issue == "Unused import":
            suggestions.append(f"Remove the unused import {bug.detail} or use it in the module.")
        elif bug.issue == "Missing return":
            suggestions.append("Ensure the function returns a value on all control paths or explicitly return None.")
        else:
            suggestions.append(f"Review the code at {bug.location}: {bug.detail}")

    if not suggestions:
        suggestions.append("No fix suggestions were found; the code appears structurally clean.")

    client = GeminiFlashClient()
    explanation = client.explain_issue("\n".join(suggestions), source)
    if explanation:
        suggestions.append("[Gemini] " + explanation)

    return suggestions
