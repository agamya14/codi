from agent.complexity import analyze_complexity
from agent.parser import parse_source


def test_analyze_complexity_simple_function():
    source = """
def greet(name):
    return f'hello {name}'
"""
    tree = parse_source(source)
    result = analyze_complexity(tree)
    assert result.complexity == "O(1)"


def test_analyze_complexity_with_loop():
    source = """
def count_items(items):
    total = 0
    for item in items:
        total += 1
    return total
"""
    tree = parse_source(source)
    result = analyze_complexity(tree)
    assert result.complexity == "O(n)"
