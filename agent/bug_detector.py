import ast
from dataclasses import dataclass
from typing import List


@dataclass
class BugReport:
    location: str
    issue: str
    detail: str


class BugDetector(ast.NodeVisitor):
    def __init__(self, source: str):
        self.source = source.splitlines()
        self.bugs: List[BugReport] = []
        self.imports = set()
        self.used_names = set()
        self.assignments = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict, ast.Set)):  # mutable default arg
                self.bugs.append(BugReport(
                    location=f"{node.name}:{node.lineno}",
                    issue="Mutable default argument",
                    detail="Using a mutable object as a default argument can cause shared state across calls."
                ))
        if not any(isinstance(stmt, ast.Return) for stmt in ast.walk(node)):
            self.bugs.append(BugReport(
                location=f"{node.name}:{node.lineno}",
                issue="Missing return",
                detail="Function may not return a value in all control paths."
            ))
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.type is None:
            self.bugs.append(BugReport(
                location=f"except:{node.lineno}",
                issue="Bare except",
                detail="Catching all exceptions can hide errors and make debugging harder."
            ))
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        if isinstance(node.test, ast.Compare) and len(node.test.ops) == 1:
            compare = node.test.ops[0]
            if isinstance(compare, ast.Is) and isinstance(node.test.comparators[0], ast.Constant) and node.test.comparators[0].value is None:
                self.bugs.append(BugReport(
                    location=f"if:{node.lineno}",
                    issue="Use 'is None' correctly",
                    detail="Prefer 'is None' or 'is not None' when comparing to None."
                ))
        self.generic_visit(node)

    def finalize(self):
        unused = sorted(self.imports - self.used_names)
        for name in unused:
            self.bugs.append(BugReport(
                location=f"import", issue="Unused import", detail=f"'{name}' is imported but never used."))

    def get_reports(self) -> List[BugReport]:
        self.finalize()
        return self.bugs


def detect_bugs(tree: ast.Module, source: str) -> List[BugReport]:
    detector = BugDetector(source)
    detector.visit(tree)
    return detector.get_reports()
