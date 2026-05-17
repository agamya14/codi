from agent.bug_detector import detect_bugs
from agent.parser import parse_source


def test_detect_mutable_default_argument():
    source = """
def add_item(x, items=[]):
    items.append(x)
    return items
"""
    tree = parse_source(source)
    reports = detect_bugs(tree, source)
    assert any(report.issue == "Mutable default argument" for report in reports)


def test_detect_unused_import():
    source = """
import sys

def foo():
    return 1
"""
    tree = parse_source(source)
    reports = detect_bugs(tree, source)
    assert any(report.issue == "Unused import" for report in reports)
