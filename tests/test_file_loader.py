from pathlib import Path

from agent.file_loader import find_python_files, read_python_file


def test_find_python_files(tmp_path: Path):
    file = tmp_path / "example.py"
    file.write_text("print('hello')\n")

    found = find_python_files(tmp_path)
    assert file in found


def test_read_python_file(tmp_path: Path):
    file = tmp_path / "example.py"
    content = "x = 1\n"
    file.write_text(content)
    assert read_python_file(file) == content
