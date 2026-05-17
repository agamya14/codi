import ast
from dataclasses import dataclass
from typing import List


@dataclass
class ComplexityAnalysis:
    function_name: str
    complexity: str
    details: List[str]

    def __str__(self) -> str:
        summary = [f"Function: {self.function_name}", f"Estimated complexity: {self.complexity}"]
        summary.extend(self.details)
        return "\n".join(summary)


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.details: List[str] = []
        self.loop_count = 0
        self.nested_depth = 0
        self.max_depth = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.loop_count = 0
        self.nested_depth = 0
        self.max_depth = 0
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.loop_count += 1
        self.nested_depth += 1
        self.max_depth = max(self.max_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_While(self, node: ast.While):
        self.loop_count += 1
        self.nested_depth += 1
        self.max_depth = max(self.max_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1

    def visit_If(self, node: ast.If):
        self.nested_depth += 1
        self.max_depth = max(self.max_depth, self.nested_depth)
        self.generic_visit(node)
        self.nested_depth -= 1


def analyze_complexity(tree: ast.Module) -> ComplexityAnalysis:
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if not functions:
        return ComplexityAnalysis(function_name="<module>", complexity="O(1)", details=["No top-level functions found."])

    first = functions[0]
    visitor = ComplexityVisitor()
    visitor.visit(first)

    if visitor.max_depth >= 3 and visitor.loop_count >= 2:
        complexity = "O(n^2) or higher"
    elif visitor.loop_count >= 1:
        complexity = "O(n)"
    else:
        complexity = "O(1)"

    details = [f"Loops: {visitor.loop_count}", f"Max nesting depth: {visitor.max_depth}"]
    return ComplexityAnalysis(function_name=first.name, complexity=complexity, details=details)
