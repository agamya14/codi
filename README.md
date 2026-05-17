# PyAgent

A modular Python AI coding agent that reads Python files, detects bugs, explains issues, analyzes time complexity, generates edge tests, runs code automatically, and suggests fixes.

## Features

- Read and parse Python sources with AST
- Detect common bugs and code smells
- Explain issues with natural language output
- Estimate time complexity of functions
- Generate edge-case pytest scenarios
- Execute code and tests automatically
- Suggest bug fixes and improvement strategies
- Orchestrate analysis with a LangGraph-style workflow
- Provide a rich CLI powered by `rich`

## Installation

```bash
python -m pip install -e .
```

## Environment variables

Create a `.env` file in the project root with:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_FLASHAPI_ENDPOINT=https://flashapi.googleapis.com/v1beta/generateText
```

The agent will load `.env` automatically on startup.

## Usage

```bash
python -m agent.cli analyze path/to/file.py
python -m agent.cli workflow path/to/file.py
```

## Development

Run tests with:

```bash
pytest
```
