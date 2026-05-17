import ast
from dataclasses import dataclass, field
from typing import List


@dataclass
class CodeMetadata:
    functions: List[str] = field(default_factory=list)
    classes: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    assignments: List[str] = field(default_factory=list)
    nodes: ast.AST = None


class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.metadata = CodeMetadata()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.metadata.functions.append(node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self.metadata.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self.metadata.classes.append(node.name)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.metadata.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module = node.module or ""
        for alias in node.names:
            self.metadata.imports.append(f"{module}.{alias.name}" if module else alias.name)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if hasattr(target, "id"):
                self.metadata.assignments.append(target.id)
        self.generic_visit(node)


def parse_source(source: str) -> ast.Module:
    tree = ast.parse(source)
    return tree


def extract_metadata(tree: ast.Module) -> CodeMetadata:
    visitor = CodeVisitor()
    visitor.visit(tree)
    visitor.metadata.nodes = tree
    return visitor.metadata
