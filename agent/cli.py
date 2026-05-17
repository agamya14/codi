import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .bug_detector import detect_bugs
from .complexity import analyze_complexity
from .file_loader import find_python_files, read_python_file
from .fix_suggester import suggest_fixes
from .flashapi_client import GeminiFlashClient
from .parser import parse_source
from .runner import execute_tests, run_python_file
from .test_generator import generate_edge_tests
from .workflow import LangGraphWorkflow

console = Console()


def print_bugs(bug_reports):
    if not bug_reports:
        console.print("[bold green]No obvious issues detected.[/]")
        return

    table = Table(title="Bug Reports", show_lines=True)
    table.add_column("Location", style="cyan")
    table.add_column("Issue", style="magenta")
    table.add_column("Detail", style="white")

    for bug in bug_reports:
        table.add_row(bug.location, bug.issue, bug.detail)

    console.print(table)


def analyze_file(path: Path):
    source = read_python_file(path)
    tree = parse_source(source)
    bug_reports = detect_bugs(tree, source)
    complexity = analyze_complexity(tree)
    tests = generate_edge_tests(tree)

    console.print(Panel(f"Analysis for [bold]{path}[/]", style="bold blue"))
    print_bugs(bug_reports)
    console.print(Panel(str(complexity), title="Complexity Summary", style="green"))

    if tests:
        console.print(Panel("Generated edge tests are available via the workflow command.", style="yellow"))
    else:
        console.print(Panel("No edge tests could be inferred from the file.", style="yellow"))


def execute_workflow(path: Path, use_flashapi: bool = False):
    workflow = LangGraphWorkflow(use_flashapi=use_flashapi)
    result = workflow.run_full_analysis(path)

    console.print(Panel(f"Workflow results for [bold]{path}[/]", style="bold blue"))
    console.print(result.get("summary", "No summary available."))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="PyAgent: AI coding analysis agent")
    parser.add_argument("command", choices=["analyze", "run", "suggest-fix", "generate-tests", "workflow"], help="Action to perform")
    parser.add_argument("path", help="Path to a Python file")
    parser.add_argument("--flashapi", action="store_true", help="Use Gemini FlashAPI for natural language explanations")
    args = parser.parse_args(argv or sys.argv[1:])

    path = Path(args.path)
    if not path.exists():
        console.print(f"[bold red]Error:[/] Path does not exist: {path}")
        raise SystemExit(1)

    if args.command == "analyze":
        analyze_file(path)
    elif args.command == "run":
        result = run_python_file(path)
        console.print(Panel(str(result), title="Execution Result", style="blue"))
    elif args.command == "suggest-fix":
        source = read_python_file(path)
        tree = parse_source(source)
        bug_reports = detect_bugs(tree, source)
        suggestions = suggest_fixes(source, bug_reports)
        console.print(Panel("\n".join(suggestions) if suggestions else "No suggestions available.", title="Fix Suggestions", style="green"))
    elif args.command == "generate-tests":
        source = read_python_file(path)
        tree = parse_source(source)
        tests = generate_edge_tests(tree)
        for test in tests:
            console.print(Panel(test, title="Generated Test", style="cyan"))
    elif args.command == "workflow":
        execute_workflow(path, use_flashapi=args.flashapi)


if __name__ == "__main__":
    main()
