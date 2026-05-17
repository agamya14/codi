import ast

from agent.parser import extract_metadata, parse_source


def test_parse_source_and_metadata():
    source = """
import os

def greet(name):
    return f'hello {name}'
"""
    tree = parse_source(source)
    metadata = extract_metadata(tree)

    assert isinstance(tree, ast.Module)
    assert metadata.functions == ["greet"]
    assert "os" in metadata.imports
