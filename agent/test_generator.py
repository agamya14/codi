import ast
from typing import List


def default_test_value(annotation: ast.expr | None) -> str:
    if isinstance(annotation, ast.Name):
        name = annotation.id
        if name == "int":
            return "0"
        if name == "str":
            return '""'
        if name == "bool":
            return "False"
    return "None"


def generate_edge_tests(tree: ast.Module) -> List[str]:
    tests: List[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            arg_names = [arg.arg for arg in node.args.args]
            if not arg_names:
                continue

            arg_values = []
            for arg in node.args.args:
                annotation = arg.annotation
                arg_values.append(default_test_value(annotation))

            test_name = f"test_{node.name}_edge_case"
            args = ", ".join(arg_values)
            tests.append(
                f"def {test_name}():\n"
                f"    assert {node.name}({args}) is not None\n"
            )
    return tests


def write_test_module(
    tests: List[str],
    path: str,
    module_name: str,
    function_names: List[str],
) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("import pytest\n")

        if function_names:
            imports = ", ".join(function_names)
            handle.write(f"from {module_name} import {imports}\n\n")

        for item in tests:
            handle.write(item)
            handle.write("\n\n")