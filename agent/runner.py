import subprocess
from pathlib import Path
from typing import Dict, Any


def run_python_file(path: Path, timeout: int = 10) -> Dict[str, Any]:
    try:
        completed = subprocess.run(["python", str(path)], capture_output=True, text=True, timeout=timeout)
        return {
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except subprocess.TimeoutExpired as exc:
        return {"exit_code": -1, "stdout": "", "stderr": f"Timeout after {timeout}s"}


def execute_tests(test_module: str, timeout: int = 20) -> Dict[str, Any]:
    try:
        completed = subprocess.run(["pytest", "-q", test_module], capture_output=True, text=True, timeout=timeout)
        return {
            "exit_code": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": -1, "stdout": "", "stderr": f"Pytest timed out after {timeout}s"}
