from pathlib import Path
from typing import List


def find_python_files(path: Path, recursive: bool = True) -> List[Path]:
    if path.is_file() and path.suffix == ".py":
        return [path]

    if path.is_dir():
        pattern = "**/*.py" if recursive else "*.py"
        return sorted(path.glob(pattern))

    return []


def read_python_file(path: Path) -> str:
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()
